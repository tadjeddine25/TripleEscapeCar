"""Generate a native Construct 3 folder project and zipped C3P. No third-party addons.
Gameplay uses event sheets; JavaScript only supplies editable campaign data at startup.
"""
import json,pathlib,shutil,itertools,subprocess,zipfile
from PIL import Image
R=pathlib.Path(__file__).resolve().parents[1];P=R/'construct';A=R/'assets'
for f in ['objectTypes','layouts','eventSheets','images','scripts','sounds','files','icons']:(P/f).mkdir(parents=True,exist_ok=True)
sids=itertools.count(250000000001);uids=itertools.count(1);imageids=itertools.count(1000001)
def sid():return next(sids)
def write(path,data):path.write_text(json.dumps(data,indent=2))
def folder(items=None):return dict(items=[] if items is None else items,subfolders=[])
objects=[];instances=[];nonworld=[]
def var(n,t='number'):return dict(name=n,type=t,desc='',show=True,sid=sid())
def sprite(name,files,variables=[]):
 frames=[]
 for i,f in enumerate(files):
  w,h=Image.open(A/f).size;shutil.copyfile(A/f,P/'images'/f'{name.lower()}-default-{i:03}.png')
  frames.append(dict(width=w,height=h,originX=.5,originY=.5,originalSource='',exportFormat='lossless',exportQuality=.8,fileType='image/png',imageSpriteId=next(imageids),useCollisionPoly=True,collisionPoly={'points':[0,0,1,0,1,1,0,1]},duration=1,tag=''))
 write(P/'objectTypes'/f'{name}.json',dict(name=name,**{'plugin-id':'Sprite'},sid=sid(),isGlobal=False,editorNewInstanceIsReplica=True,instanceVariables=[var(v) for v in variables],behaviorTypes=[],effectTypes=[],animations=folder([dict(frames=frames,sid=sid(),name='Default',isLooping=False,isPingPong=False,repeatCount=1,repeatTo=0,speed=0)])))
 objects.append(name)
def inst(name,x,y,w,h,iv={},props=None,origin=.5):
 uid=next(uids);s=sid();o=dict(type=name,properties=props or {'initially-visible':True,'initial-animation':'Default','initial-frame':0,'enable-collisions':True},uid=uid,sid=s,tags='',instanceVariables=iv,behaviors={},instanceFolderItem={'sid':s,'expanded':True},showing=True,locked=False,world=dict(x=x,y=y,width=w,height=h,originX=origin,originY=origin,color=[1,1,1,1],angle=0,zElevation=0))
 instances.append(o);return o
def ace(obj,id,**params):
 o=dict(id=id,objectClass=obj,sid=sid())
 if params:o['parameters']=params
 return o
def sy(id,**p):return ace('System',id,**p)
def setg(n,v):return sy('set-eventvar-value',variable=n,value=str(v))
def cmp(a,b,op=0):return sy('compare-two-values',**{'first-value':str(a),'comparison':op,'second-value':str(b)})
def call(n,*args):return dict(callFunction=n,sid=sid(),**({'parameters':list(args)} if args else {}))
def event(conds=[],acts=[],children=[]):
 o=dict(eventType='block',conditions=conds,actions=acts,sid=sid())
 if children:o['children']=children
 return o
def fn(n,args=[],acts=[],children=[]):
 return dict(functionName=n,functionDescription='',functionCategory='Buster Block Shooter',functionReturnType='none',functionCopyPicked=False,functionIsAsync=False,functionParameters=[dict(name=a,type='number',initialValue='0',comment='',sid=sid()) for a in args],eventType='function-block',conditions=[],actions=acts,sid=sid(),children=children)
def loop(n,end,start='0'):return sy('for',name=json.dumps(n),**{'start-index':start,'end-index':str(end)})
def at(x,y,v):return ace('Board','set-at-xy',x=x,y=y,value=v)
def opacity(obj,v):return ace(obj,'set-opacity',opacity=str(v))
def txt(obj,v):return ace(obj,'set-text',text=v)
def comment(s):return dict(eventType='comment',text=s)

