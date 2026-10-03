"""V34 manufacturing/hardware delta with exact retained source authority. CERN-OHL-S-2.0."""
from pathlib import Path
import json,sys,copy,collections,csv,hashlib,gzip,math
import FreeCAD as A,Part,MeshPart
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,V
O=R/'exports/generated/backbox-v34';B=R/'exports/generated/service-productization-v338';g=json.loads((O/'geometry-validation.json').read_text());assert g['pass'];p=load(O/'candidate.FCStd');old=load(B/'play.FCStd')
def read(f):return json.loads(Path(f).read_text())
def dump(f,j):Path(f).write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
def mesh(s):
 m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.5,AngularDeflection=.6,Relative=False);v,f=m.Topology;return {'vertices':[list(x) for x in v],'faces':f}
def mat(origin,u,v,w):
 a=A.Matrix()
 for i in range(3):
  for j,col in enumerate([u,v,w]):setattr(a,f'A{i+1}{j+1}',col[i])
 a.A14,a.A24,a.A34=origin;return a
reg=read(B/'manufacturing-register.json');removed=set(g['retired']);changed=set(g['changed']);oldrows=reg['parts'];retiredrows=[a for a in oldrows if a['source_component'] in removed];parts=[copy.deepcopy(a) for a in oldrows if a['source_component'] not in removed and a['source_component'] not in changed]
rebuild=[]
for n in ['BB_SideL','BB_SideR','BB_Top']:
 a=copy.deepcopy(next(a for a in oldrows if a['source_component']==n));matrix=A.Matrix(*a['local_to_installed_matrix']);rebuild.append((n,a['manufacturing_part_id'],a['instance_id'],a['nominal_stock_thickness_mm'],matrix,a))
new=[('BB_MONITOR_PLATE','M074',18,mat([-76,1258,854],[1,0,0],[0,0,1],[0,-1,0])),('BB_MONITOR_STOP_L','M075',12,mat([-60,1240,854],[0,1,0],[0,0,-1],[-1,0,0])),('BB_MONITOR_STOP_R','M075',12,mat([660,1240,824],[0,1,0],[0,0,1],[1,0,0])),('BB_DMD_SPEAKER_PANEL','M076',18,mat([-76,1197,616],[1,0,0],[0,0,1],[0,-1,0])),('BB_GLASS_TOP_RETAINER','M077',12,mat([-72,1101,1290.8],[1,0,0],[0,1,0],[0,0,1])),('BB_GLASS_BOTTOM_SEAT','M037',18,mat([-72,1108,846],[1,0,0],[0,-1,0],[0,0,-1]))]
for i,(n,f,t,m) in enumerate(new):rebuild.append((n,f,'V34-'+n,t,m,{}))
newmesh={};changedrows=[]
for n,f,i,t,m,a in rebuild:
 s=p[n];q=s.copy();q.transformShape(m.inverse(),True);b=q.BoundBox
 file=O/(i+'-finished.brep');q.exportBrep(str(file));reb=q.copy();reb.transformShape(m,True);error=s.cut(reb).Volume+reb.cut(s).Volume;assert error<1e-4,(n,error)
 profile=[]
 for face in q.Faces:
  if abs(face.normalAt(0,0).z)>.999:profile.append(face)
 outer_area=max((Part.Face(face.OuterWire).Area for face in profile),default=b.XLength*b.YLength)
 a.update(manufacturing_part_id=f,instance_id=i,source_component=n,assembly_id='BB_V34',quantity=1,description_en=n.replace('BB_','').replace('_',' ').title(),description_pt_BR={'BB_MONITOR_PLATE':'Placa VESA estrutural capturada','BB_MONITOR_STOP_L':'Batente esquerdo do monitor','BB_MONITOR_STOP_R':'Batente direito do monitor','BB_DMD_SPEAKER_PANEL':'Painel único DMD e alto-falantes','BB_GLASS_TOP_RETAINER':'Retentor superior removível do vidro','BB_GLASS_BOTTOM_SEAT':'Assento inferior do vidro'}.get(n,n),material_class='STRUCTURAL_PREMIUM',manufacturing_class='CNC_PLYWOOD',nominal_stock_thickness_mm=t,finished_reference_thickness_mm=t,finished_xy_bounds_mm=[b.XMin,b.YMin,b.XMax,b.YMax],local_to_installed_matrix=list(m.A),face_A_outward_world=[-m.A13,-m.A23,-m.A33],machining_face='FACE_A',opposite_face='FACE_B_NO_CNC',opposite_face_cnc=False,finished_member_brep=str(file.relative_to(R)),cnc_stage_brep=None,outer_contour_brep=None,cnc_outer_access_brep=None,version='V34',volume_mm3=s.Volume,projected_area_mm2=outer_area,geometry_authority='exports/generated/backbox-v34/candidate.FCStd#'+n,manufacturing_release=False,fit_dependent=True,coupon_dependent=True,fit_expression='actual stock + coupon clearance; reference hardware cuts not released',manufacturing_status='ONE_SIDE_CNC_PLUS_MANUAL_FINISH',manual_finish=[{'operation':'SELECTED_HARDWARE_DRILLING','face_datum':'FACE_A','instruction':'Reference only. Purchased screw, insert/cross-dowel, glass liner and jig dimensions required. Use clamped guide and depth stop for edge bores. No CNC flip.','depth_mm':None}],operations={'CUT':'exact contour; only selected monitor/speaker apertures after hardware confirmation','POCKET':'side inside rebates/guides or glass-seat top groove, as applicable','LOCATOR':'hardware-dependent; no guessed production pilot','ENGRAVE':'optional hidden FACE_A ID','REFERENCE':'nominal fit geometry; NOT FOR CNC'},corner_classes=['A_R2_OR_LARGER','D_COUPON_FIT_HOLD'],reconstruction_difference_mm3=error)
 # Remove stale machining feature lists from superseded faces rather than inheriting them.
 for k in ['through_cuts','pockets','feature_register','joinery','review_outline','cnc_vs_finished_difference_before_manual_mm3','blank_outside_error_mm3']:
  if k in a:a.pop(k)
 a['one_face_plan']=('Inside side face: profile + open-front rebates + top-open R2 dado; opposite face only manual fastener finishing.' if n.startswith('BB_Side') else 'Glass bottom seat FACE_A top: profile and8mm-deep open-end groove,10mm web.' if n=='BB_GLASS_BOTTOM_SEAT' else 'Contour/through cuts from FACE_A; edge or selected hardware bores manually guided from the documented FACE_A datum. No second CNC face.')
 parts.append(a);changedrows.append(a);newmesh[i]=mesh(q)
