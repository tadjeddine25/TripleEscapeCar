import fs from 'node:fs';
let seed=61723;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;}
const levels=[];
for(let i=0;i<40;i++){let rows=i===0?2:i<4?3:i<10?4:i<20?5:6,types=i===0?2:Math.min(6,3+Math.floor(i/8)),blocks=[],tanks=[];
 for(let y=0;y<rows;y++){let x=0;while(x<6){const w=Math.min(6-x,i===0?3:1+rand(3)),hp=i===0?3:3+rand(Math.min(10,4+Math.floor(i/5)));blocks.push({id:blocks.length,x,y,w,hp,maxHP:hp,color:rand(types)});x+=w;}}
 const order=[...blocks].sort((a,b)=>b.y-a.y||a.x-b.x);
 for(const b of order){const id=tanks.length;tanks.push({id,col:id%3,order:Math.floor(id/3),color:b.color,ammo:b.hp});}
 levels.push({id:i+1,name:i===0?'First shots':i%5===4?'A clear horizon':['Castle courtyard','Colour blockade','Breakthrough','The narrow path'][i%4],cols:6,rows,blocks,tanks,solution:tanks.map(t=>t.id)});
}
fs.writeFileSync('assets/levels.json',JSON.stringify(levels,null,2));fs.writeFileSync('src/campaign.js','export const LEVELS='+JSON.stringify(levels)+';\n');console.log('40 campaigns generated');
