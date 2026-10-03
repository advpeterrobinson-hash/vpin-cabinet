"""Closed support architecture gate; physical/CNC qualification remains held.
Original CERN-OHL-S-2.0. Geometry, motion, access and load evidence are separate.
"""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/front-landings-v3363'
def read(n):return json.loads((O/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
C=json.loads((R/'config/front_landings_v3363.json').read_text());g=read('geometry-validation.json');m=read('motion-validation.json');a=read('tool-access.json');l=read('load-screen.json');h=read('internal-hardware-validation.json')
checks=[]
def ck(n,v):checks.append({'name':n,'pass':bool(v)});assert v,n
native=sha(O/'play.FCStd')
ck('exact native geometry valid',g['pass'] and all(q['pass'] for q in g['checks']))
ck('all previous wood hardware and datums preserved',g['current_shapes_changed']==[])
ck('distinct purchased hardware clears both engaged and released',h['pass'] and h['source_sha256']==native and all(q['pass'] for q in h['checks']))
ck('two full intentional front contacts',len(g['contacts'])==2 and all(q['area_mm2']>450 and q['base_penetration_mm3']<1e-5 and q['outer_edge_gap_mm']>=9.99 for q in g['contacts']))
ck('direct full-strength side attachment exists',g['side_attachment']['quantity']==8 and g['side_attachment']['remaining_exterior_skin_mm']>=6 and g['side_attachment']['row_separation_mm']==36)
ck('earliest passing simple-body search retains5mm reserve',g['selected']['pad_y_mm']==245 and all(q['distance_mm']>=5-1e-7 for q in g['selected']['nearby_obstacles']))
ck('positive threaded closed retention geometry',6<=g['retention']['engagement_mm']<=8 and g['retention']['jamnut_washer_stack_mm']<g['retention']['nominal_body_to_underhead_gap_mm'])
ck('receiver blind skin and release reserve',g['retention']['minimum_nominal_skin_vertical_mm']>=6 and g['retention']['release_mm']>g['retention']['engagement_mm'])
ck('continuous service lift and rear-seating plus fold pass',m['pass'] and all(q['pass'] for q in m['checks']))
ck('motion tied to exact current native',m['source_sha256'][str((O/'play.FCStd').relative_to(R))]==native)
ck('both retention and adjustment physically sized approach envelopes pass',a['pass'] and len(a['operations'])==4 and not a['preliminary_without_new_supports'] and all(q['minimum_clearance_mm']>=2-1e-6 for q in a['operations'].values()))
ck('access tied to exact current native',a['source_sha256']==native)
ck('eight side attachment driver paths clear with module removed',len(a['side_attachment_access'])==8 and all(q['pass'] for q in a['side_attachment_access'].values()))
ck('nine mass sensitivity cases retain positive front and rear reactions',l['pass'] and len(l['payload_scenarios'])==9)
ck('load evidence tied to unchanged original geometry',l['source_sha256']==sha(R/l['source'])==g['source_sha256'])
ck('front overhang reduced without relocating accepted geometry',l['relative_front_vs_T1']['uniform_moment']<.34 and l['relative_front_vs_T1']['uniform_deflection_tendency_same_EI']<.12)
ck('normal pose fixed;adjuster travel not arbitrary pitch change',C['landing']['selected_adjustment_plus_minus_mm']==3 and not g['adjustment']['5']['stack_pass'] and 'adjustment_rule' in m)
ck('no final holes released',not C['manufacturing_release'] and C['measured_thickness_mm'] is None and C['selected_coupon_clearance_mm'] is None and C['retention']['existing_M025_and_side_shapes_unchanged'])
out={'version':'V33.6.3','architecture_pass':True,'status':'PASS','closed_position_support_valid':True,'closed_position_support_status':'PASS_NOMINAL_DESIGN_ARCHITECTURE',
 'source':str((O/'play.FCStd').relative_to(R)),'source_sha256':native,'native_sha256':native,'checks':checks,
 'authority':'DESIGN_ARCHITECTURE_ONLY_NOT_MANUFACTURING_OR_STRUCTURAL_CERTIFICATION',
 'load_path':{'rear':'base/straps → wooden dowel → existing cradles → cabinet floor','front':'base → two articulated adjustable pads → laminated side bodies → eight positive side screws / side bearing → full cabinet sides → cabinet/floor/legs'},
 'intentional_supports':['rear dowel/cradle pair','FrontLandingL_ContactPad','FrontLandingR_ContactPad'],
 'crossmembers':'T1/T2/T3 are structural cabinet crossmembers;22mm nominal gap is intentional. They do not carry closed playfield weight.',
 'retention':'Two captive M6 threaded clamps. Release/retract10.5mm through open front coin door before service/lift; no support-body or electronics removal. Commodity thin jamnut stops are set after leveling to7mm receiver engagement.',
 'adjustment_rule':'±3mm hardware travel compensates stock/assembly tolerance ONLY to reproduce9.906669deg nominal pose with left/right level and rear dowel fully seated. Lowering the complete pose3mm collides with button envelopes and is forbidden. No opposed-adjuster twist.',
 'hardware_uncertainty':['M8 articulated pad has to remain captive and accommodate>=10deg','M6×100 fully-threaded bolt +thin jamnuts/washer stack','thread-compatible push-on captive retainer; no custom groove','M6 receiver pilot/depth and rigid drill guide for vertical bore in sloped M025','side screw12mm embedment and layer fastening'],
 'physical_qualification_required':True,'manufacturing_release':False,'manufacturing_ready':False,
 'pending':['actual production plywood thickness','actual display and adapters','physical coupon and selected clearances','all new purchased hardware and captive-stack dimensions','rigid receiver drilling guide/depth-stop validation','side anchorage/receiver pull-out, whole-board stiffness and cyclic load tests'],
 'evidence_sha256':{n:sha(O/n) for n in ['geometry-validation.json','motion-validation.json','tool-access.json','load-screen.json','internal-hardware-validation.json']}}
(O/'support-validation.json').write_text(json.dumps(out,indent=2)+'\n');print('V3363_CLOSED_SUPPORT_ARCHITECTURE_PASS',len(checks),'CNC BLOCKED; physical qualification required')
