# Buster Block Shooter QA

## Passed

- Six Node rules tests: 0 failures, 0 skipped.
- All 40 level witnesses win with empty block boards and exhausted tank ammo.
- In-bounds nonoverlapping blocks and exact per-colour ammo/health totals on all levels.
- Front-of-queue gating, duplicate input rejection and five-bay capacity.
- Exposed-path checks, wrong-colour blocking, one ammo/HP per hit and spent tank departure.
- Exact Undo snapshot restoration, pause/resume, restart, five stranded tanks causing a jam, and Undo recovering from that jam.
- Headless Chromium real pointer playthroughs of levels 1, 20 and 40, including complete numbered-block clearing.
- Browser Next, pause/resume, mobile-scaled input at 360×740, and Undo; no page exceptions.
- Native project JSON parsing, object/function/image references and C3P ZIP CRC checks.

Evidence: `assets/validation.json`, `dist/browser-qa.json`, and screenshots in dist (also included in the source archive's QA directory).

## Unverified / limitations

- Construct editor opening, r506 compatibility, native ACE schemas, native Preview and official HTML5 export. Editor access was blocked in this environment; structural checks and browser tests do not validate native events.
- Browser audio listening/balance, Safari/Firefox, mobile hardware, assistive technology and human playtesting/difficulty calibration.
- Native project has no audio or persistent progress save, and its hint is a rule reminder. Browser version includes audio, local progress, level selection and a live legal-shot hint. Native Undo is implemented but runtime-unverified.
- No Poki SDK, interstitial ads or platform certification is included.

The HTML5 ZIP is the tested standalone browser companion, not a Construct-generated export. No claim of guaranteed session length, commercial performance or endless unique levels is made; the campaign contains 40 levels.

## C3P import repair

The initially delivered archive failed to open in the user's Construct editor. A comparison with 15 Construct-generated C3P examples found a packaging difference: native archives use backslash-separated ZIP entry names. The generator now matches that convention, emits editor-state files and uses a conventional project identifier. Checks now resolve project references using native archive paths and reject forward-slash entries. This repairs the observed packaging mismatch; editor acceptance of the rebuilt file remains unverified.

The archive-path revision was also reported to fail in Construct r506.3. Further comparison found sprite image identifiers had incorrectly reused the large event SID sequence; these now use separate small positive IDs, consistent with native examples. The actual loader exception is still needed to diagnose remaining import rejection. Neither revision is editor-verified.
