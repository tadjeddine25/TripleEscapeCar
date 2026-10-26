"""Generate a native Construct 3 folder project and zipped C3P. No third-party addons.
Gameplay uses event sheets; JavaScript only supplies editable campaign data at startup.
"""
import json,pathlib,shutil,itertools,subprocess,zipfile
from PIL import Image
R=pathlib.Path(__file__).resolve().parents[1];P=R/'construct';A=R/'assets'
for f in ['objectTypes','layouts','eventSheets','images','scripts','sounds','files','icons']:(P/f).mkdir(parents=True,exist_ok=True)
sids=itertools.count(250000000001);uids=itertools.count(1)
def sid():return next(sids)
def write(path,data):path.write_text(json.dumps(data,indent=2))
def folder(items=None):return dict(items=[] if items is None else items,subfolders=[])
objects=[];instances=[];nonworld=[]
def var(n,t='number'):return dict(name=n,type=t,desc='',show=True,sid=sid())
def sprite(name,files,variables=[]):
 frames=[]
 for i,f in enumerate(files):
  w,h=Image.open(A/f).size;shutil.copyfile(A/f,P/'images'/f'{name.lower()}-default-{i:03}.png')
  frames.append(dict(width=w,height=h,originX=.5,originY=.5,originalSource='',exportFormat='lossless',exportQuality=.8,fileType='image/png',imageSpriteId=sid(),useCollisionPoly=True,collisionPoly={'points':[0,0,1,0,1,1,0,1]},duration=1,tag=''))
 write(P/'objectTypes'/f'{name}.json',dict(name=name,**{'plugin-id':'Sprite'},sid=sid(),isGlobal=False,editorNewInstanceIsReplica=True,instanceVariables=[var(v) for v in variables],behaviorTypes=[],effectTypes=[],animations=folder([dict(frames=frames,sid=sid(),name='Default',isLooping=False,isPingPong=False,repeatCount=1,repeatTo=0,speed=0)])))
 objects.append(name)
def inst(name,x,y,w,h,iv={},props=None,origin=.5):
 uid=next(uids);s=sid();o=dict(type=name,properties=props or {'initially-visible':True,'initial-animation':'Default','initial-frame':0,'enable-collisions':True},uid=uid,sid=s,tags='',instanceVariables=iv,behaviors={},instanceFolderItem={'sid':s,'expanded':True},showing=True,locked=False,world=dict(x=x,y=y,width=w,height=h,originX=origin,originY=origin,color=[1,1,1,1],angle=0,zElevation=0))
 instances.append(o);return o
sprite('Backdrop',['background-6.png','background-7.png']);inst('Backdrop',270,480,540,960)
vvars=['vid','kind','gx','gy','dir','phase','arrival','slot','sx','sy','ex','ey','flash','bump']
sprite('Vehicle',[f'vehicle-{i}.png' for i in range(6)],vvars);inst('Vehicle',-100,-100,50,100,{v:0 for v in vvars})
sprite('Hand',['hand.png']);inst('Hand',150,330,42,42)
sprite('Modal',['modal.png']);inst('Modal',270,480,540,960)
buttons={'Undo':('undo',117,908,134,54),'Hint':('hint',269,908,134,54),'Restart':('restart',66,179,46,54),'Pause':('pause',474,179,46,54),'Sound':('sound',474,114,46,54),'Previous':('previous',168,167,38,54),'Forward':('forward',372,167,38,54),'Next':('next',270,525,242,54),'Retry':('retry',270,525,242,54),'Resume':('resume',270,525,242,54)}
for n,(asset,x,y,w,h) in buttons.items():sprite(n,[f'button-{asset}.png']);inst(n,x,y,w,h)
texts=[('LevelLabel',270,167,140,30,14),('LevelName',270,207,440,30,20),('Message',270,238,460,26,13),('TrayLabel',270,860,450,24,12),('ModalTitle',270,405,434,52,25),('ModalCaption',270,450,430,42,14),('FooterLabel',409,905,126,42,11)]
for n,x,y,w,h,size in texts:
 objects.append(n);write(P/'objectTypes'/f'{n}.json',dict(name=n,**{'plugin-id':'Text'},sid=sid(),isGlobal=False,instanceVariables=[],behaviorTypes=[],effectTypes=[]))
 inst(n,x-w/2,y-h/2,w,h,props={'text':'','enable-bbcode':True,'font':'Arial','size':size,'line-height':0,'bold':True,'italic':False,'color':[.20,.36,.31,1],'horizontal-alignment':'center','vertical-alignment':'center','wrapping':'word','text-direction':'ltr','icon-set':-1,'initially-visible':True,'origin':'top-left','read-aloud':False},origin=0)
