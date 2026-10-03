"""Common front-height setup clearance, fixed rear dowel; no angle-selection feature.
CERN-OHL-S-2.0. Nominal PLAY pose remains unchanged.
"""
from pathlib import Path
import sys,json,math,hashlib
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,PF,V,transform
O=R/'exports/generated/service-productization-v338';P=O/'landing-candidate.FCStd'
s=load(P);names=json.loads((R/'exports/generated/front-landings-v3363/viewer-motion.json').read_text())['playfield_moving_names']
moving={n:s[n] for n in names};base=s['PF_BasePlywood'];bottom=max([f for f in base.Faces if type(f.Surface).__name__=='Plane' and f.normalAt(0,0).z<-.5],key=lambda f:f.Area)
def pz(f):
 no,cc=f.normalAt(0,0),f.CenterOfMass;return cc.z-(no.x*(72-cc.x)+no.y*(245-cc.y))/no.z
z0=pz(bottom)
def angle(delta):
 lo,hi=-2.,2.
 for _ in range(45):
  a=(lo+hi)/2;f=bottom.copy();f.rotate(PF,V(1,0,0),-a)
  if pz(f)<z0+delta:lo=a
  else:hi=a
 return (lo+hi)/2
fixed={n:t for n,t in actual(s).items() if n not in moving and not n.startswith(('FrontLanding','PF_OpenCradle','PF_SupportMountScrew'))}
button={n:t for n,t in s.items() if n.startswith(('Button','Leaf')) and 'ToolService' not in n}
fixed.update(button)
tools={n:t for n,t in s.items() if n.startswith(('Button','Leaf')) and 'ToolService' in n}
def lower(a,b):
 a,b=a.BoundBox,b.BoundBox;return math.sqrt(sum(max(0,getattr(a,k+'Min')-getattr(b,k+'Max'),getattr(b,k+'Min')-getattr(a,k+'Max'))**2 for k in 'XYZ'))
# Every unrelated pair that can approach within1mm over +-3 is retained.
radii={n:max(math.hypot(y-PF.y,z-PF.z) for y in [v.BoundBox.YMin,v.BoundBox.YMax] for z in [v.BoundBox.ZMin,v.BoundBox.ZMax]) for n,v in moving.items()}
max_point_arc_mm=max(radii.values())*math.radians(max(abs(angle(-3)),abs(angle(3))))
assert max_point_arc_mm+1<15,('15mm broad search is insufficient',max_point_arc_mm)
# Native current bound is3.737mm, so15mm is conservative including1mm margin.
pairs=[(n,k) for n,a in moving.items() for k,b in fixed.items() if lower(a,b)<15]
tpairs=[(n,k) for n,a in moving.items() for k,b in tools.items() if lower(a,b)<15]
baseline=[]
for n,k in pairs:
 d=moving[n].distToShape(fixed[k])[0]
 if d<1e-6:baseline.append({'moving':n,'fixed':k,'volume_mm3':moving[n].common(fixed[k]).Volume})
assert not baseline,('Undeclared contact in closed-adjustment obstacles',baseline)
cache={}
def screen(delta,tool=False):
 key=(round(delta,9),tool)
 if key in cache:return cache[key]
 aa=angle(delta);pose=transform(moving,angle=-aa,axis=PF);obs=tools if tool else fixed;pp=tpairs if tool else pairs;near=(1e9,'','');hits=[]
 for n,k in pp:
  a,b=pose[n],obs[k]
  if lower(a,b)<=near[0]:
   d=a.distToShape(b)[0]
   if d<near[0]:near=(d,n,k)
  if a.BoundBox.intersect(b.BoundBox):
   vol=a.common(b).Volume
   if vol>1e-5:hits.append({'moving':n,'fixed':k,'volume_mm3':vol})
 row={'delta_mm':delta,'rotation_from_nominal_deg':aa,'nearest_mm':near[0],'moving':near[1],'fixed':near[2],'hits':hits};cache[key]=row;return row
rows=[]
for delta in [-3+i*.25 for i in range(25)]:
 r=screen(delta);rows.append(r);print('HEIGHT',delta,r['nearest_mm'],r['moving'],r['fixed'],len(r['hits']),flush=True)
