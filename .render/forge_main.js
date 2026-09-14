class World {
  constructor(canvas) {
    this.renderer = new T.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
    this.renderer.outputColorSpace = T.SRGBColorSpace;
    this.renderer.toneMapping = T.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.18;
    this.scene = new T.Scene();
    this.camera = new T.PerspectiveCamera(34, 9 / 16, 0.1, 200);
    this.camera.position.set(0, 0, 9);
    this.target = new T.Vector3(0, 0, 0);

    this.scene.add(new T.HemisphereLight(0xcfe0ff, 0x1b1030, 1.15));
    this.key = new T.DirectionalLight(0xfff0dd, 2.2);
    this.key.position.set(4.5, 6, 9);
    this.fill = new T.DirectionalLight(0xdfe8ff, 1.15);
    this.fill.position.set(-5, 1.5, 7);
    this.scene.add(this.key, this.fill);
    this.rimA = new T.PointLight(0xFFB01F, 26, 26, 2); this.rimA.position.set(-4.4, 1.6, 3.4);
    this.rimB = new T.PointLight(0x12E2C4, 22, 26, 2); this.rimB.position.set(4.6, -2.2, 2.6);
    this.scene.add(this.rimA, this.rimB);

    // procedural environment so metal and gloss have something real to reflect
    const envTex = canvasTexture(1024, 512, (g, w, h) => {
      const grad = g.createLinearGradient(0, 0, 0, h);
      grad.addColorStop(0, '#2b2350'); grad.addColorStop(.45, '#120c26'); grad.addColorStop(1, '#05030e');
      g.fillStyle = grad; g.fillRect(0, 0, w, h);
      const blob = (x, y, r, c) => {
        const rg = g.createRadialGradient(x, y, 0, x, y, r);
        rg.addColorStop(0, c); rg.addColorStop(1, 'rgba(0,0,0,0)');
        g.fillStyle = rg; g.fillRect(x - r, y - r, r * 2, r * 2);
      };
      blob(250, 150, 220, 'rgba(255,176,31,.85)');
      blob(760, 190, 200, 'rgba(18,226,196,.8)');
      blob(520, 420, 260, 'rgba(123,43,255,.5)');
    });
    envTex.mapping = T.EquirectangularReflectionMapping;
    const pmrem = new T.PMREMGenerator(this.renderer);
    this.scene.environment = pmrem.fromEquirectangular(envTex).texture;

    this.root = new T.Group();
    this.scene.add(this.root);

    this.dust = this.makeDust();
    this.root.add(this.dust);
  }

  makeDust() {
    const N = 420, pos = new Float32Array(N * 3), col = new Float32Array(N * 3);
    const c1 = new T.Color(0xFFB01F), c2 = new T.Color(0x12E2C4);
    for (let i = 0; i < N; i++) {
      pos[i * 3] = (Math.random() - .5) * 26;
      pos[i * 3 + 1] = (Math.random() - .5) * 34;
      pos[i * 3 + 2] = -Math.random() * 30 + 4;
      const c = Math.random() < .5 ? c1 : c2;
      col[i * 3] = c.r; col[i * 3 + 1] = c.g; col[i * 3 + 2] = c.b;
    }
    const geo = new T.BufferGeometry();
    geo.setAttribute('position', new T.BufferAttribute(pos, 3));
    geo.setAttribute('color', new T.BufferAttribute(col, 3));
    const sprite = canvasTexture(64, 64, (g, w) => {
      const rg = g.createRadialGradient(32, 32, 0, 32, 32, 32);
      rg.addColorStop(0, 'rgba(255,255,255,1)'); rg.addColorStop(.35, 'rgba(255,255,255,.5)');
      rg.addColorStop(1, 'rgba(255,255,255,0)');
      g.fillStyle = rg; g.fillRect(0, 0, w, w);
    });
    const mat = new T.PointsMaterial({ size: .1, map: sprite, vertexColors: true, transparent: true,
      blending: T.AdditiveBlending, depthWrite: false, opacity: .9 });
    return new T.Points(geo, mat);
  }

  setTheme(a, b) { this.rimA.color.set(a); this.rimB.color.set(b); }
  resize() {
    const r = this.renderer.domElement.parentElement.getBoundingClientRect();
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 6));
    this.renderer.setSize(r.width, r.height, false);
    this.camera.aspect = r.width / r.height;
    this.camera.updateProjectionMatrix();
  }
  render() {
    this.camera.lookAt(this.target);
    this.renderer.render(this.scene, this.camera);
  }
}

