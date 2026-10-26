import test from 'node:test';import assert from 'node:assert/strict';
import {LEVELS} from '../src/campaign.js';import {Game,firstBlocker,insertAndMatch,cells,solve} from '../src/core.js';
test('40 campaigns have exact grids, unique ids, valid counts, and executable witnesses',()=>{
 assert.equal(LEVELS.length,40);
 for(const level of LEVELS){const occ=new Set(),ids=new Set(),counts=Array(6).fill(0);
  for(const v of level.vehicles){assert(!ids.has(v.id));ids.add(v.id);counts[v.type]++;for(const [x,y] of cells(v)){assert(x>=0&&x<level.cols&&y>=0&&y<level.rows);assert(!occ.has(x+','+y));occ.add(x+','+y);}}
  assert(counts.every(c=>c%3===0));const g=new Game([level]);assert(g.legal().length>0);
  for(const id of level.solution){assert(g.request(id).accepted,`level ${level.id}, car ${id}`);assert.equal(g.state,'ResolvingMove');g.resolve();assert.notEqual(g.state,'Lost');}
  assert.equal(g.state,'Won');assert.equal(g.board.length,0);assert.equal(g.tray.length,0);assert.equal(g.transit,null);
 }
});
test('first level: all 720 choices are safe and always finish',()=>{
 function visit(board,tray){if(!board.length){assert.equal(tray.length,0);return;}for(const v of board){assert.equal(firstBlocker(v,board,6,6),null);const next=insertAndMatch(tray,v);assert(next.tray.length<7);visit(board.filter(o=>o.id!==v.id),next.tray);}}visit(LEVELS[0].vehicles,[]);
});
test('blocked taps preserve board, history, tray and moves; first obstruction is reported',()=>{
 const g=new Game([LEVELS[1]]),v=g.board.find(v=>firstBlocker(v,g.board,6,6)!==null),before=JSON.stringify(g.board);
 assert(v);const r=g.request(v.id);assert.equal(r.reason,'blocked');assert.equal(JSON.stringify(g.board),before);assert.equal(g.moves,0);assert.equal(g.history.length,0);assert.equal(g.tray.length,0);
});
test('forward ray handles up, right, down and left and checks full path',()=>{
 for(let d=0;d<4;d++){let v={id:0,type:0,x:2,y:2,d};const [dx,dy]=[[0,-1],[1,0],[0,1],[-1,0]][d];let b={id:1,type:0,x:2+dx*2,y:2+dy*2,d};if(dx<0)b.x=0;if(dy<0)b.y=0;
 assert.equal(firstBlocker(v,[v,b],6,6),1);assert.equal(firstBlocker(v,[v],6,6),null);}
});
test('matching ignores direction, groups types and clears seventh arriving triple before loss',()=>{
 const tray=[0,0,1,1,2,3].map((type,id)=>({type,id,d:id%4}));const result=insertAndMatch(tray,{type:0,id:99,d:3});assert.equal(result.matched.length,3);assert.equal(result.tray.length,4);
 const g=new Game([LEVELS[0]]);g.tray=tray;g.board=[{type:0,id:99,d:0,x:0,y:0}];assert(g.request(99).accepted);g.resolve();assert.notEqual(g.state,'Lost');assert.equal(g.tray.length,4);
});
test('seven unmatched slots lose only on resolution',()=>{const g=new Game([LEVELS[0]]);g.tray=[0,0,1,1,2,2].map((type,id)=>({type,id:id+10}));g.board=[{id:0,type:3,x:0,y:0,d:0}];assert(g.request(0).accepted);assert.equal(g.state,'ResolvingMove');g.resolve();assert.equal(g.state,'Lost');});
test('atomic inputs, pause, undo, restart and win gate',()=>{const g=new Game([LEVELS[0]]);const before=JSON.stringify(g.board);assert(g.pause());assert(!g.request(0).accepted);assert(!g.undo());g.resume();assert(g.request(0).accepted);assert(!g.request(0).accepted);assert(!g.request(1).accepted);assert(!g.undo());assert(!g.pause());g.resolve();assert(g.undo());assert.equal(JSON.stringify(g.board),before);assert.equal(g.moves,0);assert.equal(g.tray.length,0);g.request(0);g.resolve();g.load(0);assert.equal(g.history.length,0);assert.equal(g.board.length,6);});
test('structural deadlock after resolved move is detected',()=>{const g=new Game([LEVELS[0]]);g.board=[{id:0,type:0,x:0,y:0,d:0},{id:1,type:1,x:1,y:2,d:1},{id:2,type:1,x:3,y:2,d:3}];assert(g.request(0).accepted);g.resolve();assert.equal(g.state,'Lost');assert.match(g.message,/No open routes/);});
test('hint solver supplies complete winning paths for all shipped levels',()=>{for(const l of LEVELS){const r=solve(l);assert(r.path,`level ${l.id} limit=${r.limited}`);const g=new Game([l]);for(const id of r.path){assert(g.request(id).accepted);g.resolve();}assert.equal(g.state,'Won');}});