for name,plugin,props in [('Campaign','Json',{}),('Board','Arr',{'width':6,'height':7,'depth':1})]:
 objects.append(name);write(P/'objectTypes'/f'{name}.json',dict(name=name,**{'plugin-id':plugin},sid=sid(),isGlobal=True,instanceVariables=[]))
 nonworld.append(dict(type=name,properties=props,uid=next(uids),sid=sid(),tags='',instanceVariables={}))
for name,props in [('Touch',{'use-mouse-input':True}),('Audio',{'timescale-audio':'sounds-only','save-load':'all','play-in-background':False,'latency-hint':'interactive','enable-multiple-tags':True,'panning-model':'hrtf','distance-model':'inverse','listener-z-height':600,'reference-distance':600,'maximum-distance':10000,'roll-off-factor':1})]:
 objects.append(name);write(P/'objectTypes'/f'{name}.json',dict(name=name,**{'plugin-id':name},sid=sid(),**{'singleglobal-inst':dict(type=name,properties=props,uid=next(uids),sid=sid(),tags='')}))
# JSON event helpers: expressions are Construct expressions, never JavaScript.
def ace(obj,id,**params):
 o=dict(id=id,objectClass=obj,sid=sid())
 if params:o['parameters']=params
 return o
def sy(id,**p):return ace('System',id,**p)
def setg(n,v):return sy('set-eventvar-value',variable=n,value=str(v))
def setv(n,v):return ace('Vehicle','set-instvar-value',**{'instance-variable':n,'value':str(v)})
def cmp(a,b,op=0):return sy('compare-two-values',**{'first-value':str(a),'comparison':op,'second-value':str(b)})
def cv(n,v,op=0):return ace('Vehicle','compare-instance-variable',**{'instance-variable':n,'comparison':op,'value':str(v)})
def call(n,*args):return dict(callFunction=n,sid=sid(),**({'parameters':list(args)} if args else {}))
def event(conds=[],acts=[],children=[]):
 o=dict(eventType='block',conditions=conds,actions=acts,sid=sid())
 if children:o['children']=children
 return o
def fn(n,args=[],acts=[],children=[]):
 return dict(functionName=n,functionDescription='',functionCategory='Toy Traffic Trio',functionReturnType='none',functionCopyPicked=False,functionIsAsync=False,functionParameters=[dict(name=a,type='number',initialValue='0',comment='',sid=sid()) for a in args],eventType='function-block',conditions=[],actions=acts,sid=sid(),children=children)
def foreach():return sy('for-each',object='Vehicle')
def loop(n,end,start='0'):return sy('for',name=json.dumps(n),**{'start-index':start,'end-index':str(end)})
def at(x,y,v):return ace('Board','set-at-xy',x=x,y=y,value=v)
def opacity(obj,v):return ace(obj,'set-opacity',opacity=str(v))
def txt(obj,v):return ace(obj,'set-text',text=v)
def position(x,y):return ace('Vehicle','set-position',x=x,y=y)
def sound(name):return call('PlaySound',str(['release','blocked','match','win','tap'].index(name)))
def comment(s):return dict(eventType='comment',text=s)
E=[]
variables={'CampaignJSON':('string',''),'Level':('number','0'),'Rows':('number','6'),'Total':('number','6'),'Top':('number','290'),'State':('string','Loading'),'Moves':('number','0'),'Matches':('number','0'),'TrayCount':('number','0'),'Selected':('number','0'),'Blocker':('number','0'),'RayX':('number','0'),'RayY':('number','0'),'DX':('number','0'),'DY':('number','0'),'MoveAge':('number','0'),'MatchCount':('number','0'),'Remaining':('number','0'),'Legal':('number','0'),'HintID':('number','-1'),'Muted':('number','0')}
for n,(t,v) in variables.items():E.append(dict(eventType='variable',name=n,type=t,initialValue=v,comment='',isStatic=False,isConstant=False,sid=sid()))
E.append(comment('NATIVE GAMEPLAY. Grid uses Board Array (0 empty; vehicle ID + 1 occupied). Sprite phase: 0 board, 1 transit, 2 tray, 3 matched. Grid anchors never follow animation positions.'))
E.append(event([sy('on-start-of-layout')],[ace('Campaign','parse',data='CampaignJSON'),call('LoadLevel')]))
# Data expressions into the loaded campaign JSON; count is explicit for old JSON plugin compatibility.
def data(key,i=None):return 'Campaign.Get(str(Level) & ".'+('vehicles." & loopindex("spawn") & ".' if i is not None else '')+key+'")'
E.append(fn('LoadLevel',acts=[setg('State','"Loading"'),ace('Vehicle','destroy'),setg('Rows',data('rows')),setg('Total',data('count')),setg('Top','262 + (7-Rows)*28'),setg('Moves','0'),setg('Matches','0'),setg('TrayCount','0'),ace('Board','set-size',width='6',height='7',depth='1'),ace('Board','clear'),ace('Backdrop','set-animation-frame',**{'frame-number':'Rows-6'}),txt('Message','Level=0 ? "Tap a car." : Level=1 ? "Clear the way for a neighbour." : "Follow the arrows. Make a trio."')],children=[
 event([loop('spawn','Total-1')],[sy('create-object',**{'object-to-create':'Vehicle','layer':'"Game"','x':'-100','y':'-100','create-hierarchy':False,'template-name':'""'}),*[setv(n,data(key,True)) for n,key in [('vid','id'),('kind','type'),('gx','x'),('gy','y'),('dir','d')]],setv('phase',0),setv('arrival',0),setv('flash',0),setv('bump',0),ace('Vehicle','set-animation-frame',**{'frame-number':'Vehicle.kind'}),ace('Vehicle','set-angle',angle='Vehicle.dir*90')]),
 event(acts=[call('Rebuild'),setg('State','"Playing"')])]))