(function () {
  const $ = (id) => document.getElementById(id);
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const AD = { totalDurationMs: 52000, prompt: 'A bedtime story about a brave little fox...' };

  const audio = new AudioEngine();
  const world = new World($('gl'));

  const els = {
    stage: $('stage'), stageInner: $('stageInner'), bgA: $('bgA'), bgB: $('bgB'),
    chromaFlash: $('chromaFlash'), progress: $('progress'),
    scenes: ['sOpen','sBook','sPages','sStyle','sRing','sFly','sVoice','sEarn','sPrice','sCta'].map($),
    openEyebrow: $('openEyebrow'), promptBox: $('promptBox'), promptText: $('promptText'),
    bookHeadline: $('bookHeadline'), bookSub: $('bookSub'),
    pagesEyebrow: $('pagesEyebrow'), pagesChip: $('pagesChip'),
    styleHeadline: $('styleHeadline'), styleChip: $('styleChip'),
    ringHeadline: $('ringHeadline'), ringChip: $('ringChip'),
    flyEyebrow: $('flyEyebrow'),
    voiceEyebrow: $('voiceEyebrow'), voiceChip: $('voiceChip'), voiceSub: $('voiceSub'),
    earnEyebrow: $('earnEyebrow'), earnNum: $('earnNum'), earnSub: $('earnSub'),
    priceEyebrow: $('priceEyebrow'), priceChip: $('priceChip'),
    ctaSub: $('ctaSub'), ctaBtn: $('ctaBtn'), ctaTrust: $('ctaTrust'), ctaUrl: $('ctaUrl'),
    playOverlay: $('playOverlay'), replayBtn: $('replayBtn'),
  };
  const on = (el) => el && el.classList.add('in');
  const off = (el) => el && el.classList.remove('in');
  const snap = (el) => { if (!el) return; el.classList.remove('snap'); void el.offsetWidth; el.classList.add('snap'); };

  const THEMES = {
    ember:  { a: '#FFB01F', b: '#FF5A1F', bg: 'radial-gradient(130% 95% at 50% 12%, #2A1206, #08040F 62%)' },
    teal:   { a: '#12E2C4', b: '#25A7FF', bg: 'radial-gradient(130% 95% at 50% 12%, #04262A, #040312 62%)' },
    violet: { a: '#7B2BFF', b: '#FF2D78', bg: 'radial-gradient(130% 95% at 50% 12%, #1E0838, #06030F 62%)' },
    rose:   { a: '#FF2D78', b: '#FFB01F', bg: 'radial-gradient(130% 95% at 50% 12%, #33062A, #09040F 62%)' },
    lime:   { a: '#B6FF3C', b: '#12E2C4', bg: 'radial-gradient(130% 95% at 50% 12%, #12280A, #040B0E 62%)' },
    gold:   { a: '#FFC857', b: '#12E2C4', bg: 'radial-gradient(130% 95% at 50% 12%, #2E1D03, #05040F 62%)' },
  };
  let bgFlip = false;
  function setTheme(name, flash) {
    const t = THEMES[name]; if (!t) return;
    els.stageInner.style.setProperty('--a', t.a);
    els.stageInner.style.setProperty('--b', t.b);
    world.setTheme(t.a, t.b);
    const inL = bgFlip ? els.bgA : els.bgB, outL = bgFlip ? els.bgB : els.bgA;
    inL.style.background = t.bg; inL.classList.add('on'); outL.classList.remove('on');
    bgFlip = !bgFlip;
    if (flash !== false && !reduceMotion) {
      els.chromaFlash.style.transition = 'none';
      els.chromaFlash.style.opacity = '.16';
      setTimeout(() => { els.chromaFlash.style.transition = 'opacity .3s ease'; els.chromaFlash.style.opacity = '0'; }, 40);
    }
  }
  function punch(s) {
    if (reduceMotion) return;
    els.stageInner.style.transition = 'none';
    els.stageInner.style.transform = `scale(${s || 1.04})`;
    els.stageInner.style.filter = 'brightness(1.16) saturate(1.22)';
    setTimeout(() => { els.stageInner.style.transform = ''; els.stageInner.style.filter = ''; }, 130);
  }

  /* ---------------------------- build the models --------------------------- */
  const COVER_KEYS = ['fox', 'puzzles', 'preschool', 'chapter', 'grammar', 'seasonal', 'bedtime'];
  const coverTex = {};
  COVER_KEYS.forEach(k => { coverTex[k] = artTexture(ART[k]); });
  const pageTex = ART.pageArt.map((u, i) => pageTexture(u, 7 + i * 2));

  const G = {
    open: new T.Group(), book: new T.Group(), pages: new T.Group(), style: new T.Group(),
    ring: new T.Group(), fly: new T.Group(), voice: new T.Group(), earn: new T.Group(),
    price: new T.Group(), cta: new T.Group(),
  };
  Object.values(G).forEach(g => { g.visible = false; world.root.add(g); });

  // --- opening: a glowing floor grid the camera skims over
  (() => {
    const grid = new T.GridHelper(64, 48, 0x7B2BFF, 0x2a1b52);
    grid.material.transparent = true; grid.material.opacity = .5;
    grid.position.set(0, -3.2, -6);
    G.open.add(grid);
    const ringGeo = new T.TorusGeometry(1.45, .03, 12, 96);
    const ringMat = new T.MeshStandardMaterial({ color: 0x7B2BFF, emissive: 0x4a18c4, emissiveIntensity: 1.7, roughness: .25, metalness: .8 });
    const halo = new T.Mesh(ringGeo, ringMat);
    halo.position.set(0, 1.35, -6.2);
    G.open.add(halo);
    G.open.userData.halo = halo;
  })();

  // --- hero book
  const heroBook = makeBook(coverTex.fox, '#FFB01F');
  G.book.add(heroBook);

  // --- open book with turning pages
  (() => {
    const coverMat = new T.MeshStandardMaterial({ color: 0x1d1740, roughness: .5, metalness: .25 });
    const left = new T.Mesh(new T.BoxGeometry(2.0, 2.8, .1), coverMat);
    left.position.set(-1.02, 0, -.06); left.rotation.y = .22;
    const right = new T.Mesh(new T.BoxGeometry(2.0, 2.8, .1), coverMat);
    right.position.set(1.02, 0, -.06); right.rotation.y = -.22;
    G.pages.add(left, right);
    const sheets = [];
    for (let i = 0; i < 5; i++) {
      const front = new T.MeshStandardMaterial({ map: pageTex[i], roughness: .88, metalness: .02, side: T.FrontSide });
      const backM = new T.MeshStandardMaterial({ color: 0xf3ead9, roughness: .9, metalness: .02, side: T.BackSide });
      const sheet = new T.Group();
      const g2 = new T.PlaneGeometry(1.96, 2.7, 12, 1);
      g2.translate(.98, 0, 0);                       // hinge on the left edge
      const a = new T.Mesh(g2, front), b = new T.Mesh(g2, backM);
      sheet.add(a, b);
      sheet.position.set(-.02, 0, .02 + i * .012);
      sheet.rotation.y = -.16;
      G.pages.add(sheet);
      sheets.push(sheet);
    }
    G.pages.userData.sheets = sheets;
    G.pages.rotation.set(.12, .3, 0);
    G.pages.scale.setScalar(.74);
  })();

  // --- style morph book
  const styleBook = makeBook(coverTex.fox, '#FF2D78');
  G.style.add(styleBook);

  // --- carousel of real books
  (() => {
    const books = COVER_KEYS.map((k, i) => {
      const b = makeBook(coverTex[k], i % 2 ? '#12E2C4' : '#FFB01F');
      b.scale.setScalar(.7);
      G.ring.add(b);
      return b;
    });
    G.ring.userData.books = books;
  })();

  const FEATURES = [
    { t: 'AI text & illustrations', s: 'Written and drawn in one pass', c: '#FFB01F',
      d: 'M4 19V5a2 2 0 0 1 2-2h11l3 3v13a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z M8 8h8 M8 12h8 M8 16h5' },
    { t: '15+ illustration styles', s: 'Switch the whole look in a click', c: '#FF2D78',
      d: 'M12 3a9 9 0 1 0 0 18c1 0 1.5-.6 1.5-1.3 0-1.4-1-1.5-1-2.4 0-.7.6-1.3 1.4-1.3H16a5 5 0 0 0 5-5c0-4.4-4-8-9-8z M7.5 11.5h.01 M10.5 8.5h.01 M14.5 8.5h.01' },
    { t: '200+ pages · PDF export', s: 'Print-ready the moment it is done', c: '#12E2C4',
      d: 'M6 2h9l5 5v15H6z M15 2v5h5 M9 13h6 M9 17h6' },
    { t: 'Storytelling voice', s: 'Every story read aloud, naturally', c: '#B6FF3C',
      d: 'M12 3v18 M8 7v10 M4 10v4 M16 7v10 M20 10v4' },
    { t: 'Cloud draft saving', s: 'Pick up exactly where you stopped', c: '#25A7FF',
      d: 'M6 18a4 4 0 0 1 .7-7.9 6 6 0 0 1 11.5 1.6A3.5 3.5 0 0 1 18 18z' },
    { t: 'Live support access', s: 'Real help while you build', c: '#7B2BFF',
      d: 'M21 15a2 2 0 0 1-2 2H8l-4 4V5a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2z' },
  ];
  const flyPanels = FEATURES.map(f => { const p = makePanel(f); p.visible = false; G.fly.add(p); return p; });

  // --- waveform of lit bars
  (() => {
    const bars = [];
    const mat = new T.MeshStandardMaterial({ color: 0xB6FF3C, emissive: 0x4f7a12, emissiveIntensity: 1.5, roughness: .25, metalness: .6 });
    for (let i = 0; i < 20; i++) {
      const b = new T.Mesh(new T.BoxGeometry(.1, 1, .1), mat);
      b.position.set((i - 9.5) * .13, 0, 0);
      G.voice.add(b); bars.push(b);
    }
    G.voice.userData.bars = bars;
    G.voice.rotation.set(.22, -.2, 0);
  })();

  // --- stacking coins
  (() => {
    const gold = new T.MeshStandardMaterial({ color: 0xFFC857, roughness: .18, metalness: 1 });
    const coins = [];
    for (let i = 0; i < 16; i++) {
      const c = new T.Mesh(new T.CylinderGeometry(.34, .34, .07, 40), gold);
      c.rotation.x = .16;
      G.earn.add(c); coins.push(c);
    }
    G.earn.userData.coins = coins;
  })();

  // --- pricing slab
  (() => {
    const geo = new T.ExtrudeGeometry(roundedShape(2.9, 3.62, .3), {
      depth: .2, bevelEnabled: true, bevelThickness: .06, bevelSize: .06, bevelSegments: 3, curveSegments: 12 });
    geo.center(); fitUV(geo);
    const tex = priceTexture();
    const slab = new T.Mesh(geo, [
      new T.MeshStandardMaterial({ map: tex, roughness: .32, metalness: .25 }),
      new T.MeshStandardMaterial({ color: 0x17123a, roughness: .28, metalness: .75 }),
    ]);
    G.price.add(slab);
    G.price.userData.slab = slab;
  })();

  // --- CTA: wordmark plaque above a hero book
  (() => {
    const geo = new T.ExtrudeGeometry(roundedShape(2.62, .84, .18), {
      depth: .26, bevelEnabled: true, bevelThickness: .07, bevelSize: .07, bevelSegments: 4, curveSegments: 14 });
    geo.center(); fitUV(geo);
    const wm = wordmarkTexture();
    const plaque = new T.Mesh(geo, [
      new T.MeshStandardMaterial({ map: wm, transparent: true, roughness: .22, metalness: .5,
        emissiveMap: wm, emissive: 0xffffff, emissiveIntensity: .32 }),
      new T.MeshStandardMaterial({ color: 0xFFB01F, roughness: .18, metalness: 1 }),
    ]);
    plaque.position.set(0, 1.98, 0);
    const b = makeBook(coverTex.fox, '#FFB01F');
    b.scale.setScalar(.62); b.position.set(0, .2, 0);
    G.cta.add(plaque, b);
    G.cta.userData.plaque = plaque; G.cta.userData.book = b;
  })();

  /* ------------------------------ scene control ---------------------------- */
  const motion = { t0: 0, running: false, last: 0, acts: {} };
  const ease = (p) => 1 - Math.pow(1 - p, 3);
  const clamp01 = (v) => v < 0 ? 0 : v > 1 ? 1 : v;

  function showScene(id, theme, group) {
    els.scenes.forEach(s => s.classList.toggle('active', s.id === id));
    Object.values(G).forEach(g => { g.visible = false; });
    if (group) group.visible = true;
    if (theme) setTheme(theme);
    punch();
    audio.whoosh(.38);
  }

  function buildWords(el, segs) {
    el.innerHTML = '';
    const out = [];
    segs.forEach(seg => seg.text.split(' ').forEach(w => {
      const s = document.createElement('span');
      s.className = 'word' + (seg.cls ? ' ' + seg.cls : '');
      s.textContent = w;
      el.appendChild(s); el.appendChild(document.createTextNode(' '));
      out.push(s);
    }));
    return out;
  }
  function revealWords(words, step) {
    words.forEach((w, i) => setTimeout(() => { w.classList.add('in'); if (i % 2 === 0) audio.tick(); }, i * step));
  }
  let typeTimer = null;
  function typeChars(el, text, speed, onChar) {
    if (typeTimer) { clearInterval(typeTimer); typeTimer = null; }
    let i = 0; el.textContent = '';
    typeTimer = setInterval(() => {
      el.textContent = text.slice(0, i + 1);
      if (onChar) onChar(i);
      if (++i >= text.length) { clearInterval(typeTimer); typeTimer = null; }
    }, speed);
  }

  /* one rAF loop drives every mesh, keyed to the timeline clock so it stays
     deterministic under the renderer's virtual time */
  function loop() {
    requestAnimationFrame(loop);
    const now = performance.now();
    const dt = Math.min(.05, (now - (motion.last || now)) / 1000);
    motion.last = now;
    const e = motion.running ? now - motion.t0 : 0;
    const A = motion.acts;

    world.dust.rotation.y = e * 0.000035;
    world.dust.position.z = 4 + ((e * 0.0016) % 12);

    if (G.open.visible) {
      const h = G.open.userData.halo;
      h.rotation.z = e * .0006; h.rotation.x = .4 + Math.sin(e * .0009) * .12;
      world.camera.position.set(Math.sin(e * .00022) * .7, .3 + Math.sin(e * .0004) * .15, 8.6);
    }
    if (A.book) {
      const p = clamp01((e - A.book.from) / A.book.dur), q = A.book.linear ? p : ease(p);
      heroBook.rotation.y = A.book.y0 + q * (A.book.y1 - A.book.y0);
      heroBook.rotation.x = A.book.x0 + q * (A.book.x1 - A.book.x0);
      heroBook.scale.setScalar(A.book.s0 + q * (A.book.s1 - A.book.s0));
      heroBook.position.y = .25;
      world.camera.position.set(0, .3, A.book.z0 + q * (A.book.z1 - A.book.z0));
    }
    if (A.pages) {
      const sheets = G.pages.userData.sheets;
      sheets.forEach((s, i) => {
        const st = A.pages.from + i * A.pages.step;
        const p = clamp01((e - st) / A.pages.dur);
        s.rotation.y = -.16 - ease(p) * 2.62;
      });
      G.pages.rotation.y = .3 - clamp01((e - A.pages.from) / 4200) * .48;
      world.camera.position.set(0, .1, 9.4);
    }
    if (A.style) {
      const p = clamp01((e - A.style.from) / A.style.dur);
      styleBook.rotation.y = -.5 + p * 1.15;
      styleBook.rotation.x = .1 - p * .2;
      styleBook.scale.setScalar(.82);
      world.camera.position.set(0, .42, 8.6);
    }
    if (A.ring) {
      const p = clamp01((e - A.ring.from) / A.ring.dur), q = ease(p);
      const books = G.ring.userData.books, n = books.length;
      const spin = A.ring.a0 + q * (A.ring.a1 - A.ring.a0);
      const R = A.ring.r0 + q * (A.ring.r1 - A.ring.r0);
      const camZ = A.ring.z;
      books.forEach((b, i) => {
        const a = spin + (i / n) * Math.PI * 2;
        const bx = Math.sin(a) * R, bz = Math.cos(a) * R;
        b.position.set(bx, Math.sin(a * 2 + i) * .12, bz);
        // turn each cover most of the way toward the lens so the artwork
        // stays readable while the ring still reads as a ring
        b.rotation.y = Math.atan2(-bx, camZ - bz) * .86;
      });
      world.camera.position.set(0, .85, A.ring.z);
      world.target.set(0, 0, 0);
    }
    if (A.fly) {
      flyPanels.forEach((pn, i) => {
        const st = A.fly.from + i * A.fly.step;
        const p = (e - st) / A.fly.dur;
        if (p < 0 || p > 1) { pn.visible = false; return; }
        pn.visible = true;
        pn.position.set((i % 2 ? 1 : -1) * .62, (i % 2 ? -.72 : .72), -14 + p * 15);
        pn.rotation.set(.04, (i % 2 ? -1 : 1) * (.5 - p * .62), (i % 2 ? 1 : -1) * .035);
        const fade = p < .16 ? p / .16 : (p > .72 ? clamp01((1 - p) / .28) : 1);
        pn.children.length; pn.material.forEach(m => { m.transparent = true; m.opacity = fade; });
      });
      world.camera.position.set(0, 0, 9.5);
    }
    if (G.voice.visible) {
      const bars = G.voice.userData.bars, tt = e / 1000;
      bars.forEach((b, i) => {
        const v = Math.abs(Math.sin(tt * 5.4 + i * .52)) * Math.abs(Math.sin(tt * 1.6 + i * .2));
        const hgt = .16 + v * 1.85;
        b.scale.y = hgt; b.position.y = 0;
      });
      G.voice.rotation.y = -.2 + Math.sin(e * .0004) * .12;
      world.camera.position.set(0, .1, 9.2);
    }
    if (A.earn) {
      const coins = G.earn.userData.coins;
      coins.forEach((c, i) => {
        const st = A.earn.from + i * A.earn.step;
        const p = clamp01((e - st) / 620), q = ease(p);
        c.visible = p > 0;
        const col = i % 3, row = Math.floor(i / 3);
        c.position.set((col - 1) * .8, -.9 + row * .14 + (1 - q) * 7, 0);
        c.rotation.y = e * .0012 + i;
        c.scale.setScalar(.6 + q * .4);
      });
      G.earn.rotation.y = Math.sin(e * .0004) * .18;
      world.camera.position.set(0, .2, 9.6);
    }
    if (A.price) {
      const p = clamp01((e - A.price.from) / A.price.dur), q = ease(p);
      const s = G.price.userData.slab;
      s.rotation.y = .85 - q * .85 + Math.sin(e * .0004) * .09;
      s.rotation.x = .18 - q * .18;
      s.position.z = -2.4 + q * 2.4;
      world.camera.position.set(0, 0, 9.9);
    }
    if (A.cta) {
      const p = clamp01((e - A.cta.from) / A.cta.dur), q = ease(p);
      const pl = G.cta.userData.plaque, bk = G.cta.userData.book;
      pl.rotation.y = -1.5 + q * 1.5; pl.position.z = -3 + q * 3;
      bk.rotation.y = -.9 + q * .62 + Math.sin(e * .0004) * .1;
      bk.rotation.x = .1;
      world.camera.position.set(0, .35, 10.2 - q * .5);
    }

    world.render();
  }

  /* --------------------------------- timeline ------------------------------ */
  function buildTimeline() {
    const tl = new Timeline(AD.totalDurationMs);
    const bookWords = buildWords(els.bookHeadline, [{ text: 'It forges the' }, { text: 'whole book', cls: 'accentA' }, { text: 'for you.' }]);
    const styleWords = buildWords(els.styleHeadline, [{ text: 'Not the look you want?' }, { text: 'Swap it.', cls: 'accentA' }]);
    const ringWords = buildWords(els.ringHeadline, [{ text: 'Any topic.' }, { text: 'Any style.', cls: 'accentA' }]);

    const BEAT = 480, BARS = Math.floor(AD.totalDurationMs / (BEAT * 4));
    const BASS = [55, 55, 73.42, 65.41], ARP = [220, 261.63, 329.63, 440, 329.63, 261.63];
    for (let bar = 0; bar < BARS; bar++) {
      const barT = bar * BEAT * 4, root = BASS[bar % BASS.length];
      const heavy = bar >= 2, mid = barT >= 3600 && barT < 49500, full = barT >= 16000 && barT < 45000;
      tl.at(barT, () => audio.sub(root));
      tl.at(barT + BEAT * 2, () => audio.sub(root * 1.5));
      if (bar % 2 === 0) tl.at(barT, () => audio.pad([root * 2, root * 3, root * 4]));
      for (let b = 0; b < 4; b++) {
        const t = barT + b * BEAT;
        if (heavy) tl.at(t, () => audio.kick());
        if (mid) tl.at(t + BEAT / 2, () => audio.hat());
      }
      if (full) for (let s = 0; s < 8; s++) tl.at(barT + s * (BEAT / 2), () => audio.arp(ARP[(bar * 8 + s) % ARP.length]));
    }

    // S1 · the idea
    tl.at(0, () => {
      motion.running = true; motion.t0 = performance.now(); motion.acts = {};
      setTheme('violet', false);
      showScene('sOpen', null, G.open);
      audio.riser(1.5);
    });
    tl.at(420, () => on(els.openEyebrow));
    tl.at(760, () => { on(els.promptBox); audio.pop(); });
    tl.at(1020, () => typeChars(els.promptText, AD.prompt, 34, (i) => { if (i % 2 === 0) audio.tick(); }));
    const typedEnd = 1020 + AD.prompt.length * 34;
    tl.at(typedEnd + 220, () => audio.riser(.85));
    tl.at(typedEnd + 900, () => { audio.impact(); punch(1.07); off(els.promptBox); off(els.openEyebrow); });

    // S2 · the book is forged
    const s2 = typedEnd + 1080;
    tl.at(s2, () => {
      showScene('sBook', 'ember', G.book);
      motion.acts = { book: { from: s2, dur: 1700, y0: -2.9, y1: -.42, x0: .55, x1: .12, s0: .16, s1: 1, z0: 13, z1: 8.2 } };
      audio.motif();
    });
    tl.at(s2 + 1600, () => { audio.impact(); punch(1.05); });
    tl.at(s2 + 1750, () => revealWords(bookWords, 70));
    tl.at(s2 + 2500, () => on(els.bookSub));
    tl.at(s2 + 2650, () => {
      motion.acts = { book: { from: s2 + 2650, dur: 2200, y0: -.42, y1: .42, x0: .12, x1: -.06, s0: 1, s1: 1.06, z0: 8.2, z1: 7.5, linear: true } };
    });

    // S3 · pages
    const s3 = s2 + 4800;
    tl.at(s3, () => {
      showScene('sPages', 'teal', G.pages);
      motion.acts = { pages: { from: s3 + 500, step: 560, dur: 900 } };
    });
    tl.at(s3 + 180, () => on(els.pagesEyebrow));
    for (let i = 0; i < 5; i++) tl.at(s3 + 500 + i * 560, () => { audio.whoosh(.3); audio.tick(); });
    tl.at(s3 + 2950, () => { on(els.pagesChip); snap(els.pagesChip); audio.pop(); });
    tl.at(s3 + 4300, () => audio.riser(.5));

    // S4 · style morph
    const s4 = s3 + 4900;
    const STYLES = [['fox','Storybook'],['puzzles','Puzzle book'],['preschool','Worksheets'],
                    ['grammar','Workbook'],['chapter','Chapter book'],['seasonal','Seasonal'],['bedtime','Bedtime']];
    tl.at(s4, () => {
      showScene('sStyle', 'rose', G.style);
      styleBook.material[4].map = coverTex.fox; styleBook.material[4].needsUpdate = true;
      motion.acts = { style: { from: s4, dur: 3900 } };
    });
    tl.at(s4 + 250, () => revealWords(styleWords, 60));
    STYLES.forEach((st, i) => { if (i === 0) return;
      tl.at(s4 + 760 + (i - 1) * 215, () => {
        styleBook.material[4].map = coverTex[st[0]];
        styleBook.material[4].needsUpdate = true;
        audio.tick(); if (i % 2 === 0) audio.click();
      });
    });
    tl.at(s4 + 2250, () => { on(els.styleChip); snap(els.styleChip); audio.pop(); });
    tl.at(s4 + 3700, () => audio.riser(.6));

    // S5 · carousel
    const s5 = s4 + 4400;
    tl.at(s5, () => {
      showScene('sRing', 'violet', G.ring);
      motion.acts = { ring: { from: s5, dur: 3200, a0: 0, a1: 7.2, r0: .9, r1: 3.2, z: 11.2 } };
      audio.impact();
    });
    for (let i = 0; i < 7; i++) tl.at(s5 + 140 + i * 95, () => audio.tick());
    tl.at(s5 + 2000, () => revealWords(ringWords, 65));
    tl.at(s5 + 2600, () => { on(els.ringChip); snap(els.ringChip); audio.pop(); });
    tl.at(s5 + 3250, () => {
      motion.acts = { ring: { from: s5 + 3250, dur: 2600, a0: 7.2, a1: 9.1, r0: 3.2, r1: 2.95, z: 10.4 } };
    });
    tl.at(s5 + 4300, () => { audio.impact(); punch(1.04); });
    tl.at(s5 + 5600, () => audio.riser(.7));

    // S6 · features fly past
    const s6 = s5 + 6100;
    tl.at(s6, () => {
      showScene('sFly', 'teal', G.fly);
      motion.acts = { fly: { from: s6 + 350, step: 1000, dur: 1950 } };
      on(els.flyEyebrow); audio.impact();
    });
    FEATURES.forEach((f, i) => tl.at(s6 + 350 + i * 1000, () => { audio.whoosh(.34); audio.pop(); }));
    tl.at(s6 + 6650, () => { off(els.flyEyebrow); audio.riser(.6); });

    // S7 · voice
    const s7 = s6 + 7250;
    tl.at(s7, () => { showScene('sVoice', 'lime', G.voice); motion.acts = {}; });
    tl.at(s7 + 160, () => on(els.voiceEyebrow));
    tl.at(s7 + 520, () => { on(els.voiceChip); audio.pop(); audio.chime(); });
    tl.at(s7 + 1000, () => on(els.voiceSub));
    tl.at(s7 + 2100, () => { audio.chime(); snap(els.voiceChip); });
    tl.at(s7 + 3900, () => audio.whoosh(.42));

    // S8 · earn
    const s8 = s7 + 4400;
    const SALES = [12.99, 8.50, 9.99, 45.00];
    tl.at(s8, () => {
      showScene('sEarn', 'gold', G.earn);
      motion.acts = { earn: { from: s8 + 300, step: 150 } };
    });
    tl.at(s8 + 150, () => on(els.earnEyebrow));
    let running = 0;
    SALES.forEach((v, i) => tl.at(s8 + 520 + i * 430, () => {
      running += v; els.earnNum.textContent = '$' + running.toFixed(2);
      snap(els.earnNum); audio.pop(); audio.tick();
    }));
    tl.at(s8 + 2500, () => { els.earnNum.textContent = '$2,480'; snap(els.earnNum); audio.impact(); punch(1.05); });
    tl.at(s8 + 2900, () => on(els.earnSub));
    tl.at(s8 + 4600, () => audio.riser(.6));

    // S9 · pricing
    const s9 = s8 + 5200;
    tl.at(s9, () => {
      showScene('sPrice', 'teal', G.price);
      motion.acts = { price: { from: s9 + 120, dur: 1100 } };
    });
    tl.at(s9 + 180, () => { on(els.priceEyebrow); audio.pop(); });
    tl.at(s9 + 1500, () => { on(els.priceChip); snap(els.priceChip); audio.click(); audio.motif(); });
    tl.at(s9 + 3400, () => { snap(els.priceChip); audio.pop(); });
    tl.at(s9 + 4200, () => audio.riser(.9));

    // S10 · CTA
    const s10 = s9 + 5200;
    tl.at(s10, () => {
      showScene('sCta', 'ember', G.cta);
      motion.acts = { cta: { from: s10, dur: 1500 } };
      audio.impact(); punch(1.06);
    });
    tl.at(s10 + 1280, () => audio.sonicLogo());
    tl.at(s10 + 1500, () => on(els.ctaSub));
    tl.at(s10 + 1900, () => { on(els.ctaBtn); audio.pop(); });
    tl.at(s10 + 2250, () => { els.ctaBtn.classList.add('ring'); audio.chime(); });
    tl.at(s10 + 2500, () => on(els.ctaTrust));
    tl.at(s10 + 2900, () => { on(els.ctaUrl); snap(els.ctaUrl); audio.motif(); });
    tl.at(s10 + 3600, () => { els.ctaBtn.classList.remove('ring'); void els.ctaBtn.offsetWidth; els.ctaBtn.classList.add('ring'); audio.pop(); });
    tl.at(s10 + 4600, () => { snap(els.ctaUrl); audio.motif(); });
    tl.at(s10 + 5400, () => audio.chime());

    return tl;
  }

  function resetAll() {
    if (typeTimer) { clearInterval(typeTimer); typeTimer = null; }
    els.stageInner.style.transform = ''; els.stageInner.style.filter = '';
    els.chromaFlash.style.opacity = '0';
    els.progress.style.width = '0%';
    els.scenes.forEach(s => s.classList.remove('active'));
    Object.values(G).forEach(g => { g.visible = false; });
    motion.acts = {}; motion.running = false;
    flyPanels.forEach(p => { p.visible = false; });
    G.earn.userData.coins.forEach(c => { c.visible = false; });
    [els.openEyebrow, els.promptBox, els.bookSub, els.pagesEyebrow, els.pagesChip, els.styleChip,
     els.ringChip, els.flyEyebrow, els.voiceEyebrow, els.voiceChip, els.voiceSub, els.earnEyebrow,
     els.earnSub, els.priceEyebrow, els.priceChip, els.ctaSub, els.ctaBtn, els.ctaTrust, els.ctaUrl].forEach(off);
    els.promptText.textContent = '';
    els.earnNum.textContent = '$0';
    els.ctaBtn.classList.remove('ring');
    [els.bookHeadline, els.styleHeadline, els.ringHeadline].forEach(h => h.querySelectorAll('.word').forEach(off));
    setTheme('violet', false);
  }

  let timeline = null;
  function startShow() {
    if (timeline) timeline.stop();
    resetAll();
    world.resize();
    timeline = buildTimeline();
    timeline.start((f) => { els.progress.style.width = (f * 100).toFixed(1) + '%'; });
  }

  world.resize();
  requestAnimationFrame(loop);
  window.addEventListener('resize', () => world.resize());

  els.playOverlay.addEventListener('click', function () {
    if (!audio.ctx) audio.init();
    this.style.display = 'none';
    startShow();
  });
  els.replayBtn.addEventListener('click', startShow);
})();
