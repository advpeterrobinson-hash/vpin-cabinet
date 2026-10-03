"""Independent inventory, print, packaging and immutable-source checks. CERN-OHL-S-2.0."""
from pathlib import Path
import json,subprocess,hashlib,collections,zipfile,xml.etree.ElementTree as ET,math,gzip
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/solid-leg-v334';checks=[]
read=lambda f:json.loads((R/f).read_text())
def ck(v,n):
 checks.append({'name':n,'pass':bool(v)})
 assert v,n
old=read('exports/generated/flatpack-v331/manufacturing-register.json');new=read('exports/generated/solid-leg-v334/manufacturing-register.json');legs={'P029','P030','P031','P032'}
cnc=[p for p in new['parts'] if p['assembly_id'] not in legs];solid=[p for p in new['parts'] if p['assembly_id'] in legs]
ck(len(cnc)==102 and len(solid)==4 and len(new['families'])==62,'102 unchanged CNC pieces +4 SW01 /62 families')
ck(cnc==[p for p in old['parts'] if p['assembly_id'] not in legs],'All unrelated manufacturing members identical')
ck(all(p['manufacturing_part_id']=='SW01' and p['nominal_stock_thickness_mm'] is None and not p['CNC_required'] for p in solid),'Solid wood never misclassified as plywood')
ck(not new['manufacturing_release'],'No release')
for row in read('exports/generated/solid-leg-v334/metrology.json'):
 ck(row['old_lamination_union_difference_mm3']<1e-3 and row['original_difference_mm3']<1e-3,'Union and accepted B-rep identical '+row['side'])
 ck(row['raw_square_stock_mm']==[54,54,126] and abs(row['triangular_blank_volume_mm3']-183708)<1e-6,'Triangular shop blank '+row['side'])
jig=read('exports/generated/solid-leg-v334/jig-validation.json')
for row in jig['rows']:
 ck(max(row['axis_error_mm'])<1e-6 and row['angle_reference_error_deg']==0,'Reference bore positions/direction '+row['side'])
 ck(not row['early_assembly_interferences'] and row['wood_interferences'],'Early-only tool access, assembled conflict exposed '+row['side'])
 ck(not row['tooling_pair_penetrations'],'No tooling self-intersection '+row['side'])
 ck(max(row['registration_distances'].values())<1e-5,'Two datum contact '+row['side'])
ck(not jig['physical_accuracy_validated'] and not jig['drilling_released'],'Print and hardware physical hold')
# Check printable3MF topology independently, compare tessellated vs exact volume.
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
vols=read('exports/generated/solid-leg-v334/print-solid-checks.json')
for f in O.glob('*-REFERENCE.3mf'):
 with zipfile.ZipFile(f) as z:root=ET.fromstring(z.read('3D/3dmodel.model'))
 vertices=[tuple(float(v.attrib[k]) for k in ('x','y','z')) for v in root.findall('.//m:vertex',ns)]
 triangles=[tuple(int(t.attrib[k]) for k in ('v1','v2','v3')) for t in root.findall('.//m:triangle',ns)]
 edges=collections.Counter(tuple(sorted((t[i],t[(i+1)%3]))) for t in triangles for i in range(3))
 ck(all(c==2 for c in edges.values()),'Watertight3MF '+f.name)
 ck(abs(min(v[2] for v in vertices))<1e-5,'Print bed orientation '+f.name)
 volume=0
 for ia,ib,ic in triangles:
  a,b,c=[vertices[i] for i in (ia,ib,ic)];volume+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
 key=f.name.split('-REFERENCE')[0];ck(abs(abs(volume)/vols[key]['volume_mm3']-1)<.01,'Print volume within1% tessellation '+f.name)
# No shop parts remain in nesting. Border/spacing pair checks remain conservative.
material=read('exports/generated/solid-leg-v334/material-utilization.json');allids=[]
for sheet in material['sheets']:
 a=sheet['placements'];allids += [p['instance_id'] for p in a]
 for p in a:ck(p['x']>=20-1e-5 and p['y']>=20-1e-5 and p['x']+p['w']<=2480+1e-5 and p['y']+p['h']<=1580+1e-5,'Sheet border '+p['instance_id'])
 for i,p in enumerate(a):
  for q in a[i+1:]:
   ck(p['x']+p['w']+15<=q['x']+1e-5 or q['x']+q['w']+15<=p['x']+1e-5 or p['y']+p['h']+15<=q['y']+1e-5 or q['y']+q['h']+15<=p['y']+1e-5,'15mm spacing '+p['instance_id']+'/'+q['instance_id'])
