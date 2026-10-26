import {LEVELS} from './campaign.js';
import {Game,DIR,TYPES} from './core.js';
const canvas=document.querySelector('#game'),ctx=canvas.getContext('2d'),images={},sounds={},buttons=[];
const assetNames=['background-6','background-7','modal','hand',...Array.from({length:6},(_,i)=>'vehicle-'+i),...['undo','hint','restart','pause','sound','previous','forward','next','retry','resume','levels'].map(n=>'button-'+n)];
await Promise.all(assetNames.map(name=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{images[name]=im;resolve();};im.onerror=()=>reject(Error('Missing asset '+name));im.src='assets/'+name+'.png';})));
for(const name of ['release','blocked','match','win','tap']){sounds[name]=new Audio('assets/'+name+'.wav');sounds[name].preload='auto';}
let prefs={level:0,done:[],muted:false};try{Object.assign(prefs,JSON.parse(localStorage.getItem('toy-traffic-trio')||'{}'));}catch{}
function save(){try{localStorage.setItem('toy-traffic-trio',JSON.stringify(prefs));}catch{}}
let anim=null,bump=null,highlight=null,particles=[],panel=false,now=0,focus=-1,toast='',toastUntil=0;
function play(n){if(prefs.muted)return;const s=sounds[n].cloneNode();s.volume=.36;s.play().catch(()=>{});}
function change(event,data){
 if(event==='release'){anim={...data,start:performance.now()};play('release');}
 if(event==='blocked'){bump={id:data.vehicle.id,start:performance.now()};highlight={id:data.blocker,until:performance.now()+500};toast='A neighbour is in the way.';toastUntil=performance.now()+1600;play('blocked');}
 if(event==='match'){play('match');for(let i=0;i<36;i++)particles.push({x:270,y:790,vx:(Math.random()-.5)*380,vy:-120-Math.random()*240,life:1,color:['#ec7775','#e8bd57','#7db39a','#9b8bc5'][i%4]});}
 if(event==='win'){play('win');prefs.done=[...new Set([...prefs.done,game.levelIndex])];prefs.level=Math.min(39,game.levelIndex+1);save();}
 if(event==='load'){anim=null;bump=null;highlight=null;particles=[];toast='';toastUntil=0;focus=-1;panel=false;}
 if(event==='undo'){anim=null;play('tap');}
 const live=document.querySelector('#live');if(live&&event!=='release')live.textContent=event==='load'?'Puzzle loaded.':event==='blocked'?'Blocked. Move the highlighted neighbour first.':event;
}
const game=new Game(LEVELS,change);game.load(Number.isInteger(prefs.level)?prefs.level:0);
window.toyTraffic={game,levels:LEVELS}; // Exposed for QA and level-authoring checks.
document.querySelector('#notice').remove();
function fit(){const ratio=540/960,w=Math.min(innerWidth,innerHeight*ratio);canvas.style.width=w+'px';canvas.style.height=w/ratio+'px';}
addEventListener('resize',fit);fit();
function im(name,x,y,w,h){ctx.drawImage(images[name],x,y,w??images[name].width,h??images[name].height);}
function text(s,x,y,size=18,color='#365e54',weight=600){ctx.fillStyle=color;ctx.font=`${weight} ${size}px "Trebuchet MS", system-ui, sans-serif`;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(s,x,y);}
function round(x,y,w,h,r,fill,stroke){ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fillStyle=fill;ctx.fill();if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=2;ctx.stroke();}}
function button(name,x,y,action,enabled=true){const a=images['button-'+name];ctx.globalAlpha=enabled?1:.44;im('button-'+name,x,y);ctx.globalAlpha=1;if(enabled)buttons.push({x,y,w:a.width,h:a.height,action});}
function pos(v){const top=262+(7-game.level.rows)*28;return {x:102+(v.x+(v.d%2?1:.5))*56,y:top+(v.y+(v.d%2?.5:1))*56};}
function vehicle(v,x,y,w=50,h=100,angle=v.d*Math.PI/2,alpha=1){ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.globalAlpha=alpha;im('vehicle-'+v.type,-w/2,-h/2,w,h);ctx.restore();}
function trayPos(i){return {x:78+i*64,y:787};}
function ease(t){return t*t*(3-2*t);}function lerp(a,b,t){return a+(b-a)*t;}
function makeHint(){const result=game.hint();if(!result)return;if(result.path?.length){highlight={id:result.path[0],until:performance.now()+2600};toast='This car has a winning route.';}else toast=result.limited?'Try a matching pair, or undo.':'This tray has no winning route. Try Undo.';toastUntil=performance.now()+2400;play('tap');}
function restart(){if(game.state==='ResolvingMove')return;game.load(game.levelIndex);play('tap');}
function next(){if(game.state!=='Won')return;game.load(game.levelIndex===39?0:game.levelIndex+1);play('tap');}
function pause(){if(panel){panel=false;game.resume();return;}if(game.state==='Paused')game.resume();else game.pause();}
function openLevels(){if(game.state!=='Playing')return;game.pause();panel=true;}
function draw(t,dt){now=t;buttons.length=0;ctx.setTransform(2,0,0,2,0,0);ctx.clearRect(0,0,540,960);im('background-'+game.level.rows,0,0);
 text('LEVEL '+String(game.levelIndex+1).padStart(2,'0')+' / 40',270,167,14,'#4c7668',800);
 text(game.level.name,270,207,20,'#2e5a50',700);
 button('restart',43,152,restart,game.state!=='ResolvingMove');button('sound',451,87,()=>{prefs.muted=!prefs.muted;save();});if(prefs.muted)text('×',474,109,27,'#be655f');
 button('pause',451,152,pause,game.state==='Playing'||game.state==='Paused');
 let info=toastUntil>t?toast:game.message;text(info,270,238,13,'#6c8b7c',500);
 const active=game.state==='Playing';
 for(const v of game.board){let p=pos(v),shake=0;
  if(bump?.id===v.id){const age=(t-bump.start)/1000;if(age<.3)shake=Math.sin(age*60)*(1-age/.3)*5;else bump=null;}
  if(highlight?.id===v.id&&highlight.until>t){const cellsW=v.d%2?112:56,cellsH=v.d%2?56:112;round(p.x-cellsW/2-3,p.y-cellsH/2-3,cellsW+6,cellsH+6,14,'#fff2b590','#f4c857');}
  if(focus===v.id&&active){ctx.setLineDash([4,3]);round(p.x-(v.d%2?58:30),p.y-(v.d%2?30:58),v.d%2?116:60,v.d%2?60:116,12,'#ffffff00','#567f71');ctx.setLineDash([]);}
  vehicle(v,p.x+DIR[v.d][0]*shake,p.y+DIR[v.d][1]*shake);
 }
 const transit=game.transit;
 for(let i=0;i<game.tray.length;i++){
  const v=game.tray[i];let x=trayPos(i).x;
  if(transit&&anim){const future=transit.result.arrival<=i?i+1:i;x=lerp(x,trayPos(future).x,ease(Math.min(1,(t-anim.start)/300)));}
  vehicle(v,x,787,27,54,0);
 }
 if(transit&&anim){const age=(t-anim.start)/1000,p=pos(transit.vehicle),[dx,dy]=DIR[transit.vehicle.d],exit={x:dx>0?500:dx<0?40:p.x,y:dy<0?262+(7-game.level.rows)*28-65:dy>0?262+(7-game.level.rows)*28+game.level.rows*56+65:p.y},dest=trayPos(transit.slot);
  if(age<.21){let a=ease(age/.21);vehicle(transit.vehicle,lerp(p.x,exit.x,a),lerp(p.y,exit.y,a),50,100,transit.vehicle.d*Math.PI/2,1-a*.35);}
  else {let a=ease(Math.min(1,(age-.21)/.31));vehicle(transit.vehicle,lerp(exit.x,dest.x,a),lerp(exit.y,dest.y,a)-Math.sin(a*Math.PI)*65,lerp(50,27,a),lerp(100,54,a),transit.vehicle.d*Math.PI/2*(1-a));}
  if(age>=.52){anim=null;game.resolve();}
 }
 if(game.levelIndex===0&&game.moves===0&&active){const p=pos(game.board[0]);im('hand',p.x+12,p.y+12+Math.sin(t/260)*5,42,42);}
 text(`${game.tray.length}${transit?' + 1':''} / 7 parked   ·   ${game.matches} ${game.matches===1?'trio':'trios'} cleared`,270,860,12,'#688879',500);
 button('undo',50,881,()=>game.undo(),game.history.length>0&&game.state!=='ResolvingMove'&&game.state!=='Paused');
 button('hint',202,881,makeHint,active);button('levels',354,881,openLevels,active);
 for(const p of particles){p.life-=dt*1.6;p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=550*dt;ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.life*5);ctx.globalAlpha=Math.max(0,p.life);ctx.fillStyle=p.color;ctx.fillRect(-3,-3,6,10);ctx.restore();}particles=particles.filter(p=>p.life>0);
 if(['Won','Lost','Paused'].includes(game.state)){
  buttons.length=0;im('modal',0,0);
  if(panel){round(43,252,454,473,30,'#f8fbef');text('A town of little puzzles',270,286,23,'#315f52',800);text('Choose a level. Every road is open.',270,316,13,'#78917f',500);
   for(let i=0;i<40;i++){let x=67+(i%8)*51,y=344+Math.floor(i/8)*57;round(x,y,44,45,12,prefs.done.includes(i)?'#6caa90':i===game.levelIndex?'#f0c66b':'#e4ecdf');text(i+1,x+22,y+23,16,prefs.done.includes(i)?'#fff':'#49715e');buttons.push({x,y,w:44,h:45,action:()=>game.load(i)});}
   button('resume',149,655,()=>{panel=false;game.resume();});
  }else{
   const won=game.state==='Won',lost=game.state==='Lost';text(won?(game.levelIndex===39?'Trio master!':'Beautifully untangled!'):lost?'A little traffic jam':'A little breather',270,407,26,'#315f52',800);
   text(won?`${game.matches} trios cleared · ${game.moves} clever moves`:lost?'The next good move is an Undo away.':'Your little cars will wait for you.',270,450,14,'#78917f',500);
   button(won?'next':lost?'retry':'resume',149,498,won?next:lost?restart:()=>game.resume());
   if(lost){button('undo',203,568,()=>game.undo(),game.history.length>0);}else text(won?'Made room for something lovely.':'No rush. No timer.',270,588,13,'#8b9c87',500);
  }
 }
}
canvas.addEventListener('pointerdown',e=>{e.preventDefault();canvas.focus();const r=canvas.getBoundingClientRect(),x=(e.clientX-r.left)*540/r.width,y=(e.clientY-r.top)*960/r.height;
 for(let i=buttons.length-1;i>=0;i--){const b=buttons[i];if(x>=b.x&&x<=b.x+b.w&&y>=b.y&&y<=b.y+b.h){b.action();return;}}
 if(game.state!=='Playing')return;
 for(const v of [...game.board].reverse()){const p=pos(v),w=v.d%2?108:52,h=v.d%2?52:108;if(Math.abs(x-p.x)<=w/2&&Math.abs(y-p.y)<=h/2){focus=v.id;game.request(v.id);return;}}
});
canvas.addEventListener('keydown',e=>{if(['ArrowRight','ArrowDown','ArrowLeft','ArrowUp',' ','Enter'].includes(e.key))e.preventDefault();if(e.key.toLowerCase()==='u')game.undo();if(e.key.toLowerCase()==='h')makeHint();if(e.key.toLowerCase()==='r')restart();if(e.key==='Escape')pause();
 if(game.state==='Playing'){const vs=game.board;if(e.key.startsWith('Arrow')){const ix=vs.findIndex(v=>v.id===focus);focus=vs[(ix+(['ArrowLeft','ArrowUp'].includes(e.key)?-1:1)+vs.length)%vs.length]?.id;document.querySelector('#live').textContent=TYPES[vs.find(v=>v.id===focus)?.type]+' selected';}if(e.key===' '||e.key==='Enter'){game.request(focus<0?vs[0]?.id:focus);}}
 else if(game.state==='Won'&&e.key==='Enter')next();
});
for(const [id,fn] of Object.entries({undo:()=>game.undo(),hint:makeHint,restart,pause,next}))document.querySelector('#a-'+id).onclick=fn;
let last=performance.now();function frame(t){const dt=Math.min(.05,(t-last)/1000);last=t;draw(t,dt);requestAnimationFrame(frame);}requestAnimationFrame(frame);