families=[]
for f in sorted({a['manufacturing_part_id'] for a in parts}):
 aa=[a for a in parts if a['manufacturing_part_id']==f];families.append({'id':f,'stock':aa[0]['nominal_stock_thickness_mm'],'class':aa[0]['material_class'],'instances':[a['instance_id'] for a in aa],'quantity':len(aa)})
cnc=[a for a in parts if a.get('manufacturing_class')!='SHOP_MADE_SOLID_WOOD_PART'];assert set(a['nominal_stock_thickness_mm'] for a in cnc)=={12,18}
counts={'manufacturing_pieces':len(parts),'CNC_plywood_pieces':len(cnc),'shop_solid_wood_parts':len(parts)-len(cnc),'canonical_families':len(families),'CNC_families':len({a['manufacturing_part_id'] for a in cnc}),'installed_components':len({a['source_component'] for a in parts})}
reg.update(version='V34',supersedes='V33.8',parts=parts,families=families,**counts,manufacturing_release=False,retired_rows=[{'id':a['manufacturing_part_id'],'instance':a['instance_id'],'source':a['source_component']} for a in retiredrows]);dump(O/'manufacturing-register.json',reg)
with (O/'manufacturing-bom.csv').open('w') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['ID','instance','source','quantity','stock_mm','material','FACE_A','status','volume_mm3'])
 for a in parts:w.writerow([a['manufacturing_part_id'],a['instance_id'],a['source_component'],1,a['nominal_stock_thickness_mm'],a['material_class'],a['face_A_outward_world'],a['manufacturing_status'],a['volume_mm3']])