sprite('Backdrop',['background.png']);inst('Backdrop',270,480,540,960)
# Native objects keep puzzle data separate from animation positions.
for name,files,vs in [('Block',[f'block-{i}.png' for i in range(6)],['bid','gx','gy','span','hp','kind']),('Tank',[f'tank-{i}.png' for i in range(6)],['tid','col','order','kind','ammo','phase','bay']),('Shot',['bullet.png'],['age','sx','sy','tx','ty'])]:
 sprite(name,files,vs);inst(name,-200,-200,8 if name=='Shot' else 50,8 if name=='Shot' else 50,{v:0 for v in vs})
for name,asset,x,y,w in [('Undo','undo',74,875,112),('Hint','hint',74,935,112),('Restart','restart',50,151,48),('Pause','pause',491,151,48),('Next','next',270,491,242),('Retry','retry',270,491,242),('Resume','resume',270,491,242)]:sprite(name,[f'button-{asset}.png']);inst(name,x,y,w,50)
for n,x,y,w,h,size,vs in [('Title',25,20,430,84,29,[]),('LevelLabel',150,120,240,44,20,[]),('Message',35,170,470,30,13,[]),('Numbers',-200,-200,80,40,24,['owner','role']),('ModalTitle',50,350,440,70,27,[])]:
 objects.append(n);write(P/'objectTypes'/f'{n}.json',dict(name=n,**{'plugin-id':'Text'},sid=sid(),isGlobal=False,instanceVariables=[var(v) for v in vs],behaviorTypes=[],effectTypes=[]));inst(n,x,y,w,h,{v:0 for v in vs},props={'text':'BUSTER\nBLOCK SHOOTER' if n=='Title' else '', 'font':'Arial','size':size,'bold':True,'italic':False,'color':[.12,.20,.27,1],'horizontal-alignment':'center','vertical-alignment':'center','wrapping':'word','initially-visible':True,'origin':'top-left','enable-bbcode':True,'line-height':0,'text-direction':'ltr','read-aloud':False},origin=0)
for name,plugin,props in [('Campaign','Json',{}),('Board','Arr',{'width':6,'height':6,'depth':1}),('History','Arr',{'width':64,'height':4,'depth':128})]:
 objects.append(name);write(P/'objectTypes'/f'{name}.json',dict(name=name,**{'plugin-id':plugin},sid=sid(),isGlobal=True,instanceVariables=[]));nonworld.append(dict(type=name,properties=props,uid=next(uids),sid=sid(),tags='',instanceVariables={}))
objects.append('Touch');write(P/'objectTypes/Touch.json',dict(name='Touch',**{'plugin-id':'Touch'},sid=sid(),**{'singleglobal-inst':dict(type='Touch',properties={'use-mouse-input':True},uid=next(uids),sid=sid(),tags='')}))
def V(obj,n,v):return ace(obj,'set-instvar-value',**{'instance-variable':n,'value':str(v)})
def C(obj,n,v,op=0):return ace(obj,'compare-instance-variable',**{'instance-variable':n,'comparison':op,'value':str(v)})
def each(obj):return sy('for-each',object=obj)
def pos(obj,x,y):return ace(obj,'set-position',x=x,y=y)
def create(obj,x='-200',y='-200',layer='Game'):return sy('create-object',**{'object-to-create':obj,'layer':json.dumps(layer),'x':x,'y':y,'create-hierarchy':False,'template-name':'""'})
def get(key):return 'Campaign.Get(str(Level) & ".'+key+'")'
def dget(group,key):return get(group+'." & loopindex("spawn") & ".'+key)
E=[]
for n,t,v in [('CampaignJSON','string',''),('State','string','Loading'),('Level','number','0'),('Rows','number','6'),('Clock','number','0'),('UndoCount','number','0'),('FrontRank','number','0'),('TargetID','number','-1'),('Obstructed','number','0'),('Bay','number','0'),('Occupied','number','0'),('ActiveCount','number','0'),('Shootable','number','0'),('Remaining','number','0')]:E.append(dict(eventType='variable',name=n,type=t,initialValue=v,isStatic=False,isConstant=False,sid=sid(),comment=''))
E.append(event([sy('on-start-of-layout')],[ace('Campaign','parse',data='CampaignJSON'),call('LoadLevel')]))
E.append(fn('LoadLevel',acts=[setg('State','"Loading"'),ace('Block','destroy'),ace('Tank','destroy'),ace('Shot','destroy'),ace('Numbers','destroy'),ace('Board','set-size',width='6',height='6',depth='1'),ace('Board','clear'),setg('Rows',get('rows')),setg('Clock',0),setg('UndoCount',0),txt('Message','"Tap a front tank. Match its colour."')],children=[
 event([loop('spawn',get('blockCount')+'-1')],[create('Block'),*[V('Block',n,dget('blocks',key)) for n,key in [('bid','id'),('gx','x'),('gy','y'),('span','w'),('hp','hp'),('kind','color')]],ace('Block','set-animation-frame',**{'frame-number':'Block.kind'}),ace('Block','set-size',width='Block.span*72',height='64'),pos('Block','54+(Block.gx+Block.span/2)*72','600-(Rows-Block.gy-.5)*64'),create('Numbers',layer='UI'),V('Numbers','owner','Block.bid'),V('Numbers','role',0)],children=[event([loop('occupy','Block.span-1')],[at('Block.gx+loopindex("occupy")','Block.gy','Block.bid+1')])]),
 event([loop('spawn',get('tankCount')+'-1')],[create('Tank'),*[V('Tank',n,dget('tanks',key)) for n,key in [('tid','id'),('col','col'),('order','order'),('kind','color'),('ammo','ammo')]],V('Tank','phase',0),ace('Tank','set-animation-frame',**{'frame-number':'Tank.kind'}),ace('Tank','set-size',width='63',height='74'),create('Numbers',layer='UI'),V('Numbers','owner','Tank.tid'),V('Numbers','role',1)]),event(acts=[setg('State','"Playing"')])]))
