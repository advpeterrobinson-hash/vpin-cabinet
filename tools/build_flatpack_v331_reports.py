"""Manufacturing inventory/BOM and conservative sheet-feasibility reports.
CERN-OHL-S-2.0. No production files or G-code.
"""
from pathlib import Path
import json,math,collections,html
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/flatpack-v331'
D=json.loads((O/'manufacturing-register.json').read_text());parts=D['parts'];byinst={p['instance_id']:p for p in parts}
C=json.loads((R/'config/hardware_catalog_v33.json').read_text());hardware={p['id']:p for p in C['hardware']}
def dump(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def md(n,lines):(O/n).write_text('\n'.join(s.rstrip() for s in lines).rstrip()+'\n')
rows=[]
for f in D['families']:
 ps=[byinst[i] for i in f['instances']];p=ps[0]
 row={k:p[k] for k in ['manufacturing_part_id','description_en','description_pt_BR','material_class','nominal_stock_thickness_mm','finished_reference_thickness_mm','finished_xy_size_mm','machining_face','opposite_face','manufacturing_status','fit_dependent','coupon_dependent','grain','outer_contour_brep','source']}
 row.update(quantity=len(ps),instances=f['instances'],assembly_ids=sorted(set(v['assembly_id'] for v in ps)),
            operations={'CUT':p['through_cuts'],'POCKET':p['pockets'],'LOCATOR':[],
                        'ENGRAVE':p['engraving'],'REFERENCE':p['reference_features']},
            manual_finish=p['manual_finish'],identical_relation='BOOLEAN_IDENTICAL_FINISHED_BREP_AND_SAME_FACE_STOCK',
            mirrored_relation='Installed handedness given by per-instance rigid placement; no second-face CNC',
            detailed_instance_register='manufacturing-register.json',full_sheet_release=False)
 rows.append(row)
bom={'status':'MANUFACTURING_PREPARATION_NOT_RELEASE','authority_for_future_nesting':True,
     'source_installed_components':93,'quantity_is_cut_pieces_not_assemblies':True,
     'measured_thickness_mm':None,'selected_coupon_clearance_mm':None,'rows':rows}
dump('manufacturing-bom.json',bom)
for lang in ('en','pt-BR'):
 pt=lang=='pt-BR';lines=['# '+('Lista de peças de madeira para fabricação — V33.1' if pt else 'Manufacturing wood BOM — V33.1'),'',
 'PRELIMINAR — NÃO USAR PARA CNC. Espessura real e folga dependem do lote/cupom.' if pt else 'PRELIMINARY — NOT FOR CNC. Actual thickness and fit clearance require production-lot measurements and coupon.', '',
 '| ID | '+('Descrição | Qtd. | Material | Chapa nominal | Acabado | X × Y mm | Face | Estado' if pt else 'Description | Qty | Class | Stock mm | Finished mm | X × Y mm | Face | Status')+' |',
 '| --- | --- | ---: | --- | ---: | ---: | --- | --- | --- |']
 for r in rows:
  dims=' × '.join(f'{v:.3f}' for v in r['finished_xy_size_mm'])
  lines.append(f"| {r['manufacturing_part_id']} | {r['description_pt_BR' if pt else 'description_en']} | {r['quantity']} | {r['material_class']} | {r['nominal_stock_thickness_mm']} | {r['finished_reference_thickness_mm']:.3f} | {dims} | FACE_A | {r['manufacturing_status']} |")
 lines+=['','## '+('Operações, conjuntos e identificação' if pt else 'Operations, assemblies and identity'),'']
 for r in rows:
  lines += [f"- **{r['manufacturing_part_id']}**: "+', '.join(r['instances'])+f". CUT {len(r['operations']['CUT'])}; POCKET {len(r['operations']['POCKET'])}; "+('acabamento manual ' if pt else 'manual finish ')+str(len(r['manual_finish']))+('; ajuste por cupom: ' if pt else '; fit-dependent: ')+str(r['fit_dependent'])+'.']
 lines+=['',('Direções, profundidades, contornos B-rep exatos, origens e instruções manuais: [manufacturing-register.json](manufacturing-register.json).' if pt else 'Detailed numeric directions, depths, exact B-rep contours, source mapping and manual instructions: [manufacturing-register.json](manufacturing-register.json).'),
          'CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet']
 md('manufacturing-wood-bom-'+lang+'.md',lines)

# A deliberate row/shelf heuristic; exact finished contours drawn inside conservative
# rectangles. No interlocking into holes and no claim of optimization.
sheets=[];stock=[];largest=[]
for thickness in sorted({p['nominal_stock_thickness_mm'] for p in parts},reverse=True):
 group=[p for p in parts if p['nominal_stock_thickness_mm']==thickness];gs=[]
 for p in group:
  w,h=p['finished_xy_size_mm'];rot=h>w
  if rot:w,h=h,w
  if not(w<=2460+1e-6 and h<=1560+1e-6):raise RuntimeError('STOP: part does not fit supplier sheet: '+p['instance_id'])
  largest.append({'instance':p['instance_id'],'id':p['manufacturing_part_id'],'finished_xy_mm':p['finished_xy_size_mm'],
     'sheet_xy_mm':[w,h],'rotation_deg':90 if rot else 0,'fits':True,
     'rotation_90_geometrically_possible':min(p['finished_xy_size_mm'])<=1560 and max(p['finished_xy_size_mm'])<=2460,
     'grain':'Assumed along longest part dimension and 2500 sheet direction; material orientation must be confirmed. No arbitrary alternate rotation used.'})
  gs.append((p,w,h,rot))
 local=[]
 for p,w,h,rot in sorted(gs,key=lambda a:(-a[2],-a[1])):
  placed=False
  for sh in local:
   for row in sh['rows']:
    if h<=row['height']+1e-6 and row['next_x']+w<=2480+1e-6:
     x,y=row['next_x'],row['y'];row['next_x']=x+w+15;placed=True;break
   if placed:break
   y=20+sum(r['height']+15 for r in sh['rows'])
   if y+h<=1580+1e-6:
    sh['rows'].append({'y':y,'height':h,'next_x':20+w+15});x=20;placed=True;break
  if not placed:
   sh={'sheet_id':f'T{thickness:g}-P{len(local)+1}','nominal_stock_mm':thickness,'material':'PREMIUM_FIRST_ALL_PARTS',
       'rows':[{'y':20,'height':h,'next_x':20+w+15}],'placements':[]};local.append(sh);x,y=20,20
  sh['placements'].append({'instance_id':p['instance_id'],'manufacturing_part_id':p['manufacturing_part_id'],
     'x_mm':x,'y_mm':y,'width_mm':w,'height_mm':h,'rotation_deg':90 if rot else 0,
     'material_class':p['material_class'],'finished_outline':p['review_outline'],'outline_local_bounds':p['finished_xy_bounds_mm']})
 sheets+=local
 area=sum(p['projected_area_mm2'] for p in group)
 stock.append({'nominal_thickness_mm':thickness,'piece_count':len(group),
    'structural_premium':sum(p['material_class']=='STRUCTURAL_PREMIUM' for p in group),
    'modular_secondary_eligible':sum(p['material_class']=='MODULAR_SECONDARY' for p in group),
    'finished_outer_contour_area_mm2':area,'area_only_sheet_lower_bound':math.ceil(area/(2460*1560)),
    'conservative_row_layout_sheets':len(local),'all_premium_first':True})
# Independent rectangle-distance check: guarantees >=15 between exact contained contours.
for sh in sheets:
 for i,a in enumerate(sh['placements']):
  assert a['x_mm']>=20 and a['y_mm']>=20 and a['x_mm']+a['width_mm']<=2480+1e-6 and a['y_mm']+a['height_mm']<=1580+1e-6
  for b in sh['placements'][i+1:]:
   dx=max(0,a['x_mm']-b['x_mm']-b['width_mm'],b['x_mm']-a['x_mm']-a['width_mm'])
   dy=max(0,a['y_mm']-b['y_mm']-b['height_mm'],b['y_mm']-a['y_mm']-a['height_mm'])
   assert math.hypot(dx,dy)>=15-1e-6
layout={'status':'PRELIMINARY_NOT_FOR_CNC','optimized':False,'method':'descending-height row heuristic with conservative bounding rectangles, exact contour overlays; no in-hole packing',
   'supplier_sheet_mm':[2500,1600],'usable_mm':[2460,1560],'border_mm':20,'spacing_mm':15,
   'grain_assumption':'Longest part axis parallel 2500 sheet edge; grade/ply direction still requires stock qualification',
   'stock':stock,'sheets':sheets,'largest_parts':sorted(largest,key=lambda p:p['sheet_xy_mm'][0]*p['sheet_xy_mm'][1],reverse=True),
   'production_authorized':False}
dump('preliminary-layout.json',layout)
lines=['# Preliminary sheet feasibility','','PRELIMINARY — NOT FOR CNC. No CAM/G-code. Not optimized. Exact contour overlays inside conservative rectangles; 20 mm border and >=15 mm spacing. All stock stays premium in this first attempt. Sheet format for non-18 mm stock is a study assumption, not a supplier stock order.','',
 '| Stock mm | Pieces | Structural | Secondary eligible | Area-only lower bound | Row-layout sheets |','| ---: | ---: | ---: | ---: | ---: | ---: |']
for s in stock:lines.append('| '+' | '.join(str(s[k]) for k in ['nominal_thickness_mm','piece_count','structural_premium','modular_secondary_eligible','area_only_sheet_lower_bound','conservative_row_layout_sheets'])+' |')
lines+=['','## Largest parts','','| ID / instance | Finished local XY mm | Sheet rotation | Fits |','| --- | --- | --- | --- |']
for p in layout['largest_parts'][:12]:lines.append(f"| {p['id']} / {p['instance']} | {p['finished_xy_mm'][0]:.3f} × {p['finished_xy_mm'][1]:.3f} | {p['rotation_deg']}° | YES |")
lines+=['','Every individual part fits. Every rotated part remains FACE_A up. Ninety-degree rotation is geometrically possible for all current members, but no arbitrary grain-swapping rotation was used to improve packing. Long-axis grain is a conservative planning assumption, not a verified veneer direction.',
 'Hold-down: every piece lies inside the border; local retention for tiny parts, narrow strips and open frames still needs supplier tabs/fixtures. A perimeter fit does not certify vacuum holding.',
 'Do not downgrade structural pieces. A secondary-stock alternative is allowed only after the small-subset/extra-premium-sheet trigger is reviewed; this task does not automatically invoke it.']
md('sheet-feasibility.md',lines)
md('stock-thickness-families.md',['# Stock thickness families','','Nominal preparation only. Every actual stock lot must be measured. Odd finished dimensions do not imply an odd sheet order.','']+
 [f"- {s['nominal_thickness_mm']:g} mm: {s['piece_count']} pieces; structural {s['structural_premium']}, secondary-eligible {s['modular_secondary_eligible']}." for s in stock]+
 ['','14 mm hinge cleats use 18 mm stock face-reduced 4 mm. Retainer strip uses 18 mm reduced to13.8. Monitor stops use18 +12 mm planar laminations rather than a30 mm blank. Cassette cleats use two12 mm layers rather than24 mm stock. Existing4/6/8 mm finished parts remain their own stock groups; no thickness substitutions.'])

specs={
 'F06':('TRULY_TBD',None,'Permanent shell/floor/cleat reinforcement schedule has no countable attachment geometry. Do not invent dense screws.'),
 'G01':('TRULY_TBD',None,'New decomposition glue lands are explicit; total cabinet adhesive still needs the complete approved glue-joint schedule and selected adhesive spread rate. Partial formula: sum(approved glue land m²) × vendor g/m² × waste factor / package grams.'),
 'F53':('FORMULA_FROM_SELECTED_HARDWARE','1 * selected_keeper.mounting_hole_count - included_fasteners','One main rear keeper; CURRENT reserve has no fastening holes. Count follows selected keeper, not its bounding box.'),
 'W06':('FORMULA_FROM_SELECTED_HARDWARE','sum(required_stack_items_for_2_pivots_and_6_floor_bolts) - matching_items_in_purchased_kits','Purchased WPC stack must be itemized; included nuts/washers contribute zero additional purchase quantity. Inclusion is conditional, not assumed.'),
 'F16':('TRULY_TBD',None,'Backbox shell/frame/rail and cleat attachment schedule is still undefined. Decomposition glue does not define original attachment screw counts.'),
 'F18':('FORMULA_FROM_SELECTED_HARDWARE','2 * (fixed_leaf_holes_used + moving_leaf_holes_used) - included_hinge_screws','Two piano hinges; actual approved used-hole schedule and supplied contents must be known. No assumed hole pitch.'),
 'F19':('TRULY_TBD',None,'Two passive bolts are counted, but their screws, cam retention and astragal wood fixing schedule are mixed in this row and not completely specified.'),
 'F22':('TRULY_TBD',None,'Two intake assemblies exist; their serviceable attachment count is not modeled. The historical two-screw comment concerns an upper fan cover, not a complete low-intake fixing schedule.'),
 'F28':('TRULY_TBD',None,'Stop/cleat decomposition glue seams are defined, but original carrier-to-rail/stop/contact-pad attachment details are not all drilled.'),
 'F31':('TRULY_TBD',None,'No current insert/baffle attachment holes; four cassette bolts are already a different counted family, not insert fasteners.'),
 'F36':('FORMULA_FROM_SELECTED_HARDWARE','sum(selected_side_channel.mounting_holes_used) + selected_lockdown_receiver.mounting_holes_used - included_fasteners','Selected glass channel/lockdown interface and supplied contents determine count.'),
 'F38':('FORMULA_FROM_SELECTED_HARDWARE','4 * selected_leg_backing.retention_holes_used - included_retention_screws','Four backing interfaces; separate from primary leg bolts. Actual selected backing may have its own supplied set.'),
 'F39':('FORMULA_FROM_SELECTED_HARDWARE','selected_front_door_frame.mounting_holes_used - included_frame_fasteners','One selected front-door frame; no invented historical count.')}
closure=[{'id':id,'classification':v[0],'quantity':None,'formula':v[1],'evidence':v[2],'source':hardware[id]['source']} for id,v in specs.items()]
dump('hardware-quantity-closure.json',{'before_unresolved':13,'exact_closed':0,'formula_driven':6,'included_in_assembly_unconditionally':0,'truly_tbd':7,'rows':closure})
md('hardware-quantity-closure.md',['# Required hardware quantity closure','','No previously unknown integer count can be derived honestly from current attachment geometry. Six rows now have explicit selected-hardware formulas; seven retain a genuine design/consumption hold. Kit contents are subtracted only after verification. This does not overwrite historical V33 BOM evidence.','',
 '| ID | Classification | Formula | Evidence |','| --- | --- | --- | --- |']+[f"| {p['id']} | {p['classification']} | {p['formula'] or '—'} | {p['evidence']} |" for p in closure])
interfaces=[{'id':h['id'],'description':h['description_en'],'source':h['source'],'hold':h['freeze_status'],'measurement_fields':h.get('measurement_fields',{})} for h in C['hardware'] if h['controls_permanent_cnc']]
dump('hardware-interface-holds.json',interfaces)
fit=[{'instance':p['instance_id'],'source_component':p['source_component'],'fit_expression':p['fit_expression'],
      'status':'PARAMETRIC_HOLD_NO_NOMINAL18_FIT_RELEASE','affected_features':[op['id'] for op in p['pockets']+p['through_cuts'] if op.get('square_mating_relief_candidate')]} for p in parts if p['fit_dependent']]
dump('fit-dependent-joints.json',fit)
md('fit-dependent-joints.md',['# Fit-dependent joints','','Reference B-reps retain nominal accepted geometry for equivalence only. Slots/captures must regenerate from measured thickness + selected coupon total clearance before manufacturing. No blanket dogbones.','']+[f"- {p['instance']}: {p['source_component']} — {p['fit_expression']}; {', '.join(p['affected_features']) or 'capture/interface profile'}." for p in fit])
manual=[{'part':p['manufacturing_part_id'],'instance':p['instance_id'],'local_to_installed_matrix':p['local_to_installed_matrix'],'operations':p['manual_finish']} for p in parts if p['manual_finish']]
dump('manual-finish-schedule.json',manual)
md('manual-finish-schedule.md',['# Manual finish schedule','','All coordinates use the part’s finished FACE_A datum; +z enters the wood. FACE_B has NO CNC. Edge/oblique bores use an ordinary drill/driver with a qualified guide; hardware/pilot depth remains provisional. No freehand drill-angle accuracy is claimed.','']+
 [f"- **{p['instance']} / {p['part']}**: "+'; '.join(x['operation']+' '+x.get('feature','') for x in p['operations'])+'. See numeric entry/exit vectors and exact removal B-rep in the JSON register.' for p in manual])
md('operation-face-report.md',['# One-sided operation audit','','Every part has a rigid local-to-installed transform. FACE_A is finished z=0, +z into wood. Full-face thickness reduction is performed first from the same side, then reset the finished-face datum. No CNC flip. Status denotes preparation-route closure, not manufacturing release.','',
 '| Instance | ID | FACE_A outward in installed XYZ | Stock / finished mm | CUT / POCKET | Manual | Blockers |','| --- | --- | --- | --- | --- | ---: | --- |']+
 [f"| {p['instance_id']} | {p['manufacturing_part_id']} | {', '.join(f'{v:.6g}' for v in p['face_A_outward_world'])} | {p['nominal_stock_thickness_mm']} / {p['finished_reference_thickness_mm']:.3f} | {len(p['through_cuts'])} / {len(p['pockets'])} | {len(p['manual_finish'])} | {'; '.join(p['blockers']) or '—'} |" for p in parts])
md('decomposition-report.md',['# Exact wood decomposition','','Every new assembly is compared by symmetric Boolean difference against its accepted installed B-rep. Difference tolerance1e-4 mm³; numerical overlap summation tolerance1e-3 mm³. No CAD reference is edited. Glue joints are a manufacturing assembly proposal, with bond/thickness and structural qualification still held.','',
 '| Assembly | Members | Union difference mm³ | Joinery |','| --- | --- | ---: | --- |']+
 [f"| {a['id']} {a['source_component']} | {', '.join(a['pieces'])} | {a['symmetric_difference_mm3']:.9g} | {a['joinery']} |" for a in D['assemblies'] if a['decomposed']]+
 ['','The15 prior blocked installed assemblies now have explicit exact members. Geometric decomposition is not a proof of adhesive bond strength. No extra screws are added to disguise an undefined original joint schedule.'])
engrave=[{'instance':p['instance_id'],'id':p['manufacturing_part_id'],**p['engraving']} for p in parts]
dump('part-id-engraving-map.json',engrave)
summary={'source_head':D['source_head'],'installed_components_audited':len(D['assemblies']),'manufacturing_piece_count':len(parts),'canonical_manufacturing_families':len(rows),
 'statuses_by_piece':dict(collections.Counter(p['manufacturing_status'] for p in parts)),
 'decomposed_prior_blockers':15,'decomposition_remaining':[], 'stock':stock,'required_hardware_before':13,
 'hardware_exact_closed':0,'hardware_formula_driven':6,'hardware_truly_tbd':7,
 'largest_by_area':layout['largest_parts'][0],'preliminary_sheets':len(sheets),'full_sheet_release':False,
 'current_geometry_changed':False,'coupon':'WAITING_FOR_PRODUCTION_LOT_MATERIAL'}
dump('summary.json',summary)
print('FLATPACK_V331_REPORTS_PASS',len(parts),'pieces;',len(sheets),'preliminary sheets;',summary['statuses_by_piece'])
