from PIL import Image,ImageDraw,ImageFont,ImageFilter
import pathlib,math,wave,struct
R=pathlib.Path(__file__).resolve().parents[1];A=R/'assets';A.mkdir(exist_ok=True)
S=3
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def canvas(w,h):return Image.new('RGBA',(w*S,h*S))
def box(d,xy,r,fill,outline=None,width=1):d.rounded_rectangle(tuple(int(a*S) for a in xy),r*S,fill,outline,width*S)
def ellipse(d,xy,fill):d.ellipse(tuple(int(a*S) for a in xy),fill)
def line(d,xy,fill,w=1):d.line(tuple((int(x*S),int(y*S)) for x,y in xy),fill,width=w*S,joint='curve')
def text(d,xy,s,size,fill,anchor='mm'):d.text((xy[0]*S,xy[1]*S),s,font=ImageFont.truetype(F,size*S),fill=fill,anchor=anchor)
def save(im,name):im.resize((im.width//S,im.height//S),Image.Resampling.LANCZOS).save(A/name)
colors=['#ed6264','#5795ef','#f2bf48','#5ebd92','#a284d4','#ed9853']
for t,c in enumerate(colors):
 im=canvas(100,200);d=ImageDraw.Draw(im)
 box(d,(9,13,94,197),21,'#1c3f4b35');box(d,(2,39,18,73),5,'#29434d');box(d,(82,39,98,73),5,'#29434d');box(d,(2,135,18,170),5,'#29434d');box(d,(82,135,98,170),5,'#29434d')
 shape=[(11,10,89,188),(10,9,90,190),(11,10,89,188),(9,8,91,190),(9,8,91,190),(15,15,85,185)][t]
 box(d,shape,19,'#344d5b');box(d,(shape[0],shape[1],shape[2],shape[3]-6),19,c)
 box(d,(18,14,82,30),8,'#ffffff55');box(d,(17,164,83,180),7,'#00000015')
 box(d,(19,39,81,79),10,'#234c64');box(d,(22,42,78,53),5,'#b4e4e4');line(d,[(25,69),(61,45)],'#ffffff55',4)
 box(d,(20,127,80,158),9,'#234c64');box(d,(24,130,76,137),4,'#b4e4e4')
 if t==1:
  box(d,(18,89,82,119),6,'#d7eafa');line(d,[(50,90),(50,118)],c,4)
 if t==2:
  box(d,(23,91,77,115),5,'#fff5cc');text(d,(50,103),'TAXI',11,'#614a29')
 if t==3:
  for x in [19,53]:box(d,(x,88,x+28,118),5,'#d7f1de')
 if t==4:
  box(d,(17,85,83,155),6,'#d9c8f0')
  for y in [96,111,126,141]:line(d,[(21,y),(79,y)],'#9879bf',3)
 if t==5:
  line(d,[(24,88),(76,151)],'#ffdfb6',7);line(d,[(76,88),(24,151)],'#ffdfb6',7)
 # Arrow points to FRONT, independent of body variant.
 d.polygon([(50*S,84*S),(68*S,103*S),(57*S,103*S),(57*S,120*S),(43*S,120*S),(43*S,103*S),(32*S,103*S)],fill='#ffffff',outline='#294453')
 for x in [20,67]:box(d,(x,22,x+13,30),3,'#fff8d1')
 for x in [18,72]:box(d,(x,169,x+10,175),3,'#b73446')
 save(im,f'vehicle-{t}.png')
for rows in [6,7]:
 im=canvas(540,960);d=ImageDraw.Draw(im)
 for y in range(960):
  a=y/960;col=tuple(int(q*(1-a)+z*a) for q,z in zip((240,247,242),(219,237,228)))
  d.rectangle((0,y*S,540*S,(y+1)*S),fill=col)
 # Soft abstract garden forms.
 for x,y,r in [(-20,185,68),(544,490,65),(33,700,34),(500,155,30)]:ellipse(d,(x-r,y-r,x+r,y+r),'#d2e7d6')
 text(d,(270,45),'THE LITTLE PUZZLE CLUB',10,'#65887d')
 text(d,(270,85),'Toy Traffic Trio',34,'#254e4b')
 text(d,(270,122),'Small cars. Clever moves.',13,'#70918a')
 box(d,(197,150,343,184),17,'#ffffff');
 y0=262+(7-rows)*28;bh=rows*56
 box(d,(63,y0-39,480,y0+bh+48),39,'#b8cfc2');box(d,(60,y0-44,480,y0+bh+40),37,'#fafff8')
 box(d,(67,y0-37,473,y0+bh+33),30,'#8da3a1')
 box(d,(76,y0-28,464,y0+bh+24),24,'#a6b8b3')
 for x in range(94,459,28):
  line(d,[(x,y0-22),(x+13,y0-22)],'#e8f0d9',2);line(d,[(x,y0+bh+18),(x+13,y0+bh+18)],'#e8f0d9',2)
 for y in range(y0,round(y0+bh),28):
  line(d,[(82,y),(82,y+13)],'#e8f0d9',2);line(d,[(458,y),(458,y+13)],'#e8f0d9',2)
 box(d,(98,y0-4,442,y0+bh+4),13,'#647f78');box(d,(102,y0,438,y0+bh),10,'#d9e5d3')
 for y in range(rows):
  for x in range(6):box(d,(104+x*56,y0+2+y*56,156+x*56,y0+54+y*56),6,'#e4eddc' if (x+y)%2==0 else '#dce7d6')
 # Garden corner studs.
 for x,y in [(67,y0-38),(469,y0-38),(67,y0+bh+25),(469,y0+bh+25)]:
  ellipse(d,(x-9,y-9,x+9,y+9),'#719f73');ellipse(d,(x-5,y-7,x+7,y+5),'#9abd86')
 text(d,(270,716),'YOUR MATCHING GARAGE',11,'#54786e')
 box(d,(35,742,505,844),22,'#b6cec0');box(d,(35,737,505,837),22,'#f9fcf5')
 for i in range(7):
  x=49+i*64;box(d,(x,751,x+58,821),12,'#dfe8dc');box(d,(x+3,754,x+55,818),10,'#eaf0e4');text(d,(x+29,787),str(i+1),14,'#c0cebd')
 text(d,(270,938),'NO TIMER  ·  JUST ONE GOOD MOVE',10,'#7a9789')
 save(im,f'background-{rows}.png')
# Button art with baked labels, native Sprite clickable objects.
for name,label,w,c in [('undo','↶  Undo',134,'#fffdf5'),('hint','✧  Hint',134,'#fffdf5'),('restart','↻',46,'#ffffff'),('pause','Ⅱ',46,'#ffffff'),('sound','♪',46,'#ffffff'),('previous','‹',38,'#ffffff'),('forward','›',38,'#ffffff'),('next','Next level  →',242,'#3d8271'),('retry','Try again',242,'#3d8271'),('resume','Keep playing',242,'#3d8271'),('levels','40 levels',112,'#fffdf5')]:
 im=canvas(w,54);d=ImageDraw.Draw(im);box(d,(0,4,w,54),17,'#adc7b8');box(d,(0,0,w,49),17,c);text(d,(w/2,24),label,18 if w>100 else 24,'#ffffff' if c=='#3d8271' else '#39695c');save(im,f'button-{name}.png')
im=canvas(540,960);d=ImageDraw.Draw(im);d.rectangle((0,0,540*S,960*S),fill='#183e39b8');box(d,(43,302,497,648),30,'#f8fbef');text(d,(270,347),'✦  ✦  ✦',31,'#e0ad43');save(im,'modal.png')
im=canvas(64,64);d=ImageDraw.Draw(im);ellipse(d,(5,5,59,59),'#fdf5d4');text(d,(32,32),'☝',32,'#5c8175');save(im,'hand.png')
# Deterministic original PCM sound assets, no external downloads.
for name,notes,duration in [('release',[420,630],.15),('blocked',[160,130],.13),('match',[523,659,784],.28),('win',[523,659,784,1047],.50),('tap',[560],.06)]:
 rate=22050;pcm=[]
 for i in range(int(rate*duration)):
  t=i/rate;seg=min(len(notes)-1,int(t/duration*len(notes)));phase=t*notes[seg]*math.tau
  env=math.sin(math.pi*(t/duration))**1.4
  pcm.append(int(8000*env*(math.sin(phase)+.2*math.sin(phase*2))/1.2))
 with wave.open(str(A/f'{name}.wav'),'w') as f:f.setparams((1,2,rate,0,'NONE','not compressed'));f.writeframes(struct.pack('<'+'h'*len(pcm),*pcm))
print('Original sprite, UI, background and audio assets generated')
