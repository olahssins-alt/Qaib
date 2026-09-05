// Renders QuickAIBook_ad_30s_single.html to synced video frames (PNG) and
// an offline-rendered audio.wav, in a single real-time browser pass.
//
// AUDIO: AudioEngine.prototype.init is monkey-patched (before the page's
// own "play" click handler ever calls it) to point `this.ctx` at a thin
// wrapper around a real OfflineAudioContext instead of a live AudioContext.
// The wrapper's `currentTime` getter reports real elapsed wall-clock
// seconds since init() was called — exactly what a live AudioContext would
// report — so every oscillator/gain/filter node the app schedules lands at
// the correct time in the offline graph. Nothing is played through actual
// audio hardware; at the end we call startRendering() to deterministically
// render the whole buffer non-realtime and encode it to WAV.
//
// VIDEO: while that same real-time playthrough runs, we screenshot the
// #stage element on a 30fps cadence synced to actual elapsed time.

const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..');
const HTML_PATH = path.join(ROOT, 'QuickAIBook_ad_30s_single.html');
const FRAMES_DIR = path.join(ROOT, '.render', 'frames');
const AUDIO_PATH = path.join(ROOT, '.render', 'audio.wav');

const FPS = 30;
const AD_DURATION_MS = 70800; // AD_CONFIG.totalDurationMs
const TAIL_MS = 500;          // small safety buffer for trailing sound/hold
const OVERRIDE_MS = process.argv[2] ? parseInt(process.argv[2], 10) : null;
const CAPTURE_MS = OVERRIDE_MS || (AD_DURATION_MS + TAIL_MS);
const FRAME_COUNT = Math.round((CAPTURE_MS / 1000) * FPS);

const TARGET_W = 2160; // 4K vertical (2160x3840, the 9:16 UHD equivalent)
const CSS_W = 390; // #frame's fixed CSS width
const SCALE = TARGET_W / CSS_W;

