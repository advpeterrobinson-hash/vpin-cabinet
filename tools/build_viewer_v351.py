"""V35.1 offline viewer with native full-width states and flat pieces; same UI/palettes."""
from pathlib import Path
import json,gzip,base64,re,copy,hashlib,subprocess
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/widebody-v351';DX=14.325
def read(p):return json.loads(Path(p).read_text())
def bi(en,pt):return {'en':en,'pt-BR':pt}
base=subprocess.check_output(['git','show','11822cb2dc9c7c7b511348df860cb76196d641be:exports/generated/viewer-v32/index.html'],cwd=R,text=True);D=json.loads(gzip.decompress(base64.b64decode(re.search(r'<script id="viewer-data"[^>]*>(.*?)</script>',base,re.S)[1])));Q=json.loads(re.search(r'<script id="v333-data"[^>]*>(.*?)</script>',base,re.S)[1]);N=json.loads(gzip.decompress((O/'viewer-native.json.gz').read_bytes()));reg=read(O/'manufacturing-register.json');audit=read(O/'width-audit.json');mass=read(O/'mass-counts.json');pack=read(O/'packaging.json');oldinst={a['key']:a for a in D['installed']};by={a['source_component']:a for a in reg['parts']};geom={};installed=[]
def put(k,m):geom[k]=m;return k
for n,m in N['states']['PLAY'].items():
 a=copy.deepcopy(oldinst.get(n,oldinst['CandidateGlassChannelL']));a['key']=n;a['geometry']=put('v35-'+n,m);a['meta']['source']=n;a['meta']['model_status']='V35.1 REFERENCE DESIGN; hardware/material/coupon HOLD';a['meta']['geometry_authority']={'file':'exports/generated/widebody-v351/play.FCStd','object':n,'sha256':hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest()}
 if n in by:
  r=by[n];a['meta'].update(families=[r['manufacturing_part_id']],instances=[r['instance_id']],thickness=r['nominal_stock_thickness_mm'],manufacturing_status=[r['manufacturing_status']])
 if n not in oldinst:a['meta'].update(id=n,names=bi(n.replace('_',' '),n.replace('_',' ')),group='hardware',scope='MAIN CABINET',kind='reference',classification='REFERENCE_ONLY_NOT_FROZEN')
 if n in ['CandidateGlassChannelL','CandidateGlassChannelR']:a['meta'].update(names=bi('Commercial polymer glass channel · routed side interface','Canal comercial de polímero · encaixe na lateral'),model_status='03-7135-1 reference; purchased profile/slot WIDTH + DEPTH NULL')
 if n=='CandidateGlass':a['meta']['names']=bi('Widebody tempered glass603.25×1092.20×5.0 reference','Vidro temperado widebody603,25×1092,20×5,0 referência')
 installed.append(a)
# Preserve optional variants as such, recentered rigidly; do not leave old600mm parts in visible states.
for n,a0 in oldinst.items():
 if n in N['states']['PLAY'] or n=='BB_PFRearChannel':continue
 if a0['meta'].get('optional_study') or n.startswith('Underfront_Button6'):
  a=copy.deepcopy(a0);m=copy.deepcopy(D['geometry'][a['geometry']]);m['vertices']=[[v[0]+DX,*v[1:]] for v in m['vertices']];a['geometry']=put('v35-optional-'+n,m);installed.append(a)
D['installed']=installed;D['states']={state:{n:put('v35-'+state+'-'+n,m) for n,m in meshes.items()} for state,meshes in N['states'].items()}
for state in D['states']:
 for a in installed:
  if a['key'] not in D['states'][state]:D['states'][state][a['key']]=None
oldetail={a['meta'].get('instance'):a for a in D['detail'] if a['meta'].get('kind')=='wood'};details=[]
for a in reg['parts']:
 i=a['instance_id'];n=a['source_component'];ob=copy.deepcopy(oldetail.get(i,next(iter(oldetail.values()))));ob['key']=i;ob['geometry']=put('v35-flat-'+i,N['manufacturing_world'][i]);ob['meta'].update(instance=i,source=n,id=a['manufacturing_part_id'],names=bi(a['description_en'],a['description_pt_BR']),thickness=a['nominal_stock_thickness_mm'],manufacturing_status=[a['manufacturing_status']],model_status='EXACT V35.1 MANUFACTURING MEMBER; NOT FOR CNC',geometry_authority={'file':a['finished_member_brep'],'local_to_installed_matrix':a['local_to_installed_matrix']});details.append(ob)