E.append(fn('QueueRank',['candidate'],acts=[setg('FrontRank',0)],children=[event([C('Tank','tid','candidate')],[setg('Bay','Tank.col'),setg('TargetID','Tank.order')]),event([C('Tank','phase',0),C('Tank','col','Bay'),C('Tank','order','TargetID',2),each('Tank')],[setg('FrontRank','FrontRank+1')])]))
E.append(fn('FreeBay',acts=[setg('Bay',-1)],children=[event([loop('bay',4),cmp('Bay',-1)],[setg('Occupied',0)],children=[event([C('Tank','phase',1),C('Tank','bay','loopindex("bay")'),each('Tank')],[setg('Occupied',1)]),event([cmp('Occupied',0)],[setg('Bay','loopindex("bay")')])])]))
E.append(event([ace('Touch','on-tap-object',object='Tank'),cmp('State','"Playing"'),C('Tank','phase',0)],[call('QueueRank','Tank.tid')],children=[event([cmp('FrontRank',0)],[call('FreeBay')],children=[event([cmp('Bay',0,5)],[call('Snapshot'),setg('UndoCount','UndoCount+1'),V('Tank','phase',1),V('Tank','bay','Bay')])])]))
# Any unoccluded column under a block is an exposed firing path. Colour must match.
E.append(fn('FindTarget',['colour'],acts=[setg('TargetID',-1)],children=[event([C('Block','hp',0,4),C('Block','kind','colour'),each('Block'),loop('column','Block.span-1')],[setg('Obstructed',0)],children=[event([cmp('Block.gy','Rows-1',2),loop('ray','Rows-1','Block.gy+1'),cmp('Board.At(Block.gx+loopindex("column"),loopindex("ray"))',0,4)],[setg('Obstructed',1)]),event([cmp('Obstructed',0)],[setg('TargetID','Block.bid')])])]))
E.append(fn('Shoot',['colour'],acts=[call('FindTarget','colour')],children=[event([cmp('TargetID',0,5),C('Block','bid','TargetID')],[V('Block','hp','Block.hp-1'),V('Tank','ammo','Tank.ammo-1'),create('Shot','Tank.X','Tank.Y-30'),V('Shot','age',0),V('Shot','sx','Tank.X'),V('Shot','sy','Tank.Y-30'),V('Shot','tx','Block.X'),V('Shot','ty','Block.Y')],children=[event([C('Block','hp',0)],[opacity('Block',0)],children=[event([loop('clear','Block.span-1')],[at('Block.gx+loopindex("clear")','Block.gy','0')])])])]))
# Copy picked Tank into Shoot so its ammo changes atomically with damage.
next(e for e in E if e.get('functionName')=='Shoot')['functionCopyPicked']=True
E.append(event([sy('every-tick')],children=[
 event([C('Tank','phase',0),each('Tank')],[call('QueueRank','Tank.tid'),pos('Tank','190+Tank.col*80','760+FrontRank*78'),opacity('Tank','FrontRank<3 ? (FrontRank=0 ? 100 : 55) : 0')]),
 event([C('Tank','phase',1),each('Tank')],[pos('Tank','94+Tank.bay*88','658'),opacity('Tank',100)]),event([C('Tank','phase',2)],[opacity('Tank',0)]),
 event([C('Numbers','role',0),each('Numbers'),C('Block','bid','Numbers.owner')],[pos('Numbers','Block.X-40','Block.Y-20'),txt('Numbers','str(Block.hp)'),opacity('Numbers','Block.hp>0 ? 100 : 0')]),
 event([C('Numbers','role',1),each('Numbers'),C('Tank','tid','Numbers.owner')],[pos('Numbers','Tank.X-40','Tank.Y-7'),txt('Numbers','str(Tank.ammo)'),opacity('Numbers','Tank.Opacity')]),
 event([cmp('State','"Playing"')],[setg('Clock','Clock+dt')],children=[event([cmp('Clock','.16',5)],[setg('Clock',0),call('Volley')])]),
 event([each('Shot')],[V('Shot','age','Shot.age+dt'),pos('Shot','lerp(Shot.sx,Shot.tx,min(1,Shot.age/.15))','lerp(Shot.sy,Shot.ty,min(1,Shot.age/.15))')],children=[event([C('Shot','age','.15',5)],[ace('Shot','destroy')])]),
 event(acts=[txt('LevelLabel','"LEVEL " & (Level+1) & " / 40"'),txt('ModalTitle','State="Won" ? "BOARD CLEARED!" : State="Lost" ? "TANK JAM!" : "TAKE A BREATHER"'),opacity('ModalTitle','State="Playing" ? 0 : 100'),opacity('Next','State="Won" ? 100 : 0'),opacity('Retry','State="Lost" ? 100 : 0'),opacity('Resume','State="Paused" ? 100 : 0')])]))
