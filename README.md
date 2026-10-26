# Toy Traffic Trio

A 40-level traffic escape × triple-matching puzzle. Release cars along their roof arrows; three of the same vehicle type clear the seven-slot garage. All four edges are exits. No timer, move limit, lives, ads, purchases, login, or external services.

## Downloads

- `dist/ToyTrafficTrio.c3p`: native, editable Construct folder project packaged as C3P; targets r506. **Structurally checked, but not opened or previewed in Construct.**
- `dist/ToyTrafficTrio-HTML5.zip`: tested, independently implemented browser companion. **This is not an official Construct-generated export.**
- `dist/ToyTrafficTrio-Source.zip`: complete source, Construct folder project, editable level data, original assets, build tools, tests, and QA evidence.

The browser implementation and Construct project share the same 40 levels and art. Construct renders native Sprite and Text objects; the project contains no HTML overlay, iframe, external canvas renderer, third-party plugins, or paid addons. Gameplay runs in native event sheets and functions. Its only startup JavaScript loads campaign data.

## Play the browser build

Extract the HTML5 ZIP. In the extracted directory run `python -m http.server 8080`, then open the served `index.html` in a browser. Serve over HTTP; JavaScript modules do not reliably load from `file://`. No dependency installation is needed to play. Portrait 9:16 display scales to fit desktop and mobile screens.

Tap or click a vehicle to release it. A blocked tap highlights its first obstruction and never changes the logical board or consumes a move. One move resolves at a time. A seventh arrival that creates a triple clears before loss is checked. Win requires an empty board, no transit, and an empty tray.

- **Undo**: reverse accepted moves, including a loss or win. Unlimited and free.
- **Hint**: browser solver highlights a move with a complete winning continuation, or recommends Undo if none exists. Native Construct Hint highlights a legal exit and asks the player to check the tray; it does not promise that exit wins.
- **Restart**: replay the current level.
- **Pause**: pause between moves.
- **Sound**: toggle the original synthesized effects; browsers may require a gesture before audio.
- **40 levels**: browser campaign picker; all puzzles available. Construct uses arrows beside the level counter.
- Browser keyboard: arrow keys select vehicles, Enter/Space release, U undo, H hint, R restart, Escape pause. Tab exposes accessible control buttons. Native project uses mouse/touch controls.

New browser players enter level 1 immediately. Local browser storage remembers completed levels and the next puzzle; it is optional and failures are handled. Construct currently starts at level 1 on each new preview and has no persistent campaign save.

## Open in Construct 3

Open `ToyTrafficTrio.c3p` using Construct's **Open → File**, ideally in r506 or a later compatible release. Alternatively open `construct/project.c3proj` as a folder project. Run Preview and inspect errors before publishing. The full project includes JavaScript data-loading scripts and may require a Construct plan that supports scripting and the project's event count; it does not require paid addons.

**Environment limitation:** `editor.construct.net` returned HTTP 403 here. We could not confirm that the editor accepts this generated project, validate its ACE schemas with the editor, preview the native events, or create an official HTML5 export. JSON/reference/archive checks are not proof of engine compatibility. Do not treat this C3P as engine-certified or production-ready until those checks pass.

Native structure:

- `construct/layouts/Game.json`: Game, UI, and Overlay render layers, 540×960 viewport.
- `construct/eventSheets/Game.json`: all gameplay events, including `LoadLevel`, `CanExit`, `MatchKind`, `SortTray`, `Outcome`, `UndoMove`, and `Rebuild`.
- `Board` Array: authoritative occupied cells, 0 empty or vehicle ID + 1 occupied.
- `Vehicle` instance variables: integer grid anchors, direction, match type, phase, arrival order, tray slot, and animation data. Positions never determine puzzle legality.
- Phases: 0 board, 1 transit, 2 tray, 3 matched/hidden. Retained arrival history enables native Undo by rebuilding the grid and replaying matches.
- States: Loading, Playing, ResolvingMove, Paused, Won, Lost. There is no ad subsystem.
- `construct/scripts/campaign.js`: editable native campaign data.
- `construct/scripts/main.js`: campaign-data initialization only.

## Edit levels

The canonical source is `assets/levels.json`, a normal JSON array. Each level has `id`, `name`, `cols`, `rows`, `vehicles`, and a `solution` witness.

Each vehicle is `{ "id": 0, "type": 0, "x": 0, "y": 0, "d": 0 }`. IDs are unique within a level. Coordinates are zero-based; `(x,y)` is always the **topmost/leftmost occupied cell**, regardless of facing. Directions: 0 up, 1 right, 2 down, 3 left. Vertical vehicles occupy `(x,y)` and `(x,y+1)`; horizontal vehicles occupy `(x,y)` and `(x+1,y)`. Match type IDs: 0 red compact, 1 blue van, 2 yellow taxi, 3 green minibus, 4 purple delivery truck, 5 orange buggy.

Use six columns and six or seven rows. Do not overlap vehicles. Every type count must be divisible by three. `solution` lists vehicle IDs in a complete legal, tray-safe winning order. Diagnostic fields such as `initialBlocked`, `solutionPeakTray`, and `relief` describe generation but do not control gameplay. Update diagnostics when authoring levels; validation independently checks the actual grid and witness.

After editing data, run `npm run build` to sync the browser module and native campaign, validate witnesses, and package both projects. Then run `npm test`, `npm run validate`, and browser QA. Check native Preview separately. Editing `construct/scripts/campaign.js` directly works inside Construct but is overwritten by the next source build. The included `construct/files/levels.json` is a reference copy; the native runtime reads its script module.

`tools/levels.py` is the deterministic initial campaign generator. It **overwrites authored levels**; do not run it to sync edits.

## Development and checks

Playing requires only a modern browser and a static HTTP server. Building the C3P/source packages requires Python 3.12+, Pillow, ffmpeg with libopus, and Node.js 22+; no npm packages are required by gameplay. `requirements-dev.txt` and `package-lock.json` record development dependencies. Browser QA uses Playwright with system Chromium (`CHROMIUM_PATH` can override the executable).

```sh
npm ci --cache /tmp/toy-traffic-npm-cache
python -m pip install -r requirements-dev.txt
npm test
npm run validate
npm run build
```

For UI QA, keep `npm run serve` running in one terminal, then run `npm run test:browser` in another. `GAME_URL` can change the test server address. Tests simulate pointer input and advance the animation clock; they are not a human pacing study.

To regenerate the original art, run `python tools/art.py` (Pillow and the documented DejaVu system font path). All art and PCM audio are original generated assets. Vehicle silhouettes, details, colors and arrows distinguish the six types. The WAV originals and converted WebM/Opus files are included. No remote fonts or CDNs are used at runtime.

## Official Construct export

Once native Preview is verified, choose Construct's **Project → Export → Web/HTML5**, select the desired output options, export, and test the generated files through an HTTP server. Recheck touch input, audio unlock, resizing, undo after matching, both win/loss paths, and saved progress expectations. That official export step was not performed in this environment.

## Known limits

The pasted brief ended at “Keep all gameplay”, and no referenced visual image was attached. The supplied complete rules guided implementation; visuals are original. All levels are solvable and have machine-checked paths, but relative difficulty and long-term appeal need human playtesting. The native project is unverified in Construct, has a simpler legal-route cue, and has no persistent progress save. The tested browser game is a companion implementation, not a runtime validation of the C3P. Browser audio output was not audited by listening, and Safari/iOS/Android hardware testing remains outstanding. See `QA.md` for exact results.