vol=sum(a['volume_mm3'] for a in parts);oldvol=sum(a['volume_mm3'] for a in oldrows);mass={'basis':'actual finished manufacturing B-rep volumes; not bounding boxes','density_kg_m3':650,'finished_wood_kg':vol*650/1e9,'previous_finished_wood_kg':oldvol*650/1e9,'finished_reduction_kg':(oldvol-vol)*650/1e9,'LOW_550_kg':vol*550/1e9,'HIGH_750_kg':vol*750/1e9,'hardware_mass':'UNKNOWN purchased hardware; not zero','counts':counts,'stock_area_m2':{str(t):sum(a['projected_area_mm2'] for a in cnc if a['nominal_stock_thickness_mm']==t)/1e6 for t in [12,18]},'retired_manufacturing_pieces':len(retiredrows),'new_manufacturing_pieces':len(new),'full_sheet_release':False};dump(O/'mass-counts.json',mass)
# All small retained plywood receives explicit role/parent/load metadata.
audit=[]
for n in sorted({a['source_component'] for a in oldrows if a['source_component'].startswith('BB_')}|{n for n,_,_,_ in new}):
 retired=n in removed and n not in p
 if retired:role='Superseded monitor/cassette/glass assembly; zero current function';parent=None;attach='RETIRED';load='none'
 elif n in ['BB_MONITOR_STOP_L','BB_MONITOR_STOP_R']:role='Fixed lower plate bearing';parent='BB_SideL/R';attach='SCREWED';load='monitor/plate vertical reaction; geometric bearing plus screw shear'
 elif n=='BB_MONITOR_PLATE':role='Monitor VESA interface';parent='BB_SideL/R + stops + BB_Top';attach='CAPTURED';load='monitor gravity/fold/nudge via bolts'
 elif n=='BB_DMD_SPEAKER_PANEL':role='Single front display/speaker mounting surface';parent='BB_SideL/R';attach='BOLTED / REMOVABLE';load='DMD/speakers; fold retention'
 elif 'ParkingPad' in n:role='Upright-lock captive parking socket, unrelated to monitor';parent='BB_Floor';attach='SCREWED';load='parked knob only, not upright clamp'
 elif 'HingeCleat' in n:role='Continuous rear-door hinge backing; preserves accepted hinge axis';parent='BB_RearFrame';attach='SCREWED';load='door/fan mass; cannot be replaced by monitor plate'
 elif 'IntakeDownBaffle' in n:role='Downward dust path and protected intake throat';parent='BB_DoorL/R';attach='SCREWED / REMOVABLE';load='own weight, not monitor support'
 elif n=='BB_GLASS_TOP_RETAINER':role='Positive front upper glass capture';parent='BB_Top';attach='SCREWED / REMOVABLE';load='glass retention in all orientations'
 elif n=='BB_GLASS_BOTTOM_SEAT':role='Padded glass seat and6mm front lip';parent='BB_SideL/R';attach='SCREWED';load='glass gravity/front retention; lower seat fasteners hardware-held'
 elif n=='BB_Top':role='Shell top and plate upper stop';parent='BB_SideL/R';attach='GLUED+MECHANICALLY_FASTENED';load='shell, captured plate upward reaction'
 elif n=='BB_CenterAstragal':role='Door centre overlap and gasket landing';parent='BB_DoorL passive leaf';attach='SCREWED';load='centre seal, active-leaf lock reaction'
 elif n in ['BB_DoorL','BB_DoorR']:role='Rear service leaf';parent='BB_HingeCleat'+n[-1]+' via continuous hinge';attach='SCREWED';load='own weight and optional fan/filter; not structural shear'
 elif 'FanBlank' in n:role='Optional unpopulated fan-station closure';parent='BB_Door'+n[-1];attach='BOLTED / REMOVABLE';load='own weight, dust closure; not monitor support'
 elif 'IntakeFilterFrame' in n:role='Serviceable insect/dust media retention';parent='BB_Door'+n[-1];attach='SCREWED / REMOVABLE';load='own weight/filter; preserves protected intake opening'
 elif n=='BB_Floor':role='Backbox lower structural bearing';parent='BB_SideL/R and main RearBearingShelf';attach='CAPTURED / SCREWED';load='backbox gravity and WPC hinge transfer; broad shelf bearing'
 elif n=='BB_RearFrame':role='Rear aperture structural continuity with doors open';parent='BB_SideL/R + BB_Top + BB_Floor';attach='SCREWED';load='shell racking and rear-door hinge/lock reactions'
 elif n in ['BB_SideL','BB_SideR']:role='Primary backbox side structure';parent='BB_Floor + BB_Top + BB_RearFrame';attach='CAPTURED / SCREWED';load='monitor guides/stops, shell, WPC floor load path'
 else:raise AssertionError('Unclassified retained backbox member '+n)
 audit.append({'name':n,'status':'RETIRED' if retired else 'RETAINED','purpose':role,'parent':parent,'attachment':attach,'load':load,'why_needed':'none; retired' if retired else role})
