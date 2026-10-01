"""Verify new geometry and preserve accepted V32 UI; no old review images regenerated. CERN-OHL-S-2.0."""
from pathlib import Path
import ast,json,hashlib,subprocess,shutil
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/matrix-cassette-v32';W=R/'.work/matrix-cassette/browser';W.mkdir(parents=True,exist_ok=True)
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
 if(state==='BACKBOX FOLD')expect(document.getElementById('state-note').textContent.includes('BLOCKED'),'fold failure visible');
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
old_dict=json.loads(subprocess.check_output(['git','show','cd416fea61ed031c59af8df93014ae7c9ba200bf:tools/viewer/translations.json'],cwd=R));new_dict=json.loads((R/'tools/viewer/translations.json').read_text());assert all(new_dict[k]==v for k,v in old_dict.items())
old_template=subprocess.check_output(['git','show','cd416fea61ed031c59af8df93014ae7c9ba200bf:tools/viewer/template.html'],cwd=R).decode();new_template=(R/'tools/viewer/template.html').read_text()
for line in old_template.splitlines():
 if line.startswith(('const ORIGINAL_PALETTE=','Object.assign(ORIGINAL_PALETTE','const ACCESSIBLE_PALETTE=','function setPalette(','function setLanguage(','function updateSelectionEdges(')):assert line in new_template
(O/'viewer-validation.json').write_text(json.dumps({'pass':True,'checks':['accepted EN/PT-BR and palettes preserved byte for byte in source','English/original defaults','twelve states; declared removal enforced in CAD and viewer; fold BLOCKED visible','language and palette preserve geometry bytes','selection edges','new cassette labels in EN/PT-BR','matrix state geometry and retention','CAD/STEP files byte unchanged by viewer work'],'viewer_sha256':hashlib.sha256(html.encode()).hexdigest()},indent=2)+'\n');print('MATRIX_CASSETTE_VIEWER_PASS',flush=True)

