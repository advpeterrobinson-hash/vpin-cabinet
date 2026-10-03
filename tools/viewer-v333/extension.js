/* V33.3 documentation overlay. Original CERN-OHL-S-2.0; no geometry authority. */
(async()=>{
'use strict';
while(!window.viewer)await new Promise(r=>setTimeout(r,30));
const V=window.viewer,T=THREE,$=id=>document.getElementById(id),Q=JSON.parse($('v333-data').textContent);$('v333-data').remove();
const tr=(a,b)=>V.language()==='en'?a:b,L=o=>o[V.language()]||o.en,clamp=x=>Math.max(0,Math.min(1,x));
const style=document.createElement('style');style.textContent=`#animation-bar{position:absolute;z-index:4;left:12px;right:12px;bottom:110px;max-width:760px;background:#fffffff2;border:1px solid #8b9fac;padding:10px;border-radius:8px}#animation-bar .buttons{display:flex;flex-wrap:wrap;gap:5px}#animation-bar button,#animation-bar select{min-width:44px;min-height:44px;padding:7px}#animation-bar input{width:100%;min-height:28px}#animation-progress{font-size:12px;max-height:48px;overflow:auto}.metric-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px}.metric-grid strong{display:block;font-size:18px}.metric-grid div{background:#edf2f5;padding:9px}.packing-label{position:absolute;background:#fffffff0;border:1px solid #20313c;padding:4px;font-size:12px;pointer-events:none}.v333-small{font-size:12px}#animation-status{border-left:3px solid #20313c;padding-left:8px;font-size:12px}@media(max-width:650px){#animation-bar{bottom:126px}#animation-bar button{font-size:12px}}`;document.head.append(style);
const panel=document.createElement('section');panel.id='v333-panel';document.querySelector('aside').insertBefore(panel,document.querySelector('aside').children[2]);
const bar=document.createElement('section');bar.id='animation-bar';bar.hidden=true;$('stage').append(bar);
let clip=null,progress=0,playing=false,speed=1,last=0,base=[],helpers=[],labels=[],packingMeshes=[],packReady=false,packLayerCount=0,animationActive=false,packingSeparators=[];
const required=m=>m.userData.meta.kind==='wood'||m.userData.meta.classification==='REQUIRED_FLATPACK_HARDWARE';
function textUI(){
 const sel=$('animation-choice')?.value||Q.clips[0].id;
 panel.innerHTML=`<details id="metrics-panel"><summary>${tr('PROJECT METRICS','MÉTRICAS DO PROJETO')}</summary><div class="metric-grid">${[[Q.metrics.manufacturing_pieces,tr('wood pieces','peças de madeira')],[Q.metrics.canonical_families,tr('wood families','famílias de madeira')],[Q.metrics.wood_mass_kg.toFixed(2)+' kg',tr('wood at650kg/m³','madeira a650kg/m³')],[Q.metrics.preliminary_sheets,tr('full-sheet assumption','hipótese de chapas inteiras')],[Q.metrics.known_fastener_minimum+' + ?',tr('known Fxx minimum','mínimo Fxx conhecido')],[Q.metrics.hardware_models,tr('hardware families','famílias de ferragens')]].map(([v,k])=>`<div><strong>${v}</strong>${k}</div>`).join('')}</div><p class="hold">${Q.metrics.manufacturing_status} · ${Q.metrics.coupon_status}<br>${tr('MANUFACTURING BLOCKED · Coupon awaiting production lot and validation.','FABRICAÇÃO BLOQUEADA · Cupom aguarda lote real e validação.')}</p><p class="v333-small">${tr('Required fasteners: ','Fixadores obrigatórios: ')}${Q.hardware.required_Fxx_models} ${tr('models; formula families','modelos; famílias por fórmula')} ${Q.hardware.formula_driven_Fxx.join(', ')}. TBD: ${Q.hardware.TBD_Fxx.join(', ')}.</p><p class="v333-small">${tr('Mechanical / full-build nominal scenarios','Cenários nominais mecânico / completo')}: ${Q.mass.mechanical_scenario_kg[1].toFixed(1)} / ${Q.mass.full_planning_build_kg[1].toFixed(1)} kg. ${tr('Includes explicit unknown-hardware allowance, not a weighed total.','Inclui provisão explícita de ferragens desconhecidas; não é total pesado.')}</p><a href="../assembly-v333/README.md" target="_blank">${tr('Material / mass / packing / audit report','Relatório de material / massa / embalagem / auditoria')}</a></details><details id="animation-panel"><summary>${tr('ASSEMBLY / SERVICE / PACKING','MONTAGEM / SERVIÇO / EMBALAGEM')}</summary><label>${tr('Process','Processo')}<select id="animation-choice">${Q.clips.map(c=>`<option value="${c.id}">${L(c.title)}</option>`).join('')}</select></label><button id="animation-open" class="full">${tr('OPEN ANIMATION','ABRIR ANIMAÇÃO')}</button><p id="animation-status">${tr('31 schematic assembly clips; validated rigid service paths identified separately. No manufacturing release.','31 animações esquemáticas; trajetos rígidos de serviço validados identificados separadamente. Sem liberação de fabricação.')}</p></details>`;
 $('animation-choice').value=sel;$('animation-open').onclick=()=>start($('animation-choice').value);
 bar.innerHTML=`<div id="animation-title"></div><input id="animation-scrub" type="range" min="0" max="1" step="0.001" value="${progress}" aria-label="${tr('Animation position','Posição da animação')}"><div class="buttons"><button id="anim-prev">${tr('PREVIOUS','ANTERIOR')}</button><button id="anim-play">${tr('PLAY','REPRODUZIR')}</button><button id="anim-pause">${tr('PAUSE','PAUSAR')}</button><button id="anim-next">${tr('NEXT','PRÓXIMA')}</button><button id="anim-restart">${tr('RESTART','REINICIAR')}</button><select id="anim-speed" aria-label="${tr('Playback speed','Velocidade')}"><option value="0.5">0.5×</option><option value="1">1×</option><option value="2">2×</option></select><button id="anim-pack-explode">${tr('PACK LAYERS','CAMADAS')}</button><button id="anim-exit">${tr('CLOSE','FECHAR')}</button></div><div id="animation-progress" aria-live="polite"></div>`;
 $('anim-pack-explode').hidden=clip?.type!=='packing';$('anim-pack-explode').onclick=()=>window.animation333.explodedPacking();$('anim-speed').value=String(speed);$('anim-speed').onchange=e=>speed=Number(e.target.value);
 $('anim-play').onclick=()=>{if(progress===1)seek(0);playing=true;};$('anim-pause').onclick=()=>playing=false;$('anim-restart').onclick=()=>{playing=false;seek(0);};$('anim-prev').onclick=()=>jump(-1);$('anim-next').onclick=()=>jump(1);$('anim-exit').onclick=exit;
 $('animation-scrub').oninput=e=>{playing=false;seek(Number(e.target.value));};
 if(clip){$('animation-title').textContent=L(clip.title);$('animation-status').textContent=L(clip.note);}
}
function resetTransforms(){for(const m of [...V.installed,...V.detail]){m.position.set(0,0,0);m.quaternion.identity();m.scale.set(1,1,1);m.material.opacity=m.userData.baseOpacity;m.material.transparent=m.userData.baseOpacity<1;m.material.emissive?.setHex(0);m.material.depthWrite=m.userData.baseOpacity>=1;}}
function clearHelpers(){for(const h of helpers){V.scene.remove(h);h.geometry?.dispose();h.material?.dispose();}helpers=[];for(const l of labels)l.el.remove();labels=[];}
function exit(){playing=false;animationActive=false;bar.hidden=true;clearHelpers();for(const m of [...packingMeshes,...packingSeparators])m.visible=false;resetTransforms();V.applyState('PLAY');}
function jump(d){const i=Q.clips.indexOf(clip);start(Q.clips[Math.max(0,Math.min(Q.clips.length-1,i+d))].id);}
function geom(id){if(V.geometryCache.has(id))return V.geometryCache.get(id);const p=V.data.geometry[id],g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(p.vertices.flat(),3));g.setIndex(p.faces.flat());g.computeVertexNormals();g.computeBoundingBox();V.geometryCache.set(id,g);return g;}
function restoreBase(){for(const b of base){b.m.geometry=b.g;b.m.visible=b.visible;b.m.position.set(0,0,0);b.m.quaternion.identity();b.m.material.opacity=b.opacity;b.m.material.transparent=b.opacity<1;b.m.material.depthWrite=b.opacity>=1;b.m.material.emissive?.setHex(0);}}
function spin(m,axis,angle,pivot){const q=new T.Quaternion().setFromAxisAngle(new T.Vector3(...axis),angle),v=new T.Vector3(...pivot);m.quaternion.copy(q);m.position.copy(v).sub(v.clone().applyQuaternion(q));}
function move(m,v){m.position.set(...v);}
function label(m,text){const el=document.createElement('div');el.className='packing-label';el.textContent=text;$('stage').append(el);labels.push({m,el});}
function makePacking(){
 if(packReady)return;
 V.applyState('EXPLODED DETAILED');const chosen=Q.packaging.candidates.find(c=>c.target_kg===25);let bi=0,rank=0;
 for(const b of chosen.bundles){
  const bx=(bi%2)*1550,by=Math.floor(bi/2)*1000;bi++;
  for(const l of b.layers){
   for(const p of l.pieces){
    const src=V.detail.find(m=>m.name===p.instance_id),info=Q.pieces[p.instance_id];if(!src)throw Error('Missing packing member '+p.instance_id);
    const inv=new T.Matrix4().fromArray(info.local_to_installed_matrix).transpose().invert();
    const trans=new T.Matrix4().makeTranslation(-info.finished_xy_bounds_mm[0],-info.finished_xy_bounds_mm[1],0);
    let orient=new T.Matrix4();if(p.rotated)orient.makeRotationZ(-Math.PI/2).premultiply(new T.Matrix4().makeTranslation(0,info.finished_xy_size_mm[0],0));
    const dest=new T.Matrix4().makeTranslation(bx+20+p.x,by+20+p.y,l.z).multiply(orient).multiply(trans).multiply(inv);
    const g=src.geometry.clone().applyMatrix4(dest),m=new T.Mesh(g,src.material.clone());m.name=p.instance_id;m.userData={...src.userData,pack:{rank,bundle:b.id,layer:l.order,id:p.id},baseOpacity:1};m.visible=false;V.scene.add(m);packingMeshes.push(m);
   }const sep=new T.Mesh(new T.BoxGeometry(b.L,b.W,2),new T.MeshStandardMaterial({color:0xe2e4e7,transparent:true,opacity:.25,depthWrite:false}));sep.position.set(bx+20+b.L/2,by+20+b.W/2,l.z+l.t+1);sep.userData.pack={rank,bundle:b.id,layer:l.order};sep.userData.baseZ=sep.position.z;sep.visible=false;V.scene.add(sep);packingSeparators.push(sep);rank++;
  }
  b.viewer_origin=[bx,by,0];
 }packLayerCount=rank;packReady=true;
}
function start(id){
 exit();clip=Q.clips.find(c=>c.id===id);if(!clip)throw Error('Unknown clip '+id);
 $('manual-panel').hidden=true;document.querySelectorAll('.part-label').forEach(e=>e.remove());animationActive=true;bar.hidden=false;progress=0;playing=false;V.select(null);resetTransforms();
 if(clip.type==='assembly'){
  V.applyState('EXPLODED DETAILED');$('tray').checked=false;V.refresh();
  for(const m of V.detail){m.position.set(0,0,0);m.visible=required(m)&&!m.userData.meta.tray&&(Number(m.userData.meta.stage)<=Number(clip.stage)||['00','01'].includes(clip.stage));}
  V.cameraPreset(Number(clip.stage)>=8&&Number(clip.stage)<=14?'BACKBOX REAR':'PLAYER');V.frame(V.detail.filter(m=>m.visible));
 }else if(clip.type==='packing'){
  makePacking();for(const m of [...V.installed,...V.detail])m.visible=false;for(const m of packingMeshes)m.visible=true;
  V.camera.position.set(3500,-3200,3500);V.controls.target.set(1400,400,100);V.frame(packingMeshes);
  const b=Q.packaging.candidates.find(c=>c.target_kg===25).bundles;
  for(const p of b){const box=new T.Box3(new T.Vector3(...p.viewer_origin),new T.Vector3(p.viewer_origin[0]+p.external_LWH_mm[0],p.viewer_origin[1]+p.external_LWH_mm[1],p.external_LWH_mm[2]));const h=new T.Box3Helper(box,0x3f5260);V.scene.add(h);helpers.push(h);}
 }else{
  const mode=clip.mode;V.applyState(['DOORS','LOCK','FAN'].includes(mode)?'BACKBOX REAR DOORS OPEN':mode==='FOLD'?'BACKBOX FOLD 90°':'PLAY');
  if(['PF','PF_LIFT','MATRIX','SHELF'].includes(mode))for(const m of V.installed){if(m.name==='CandidateGlass'||mode!=='MATRIX'&&m.userData.meta.group==='matrix')m.visible=false;}
  if(mode==='SHELF')for(const m of V.installed)if(m.userData.meta.group==='playfield')m.visible=false;
  if(mode==='DISPLAY')for(const m of V.installed)if(['glass','retainer','bezel'].includes(Q.motions.groups[m.name])||m.name.includes('MonitorStopScrew')||m.name.includes('MonitorClampReserve'))m.visible=false;
  if(mode==='GLASS')for(const m of V.installed)if(Q.motions.groups[m.name]==='retainer')m.visible=false;
  if(mode==='CASSETTE')for(const m of V.installed)if(m.name.includes('CassetteFastener')||m.name.includes('CassetteBolt'))m.visible=false;
  if(mode==='DOORS'){
   // Use PLAY rigid geometry for leaves with retracted latch endpoint geometry.
   for(const m of V.installed){const group=Q.motions.groups[m.name];if(['doorL','doorR'].includes(group))m.geometry=geom(V.data.states.PLAY[m.name]||m.userData.baseGeometry);}
  }
  V.cameraPreset(['PF','PF_LIFT','MATRIX','SHELF'].includes(mode)?'INTERIOR':['GLASS','DISPLAY','CASSETTE','FOLD'].includes(mode)?'BACKBOX FRONT':'BACKBOX REAR');
 }
 base=V.installed.map(m=>({m,g:m.geometry,visible:m.visible,opacity:m.material.opacity}));
 $('anim-pack-explode').hidden=clip.type!=='packing';$('animation-choice').value=id;$('animation-panel').open=true;$('animation-title').textContent=L(clip.title);$('animation-status').textContent=L(clip.note);seek(0);
 if(clip.type==='assembly'&&['00','01'].includes(clip.stage))V.frame(V.detail.filter(m=>m.visible));
 if(clip.type==='service'){
  const relevant=()=>V.installed.filter(m=>m.visible&&(['PF','PF_LIFT','MATRIX','SHELF'].includes(clip.mode)||m.name.startsWith('BB_')));
  const box=new T.Box3();for(const m of relevant())box.union(new T.Box3().setFromObject(m));seek(1);for(const m of relevant())box.union(new T.Box3().setFromObject(m));seek(0);
  if(!box.isEmpty()){const size=box.getSize(new T.Vector3()),dummy=new T.Mesh(new T.BoxGeometry(size.x,size.y,size.z),new T.MeshBasicMaterial());dummy.position.copy(box.getCenter(new T.Vector3()));V.frame([dummy]);dummy.geometry.dispose();dummy.material.dispose();}
 }
}
let flexObjects={};
function flexLoop(side,deg){
 const cfg=Q.motions.fan_flex,a=new T.Vector3(...cfg.fixed_anchor_left_mm),b=new T.Vector3(...cfg.door_anchor_left_mm);if(side==='R'){a.x=600-a.x;b.x=600-b.x;}
 const h=Q.motions.door_axes[side==='L'?0:1],p=new T.Vector3(h[0],h[1],0);b.sub(p).applyAxisAngle(new T.Vector3(0,0,1),deg*Math.PI/180*(side==='L'?1:-1)).add(p);
 const points=amp=>Array.from({length:81},(_,i)=>{const t=i/80;return new T.Vector3(a.x*(1-t)+b.x*t+(side==='L'?1:-1)*amp*Math.sin(Math.PI*t),a.y*(1-t)+b.y*t,a.z+(b.z-a.z)*(1-Math.cos(Math.PI*t))/2);});
 let lo=0,hi=100;for(let i=0;i<25;i++){const mid=(lo+hi)/2,pts=points(mid);let len=0;for(let j=1;j<pts.length;j++)len+=pts[j].distanceTo(pts[j-1]);if(len<cfg.length_mm)lo=mid;else hi=mid;}
 let obj=flexObjects[side];if(!obj||!helpers.includes(obj)){obj=new T.Line(new T.BufferGeometry(),new T.LineBasicMaterial({color:0x273f56}));V.scene.add(obj);helpers.push(obj);flexObjects[side]=obj;}obj.geometry.dispose();obj.geometry=new T.BufferGeometry().setFromPoints(points((lo+hi)/2));
}
function seek(t){
 progress=clamp(t);if(!clip)return;$('animation-scrub').value=progress;
 for(const l of labels)l.el.remove();labels=[];
 let caption='';const p=progress;
 if(clip.type==='assembly'){
  for(const m of V.detail){const meta=m.userData.meta,same=meta.stage===clip.stage;let visible=required(m)&&!meta.tray&&Number(meta.stage)<=Number(clip.stage);if(clip.stage==='01')visible=meta.kind==='wood';if(clip.stage==='00')visible=required(m)&&!meta.tray;m.visible=visible;if(!visible)continue;
   m.position.set(0,0,0);m.material.opacity=same||clip.stage==='00'?m.userData.baseOpacity:.32;m.material.transparent=m.material.opacity<1;m.material.depthWrite=m.material.opacity>=1;m.material.emissive.setHex(0);
   if(same||clip.stage==='01'){
    // Do not linearly interpolate an unvalidated insertion path. Fade from the
    // semantic exploded pose, then fade into its exact installed position.
    if(clip.first_stage_step||clip.stage==='01'){
     const off=m.userData.entry.offset;if(p<.5)m.position.fromArray(off);
     m.material.opacity=p<.5?1-p*1.6:.2+(p-.5)*1.6;m.material.transparent=m.material.opacity<1;
    }
    m.material.emissive.setHex(0x202020);
   }
  }
  for(const h of helpers){V.scene.remove(h);h.geometry?.dispose();h.material?.dispose();}helpers=[];
  const next=V.detail.filter(m=>m.visible&&m.userData.meta.stage===clip.stage);
  for(const m of next.slice(0,8)){const b=new T.BoxHelper(m,0x20313c);b.material.depthTest=false;b.renderOrder=20;V.scene.add(b);helpers.push(b);const meta=m.userData.meta,h=V.data.hardware.find(h=>h.id===meta.hardware_id),ins=h?.instances.find(i=>i.object===meta.source);const dir=ins?.installation_direction||meta.face_A?.map(v=>-v);if(dir){const a=new T.ArrowHelper(new T.Vector3(...dir).normalize(),new T.Box3().setFromObject(m).getCenter(new T.Vector3()),65,0x20313c,14,8);V.scene.add(a);helpers.push(a);}}
  for(const m of next.slice(0,8))label(m,m.userData.meta.id+' · '+(m.userData.meta.instance||m.userData.meta.hardware_id));
  caption=clip.stage==='00'?tr('PREPARATION CHECKPOINT — cabinet context. ','VERIFICAÇÃO PREPARATÓRIA — contexto do gabinete. ')+L(clip.check):tr('Arrows: nominal install direction, not validated insertion. NEXT / INSPECT: ','Setas: direção nominal, não trajetória validada. PRÓXIMO / INSPECIONAR: ')+clip.piece_ids.join(', ')+tr(' · Hardware: ',' · Ferragens: ')+clip.hardware_ids.join(', ');
 }else if(clip.type==='packing'){
  const f=clip.mode==='UNPACK'?1-p:p,index=Math.min(packLayerCount-1,Math.floor(f*packLayerCount));
  for(const m of packingMeshes){const r=m.userData.pack.rank;m.visible=r<=index&&!(clip.mode==='UNPACK'&&p===1);m.position.z=r===index?(1-(f*packLayerCount-index))*120:0;m.material.emissive.setHex(r===index?0x202020:0);}
  for(const sep of packingSeparators){sep.position.z=sep.userData.baseZ;sep.visible=sep.userData.pack.rank<index&&!(clip.mode==='UNPACK'&&p===1);}
  for(const b of Q.packaging.candidates.find(c=>c.target_kg===25).bundles){const mesh=packingMeshes.find(m=>m.visible&&m.userData.pack.bundle===b.id);if(mesh)label(mesh,b.id+' · '+b.gross_nominal_kg.toFixed(1)+' kg');}
  const current=packingMeshes.filter(m=>m.visible&&m.userData.pack.rank===index);for(const m of current.slice(0,12))label(m,m.userData.pack.bundle+' · '+m.userData.pack.id+' · '+m.name);
  caption=tr('Layer ','Camada ')+(index+1)+' / '+packLayerCount+' · '+current.map(m=>m.userData.pack.bundle+': '+m.userData.pack.id+' / '+m.name).join(', ');
 }else{
  restoreBase();const mode=clip.mode;
  for(const m of V.installed){
   const n=m.name,g=Q.motions.groups[n];
   if(mode==='PF'&&Q.motions.pf_names.includes(n))spin(m,[1,0,0],-50*p*Math.PI/180,Q.motions.pf_axis);
   if(mode==='PF_LIFT'&&Q.motions.pf_names.includes(n))move(m,[0,0,48*p]);
   if(mode==='FOLD'&&Q.motions.fold_names.includes(n))spin(m,[1,0,0],-(1-p)*Math.PI/2,Q.motions.wpc_axis);
   if(mode==='MATRIX'){
    if(n.startsWith('MX_')&&(/Retain|Thumb|Screw/.test(n))&&!n.includes('Fixed'))m.visible=false;
    if(n.startsWith('Matrix')){spin(m,[1,0,0],-26*clamp(p*3)*Math.PI/180,Q.motions.matrix_axis);m.position.y-=68*clamp(p*3-1);m.position.z+=100*clamp(p*3-2);}
    if(n.includes('Connector')||n.includes('CableLoop'))m.visible=false;
   }
   if(mode==='DOORS'){
    let side=g==='doorL'||g==='unlockedL'?'L':g==='doorR'||g==='unlockedR'?'R':null;
    if(side){const deg=100*clamp(p*2-(side==='L'?1:0)),axis=Q.motions.door_axes[side==='L'?0:1];if(g.startsWith('unlocked'))spin(m,[0,0,1],(deg-100)*Math.PI/180*(side==='L'?1:-1),[...axis,0]);else spin(m,[0,0,1],deg*Math.PI/180*(side==='L'?1:-1),[...axis,0]);}
    if(n.startsWith('BB_FlexCorridor'))m.visible=false;
   }
   if(mode==='LOCK'){
    for(const [side,i] of [['L',0],['R',1]])if(n.startsWith('BB_UprightLock'+side)){
     const u=clamp(p*2-i),cfg=Q.motions.locks,src=cfg.lock_centers_xy_mm[i],dst=cfg.parking_centers_xy_mm[i];
     if(n.endsWith('Knob')||n.endsWith('Washer'))move(m,[(dst[0]-src[0])*clamp(u*3-1),(dst[1]-src[1])*clamp(u*3-1),80*clamp(u*3)-44*clamp(u*3-2)]);
     if(n.endsWith('Tether')){m.visible=false;/* Flexible stow/un-stow is not a rigid-body path. */}
    }
   }
   if(mode==='GLASS'&&n==='BB_Backglass')move(m,[0,0,500*p]);
   if(mode==='DISPLAY'&&['display','adapter'].includes(g)&&!n.includes('Reserve'))move(m,[0,-400*p,0]);
   if(mode==='CASSETTE'&&g==='cassette'&&!n.includes('Reserve'))move(m,[0,-240*p,0]);
   if(mode==='FAN'&&['BB_FanL','BB_FanR'].includes(n)){const side=n.endsWith('L')?'L':'R',u=clamp(p*2-(side==='L'?0:1)),v=new T.Vector3(0,-160*u,0).applyAxisAngle(new T.Vector3(0,0,1),100*Math.PI/180*(side==='L'?1:-1));m.position.copy(v);}
   if(mode==='SHELF'&&n.startsWith('SHELF_')&&!n.includes('SUPPORT')){m.material.transparent=true;m.material.opacity=1-p*.95;m.material.emissive.setHex(0x202020);}
  }
  if(mode==='DOORS'){flexLoop('R',100*clamp(p*2));flexLoop('L',100*clamp(p*2-1));}
  caption=tr('Process progress ','Progresso ')+Math.round(100*p)+'%';
 }
 $('animation-progress').textContent=caption;$('mode-tag').textContent=L(clip.title)+' · '+(clip.type==='assembly'?tr('SCHEMATIC ASSEMBLY ANIMATION','ANIMAÇÃO ESQUEMÁTICA DE MONTAGEM'):clip.status.includes('SCHEMATIC_SERVICE')?tr('SCHEMATIC SERVICE','SERVIÇO ESQUEMÁTICO'):tr('REVIEW — NOT FOR CNC','REVISÃO — NÃO USAR NO CNC'));
 $('state-note').textContent=L(clip.note);
}
function tick(now){requestAnimationFrame(tick);const dt=Math.min((now-last)/1000,.1);last=now;if(playing&&animationActive){seek(progress+dt*speed/clip.duration_s);if(progress===1)playing=false;}
 for(const l of labels){const b=new T.Box3().setFromObject(l.m),p=b.getCenter(new T.Vector3()).project(V.camera),w=V.renderer.domElement.clientWidth,h=V.renderer.domElement.clientHeight;l.el.style.left=Math.max(5,Math.min(w-190,(p.x+1)*w/2))+'px';l.el.style.top=Math.max(45,Math.min(h-260,(1-p.y)*h/2))+'px';l.el.hidden=!l.m.visible||p.z>1;}
}
// Any explicit normal viewer action leaves animation mode; camera/palette remain
// usable during playback. Never leave a fold transform on a PLAY mesh.
for(const id of ['service-state','hide-pf','hide-supports','interior','bb-interior','show-all','reset','open-manual','scope','detail-filter','family-focus','search'])$(id).addEventListener(['service-state','scope','detail-filter','family-focus'].includes(id)?'change':id==='search'?'input':'click',()=>{if(animationActive)exit();},true);
for(const id of ['lang-en','lang-pt'])$(id).addEventListener('click',()=>{setTimeout(()=>{textUI();if(animationActive)seek(progress);},0);});
textUI();window.animation333={data:Q,start,seek,exit,get clip(){return clip;},get progress(){return progress;},get playing(){return playing;},get packingMeshes(){return packingMeshes;},explodedPacking:()=>{start('pack');seek(1);for(const m of [...packingMeshes,...packingSeparators]){m.visible=true;m.position.z+=(m.userData.pack.layer-1)*45;}V.frame(packingMeshes);$('mode-tag').textContent=tr('EXPLODED PACKING — LAYER ORDER','EMBALAGEM EXPLODIDA — ORDEM DAS CAMADAS');},play:()=>playing=true,pause:()=>playing=false};
const params=new URLSearchParams(location.search);if(params.has('animation'))start(params.get('animation'));document.body.dataset.animationReady='true';requestAnimationFrame(tick);
})().catch(e=>{console.error(e);const el=document.getElementById('error');el.hidden=false;el.textContent='V33.3: '+e.message;});
