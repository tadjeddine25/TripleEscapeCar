export const DIR = [[0,-1],[1,0],[0,1],[-1,0]];
export const TYPES = ['Red compact','Blue van','Yellow taxi','Green minibus','Purple delivery truck','Orange buggy'];
export function cells(v) {return [0,1].map(i=>[v.x+(v.d%2)*i,v.y+(1-v.d%2)*i]);}
export function firstBlocker(v, board, cols, rows) {
 const occupied=new Map(); for(const o of board) if(o.id!==v.id) for(const [x,y] of cells(o)) occupied.set(x+','+y,o.id);
 const [dx,dy]=DIR[v.d];let x=v.x+(v.d===1?1:0)+dx,y=v.y+(v.d===2?1:0)+dy;
 while(x>=0&&x<cols&&y>=0&&y<rows){if(occupied.has(x+','+y))return occupied.get(x+','+y);x+=dx;y+=dy;}return null;
}
export function insertAndMatch(tray,v) {
 const next=[...tray,v].sort((a,b)=>a.type-b.type);
 const match=next.filter(o=>o.type===v.type);
 return {tray:match.length===3?next.filter(o=>o.type!==v.type):next,matched:match.length===3?match:[],arrival:next.findIndex(o=>o.id===v.id)};
}
export function solve(level,board=level.vehicles,tray=[],limit=300000) {
 const all=board, n=all.length,full=(1<<n)-1,memo=new Set();let nodes=0;
 function dfs(mask,counts){
  if(++nodes>limit)return null;
  if(mask===0)return counts.every(c=>c===0)?[]:null;
  const key=mask+':'+counts.join('');if(memo.has(key))return null;
  const remaining=all.filter((v,i)=>mask&(1<<i));
  const options=remaining.filter(v=>firstBlocker(v,remaining,level.cols,level.rows)===null).sort((a,b)=>counts[b.type]-counts[a.type]);
  for(const v of options){const next=counts.slice();next[v.type]=(next[v.type]+1)%3;if(next.reduce((a,b)=>a+b,0)>=7)continue;
   const i=all.indexOf(v),tail=dfs(mask&~(1<<i),next);if(tail)return [v.id,...tail];}
  memo.add(key);return null;
 }
 const counts=Array(6).fill(0);for(const v of tray)counts[v.type]++;
 return {path:dfs(full,counts),nodes,limited:nodes>limit};
}
export class Game {
 constructor(levels,onChange=()=>{}) {this.levels=levels;this.onChange=onChange;this.levelIndex=0;this.state='Loading';this.load(0);}
 load(index){this.levelIndex=Math.max(0,Math.min(this.levels.length-1,index));this.level=this.levels[this.levelIndex];this.board=structuredClone(this.level.vehicles);this.tray=[];this.transit=null;this.history=[];this.moves=0;this.matches=0;this.state='Playing';this.message=this.levelIndex===0?'Tap a car.':this.levelIndex===1?'Clear the way for a neighbour.':'Follow the arrows. Make a trio.';this.onChange('load');}
 legal(){return this.board.filter(v=>firstBlocker(v,this.board,this.level.cols,this.level.rows)===null);}
 request(id){
  if(this.state!=='Playing')return {accepted:false,reason:'state'};
  const v=this.board.find(o=>o.id===id);if(!v)return {accepted:false,reason:'missing'};
  const blocker=firstBlocker(v,this.board,this.level.cols,this.level.rows);
  if(blocker!==null){this.onChange('blocked',{vehicle:v,blocker});return {accepted:false,reason:'blocked',blocker};}
  if(this.tray.length>=7)return {accepted:false,reason:'capacity'};
  this.history.push({board:structuredClone(this.board),tray:structuredClone(this.tray),moves:this.moves,matches:this.matches,message:this.message});
  const result=insertAndMatch(this.tray,v);this.state='ResolvingMove';this.board=this.board.filter(o=>o.id!==id);this.transit={vehicle:v,slot:result.arrival,result};this.moves++;this.onChange('release',this.transit);return {accepted:true};
 }
 resolve(){
  if(this.state!=='ResolvingMove'||!this.transit)return false;
  const {result}=this.transit;this.tray=result.tray;this.transit=null;
  if(result.matched.length){this.matches++;this.onChange('match',result.matched);}
  if(!this.board.length&&!this.tray.length){this.state='Won';this.message='A little order. A big smile.';this.onChange('win');}
  else if(this.tray.length>=7){this.state='Lost';this.message='The garage is full. Undo or try again.';this.onChange('loss');}
  else if(this.board.length&&!this.legal().length){this.state='Lost';this.message='No open routes. Undo or try again.';this.onChange('deadlock');}
  else {this.state='Playing';this.message=this.levelIndex===0&&this.moves===1?'Match 3 to clear!':result.matched.length?'Lovely trio! Room for the next.':'Find your next little trio.';this.onChange('resolved');}
  return true;
 }
 undo(){if(this.state==='ResolvingMove'||this.state==='Paused'||!this.history.length)return false;const s=this.history.pop();Object.assign(this,s);this.transit=null;this.state='Playing';this.onChange('undo');return true;}
 pause(){if(this.state!=='Playing')return false;this.state='Paused';this.onChange('pause');return true;}
 resume(){if(this.state!=='Paused')return false;this.state='Playing';this.onChange('resume');return true;}
 hint(){if(this.state!=='Playing')return null;return solve(this.level,this.board,this.tray);}
}