for a0 in D['detail']:
 if a0['meta'].get('kind')=='wood':continue
 n=a0['meta'].get('source');ins=next((a for a in installed if a['key']==n),None)
 if ins:
  a=copy.deepcopy(a0);a['geometry']=ins['geometry'];a['meta']['geometry_authority']=ins['meta']['geometry_authority'];details.append(a)
D['detail']=details
# Optional clean side-gap visualization; not BOM hardware.
for n in ['OptionalLEDEnvelopeL','OptionalLEDEnvelopeR']:
 a=copy.deepcopy(oldinst['CandidateGlassChannelL']);a['key']=n;a['geometry']=put('v35-'+n,N['variants'][n]);a['meta'].update(source=n,id=n,names=bi('Optional LED/diffuser space — not supplied','Espaço opcional LED/difusor — não fornecido'),group='future',kind='reference',classification='FUTURE_ELECTRONICS_HARDWARE',optional_study=True,model_status='CLEARANCE ONLY; no mandatory hardware, machining or wiring');installed.append(a)
 for state in D['states']:D['states'][state][n]=None
# Recenter V34.2 monitor comparison variants too; preserve its controls.
if 'v342_study' in D:
 for n,key in D['v342_study']['variants'].items():
  m=copy.deepcopy(D['geometry'][key]);m['vertices']=[[v[0]+DX,*v[1:]] for v in m['vertices']];put(key,m)
D['geometry']=geom;D['geometry_revision']='V35.1';D['source_head']='11822cb2dc9c7c7b511348df860cb76196d641be';D['manufacturing_release']=False
D['engineering_hold']=bi('V35.1 reference widebody628.65mm; commercial fit, actual hardware/stock/coupon and raised service support HOLD.','V35.1 widebody628,65mm; encaixe comercial, ferragens/material/cupom e apoio elevado PENDENTES.')
Q['motions']['fold_names']=[a['key'] for a in installed if a['key'].startswith('BB_') and a['key']!='BB_PFRearChannel'];Q['motions']['groups']={n:g for n,g in Q['motions']['groups'].items() if n in N['states']['PLAY']}
for k in ['pf_axis','wpc_axis','matrix_axis']:Q['motions'][k][0]+=DX
Q['motions']['door_axes']=[[x+DX,y] for x,y in Q['motions']['door_axes']]
for k in ['lock_centers_xy_mm','parking_centers_xy_mm']:Q['motions']['locks'][k]=[[x+DX,y] for x,y in Q['motions']['locks'][k]]
Q['pieces']={a['instance_id']:{'local_to_installed_matrix':a['local_to_installed_matrix'],'finished_xy_size_mm':[a['finished_xy_bounds_mm'][2]-a['finished_xy_bounds_mm'][0],a['finished_xy_bounds_mm'][3]-a['finished_xy_bounds_mm'][1]],'finished_xy_bounds_mm':a['finished_xy_bounds_mm'],'manufacturing_part_id':a['manufacturing_part_id'],'id':a['manufacturing_part_id'],'instance_id':a['instance_id'],'nominal_stock_thickness_mm':a['nominal_stock_thickness_mm']} for a in reg['parts']}
bundles=[]
for b in pack['bundles']:
 layers=[]
 for i,a in enumerate(b['parts']):
  r=Q['pieces'][a['id']];w,h=r['finished_xy_size_mm'];rot=w<h;ll,ww=sorted([w,h],reverse=True)
  layers.append({'t':a['thickness_envelope_mm'],'z':20+a['stack_z_mm'],'order':i+1,'pieces':[{'instance_id':a['id'],'id':r['id'],'x':a.get('packing_x_mm',(b['L']-ll)/2),'y':a.get('packing_y_mm',(b['W']-ww)/2),'rotated':rot,'mass_kg':a['mass_nominal_kg']}]})
 bundles.append({'id':b['id'],'wood_mass_kg':b['nominal_wood_kg'],'L':b['L'],'W':b['W'],'layers':layers,'external_mm':b['external_mm'],'high_gross_kg':b['high_gross_kg']})
Q['packaging']={'preferred_target_kg':25,'status':'V35.1 PRELIMINARY /1kg packaging allowance; physical shipping qualification pending','candidates':[{'target_kg':25,'bundles':bundles}]};Q['mass'].update(wood_kg=mass['wood_NOMINAL_kg']);Q['metrics'].update(manufacturing_pieces=66,canonical_families=45,wood_mass_kg=mass['wood_NOMINAL_kg']);Q['engineering_hold']=D['engineering_hold']
Q['metrics'].update(wood_finished_reference_mass_kg=mass['wood_NOMINAL_kg'],preliminary_sheets=' / '.join(t+'mm:'+str(d['sheet_count']) for t,d in read(O/'nesting.json').items())+' PRELIMINARY',manufacturing_status='BLOCKED; PURCHASED HARDWARE / COUPON')
for key in ['wood_flatpack_kg','wood_finished_reference_kg','installed_wood_kg']:
 Q['mass'][key]=[mass['wood_LOW_kg'],mass['wood_NOMINAL_kg'],mass['wood_HIGH_kg']]