dump(O/'attachment-audit.json',audit)
# Canonical hardware retirement exposes unknowns and preserves unrelated families.
cat=read(R/'config/hardware_catalog_v338.json');retireids=['F24','F25','F26','F27','F28','F31','F57','W09','I09','I10','I11','W10']
for h in cat['hardware']:
 if h['id'] in retireids:h.update(active=False,quantity=0,quantity_status='RETIRED_V34',design_status='RETIRED',notes='V34 retires obsolete monitor/cassette interface; historical dimensions in V33.8 catalogue.',instances=[])
 elif h['id']=='F16':h['notes']='Remaining shell/rear-frame/hinge backing joint schedule. Excludes retired rails/cleats and new separately counted top/stop hardware.'
 elif h['id']=='F30':h.update(description_en='Lower panel side-operated machine screw',description_pt_BR='Parafuso lateral do painel DMD/alto-falantes',quantity=4,instances=[],nominal_dimensions={'thread_family':'M4 reference','length_mm':None},notes='4 into panel cross-dowels; purchased thread/edge/washer/retention qualification HOLD')
 elif h['id']=='I12':h.update(description_en='Lower panel captive cross-dowel',description_pt_BR='Porca cilíndrica cativa do painel inferior',quantity=4,instances=[],notes='Metal cross-dowel in18mm panel; exact diameter/edge drill and tool access require physical hardware')
 elif h['id']=='F29':h.update(quantity=4,quantity_status='ONE_SELECTED_VESA_PATTERN_FOUR_POINTS',notes='4 monitor screws only. Stack =18mm plate + washer +0..12 spacer + actual thread engagement. No length/thread guessed.')
 elif h['id']=='F33':h.update(quantity=4,quantity_status='VESA75_OWNER_REFERENCE_FOUR_POINTS',notes='4 screws for selected direct VESA DMD. Non-VESA fallback not part of minimum hardware.')
 elif h['id']=='G10':h['notes']='V34 front-installed study752x459x4, final cut derives from actual liners/opening; old465 height superseded.'
 elif h['id']=='G08':h['notes']='V34 replaceable side back/lateral cushions, not top-loading U service channels.'
 elif h['id']=='G09':h['notes']='Padded bottom seat and upper anti-rattle cushion; final liner thickness selected after actual glass.'
 elif h['id']=='I08':h['notes']='2 metal retainer receivers in top underside; thread matches V34 strip screw family, no final size.'
template=copy.deepcopy(next(h for h in cat['hardware'] if h['id']=='F30'))
for id,en,pt,qty,cls in [('F63','Top direct side wood screw','Parafuso lateral direto do topo',4,'REQUIRED_FLATPACK_HARDWARE'),('F64','Monitor fixed-stop wood screw','Parafuso do batente fixo do monitor',4,'REQUIRED_FLATPACK_HARDWARE'),('F65','Glass upper-strip machine screw','Parafuso do retentor superior do vidro',2,'REQUIRED_FLATPACK_HARDWARE'),('W13','VESA large load washer','Arruela larga VESA',8,'USER_ADAPTER_HARDWARE'),('B19','Monitor tubular spacer','Espaçador tubular do monitor',4,'USER_ADAPTER_HARDWARE')]:
 assert not any(h['id']==id for h in cat['hardware']);h=copy.deepcopy(template);h.update(id=id,description_en=en,description_pt_BR=pt,quantity=qty,quantity_status='ARCHITECTURE_COUNT_HARDWARE_HOLD',flatpack_classification=cls,source=['config/backbox_simplification_v34.json'],instances=[],nominal_dimensions={'diameter_mm':None,'length_mm':None},notes='New V34 architecture, commodity hardware only. Actual thread/length/bore/engagement PURCHASE_BEFORE_CNC.',model={'strategy':'V34_REFERENCE_ONLY','path':'exports/generated/backbox-v34/study-hardware.FCStd','detailed_threads':False});cat['hardware'].append(h)
