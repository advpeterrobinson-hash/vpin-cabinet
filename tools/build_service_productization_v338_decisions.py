"""Explicit V33.8 engineering choices and limits. CERN-OHL-S-2.0."""
from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/service-productization-v338'
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def write(n,d):(O/n).write_text(json.dumps(d,indent=2)+'\n')
P=str(O.relative_to(R))+'/'
g=read(P+'geometry-validation.json');a=read(P+'adjustment-validation.json');k=read(P+'landing-study.json');c=read('config/service_productization_v338.json');prior=read('exports/generated/front-landings-v3363/load-screen.json')
assert g['pass'] and a['pass'] and k['pass']
assert c['adjustment']['final_safe_range_mm']==a['geometric_common_height_setup_window_mm']
assert c['retention']['selected_option']=='A'
# The same moving mass/COM, front/rear bearing locations, lever and screw group
# produce the same reaction demands. Material capacity is deliberately unknown.
net_area=70*54-4*math.pi*2.5**2
I=70*54**3/12-4*(math.pi*2.5**4/4+math.pi*2.5**2*18**2)
scenarios=[]
for row in prior['payload_scenarios']:
 q=dict(row);q.update(root_net_area_mm2=net_area,root_section_modulus_mm3=I/27,
  elastic_root_bending_stress_demand_MPa=row['factor2_body_wall_moment_Nm']*1000/(I/27),
  root_average_shear_demand_MPa=row['factor2_front_each_N']/net_area,
  contact_average_pressure_demand_MPa=row['factor2_front_each_N']/(math.pi*12**2))
 scenarios.append(q)
load={'status':'GEOMETRIC_LOAD_PATH_SCREEN_PASS; MATERIAL_CAPACITY_UNQUALIFIED','decision':'PROMOTE_SW02_DESIGN_CANDIDATE','grain':'Preferred X/68mm cantilever direction; no SW02 end-grain screw withdrawal credit','basis':'Exact unchanged M025, display, dowel, contacts, receiver, side-screw axes and embedment. SW02 eliminates two glue planes and four obsolete binders; it does not establish superior material strength.','same_root_net_section_as_original_mm2':net_area,'root_section_modulus_mm3':I/27,'section_method':'70x54 rectangle minus four longitudinal radius2.5 clearance bores at Z+9/+45. Root before adjuster/retention bores; simple beam demand only, not notch stress or allowable.','minimum_screw_axis_to_Y_edge_mm':9,'head_recess_to_Y_edge_mm':4.5,'side_screw_plywood_embedment_mm':12,'remaining_side_exterior_skin_mm':6,'functional_comparison':g['SW02'],'scenarios':scenarios,'strength_capacity':None,'not_certification':True,'material_qualification_holds':['dry stable straight knot-free species and grain selection','same-wood drilling coupon with clamped portable perpendicular guide','head bearing and splitting at9mm center-to-edge /4.5mm head ligament','side plywood12mm embedment cyclic shear/withdrawal; no wall friction credited','M8 insert pull-out and local splitting; M6 receiver in M025','whole assembly bounce/nudge, deflection and uplift qualification'],'source_sha256':{'native':g['native_sha256'],'prior_load_screen':sha('exports/generated/front-landings-v3363/load-screen.json')},'manufacturing_release':False}
write('SW02-load-screen.json',load)
ret={'selected_option':'A','selected_description':'Two existing captive M6x100 tool-operated threaded retainers','count':2,'tool_required':True,'positive_retention':'Metal threaded M025 receiver; nominal7mm engagement, reset6–8mm after setup; physical anti-loosening/nudge qualification still held','captivity':'Existing washer/jamnut stop and push-on shank retainer architecture retained; release10.5mm before opening','A':{'decision':'RETAIN_CURRENT','new_custom_metal':0,'access':'Existing110deg coin-door tool corridor passes against SW02; original mechanism and tools are unchanged'},'B':{'decision':'PACKAGING_PASS_NOT_PROMOTED','envelopes':k['hand_knob_candidates'],'operation':'Conservative finger sweep plus70x70x28mm palm via front/coin-door, each left/right independent; full10.5mm downward release included','reason':'No selected commodity M6x100 hand unit or positively retained long-bolt grip has demonstrated equal captivity/anti-release performance. A press-fit catalogue family or short-stud hand knob is not that proof.','needed':'Selected long-shank commodity knob/assembly, grip retention, no loose pieces, thread engagement and cyclic/nudge trial'},'C':{'decision':'REJECT_CURRENT_INTERFACE','reason':'Commercial ball-lock pin needs a compatible locking shoulder/bushing. The current blind threaded receiver has none; a plain pin in an M6 receiver is not positive retention. New bushing/receiver geometry would add complexity and remove protected receiver material.','viable_candidate':False,'final_sku':None},'normal_sequence':['Open coin door','Release both captive retainers with tool','Remove main playfield glass and matrix as required','Raise only using a defined and physically qualified primary support procedure; CURRENT primary50deg support remains unresolved'],'source_sha256':{'landing_study':sha(P+'landing-study.json'),'native':g['native_sha256']},'manufacturing_release':False}
write('retention-decision.json',ret)
sources={'license':'Original analysis CERN-OHL-S-2.0; external vendor/catalogue content is referenced, not copied into project CAD. No imported vendor mesh/drawing.','sources':[
 {'url':'https://www.elesa-ganter.com/siteassets/PDF/EN/GN%207336.pdf','authority':'Manufacturer catalogue','supports':'Nominal hand-knob family reference. M6 diameter34/head21 example; this does not prove100mm stud availability.','status':'REFERENCE_NOT_PURCHASED'},
 {'url':'https://www.elesa.com/static/sfogliabili/files/QuickCatalogue_ENG_monza_web.pdf','authority':'Manufacturer catalogue','supports':'MDA/MCT fluted grip families accepting pressed hex bolts/nuts. No selected product or captive-grip safety qualification.','status':'REFERENCE_NOT_PURCHASED'},
 {'url':'https://www.elesa-ganter.com/en/www/Indexing-elements--Stainless-Steel-Ball-lock-pins--GN1133','authority':'Manufacturer product page','supports':'Push-button ball-lock architecture requires suitable mating capture; not compatible by assumption with blind M6 thread.','status':'REFERENCE_NOT_PURCHASED'},
 {'url':'https://www.elesa.com/siteassets/PDF/PDF_EN/GN%201140.pdf','authority':'Manufacturer catalogue','supports':'Matching holding-bushing concept; not selected or added to CURRENT.','status':'REFERENCE_NOT_PURCHASED'},
 {'url':'https://research.fs.usda.gov/fpl/wood-handbook','authority':'USDA Forest Products Laboratory','supports':'Wood orthotropy, grain/material dependence and fastener qualification. Orientation rationale is engineering inference, no material capacity inferred.','status':'GENERAL_MATERIAL_REFERENCE'},
 {'url':'https://research.fs.usda.gov/download/treesearch/62244.pdf','authority':'USDA chapter5','supports':'Mechanical-property/grain variability; no species allowable selected.','status':'GENERAL_MATERIAL_REFERENCE'},
 {'url':'https://research.fs.usda.gov/treesearch/62253','authority':'USDA chapter8','supports':'Joint grain/moisture/fastening dependence; physical qualification remains held.','status':'GENERAL_MATERIAL_REFERENCE'}]}
write('landing-sources.json',sources)
print('V338_DECISIONS_PASS',len(scenarios),'load scenarios; retentionA; geometric setup window',c['adjustment']['final_safe_range_mm'])