ck(sorted(allids)==sorted(p['instance_id'] for p in cnc),'Exactly102 CNC members nested, no solid blocks')
packing=read('exports/generated/solid-leg-v334/packaging.json');by={p['instance_id']:p for p in new['parts']}
for c in packing['candidates']:
 ids=[]
 for b in c['bundles']:
  ck(b['gross_high_density_kg']<=c['target_kg']+1e-6,'Package high-density target '+b['id'])
  total=0
  for l in b['layers']:
   for p in l['pieces']:
    ids.append(p['instance_id']);q=by[p['instance_id']];w,h=sorted(q['finished_xy_size_mm'],reverse=True)
    ck(abs(l['t']-q['finished_reference_thickness_mm'])<1e-5 and p['x']+w<=b['L']+1e-5 and p['y']+h<=b['W']+1e-5,'Packing extent '+b['id']+'/'+p['instance_id']);total+=p['mass_kg']
  ck(abs(total-b['wood_mass_kg'])<1e-7,'Packing mass '+b['id'])
 ck(sorted(ids)==sorted(by),'All106 pieces once in '+str(c['target_kg'])+'kg proposal')
mass=read('exports/generated/solid-leg-v334/mass-budget.json');oldmass=read('exports/generated/assembly-v333/mass-budget.json')
ck(abs(mass['installed_wood_kg'][1]-oldmass['wood_flatpack_kg'][1])<1e-7,'Equal density preserves installed mass')
ck(mass['wood_flatpack_kg'][1]>mass['installed_wood_kg'][1],'Shipping blank mass not confused with drilled mass')
ck(mass['known_measured_hardware_mass_kg'] is None and mass['unknown_hardware_items'],'Unknown hardware never zeroed')
manual=read('exports/generated/solid-leg-v334/assembly-manual.json');steps=[st for s in manual['stages'] for st in s['steps']]
ck(len(steps)==31 and len(manual['part_preparation'])==102,'31-step manual +102 untouched CNC prep cards +4 shop cards')
ck(any(s['id']=='02.0' for s in steps) and not any(s['id']=='16.1' for s in steps),'Earlier drill checkpoint replaces glue-up')
ck(not any('-L1' in str(s) and 'P029' in str(s) for s in steps),'No retired leg layers in manual steps')
# Hash every protected historical engineering/configuration asset, not just volumes.
HEAD=read('config/solid_leg_blocks_v334.json')['head_before'];protected=[]
for name in subprocess.check_output(['git','ls-tree','-r','--name-only',HEAD],cwd=R,text=True).splitlines():
 if name.startswith(('config/','cad/','library/','exports/generated/flatpack-v331/','exports/generated/hardware-v33/','exports/generated/backbox-lock-integration-v32/')):
  f=R/name
  if not f.is_file():continue
  expected=subprocess.check_output(['git','rev-parse',HEAD+':'+name],cwd=R,text=True).strip();actual=subprocess.check_output(['git','hash-object',str(f)],cwd=R,text=True).strip();ck(actual==expected,'Unchanged '+name);protected.append({'path':name,'git_blob':actual})
vr=read('exports/generated/solid-leg-v334/viewer-regression.json')
ck(vr['all_installed_geometry_and_state_ids_unchanged'] and vr['geometry_dictionary_unchanged'] and vr['CNC_manufacturing_meshes_unchanged'],'Viewer CURRENT geometry and other detailed meshes unchanged')
report={'pass':True,'head_before':HEAD,'checks':checks,'protected_files':protected,'manufacturing_release':False,'physical_drilling_qualified':False,'counts':dict(collections.Counter(p['manufacturing_status'] for p in new['parts']))}
(O/'engineering-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('V334_ENGINEERING_PASS',len(checks),report['counts'])