# Rebuild grid from anchors and rebuild tray by replaying retained arrival order. This provides unbounded Undo without opaque engine snapshots.
E.append(fn('Rebuild',acts=[ace('Board','clear'),setg('Matches',0)],children=[
 event([foreach()],[setv('phase','Vehicle.arrival=0 ? 0 : 3')]),
 event([cv('phase',0),foreach()],[at('Vehicle.gx','Vehicle.gy','Vehicle.vid+1'),at('Vehicle.gx+(Vehicle.dir%2)','Vehicle.gy+(1-Vehicle.dir%2)','Vehicle.vid+1')]),
 event([loop('history','Moves','1')],children=[event([cv('arrival','loopindex("history")')],[setv('phase',2),call('MatchKind','Vehicle.kind')])]),
 event(acts=[call('SortTray')])]))
# Path checks scan beyond front bumper to every boundary cell, taking the first obstruction.
E.append(fn('CanExit',['candidate'],acts=[setg('Blocker',0)],children=[event([cv('vid','candidate')],[setg('RayX','Vehicle.gx+(Vehicle.dir=1 ? 1 : 0)'),setg('RayY','Vehicle.gy+(Vehicle.dir=2 ? 1 : 0)'),setg('DX','Vehicle.dir=1 ? 1 : Vehicle.dir=3 ? -1 : 0'),setg('DY','Vehicle.dir=2 ? 1 : Vehicle.dir=0 ? -1 : 0')]),event([loop('ray',7, '1'),cmp('Blocker',0),cmp('RayX+DX*loopindex("ray")',0,5),cmp('RayX+DX*loopindex("ray")',6,2),cmp('RayY+DY*loopindex("ray")',0,5),cmp('RayY+DY*loopindex("ray")','Rows',2),cmp('Board.At(RayX+DX*loopindex("ray"),RayY+DY*loopindex("ray"))',0,4)],[setg('Blocker','Board.At(RayX+DX*loopindex("ray"),RayY+DY*loopindex("ray"))')])]))
E.append(comment('Input is accepted only while Playing. The entire move reserves one slot and resolves before input resumes.'))
E.append(event([ace('Touch','on-tap-object',object='Vehicle'),cmp('State','"Playing"'),cv('phase',0)],[setg('Selected','Vehicle.vid'),call('CanExit','Selected')],children=[
 event([cmp('Blocker',0),cmp('TrayCount',7,2)],[setg('State','"ResolvingMove"'),setg('Moves','Moves+1'),setg('MoveAge',0),setv('arrival','Moves'),setv('phase',1),setv('sx','Vehicle.X'),setv('sy','Vehicle.Y'),setv('ex','Vehicle.dir=1 ? 500 : Vehicle.dir=3 ? 40 : Vehicle.X'),setv('ey','Vehicle.dir=0 ? Top-65 : Vehicle.dir=2 ? Top+Rows*56+65 : Vehicle.Y'),at('Vehicle.gx','Vehicle.gy','0'),at('Vehicle.gx+(Vehicle.dir%2)','Vehicle.gy+(1-Vehicle.dir%2)','0'),sound('release')]),
 event([cmp('Blocker',0,4)],[setv('bump','time+.28'),txt('Message','"A neighbour is in the way."'),sound('blocked')],children=[event(acts=[call('FlashBlocker')])])]))