async function main() {
  fs.rmSync(FRAMES_DIR, { recursive: true, force: true });
  fs.mkdirSync(FRAMES_DIR, { recursive: true });

  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--autoplay-policy=no-user-gesture-required'],
  });
  const page = await browser.newPage({
    viewport: { width: CSS_W, height: 900 },
    deviceScaleFactor: SCALE,
  });

  const pageErrors = [];
  page.on('pageerror', (err) => pageErrors.push(String(err)));
  page.on('console', (msg) => {
    if (msg.type() === 'error' && !/ERR_CONNECTION_RESET|ERR_INTERNET_DISCONNECTED/.test(msg.text())) {
      pageErrors.push(msg.text());
    }
  });

  await page.goto('file://' + HTML_PATH);

  // Redirect AudioEngine's real-time output into an OfflineAudioContext.
  await page.evaluate((captureSeconds) => {
    const sampleRate = 44100;
    const offline = new OfflineAudioContext(2, Math.ceil(sampleRate * captureSeconds), sampleRate);
    window.__offlineCtx = offline;

    class FakeCtx {
      constructor(real) {
        this._real = real;
        this._t0 = performance.now();
      }
      get currentTime() { return (performance.now() - this._t0) / 1000; }
      get destination() { return this._real.destination; }
      get sampleRate() { return this._real.sampleRate; }
      createGain() { return this._real.createGain(); }
      createOscillator() { return this._real.createOscillator(); }
      createBuffer(...a) { return this._real.createBuffer(...a); }
      createBufferSource() { return this._real.createBufferSource(); }
      createBiquadFilter() { return this._real.createBiquadFilter(); }
    }

    // AudioEngine is a top-level class declared outside the page's IIFE,
    // so it's reachable here even though the actual `audio` instance is
    // closed over privately. Patching the prototype method redirects that
    // private instance's init() call without needing to reach it directly.
    AudioEngine.prototype.init = function () {
      this.ctx = new FakeCtx(offline);
      this.master = this.ctx.createGain();
      this.master.gain.value = 0.6;
      this.master.connect(this.ctx.destination);
    };

    // Under CDP virtual time, the `now` timestamp requestAnimationFrame
    // hands its callback does NOT track the virtual clock (it keeps
    // advancing in real wall-clock time) even though explicit
    // performance.now() calls do. Both Timeline.start()'s elapsed-time math
    // and animateCounter()'s counting animation trust that argument, so
    // under virtual time they'd race far ahead of the intended schedule
    // (a whole scene reached per real second spent screenshotting). Fix
    // every such call site at once by overriding the global rAF to hand
    // callbacks a performance.now()-derived timestamp instead of the
    // native one.
    const nativeRAF = window.requestAnimationFrame.bind(window);
    window.requestAnimationFrame = (cb) => nativeRAF(() => cb(performance.now()));
  }, CAPTURE_MS / 1000);

  // Screenshotting #stage at 1080x1920 takes far longer per-frame (measured
  // ~0.5s) than a 33ms/frame real-time budget allows, which would otherwise
  // badly desync frames from the page's real-time clock (performance.now()
  // keeps advancing while we're busy encoding a screenshot). Decouple frame
  // capture speed from the page's clock entirely with CDP virtual time:
  // freeze it, advance it by exactly one frame interval, screenshot while
  // it's frozen (however long that takes in real wall-clock time), repeat.
  // performance.now()/rAF/CSS transitions/setTimeout all key off this same
  // virtual clock, so the FakeCtx audio timestamps stay in lockstep too.
  const client = await page.context().newCDPSession(page);
  await client.send('Emulation.setVirtualTimePolicy', { policy: 'pause' });

  await page.click('#playOverlay');
  const stage = await page.$('#stage');

  const frameIntervalMs = 1000 / FPS;
  const t0 = Date.now();
  for (let i = 0; i < FRAME_COUNT; i++) {
    const expired = new Promise((resolve) => client.once('Emulation.virtualTimeBudgetExpired', resolve));
    await client.send('Emulation.setVirtualTimePolicy', { policy: 'advance', budget: frameIntervalMs });
    await expired;
    await stage.screenshot({ path: path.join(FRAMES_DIR, `frame-${String(i + 1).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 96 });
    if ((i + 1) % 100 === 0) console.log(`  frame ${i + 1}/${FRAME_COUNT} (${Math.round((Date.now() - t0) / 1000)}s real elapsed)`);
  }

  console.log(`Captured ${FRAME_COUNT} frames (virtual time) over ${(Date.now() - t0)}ms real time.`);

  // Virtual time is left paused after the last budget expires, which
  // freezes the renderer's task queue — startRendering()'s completion is
  // delivered via that same queue, so it would hang forever otherwise.
  // Let time run freely again before touching the OfflineAudioContext.
  await client.send('Emulation.setVirtualTimePolicy', { policy: 'advance' });

  const wavBase64 = await page.evaluate(async () => {
    const rendered = await window.__offlineCtx.startRendering();

    function encodeWav(buf) {
      const numChan = buf.numberOfChannels;
      const sr = buf.sampleRate;
      const numFrames = buf.length;
      const blockAlign = numChan * 2;
      const dataSize = numFrames * blockAlign;
      const ab = new ArrayBuffer(44 + dataSize);
      const view = new DataView(ab);
      const writeStr = (off, s) => { for (let i = 0; i < s.length; i++) view.setUint8(off + i, s.charCodeAt(i)); };
      writeStr(0, 'RIFF'); view.setUint32(4, 36 + dataSize, true); writeStr(8, 'WAVE');
      writeStr(12, 'fmt '); view.setUint32(16, 16, true); view.setUint16(20, 1, true);
      view.setUint16(22, numChan, true); view.setUint32(24, sr, true);
      view.setUint32(28, sr * blockAlign, true); view.setUint16(32, blockAlign, true);
      view.setUint16(34, 16, true); writeStr(36, 'data'); view.setUint32(40, dataSize, true);
      const chans = []; for (let c = 0; c < numChan; c++) chans.push(buf.getChannelData(c));
      let o = 44;
      for (let i = 0; i < numFrames; i++) {
        for (let c = 0; c < numChan; c++) {
          let s = Math.max(-1, Math.min(1, chans[c][i]));
          s = s < 0 ? s * 0x8000 : s * 0x7fff;
          view.setInt16(o, s, true); o += 2;
        }
      }
      return ab;
    }

    const wavBuf = encodeWav(rendered);
    const bytes = new Uint8Array(wavBuf);
    let binary = '';
    const chunk = 0x8000;
    for (let i = 0; i < bytes.length; i += chunk) binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
    return btoa(binary);
  });

  fs.writeFileSync(AUDIO_PATH, Buffer.from(wavBase64, 'base64'));
  console.log('Wrote', AUDIO_PATH, fs.statSync(AUDIO_PATH).size, 'bytes');

  console.log('Page errors:', pageErrors.length ? pageErrors : 'none');

  await browser.close();

  if (pageErrors.length) process.exitCode = 1;
}

main().catch((err) => { console.error(err); process.exit(1); });
