"""Independent conservation, containment and authority checks. CERN-OHL-S-2.0."""
from pathlib import Path
import json,math,hashlib,subprocess,gzip
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/assembly-v333'
read=lambda n:json.loads((O/n).read_text());checks=[]
def check(ok,name):
 checks.append({'name':name,'pass':bool(ok)})
 assert ok,name
p=json.loads((R/'exports/generated/flatpack-v331/manufacturing-register.json').read_text())['parts'];ids={q['instance_id'] for q in p};byid={q['instance_id']:q for q in p}
metrics=read('brep-metrics.json');mass=read('mass-budget.json');materials=read('material-utilization.json');pack=read('packaging.json');hw=read('hardware-dashboard.json')
check(len(ids)==len(p)==130,'130 unique manufacturing pieces');check(len({q['manufacturing_part_id'] for q in p})==66,'66 canonical families')
check(abs(sum(q['volume_mm3'] for q in p)-mass['wood_volume_mm3'])<1e-4,'Mass uses actual authoritative B-rep volumes')
check(all(abs(q['volume_mm3']-byid[q['instance_id']]['volume_mm3'])<1e-4 for q in metrics),'Independent B-rep volume extraction matches register')
for s in materials['stocks']:
 area=s['hold_down_area_mm2']+s['spacing_reserved_area_mm2']+s['bounding_rectangle_contour_loss_mm2']+s['cutout_area_mm2']+s['projected_material_area_mm2']+s['reusable_rectangular_offcut_area_mm2']+s['small_unallocated_area_mm2']
 check(abs(area-s['purchased_full_sheet_area_mm2'])<1e-4,'Area conservation '+str(s['thickness_mm']))
 check(abs(s['waste_percent_gross_including_offcuts']+s['utilization_percent_net']-100)<1e-8,'Utilization + gross waste100 '+str(s['thickness_mm']))
for sh in materials['sheets']:
 for i,a in enumerate(sh['placements']):
  check(a['x']>=20 and a['y']>=20 and a['x']+a['w']<=2480+1e-6 and a['y']+a['h']<=1580+1e-6,'Sheet border '+a['instance_id'])
  for b in sh['placements'][i+1:]:
   dx=max(0,a['x']-b['x']-b['w'],b['x']-a['x']-a['w']);dy=max(0,a['y']-b['y']-b['h'],b['y']-a['y']-a['h'])
   check(math.hypot(dx,dy)>=15-1e-6,'15mm sheet separation '+a['instance_id']+'/'+b['instance_id'])
check({a['instance_id'] for sh in materials['sheets'] for a in sh['placements']}==ids,'Nesting contains all130')
for s in materials['stocks']:
 if 'practical_small_stock_layout' not in s:continue
 L,W=s['practical_stock_rectangles_mm'][0];a=s['practical_small_stock_layout']['placements']
 check({q['instance_id'] for q in a}=={q['instance_id'] for q in p if q['nominal_stock_thickness_mm']==s['thickness_mm']},'Small-stock inventory '+str(s['thickness_mm']))
 check(all(q['x']>=20 and q['y']>=20 and q['x']+q['w']<=L-20 and q['y']+q['h']<=W-20 for q in a),'Small stock border '+str(s['thickness_mm']))
for c in pack['candidates']:
 seen=[];woodmass=0
 for b in c['bundles']:
  check(b['gross_high_density_kg']<=c['target_kg']+1e-6,'High-density package mass cap '+b['id'])
  check(all(0<=x<=b['external_LWH_mm'][i] for i,x in enumerate(b['wood_center_of_gravity_mm'])),'CG within package '+b['id'])
  woodmass+=b['wood_mass_kg']
  for l in b['layers']:
   for i,a in enumerate(l['pieces']):
    seen.append(a['instance_id']);w,h=sorted(byid[a['instance_id']]['finished_xy_size_mm'],reverse=True)
    check(a['x']>=0 and a['y']>=0 and a['x']+w<=b['L']+1e-6 and a['y']+h<=b['W']+1e-6,'Package footprint '+b['id']+'/'+a['instance_id'])
    for other in l['pieces'][i+1:]:
     w2,h2=sorted(byid[other['instance_id']]['finished_xy_size_mm'],reverse=True)
     dx=max(0,a['x']-other['x']-w2,other['x']-a['x']-w);dy=max(0,a['y']-other['y']-h2,other['y']-a['y']-h)
     check(math.hypot(dx,dy)>=5-1e-6,'Packing layer separation '+a['instance_id']+'/'+other['instance_id'])
 check(len(seen)==len(set(seen))==130 and set(seen)==ids,'All130 once in target '+str(c['target_kg']))
 check(abs(woodmass-mass['wood_flatpack_kg'][1])<1e-8,'Pack wood mass conservation '+str(c['target_kg']))
check(mass['mechanical_exact_total_kg'] is None and mass['known_measured_hardware_mass_kg'] is None,'Unknown mass never zero')
check(hw['known_required_Fxx_minimum']==160 and len(hw['formula_driven_Fxx'])==5 and len(hw['TBD_Fxx'])==6,'Known minimum +5formula +6TBD preserved')
anim=read('animations.json');check(sum(c['type']=='assembly' for c in anim['clips'])==31,'31 schematic assembly clips');check(sum(c['type']=='service' for c in anim['clips'])==11,'11 service clips');check(sum(c['type']=='packing' for c in anim['clips'])==2,'2 packing clips')
check(all(c['status']=='SCHEMATIC_ASSEMBLY_ANIMATION' for c in anim['clips'] if c['type']=='assembly'),'No unvalidated assembly-motion claim')
audit=read('assembly-validation.json');check(len(audit['steps'])==31 and all(s['dependency_order']=='PASS' for s in audit['steps']),'All31 dependency checks');check(len(read('insertion-screens.json')['parts'])==130,'130 real-piece insertion screens')
protection=read('geometry-protection.json')
for q in protection['unchanged_files']:
 actual=subprocess.check_output(['git','hash-object',str(R/q['path'])],cwd=R,text=True).strip();check(actual==q['git_blob'],'Unchanged '+q['path'])
# V33.2 geometry payload is embedded verbatim in the new viewer. New motion uses
# Object3D transforms only; manufactured geometry remains untouched.
import re,base64
viewer=R/'exports/generated/viewer-v32/index.html';html=viewer.read_text();embedded=re.search(r'<script id="viewer-data" type="application/octet-stream">(.*?)</script>',html).group(1)
check(base64.b64decode(embedded)==(R/'exports/generated/viewer-v332/viewer-data.json.gz').read_bytes(),'Original entire installed/detailed geometry payload byte identical')
browser=read('browser-validation.json');digest=hashlib.sha256(viewer.read_bytes()).hexdigest();check(browser['pass'] and browser['viewer_sha256']==digest,'Current offline/touch proof matches HTML')
legacy=read('legacy-browser-validation.json');check(legacy['pass'] and legacy['viewer_sha256']==digest,'Existing53viewer regressions pass current HTML')
source=json.loads((R/'config/current_v32.json').read_text())['geometry_directory']+'/mesh.json'
report={'pass':True,'checks':checks,'viewer_sha256':digest,'source_mesh_sha256':hashlib.sha256((R/source).read_bytes()).hexdigest(),'geometry_changed':False,'manufacturing_release':False,'source_head':protection['head_before']}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('V333_METRICS_PASS',len(checks))
