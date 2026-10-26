from PIL import Image,ImageDraw,ImageFont
import pathlib,math,struct,wave
R=pathlib.Path(__file__).resolve().parents[1];A=R/'assets';S=2
C=['#39adfa','#ffbd35','#65ce40','#f15b9a','#9671ef','#e3e4df'];F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def new(w,h):return Image.new('RGBA',(w*S,h*S))
def box(d,xy,r,c):d.rounded_rectangle([int(v*S) for v in xy],r*S,fill=c)
def ell(d,xy,c):d.ellipse([int(v*S) for v in xy],fill=c)
def text(d,x,y,t,size,c):d.text((x*S,y*S),t,font=ImageFont.truetype(F,size*S),anchor='mm',fill=c)
def save(im,n):im.resize((im.width//S,im.height//S),Image.Resampling.LANCZOS).save(A/n)
for i,c in enumerate(C):
 im=new(96,112);d=ImageDraw.Draw(im);ell(d,(4,88,94,110),'#39474744');box(d,(3,35,25,101),9,'#344458');box(d,(71,35,93,101),9,'#344458')
 for y in range(42,97,13):
  box(d,(6,y,22,y+6),2,'#768091');box(d,(74,y,90,y+6),2,'#768091')
 box(d,(20,37,77,103),15,'#3b5770');box(d,(19,31,77,95),15,c);box(d,(24,36,72,45),6,'#ffffff77');ell(d,(27,28,70,72),'#294c6c');ell(d,(29,24,68,65),c);box(d,(39,2,57,41),5,'#294b65');box(d,(41,0,55,34),4,c);box(d,(42,1,54,7),2,'#ffffffaa');box(d,(30,67,67,86),6,'#16395055');save(im,f'tank-{i}.png')
 im=new(144,64);d=ImageDraw.Draw(im);box(d,(1,4,143,64),10,'#4e5b59');box(d,(1,0,143,58),10,c);box(d,(6,4,138,15),6,'#ffffff44');box(d,(7,48,137,56),5,'#00000018');save(im,f'block-{i}.png')
im=new(540,960);d=ImageDraw.Draw(im)
for y in range(960):
 a=min(1,y/800);co=tuple(int(x*(1-a)+z*a) for x,z in zip((93,198,250),(255,234,182)));d.rectangle((0,y*S,540*S,(y+1)*S),fill=co)
for x,y in [(30,60),(420,100),(300,20)]:
 for dx,dy,r in [(0,0,22),(25,-10,30),(57,0,24)]:ell(d,(x+dx-r,y+dy-r,x+dx+r,y+dy+r),'#ffffffcc')
# Original castle silhouettes and banners.
for x in [3,456]:
 box(d,(x,155,x+80,560),4,'#d6c8a3');box(d,(x-8,137,x+88,178),3,'#eee3c0')
 for dx in [0,30,60]:box(d,(x+dx,120,x+dx+18,156),2,'#eee3c0')
 for y in range(195,550,80):box(d,(x+30,y,x+47,y+30),7,'#9aa98f')
 d.polygon([(int((x+30)*S),80*S),(int((x+30)*S),113*S),(int((x+66)*S),95*S)],fill='#f27c67')
box(d,(28,201,512,623),22,'#aa9b87');box(d,(43,214,497,607),12,'#7c8985');box(d,(49,219,491,603),8,'#dbe2d0')
for x in range(30,510,28):
 for y in [200,605]:box(d,(x,y,x+26,y+22),4,'#e2ddcb');box(d,(x+2,y+1,x+24,y+5),2,'#f7f2e1')
for y in range(222,600,28):
 for x in [28,490]:box(d,(x,y,x+22,y+26),4,'#e2ddcb')
box(d,(41,629,499,703),24,'#c1b79b');box(d,(41,624,499,697),22,'#f4edd8')
for i in range(5):box(d,(51+i*88,633,129+i*88,688),13,'#647484');box(d,(55+i*88,637,125+i*88,683),11,'#7b8997')
# Path with garden edges.
for y in range(720,960,47):
 for x in [0,435]:
  ell(d,(x,y,x+95,y+32),'#87ba5a');ell(d,(x+8,y-5,x+76,y+18),'#b0d76b')
for y in range(718,960,40):
 for x in range(98,430,65):box(d,(x+(y%3)*8,y,x+52+(y%3)*8,y+20),7,'#f5deb0')
save(im,'background.png')
for name,label,w in [('undo','Undo',112),('hint','Hint',112),('restart','↻',48),('pause','Ⅱ',48),('sound','♪',48),('next','Next level →',242),('retry','Try again',242),('resume','Keep blasting',242),('levels','Levels',112)]:
 im=new(w,50);d=ImageDraw.Draw(im);box(d,(0,5,w,50),14,'#775130');box(d,(0,0,w,44),14,'#e99136' if w==242 else '#fff4dc');text(d,w/2,23,label,18,'#fff' if w==242 else '#725536');save(im,f'button-{name}.png')
for name,notes,dur in [('shot',[700,350],.07),('break',[400,600,900],.18),('win',[523,659,784,1047],.45),('launch',[240,420],.12)]:
 rate=22050;data=[]
 for i in range(int(dur*rate)):
  t=i/rate;f=notes[min(len(notes)-1,int(t/dur*len(notes)))];data.append(int(5000*math.sin(t*f*math.tau)*(1-t/dur)**2))
 with wave.open(str(A/f'{name}.wav'),'w') as f:f.setparams((1,2,rate,0,'NONE',''));f.writeframes(struct.pack('<'+'h'*len(data),*data))
