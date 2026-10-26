import pathlib,json,subprocess,zipfile,sys
R=pathlib.Path(__file__).resolve().parents[1];D=R/'dist';D.mkdir(exist_ok=True)
levels=json.loads((R/'assets/levels.json').read_text());(R/'src/campaign.js').write_text('export const LEVELS = '+json.dumps(levels,separators=(',',':'))+';\n')
subprocess.run(['node','tools/validate.js'],cwd=R,check=True)
subprocess.run([sys.executable,'tools/construct.py'],cwd=R,check=True)
subprocess.run([sys.executable,'tools/check_construct.py'],cwd=R,check=True)
with zipfile.ZipFile(D/'ToyTrafficTrio-HTML5.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in [R/'index.html',R/'README.md',R/'QA.md',*(R/'src').glob('*.js'),*(R/'assets').glob('*')]:
  if p.is_file():z.write(p,p.relative_to(R))
with zipfile.ZipFile(D/'ToyTrafficTrio-Source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in R.rglob('*'):
  if p.is_file() and not any(s in p.relative_to(R).parts for s in ['.git','node_modules','dist','__pycache__']):z.write(p,pathlib.Path('ToyTrafficTrio')/p.relative_to(R))
 for n in ['browser-qa.json','construct-structural-qa.json','screenshot-level1.png','screenshot-level40.png','screenshot-win.png','screenshot-mobile.png']:
  if (D/n).exists():z.write(D/n,pathlib.Path('ToyTrafficTrio/QA')/n)
print('Packaged C3P, playable browser ZIP, and complete editable source ZIP.')
