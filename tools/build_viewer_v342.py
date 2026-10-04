"""V34 offline viewer delta; same controls/palettes, actual flat pieces. CERN-OHL-S-2.0."""
from pathlib import Path
import json,gzip,base64,re,subprocess,copy,math,hashlib
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/backbox-v342'
def read(f):return json.loads(Path(f).read_text())
def bi(a,b):return {'en':a,'pt-BR':b}
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
base=subprocess.check_output(['git','show','8d951bc37a38d5e3820cbde93700f1161ff32fb1:exports/generated/viewer-v32/index.html'],cwd=R,text=True)
D=json.loads(gzip.decompress(base64.b64decode(re.search(r'<script id="viewer-data"[^>]*>(.*?)</script>',base,re.S)[1])));Q=json.loads(re.search(r'<script id="v333-data"[^>]*>(.*?)</script>',base,re.S)[1])
N=json.loads(gzip.decompress((O/'viewer-native.json.gz').read_bytes()));reg=read(O/'manufacturing-register.json');delta=read(O/'manufacturing-delta.json');manual=read(O/'assembly-manual.json');cat=read(R/'config/hardware_catalog_v342.json');mass=read(O/'mass-counts.json');inv=read(O/'geometry-inventory.json')['parts'];removed=set(N['removed']);owned=set(N['changed'])|set(N['added']);by={a['source_component']:a for a in reg['parts']};oldi={a['key']:a for a in D['installed']};hwmap=cat['object_to_id'];hw={a['id']:a for a in cat['hardware']};retiredh=set(delta['retired_hardware_ids'])
D['installed']=[a for a in D['installed'] if a['key'] not in removed|owned];D['detail']=[a for a in D['detail'] if a['meta'].get('source') not in removed|owned and a['meta'].get('hardware_id') not in retiredh]
def geom(n,m):D['geometry'][n]=m;return n
for n in sorted(owned):
 a=by.get(n);id=hwmap.get(n);h=hw.get(id,{});iswood=a is not None
 group=oldi[n]['meta']['group'] if n in oldi else 'bbglass' if n.startswith('BB_Acrylic') else 'bbdoors' if n.startswith('BB_Door') else 'bbfans' if n.startswith('BB_Lower') else 'carrier' if n.startswith(('BB_MONITOR','BB_VESA')) else 'cassette' if n.startswith(('BB_DMD','BB_Speaker','BB_Panel')) else 'bbglass' if n.startswith(('BB_Acrylic','BB_GLASS')) else 'bbshell' if iswood else 'future' if 'ToyZone' in n else 'bbhardware'
 m=copy.deepcopy(oldi.get(n,oldi['BB_MONITOR_PLATE'])['meta']);m.update(id=a['manufacturing_part_id'] if a else id or n.replace('BB_',''),source=n,names=bi(a['description_en'] if a else h.get('description_en',n.replace('BB_','').replace('_',' ')),a['description_pt_BR'] if a else h.get('description_pt_BR',n.replace('BB_','').replace('_',' '))),group=group,scope='BACKBOX' if n.startswith('BB_') else 'MAIN CABINET',kind='wood' if iswood else 'hardware' if id else 'reference',assembly='backbox_v34',stage='08',material=a['material_class'] if a else h.get('material','REFERENCE'),thickness=a['nominal_stock_thickness_mm'] if a else None,quantity=2 if n.startswith('BB_MONITOR_STOP_') else 1,hardware_id=id,families=[a['manufacturing_part_id']] if a else [],instances=[a['instance_id']] if a else [],manufacturing_status=[a['manufacturing_status']] if a else ['HARDWARE_PENDING'],status='WAITING_FOR_PHYSICAL_MEASUREMENT',classification='REQUIRED_FLATPACK_HARDWARE' if iswood else h.get('flatpack_classification','FUTURE_ELECTRONICS_HARDWARE'),model_status='V34 DESIGN CANDIDATE; fit/hardware/material held',geometry_authority={'file':'exports/generated/backbox-v342/play.FCStd','sha256':N['source_sha256'],'object':n,'status':'V34_DESIGN_CANDIDATE'})
 if n=='BB_MONITOR_PLATE':m['model_status']+=' · CAPTURED during shell assembly; no routine plate removal'
 if 'SpeakerEnvelope' in n:m['model_status']+=' · <=90 mm rear driver depth; hardware-dependent'
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
D.update(geometry_revision='V34.2',manual=manual,hardware=cat['hardware'],source_head='8d951bc37a38d5e3820cbde93700f1161ff32fb1',source_mesh_sha256=N['source_sha256'],manufacturing_release=False)
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
Q['motions']['fold_names']=[n for n in Q['motions']['fold_names'] if n not in removed]+[n for n in owned if n.startswith('BB_') and n not in Q['motions']['fold_names']]
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
Q['metrics'].update(manufacturing_pieces=reg['manufacturing_pieces'],CNC_pieces=reg['CNC_plywood_pieces'],shop_solid_pieces=6,canonical_families=reg['canonical_families'],wood_mass_kg=mass['wood_kg'],wood_finished_reference_mass_kg=mass['wood_kg'],wood_shipping_mass_kg=None,wood_mass_basis='ACTUAL_FINISHED_BREPS; shipping allowance not a measured wood mass',known_fastener_minimum=known,hardware_models=len(active),preliminary_sheets='V34 HOLD')
# Do not retain stale mechanical/full-build mass totals after reference payload changes.
base=base.replace("${Q.mass.mechanical_scenario_kg[1].toFixed(1)} / ${Q.mass.full_planning_build_kg[1].toFixed(1)} kg", "HOLD — V34 purchased hardware / monitor / DMD / speakers")
D['quantity_overlay']={'status':'V34 authoritative hardware catalogue','minimum_known_required_Fxx':known}
base=base.replace('V33.8','V34').replace('DMD / speaker cassette','DMD / speaker panel').replace('Cassete DMD / alto-falantes','Painel DMD / alto-falantes')
base=base.replace('../service-productization-v338/README.md','../backbox-v342/README.md').replace('../service-productization-v338/manufacturing-bom','../backbox-v342/manufacturing-bom').replace('../assembly-v333/README.md','../backbox-v342/README.md')
# Current native metadata and optional mode.
for a in D['installed']:
 n=a['key']
 if n.startswith('BB_Acrylic'):a['meta']['group']='bbglass'
 if n=='PF_LockdownGlassRetainer':a['meta'].update(group='hardware',scope='MAIN CABINET',names=bi('Lockdown glass containment reference','Referência de contenção pelo lockdown'),status='HARDWARE_PENDING')
 if n.startswith('BB_Lower'):a['meta']['group']='bbfans'
 if n=='BB_AcrylicMask':a['meta']['names']=bi('Rear painted black mask — provisional window','Máscara preta traseira — janela provisória')
