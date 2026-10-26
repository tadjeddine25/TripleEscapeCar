# Buster Block Shooter

Tap the tanks. Shoot the blocks. Clear the board.

A complete replacement of the previous game: colour-matched tanks, numbered castle blocks, five firing bays, three tank queues, automatically aimed shots, ammo management, and 40 editable campaign levels. Original tank sprites, backgrounds and shooting sounds are included. No downloaded commercial game assets are used.

## Play

Extract `dist/BusterBlockShooter-HTML5.zip` and run `python -m http.server 8080` from that directory. Open the served page in a modern browser. JavaScript modules require HTTP rather than opening the file directly. No dependency installation is needed to play.

Tap the **front tank in any of three queues** to deploy it into a free firing bay. Tanks automatically aim at matching-colour blocks that have at least one clear vertical path from below. Each hit costs one ammo and removes one block HP. Blocks remain fixed until their number reaches zero; then their occupied cells become available for shots at blocks above. Spent tanks leave their bay. Up to five tanks can shoot simultaneously, one hit per tank every 160 ms. The player chooses deployment order, not individual shot targets.

Clear all blocks to win. If all five bays contain stranded tanks with no matching exposed target, the board jams. Undo returns to the exact state immediately before the most recent deployment, including damage, tank ammo and queue order. Restart is always available. There is no timer, limited lives, login, or purchase flow.

The browser game supports sound/mute, undo, hint, restart, pause/resume, a 40-level picker and local progress storage. Hint identifies a front tank that can shoot now; it does not certify a full winning continuation. The queue shows its first three rows and advances as tanks deploy. Controls: mouse or touch; keyboard 1/2/3 deploys from each column, U undo, H hint, R restart, Escape pause. Tab exposes control buttons.

## Construct project

`dist/BusterBlockShooter.c3p` is the generated native project targeting Construct 3 r506; `construct/project.c3proj` is its editable folder form. Open with Construct's Open → File and run Preview. All gameplay/rendering uses native Sprite, Text, Touch, JSON and Array objects with native event sheets/functions. Startup JavaScript loads campaign data only. There is no HTML overlay or external canvas inside the C3P. A plan that supports scripting and the project's event count may be required; no third-party or paid addons are used.

Native implementation includes tank queues, five bays, colour/exposure checks, ammo/HP, bullets, win/jam detection, restart, undo and pause. The browser has richer effects, original audio, progress persistence, the level picker and the actionable hint; native preview currently has no audio or persistent progress and its hint provides a rule reminder. This is a separate native implementation, not a wrapper around the browser canvas.

**Construct editor opening, ACE compatibility and runtime behavior have not been tested.** The editor host was inaccessible in this environment. Structural reference/ZIP checks do not prove that the C3P opens or plays correctly. Test native Preview before relying on the project. The browser ZIP is an independently tested companion, **not an official Construct HTML5 export**. To obtain an official export, open/verify the native project and use Construct's Web/HTML5 export workflow, then test the generated output through HTTP.

## Levels and editing

`assets/levels.json` is canonical. Every level contains `cols`, `rows`, `blocks`, `tanks` and a legal `solution` deployment order. Blocks use `{id,x,y,w,hp,maxHP,color}`: six logical columns, row zero at the top, width in cells, one row tall. Tanks use `{id,col,order,color,ammo}`: three queue columns with increasing depth. Colour IDs: 0 blue, 1 gold, 2 green, 3 pink, 4 purple, 5 pearl. Unique IDs and nonoverlapping blocks are required. Total ammo equals block HP for each colour in all shipped levels.

Edit the JSON and its winning `solution`, then run `npm run build` to synchronize both campaign modules, validate, generate the C3P and package the downloads. `tools/levels.mjs` is the deterministic initial generator; running it **overwrites authored levels**. Native campaign edits inside `construct/scripts/campaign.js` work in Construct but are overwritten by the next source build.

The native `Board` Array stores occupied cells by block ID. `History` stores HP, ammo, phase and bay snapshots for Undo; animations never decide puzzle truth. Event functions include LoadLevel, QueueRank, FreeBay, FindTarget, Shoot, Volley, Snapshot and UndoMove.

## Development

Use Node.js 22+ and Python 3.12+. Building requires Pillow (`requirements-dev.txt`). Browser QA requires Playwright and a system Chromium executable (`CHROMIUM_PATH` overrides its path).

```sh
npm ci --cache /tmp/buster-npm-cache
python -m pip install -r requirements-dev.txt
npm test
npm run build
npm run serve
# In another terminal:
npm run test:browser
```

`GAME_URL` overrides the browser QA server URL. Art can be regenerated with `python tools/art.py`; it uses the DejaVu Sans system font path documented in that script. No remote fonts, trackers, ad libraries or network services are required at runtime. Poki ads/SDK have not been integrated; hosting on Poki still requires its onboarding and lifecycle/ad integration.

The supplied reference guided the castle setting, palette, block numerals and tank staging; artwork is newly generated. The prototype campaign has machine-checked solutions, not human difficulty calibration. See QA.md for executed checks and outstanding native/hardware testing.
