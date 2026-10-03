/** Offline animation/packaging regression. CERN-OHL-S-2.0. */
import {chromium} from 'playwright';import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
const R=process.cwd(),O=path.join(R,'exports/generated/assembly-v333'),checks=[],errors=[],net=[],views=[];
const check=(ok,name,details)=>{checks.push({name,pass:!!ok,details});if(!ok)throw Error(name+' '+JSON.stringify(details));};
const browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try{
const ctx=await browser.newContext({viewport:{width:1600,height:1050},offline:true}),p=await ctx.newPage();p.on('pageerror',e=>errors.push(e.message));p.on('request',r=>{if(r.url().startsWith('http'))net.push(r.url());});
await p.goto('file://'+path.join(R,'exports/generated/viewer-v32/index.html'));await p.waitForFunction(()=>document.body.dataset.animationReady==='true',null,{timeout:90000});
async function shot(n,title){await p.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));await p.screenshot({path:path.join(O,n+'.png')});views.push({image:n+'.png',title});}
check(await p.evaluate(()=>animation333.data.clips.length===44),'31 assembly +11 service +2 packing clips');
check(await p.evaluate(()=>animation333.data.metrics.manufacturing_pieces===130&&animation333.data.metrics.canonical_families===66),'Metrics from authoritative inventory');
await p.locator('#metrics-panel').evaluate(e=>e.open=true);await shot('01-metrics','Project metrics and current cabinet');
const clips=await p.evaluate(()=>animation333.data.clips.map(c=>({id:c.id,type:c.type})));
for(const c of clips){
 await p.evaluate(id=>animation333.start(id),c.id);
 for(const t of [0,.25,.5,.75,1])await p.evaluate(t=>animation333.seek(t),t);
 check(await p.evaluate(()=>[...viewer.installed,...viewer.detail,...animation333.packingMeshes].every(m=>[...m.position.toArray(),...m.quaternion.toArray()].every(Number.isFinite))),'Finite transforms '+c.id);
 if(c.type==='assembly')check(await p.evaluate(()=>viewer.detail.some(m=>m.visible)),'Assembly/checkpoint has visible real CAD '+c.id);
 if(c.type==='assembly')check(await p.locator('#mode-tag').textContent().then(t=>t.includes('SCHEMATIC ASSEMBLY ANIMATION')),'Honest assembly label '+c.id);
}
// Numeric endpoints: exact accepted service vertices under the animated transform.
async function endpoint(id,state,names){
 return await p.evaluate(({id,state,names})=>{
  animation333.exit();viewer.applyState(state);const refs={};for(const name of names){const m=viewer.installed.find(m=>m.name===name);refs[name]=m.geometry.attributes.position.array.slice();}
  animation333.start(id);animation333.seek(1);let max=0;
  for(const name of names){const m=viewer.installed.find(m=>m.name===name);m.updateMatrix();const a=m.geometry.attributes.position.array,r=refs[name];if(a.length!==r.length)return {differentTopology:name};for(let i=0;i<a.length;i+=3){const v=new THREE.Vector3(a[i],a[i+1],a[i+2]).applyMatrix4(m.matrix);let nearest=Infinity;for(let j=0;j<r.length;j+=3)nearest=Math.min(nearest,Math.hypot(v.x-r[j],v.y-r[j+1],v.z-r[j+2]));max=Math.max(max,nearest);}}
  return {max};
 },{id,state,names});
}
for(const [id,state,names] of [['service-pf-service','PLAYFIELD SERVICE 50°',['PF_BasePlywood','PLAYFIELD_ENVELOPE']],['service-pf-lift','PLAYFIELD LIFT-OUT',['PF_BasePlywood']],['service-fold','BACKBOX FOLD 90°',['BB_Floor','BB_Backglass','BB_LowerCassetteFrame','BB_DoorL']],['service-doors','BACKBOX REAR DOORS OPEN',['BB_DoorL','BB_DoorR']],['service-unlock','BACKBOX UNLOCKED',['BB_UprightLockLKnob','BB_UprightLockRKnob']]]){
 const result=await endpoint(id,state,names);check(result.max<(id==='service-unlock'?.6:.002),'Matches accepted endpoint '+id,result);
}
await p.evaluate(()=>{animation333.start('assembly-05.1');animation333.seek(.28);});await shot('02-assembly','Schematic cradle assembly — real pieces and F01');
await p.evaluate(()=>{animation333.start('pack');animation333.seek(1);});check(await p.evaluate(()=>animation333.packingMeshes.length===130&&animation333.packingMeshes.every(m=>m.visible)),'Packing includes all130 actual members once');await shot('03-packages','Preferred25kg wood bundle candidate');
await p.evaluate(()=>animation333.explodedPacking());await shot('14-exploded-packing','Exploded packing — actual layer order');await p.evaluate(()=>{animation333.start('pack');animation333.seek(.4);});await shot('04-packing-layer','Layer-by-layer packing / part identification');
await p.evaluate(()=>{animation333.start('unpack');animation333.seek(.35);});await shot('05-unpacking','Unpack and identify pieces');
for(const [id,t,n,title] of [['service-fold',.5,'06-fold45','Validated populated fold45°'],['service-doors',.75,'07-doors','Active then passive door sweep'],['service-unlock',.3,'08-lock-parking','Rear-operated lock release and parking'],['service-glass',.6,'09-glass','Glass lift with display retained'],['service-display',.65,'10-display','Front display withdrawal'],['service-cassette',.7,'11-cassette','Independent cassette withdrawal'],['service-fan',.7,'12-fan','Fan service with doors open']]){await p.evaluate(({id,t})=>{animation333.start(id);animation333.seek(t);},{id,t});await shot(n,title);}
// Playback controls with touch context and offline operation.
await ctx.close();const touchctx=await browser.newContext({viewport:{width:834,height:1194},hasTouch:true,offline:true}),touch=await touchctx.newPage();await touch.goto('file://'+path.join(R,'exports/generated/viewer-v32/index.html'));await touch.waitForFunction(()=>document.body.dataset.animationReady==='true');
await touch.evaluate(()=>animation333.start('service-fold'));await touch.locator('#anim-play').tap();await touch.waitForFunction(()=>animation333.progress>0,null,{timeout:10000});check(await touch.evaluate(()=>animation333.progress>0&&animation333.playing),'Tablet touch PLAY advances');await touch.locator('#anim-pause').tap();const at=await touch.evaluate(()=>animation333.progress);await touch.waitForTimeout(150);check(await touch.evaluate(()=>animation333.progress)===at,'PAUSE stable');
await touch.selectOption('#anim-speed','2');await touch.locator('#anim-restart').tap();check(await touch.evaluate(()=>animation333.progress===0),'RESTART');await touch.locator('#anim-next').tap();check(await touch.evaluate(()=>animation333.clip.id==='service-glass'),'NEXT');await touch.locator('#anim-prev').tap();check(await touch.evaluate(()=>animation333.clip.id==='service-fold'),'PREVIOUS');
await touch.locator('#lang-pt').tap();await touch.locator('#palette').selectOption('accessible');await touch.waitForTimeout(150);check(await touch.locator('#anim-play').textContent()==='REPRODUZIR','Portuguese playback');check(await touch.evaluate(()=>[...document.querySelectorAll('#animation-bar button,#animation-bar select')].filter(e=>e.getClientRects().length).every(e=>e.getBoundingClientRect().height>=44)),'Tablet44px playback targets');check(await touch.evaluate(()=>document.documentElement.scrollWidth===innerWidth),'Tablet no horizontal overflow');await touch.screenshot({path:path.join(O,'13-tablet.png')});views.push({image:'13-tablet.png',title:'Tablet playback — PT-BR / Accessible'});
await touch.locator('#anim-exit').tap();check(await touch.evaluate(()=>viewer.installed.every(m=>m.quaternion.equals(new THREE.Quaternion()))),'Exit clears motion transforms');await touchctx.close();
check(!errors.length,'No JS errors',errors);check(!net.length,'Offline no network',net);
fs.writeFileSync(path.join(O,'browser-validation.json'),JSON.stringify({pass:true,checks,errors,network:net,tablet_playback:'PASS_EMULATED_TOUCH_PHYSICAL_FPS_NOT_CERTIFIED',viewer_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(R,'exports/generated/viewer-v32/index.html'))).digest('hex')},null,2)+'\n');fs.writeFileSync(path.join(O,'review-views.json'),JSON.stringify(views,null,2)+'\n');console.log('V333_BROWSER_PASS',checks.length);
}finally{await browser.close();}
