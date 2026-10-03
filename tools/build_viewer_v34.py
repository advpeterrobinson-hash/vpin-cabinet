"""V34 offline viewer delta; same controls/palettes, actual flat pieces. CERN-OHL-S-2.0."""
from pathlib import Path
import json,gzip,base64,re,subprocess,copy,math,hashlib
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/backbox-v34'
def read(f):return json.loads(Path(f).read_text())
def bi(a,b):return {'en':a,'pt-BR':b}
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
base=subprocess.check_output(['git','show','0993d9768582290915f7166c53507ffd2aa434b6:exports/generated/viewer-v32/index.html'],cwd=R,text=True)
D=json.loads(gzip.decompress(base64.b64decode(re.search(r'<script id="viewer-data"[^>]*>(.*?)</script>',base,re.S)[1])));Q=json.loads(re.search(r'<script id="v333-data"[^>]*>(.*?)</script>',base,re.S)[1])
N=json.loads(gzip.decompress((O/'viewer-native.json.gz').read_bytes()));reg=read(O/'manufacturing-register.json');delta=read(O/'manufacturing-delta.json');manual=read(O/'assembly-manual.json');cat=read(R/'config/hardware_catalog_v34.json');mass=read(O/'mass-counts.json');inv=read(O/'geometry-inventory.json')['parts'];removed=set(N['removed']);owned=set(N['changed'])|set(N['added']);by={a['source_component']:a for a in reg['parts']};oldi={a['key']:a for a in D['installed']};hwmap=cat['object_to_id'];hw={a['id']:a for a in cat['hardware']};retiredh=set(delta['retired_hardware_ids'])
D['installed']=[a for a in D['installed'] if a['key'] not in removed|owned];D['detail']=[a for a in D['detail'] if a['meta'].get('source') not in removed|owned and a['meta'].get('hardware_id') not in retiredh]
def geom(n,m):D['geometry'][n]=m;return n
for n in sorted(owned):
 a=by.get(n);id=hwmap.get(n);h=hw.get(id,{});iswood=a is not None
 group='carrier' if n.startswith(('BB_MONITOR','BB_VESA')) else 'cassette' if n.startswith(('BB_DMD','BB_Speaker','BB_Panel')) else 'bbglass' if n.startswith(('BB_Glass','BB_Backglass','BB_GLASS')) else 'bbshell' if iswood else 'future' if 'ToyZone' in n else 'bbhardware'
 m=copy.deepcopy(oldi.get(n,oldi['BB_ReplaceableVESAPlate'])['meta']);m.update(id=a['manufacturing_part_id'] if a else id or n.replace('BB_',''),source=n,names=bi(a['description_en'] if a else h.get('description_en',n.replace('BB_','').replace('_',' ')),a['description_pt_BR'] if a else h.get('description_pt_BR',n.replace('BB_','').replace('_',' '))),group=group,scope='BACKBOX',kind='wood' if iswood else 'hardware' if id else 'reference',assembly='backbox_v34',stage='08',material=a['material_class'] if a else h.get('material','REFERENCE'),thickness=a['nominal_stock_thickness_mm'] if a else None,quantity=2 if n.startswith('BB_MONITOR_STOP_') else 1,hardware_id=id,families=[a['manufacturing_part_id']] if a else [],instances=[a['instance_id']] if a else [],manufacturing_status=[a['manufacturing_status']] if a else ['HARDWARE_PENDING'],status='WAITING_FOR_PHYSICAL_MEASUREMENT',classification='REQUIRED_FLATPACK_HARDWARE' if iswood else h.get('flatpack_classification','FUTURE_ELECTRONICS_HARDWARE'),model_status='V34 DESIGN CANDIDATE; fit/hardware/material held',geometry_authority={'file':'exports/generated/backbox-v34/play.FCStd','sha256':N['source_sha256'],'object':n,'status':'V34_DESIGN_CANDIDATE'})
 if n=='BB_MONITOR_PLATE':m['model_status']+=' · CAPTURED during shell assembly; no routine plate removal'
 if 'SpeakerEnvelope' in n:m['model_status']+=' · <=60 mm rear driver depth; hardware-dependent'
 off=[-100 if n.endswith('L') else 100 if n.endswith('R') else 0,-140,180 if n=='BB_Top' else 70 if n=='BB_MONITOR_PLATE' else 0]
 obj={'key':n,'geometry':geom('v34-'+n,N['states']['PLAY'][n]),'meta':m,'overview':off};D['installed'].append(obj)
 if iswood:
  dm=copy.deepcopy(m);dm.update(instance=a['instance_id'],face_A=a['face_A_outward_world'],finish_count=len(a.get('manual_finish',[])));dm['geometry_authority']={'file':a['finished_member_brep'],'sha256':sha(R/a['finished_member_brep']),'local_to_installed_matrix':a['local_to_installed_matrix'],'status':'V34_EXACT_MANUFACTURING_MEMBER'}
  D['detail'].append({'key':a['instance_id'],'geometry':geom('v34-part-'+a['instance_id'],N['manufacturing_world'][a['instance_id']]),'meta':dm,'offset':off})
 elif id:
  dm=copy.deepcopy(m);dm.update(instance=n,quantity=1);D['detail'].append({'key':'v34-hw-'+n,'geometry':obj['geometry'],'meta':dm,'offset':[off[0],-55 if 'VESA' in n else 0,55]})
 for state in D['states']:D['states'][state].pop(n,None)