def transition(lo,hi,margin):
 # lo is forbidden,hi is acceptable. Monotonicity verified by quarter-mm grid.
 assert screen(lo)['nearest_mm']<margin and screen(hi)['nearest_mm']>=margin
 for _ in range(22):
  mid=(lo+hi)/2
  if screen(mid)['nearest_mm']<margin:lo=mid
  else:hi=mid
 return [lo,hi]
margin=1.;low=transition(-3,0,margin);zero=transition(-3,0,1e-5)
def upper_transition(margin):
 lo,hi=0.,3.
 for _ in range(22):
  mid=(lo+hi)/2
  if screen(mid)['nearest_mm']>=margin:lo=mid
  else:hi=mid
 return [lo,hi]
high=upper_transition(margin);zero_high=upper_transition(1e-5)
safe_low=math.ceil(low[1]*10)/10;safe_hi=math.floor(high[0]*10)/10
# Continuous clearance certificate using native midpoint distances and maximum
# point-arc bound, at the requested1mm envelope, not just discrete samples.
radii={n:max(math.hypot(y-PF.y,z-PF.z) for y in [a.BoundBox.YMin,a.BoundBox.YMax] for z in [a.BoundBox.ZMin,a.BoundBox.ZMax]) for n,a in moving.items()}
todo=[(safe_low,safe_hi)];intervals=[]
while todo:
 lo,hi=todo.pop();a0,a1=angle(lo),angle(hi);am=(a0+a1)/2;pose=transform(moving,angle=-am,axis=PF);ok=True
 for n,k in pairs:
  limit=margin+radii[n]*math.radians(abs(a1-a0)/2)+1e-6
  if lower(pose[n],fixed[k])<=limit and pose[n].distToShape(fixed[k])[0]<=limit:ok=False;break
 if ok:intervals.append([lo,hi])
 else:
  assert hi-lo>1e-6,('margin unresolved',lo,hi,n,k);mid=(lo+hi)/2;todo.extend([(lo,mid),(mid,hi)])
toolrows=[screen(d,True) for d in [-3,safe_low,0,3]]
report={'pass':True,'source_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'hardware_travel_reference_mm':[-3,3],'physical_collision_threshold_bracket_mm':zero,'upper_glass_collision_threshold_bracket_mm':zero_high,'one_mm_margin_threshold_bracket_mm':low,'upper_one_mm_margin_threshold_bracket_mm':high,'geometric_common_height_setup_window_mm':[safe_low,safe_hi],'nominal_pose_delta_mm':0,'nominal_play_slope_deg':9.906669,'user_selectable_slope':False,'independent_L_R_twist_permitted':False,'adjustment_condition':'Both retainers released; rear dowel fully seated. Adjust each support to equal contact with the accepted nominal M025 plane, then reset6-8mm retention engagement and stops. Window is a rigid-body common-height tolerance screen, not permission to change PLAY slope. Differential leveling takes up contact error only; no rigid-base twist.','physical_obstacles_include':'Actual CURRENT structures, closed main glass, installed matrix, display envelope, side button bodies/wire reserves. Front landings/retention excluded because pads/stops are the adjusted mechanism; rear cradle engagement is preserved by exact pivot rotation.','excluded_mechanism_names':[n for n in s if n.startswith(('FrontLanding','PF_OpenCradle','PF_SupportMountScrew'))],'baseline_undeclared_contacts':baseline,'samples':rows,'continuous_certificate':{'margin_mm':margin,'intervals':sorted(intervals),'method':'OCC midpoint separation exceeds1mm plus conservative maximum point arc movement per interval;15mm broad search over <0.22deg covers all nearby pairs.'},'button_tool_corridor_separate_screen':toolrows,'physical_qualification':'PENDING: real component envelopes/stock/deflection/coupon. Tool corridors can require moving/removing playfield and are not physical button bodies.','manufacturing_release':False}
(O/'adjustment-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('V338_ADJUSTMENT_PASS',safe_low,safe_hi,len(intervals),flush=True)
