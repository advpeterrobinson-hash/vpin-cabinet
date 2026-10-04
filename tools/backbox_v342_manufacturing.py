"""Exact V34.2 wood/hardware delta and material ledger. CERN-OHL-S-2.0."""
from backbox_v342_common import *
import copy,csv,collections
G=json.loads((O/'geometry-validation.json').read_text());assert G['pass'];p=load(O/'candidate.FCStd');reg=json.loads((R/'exports/generated/backbox-v34/manufacturing-register.json').read_text());before=copy.deepcopy(reg);ret=set(G['retired']);changed=set(G['wood_changed']);rows=[];errors=[]
for src in reg['parts']:
 if src['source_component'] in ret:continue
 a=copy.deepcopy(src);n=a['source_component']
 if n=='BB_MONITOR_PLATE':a['manufacturing_part_id']='M078';a['superseded_ambiguous_family_id']='M074';a['id_correction']='V34 duplicated M074 with12mm Underfront_Plate; geometry unchanged by ID correction'
 if n in changed:
  q=p[n].copy();m=A.Matrix(*a['local_to_installed_matrix']);q.transformShape(m.inverse(),True);fp=O/(a['instance_id']+'-finished.brep');q.exportBrep(str(fp));back=q.copy();back.transformShape(m,True);e=back.cut(p[n]).Volume+p[n].cut(back).Volume;assert e<1e-3;errors.append(e);b=q.BoundBox
  a.update(version='V34.2',finished_member_brep=str(fp.relative_to(R)),volume_mm3=q.Volume,finished_xy_bounds_mm=[b.XMin,b.YMin,b.XMax,b.YMax],geometry_authority='exports/generated/backbox-v342/candidate.FCStd#'+n,reconstruction_difference_mm3=e,manufacturing_release=False,manufacturing_status='ONE_SIDE_CNC_PLUS_MANUAL_FINISH',fit_dependent=True,coupon_dependent=True,cnc_stage_brep=None,outer_contour_brep=None,cnc_outer_access_brep=None)
  for k in ['through_cuts','pockets','feature_register','joinery','review_outline']:a.pop(k,None)
  a['one_face_plan']='FACE_A inside / top: direct guide or fan through cuts or local glass-plane bevel; FACE_B NO CNC. Purchased channels/fasteners and cutter/coupon define final fit.'
  a['manual_finish']=[{'operation':'HARDWARE_AND_FIT_HOLD','face_datum':'FACE_A','depth_mm':None,'instruction':'Selected hardware drilling, coupon fit and angled-pocket surface qualification before release; no CNC flip.'}]
  if n=='BB_Floor':a['one_face_plan']='FACE_A TOP: local variable-depth front rebate follows measured glass plane9.90666925365deg. No base tilt. Ø4 cutter accessible from above; small R2 corners/finish and minimum front skin require coupon/supplier validation.'
  if n.startswith('BB_Door'):a['one_face_plan']='FACE_A inside: contour,2xØ116 reference openings and105mm pitch reference bores. Final purchased fan/grill drilling HOLD; no filter frames/baffles.'
  a['operations']={'CUT':'nominal outer contour and functional openings','POCKET':a['one_face_plan'],'LOCATOR':'final purchased hardware only','ENGRAVE':'optional hidden ID','REFERENCE':'NOT FOR CNC'}
 rows.append(a)
families=[{'id':f,'quantity':sum(a['manufacturing_part_id']==f for a in rows),'instances':[a['instance_id'] for a in rows if a['manufacturing_part_id']==f]} for f in sorted({a['manufacturing_part_id'] for a in rows})]
reg.update(version='V34.2',supersedes='V34',parts=rows,families=families,manufacturing_pieces=len(rows),CNC_plywood_pieces=sum(a['nominal_stock_thickness_mm'] is not None for a in rows),canonical_families=len(families),CNC_families=len(families)-2,installed_components=len({a['source_component'] for a in rows}),retired_rows=[{'id':a['manufacturing_part_id'],'instance':a['instance_id'],'source':a['source_component']} for a in before['parts'] if a['source_component'] in ret]);dump('manufacturing-register',reg)
with (O/'manufacturing-bom.csv').open('w') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(['ID','instance','source','stock','quantity','material','status','volume_mm3'])
 for a in rows:w.writerow([a['manufacturing_part_id'],a['instance_id'],a['source_component'],a['nominal_stock_thickness_mm'],1,a['material_class'],a['manufacturing_status'],a['volume_mm3']])