# Native animation. All authoritative grid mutation happened once in the accepted move event above.
E.append(event([sy('every-tick')],children=[
 event([cv('phase',0),foreach()],[position('102+(Vehicle.gx+(Vehicle.dir%2=1 ? 1 : .5))*56+(Vehicle.bump>time ? sin((Vehicle.bump-time)*2200)*4 : 0)','Top+(Vehicle.gy+(Vehicle.dir%2=1 ? .5 : 1))*56'),ace('Vehicle','set-size',width='50',height='100'),ace('Vehicle','set-angle',angle='Vehicle.dir*90'),opacity('Vehicle','Vehicle.flash>time ? 55+45*sin(time*1800) : 100')]),
 event([cv('phase',2),foreach()],[position('lerp(Vehicle.X,78+Vehicle.slot*64,min(1,dt*18))','lerp(Vehicle.Y,787,min(1,dt*18))'),ace('Vehicle','set-size',width='27',height='54'),ace('Vehicle','set-angle',angle='0'),opacity('Vehicle',100)]),
 event([cv('phase',3)],[opacity('Vehicle',0)]),
 event([cmp('State','"ResolvingMove"')],[setg('MoveAge','MoveAge+dt')],children=[
  event([cv('phase',1),cmp('MoveAge','.21',2)],[position('lerp(Vehicle.sx,Vehicle.ex,MoveAge/.21)','lerp(Vehicle.sy,Vehicle.ey,MoveAge/.21)')]),
  event([cv('phase',1),cmp('MoveAge','.21',5)],[position('lerp(Vehicle.ex,78+TrayCount*64,min(1,(MoveAge-.21)/.31))','lerp(Vehicle.ey,787,min(1,(MoveAge-.21)/.31))-sin(min(1,(MoveAge-.21)/.31)*180)*65'),ace('Vehicle','set-size',width='lerp(50,27,min(1,(MoveAge-.21)/.31))',height='lerp(100,54,min(1,(MoveAge-.21)/.31))'),ace('Vehicle','set-angle',angle='Vehicle.dir*90*(1-min(1,(MoveAge-.21)/.31))')]),
  event([cv('phase',1),cmp('MoveAge','.52',5)],[setv('phase',2),call('MatchKind','Vehicle.kind'),call('SortTray'),call('Outcome')])]),
 event(acts=[txt('LevelLabel','"LEVEL " & (Level+1) & " / 40"'),txt('LevelName',data('name')),txt('TrayLabel','TrayCount & " / 7 parked   ·   " & Matches & " trios cleared"'),txt('FooterLabel','"40 levels\n‹ choose above ›"'),opacity('Hand','Level=0 & Moves=0 & State="Playing" ? 100 : 0'),opacity('Modal','State="Won" | State="Lost" | State="Paused" ? 100 : 0'),opacity('ModalTitle','State="Won" | State="Lost" | State="Paused" ? 100 : 0'),opacity('ModalCaption','State="Won" | State="Lost" | State="Paused" ? 100 : 0'),opacity('Next','State="Won" ? 100 : 0'),opacity('Retry','State="Lost" ? 100 : 0'),opacity('Resume','State="Paused" ? 100 : 0'),txt('ModalTitle','State="Won" ? "Beautifully untangled!" : State="Lost" ? "A little traffic jam" : "A little breather"'),txt('ModalCaption','State="Won" ? Matches & " trios cleared · " & Moves & " clever moves" : State="Lost" ? "Undo or try a different order." : "Your little cars will wait for you."'),opacity('Undo','Moves>0 & State<>"ResolvingMove" & State<>"Paused" ? 100 : 40'),opacity('Hint','State="Playing" ? 100 : 40'),opacity('Sound','Muted=0 ? 100 : 40')])]))