E.append(fn('Volley',children=[event([C('Tank','phase',1),each('Tank')],[call('Shoot','Tank.kind')],children=[event([C('Tank','ammo',0)],[V('Tank','phase',2)])]),event(acts=[setg('Remaining',0),setg('ActiveCount',0),setg('Shootable',0)]),event([C('Block','hp',0,4),each('Block')],[setg('Remaining','Remaining+1')]),event([C('Tank','phase',1),each('Tank')],[setg('ActiveCount','ActiveCount+1'),call('FindTarget','Tank.kind')],children=[event([cmp('TargetID',0,5)],[setg('Shootable','Shootable+1')])]),event([cmp('Remaining',0)],[setg('State','"Won"')]),event([cmp('ActiveCount',5),cmp('Shootable',0),cmp('Remaining',0,4)],[setg('State','"Lost"')])]))
for obj,conds,acts in [('Restart',[],[call('LoadLevel')]),('Retry',[cmp('State','"Lost"')],[call('LoadLevel')]),('Next',[cmp('State','"Won"')],[setg('Level','(Level+1)%40'),call('LoadLevel')]),('Pause',[cmp('State','"Playing"')],[setg('State','"Paused"')]),('Resume',[cmp('State','"Paused"')],[setg('State','"Playing"')]),('Hint',[],[txt('Message','"Pick a colour with an open path from below."')]),('Undo',[cmp('UndoCount',0,4)],[call('UndoMove')])]:E.append(event([ace('Touch','on-tap-object',object=obj),*conds],acts))

def history(x,y,v):return ace('History','set-at-xyz',x=x,y=y,z='UndoCount',value=v)
E.append(fn('Snapshot',children=[event([each('Block')],[history('Block.bid','0','Block.hp')]),event([each('Tank')],[history('Tank.tid','1','Tank.ammo'),history('Tank.tid','2','Tank.phase'),history('Tank.tid','3','Tank.bay')])]))
E.append(fn('UndoMove',acts=[setg('UndoCount','UndoCount-1'),ace('Board','clear'),ace('Shot','destroy'),setg('State','"Playing"'),setg('Clock',0)],children=[event([each('Block')],[V('Block','hp','History.At(Block.bid,0,UndoCount)'),opacity('Block','Block.hp>0 ? 100 : 0')],children=[event([C('Block','hp',0,4),loop('restore','Block.span-1')],[at('Block.gx+loopindex("restore")','Block.gy','Block.bid+1')])]),event([each('Tank')],[V('Tank','ammo','History.At(Tank.tid,1,UndoCount)'),V('Tank','phase','History.At(Tank.tid,2,UndoCount)'),V('Tank','bay','History.At(Tank.tid,3,UndoCount)')])]))

