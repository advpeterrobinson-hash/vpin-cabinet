"""Current V33.5 promotion and protected-baseline regression. CERN-OHL-S-2.0."""
from pathlib import Path
import json,gzip,hashlib,subprocess,collections,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/structural-v335';checks=[]
def read(p):return json.loads((R/p).read_text())
def check(n,v,d=None):checks.append({'name':n,'pass':bool(v),'detail':d});assert v,(n,d)
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
C=read('config/structural_simplification_v335.json');reg=read('exports/generated/structural-v335/manufacturing-register.json');old=read('exports/generated/solid-leg-v334/manufacturing-register.json');v=read('exports/generated/structural-v335/geometry-validation.json');m=read('exports/generated/structural-v335/motion-validation.json')
check('all native geometry checks pass',v['pass'] and all(x['pass'] for x in v['checks']))
check('all differential service checks pass',m['pass'] and all(x['pass'] for x in m['checks']))
check('authorized wood differences only',{p['name'] for p in v['changed']}=={'SIDE_L','SIDE_R','FRONT','REAR','FLOOR','BACKBOX_BASE','BB_MonitorCarrier0','BB_MonitorCarrier1'})
check('exact source authority immutable',sha(C['source'])==v['source_sha256'])
# Every old V33.4 source/model/jig artifact remains byte-identical to HEAD BEFORE.
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',C['head_before'],'--','exports/generated/solid-leg-v334','config/solid_leg_blocks_v334.json','tools/solid_leg_v334.py','tools/viewer-v334','config/manufacturing/profiles/peter_supplier_v1.json','config/wpc_kinematics_v32.json','exports/generated/backbox-lock-integration-v32'],cwd=R,text=True).splitlines()
for path in paths:
 b=subprocess.check_output(['git','show',C['head_before']+':'+path],cwd=R)
 check('protected '+path,hashlib.sha256(b).hexdigest()==sha(path))
ps=reg['parts'];check('101 physical /97 CNC /4 solid /59 families',len(ps)==101 and reg['CNC_plywood_pieces']==97 and len(reg['families'])==59)
check('M006 retained twice',sum(p['manufacturing_part_id']=='M006' for p in ps)==2)
check('old layers and4mm pads not resurrected',not any(p['manufacturing_part_id'] in ['M019','M020','M021','M022','M023','M046','M047','M048','M049'] or p['nominal_stock_thickness_mm']==4 for p in ps))
check('SW01 exact records preserved',[p for p in ps if p['manufacturing_part_id']=='SW01']==[p for p in old['parts'] if p['manufacturing_part_id']=='SW01'])
check('all one-sided /manual plans, no operation blockers',all(p['manufacturing_status'] in ['ONE_SIDE_CNC_READY','ONE_SIDE_CNC_PLUS_MANUAL_FINISH','SHOP_MADE_SOLID_WOOD_PART'] and not p.get('blockers') and not p.get('opposite_face_cnc') for p in ps))
check('only permitted part records changed',all(p==next(q for q in old['parts'] if q['instance_id']==p['instance_id']) for p in ps if p.get('version')!='V33.5'))
check('unknown production fit stays null',C['measured_thickness_mm'] is None and C['selected_coupon_clearance_mm'] is None and not C['release'])
check('under-front centers remain unresolved',C['underfront_controls']['installed_origin_mm'] is None and C['underfront_controls']['control_centers_mm'] is None)
for p in ps:
 if p.get('version')=='V33.5':check(p['instance_id']+' exact B-rep available',(R/p['finished_member_brep']).exists() and p['blank_outside_error_mm3']<1e-4)
