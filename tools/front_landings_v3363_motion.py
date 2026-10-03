"""Native differential motion proof for front landings. CERN-OHL-S-2.0."""
from pathlib import Path
import hashlib,json,math,sys,traceback
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,pf_names,PF,WPC,V,transform,certify,build_locks,with_tethers
C=json.loads((R/'config/front_landings_v3363.json').read_text());O=R/C['output']
report={'checks':[],'certificates':{},'samples':{},'adjustment_pose_screen':{},'manufacturing_release':False,'pass':False}
def save(): (O/'motion-validation.json').write_text(json.dumps(report,indent=2)+'\n')
def ck(name,value,details=None):
 report['checks'].append({'name':name,'pass':bool(value),'detail':details});save();print(name,bool(value),flush=True)
 if not value:raise AssertionError((name,details))
def hits(mov,obs):
 out=[]
 for n,s in mov.items():
  for m,t in obs.items():
   if n==m or not s.BoundBox.intersect(t.BoundBox):continue
   volume=s.common(t).Volume
   if volume>1e-4:out.append({'moving':n,'fixed':m,'volume_mm3':volume})
 return out
def translation(mov,obs,start=.001,end=48):
 todo=[(start,end)];rows=[]
 while todo:
  lo,hi=todo.pop();mid=(lo+hi)/2;posed=transform(mov,lift=mid);limit=(hi-lo)/2+1e-6;ok=True
  for n,s in posed.items():
   a=s.BoundBox
   for m,t in obs.items():
    b=t.BoundBox;lb=math.sqrt(sum(max(0,getattr(a,k+'Min')-getattr(b,k+'Max'),getattr(b,k+'Min')-getattr(a,k+'Max'))**2 for k in 'XYZ'))
    if lb>limit:continue
    if s.distToShape(t)[0]<=limit:ok=False;break
   if not ok:break
  if ok:rows.append([lo,hi])
  else:
   assert hi-lo>1e-6,('translation unresolved',lo,hi,n,m)
   todo.extend([(lo,mid),(mid,hi)])
 return {'range_mm':[start,end],'intervals':sorted(rows),'method':'OCC midpoint separation exceeds half translation interval'}