cat.update(version='V34',source_head='0993d9768582290915f7166c53507ffd2aa434b6',v34_retirements=retireids,manufacturing_ready=False)
cat['object_to_id']={k:v for k,v in cat.get('object_to_id',{}).items() if k not in removed}
for n in g['added_hardware']:
 id='F63' if 'TopDirect' in n else 'F64' if 'STOP' in n else 'F65' if 'GlassTop' in n else 'F30' if 'PanelBolt' in n else 'I12' if 'CrossDowel' in n else 'W13' if 'Washer' in n else 'B19' if 'Spacer' in n else 'F33' if 'DMDVESA' in n else 'F29'
 cat['object_to_id'][n]=id
 h=next(a for a in cat['hardware'] if a['id']==id);h['instances'].append({'object':n,'coordinate_xyz_mm':list(p[n].BoundBox.Center),'coordinate_meaning':'reference envelope centre; not final drill datum','source':'exports/generated/backbox-v34/candidate.FCStd','installation_direction':([-1 if p[n].BoundBox.Center.x<300 else 1,0,0] if id=='F64' else [1 if p[n].BoundBox.Center.x<300 else -1,0,0]) if id in ['F63','F64','F30'] else [0,0,1] if id=='F65' else [0,-1,0]})
# Current instances may not point to retired geometry.
for h in cat['hardware']:h['instances']=[a for a in h.get('instances',[]) if a.get('object') not in removed]
for id,names in [('G08',['BB_GlassSideCushionL','BB_GlassBackCushionL','BB_GlassSideCushionR','BB_GlassBackCushionR']),('G09',['BB_GlassBottomCushion','BB_GlassTopCushion'])]:
 h=next(a for a in cat['hardware'] if a['id']==id)
 if id=='G08':h.update(description_en='Backglass side cushion sets',description_pt_BR='Conjuntos de almofadas laterais do vidro',quantity=2,quantity_status='TWO_SIDES_BACK_AND_LATERAL_STRIPS')
 h['instances']=[{'object':n,'coordinate_xyz_mm':list(p[n].BoundBox.Center),'coordinate_meaning':'reference cushion centre, not a drilling datum','installation_direction':None,'source':'exports/generated/backbox-v34/candidate.FCStd'} for n in names]
 for n in names:cat['object_to_id'][n]=id
# F16 retains unresolved remaining shell and lower-seat fixings; not guessed quantities.
next(a for a in cat['hardware'] if a['id']=='F16')['notes']+=' Includes lower glass-seat attachment pending joint/fastener qualification.'
dump(R/'config/hardware_catalog_v34.json',cat)
(O/'manufacturing-mesh-delta.json.gz').write_bytes(gzip.compress(json.dumps(newmesh,separators=(',',':')).encode(),mtime=0));dump(O/'manufacturing-delta.json',{'retired_instances':[a['instance_id'] for a in retiredrows],'changed_rows':[a['instance_id'] for a in changedrows],'retired_hardware_ids':retireids,'counts':counts,'reconstruction_max_mm3':max(a['reconstruction_difference_mm3'] for a in changedrows),'wood_stocks':[12,18],'release':False})
dump(R/'config/manufacturing/flatpack_v34.json',{'version':'V34','current_register':'exports/generated/backbox-v34/manufacturing-register.json','current_BOM':'exports/generated/backbox-v34/manufacturing-bom.csv','active_nominal_plywood_stocks_mm':[12,18],'release':False,'hardware_catalog':'config/hardware_catalog_v34.json','fit':'measured stock + coupon; never nominal as measured','manual_finish':'edge hardware drilling with qualified guide; one-face CNC only'})
print('V34_MANUFACTURING',counts,'mass',mass['finished_wood_kg'],'reduction',mass['finished_reduction_kg'])
