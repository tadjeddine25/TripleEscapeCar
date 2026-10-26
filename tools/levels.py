"""Deterministic domino packing, dependency generation, and campaign witness generation."""
import random,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
rng=random.Random(250631)
DIR=[(0,-1),(1,0),(0,1),(-1,0)]
def cells(v):
 return [(v['x']+i*(v['d']%2),v['y']+i*(1-v['d']%2)) for i in range(2)]
def blocker(v,vs,w=6,h=6):
 occupied={p:o['id'] for o in vs if o['id']!=v['id'] for p in cells(o)}
 dx,dy=DIR[v['d']]; x,y=v['x'],v['y']
 if v['d']==1:x+=1
 if v['d']==2:y+=1
 x+=dx;y+=dy
 while 0<=x<w and 0<=y<h:
  if (x,y) in occupied:return occupied[x,y]
  x+=dx;y+=dy
 return None
def tiling(h):
 def fill(free,vs):
  if not free:return vs
  x,y=min(free,key=lambda p:(p[1],p[0]))
  options=[(1,0),(0,1)];rng.shuffle(options)
  for dx,dy in options:
   q=x+dx,y+dy
   if q in free:
    got=fill(free-{(x,y),q},vs+[dict(id=len(vs),x=x,y=y,d=1 if dx else 2)])
    if got:return got
 return fill({(x,y) for x in range(6) for y in range(h)},[])
def peel(vs,h):
 remaining=[v.copy() for v in vs];out=[]
 while remaining:
  opts=[]
  for v in remaining:
   for d in ([1,3] if v['d']%2 else [0,2]):
    a={**v,'d':d}
    if blocker(a,remaining,6,h) is None:opts.append(a)
  if not opts:return None
  a=rng.choice(opts);out.append(a);remaining=[v for v in remaining if v['id']!=a['id']]
 return out
levels=[]
names=['First little trio','Make some room','Crossroads','One at a time','A sunny detour','Van together','The blocker','Toy town','Room to breathe','Rush-hour rhythm','New neighbours','Mind the gap','Good company','Colour parade','Sunday drive','Busy boulevard','Side street','A perfect pocket','Taking turns','Easy does it','Full house','The long way','Traffic ballet','Six of a kind','Coastal cruise','Tangled avenues','Little logistics','Order of things','Gridlock garden','A quiet corner','Toy metropolis','Follow the arrows','Pocket planner','The grand shuffle','Scenic route','Bright bottleneck','Final stretch','Trio master','Almost home','The big send-off']
for n in range(1,41):
 count=6 if n==1 else 9 if n<=3 else 12 if n<=6 else 15 if n<=10 else (15 if n%5==0 else 18) if n<=20 else (18 if n%5==0 else 21)
 h=7 if count==21 else 6
 types=2 if n==1 else 3 if n<=4 else min(4 if n<=10 else 5 if n<=20 else 6,count//3)
 while True:
  vs=tiling(h);rng.shuffle(vs);vs=vs[:count]
  order=peel(vs,h)
  if not order:continue
  if n==1:
   # Six independent outward vehicles; every possible first-level ordering is safe.
   order=[dict(id=i,x=(i%3)*2,y=0 if i<3 else 4,d=0 if i<3 else 2) for i in range(6)]
  seq=sum(([i%types]*3 for i in range(count//3)),[])
  for _ in range(5000):
   rng.shuffle(seq);tray=[];peak=0
   for t in seq:
    tray.append(t)
    if tray.count(t)==3:tray=[a for a in tray if a!=t]
    peak=max(peak,len(tray))
    if len(tray)>=7:break
   else:break
  else:continue
  for v,t in zip(order,seq):v['type']=t
  deps=sum(blocker(v,order,6,h) is not None for v in order)
  if n==2 and deps==0:continue
  if n>3 and deps<count//3:continue
  break
 for i,v in enumerate(order):v['id']=i
 # Reassign IDs after dependency generation; witness is this exact peel ordering.
 levels.append(dict(id=n,name=names[n-1],cols=6,rows=h,vehicles=order,solution=[v['id'] for v in order],initialBlocked=deps,solutionPeakTray=peak,relief=n%5==0))
(ROOT/'assets/levels.json').write_text(json.dumps(levels,indent=2))
(ROOT/'src/campaign.js').write_text('export const LEVELS = '+json.dumps(levels,separators=(',',':'))+';\n')
print(f'Generated {len(levels)} levels')