for state,d in D['states'].items():
 for n in removed:d.pop(n,None)
 for n,m in N['states'][state].items():d[n]=geom('v34-'+state+'-'+n,m)
for gr in D['groups']:
 if gr['id']=='carrier':gr['names']=bi('Captured monitor plate','Placa capturada do monitor')
 if gr['id']=='cassette':gr['names']=bi('DMD / speaker panel','Painel DMD / alto-falantes')
D.update(geometry_revision='V34',manual=manual,hardware=cat['hardware'],source_head='0993d9768582290915f7166c53507ffd2aa434b6',source_mesh_sha256=N['source_sha256'],manufacturing_release=False)
# Replace backbox framework steps with explicit owner assembly order; all trajectories schematic unless labeled otherwise.
Q['clips']=[a for a in Q['clips'] if a['type']!='assembly']
for stage in manual['stages']:
 for st in stage['steps']:
  Q['clips'].append({'id':'assembly-'+st['id'],'type':'assembly','title':{k:st['id']+' · '+v for k,v in st['title'].items()},'stage':stage['id'],'step':st['id'],'first_stage_step':True,'duration_s':8,'status':'SCHEMATIC_ASSEMBLY_ANIMATION','piece_ids':st['component_ids'],'hardware_ids':st['hardware_ids'],'action':st['action'],'check':st['check'],'note':{k:('SCHEMATIC ASSEMBLY ANIMATION. ' if k=='en' else 'ANIMAÇÃO ESQUEMÁTICA DE MONTAGEM. ')+v+' '+st['hold'][k] for k,v in st['action'].items()}})
Q['clips']=sorted([a for a in Q['clips'] if a['type']=='assembly'],key=lambda a:tuple(int(x) for x in a['step'].split('.')))+[a for a in Q['clips'] if a['type']!='assembly']
for a in Q['clips']:
 if a['id']=='service-glass':a.update(title=bi('Backglass FRONT removal','Remoção FRONTAL do vidro'),note=bi('Remove upper strip screws/strip; lift1mm, tilt top forward10°, lift6mm further, withdraw. Shell top and monitor plate remain fixed. Purchased fit qualification HOLD.','Retire parafusos/tira superior; levante1mm, incline10°, eleve mais6mm e retire pela frente. Topo e placa VESA fixos. Ensaio físico PENDENTE.'))
 if a['id']=='service-display':a.update(title=bi('Monitor FRONT removal — plate fixed','Monitor pela FRENTE — placa fixa'),note=bi('Remove glass/strip; support monitor; remove4 rear VESA bolts. Raise to+5mm insertion height then withdraw FRONT. Never remove shell top or captured plate.','Retire vidro/tira; sustente monitor; retire4 parafusos VESA por trás. Eleve5mm e retire pela FRENTE. Topo e placa capturada ficam.'))
 if a['id']=='service-cassette':a.update(title=bi('Single DMD / speaker panel removal','Remoção do painel único DMD / alto-falantes'),note=bi('Release4 SIDE-operated panel screws; keep cross-dowels captive; remove complete panel FRONT. No routine fold removal. Hardware dimensions pending.','Solte4 parafusos LATERAIS; porcas cativas ficam; retire painel completo pela FRENTE. Não remover para dobra normal. Ferragens pendentes.'))
