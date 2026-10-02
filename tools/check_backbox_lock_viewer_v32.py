"""Preserve accepted viewer UI while validating populated backbox geometry. CERN-OHL-S-2.0."""
from pathlib import Path
import ast,json,hashlib,subprocess,shutil
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/backbox-lock-integration-v32';W=R/'.work/backbox-lock/browser';W.mkdir(parents=True,exist_ok=True)
html=(R/'exports/generated/viewer-v32/index.html').read_text();q=json.loads((O/'validation.json').read_text());assert all(c['pass'] for c in q['checks'])
parsed=ast.parse((R/'tools/check_review_viewer_v32.py').read_text());smoke=next(ast.literal_eval(node.value) for node in parsed.body if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='smoke' for t in node.targets))
extra=r'''
expect(Object.keys(STATES).length===12,'existing twelve state controls preserved');
expect(REVIEW.backbox_service.promoted,'populated backbox geometry selected');
for(const state of Object.keys(STATES)){
 v.applyState(state);
 for(const id of ['BB_Backglass','BB_Display32','BB_DMDEnvelope','BB_SpeakerEnvelopeL','BB_SpeakerEnvelopeR','BB_LowerCassetteFrame','BB_DoorL','BB_DoorR','BB_UprightLockLKnob','BB_UprightLockRKnob'])expect(v.meshes.find(m=>m.name===id)?.visible,'populated component retained '+state+' '+id);
 expect(v.meshes.find(m=>m.name==='BB_Backglass').material.transparent,'backglass material');
 const snapshots=v.meshes.map(m=>[m.geometry,m.geometry.attributes.position.array.slice(),m.userData.stateAbsent]);
 v.setLanguage('pt-BR');v.setPalette('accessible');
 expect(v.meshes.every((m,i)=>m.geometry===snapshots[i][0]&&m.geometry.attributes.position.array.every((x,j)=>x===snapshots[i][1][j])&&m.userData.stateAbsent===snapshots[i][2]),'language/palette preserve new geometry');
 if(state==='BACKBOX FOLD')expect(document.getElementById('state-note').textContent.includes('travas soltas e guardadas'),'Portuguese lock prerequisites');
 v.setLanguage('en');v.setPalette('original');
 if(state==='BACKBOX FOLD'){
  expect(document.getElementById('state-note').textContent.includes('locks released and parked'),'English lock prerequisites');
  expect(v.meshes.find(m=>m.name==='MatrixCarrier').userData.stateAbsent,'matrix removed');
  expect(v.meshes.find(m=>m.name==='CandidateGlass').userData.stateAbsent,'only main glass removed');
  expect(v.meshes.find(m=>m.name==='BB_UprightLockLKnob').geometry.boundingBox.min.x>160,'left knob parked');
 }
}
v.applyState('PLAY');document.getElementById('reset').click();
'''
smoke=smoke.replace("document.body.dataset.reviewSmoke='PASS';",extra+"document.body.dataset.reviewSmoke='PASS';")
page=W/'validation.html';page.write_text(html.replace('</body>',smoke+'</body>'));chrome=shutil.which('google-chrome') or shutil.which('chromium');assert chrome
cmd=[chrome,'--headless','--no-sandbox','--disable-dev-shm-usage','--disable-background-networking','--no-first-run','--user-data-dir='+str(W/'profile'),'--allow-file-access-from-files','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--window-size=1600,1100','--virtual-time-budget=4000','--timeout=45000','--screenshot='+str(O/'viewer-current.png'),'--dump-dom',page.as_uri()]
with (W/'dom.html').open('w') as out,(W/'chrome.log').open('w') as err:res=subprocess.run(cmd,stdout=out,stderr=err,timeout=90)
dom=(W/'dom.html').read_text();assert res.returncode==0 and 'data-review-smoke="PASS"' in dom,dom[-3000:]
source='f3e2eee32fde61835376c53b462436b996f01794'
old=json.loads(subprocess.check_output(['git','show',source+':tools/viewer/translations.json'],cwd=R));new=json.loads((R/'tools/viewer/translations.json').read_text());assert all(new[k]==v for k,v in old.items())
oldtemplate=subprocess.check_output(['git','show',source+':tools/viewer/template.html'],cwd=R).decode();template=(R/'tools/viewer/template.html').read_text()
for line in oldtemplate.splitlines():
 if line.startswith(('const ORIGINAL_PALETTE=','Object.assign(ORIGINAL_PALETTE','const ACCESSIBLE_PALETTE=','function setPalette(','function setLanguage(','function updateSelectionEdges(','function applyState(','function restore(')):assert line in template
assert '<script src="http' not in html and '<link href="http' not in html
(O/'viewer-validation.json').write_text(json.dumps({'pass':True,'checks':['English/original defaults; existing twelve state controls','prior translations and palette definitions preserved','PT-BR/accessible toggles do not alter geometry','populated cassette/display/backglass retained in every state','parked knobs in fold; main glass and matrix absent','selection/hide/isolate/focus/cut/search preserved','offline WebGL screenshot'],'viewer_sha256':hashlib.sha256(html.encode()).hexdigest(),'mesh_sha256':hashlib.sha256((O/'mesh.json').read_bytes()).hexdigest(),'manufacturing_ready':False},indent=2)+'\n');print('BACKBOX_LOCK_VIEWER_PASS',flush=True)
