export const COLORS=['#39adfa','#ffbd35','#65ce40','#f15b9a','#9671ef','#e3e4df'];
export const NAMES=['Blue','Gold','Green','Pink','Purple','Pearl'];
export function exposed(block,blocks){for(let x=block.x;x<block.x+block.w;x++)if(!blocks.some(b=>b.id!==block.id&&b.hp>0&&b.y>block.y&&x>=b.x&&x<b.x+b.w))return true;return false;}
export function target(tank,blocks){return blocks.filter(b=>b.hp>0&&b.color===tank.color&&exposed(b,blocks)).sort((a,b)=>b.y-a.y||a.x-b.x)[0]||null;}
export class Game{
 constructor(levels,onEvent=()=>{}){this.levels=levels;this.onEvent=onEvent;this.load(0);}
 load(n){this.index=Math.max(0,Math.min(this.levels.length-1,n));this.level=this.levels[this.index];this.blocks=structuredClone(this.level.blocks);this.tanks=structuredClone(this.level.tanks).map(t=>({...t,phase:'queue',bay:-1}));this.state='Playing';this.history=[];this.shots=0;this.launched=0;this.onEvent('load');}
 front(){return this.tanks.filter(t=>t.phase==='queue'&&!this.tanks.some(o=>o.phase==='queue'&&o.col===t.col&&o.order<t.order));}
 active(){return this.tanks.filter(t=>t.phase==='active');}
 launch(id){if(this.state!=='Playing')return false;let t=this.front().find(t=>t.id===id);if(!t||this.active().length>=5)return false;this.history.push({blocks:structuredClone(this.blocks),tanks:structuredClone(this.tanks),shots:this.shots,launched:this.launched});let occupied=this.active().map(t=>t.bay);t.bay=[0,1,2,3,4].find(b=>!occupied.includes(b));t.phase='active';this.launched++;this.onEvent('launch',t);return true;}
 step(){if(this.state!=='Playing')return [];let hits=[];for(const t of this.active()){const b=target(t,this.blocks);if(!b)continue;b.hp--;t.ammo--;this.shots++;hits.push({tank:structuredClone(t),block:structuredClone(b)});this.onEvent('hit',{tank:t,block:b});if(t.ammo===0){t.phase='spent';this.onEvent('depart',t);}}
 this.blocks=this.blocks.filter(b=>b.hp>0);
 if(!this.blocks.length){this.state='Won';this.onEvent('win');}
 else if(!this.active().some(t=>target(t,this.blocks))&&(this.active().length===5||!this.front().length)){this.state='Lost';this.onEvent('jam');}return hits;}
 undo(){if(!this.history.length||this.state==='Paused')return false;Object.assign(this,this.history.pop());this.state='Playing';this.onEvent('undo');return true;}
 pause(){if(this.state!=='Playing')return false;this.state='Paused';return true;}
 resume(){if(this.state!=='Paused')return false;this.state='Playing';return true;}
 hint(){return this.front().find(t=>target(t,this.blocks))||null;}
}
