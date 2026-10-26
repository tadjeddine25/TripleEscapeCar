import pathlib,json,zipfile
R=pathlib.Path(__file__).resolve().parents[1];P=R/'construct';project=json.loads((P/'project.c3proj').read_text());objects={p.stem:json.loads(p.read_text()) for p in (P/'objectTypes').glob('*.json')};sheet=json.loads((P/'eventSheets/Game.json').read_text());functions={e['functionName'] for e in sheet['events'] if 'functionName' in e};assert project['name']=='Buster Block Shooter';assert set(objects)==set(project['objectTypes']['items'])
def check(o):
 if isinstance(o,dict):
  if 'callFunction' in o:assert o['callFunction'] in functions
  if 'objectClass' in o:assert o['objectClass'] in objects or o['objectClass']=='System'
  for v in o.values():check(v)
 elif isinstance(o,list):
  for v in o:check(v)
check(sheet)
for name,o in objects.items():
 for a in o.get('animations',{}).get('items',[]):
  for i,f in enumerate(a['frames']):
   assert 0 < f['imageSpriteId'] <= 2**32-1, 'Image IDs must not reuse the much larger SID sequence'
   assert (P/'images'/f'{name.lower()}-{a["name"].lower()}-{i:03}.png').exists()
with zipfile.ZipFile(R/'dist/BusterBlockShooter.c3p') as z:
 assert z.testzip() is None
 assert not any('/' in n for n in z.namelist()), 'C3P entries must match native Construct backslash paths'
 assert 'project.uistate.json' in z.namelist()
 for name in project['objectTypes']['items']:assert 'objectTypes'+chr(92)+name+'.json' in z.namelist()
 for name in project['layouts']['items']:assert 'layouts'+chr(92)+name+'.json' in z.namelist()
 for name in project['eventSheets']['items']:assert 'eventSheets'+chr(92)+name+'.json' in z.namelist()
 for f in P.rglob('*'):
  if f.is_file():assert z.read(str(f.relative_to(P)).replace('/',chr(92)))==f.read_bytes()
print('Construct JSON, object/function/image references and archive CRC passed. Editor/runtime UNVERIFIED.')
