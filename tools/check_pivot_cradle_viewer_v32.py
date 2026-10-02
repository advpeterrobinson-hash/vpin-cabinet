"""Verify new geometry and preserve accepted V32 UI; no old review images regenerated. CERN-OHL-S-2.0."""
from pathlib import Path
import ast,json,hashlib,subprocess,shutil
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/pivot-cradle-integration-v32';W=R/'.work/pivot-cradle/browser';W.mkdir(parents=True,exist_ok=True)
html=(R/'exports/generated/viewer-v32/index.html').read_text();original={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.suffix in ('.FCStd','.step')}
# Reuse the accepted interface checks unchanged, without running its screenshot workflow.
parsed=ast.parse((R/'tools/check_review_viewer_v32.py').read_text());smoke=next(ast.literal_eval(node.value) for node in parsed.body if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='smoke' for t in node.targets))
extra=r'''
v.reviewView('matrix-installed');
for(const state of ['MATRIX INSTALLED','MATRIX UNLOCK','MATRIX FORWARD','MATRIX EXTRACTION','MATRIX REMOVED','PLAYFIELD SERVICE','LIFT-OUT','BACKBOX FOLD','MATRIX EXPLODED']){
 v.applyState(state);
 const gone=['MATRIX REMOVED','PLAYFIELD SERVICE','LIFT-OUT','BACKBOX FOLD'].includes(state);
 const carrier=v.meshes.find(m=>m.name==='MatrixCarrier');expect(carrier.userData.stateAbsent===gone,'explicit matrix state presence');
 if(gone)expect(document.getElementById('state-note').textContent.includes('MATRIX REMOVED'),'visible prerequisite');
 const snapshots=v.meshes.map(m=>[m.geometry,m.geometry.attributes.position.array.slice(),m.userData.stateAbsent]);
 v.setLanguage('pt-BR');v.setPalette('accessible');
 expect(v.meshes.every((m,i)=>m.geometry===snapshots[i][0]&&m.geometry.attributes.position.array.every((x,j)=>x===snapshots[i][1][j])&&m.userData.stateAbsent===snapshots[i][2]),'new states translations/palette preserve geometry');
 if(gone)expect(document.getElementById('state-note').textContent.includes('MATRIZ REMOVIDA'),'Portuguese prerequisite');
 v.setLanguage('en');v.setPalette('original');
 if(state==='BACKBOX FOLD'){expect(document.getElementById('state-note').textContent.includes('Wood fold 0–90° validated'),'validated wood fold visible');expect(v.meshes.filter(m=>m.name.startsWith('BB_')&&m.visible).length===8,'eight actual backbox wood parts visible');expect(!v.meshes.some(m=>m.name==='PF_BackboxCheckEnvelope'),'superseded envelope absent');}
}
for(const state of ['SERVICE','PLAYFIELD SERVICE','LIFT-OUT','BACKBOX FOLD']){
 const saved=REVIEW.matrix_cassette.prerequisites[state];REVIEW.matrix_cassette.prerequisites[state]=['GLASS_REMOVED'];let rejected=false;
 try{v.applyState(state);}catch(e){rejected=true;}expect(rejected,'negative missing prerequisite rejected');REVIEW.matrix_cassette.prerequisites[state]=saved;
}
v.reviewView('matrix-retention');v.select(v.meshes.find(m=>m.name==='MX_RetainerL'));expect(v.selectionEdges().visible,'cassette retainer outline');
v.setLanguage('pt-BR');expect(document.getElementById('selection').textContent.includes('PARAFUSO MANUAL'),'new translated label');v.setLanguage('en');
v.reviewView('player-left');
'''
smoke=smoke.replace("document.body.dataset.reviewSmoke='PASS';",extra+"document.body.dataset.reviewSmoke='PASS';")
page=W/'validation.html';page.write_text(html.replace('</body>',smoke+'</body>'));chrome=shutil.which('google-chrome') or shutil.which('chromium');assert chrome
command=[chrome,'--headless','--no-sandbox','--disable-dev-shm-usage','--disable-background-networking','--no-first-run','--user-data-dir='+str(W/'profile'),'--allow-file-access-from-files','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--window-size=1600,1100','--virtual-time-budget=2500','--timeout=30000','--dump-dom',page.as_uri()]
with (W/'dom.html').open('w') as out,(W/'chrome.log').open('w') as err:result=subprocess.run(command,stdout=out,stderr=err,timeout=60)
dom=(W/'dom.html').read_text();assert result.returncode==0 and 'data-review-smoke="PASS"' in dom,dom[-2000:]
assert all(hashlib.sha256((O/name).read_bytes()).hexdigest()==h for name,h in original.items())
# Existing translation entries and palette/edge implementations must remain exactly accepted.
old_dict=json.loads(subprocess.check_output(['git','show','ca56e7f98f119a99c6a5a28f4a903a3b6c95b997:tools/viewer/translations.json'],cwd=R));new_dict=json.loads((R/'tools/viewer/translations.json').read_text());assert all(new_dict[k]==v for k,v in old_dict.items())
old_template=subprocess.check_output(['git','show','ca56e7f98f119a99c6a5a28f4a903a3b6c95b997:tools/viewer/template.html'],cwd=R).decode();new_template=(R/'tools/viewer/template.html').read_text()
for line in old_template.splitlines():
 if line.startswith(('const ORIGINAL_PALETTE=','Object.assign(ORIGINAL_PALETTE','const ACCESSIBLE_PALETTE=','function setPalette(','function setLanguage(','function updateSelectionEdges(')):assert line in new_template
(O/'viewer-validation.json').write_text(json.dumps({'pass':True,'checks':['accepted EN/PT-BR and palettes preserved byte for byte in source','English/original defaults','twelve states; declared removal enforced in CAD and viewer; validated wood fold / provisional hardware visible','language and palette preserve geometry bytes','selection edges','new fold status in EN/PT-BR','matrix state geometry and retention','CAD/STEP files byte unchanged by viewer work'],'viewer_sha256':hashlib.sha256(html.encode()).hexdigest()},indent=2)+'\n');print('PIVOT_CRADLE_VIEWER_PASS',flush=True)