mass=sum(a['volume_mm3'] for a in rows)*650/1e9;previous=sum(a['volume_mm3'] for a in before['parts'])*650/1e9
woodremoved=sum(a['volume_mm3'] for a in before['parts'] if a['source_component'] in ret)/1e6
massdata={'basis':'actual finished B-rep volume','density_kg_m3':650,'wood_kg':mass,'previous_wood_kg':previous,'delta_kg':mass-previous,'LOW550_kg':mass*550/650,'HIGH750_kg':mass*750/650,'acrylic3mm_kg':p['BB_AcrylicFront'].Volume*1180/1e9,'playfield_glass5mm_kg':p['CandidateGlass'].Volume*2500/1e9,'hardware_mass':'UNKNOWN_NOT_ZERO','removed_backbox_wood_volume_litre':woodremoved,'plywood_stocks':sorted({a['nominal_stock_thickness_mm'] for a in rows if a['nominal_stock_thickness_mm'] is not None}),'counts':{k:reg[k] for k in ['manufacturing_pieces','CNC_plywood_pieces','canonical_families','installed_components']},'reconstruction_max_mm3':max(errors)};dump('mass-counts',massdata)
cat=json.loads((R/'config/hardware_catalog_v34.json').read_text());retireids=['F22','F23','B10','G07'];by={h['id']:h for h in cat['hardware']}
for id in retireids:by[id].update(active=False,quantity=0,quantity_status='RETIRED_V342',design_status='RETIRED',instances=[],notes='Removed backbox-only filter/baffle/cable management system; builder routing is not a universal cabinet interface.')
for h in cat['hardware']:h['instances']=[a for a in h.get('instances',[]) if a.get('object') not in ret]
by['G10'].update(description_en='Clear acrylic backbox front with rear black mask',description_pt_BR='Frente de acrílico transparente com máscara preta traseira',material='PMMA_ACRYLIC',nominal_dimensions={'reference_mm':[752,459,3],'final_cut_mm':None},notes='3mm planning choice; no backglass. Actual flatness/thickness/channel/thermal fit and rear mask cut remain HOLD.')
by['G11']['notes']='5mm nominal tempered safety playfield glass;115? no released order size. Reference575x1142 on slope; actual channel/lockdown/fit defines final cut.'
by['G11']['notes']=by['G11']['notes'].replace('115? ','')
by['E02'].update(description_en='TCL 32S5K primary monitor reference',description_pt_BR='Monitor de referência principal TCL32S5K',nominal_dimensions={'without_stand_mm':[715,422,75],'mass_kg':3.15,'VESA_mm':[100,100],'thread':'M4','boss_plane_mm':None},notes='Official NZ specification. Purchased local variant, boss position/depth and screw engagement remain HOLD. Not a mandatory electronics purchase.')
by['F29']['notes']='4 M4-family reference VESA100 screws. Length =18mm plate +washer +selected spacer +actual monitor engagement; manufacturer M4x10 reference is NOT the assembled cabinet screw length.'
for id in ['G08','G09']:by[id]['description_en']=by[id]['description_en'].replace('Backglass','Acrylic front');by[id]['notes']='Replaceable acrylic seat liners; actual thickness/thermal-fit coupon HOLD.'
by['F65']['description_en']='Acrylic upper-retainer screw'
template=copy.deepcopy(by['F30'])
for id,desc,qty,cls in [('F66','Lower passive grille M4-family fixing',8,'REQUIRED_FLATPACK_HARDWARE'),('F67','Lower active fan/grille M4-family through bolt',8,'OPTIONAL_FLATPACK_HARDWARE'),('H28','Optional lower120mm intake fan',2,'OPTIONAL_FLATPACK_HARDWARE'),('B20','Commodity120mm lower protective grille',2,'REQUIRED_FLATPACK_HARDWARE'),('B21','Rear playfield-glass plastic U-channel',1,'REQUIRED_FLATPACK_HARDWARE')]:
 h=copy.deepcopy(template);h.update(id=id,description_en=desc,description_pt_BR={'F66':'Fixação M4 da grade passiva inferior','F67':'Parafuso M4 do ventilador/grade inferior','H28':'Ventilador inferior120mm opcional','B20':'Grade de proteção comercial120mm','B21':'Canal U plástico traseiro do vidro do playfield'}[id],quantity=qty,flatpack_classification=cls,quantity_status='EXACT_ARCHITECTURE_COUNT_HARDWARE_DIMENSIONS_HOLD',nominal_dimensions={'final_dimensions':None},instances=[],source=['config/backbox_hardening_v342.json'],notes='Purchased hardware/profile before final cuts. F67 replaces F66 in active mode; do not add both fastener stacks. Protective-grille finger safety and actual fan hardware require physical verification.',model={'strategy':'ORIGINAL_REFERENCE_ENVELOPE','path':'exports/generated/backbox-v342/variants.FCStd','detailed_threads':False});cat['hardware'].append(h);by[id]=h
