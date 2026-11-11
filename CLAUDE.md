# VocalPrep — working notes for Claude

The user (Lawrence) is a composer and singer. VocalPrep is their iPad app for practising exercises from singing lessons.
They work on the iPad through Claude on the web/app; this repo is the master copy.

## The app
- One file: `app/vocalprep_vNN.html` (HTML + CSS + JS, no build step, no libraries).
- `build.py` copies it to `site/index.html` and adds the offline service worker, manifest and drawn icons (needs Pillow).
- `.github/workflows/deploy.yml` builds and publishes to https://l-sial.github.io/vocalprep/ on every push to `main` (1–2 min).
- The iPad picks up a new version when the app is closed fully and reopened while online. Version bottom left (`<span class="ver">vNN</span>`).
- `HANDOFF.md` = change history and design notes (newest at the end).
- The design mockups (stages 1 and 2, keyboard): https://claude.ai/artifact/9piM2qzGU89QgMjEyzqL87

## How to make a change
1. `git mv` the html to the next number (v1 → v2) so there is only ever ONE html in `app/`.
2. Change `<span class="ver">vNN</span>`.
3. Make the change; plain functions, comments starting `// vNN:` that say why.
4. Extract the `<script>` and run `node --check`; if possible load `site/` (after `python3 build.py`) in a headless
   browser and check for errors. Test hooks: `window.__vp`.
5. Add a `## vNN (date)` section at the end of `HANDOFF.md`.
6. Commit; push to `main` if allowed, otherwise push a branch, open a pull request and tell the user to tap **Merge**.
   Then: wait ~2 minutes, close the app fully, reopen, check the version bottom left.

## The user's rules
- Short replies at the end of a task: the result and how to use it, numbered steps, one step per number.
- Interface words: **region** (not excerpt/clip), **Repository** (right panel), **Capture** / **Practise**, **Lessons**.
- Time is real time m:ss. Highest resolution (regions are stored as 24-bit WAV). Attacks 3 ms; envelopes exponential.
- Colours: parchment (#F2EDE2 / #FBF8F2) with black and muted grey-blacks only.
- The pitch keyboard: E2–C4, no note names anywhere, keys do not light up. Default pattern **Note** (plays the key
  touched); patterns live in `PATTERNS` and more will be asked for (e.g. other scales) — add them there.
- Backups go to Dropbox through the share sheet (Save to Files › Dropbox); the app can't write there by itself.
- Never handle passwords or secrets. Never delete the user's files; the app only removes its own copies, after asking.
- Don't change the saved data in a way older versions can't read: add fields, don't rename them.

## Data (IndexedDB `vocalprep`)
- `lessons` {id, name, srcName, srcSize, day, dur, markers[{id,t,note}], hasAudio, view}; `lessonFiles` (the recording, by lesson id).
- `regions` {id, name, note, lessonId, lessonName, lessonDay, start, end, dur, instr (where the singing starts, s), peaks[300]};
  `regionAudio` (24-bit WAV blob, by region id).
- `days` {day: 'yyyy-mm-dd', items: [regionId]} — the Practise list of each day.