def main():
 old=load(R/C['source']);new=load(O/'play.FCStd');released=load(O/'released.FCStd');geo=json.loads((O/'geometry-validation.json').read_text());meta=json.loads((O/'viewer-motion.json').read_text())
 paths=[R/C['source'],O/'play.FCStd',O/'released.FCStd'];report['source_sha256']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
 moving={n:s for n,s in actual(old).items() if n in pf_names(old)};moving.update({n:new[n] for n in geo['moving_receiver_names']})
 landing={n:released[n] for n in geo['new_wood_names']+geo['new_hardware_names'] if n not in moving}
 removed={n for n in old if n=='CandidateGlass' or n.startswith(('Matrix','MX_Retainer')) or n in ['MX_MovingConnectorReserve','MX_CableLoopReserve']}
 original_fixed={n:s for n,s in actual(old).items() if n not in moving and n not in removed}
 buttons={n:s for n,s in old.items() if n.startswith(('Leaf','Button'))}
 report['prerequisites']=['Main playfield glass removed','Matrix removed','Both captive M6 retention bolts released/parked','Rear dowel seated','Service support method remains required at50 degrees']
 # Every new fixed part is below the original underside plane. During initial
 # forward opening its signed distance increases strictly: with y<PivotY,
 # z<PivotZ, both terms of d(clearance)/d(angle) are positive for0..0.001deg.
 base=old['PF_BasePlywood'];bottom=max([f for f in base.Faces if type(f.Surface).__name__=='Plane' and f.normalAt(0,0).z<-.5],key=lambda f:f.Area);normal=-bottom.normalAt(0,0);center=bottom.CenterOfMass
 def plane_z(x,y):return center.z-(normal.x*(x-center.x)+normal.y*(y-center.y))/normal.z
 pp=[V(x,y,plane_z(x,y)) for x,y in [(-1000,-1000),(2000,-1000),(2000,2500),(-1000,2500)]]
 above=Part.Face(Part.makePolygon(pp+[pp[0]])).extrude(normal*1000)
 early=[]
 for n,s in landing.items():
  b=s.BoundBox
  # The exact finite half-space prism covers every new part and tests curved
  # surfaces too. Vertex gaps are supplementary diagnostics, not the proof.
  vals=[normal.dot(center-v.Point) for v in s.Vertexes]
  early.append({'name':n,'min_signed_vertex_gap_mm':min(vals),'volume_above_support_plane_mm3':s.common(above).Volume,'all_y_forward':b.YMax<PF.y,'all_z_below_axis':b.ZMax<PF.z})
 ck('initial release has increasing separating-plane distance',all(a['volume_above_support_plane_mm3']<1e-5 and a['all_y_forward'] and a['all_z_below_axis'] for a in early),early)
 report['certificates']['initial_release_analytic']={'range_deg':[0,.001],'derivative':'(nz cos(theta)-ny sin(theta))*(pivotY-y)+(-ny cos(theta)-nz sin(theta))*(pivotZ-z) >0 for all fixed landing points','plane_normal':list(normal),'positive_derivative_interval_limit_deg':math.degrees(math.atan2(-normal.y,normal.z)),'intentional_zero_angle_contact':True}
 report['certificates']['service']=certify(moving,landing,.001,50,PF,poser=lambda ss,a:transform(ss,angle=-a,axis=PF))
 ck('continuous service0to50 clears fixed landings',True,{'interval_count':len(report['certificates']['service']['intervals'])})
 report['certificates']['lift']=translation(moving,landing)
 ck('continuous lift0to48 clears fixed landings',True,{'interval_count':len(report['certificates']['lift']['intervals']),'initial0to.001':'upward plane separation increases by nz times lift'})
 tilted=transform(moving,angle=-2,axis=PF)
 report['certificates']['rear_seating']=translation(tilted,landing,0,48)
 ck('rear seating2deg plus48to0lift clears newlandings',True)
 # New receivers are inside/on M025; nearby old structure still requires its
 # own differential proof. Do not inherit a non-existent receiver certificate.
 rec={n:new[n] for n in geo['moving_receiver_names']}
 report['certificates']['receivers_vs_original']=certify(rec,original_fixed,0,50,PF,poser=lambda ss,a:transform(ss,angle=-a,axis=PF))
 report['certificates']['receivers_lift_vs_original']=translation(rec,original_fixed,0,48)
 ck('new receiver motion clears existing structures',True)
 for label,values,poser in [('service',[0,.001,.01,.1,.25,.5]+list(range(1,51)),lambda a:transform(moving,angle=-a,axis=PF)),('lift',[0,.001,.01,.1]+list(range(1,49)),lambda a:transform(moving,lift=a)),('rear_seating',list(range(49)),lambda a:transform(tilted,lift=a))]:
  rows=[]
  for val in values:
   posed=poser(val);hh=hits(posed,original_fixed|landing)
   rows.append({'value':val,'hits':hh,'base_pad_minimum_gap_mm':min(posed['PF_BasePlywood'].distToShape(landing['FrontLanding'+side+'_ContactPad'])[0] for side in ['L','R'])})
  report['samples'][label]=rows;ck(label+' whole assembly sampled clear',not any(r['hits'] for r in rows),[r for r in rows if r['hits']])
 # Stock travel is not an authorization to twist the rigid base or change its
 # playing pose. Screen both-common-height alternatives around the rear axis.
 y=C['search']['selected_pad_y_mm'];x=C['landing']['pad_left_x_mm']
 def pz(face):
  no,cc=face.normalAt(0,0),face.CenterOfMass;return cc.z-(no.x*(x-cc.x)+no.y*(y-cc.y))/no.z
 z0=pz(bottom)
 for delta in [-5,-3,0,3,5]:
  lo,hi=-2.,2.
  for _ in range(50):
   a=(lo+hi)/2;f=bottom.copy();f.rotate(PF,V(1,0,0),-a)
   if pz(f)<z0+delta:lo=a
   else:hi=a
  angle=(lo+hi)/2;pose=transform(moving,angle=-angle,axis=PF)
  reserve_hits=hits(pose,buttons);structure_hits=hits(pose,original_fixed)
  minbutton=min((pose['PF_BasePlywood'].distToShape(s)[0],n) for n,s in buttons.items())
  report['adjustment_pose_screen'][str(delta)]={'common_height_delta_mm':delta,'rotation_from_current_deg':angle,'button_hits':reserve_hits,'structure_hits':structure_hits,'minimum_base_button_reserve_gap_mm':minbutton[0],'limiting_button_reference':minbutton[1]}
 report['adjustment_rule']='Plus/minus3 mm is mechanical tolerance-compensation travel. Adjust both pads to CURRENT9.906669deg pose and equal contact; do not twist M025 against the fixed rear dowel. Reset jamnut stops for6–8mm receiver engagement after any adjustment. Pose alternatives above are clearance screens, not new accepted PLAY states.'
 ck('nominal playing pose preserves all button envelopes',not report['adjustment_pose_screen']['0']['button_hits'])
 # Populated backbox retains its established motion; only additions need
 # a new swept clearance certificate.
 backbox={n:s for n,s in new.items() if n.startswith('BB_') and 'ToyZone' not in n and 'HingeAccess' not in n and 'RetractedReserve' not in n};backbox.update(with_tethers(build_locks(True)[0],True))
 additions={n:new[n] for n in geo['new_wood_names']+geo['new_hardware_names']}
 report['certificates']['backbox_vs_additions']=certify(backbox,additions,0,90,WPC)
 ck('populated backbox0to90 clears all additions',True)
 ck('input native bytes remain unchanged',all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in report['source_sha256'].items()))
 meta['closing']['validated']=True;meta['status']='NATIVE_CLEARANCE_VALIDATED; hardware and physical load qualification pending';(O/'viewer-motion.json').write_text(json.dumps(meta,indent=2)+'\n')
 report['pass']=all(c['pass'] for c in report['checks']);save();print('V3363_MOTION_PASS',len(report['checks']),flush=True)
try:main()
except Exception as exc:report['error']=str(exc);report['traceback']=traceback.format_exc();save();print(report['traceback'],flush=True);raise