# Matching is always checked before tray-full loss.
E.append(fn('MatchKind',['matchType'],acts=[setg('MatchCount',0)],children=[event([cv('phase',2),cv('kind','matchType'),foreach()],[setg('MatchCount','MatchCount+1')]),event([cmp('MatchCount',3),cv('phase',2),cv('kind','matchType')],[setv('phase',3),opacity('Vehicle',0),setg('Matches','Matches+1'),sound('match')])]))
E.append(fn('SortTray',acts=[setg('TrayCount',0)],children=[event([loop('types',5)],children=[event([cv('phase',2),cv('kind','loopindex("types")'),foreach()],[setv('slot','TrayCount'),setg('TrayCount','TrayCount+1')])])]))
E.append(fn('Outcome',acts=[setg('Remaining',0),setg('Legal',0),setg('State','"Playing"'),txt('Message','Level=0 & Moves=1 ? "Match 3 to clear!" : "Find your next little trio."')],children=[event([cv('phase',0),foreach()],[setg('Remaining','Remaining+1'),call('CanExit','Vehicle.vid')],children=[event([cmp('Blocker',0)],[setg('Legal','Legal+1')])]),event([cmp('Remaining',0),cmp('TrayCount',0)],[setg('State','"Won"'),sound('win')]),event([cmp('TrayCount',7)],[setg('State','"Lost"')]),event([cmp('Remaining',0,4),cmp('Legal',0)],[setg('State','"Lost"'),txt('Message','"No open routes. Undo or try again."')])]))
E.append(fn('UndoMove',acts=[setg('State','"Loading"')],children=[event([cv('arrival','Moves')],[setv('arrival',0)]),event(acts=[setg('Moves','Moves-1'),call('Rebuild'),call('Outcome'),sound('tap')])]))
for obj,conds,acts in [
 ('Undo',[cmp('Moves',0,4),cmp('State','"ResolvingMove"',1),cmp('State','"Paused"',1)],[call('UndoMove')]),
 ('Restart',[cmp('State','"ResolvingMove"',1)],[call('LoadLevel')]),
 ('Retry',[cmp('State','"Lost"')],[call('LoadLevel')]),
 ('Next',[cmp('State','"Won"')],[setg('Level','(Level+1)%40'),call('LoadLevel')]),
 ('Previous',[cmp('State','"Playing"')],[setg('Level','(Level+39)%40'),call('LoadLevel')]),
 ('Forward',[cmp('State','"Playing"')],[setg('Level','(Level+1)%40'),call('LoadLevel')]),
 ('Pause',[cmp('State','"Playing"')],[setg('State','"Paused"')]),
 ('Resume',[cmp('State','"Paused"')],[setg('State','"Playing"')]),
 ('Sound',[],[setg('Muted','1-Muted')]),
 ('Hint',[cmp('State','"Playing"')],[call('FindHint')])]:E.append(event([ace('Touch','on-tap-object',object=obj),*conds],acts))
# A native route cue highlights an open exit; browser companion has a full current-state solver.
E.append(fn('FindHint',acts=[setg('HintID',-1)],children=[event([cv('phase',0),foreach(),cmp('HintID',-1)],[call('CanExit','Vehicle.vid')],children=[event([cmp('Blocker',0)],[setg('HintID','Vehicle.vid'),setv('flash','time+2'),txt('Message','"An open route. Check your tray first."')])])]))
E.append(fn('FlashBlocker',children=[event([cv('vid','Blocker-1')],[setv('flash','time+.5')])]))
E.append(fn('PlaySound',['soundID'],children=[event([cmp('Muted',0),cmp('State','"Loading"',1)],[ace('Audio','play-by-name',folder='sounds',**{'audio-file-name':'tokenat("release,blocked,match,win,tap",soundID,",")','loop':'not-looping','volume':'-12','stereo-pan':'0','tag-optional':'"sfx"'})])]))
write(P/'eventSheets/Game.json',dict(name='Game',events=E,sid=sid()))
# Layers: art/vehicles below modal; control sprites remain accessible above modal.
base=dict(name='Game',overriden=0,subLayers=[],instances=instances,sid=sid(),effectTypes=[],isInitiallyVisible=True,isInitiallyInteractive=True,isHTMLElementsLayer=False,color=[1,1,1,1],backgroundColor=[.86,.93,.88,1],isTransparent=False,parallaxX=1,parallaxY=1,scaleRate=1,forceOwnTexture=False,renderingMode='2d',drawOrder='z-order',useRenderCells=False,blendMode='normal',zElevation=0,**{'global':False})
layers=[]
for lname,names in [('Game',{'Backdrop','Vehicle'}),('UI',set(objects)-{'Backdrop','Vehicle','Modal','ModalTitle','ModalCaption','Next','Retry','Resume'}),('Overlay',{'Modal','ModalTitle','ModalCaption','Next','Retry','Resume'})]:
 layer={**base,'name':lname,'sid':sid(),'instances':[i for i in instances if i['type'] in names],'isTransparent':lname!='Game'}
 layers.append(layer)
