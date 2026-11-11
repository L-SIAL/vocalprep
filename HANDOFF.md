# VocalPrep — change history

## v1 (11 Nov 2026)
First version, from the stage 1 / stage 2 mockups (https://claude.ai/artifact/9piM2qzGU89QgMjEyzqL87).
Grew out of the LH Audio Editor v1 (spectral-score PR #2, not merged).
- **Capture:** Lessons… › Open recording… (decoded with Web Audio; the file's bytes are kept in `lessonFiles`).
  Waveform with overview strip, ruler, markers (+ Marker / M, also while playing; notes in the Markers list, Copy / Share
  as text). Drag to select a region (snaps to markers), drag its edges, double-tap between markers (`regionBetweenMarkers`).
  **Add to repository** (Return) stores the region as its own 24-bit WAV with 3 ms fades (`sliceRange`, `wavBytes`)
  plus 300 peaks for the small waveform; named after the marker it starts at (`nameFor`).
  **Finish lesson** asks: remove the recording (regions stay) / keep it; then goes to Practise.
- **Practise:** today's list (`days[viewDay].items`). Drag a region from the Repository by ⋮⋮ (or tap +); drag ⋮⋮ in the
  list to reorder (`startDrag` / `dragMove` / `dragEnd`). Row: ▶, name (editable), lesson date · length · talk,
  small waveform (tap = play from there, drag the handle = where the singing starts, `r.instr`), Instructions /
  Sing along / ⟲ loop / Share / ✕ (out of this list), and the region's note (one note per region, every day).
  Day chips show earlier days. ▶ Play the list (2 s between regions). Export ▾: share the regions (WAV), join into one
  file (1 s gaps), share or copy names and notes as text.
- **Repository:** all regions grouped by lesson, search, "✓ today / last used / not used yet", ⋯ Rename / Share / Delete.
- **Keyboard** (top bar, both stages): A2–C4, no note names, keys don't light. A key plays the note (2 beats), a beat's
  rest, then 1-2-3-4-5-4-3-2-1 of its major scale, the last held 2 beats. Tempo 40–160 bpm, Volume (localStorage
  vpTempo / vpVol). Synthesised piano (`kbNote`): stretched partials, hammer position 1/7.5, three strings on the low
  partials, 3 ms attack, prompt + aftersound decay, darkening low-pass, felt knock, short reverb.
- Share sheet via `navigator.share({files})`; if iPadOS refuses because the gesture expired, a "Ready – Share" dialog
  asks for one more tap. Fallback: download.
- Tested headless (1180×820 and 820×1180): open WAV, markers, double-tap select, add 2 regions, finish (recording
  removed), + and drag into today's list, note, instr handle, Sing along, keyboard, share (download), reload restores.
  Not yet tested on the iPad itself.

## v2 (11 Nov 2026)
- **Backup ▾** (Repository header): **Back up to Dropbox…** asks first (the tap on Continue gives the share sheet a fresh
  gesture), then shares every region's WAV ("<name> - <id>.wav") plus "VocalPrep backup <date>.json" (regions with
  names, notes, singing starts, peaks, file names; the day lists). The user picks Save to Files › Dropbox › a folder.
  Last backup date in localStorage vpLastBackup, shown in the menu. **Restore from a backup…**: a multi-file picker
  (#restoreIn); takes the newest .json, matches WAVs by file name, adds regions that aren't here (keeps existing
  ones as they are) and merges the day lists. `backup()`, `restore()`; `shareFiles` now returns true when shared.
- **Keyboard:** range E2–C4 (`KB_LO` 40, was A2). What a key plays is a pattern (`PATTERNS`, segmented buttons
  in the dock, localStorage vpPattern): **Note** (default) sounds while the key is held and the dampers drop on release
  (`keyDown` / `keyUp`, `kbNote` now returns a handle with `release()`); **5 notes up & down** is the v1 behaviour.
  Add more patterns as `{ id, name, steps: [semitones…] }`. Tempo is disabled in Note mode. Dock is now two rows
  (controls, then keys); key width fits the space (`buildKeys`, rebuilt on resize).
- Opening a recording sets the waveform and the lesson together (a tap in between could hit an empty lesson).
- Tested headless: Note hold/release, pattern, backup (captured share files), restore into an empty app (2 regions,
  note and day list back), no errors.