for n in removed:Q['motions']['groups'].pop(n,None)
for n in owned:Q['motions']['groups'][n]='retainer' if n.startswith(('BB_GLASS_TOP','BB_GlassTopScrew','BB_GlassTopCushion')) else 'glass' if n=='BB_Backglass' else 'display' if n=='BB_Display32' else 'cassette' if n.startswith(('BB_DMD','BB_Speaker','BB_PanelCross')) else 'fixed'
Q['motions']['fold_names']=[n for n in Q['motions']['fold_names'] if n not in removed]+[n for n in owned if n not in Q['motions']['fold_names']]
oldpieces=Q['pieces'];Q['pieces']={}
for a in reg['parts']:
 ii=a['instance_id'];info=copy.deepcopy(oldpieces.get(ii,{}));xy=a['finished_xy_bounds_mm'];info.update(id=a['manufacturing_part_id'],instance_id=ii,local_to_installed_matrix=a['local_to_installed_matrix'],finished_xy_bounds_mm=xy,finished_xy_size_mm=[xy[2]-xy[0],xy[3]-xy[1]],nominal_stock_thickness_mm=a['nominal_stock_thickness_mm']);
 if ii in delta['changed_rows']:info.pop('packing_mesh',None)
 Q['pieces'][ii]=info
# Honest simple packing projection, one piece per separated layer; not optimized/shipping-certified.
bundles=[]
for a in sorted(reg['parts'],key=lambda a:a['volume_mm3'],reverse=True):
 kg=a['volume_mm3']*650/1e9;b=next((b for b in bundles if b['wood_mass_kg']+kg<=17.2),None)
 if b is None:b={'id':'V34-P'+str(len(bundles)+1),'wood_mass_kg':0,'L':0,'W':0,'layers':[],'z':10};bundles.append(b)
 xy=a['finished_xy_bounds_mm'];w,h=xy[2]-xy[0],xy[3]-xy[1];rot=h>w;l,ww=(h,w) if rot else (w,h);t=a.get('finished_reference_thickness_mm') or 54
 b['L']=max(b['L'],l);b['W']=max(b['W'],ww);b['layers'].append({'t':t,'z':b['z'],'order':len(b['layers'])+1,'pieces':[{'instance_id':a['instance_id'],'id':a['manufacturing_part_id'],'x':0,'y':0,'rotated':rot,'mass_kg':kg}]});b['z']+=t+2;b['wood_mass_kg']+=kg