cat['object_to_id']={k:v for k,v in cat['object_to_id'].items() if k not in ret}
newmap={n:'G10' if n in ['BB_AcrylicFront','BB_AcrylicMask'] else 'G08' if 'SideLiner' in n or 'BackLiner' in n else 'G09' if 'Liner' in n else 'F65' if 'RetainerScrew' in n else 'F66' if 'LowerGrillScrew' in n else 'B20' if 'LowerGrill' in n else 'B21' if n=='BB_PFRearChannel' else None for n in p if n not in cat['object_to_id']}
for n,id in newmap.items():
 if id:cat['object_to_id'][n]=id;by[id]['instances'].append({'object':n,'coordinate_xyz_mm':list(p[n].BoundBox.Center),'installation_direction':[0,-1,0],'coordinate_meaning':'reference centre, not released drilling'})
for side in ['L','R']:cat['object_to_id']['BB_LowerIntakeFan'+side]='H28'
# Refresh installed coordinates rather than carrying V34 VESA positions.
for h in cat['hardware']:
 for inst in h.get('instances',[]):
  n=inst.get('object')
  if n in p and n in G['changed']:inst['coordinate_xyz_mm']=list(p[n].BoundBox.Center);inst['coordinate_meaning']='reference geometry centre; exact hardware drilling HOLD'
for id in ['G10','G11','F66','B20','B21']:by[id]['model']={'strategy':'ORIGINAL_REFERENCE_ENVELOPE','path':'exports/generated/backbox-v342/candidate.FCStd','detailed_threads':False}
by['G11']['nominal_dimensions']={'reference_cut_mm':[575,1142,5],'final_cut_mm':None}
by['B21']['material']='commodity plastic / compliant liner; selected profile HOLD'
by['H28']['material']='commodity fan assembly; mixed materials'
by['H28']['instances']=[{'object':'BB_LowerIntakeFan'+side,'coordinate_xyz_mm':[x,1297.6,738],'installation_direction':[0,1,0],'coordinate_meaning':'reference body centre; not drilling'} for side,x in [('L',155),('R',445)]]
rearfix=copy.deepcopy(template);rearfix.update(id='F68',description_en='Rear playfield-glass channel attachment, selected profile dependent',description_pt_BR='Fixação do canal traseiro do vidro, dependente do perfil',quantity=None,quantity_status='FORMULA_FROM_SELECTED_HARDWARE',quantity_formula='selected rear-channel manufacturer attachment count; no drilled centres released',flatpack_classification='REQUIRED_FLATPACK_HARDWARE',freeze_status='PURCHASE_BEFORE_CNC',nominal_dimensions={'diameter_mm':None,'length_mm':None},instances=[],notes='Positive channel-to-BB_Floor attachment must be qualified with selected profile and residual wood thickness. No unsupported short wood-screw engagement is approved.',model={'strategy':'UNRESOLVED_NO_FIT_MODEL','detailed_threads':False},source=['config/backbox_hardening_v342.json']);cat['hardware'].append(rearfix)
assert len({h['id'] for h in cat['hardware']})==len(cat['hardware'])
cat.update(version='V34.2',source_head=C['head_before'] if 'C' in globals() else '8d951bc37a38d5e3820cbde93700f1161ff32fb1',manufacturing_ready=False,v342_retirements=retireids)
(R/'config/hardware_catalog_v342.json').write_text(json.dumps(cat,indent=2,ensure_ascii=False)+'\n')
(R/'config/manufacturing/flatpack_v342.json').write_text(json.dumps({'version':'V34.2','current_register':'exports/generated/backbox-v342/manufacturing-register.json','current_BOM':'exports/generated/backbox-v342/manufacturing-bom.csv','active_nominal_plywood_stocks_mm':[12,18],'release':False,'hardware_catalog':'config/hardware_catalog_v342.json','actual_thickness_mm':None,'coupon_clearance_mm':None},indent=2)+'\n')
dump('manufacturing-delta',{'retired_instances':[a['instance'] for a in reg['retired_rows']],'changed_rows':[a['instance_id'] for a in rows if a['source_component'] in changed],'retired_hardware_ids':retireids,'reconstruction_max_mm3':max(errors),'counts':massdata['counts']})
print('V342_MANUFACTURING',massdata['counts'],mass)