packing=read('exports/generated/structural-v335/packaging.json');chosen=next(c for c in packing['candidates'] if c['target_kg']==25)
flat=[i['instance_id'] for b in chosen['bundles'] for l in b['layers'] for i in l['pieces']]
check('packing contains each permanent piece once',collections.Counter(flat)==collections.Counter(p['instance_id'] for p in ps))
check('all preferred bundles <=25kg at high density',all(b['gross_high_density_kg']<=25 for b in chosen['bundles']))
check('tooling/glass/electronics not wood packing',all(not x.startswith(('JIG','TOOL')) for x in flat) and not packing['glass_electronics_in_wood_bundles'])
material=read('exports/generated/structural-v335/material-utilization.json')
for s in material['stocks']:check('sheet feasibility '+str(s['thickness_mm']),all(max(p['finished_xy_size_mm'])<=2460 and min(p['finished_xy_size_mm'])<=1560 for p in ps if p['nominal_stock_thickness_mm']==s['thickness_mm']))
metrics=read('exports/generated/structural-v335/packing-metrics.json');mass=read('exports/generated/structural-v335/mass-budget.json');vol=sum(p['volume_mm3'] for p in metrics)
check('mass derives from actual piece volumes plus undrilled SW01 stock',abs(vol-mass['wood_volume_mm3'])<1e-3)
check('no false known-zero hardware total',mass['mechanical_exact_total_kg'] is None and mass['unknown_hardware_items'])
cat=read('config/hardware_catalog_v335.json');H={h['id']:h for h in cat['hardware']}
check('F10 obsolete /F56 optional interior screws /I03 floor only',H['F10']['quantity']==0 and H['F56']['quantity']==8 and H['I03']['quantity']==8)
check('F28 unresolved remainder preserved /rail retention separately counted',H['F28']['quantity'] is None and H['F57']['quantity']==2 and H['F58']['quantity'] is None)
for row in read('templates/pocket-holes/source-metadata.json'):
 root=ET.parse(R/'templates/pocket-holes'/row['file']).getroot();w,h=row['physical_size_mm']
 check(row['file']+' physical SVG scale',root.attrib['width']==str(w)+'mm' and root.attrib['height']==str(h)+'mm' and list(map(float,root.attrib['viewBox'].split()))==[0,0,w,h])
 check(row['file']+' calibration +no jig geometry',row['calibration_square_mm']==[100,100] and row['scale_bar_mm']==100 and row['jig_reference_offset_mm'] is None and not row['actual_drilling_released'])
D=json.loads(gzip.decompress((O/'viewer-data.json.gz').read_bytes()));oldD=json.loads(gzip.decompress((R/'exports/generated/solid-leg-v334/viewer-data.json.gz').read_bytes()))
changed={r['name'] for r in v['changed']};removed=set(v['removed']);lookup={p['key']:p for p in D['installed']}
for p in oldD['installed']:
 if p['key'] in changed|removed:continue
 check('unchanged viewer geometry '+p['key'],D['geometry'][lookup[p['key']]['geometry']]==oldD['geometry'][p['geometry']])
check('real101 wood meshes; no obsolete pads',sum(p['meta']['kind']=='wood' for p in D['detail'])==101 and not any(p['meta']['source'] in removed for p in D['detail']))
check('plunger visible geometry restored',all(n in lookup for n in ['PlungerHandleProvisional','PlungerShaftProvisional','PlungerFrontInterfaceProvisional']))
browser=read('exports/generated/structural-v335/browser-validation.json');check('offline/tablet browser validation current',browser['pass'] and browser['viewer_sha256']==sha('exports/generated/viewer-v32/index.html'))
check('24 review views present',len(read('exports/generated/structural-v335/review-index.json'))==24)
check('no final full-sheet/CAM output',not list(O.glob('*.nc')) and not list(O.glob('*production*.dxf')))
result={'pass':True,'checks':checks,'native_geometry_checks':len(v['checks']),'native_motion_checks':len(m['checks']),'browser_checks':len(browser['checks']),'source_head':C['head_before'],'viewer_sha256':sha('exports/generated/viewer-v32/index.html'),'source_mesh_sha256':sha('exports/generated/structural-v335/mesh.json.gz'),'manufacturing_ready':False,'manufacturing_release':False}
(O/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print('V335_REGRESSION_PASS',len(checks),'+',len(browser['checks']),'browser +',len(v['checks'])+len(m['checks']),'native')
