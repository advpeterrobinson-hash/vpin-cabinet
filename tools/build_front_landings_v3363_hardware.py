"""Append-only V33.6.3 commodity landing hardware. CERN-OHL-S-2.0.
No vendor CAD imported; geometry is an original packaging envelope. The exact
counts describe selected interfaces, not measured or manufacturing-frozen SKUs.
"""
from pathlib import Path
import json,copy,hashlib,csv
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/front-landings-v3363'
def read(p):return json.loads((R/p).read_text())
def dump(p,v):(R/p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
C=read('config/front_landings_v3363.json');G=read(str(O.relative_to(R))+'/geometry-validation.json')
assert G['pass'];assert not G['manufacturing_release']
cat=read('config/hardware_catalog_v335.json');old=copy.deepcopy(cat['hardware']);assert len(old)==151
prefix='exports/generated/front-landings-v3363/'
family_sources={
 'M8_FOOT':[
  'https://www.essentracomponents.com.br/set-ap/Catalogo_Master_Brasil.pdf',
  'https://www.elierre.com.br/p-pe-nivelador-m8-247'],
 'M6_RECEIVER':['https://www.bigfer.com.br/bucha-bigfer/',
  'https://portal.bigfer.com.br/index.php?keyword=M6&route=product%2Fsearch',
  'https://jomarcakits.com.br/blog/source/Catalogo.pdf'],
 'M8_INSERT':['https://renametalurgica.com.br/produtos/porca-garra'],
 'METRIC_FASTENER':['https://www.ciser.com.br/'],
 'CAPTIVE_RETAINER':['https://parts.cat.com/en/catcorp/product/201-5493']}
specs=[
 ('F59','Landing-to-side wood screw','Parafuso do apoio para a lateral',8,['SideScrew1','SideScrew2','SideScrew3','SideScrew4'],{'nominal_diameter_mm':4.5,'underhead_reference_mm':80,'side_engagement_reference_mm':12},'wood screw drive, hardware-dependent','METRIC_FASTENER'),
 ('F60','Landing lamination wood screw','Parafuso das lâminas do apoio',4,['LaminationScrew1','LaminationScrew2'],{'nominal_diameter_mm':4.5,'underhead_reference_mm':50},'wood screw drive, hardware-dependent','METRIC_FASTENER'),
 ('F61','Captive closed-playfield retention hex bolt, M6 family','Parafuso sextavado cativo de retenção do playfield, família M6',2,['RetentionBolt'],{'thread_family':'M6','underhead_reference_mm':100,'nominal_engagement_mm':7,'release_drop_reference_mm':C['retention']['release_drop_mm']},'compact 10 mm spanner reference; actual head measured','METRIC_FASTENER'),
 ('H27','M8 articulated landing foot with replaceable contact pad','Pé articulado M8 do apoio com contato substituível',2,['AdjusterStem','SwivelJoint','SwivelDisc','ContactPad'],{'thread_family':'M8','contact_diameter_reference_mm':24,'contact_thickness_reference_mm':3,'minimum_articulation_required_deg':10,'adjustment_plus_minus_mm':3,'stem_length_config_reference_mm':C['landing']['adjuster_stem_length_reference_mm']},'selected foot adjustment tool','M8_FOOT'),
 ('I15','M8 metal landing receiver insert','Inserto metálico M8 do apoio',2,['AdjusterInsert'],{'thread_family':'M8','outer_diameter_reference_mm':12,'length_reference_mm':16},'purchased insert driver and qualified depth stop','M8_INSERT'),
 ('I16','M8 adjuster locknut','Contraporca M8 do regulador',2,['AdjusterLocknut'],{'thread_family':'M8','thickness_reference_mm':6.5},'13 mm spanner reference; verify purchased nut','METRIC_FASTENER'),
 ('I17','Blind-installed M6 metal retention receiver','Inserto metálico M6 de retenção em furo cego',2,['RetentionReceiver'],{'thread_family':'M6','outer_diameter_reference_mm':10,'length_reference_mm':10,'maximum_reference_blind_bore_depth_mm':C['retention']['maximum_blind_drill_depth_mm']},'qualified rigid angled drill guide, depth stop, purchased insert driver','M6_RECEIVER'),
 ('I18','M6 thin jam nut for retention stop stack','Contraporca fina M6 para batente de retenção',4,['RetentionJamnut1','RetentionJamnut2'],{'thread_family':'M6','thickness_reference_mm':3.2},'two compact 10 mm spanners reference','METRIC_FASTENER'),
 ('W11','M8 landing adjuster washer','Arruela M8 do regulador do apoio',2,['AdjusterWasher'],{'thread_family':'M8','outer_diameter_reference_mm':16,'thickness_reference_mm':1.6},'none','METRIC_FASTENER'),
 ('W12','M6 retention bearing washer','Arruela M6 de apoio da retenção',2,['RetentionWasher'],{'thread_family':'M6','outer_diameter_reference_mm':14,'thickness_reference_mm':1.6},'none','METRIC_FASTENER'),
 ('B17','M6-family captive push-on retaining ring','Anel de retenção cativo tipo pressão para família M6',2,['RetentionPushRing'],{'shaft_family':'M6','outer_diameter_reference_mm':9,'thickness_reference_mm':1},'purchased retaining-ring installer; removal method hardware-dependent','CAPTIVE_RETAINER')]
props=G['part_properties'];mapping={};new=[]
for id,en,pt,qty,suffixes,dims,tool,src in specs:
 instances=[]
 for side in 'LR':
  for suffix in suffixes:
   name=f'FrontLanding{side}_{suffix}';assert name in props,name
   b=props[name]['bounds_mm']
   if isinstance(b,dict):raise AssertionError('Unexpected bounds schema')
   # Native bbox format: [xmin,ymin,zmin,xmax,ymax,zmax]. Coordinates are
   # visualization centers only; explicit native service axes govern drilling.
   center=[(b[i]+b[i+3])/2 for i in range(3)]
   direction=[-1,0,0] if suffix.startswith('SideScrew') and side=='L' else [1,0,0] if suffix.startswith('SideScrew') else [0,0,-1] if suffix.startswith('LaminationScrew') or id in ('H27','I15','I16','W11','B17') else [0,0,1]
   instances.append({'object':name,'coordinate_xyz_mm':center,'coordinate_meaning':'nominal B-rep envelope center; not a drill-center release','installation_direction':direction,'direction_status':'SCHEMATIC_PACKAGING_DIRECTION_HARDWARE_PENDING','source':prefix+'play.FCStd','mirrored_pair':True,'logical_assembly_instance':side})
   mapping[name]=id
 h={'id':id,'description_en':en,'description_pt_BR':pt,'flatpack_classification':'REQUIRED_FLATPACK_HARDWARE',
  'assembly_stage':'05','parent_assembly':'playfield_landings','quantity':qty,'quantity_status':'EXACT_FROM_DESIGN_INTERFACES_HARDWARE_PROVISIONAL',
  'unit':'piece','material':'steel / selected finish' if id!='H27' else 'steel stem, articulated polymer/metal pad, replaceable resilient contact; actual materials pending',
  'nominal_dimensions':dims,'dimensional_authority':'PROVISIONAL_PACKAGING_REFERENCE_NOT_PURCHASED',
  'freeze_status':'PURCHASE_BEFORE_CNC','design_status':'PROVISIONAL','measurement_required':True,'controls_permanent_cnc':True,
  'source':['config/front_landings_v3363.json',prefix+'geometry-validation.json']+family_sources[src],
  'source_license':'CERN-OHL-S-2.0 original envelope; external links are citations only, no vendor CAD copied',
  'supplier':None,'price_BRL':None,'notes':'Exact architectural count; purchased dimensions, material/grade, fit and physical load qualification remain HOLD. No final bores or thread substitution authorized.',
  'instances':instances,'model':{'strategy':'REFERENCE_ENVELOPE_ONLY','kind':'original simplified B-rep','path':prefix+'play.FCStd','detailed_threads':False},
  'service_removable':True,'normal_assembly_removable':True,'tool_family':tool,'installed_coordinate_status':'REFERENCE_ENVELOPE_CENTER',
  'measurement_fields':{'actual_dimensions_mm':None,'selected_manufacturer_part':None,'thread_standard_and_pitch':None,
   'drive_and_size':None,'mount_pattern_and_count':None,'installed_stack_and_engagement_mm':None,'material_grade':None,'physical_fit_approved':False}}
 if id=='H27':
  h['notes']+=' Stem/joint/disc/pad are visual subparts of TWO purchased foot assemblies, not eight purchased parts. Require captive articulation ≥10° in this inverted support orientation and include contact thickness in stack; purchased foot load rating and inverted suitability unqualified. ±3 mm is installation/stock compensation around the unchanged CURRENT pose, not permission to change the playing angle; whole-pose range extremes are not validated.'
  h['nominal_dimensions']['modeled_stem_cylinder_length_mm']=props['FrontLandingL_AdjusterStem']['bounds_mm'][5]-props['FrontLandingL_AdjusterStem']['bounds_mm'][2]
  h['measurement_fields'].update(articulation_degrees=None,captive_inverted_operation_approved=False,contact_compression_mm=None,adjustment_engagement_at_both_limits_mm=None)
 if id=='I17':
  h['notes']+=' Blind describes the wood bore, not necessarily a closed-end insert. Two vertical-world receivers enter the inclined M025 underside; rigid angled drill guide and depth-stop coupon are mandatory. M025 reference B-rep has no released receiver holes.'
  h['measurement_fields'].update(pilot_diameter_mm=None,blind_axial_depth_mm=None,drill_point_allowance_mm=None,remaining_top_skin_mm=None,pullout_test_approved=False)
 if id=='B17':h['notes']+=' Primary source is a mechanism example for M5, NOT selected M6 hardware or verified Brazilian stock. Qualify push-on retention on selected fully threaded M6 bolt, drop travel and removal/reuse; do not assume a smooth shaft or custom groove.'
 if id=='F59':h['notes']+=' Four per support; 12 mm nominal side engagement leaves 6 mm nominal skin. Actual plywood, screw/head and pilot must prevent exterior breakthrough.'
 if id=='F61':h['notes']+=' TOOL OPERATED, not hand-knob operated. Two thin jam nuts plus washer set engagement; captivity is a separate B17 part. No custom metal.'
 new.append(h)
cat.update(version='V33.6.3',source_head='349f0375c78f7308e5912d389b606d26d51f4b80',manufacturing_ready=False)
cat['hardware']=old+new;cat['object_to_id'].update(mapping)
assert cat['hardware'][:151]==old and len(cat['hardware'])==162
cat['v3363_authority']={'previous_catalog':'config/hardware_catalog_v335.json','append_only_ids':[x['id'] for x in new],
 'source_native_sha256':hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest(),'quantity_rule':'Exact new interface counts; no old TBD/formulas changed','custom_metal_added':0}
dump('config/hardware_catalog_v3363.json',cat)
closure=read('exports/generated/structural-v335/hardware-quantity-closure.json');closure['version']='V33.6.3'
closure['rows'] += [{'id':h['id'],'classification':'EXACT_FROM_DESIGN','quantity':h['quantity'],'source':'config/front_landings_v3363.json','hardware_status':'PURCHASE_BEFORE_CNC'} for h in new]
dump(prefix+'hardware-quantity-closure.json',closure);dump(prefix+'landing-hardware-map.json',mapping)
dump(prefix+'landing-hardware-bom.json',{'version':'V33.6.3','manufacturing_release':False,'hardware':new,'existing_catalog_entries_unchanged':151})
with (O/'landing-hardware-bom.csv').open('w') as f:
 keys=['id','description_en','description_pt_BR','quantity','unit','freeze_status','notes'];w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({k:h[k] for k in keys} for h in new)
lines=['# V33.6.3 landing hardware sources','','All links are manufacturer/family evidence. No exact SKU is selected; no vendor CAD is imported. Current quantity is architectural; dimensions and load performance remain PURCHASE_BEFORE_CNC.','']
for key,urls in family_sources.items():
 lines+=['## '+key,'']+['- '+u for u in urls]+['']
lines+=['## Scope and negative controls','','The Essentra Brazil catalog demonstrates commodity articulated and M8 foot families. Articulation angles apply only to the identified manufacturer family, not every compact foot. The selected original envelope requires at least 10° articulation and captive inverted operation, both to verify physically.','','Bigfer/Jomarca establish M6 wood-insert families; they do not certify a 10 mm blind receiver in this plywood. Porca-garra M8 and screw-in inserts are not interchangeable without fit review. The blind receiver requires a qualified angled drill guide and depth-stop coupon.','','No current price, supplier stock, structural capacity or CNC drilling release is asserted. Generic Ciser catalog identity is procurement direction only; exact fastener dimensions are provisional config values, not claimed selected manufacturer specifications.']
(O/'hardware-sources.md').write_text('\n'.join(lines)+'\n')
status=['# V33.6.3 hardware status','','All eleven new families remain **PURCHASE_BEFORE_CNC**. No purchased SKU is selected. Existing151 catalog rows and their unknown quantities remain unchanged.','','| ID | Qty | Family | Status |','|---|---:|---|---|']
status += [f"| {h['id']} | {h['quantity']} | {h['description_en']} | {h['freeze_status']} |" for h in new]
status += ['','The two H27 foot assemblies each include four visual subparts; do not buy/count eight assemblies. All new hardware mass remains UNKNOWN.','','Mandatory qualification: foot articulation/captivity in inverted use; M8 receiver/pilot and thread engagement; side-screw embedment/no breakout; M6 fully threaded bolt/stop-stack travel; thread-compatible captive ring; blind receiver pull-out, oblique rigid drill guide, drill-point depth and intact top skin. ±3 mm is tolerance compensation around CURRENT, not a qualified playing-angle change.','','Each landing is laminated with glue and two screws. Attach it to the cabinet side with four screws and no glue, preserving replacement.','','Original envelopes are CERN-OHL-S-2.0; cited external sources keep their copyright. No vendor CAD is copied. See hardware-sources.md.']
(O/'hardware-status.md').write_text('\n'.join(status)+'\n')
print('V3363_HARDWARE_PASS' ,len(cat['hardware']),len(new),sum(h['quantity'] for h in new if h['id'].startswith('F')))