for b in bundles:b.update(external_LWH_mm=[b['L']+40,b['W']+40,b['z']+10],gross_nominal_kg=b['wood_mass_kg']+2,gross_high_kg=b['wood_mass_kg']*850/650+2)
Q['packaging']={'preferred_target_kg':25,'status':'V34 PRELIMINARY ONE-PART-PER-LAYER; packaging2kg allowance; no shipping qualification','candidates':[{'target_kg':25,'bundles':bundles}],'hardware_box':'SEPARATE','glass_electronics_in_wood_bundles':False};(O/'packaging.json').write_text(json.dumps(Q['packaging'],indent=2)+'\n')
active=[a for a in cat['hardware'] if a.get('active',True) and a.get('design_status')!='RETIRED'];f=[a for a in active if a['id'].startswith('F') and a['flatpack_classification']=='REQUIRED_FLATPACK_HARDWARE'];known=sum(a['quantity'] for a in f if isinstance(a['quantity'],(int,float)))
Q['hardware'].update(required_Fxx_models=len(f),known_required_Fxx_quantity=known,formula_driven_Fxx=[a['id'] for a in f if a['quantity'] is None and 'FORMULA' in a['quantity_status']],TBD_Fxx=[a['id'] for a in f if a['quantity'] is None and 'FORMULA' not in a['quantity_status']])
Q['metrics'].update(manufacturing_pieces=reg['manufacturing_pieces'],CNC_pieces=reg['CNC_plywood_pieces'],shop_solid_pieces=6,canonical_families=reg['canonical_families'],wood_mass_kg=mass['finished_wood_kg'],wood_finished_reference_mass_kg=mass['finished_wood_kg'],wood_shipping_mass_kg=None,wood_mass_basis='ACTUAL_FINISHED_BREPS; shipping allowance not a measured wood mass',known_fastener_minimum=known,hardware_models=len(active),preliminary_sheets='V34 HOLD')
# Do not retain stale mechanical/full-build mass totals after reference payload changes.
base=base.replace("${Q.mass.mechanical_scenario_kg[1].toFixed(1)} / ${Q.mass.full_planning_build_kg[1].toFixed(1)} kg", "HOLD — V34 purchased hardware / monitor / DMD / speakers")
# Keep payloads visible in their explicit assembly steps without making them mandatory electronics.
base=base.replace("let visible=","let visible=",1)
base=base.replace("m.visible=visible;if(!visible)continue;","if(clip.stage==='08'&&clip.piece_ids?.some(id=>id===m.name||id===meta.source))visible=true;m.visible=visible;if(!visible)continue;")
base=base.replace("done.includes(m.name)","(done.includes(m.name)||done.includes(meta.source)||Q.clips.filter(c=>c.type==='assembly'&&c.stage==='08'&&Number(c.step.split('.')[1])<=Number(clip.step.split('.')[1])).some(c=>c.hardware_ids?.includes(meta.hardware_id)))")
D['quantity_overlay']={'status':'V34 authoritative hardware catalogue','minimum_known_required_Fxx':known}
base=base.replace('V33.8','V34').replace('DMD / speaker cassette','DMD / speaker panel').replace('Cassete DMD / alto-falantes','Painel DMD / alto-falantes')
# Captured plate must never animate as a removable monitor adapter.
base=base.replace("if(mode==='GLASS'&&n==='BB_Backglass')move(m,[0,0,500*p]);", "if(mode==='GLASS'&&n==='BB_Backglass'){const a=10*clamp(p*4-1)*Math.PI/180;spin(m,[1,0,0],a,[300,1116,841]);m.position.z+=clamp(p*4)+6*clamp(p*4-2);m.position.y-=200*clamp(p*4-3);}")
base=base.replace("if(mode==='DISPLAY'&&['display','adapter'].includes(g)&&!n.includes('Reserve'))move(m,[0,-400*p,0]);", "if(mode==='DISPLAY'&&n==='BB_Display32')move(m,[0,-400*clamp(p*2-1),5*clamp(p*2)]);")
base=base.replace("if(mode==='CASSETTE')for(const m of V.installed)if(m.name.includes('CassetteFastener')||m.name.includes('CassetteBolt'))m.visible=false;", "if(mode==='CASSETTE')for(const m of V.installed)if(m.name.startsWith('BB_PanelBolt'))m.visible=false;")
base=base.replace("if(mode==='GLASS')for(const m of V.installed)","if(mode==='DISPLAY')for(const m of V.installed)if(m.name.startsWith('BB_VESA'))m.visible=false;if(mode==='GLASS')for(const m of V.installed)")
# Animation assembly stage08 is per-step, not all shell/display pieces appearing together.
base=base.replace("const meta=m.userData.meta,same=meta.stage===clip.stage||clip.piece_ids?.includes(m.name);", "const meta=m.userData.meta,same=(clip.stage==='08'?clip.piece_ids?.some(id=>id===m.name||id===meta.source):meta.stage===clip.stage||clip.piece_ids?.includes(m.name));")
base=base.replace("m.visible=visible;if(!visible)continue;", "if(clip.stage==='08'&&meta.stage==='08'){const done=Q.clips.filter(c=>c.type==='assembly'&&c.stage==='08'&&Number(c.step.split('.')[1])<=Number(clip.step.split('.')[1])).flatMap(c=>c.piece_ids);visible=(done.includes(m.name)||done.includes(meta.source)||Q.clips.filter(c=>c.type==='assembly'&&c.stage==='08'&&Number(c.step.split('.')[1])<=Number(clip.step.split('.')[1])).some(c=>c.hardware_ids?.includes(meta.hardware_id)));}m.visible=visible;if(!visible)continue;")
base=base.replace('../service-productization-v338/README.md','../backbox-v34/README.md').replace('../service-productization-v338/manufacturing-bom','../backbox-v34/manufacturing-bom').replace('../assembly-v333/README.md','../backbox-v34/README.md')
used={a['geometry'] for a in D['installed']+D['detail']}
for st in D['states'].values():used.update(v for v in st.values() if v)
D['geometry']={k:m for k,m in D['geometry'].items() if k in used}
base=re.sub(r'(<script id="viewer-data"[^>]*>).*?(</script>)',lambda m:m[1]+base64.b64encode(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0)).decode()+m[2],base,flags=re.S)
base=re.sub(r'(<script id="v333-data"[^>]*>).*?(</script>)',lambda m:m[1]+json.dumps(Q,separators=(',',':'),ensure_ascii=False).replace('</','<\\/')+m[2],base,flags=re.S)
(R/'exports/generated/viewer-v32/index.html').write_text(base);(O/'viewer-data.json.gz').write_bytes(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0));(O/'animations.json').write_text(json.dumps(Q['clips'],indent=2,ensure_ascii=False)+'\n');(O/'project-metrics.json').write_text(json.dumps(Q['metrics'],indent=2)+'\n');(O/'hardware-dashboard.json').write_text(json.dumps(Q['hardware'],indent=2)+'\n')
(O/'viewer-authority.json').write_text(json.dumps({'revision':'V34','native_sha256':N['source_sha256'],'html_sha256':sha(R/'exports/generated/viewer-v32/index.html'),'installed_count':len(D['installed']),'manufacturing_count':len(Q['pieces']),'retired_absent':not any(a['key'] in removed for a in D['installed']),'manufacturing_release':False},indent=2)+'\n');print('V34_VIEWER',len(Q['pieces']),len(Q['clips']),len(bundles))