for n,m in N['variants'].items():
 if 'LowerIntakeFan' not in n:continue
 meta=copy.deepcopy(oldi['BB_FanL']['meta']);meta.update(id='H28',source=n,hardware_id='H28',group='bbfans',names=bi('Optional lower intake fan','Ventoinha inferior opcional'),optional_study=True,status='HARDWARE_PENDING',kind='hardware',classification='OPTIONAL_FLATPACK_HARDWARE')
 D['installed'].append({'key':n,'geometry':geom('v342-'+n,m),'meta':meta,'overview':[0,100,0]})
 D['detail'].append({'key':'v342-hw-'+n,'geometry':'v342-'+n,'meta':copy.deepcopy(meta),'offset':[0,100,0]})
 D['states']['PLAY'][n]=None
for a in D['installed']:
 n=a['key']
 if n.startswith(('BB_Door','BB_Lower','BB_Fan')) and n.endswith(('L','R')):Q['motions']['groups'][n]='door'+n[-1]
 if n in ['BB_AcrylicFront','BB_AcrylicMask']:Q['motions']['groups'][n]='glass'
 if n.startswith('BB_AcrylicRetainerScrew'):Q['motions']['groups'][n]='retainer'
Q['motions'].pop('fan_flex',None)
for clip in Q['clips']:
 if clip['id']=='service-glass':clip.update(title=bi('Acrylic FRONT removal','Remoção FRONTAL do acrílico'),note=bi('Remove upper strip. Lift1mm, tilt10°, lift6mm and withdraw FRONT. Acrylic mask follows sheet. Plate/top remain fixed. Physical fit HOLD.','Retire tira. Eleve1mm, incline10°, eleve6mm e retire pela FRENTE. Máscara acompanha chapa. Placa/topo fixos. Ensaio físico PENDENTE.'))
 if clip['id']=='service-doors':clip['note']=bi('Open active then passive leaf; modeled0–100degree sweep. Builder must qualify actual flexible fan wiring; no universal anchor/loop modeled.','Abra folha ativa e depois passiva; giro modelado0–100graus. Usuário qualifica fios flexíveis reais; sem ancoragem universal.')
 if clip['id']=='service-display':clip['note']=bi('Remove acrylic/strip; support TV; remove4 rear VESA bolts; raise15mm then withdraw FRONT. Plate/top stay fixed. Actual TCL bosses/ports unmeasured.','Retire acrílico/tira; sustente TV; retire4 parafusos VESA traseiros; eleve15mm e retire pela FRENTE. Placa/topo ficam. Bosses/portas TCL não medidos.')
