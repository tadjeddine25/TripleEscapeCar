import pathlib,json,subprocess,zipfile,sys
R=pathlib.Path(__file__).resolve().parents[1];D=R/'dist';D.mkdir(exist_ok=True)
levels=json.loads((R/'assets/levels.json').read_text());(R/'src/campaign.js').write_text('export const LEVELS='+json.dumps(levels)+';\n')
for cmd in [['node','tools/validate.mjs'],[sys.executable,'tools/construct.py'],[sys.executable,'tools/check_construct.py']]:subprocess.run(cmd,cwd=R,check=True)
with zipfile.ZipFile(D/'BusterBlockShooter-HTML5.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [R/'index.html',R/'README.md',R/'QA.md',*(R/'src').glob('*.js'),*(R/'assets').glob('*')]:
  if f.is_file():z.write(f,f.relative_to(R))
with zipfile.ZipFile(D/'BusterBlockShooter-Source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in R.rglob('*'):
  if f.is_file() and not any(p in f.relative_to(R).parts for p in ['.git','node_modules','dist','__pycache__']):z.write(f,pathlib.Path('BusterBlockShooter')/f.relative_to(R))
 for f in D.glob('*.png'):z.write(f,pathlib.Path('BusterBlockShooter/QA')/f.name)
 if (D/'browser-qa.json').exists():z.write(D/'browser-qa.json','BusterBlockShooter/QA/browser-qa.json')
print('C3P, HTML5 companion and source archives packaged.')
