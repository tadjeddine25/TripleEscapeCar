# QA report

## Executed and passed

- Node.js rules suite: **9 tests passed, 0 failed, 0 skipped**.
- **40/40** campaign witness replays ended Won with empty board, no transit and empty tray.
- Independent current-state search found a winning path for **40/40** levels, and the rules tests replayed every returned path.
- Grid checks: unique IDs, no overlaps, in-bounds two-cell footprints, each match count divisible by three, and at least one initial legal exit in every level.
- All **720** first-level orderings completed safely. Level 2 contains blocked vehicles.
- Forward blocking checked in all four directions; blocked inputs preserved board, tray, history and move count.
- Seventh-slot triple resolved before loss; seven unmatched slots caused loss only after resolution.
- Repeated input and undo during transit were rejected. Pause/resume, restart, undo restoration, and structural deadlock detection passed.
- **Headless Chromium pointer-input campaign: 40/40 levels won** using real canvas click coordinates, with deterministic advancement of the animation clock.
- UI checks: Undo, pause/resume, Next after level 40, blocked taps, rapidly repeated taps, progress stored for all 40 completions, and narrow 360×740 pointer scaling passed.
- UI run reported **0 page exceptions and 0 failed asset requests**.
- Screenshots inspected: first puzzle, dense final puzzle, win overlay, and mobile viewport. All original art/audio assets are local.
- C3P structural checks: project JSON parsed; all object, function, instance-variable, image, script, sound and icon references resolved; basic expression delimiter checks passed; archive CRC passed and its files matched the folder project. Only built-in Construct plugins are declared. Gameplay event sheet contains no JavaScript actions or external renderers.

Machine-readable evidence: `assets/validation.json`, `dist/browser-qa.json`, and `dist/construct-structural-qa.json`. Source ZIP includes QA evidence and screenshots under `QA/`.

## Not verified

- **Construct editor open, r506 compatibility, ACE-schema acceptance, native runtime preview, native gameplay execution, and official Construct HTML5 export.** The editor host returned HTTP 403. Structural checks do not establish that the C3P opens or runs.
- Native event sheet behavior is implemented but is not covered by the browser companion's runtime tests.
- Native campaign persistence is not implemented; browser progress storage is implemented and tested.
- Native Hint shows a legal exit; browser Hint uses a complete winning-path search. Their guarantees differ.
- Actual speaker output/listening, audio balance on mobile hardware, Safari/Firefox, iOS/Android devices, long sessions, accessibility assistive-device testing, human difficulty calibration and user retention.
- No reference image was available; the pasted specification was truncated. No claims depend on the missing content.

## Delivery status

The browser companion is playable and passed the checks above. The generated native C3P is editable source with structural validation, supplied for editor verification. The browser ZIP is explicitly **not an official Construct export**. A completed Construct editor-open/preview test and an official export remain outstanding.