base=base.replace("n==='BB_Backglass'","['BB_AcrylicFront','BB_AcrylicMask'].includes(n)").replace("5*clamp(p*2)]","15*clamp(p*2)]")
base=base.replace("if(mode==='DOORS'){flexLoop('R',100*clamp(p*2));flexLoop('L',100*clamp(p*2-1));}","/* Builder-specific flexible wiring, no universal cable-loop geometry. */")
base=base.replace("'BB_Backglass'","'BB_AcrylicFront'").replace('Backbox front glass','Backbox acrylic front').replace('Vidro frontal do backbox','Acrílico frontal do backbox')
base=base.replace('../backbox-v34/','../backbox-v342/').replace('V34 purchased hardware','V34.2 purchased hardware')
base=base.replace("if(mode==='DISPLAY')for(const m of V.installed)","if(mode==='DISPLAY')for(const m of V.installed)")
# Extra simple offline comparison panel; source meshes are original native B-reps.
D['v342_study']={'variants':{n:geom('v342-study-'+n,m) for n,m in N['variants'].items()},'hold':bi('TCL outer specification verified; bosses, active image and connectors are sensitivity assumptions. No CNC release.','Dimensões externas TCL verificadas; bosses, imagem e conectores são hipóteses. CNC bloqueado.')}
base=base.replace('function colorFor(m,v){',"function colorFor(m,v){if(m.source==='BB_AcrylicMask')return 0x101214;").replace('Assembly atlas V34','Assembly atlas V34.2')
base=base.replace('</body>',(R/'tools/viewer_v342_study.html').read_text()+'\n</body>')
used={a['geometry'] for a in D['installed']+D['detail']}
for st in D['states'].values():used.update(v for v in st.values() if v)
used.update(D['v342_study']['variants'].values());D['geometry']={k:m for k,m in D['geometry'].items() if k in used}
base=re.sub(r'(<script id="viewer-data"[^>]*>).*?(</script>)',lambda m:m[1]+base64.b64encode(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0)).decode()+m[2],base,flags=re.S)
base=re.sub(r'(<script id="v333-data"[^>]*>).*?(</script>)',lambda m:m[1]+json.dumps(Q,separators=(',',':'),ensure_ascii=False).replace('</','<\\/')+m[2],base,flags=re.S)
(R/'exports/generated/viewer-v32/index.html').write_text(base);(O/'viewer-data.json.gz').write_bytes(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0));(O/'animations.json').write_text(json.dumps(Q['clips'],indent=2,ensure_ascii=False)+'\n');(O/'project-metrics.json').write_text(json.dumps(Q['metrics'],indent=2)+'\n');(O/'hardware-dashboard.json').write_text(json.dumps(Q['hardware'],indent=2)+'\n')
(O/'viewer-authority.json').write_text(json.dumps({'revision':'V34.2','native_sha256':N['source_sha256'],'html_sha256':sha(R/'exports/generated/viewer-v32/index.html'),'installed_count':len(D['installed']),'manufacturing_count':len(Q['pieces']),'retired_absent':not any(a['key'] in removed for a in D['installed']),'manufacturing_release':False},indent=2)+'\n');print('V34_VIEWER',len(Q['pieces']),len(Q['clips']),len(bundles))