write(P/'eventSheets/Game.json',dict(name='Game',events=E,sid=sid()))
layers=[]
for lname,names in [('Game',{'Backdrop','Block','Tank','Shot'}),('UI',set(objects)-{'Backdrop','Block','Tank','Shot'})]:layers.append(dict(name=lname,overriden=0,subLayers=[],instances=[i for i in instances if i['type'] in names],sid=sid(),effectTypes=[],isInitiallyVisible=True,isInitiallyInteractive=True,isHTMLElementsLayer=False,color=[1,1,1,1],backgroundColor=[.4,.7,.9,1],isTransparent=lname!='Game',parallaxX=1,parallaxY=1,scaleRate=1,forceOwnTexture=False,renderingMode='2d',drawOrder='z-order',useRenderCells=False,blendMode='normal',zElevation=0,**{'global':False}))
write(P/'layouts/Game.json',dict(name='Game',layers=layers,**{'scene-graphs-folder-root':folder()},sid=sid(),**{'nonworld-instances':nonworld},effectTypes=[],width=540,height=960,unboundedScrolling=False,vpX=.5,vpY=.5,projection='perspective',eventSheet='Game'))
levels=json.loads((A/'levels.json').read_text());native=[{**l,'blockCount':len(l['blocks']),'tankCount':len(l['tanks'])} for l in levels]
(P/'scripts/campaign.js').write_text('export const LEVELS='+json.dumps(native)+';\n');(P/'scripts/main.js').write_text('import {LEVELS} from "./campaign.js";\nrunOnStartup(runtime=>runtime.addEventListener("beforeprojectstart",()=>{runtime.globalVars.CampaignJSON=JSON.stringify(LEVELS);}));\n')
root={k:folder() for k in ['script','sound','music','video','font','icon','general']}
for n,purpose in [('main.js','main'),('campaign.js','none')]:root['script']['items'].append(dict(name=n,type='application/javascript',sid=sid(),**{'script-info':{'purpose':purpose}}))
props=json.loads((A/'construct-properties.json').read_text());props.update(description='Colour-matched tanks blast numbered castle blocks.',author='Buster Block Shooter',appId='com.buster.blockshooter',version='1.0.0')
write(P/'project.c3proj',dict(projectFormatVersion=1,savedWithRelease=50600,name='Buster Block Shooter',runtime='c3',useWorker='auto',bundleAddons=False,usedAddons=[dict(type='plugin',id=i,name=n,author='Scirra',bundled=False) for i,n in [('Sprite','Sprite'),('Text','Text'),('Touch','Touch'),('Json','JSON'),('Arr','Array')]],uniqueId='bustr061723',objectTypes=folder(objects),functionsName='Functions',autosaveData=None,containers=[],families=folder(),layouts=folder(['Game']),eventSheets=folder(['Game']),rootFileFolders=root,timelines=folder(),flowcharts=folder(),properties=props,viewportWidth=540,viewportHeight=960,firstLayout='Game'))
write(P/'project.uistate.json',{'openTabs':{'active':{'name':'Game','type':'layout'},'open':[{'name':'Game','type':'layout'},{'name':'Game','type':'eventSheet'}]},'previewEffects':True,'previewBrowser':'default','pauseOnUnfocus':False})
write(P/'projectfiles.uistate.json',[])
write(P/'objecttypes.uistate.json',[])
with zipfile.ZipFile(R/'dist/BusterBlockShooter.c3p','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(P.rglob('*'),key=lambda f:(f.name!='project.c3proj',str(f))):
  if f.is_file():z.write(f,str(f.relative_to(P)).replace('/',chr(92)))
print('Native Buster Block Shooter C3P generated (editor preview unverified).')