write(P/'layouts/Game.json',dict(name='Game',layers=layers,**{'scene-graphs-folder-root':folder()},sid=sid(),**{'nonworld-instances':nonworld},effectTypes=[],width=540,height=960,unboundedScrolling=False,vpX=.5,vpY=.5,projection='perspective',eventSheet='Game'))
levels=json.loads((A/'levels.json').read_text());nativeLevels=[{**l,'count':len(l['vehicles'])} for l in levels]
(P/'scripts/campaign.js').write_text('export const LEVELS = '+json.dumps(nativeLevels,separators=(',',':'))+';\n')
(P/'scripts/main.js').write_text('import { LEVELS } from "./campaign.js";\n// Data loading only. All gameplay and rendering are native Construct events and objects.\nrunOnStartup(runtime => { runtime.addEventListener("beforeprojectstart", () => { runtime.globalVars.CampaignJSON = JSON.stringify(LEVELS); }); });\n')
shutil.copyfile(A/'levels.json',P/'files/levels.json')
# Base schema follows public Construct folder-project examples, with original content only.
props=json.loads((A/'construct-properties.json').read_text());props.update(description='A forty-level traffic escape and triple-matching toy puzzle.',version='1.0.0',author='Toy Traffic Trio',authorEmail='',authorWebsite='',appId='com.toytraffic.trio',fullscreenMode='letterbox-scale',orientations='portrait',sampling='trilinear',webgpu='auto',renderingMode='auto',loaderStyle='progress',gpuPreference='default')
rootFiles={k:folder() for k in ['script','sound','music','video','font','icon','general']}
for n,purpose in [('main.js','main'),('campaign.js','none')]:rootFiles['script']['items'].append(dict(name=n,type='application/javascript',sid=sid(),**{'script-info':{'purpose':purpose}}))
rootFiles['general']['items'].append(dict(name='levels.json',type='application/json',sid=sid(),**{'file-info':{'purpose':'none'}}))
for n in ['release','blocked','match','win','tap']:
 out=P/'sounds'/f'{n}.webm';subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(A/f'{n}.wav'),'-c:a','libopus',str(out)],check=True)
 rootFiles['sound']['items'].append(dict(name=f'{n}.webm',type='audio/webm; codecs=opus',sid=sid(),**{'file-info':{'purpose':'none'}}))
for size in [16,32,64,128,256,512]:
 im=Image.new('RGBA',(size,size),'#dcece0');car=Image.open(A/'vehicle-0.png');car.thumbnail((int(size*.55),int(size*.9)),Image.Resampling.LANCZOS);im.alpha_composite(car,((size-car.width)//2,(size-car.height)//2));im.save(P/'icons'/f'icon-{size}.png');rootFiles['icon']['items'].append(dict(name=f'icon-{size}.png',type='image/png',sid=sid(),**{'icon-info':{'purpose':'app-icon'}}))
project=dict(projectFormatVersion=1,savedWithRelease=50600,name='Toy Traffic Trio',runtime='c3',useWorker='auto',bundleAddons=False,usedAddons=[dict(type='plugin',id=n,name=title,author='Scirra',bundled=False) for n,title in [('Sprite','Sprite'),('Text','Text'),('Touch','Touch'),('Audio','Audio'),('Arr','Array'),('Json','JSON')]],uniqueId='toytraffictrio250631',objectTypes=folder(objects),functionsName='Functions',autosaveData=None,containers=[],families=folder(),layouts=folder(['Game']),eventSheets=folder(['Game']),rootFileFolders=rootFiles,timelines=folder(),flowcharts=folder(),properties=props,viewportWidth=540,viewportHeight=960,firstLayout='Game')
write(P/'project.c3proj',project)
with zipfile.ZipFile(R/'dist/ToyTrafficTrio.c3p','w',zipfile.ZIP_DEFLATED) as z:
 for p in P.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(P))
print('Native event project generated:',len(objects),'object types,',len(E),'top-level events')
