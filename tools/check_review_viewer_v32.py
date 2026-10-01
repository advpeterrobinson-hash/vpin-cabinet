"""Render the six required CAD/viewer review views and exercise service states. CERN-OHL-S-2.0."""
from pathlib import Path
import json
import re
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exports/generated/viewer-v32'
WORK=ROOT/'.work/service-correction-v32/browser';WORK.mkdir(parents=True,exist_ok=True)
browser=shutil.which('google-chrome') or shutil.which('chromium')
assert browser, 'Chrome/Chromium required for actual WebGL screenshots'
html=(OUT/'index.html').read_text()
smoke=r'''
<script>
try {
const v=window.viewer;if(!v)throw Error('viewer failed to start');
const expect=(ok,name)=>{if(!ok)throw Error(name)};
v.reviewView('play-oblique');
for(const state of ['PLAY','SERVICE','LIFT-OUT','EXPLODED']){
 v.applyState(state);expect(v.currentState()===state,'state selection');
 const dowel=v.meshes.find(m=>m.name==='PF_WoodDowel');
 expect(dowel.visible,'wooden dowel visibility');
 for(const name of ['PF_OpenCradleL','PF_OpenCradleR'])expect(v.meshes.find(m=>m.name===name).visible,'open cradle visible');
 expect(v.meshes.filter(m=>/^PF_CommercialStrap/.test(m.name)&&m.visible).length===4,'exactly four straps');
 const display=v.meshes.find(m=>m.name==='PLAYFIELD_ENVELOPE');
 expect(display.visible===(state!=='EXPLODED'),'display presence');
 if(state==='LIFT-OUT')expect(Math.abs(dowel.geometry.boundingBox.min.z-dowel.userData.playGeometry.boundingBox.min.z-42)<.01,'42mm vertical lift');

}
v.reviewView(new URLSearchParams(location.search).get('review')||'player-left');
v.reviewView('play-oblique');
const part=v.meshes.find(m=>m.name==='LeafButton_primary_L');v.select(part);
document.getElementById('isolate').click();expect(v.meshes.filter(m=>m.visible).length===1,'isolate');
document.getElementById('hide').click();expect(!part.visible,'hide');
document.getElementById('search').value='LeafButton_primary_L';document.getElementById('search').dispatchEvent(new Event('input'));
expect(document.getElementById('parts').children.length===1,'search');
document.getElementById('reset').click();
document.getElementById('axis').value='z';document.getElementById('axis').dispatchEvent(new Event('change'));
expect(v.meshes[0].material.clippingPlanes.length===1,'cut');
document.getElementById('reset').click();expect(v.meshes[0].material.clippingPlanes.length===0,'restore cut');
document.getElementById('search').value='';document.getElementById('search').dispatchEvent(new Event('input'));
v.reviewView(new URLSearchParams(location.search).get('review')||'player-left');
document.body.dataset.reviewSmoke='PASS';
}catch(e){document.body.dataset.reviewSmoke='FAIL';document.getElementById('error').hidden=false;document.getElementById('error').textContent='SMOKE FAIL: '+e.message;}
</script>
'''
page=WORK/'smoke.html';page.write_text(html.replace('</body>',smoke+'</body>'))
views=['player-left','player-right','play-oblique','service','side-detail','closed-detail']
results=[]
for i,view in enumerate(views,1):
    screenshot=OUT/f'{i:02d}-{view}.png'
    command=[browser,'--headless','--no-sandbox','--disable-dev-shm-usage','--disable-background-networking',
        '--no-first-run','--user-data-dir='+str(WORK/'profile'),'--allow-file-access-from-files',
        '--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader',
        '--window-size=1600,1100','--virtual-time-budget=1800','--timeout=25000',
        '--screenshot='+str(screenshot),'--dump-dom',page.as_uri()+'?review='+view]
    with (WORK/f'{view}.dom').open('w') as output,(WORK/f'{view}.log').open('w') as errors:
        process=subprocess.run(command,stdout=output,stderr=errors,timeout=50)
    dom=(WORK/f'{view}.dom').read_text()
    assert process.returncode==0 and 'data-review-smoke="PASS"' in dom, view+' browser runtime failed'
    assert screenshot.stat().st_size>20000, 'Blank screenshot: '+view
    assert '<canvas' in dom and not re.search(r'<div id="error" role="alert"\s*>',dom),view+' WebGL error'
    results.append({'view':view,'pass':True,'screenshot':str(screenshot.relative_to(ROOT))})
    print('VIEWER_REVIEW_PASS',view,flush=True)
(OUT/'browser-verification.json').write_text(json.dumps({'views':results,'states_checked':4,
    'checks':['WebGL render','state selection','display position','wooden dowel, open cradles and exactly four straps visible','42mm lift-out','isolate','hide','search','cut','restore'],
    'manufacturing_ready':False,'structural_proof':False},indent=2)+'\n')
