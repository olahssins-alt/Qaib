---
name: teepublic-upload
description: Fill the TeePublic upload form for ready-made designs, one at a time, using a prepared manifest (title, main tag, tags, description, product and color choices). Use when the user asks to upload, list or fill TeePublic designs from this skill's manifest. Never publishes; the user presses Publish.
---

# TeePublic upload (fill only, never publish)

Everything needed is in this folder, so do not research or rewrite anything:

- `manifest.json`: for each design, the PNG path, title, main tag, tags, description, products and colors. Use these strings exactly as written.
- `designs/*.png`: the print files, 4500x5500, transparent.

## Rules
1. **Never press Publish, Submit for sale or any final button.** Fill the form, then stop and tell the user the design is ready for review.
2. **Never type or ask for a password or payment detail.** The user is already signed in. If a login or captcha page appears, stop and tell the user.
3. **One design at a time.** After each, wait for the user to say "next". Do not batch several designs.
4. If the form differs from what is described here, or a field is missing, stop and ask. Do not guess.
5. Do not change any text in the manifest. Do not add tags or edit the description.
6. Only dark shirt colors (black, navy, charcoal, forest green). Turn off light colors, because the designs have cream text that disappears on white.

## Keep token use low
- Open one tab and reuse it for all designs.
- Read the page as text (accessibility tree, find or read_page) instead of taking screenshots. Take a screenshot only to confirm the final state of a design, or when a field cannot be found as text.
- Fill several fields in one call when the tool allows it.
- Read `manifest.json` once at the start. Do not re-read it per design; keep the current design's fields in mind.
- Do not narrate each click. Report once per design.

## Steps for each design with status "pending"
1. Open the TeePublic new-design upload page from the user's dashboard (Upload Design).
2. Select the design file `designs/<id>.png` in the file input. If the browser tool cannot choose a local file, stop and ask the user to pick it, then continue after they confirm.
3. Fill: Title, Main tag, Tags (all, in the manifest order), Description.
4. Select the products listed in `products` (default product first) and the colors in `colors`.
5. Check the form shows no error messages. Do not press Publish.
6. Tell the user in two lines: the design id and "filled, waiting for your review". Then set `status` to `filled` in your notes and wait.

## Before the user publishes
Remind them once per session: search the title on teepublic.com for an almost identical design, and change the wording if one exists.

## If something goes wrong
After two failed attempts at the same step, stop and tell the user what you tried. Do not keep retrying.
