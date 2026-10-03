"""Read-only V33.8 independent geometry/claim screen. CERN-OHL-S-2.0.
This verifies the adjustment broad-phase bound and excluded rear mechanism at
explicit setup samples. It does not certify physical strength or service support.
"""
from pathlib import Path
import sys,json,hashlib,math
import FreeCAD as A
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,PF,V,transform
O=R/'exports/generated/service-productization-v338'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inputs=[Path(__file__),R/'tools/front_landing_adjustment_v338.py',R/'tools/combine_service_productization_v338.py',O/'landing-candidate.FCStd',O/'play.FCStd',O/'adjustment-validation.json',O/'geometry-validation.json',O/'manufacturing-audit.json',O/'SW02-load-screen.json',O/'retention-decision.json',O/'metrics-authority.json',O/'assembly-manual.json',R/'exports/generated/front-landings-v3363/viewer-motion.json']
hashes={str(p.relative_to(R)):sha(p) for p in inputs}
s=load(O/'landing-candidate.FCStd');r=read(O/'adjustment-validation.json')
names=read(R/'exports/generated/front-landings-v3363/viewer-motion.json')['playfield_moving_names'];moving={n:s[n] for n in names}
checks=[]
def ck(name,passed,detail=None):
 checks.append({'name':name,'pass':bool(passed),'detail':detail});assert passed,(name,detail)
radii={n:max(math.hypot(y-PF.y,z-PF.z) for y in [a.BoundBox.YMin,a.BoundBox.YMax] for z in [a.BoundBox.ZMin,a.BoundBox.ZMax]) for n,a in moving.items()}
maxname=max(radii,key=radii.get);amax=max(abs(x['rotation_from_nominal_deg']) for x in r['samples']);arc=radii[maxname]*math.radians(amax)
ck('Native adjustment report uses the inspected candidate',r['source_sha256']==sha(O/'landing-candidate.FCStd'))
ck('15 mm broad-phase radius exceeds maximum point motion plus 1 mm margin',arc+1+1e-6<15,{'maximum_radius_mm':radii[maxname],'maximum_radius_object':maxname,'maximum_rotation_deg':amax,'maximum_arc_displacement_mm':arc,'margin_mm':1,'broad_phase_mm':15})
base=s['PF_BasePlywood'];bottom=max([f for f in base.Faces if type(f.Surface).__name__=='Plane' and f.normalAt(0,0).z<-.5],key=lambda f:f.Area)
def z_at_support(f):
 n,c=f.normalAt(0,0),f.CenterOfMass;return c.z-(n.x*(72-c.x)+n.y*(245-c.y))/n.z
z0=z_at_support(bottom)
def angle(delta):
 lo,hi=-2.,2.
 for _ in range(45):
  a=(lo+hi)/2;f=bottom.copy();f.rotate(PF,V(1,0,0),-a)
  if z_at_support(f)<z0+delta:lo=a
  else:hi=a
 return (lo+hi)/2
obs={n:t for n,t in s.items() if n.startswith(('PF_OpenCradle','PF_SupportMountScrew'))};samples=[]
for delta in [r['geometric_common_height_setup_window_mm'][0],-1,0,r['geometric_common_height_setup_window_mm'][1]]:
 pose=transform(moving,angle=-angle(delta),axis=PF);hits=[];contact=[];near=[]
 for n,a in pose.items():
  for k,b in obs.items():
   distance=a.distToShape(b)[0]
   if a.BoundBox.intersect(b.BoundBox):
    volume=a.common(b).Volume
    if volume>1e-5:hits.append({'moving':n,'fixed':k,'volume_mm3':volume})
   if distance<1e-6:contact.append({'moving':n,'fixed':k})
   else:near.append((distance,n,k))
 nearest=min(near)
 row={'common_height_delta_mm':delta,'rotation_deg':angle(delta),'penetrations':hits,'contacts':contact,'nearest_noncontact':{'distance_mm':nearest[0],'moving':nearest[1],'fixed':nearest[2]}};samples.append(row)
 ck(f'Rear mechanism sample {delta:g} mm has only intended seated-dowel contact',not hits and all(c['moving']=='PF_WoodDowel' and c['fixed'].startswith('PF_OpenCradle') for c in contact) and nearest[0]>1,row)
g=read(O/'geometry-validation.json');a=read(O/'manufacturing-audit.json');loadscreen=read(O/'SW02-load-screen.json');ret=read(O/'retention-decision.json')
ck('Native snapshot matches geometry and manufacturing evidence',g['pass'] and a['pass'] and g['native_sha256']==a['native_geometry_sha256']==sha(O/'play.FCStd'))
ck('Selected retention remains A with tool and physical hold',ret['selected_option']=='A' and ret['tool_required'] is True and ret['count']==2 and ret['manufacturing_release'] is False)
ck('Load screen does not claim material capacity or certification',loadscreen['strength_capacity'] is None and loadscreen['not_certification'] is True and not loadscreen['manufacturing_release'])
ck('Setup window is distinct from mechanical travel and not angle/twist permission',r['hardware_travel_reference_mm']==[-3,3] and r['geometric_common_height_setup_window_mm']==[-1.9,.9] and r['nominal_pose_delta_mm']==0 and not r['user_selectable_slope'] and not r['independent_L_R_twist_permitted'])
ma=read(O/'metrics-authority.json');stale=[q['path'] for q in ma['sources'] if sha(R/q['path'])!=q['sha256']]
ck('Metrics authority binds the current manual and sources',not stale,stale)
for p,digest in hashes.items():assert sha(R/p)==digest,('Concurrent input change',p)
report={'version':'V33.8','pass':all(c['pass'] for c in checks),'checks':checks,'source_sha256':hashes,'native_sha256':sha(O/'play.FCStd'),'rear_mechanism_samples':samples,'scope':'Independent conservative broad-phase bound and explicit rear-mechanism samples; source/claim consistency. Final safe range also relies on the root continuous certificate.','limitations':['Sampled rear check is not a new full-path certificate; rear dowel rotation is concentric and contacts intentional.','Simple load-path demand is not combined torsion/notch/material capacity.','No physical service-support or manufacturing release; primary raised-playfield support remains OPERATIONAL HOLD.'],'manufacturing_release':False}
(O/'independent-qa.json').write_text(json.dumps(report,indent=2)+'\n')
print('V338_INDEPENDENT_QA_PASS',len(checks),flush=True)
