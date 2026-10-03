/* Original tooling review; CERN-OHL-S-2.0. No drilling release. */
(async()=>{
while(!window.viewer)await new Promise(r=>setTimeout(r,30));
const V=window.viewer,T=THREE,D=JSON.parse(document.getElementById('v334-jig').textContent),group=new T.Group();V.scene.add(group);
let side='FL',mode='fit',members=[];
function hide(){group.visible=false;}
function show(m='fit',corner=side){
 side=corner;mode=m;group.clear();members=[];V.select(null);
 for(const o of [...V.installed,...V.detail])o.visible=false;
 for(const [name,shape] of Object.entries(D.scenes[side])){
  const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(shape.vertices.flat(),3));g.setIndex(shape.faces.flat());g.computeVertexNormals();
  const isBlock=name.endsWith('Solid'),isTool=name.startsWith('Drill')||name.startsWith('Bit'),isClamp=name.startsWith('Clamp');
  const mesh=new T.Mesh(g,new T.MeshStandardMaterial({color:isBlock?0xcab081:isClamp?0x59656c:isTool?0x657f92:0x88aaa4,transparent:true,opacity:isTool?.35:1,side:T.DoubleSide,flatShading:true}));mesh.name=name;
  const edge=new T.LineSegments(new T.EdgesGeometry(g,25),new T.LineBasicMaterial({color:0x20313c,transparent:true,opacity:.45}));mesh.add(edge);group.add(mesh);members.push(mesh);
 }
 group.visible=true;const block=members.find(m=>m.name.endsWith('Solid')),center=new T.Box3().setFromObject(block).getCenter(new T.Vector3()),nx=side.endsWith('L')?1:-1,ny=side.startsWith('F')?1:-1;V.controls.target.copy(center);V.camera.position.copy(center).add(new T.Vector3(nx*240-ny*90,ny*240+nx*90,130));V.frame(members.filter(m=>!m.name.startsWith('Drill')));V.camera.position.sub(V.controls.target).multiplyScalar(1.25).add(V.controls.target);seek(0);
}
function seek(t){
 const phase=mode,normal=side==='FL'?[1,1,0]:side==='FR'?[-1,1,0]:side==='RL'?[1,-1,0]:[-1,-1,0];
 for(const m of members){const block=m.name.endsWith('Solid'),bit=m.name.startsWith('Bit'),drill=m.name.startsWith('Drill'),jaw=m.name.startsWith('Clamp');
  m.position.set(0,0,0);m.visible=block||phase!=='place'&&phase!=='test';m.material.opacity=drill?.22:1;if(m.name==='PlateReference'){m.visible=phase==='test';if(phase==='test'){if(t<.5)m.position.set(normal[0]*30,normal[1]*30,0);m.material.opacity=t<.5?1-t*1.6:.2+(t-.5)*1.6;}else continue;}
  if(phase==='place'&&block){if(t<.5)m.position.z=70;m.material.opacity=t<.5?1-t*1.6:.2+(t-.5)*1.6;}
  if(phase==='fit'&&!block){if(t<.5)m.position.set(normal[0]*60,normal[1]*60,30);m.material.opacity=t<.5?1-t*1.6:.2+(t-.5)*1.6;}
  if((bit||drill)&&phase!=='drill')m.visible=false;if(bit&&phase==='test'){m.visible=true;m.material.opacity=.2;}
  if(jaw&&!['clamp','drill'].includes(phase))m.visible=false;
  if(phase==='clamp'&&jaw)m.position.set(normal[0]*20*(1-t),normal[1]*20*(1-t),0);
  if(phase==='drill'&&bit)m.position.set(normal[0]*30*(1-t),normal[1]*30*(1-t),0);
 }
}
const box=document.createElement('section');box.id='leg-jig-panel';document.querySelector('aside').append(box);
function ui(){const pt=V.language()==='pt-BR';box.innerHTML=`<details><summary>${pt?'GABARITO DOS PÉS · FERRAMENTAL':'LEG DRILL JIG · TOOLING'}</summary><select id="jig-corner" aria-label="FL / FR / RL / RR">${['FL','FR','RL','RR'].map(s=>`<option ${s===side?'selected':''}>${s}</option>`).join('')}</select><button id="jig-open">${pt?'INSPECIONAR GABARITO':'INSPECT JIG'}</button><p>${pt?'F: espaçador14mm. R: sem espaçador. Seta em relevo aponta para CIMA. Batente no topo e placa na diagonal.':'F:14mm spacer. R: bare stop. Raised arrow points UP. Stop on top and plate on diagonal.'}</p><p class="hold">${pt?'58 /57,15mm: medir ferragens. Grampos completos, buchas e furadeira: PENDENTES.':'58 /57.15mm: measure hardware. Full clamps, bushings and drill: HOLD.'}</p><a href="../solid-leg-v334/README.md" target="_blank">${pt?'Manual e arquivos STEP / STL /3MF':'Manual and STEP / STL /3MF files'}</a></details>`;
 document.getElementById('jig-open').onclick=()=>{window.animation333.start('jig-fit');};document.getElementById('jig-corner').onchange=e=>{side=e.target.value;window.animation333.start('jig-fit');};}
window.legJig={show,seek,hide,get members(){return members;},get side(){return side;}};ui();
for(const id of ['lang-en','lang-pt'])document.getElementById(id).addEventListener('click',()=>setTimeout(ui,0));
})().catch(console.error);