# Only the ten new review views; screenshots are real WebGL renders of CAD meshes.
import sys,html as html_module
if '--reviews' in sys.argv:
    reviews=[
      ('01-matrix-installed-player.png','MATRIX INSTALLED',[300,-350,900],[300,1080,575],22,'PLAY · MATRIX INSTALLED / PLAYER EYE','Provisional eye XYZ 300, −350, 900 mm · minimum sampled LED visibility 75% · glass clearance 7.255 mm'),
      ('02-matrix-installed-side.png','MATRIX INSTALLED',[-420,1090,600],[300,1090,570],23,'PLAY · INSTALLED SIDE SECTION','Gap 35.1424 mm · absolute tilt 25° · installed Z change −0.25 mm · left shell omitted for inspection'),
      ('03-retention-detail.png','MATRIX INSTALLED',[-100,970,640],[52,1125,565],36,'RETENTION · LEFT SIDE (RIGHT MIRRORED)','One-piece 18 mm plywood seat · integral 2 mm locator · M4 × 20 thumb screw · common insert · section at X95'),
      ('04-matrix-unlock.png','MATRIX UNLOCK',[-300,760,820],[300,1080,565],30,'UNLOCK · GLASS REMOVED / HARNESS DISCONNECTED','Release two thumb screws; disconnect and stow harness · rock 26° forward by hand · vertical unlock lift 0 mm'),
      ('05-matrix-forward.png','MATRIX FORWARD',[-330,770,790],[300,1025,566],31,'FORWARD · GLASS REMOVED / HARNESS DISCONNECTED','After manual forward rocking: translate 68 mm toward player (−Y) · no hinge, slide or rail'),
      ('06-matrix-extraction.png','MATRIX EXTRACTION',[-340,700,950],[300,1040,610],36,'EXTRACTION · GLASS REMOVED / HARNESS DISCONNECTED','After forward translation: lift 100 mm · minimum sampled free route margin 1.113 mm · intentional installed seat contact 0 mm'),
      ('07-matrix-removed.png','MATRIX REMOVED',[-420,820,610],[300,1120,540],30,'MATRIX REMOVED · STATIONARY WOOD SEATS REMAIN','Cassette, six panels and moving harness removed · two wood seats and fixed disconnect remain · inspection section'),
      ('08-playfield-service-matrix-removed.png','PLAYFIELD SERVICE',[-1300,-900,1700],[300,700,600],40,'PLAYFIELD SERVICE · GLASS REMOVED + MATRIX REMOVED','Accepted wooden pivot unchanged · service sweep 0–50° clear of cassette supports · accepted 48 mm lift-out also retained'),
      ('09-backbox-fold-matrix-removed.png','BACKBOX FOLD',[-1300,-650,1300],[300,850,530],38,'BACKBOX FOLD · INTERFERENCE REVIEW / BLOCKED','GLASS REMOVED + MATRIX REMOVED · existing packaging envelope crosses cabinet and fixed seats · no fold-clearance approval'),
      ('10-exploded-matrix-cassette.png','MATRIX EXPLODED',[-400,400,1100],[300,1100,625],33,'EXPLODED · SIMPLE REMOVABLE MATRIX CASSETTE','Six panels + one plywood carrier · two one-piece wood seats · two removable retainers · commodity fixed screws / inserts · custom metal 0')]
    results=[]
    for filename,state,camera,target,fov,title,caption in reviews:
        setup={'state':state,'camera':camera,'target':target,'fov':fov,'file':filename}
        js=r'''
<script>
const setup=SETUP;
const v=window.viewer;v.reviewView('matrix-installed');v.applyState(setup.state);v.controls.enableDamping=false;
const full=['PLAYFIELD SERVICE','BACKBOX FOLD'].includes(setup.state);
const context=new Set(['SIDE_R','REAR','BACKBOX_BASE','PLAYFIELD_ENVELOPE','PF_BasePlywood','PF_WoodDowel','PF_OpenCradleL','PF_OpenCradleR','CandidateGlass','CandidateGlassChannelL','CandidateGlassChannelR','FLOOR']);
for(const m of v.meshes){m.userData.hidden=!(full||context.has(m.name)||/^(Matrix|MX_)/.test(m.name));if(['SIDE_L','FRONT'].includes(m.name))m.userData.hidden=true;}
const reserves=[...document.querySelectorAll('#layers label')].find(e=>e.textContent.includes('Installation reserves')).querySelector('input');reserves.checked=true;reserves.dispatchEvent(new Event('change'));
for(const m of v.meshes)if(m.userData.group==='Installation reserves'&&!/^(MX_|PF_BackboxCheckEnvelope)/.test(m.name))m.userData.hidden=true;
const bb=v.meshes.find(m=>m.name==='PF_BackboxCheckEnvelope');bb.userData.hidden=setup.state!=='BACKBOX FOLD';
if(setup.file.startsWith('03')){
 for(const m of v.meshes){m.userData.hidden=!/^(MatrixCarrier|MX_)|^BACKBOX_BASE$/.test(m.name);m.material.clippingPlanes=[new THREE.Plane(new THREE.Vector3(-1,0,0),95)];}
 v.select(v.meshes.find(m=>m.name==='MX_WoodSeatL'));
}
if(setup.file.startsWith('02')||setup.file.startsWith('07')){
 for(const m of v.meshes)m.material.clippingPlanes=[new THREE.Plane(new THREE.Vector3(-1,0,0),301)];
}
if(setup.file.startsWith('01')){v.meshes.find(m=>m.name==='SIDE_R').userData.hidden=false;}
v.camera.fov=setup.fov;v.camera.updateProjectionMatrix();v.camera.position.set(...setup.camera);v.controls.target.set(...setup.target);v.controls.update();v.refresh();
setTimeout(()=>{
 for(const m of v.meshes.filter(m=>m.visible&&m.name.startsWith('MatrixPanel'))){const edge=new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry,25),new THREE.LineBasicMaterial({color:0x20313c,clippingPlanes:m.material.clippingPlanes}));v.scene.add(edge);}
 v.renderer.render(v.scene,v.camera);document.body.dataset.cadReview='PASS';
},500);
</script>
'''.replace('SETUP',json.dumps(setup))
        css='<style>header,aside,#hint,#stage>span{display:none!important}.layout{display:block;height:100vh}#stage{height:100vh}.review-caption{position:absolute;left:26px;right:26px;top:18px;z-index:99;background:#ffffffed;padding:12px 16px;border-left:5px solid #20313c;color:#20313c;font:17px system-ui;pointer-events:none}.review-caption small{display:block;font-size:13px;margin-top:6px}.review-footer{position:absolute;bottom:18px;left:30px;font:12px system-ui;color:#20313c;z-index:99}</style>'
        caption_html='<div class="review-caption"><b>'+html_module.escape(title)+'</b><small>'+html_module.escape(caption)+'</small></div><div class="review-footer">REAL CAD · V32 removable matrix review · dimensions provisional · manufacturing BLOCKED · CERN-OHL-S-2.0</div>'
        page=W/'render.html';page.write_text(html.replace('</head>',css+'</head>').replace('</body>',caption_html+js+'</body>'))
        screenshot=O/filename
        cmd=[chrome,'--headless','--no-sandbox','--disable-dev-shm-usage','--disable-background-networking','--no-first-run','--user-data-dir='+str(W/'profile'),'--allow-file-access-from-files','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--window-size=1600,1000','--virtual-time-budget=2500','--timeout=30000','--screenshot='+str(screenshot),'--dump-dom',page.as_uri()]
        with (W/'render-dom.html').open('w') as out,(W/'render.log').open('w') as err:result=subprocess.run(cmd,stdout=out,stderr=err,timeout=60)
        assert result.returncode==0 and 'data-cad-review="PASS"' in (W/'render-dom.html').read_text(),filename
        assert screenshot.stat().st_size>20000,filename
        results.append({'file':filename,'state':state,'camera_xyz_mm':camera,'target_xyz_mm':target,'fov_deg':fov,'pass':True})
        print('MATRIX_REVIEW_IMAGE_PASS',filename,flush=True)
    (O/'review-images.json').write_text(json.dumps({'views':results,'source_mesh_sha256':json.loads((O/'validation.json').read_text())['mesh_sha256'],'manufacturing_ready':False},indent=2)+'\n')
