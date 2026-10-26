"""Structural checks only. Does not claim editor/runtime validation."""
import json,pathlib,re,zipfile
R=pathlib.Path(__file__).resolve().parents[1];P=R/'construct'
project=json.loads((P/'project.c3proj').read_text());objects={p.stem:json.loads(p.read_text()) for p in (P/'objectTypes').glob('*.json')};events=json.loads((P/'eventSheets/Game.json').read_text())
assert project['savedWithRelease']==50600
assert set(project['objectTypes']['items'])==set(objects)
functions={e['functionName'] for e in events['events'] if 'functionName' in e}
variables={e['name'] for e in events['events'] if e.get('eventType')=='variable'}
refs=0;aces=0;expressions=0
for name,obj in objects.items():
 for anim in obj.get('animations',{}).get('items',[]):
  for i,frame in enumerate(anim['frames']):
   assert (P/'images'/f"{name.lower()}-{anim['name'].lower()}-{i:03}.png").is_file();refs+=1
layout=json.loads((P/'layouts/Game.json').read_text())
for layer in layout['layers']:
 for instance in layer['instances']:assert instance['type'] in objects
for category,folder in [('script','scripts'),('sound','sounds'),('icon','icons'),('general','files')]:
 for file in project['rootFileFolders'][category]['items']:assert (P/folder/file['name']).is_file()
def walk(o):
 global aces,expressions
 if isinstance(o,dict):
  if 'callFunction' in o:assert o['callFunction'] in functions
  if 'objectClass' in o:assert o['objectClass'] in objects or o['objectClass'] in ['System','Functions'];aces+=1
  if o.get('id')=='set-eventvar-value':assert o['parameters']['variable'] in variables
  if o.get('id') in ['set-instvar-value','compare-instance-variable']:
   assert o['parameters']['instance-variable'] in [v['name'] for v in objects[o['objectClass']]['instanceVariables']]
  if 'parameters' in o:
   vals=o['parameters'].values() if isinstance(o['parameters'],dict) else o['parameters']
   for v in vals:
    if isinstance(v,str):
     # Check balanced expression syntax outside quoted strings.
     s=re.sub(r'"(?:[^"\\]|\\.)*"','',v);assert s.count('(')==s.count(')'),v;assert s.count('"')==0,v;expressions+=1
  for v in o.values():walk(v)
 elif isinstance(o,list):
  for v in o:walk(v)
walk(events)
with zipfile.ZipFile(R/'dist/ToyTrafficTrio.c3p') as z:
 assert z.testzip() is None;assert 'project.c3proj' in z.namelist()
 for f in P.rglob('*'):
  if f.is_file():assert z.read(str(f.relative_to(P)))==f.read_bytes()
report=dict(status='structural checks passed',editorOpenTest='NOT RUN: editor.construct.net returned HTTP 403',runtimePreview='NOT RUN',officialHTML5Export='NOT RUN',objectTypes=len(objects),functions=len(functions),imageReferences=refs,eventACEs=aces,parameterStringsChecked=expressions,archiveCRC='passed')
(R/'dist/construct-structural-qa.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
