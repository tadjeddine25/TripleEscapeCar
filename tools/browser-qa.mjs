import {chromium} from 'playwright';import assert from 'node:assert/strict';import fs from 'node:fs';
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox']});
const page=await browser.newPage({viewport:{width:540,height:960},deviceScaleFactor:1});const errors=[],failed=[];page.on('pageerror',e=>errors.push(e.message));page.on('requestfailed',r=>failed.push(r.url()));
await page.clock.install();await page.goto(process.env.GAME_URL||'http://127.0.0.1:8080');await page.waitForFunction(()=>window.toyTraffic);await page.clock.runFor(50);
async function info(){return page.evaluate(()=>({state:toyTraffic.game.state,board:toyTraffic.game.board.length,tray:toyTraffic.game.tray.length,moves:toyTraffic.game.moves,matches:toyTraffic.game.matches}));}
async function tapCar(id){const p=await page.evaluate(id=>{const g=toyTraffic.game,v=g.board.find(v=>v.id===id);return {x:102+(v.x+(v.d%2?1:.5))*56,y:262+(7-g.level.rows)*28+(v.y+(v.d%2?.5:1))*56};},id);const r=await page.locator('canvas').boundingBox();await page.mouse.click(r.x+p.x*r.width/540,r.y+p.y*r.height/960);}
await tapCar(0);assert.equal((await info()).state,'ResolvingMove');await tapCar(1);assert.equal((await info()).moves,1);await page.clock.fastForward(650);assert.equal((await info()).state,'Playing');
await page.mouse.click(117,905);assert.equal((await info()).moves,0);assert.equal((await info()).board,6);await page.clock.runFor(25);
await page.mouse.click(474,178);assert.equal((await info()).state,'Paused');await tapCar(0);assert.equal((await info()).moves,0);await page.clock.runFor(40);await page.mouse.click(270,520);assert.equal((await info()).state,'Playing');
const results=[];
for(let level=0;level<40;level++){
 await page.evaluate(i=>toyTraffic.game.load(i),level);await page.clock.runFor(20);
 const sequence=await page.evaluate(()=>toyTraffic.game.level.solution);
 for(const id of sequence){await tapCar(id);assert.equal((await info()).state,'ResolvingMove',`level ${level+1} car ${id}`);await page.clock.fastForward(650);}
 const r=await info();assert.equal(r.state,'Won',`level ${level+1}`);assert.equal(r.tray,0);assert.equal(r.board,0);results.push({level:level+1,...r});
}
await page.clock.runFor(40);await page.screenshot({path:'dist/screenshot-win.png'});
// Next button replays campaign after level 40.
await page.mouse.click(270,520);assert.equal((await info()).state,'Playing');assert.equal(await page.evaluate(()=>toyTraffic.game.levelIndex),0);
// Native-scale pointer handling on a narrow touch viewport.
await page.setViewportSize({width:360,height:740});await page.clock.runFor(40);await page.screenshot({path:'dist/screenshot-mobile.png'});await tapCar(0);assert.equal((await info()).state,'ResolvingMove');await page.clock.fastForward(650);assert.equal((await info()).moves,1);
// Verify a blocked pointer tap cannot mutate game truth.
await page.evaluate(()=>toyTraffic.game.load(1));await page.clock.runFor(20);const blocked=await page.evaluate(async()=>{const {firstBlocker}=await import('./src/core.js');const g=toyTraffic.game;return g.board.find(v=>firstBlocker(v,g.board,g.level.cols,g.level.rows)!==null).id;});
const before=await info();await tapCar(blocked);assert.deepEqual(await info(),before);await page.clock.runFor(300);
// Progress can be stored without losing it on reload.
assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('toy-traffic-trio')).done.length),40);
assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);
const report={browser:'Chromium',levelsWonThroughPointerInput:results.length,rapidInput:true,undo:true,pauseResume:true,mobilePointer:true,blockedTap:true,nextButton:true,progressStored:true,pageErrors:errors,failedRequests:failed,results};fs.writeFileSync('dist/browser-qa.json',JSON.stringify(report,null,2));console.log(JSON.stringify({...report,results:undefined},null,2));await browser.close();