Q['mass'].update(mechanical_exact_total_kg=None,mechanical_scenario_kg=None,full_planning_build_kg=None,glass_reference_kg=mass['glass_reference_mass_kg'],full_planning_status='UNKNOWN: commercial hardware not measured; no V35.1 total claimed',wood_status='ACTUAL_FINISHED_BREP; packing allowance separate')
D['manual']=read(O/'assembly-manual.json');D['hardware']=read(R/'config/hardware_catalog_v351.json')
cat=D['hardware'];hby={a['id']:a for a in cat['hardware']}
for a in D['installed']:
 n=a['key'];id=cat['object_to_id'].get(n)
 if id in hby:
  h=hby[id];a['meta'].update(id=id,hardware_id=id,names=bi(h['description_en'],h['description_pt_BR']),classification=h['flatpack_classification'],status=h['freeze_status'])
 if n.startswith('CommercialSiderail'):
  a['meta']['optional_study']=True
  for state in D['states']:D['states'][state][n]=None
for clip in Q['clips']:
 if clip.get('type')=='assembly':
  st=next((s for t in D['manual']['stages'] for s in t['steps'] if s['id']==clip.get('step')),None)
  if st:clip.update(action=st['action'],check=st['check'],note=st['hold'])
# Mark existing manual shared source stale dimensions until promoted manual overlay is applied.
D['manual']['v35_overlay']={'width':628.65,'length':1308.1,'backbox_width':780,'glass':[603.25,1092.2,5.0],'service_support':'HOLD'}
# Keep existing UI; append two explicit optional-gap buttons, no geometry changes.
addon='''<div style="position:fixed;right:12px;top:70px;z-index:15;display:grid;grid-template-columns:1fr 1fr;max-width:400px;background:#fff;padding:8px;border:1px solid #888;border-radius:6px"><button id="gap-black" style="min-height:44px">BLACK GAP / VÃO PRETO</button><button id="gap-led" style="min-height:44px">LED SPACE / ESPAÇO LED</button><button id="rail-off" style="min-height:44px">NO SIDERAIL / SEM SIDERAIL</button><button id="rail-on" style="min-height:44px">OPTIONAL RAIL / OPCIONAL</button><small style="display:block;grid-column:1 / -1">V35.1 · commercial architecture / arquitetura comercial · CNC HOLD</small></div><script>window.addEventListener('load',()=>{const style=()=>{if(!window.viewer)return requestAnimationFrame(style);const m=viewer.installed.find(m=>m.name==='PLAYFIELD_ENVELOPE');if(m){m.userData.baseOpacity=1;m.material.opacity=1;m.material.transparent=false;m.material.depthWrite=true;}};style();const toggle=v=>{for(const m of viewer.installed)if(m.name.startsWith('OptionalLEDEnvelope'))m.visible=v;};document.getElementById('gap-black').onclick=()=>toggle(false);document.getElementById('gap-led').onclick=()=>toggle(true);const rails=v=>{for(const m of viewer.installed)if(m.name.startsWith('CommercialSiderail'))m.visible=v;};document.getElementById('rail-off').onclick=()=>rails(false);document.getElementById('rail-on').onclick=()=>rails(true);});</script>'''
base=base.replace('Atlas de montagem V34.2','Atlas de montagem V35.1').replace('Assembly atlas V34.2','Assembly atlas V35.1').replace('</body>',addon+'</body>').replace('Assembly atlas V34.2','Assembly atlas V35.1').replace('../backbox-v342/','../widebody-v351/')
encoded=base64.b64encode(gzip.compress(json.dumps(D,separators=(',',':'),ensure_ascii=False).encode(),mtime=0)).decode()
base=re.sub(r'(<script id="viewer-data"[^>]*>).*?(</script>)',lambda m:m[1]+encoded+m[2],base,flags=re.S)
base=re.sub(r'(<script id="v333-data"[^>]*>).*?(</script>)',lambda m:m[1]+json.dumps(Q,separators=(',',':'),ensure_ascii=False)+m[2],base,flags=re.S)
(O/'viewer.html').write_text(base);print('V35.1_VIEWER',len(installed),len(details),len(geom))
