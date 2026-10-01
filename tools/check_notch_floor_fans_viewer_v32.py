"""Verify new geometry and preserve accepted V32 UI; no old review images regenerated. CERN-OHL-S-2.0."""
from pathlib import Path
import ast,json,hashlib,subprocess,shutil
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/notch-floor-fans-v32';W=R/'.work/service-correction-v32/notch-fan-browser';W.mkdir(parents=True,exist_ok=True)
html=(R/'exports/generated/viewer-v32/index.html').read_text();original={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.suffix in ('.FCStd','.step')}
# Reuse the accepted interface checks unchanged, without running its screenshot workflow.
parsed=ast.parse((R/'tools/check_review_viewer_v32.py').read_text());smoke=next(ast.literal_eval(node.value) for node in parsed.body if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='smoke' for t in node.targets))
extra=r'''
const base=v.meshes.find(m=>m.name==='PF_BasePlywood');const play=base.userData.playGeometry.attributes.position.array;
expect(play.length>0,'new notched playfield present');
for(const state of ['PLAY','SERVICE','LIFT-OUT','EXPLODED']){
 v.applyState(state);
 for(const side of ['L','R']){
  const fan=v.meshes.find(m=>m.name==='FloorIntakeFan'+side),filter=v.meshes.find(m=>m.name==='RemovableIntakeFilter'+side);
  expect(!!fan&&!!filter,'two new fan stations present');expect(fan.visible===(state!=='EXPLODED'),'fan state presence');expect(fan.geometry===fan.userData.playGeometry,'floor fans stationary');
  if(state==='PLAY'){const b=fan.geometry.boundingBox;expect(Math.abs(b.min.z-36)<.01&&Math.abs(b.max.z-61)<.01,'inside floor 25mm fan');expect(Math.abs(b.max.x-b.min.x-120)<.01&&Math.abs(b.max.y-b.min.y-120)<.01,'shared 120mm fan format');}
 }
}
v.applyState('PLAY');v.select(v.meshes.find(m=>m.name==='FloorIntakeFanL'));expect(document.getElementById('selection').textContent.includes('FLOOR INTAKE FAN L'),'canonical new fan label');document.getElementById('lang-pt').click();expect(document.getElementById('selection').textContent.includes('VENTOINHA DE ADMISSÃO NO PISO E'),'new fan Portuguese label');document.getElementById('lang-en').click();
expect(!v.meshes.some(m=>m.name==='CandidateIntakeFilterFrame1'),'old passive filter frame retired');
'''
smoke=smoke.replace("document.body.dataset.reviewSmoke='PASS';",extra+"document.body.dataset.reviewSmoke='PASS';")
page=W/'validation.html';page.write_text(html.replace('</body>',smoke+'</body>'));chrome=shutil.which('google-chrome') or shutil.which('chromium');assert chrome
command=[chrome,'--headless','--no-sandbox','--disable-dev-shm-usage','--disable-background-networking','--no-first-run','--user-data-dir='+str(W/'profile'),'--allow-file-access-from-files','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--window-size=1600,1100','--virtual-time-budget=2500','--timeout=30000','--dump-dom',page.as_uri()]
with (W/'dom.html').open('w') as out,(W/'chrome.log').open('w') as err:result=subprocess.run(command,stdout=out,stderr=err,timeout=60)
dom=(W/'dom.html').read_text();assert result.returncode==0 and 'data-review-smoke="PASS"' in dom,dom[-2000:]
assert all(hashlib.sha256((O/name).read_bytes()).hexdigest()==h for name,h in original.items())
# Existing translation entries and palette/edge implementations must remain exactly accepted.
old_dict=json.loads(subprocess.check_output(['git','show','cd416fea61ed031c59af8df93014ae7c9ba200bf:tools/viewer/translations.json'],cwd=R));new_dict=json.loads((R/'tools/viewer/translations.json').read_text());assert all(new_dict[k]==v for k,v in old_dict.items())
old_template=subprocess.check_output(['git','show','cd416fea61ed031c59af8df93014ae7c9ba200bf:tools/viewer/template.html'],cwd=R).decode();new_template=(R/'tools/viewer/template.html').read_text()
for line in old_template.splitlines():
 if line.startswith(('const ORIGINAL_PALETTE=','Object.assign(ORIGINAL_PALETTE','const ACCESSIBLE_PALETTE=','function setPalette(','function setLanguage(','function updateSelectionEdges(')):assert line in new_template
(O/'viewer-validation.json').write_text(json.dumps({'pass':True,'checks':['accepted EN/PT-BR and palettes preserved byte for byte in source','English/original defaults','four states','language and palette preserve geometry bytes','selection edges','new fan/filter labels','fan position and stationary states','old passive filter frames removed','CAD/STEP files byte unchanged by viewer work'],'viewer_sha256':hashlib.sha256(html.encode()).hexdigest()},indent=2)+'\n');print('NOTCH_FAN_VIEWER_PASS',flush=True)
