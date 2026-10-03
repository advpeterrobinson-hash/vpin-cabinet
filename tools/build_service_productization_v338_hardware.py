"""Scoped V33.8 hardware lifecycle overlay. CERN-OHL-S-2.0.
No hardware dimensions selected, no unresolved counts closed by assumption.
"""
from pathlib import Path
import json,copy,hashlib,csv
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/service-productization-v338'
def read(p):return json.loads(Path(p).read_text())
def dump(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
C=read(R/'config/service_productization_v338.json');G=read(O/'geometry-validation.json');assert G['pass'] and not G['manufacturing_release']
cat=read(R/'config/hardware_catalog_v337.json');old=copy.deepcopy(cat['hardware']);rows={h['id']:h for h in cat['hardware']}
retired=rows['F60'];assert retired['quantity']==4
retired.update(quantity=0,quantity_status='RETIRED_BY_SW02_SOLID_BLOCK',flatpack_classification='REFERENCE_ONLY_NOT_FROZEN',freeze_status='PROVISIONAL',design_status='SUPERSEDED',instances=[],controls_permanent_cnc=False,notes=retired['notes']+' V33.8: four lamination screws eliminated with the six plywood layers. ID preserved for history; zero current purchase quantity and no current installed instances.')
# H27's dimensions/instances remain unchanged. Its active explanatory note
# must not describe the old mechanical travel as a usable installed range.
h27=rows['H27'];old_tail='±3 mm is installation/stock compensation around the unchanged CURRENT pose, not permission to change the playing angle; whole-pose range extremes are not validated.'
assert h27['notes'].count(old_tail)==1
h27['notes']=h27['notes'].replace(old_tail,'Reference mechanical hardware travel is ±3 mm only. The V33.8 installed common-height setup screen is −1.9 to +0.9 mm with 1 mm geometric clearance; ±3 mm is NOT a usable installed range. Setup must reproduce the unchanged nominal PLAY pose, not select a playing angle or impose differential twist. Purchased tolerances, contact leveling and physical qualification remain held.')
removed_names=[f'FrontLanding{s}_LaminationScrew{i}' for s in 'LR' for i in (1,2)]
for name in removed_names:assert cat['object_to_id'].pop(name)=='F60'
# Preserve reference hardware rows and nominal dimensions; expose a distinct
# active installed-range authority instead of pretending mechanical travel is usable.
cat.update(version='V33.8',source_head=C['head_before'],authority='V33.8 SW02 simplification and scoped serviceability studies; purchased hardware and all manufacturing release remain held',manufacturing_ready=False)
cat['v338_authority']={'previous_catalog':'config/hardware_catalog_v337.json','changed_existing_ids':['F60','H27'],'metadata_only_changed_ids':{'H27':['notes']},'retired_required_quantity':{'F60':4},'retention':'A: original captive M6×100 tool-operated bolt and all stops/captivity retained','source_native_sha256':hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest(),'minimum_optional_dependency':False}
cat['v338_adjustment_authority']={'hardware_id':'H27','mechanical_reference_travel_mm':C['adjustment']['mechanical_travel_reference_mm'],'safe_installed_range_mm':C['adjustment'].get('final_safe_range_mm'),'scope':C['adjustment']['permitted_use'],'source':'config/service_productization_v338.json#adjustment','rule':'Mechanical±3 mm is not a safe installed-use claim; setup uses only the separately validated installed range. No user-selected playing-angle adjustment or unvalidated differential twist.'}
cat['v338_optional_studies']={'accessory_board':'ACC01 separate optional BOM if validated; no minimum wood/hardware quantity added','safety_straps':'Study only unless explicitly promoted by the final safety report; no textile rating or required quantity inferred','commercial_drill_guide':'Required qualified tool for SW02 drilling; not installed cabinet hardware'}
assert [h for h in cat['hardware'] if h['id'] not in ('F60','H27')]==[h for h in old if h['id'] not in ('F60','H27')]
assert {k:v for k,v in h27.items() if k!='notes'}=={k:v for k,v in next(h for h in old if h['id']=='H27').items() if k!='notes'}
dump(R/'config/hardware_catalog_v338.json',cat)
closure=read(R/'exports/generated/two-stock-user-module-v337/hardware-quantity-closure.json');closure['version']='V33.8'
for row in closure['rows']:
 if row['id']=='F60':row.update(classification='RETIRED_FROM_CURRENT',quantity=0,reason='SW02 solid blocks eliminate four binder screws')
dump(O/'hardware-quantity-closure.json',closure)
dump(O/'hardware-lifecycle.json',{'version':'V33.8','pass':True,'retired_required':[{'id':'F60','before':4,'after':0}],'unchanged_existing_families':164,'metadata_only_changes':{'H27':['notes']},'new_required_hardware':0,'selected_retention':'A','manufacturing_release':False,'optional_studies_separate':True})
(O/'hardware-status.md').write_text('# V33.8 hardware status\n\nSW02 eliminates F60 ×4 lamination screws and the lamination glue-up. F60 remains a historical catalog ID with current quantity zero. H27 receives a notes-only correction separating mechanical ±3 mm travel from the −1.9/+0.9 mm installed setup screen. Its dimensions, quantity and all other fields remain unchanged. The other 164 catalog families remain byte-equivalent; all unresolved purchased hardware remains held.\n\nThe two original captive M6×100 tool-operated retainers remain selected. Hand knobs and quick pins are studies, not added required hardware. Mechanical adjuster travel and the safe installed setting range are separate authorities; see config/service_productization_v338.json.\n\nSW02 drilling requires a qualified clamped portable perpendicular guide, a scale-verified center template, selected bits/countersink and depth stops. Paper alone does not control the54/68 mm paths. Guide/wood/hardware coupon and structural qualification remain pending.\n\nOptional accessory boards/clamps and safety-strap studies remain outside the minimum mechanical BOM unless separately accepted. No custom metal or new mandatory electronics are added.\n')
# A separate accessory ledger is deliberately not merged into the installed
# register, required catalog quantities, minimum sheet study or wood packages.
mod=read(R/'config/service_modularity_v338.json');board=mod['optional_board']
accessories=[
 {'id':board['family'],'description_en':'Optional removable accessory board','description_pt_BR':'Placa opcional removível para acessórios','classification':'OPTIONAL_STUDY_NOT_MINIMUM_FLATPACK','required_quantity':0,'user_selected_quantity':None,'quantity_formula':'N = builder-selected board count','study_sample_quantity':len(board['samples']),'material':'12 mm plywood, MODULAR_SECONDARY','nominal_dimensions_mm':[board['width_mm'],board['depth_mm'],board['nominal_stock_mm']],'selected_sku':None,'source':'config/service_modularity_v338.json#optional_board','status':'OPTIONAL; payload and purchased clamp qualification pending'},
 {'id':'ACC01-CLAMPS','description_en':'Commodity removable clamps for each selected accessory board','description_pt_BR':'Grampos comerciais removíveis para cada placa de acessórios escolhida','classification':'OPTIONAL_HARDWARE_INTERFACE_NOT_SELECTED','required_quantity':0,'user_selected_quantity':None,'quantity_formula':str(board['clamps_per_board'])+' × N selected ACC01 boards','study_sample_quantity':board['clamps_per_board']*len(board['samples']),'material':'Commodity clamp; purchased construction and dimensions pending','nominal_dimensions_mm':None,'selected_sku':board['clamp_selected_sku'],'source':'config/service_modularity_v338.json#optional_board','status':'PURCHASE_BEFORE_ASSEMBLY; no permanent cabinet holes; no load rating assumed'},
 {'id':'STUDY-SAFETY-STRAPS','description_en':'Secondary safety straps and anchors, unselected study','description_pt_BR':'Cintas secundárias e ancoragens, estudo não selecionado','classification':'REFERENCE_ONLY_NOT_FROZEN','required_quantity':0,'user_selected_quantity':0,'quantity_formula':'0 promoted; no straps or anchors in minimum cabinet','study_sample_quantity':2,'material':'Rated webbing and anchors would require future selection','nominal_dimensions_mm':None,'selected_sku':None,'source':'exports/generated/service-productization-v338/safety-report.md','status':'NONE PROMOTED; primary raised-playfield support remains OPERATIONAL HOLD'}]
ledger={'version':'V33.8','minimum_BOM_includes_these_rows':False,'included_in_minimum_nesting_mass_or_packing':False,'no_new_manufacturing_family':True,'manufacturing_release':False,'rows':accessories,'source_sha256':{'config/service_modularity_v338.json':hashlib.sha256((R/'config/service_modularity_v338.json').read_bytes()).hexdigest()}}
dump(O/'optional-accessories.json',ledger)
with (O/'optional-accessories.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(accessories[0]));writer.writeheader()
 for row in accessories:writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,list) else v for k,v in row.items()})
print('V338_HARDWARE_PASS',len(cat['hardware']), 'retired F60x4; optional ledger separate')
