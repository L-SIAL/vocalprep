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
