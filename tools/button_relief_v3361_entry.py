"""V33.6.1 owner front-button datums and minimal open-front edge relief.
Original parametric geometry; CERN-OHL-S-2.0. Hardware/CNC release remains held.
"""
from pathlib import Path
import json,sys,math,gzip,hashlib
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,V
C=json.loads((R/'config/button_relief_v3361.json').read_text());O=R/C['output'];O.mkdir(parents=True,exist_ok=True);(O/'brep').mkdir(exist_ok=True)
old=load(R/C['source']);new=dict(old);study={};checks=[];data={}
review=json.loads((R/'exports/generated/notch-floor-fans-v32/validation.json').read_text())['review'];alpha=review['closed_slope_deg'];bz=400.05+45*math.tan(math.radians(alpha))-12-55*math.cos(math.radians(alpha))
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def tf(s):s=s.copy();s.rotate(V(),V(1,0,0),alpha);s.translate(V(0,45,bz));return s
def inv(s):s=s.copy();s.translate(V(0,-45,-bz));s.rotate(V(),V(1,0,0),-alpha);return s
def mirror(s):
 m=A.Matrix();m.A11=-1;m.A14=600;s=s.copy();s.transformShape(m,True);return s
def diff(a,b):
 if a.isSame(b) or a.exportBrepToString()==b.exportBrepToString():return 0.0
 return a.cut(b).Volume+b.cut(a).Volume
def ck(n,v,detail=None):checks.append({'name':n,'pass':bool(v),'detail':detail});print(n,bool(v),flush=True)
def hits(s,obs):
 out=[]
 for n,b in obs.items():
  if s.BoundBox.intersect(b.BoundBox):
   vol=s.common(b).Volume
   if vol>1e-4:out.append({'part':n,'volume_mm3':vol})
 return out
def mesh(s):
 vv,ff=s.tessellate(.3);return {'vertices':[list(p) for p in vv],'faces':ff}
# Derive Z from exact present side shape, not the old Z270 or a copied height.
b=C['side_buttons'];left=old['SIDE_L'].copy();bore=b['reference_bore_for_visualization_mm'];pdiam,pdepth=b['reference_nut_pocket_for_visualization_mm'];centers=[]
for supplied in b['centers']:
 kind=supplied['kind'];y=supplied['y_mm'];top=old['SIDE_L'].common(Part.makeLine(V(.1,y,-100),V(.1,y,1000))).BoundBox.ZMax;z=top-b['local_top_offset_mm'];centers.append({'kind':kind,'y_mm':y,'z_mm':z,'local_top_z_mm':top,'offset_below_top_mm':65})
 ck(kind+' owner center from actual side top',abs(z-supplied['z_mm'])<1e-6 and y==({'primary':89,'secondary':127}[kind]),{'y_mm':y,'z_mm':z,'top_z_mm':top})
 before=old['LeafButton_'+kind+'_L'].BoundBox.Center;dy=y-before.y;dz=z-before.z
 left=left.fuse(Part.makeCylinder(bore/2,18,V(0,before.y,before.z),V(1,0,0))).fuse(Part.makeCylinder(pdiam/2,pdepth,V(18-pdepth,before.y,before.z),V(1,0,0))).removeSplitter()
 left=left.cut(Part.makeCylinder(bore/2,20,V(-1,y,z),V(1,0,0))).cut(Part.makeCylinder(pdiam/2,pdepth+1,V(18-pdepth,y,z),V(1,0,0))).removeSplitter()
 for n,s in old.items():
  if kind in n and n.startswith(('Leaf','Button')):
   q=s.copy();q.translate(V(0,dy,dz));new[n]=q;study['Old_'+n]=s.copy()
new['SIDE_L']=left;new['SIDE_R']=mirror(left);data['button_centers']=centers
ck('button side symmetry',diff(new['SIDE_R'],mirror(new['SIDE_L']))<1e-5)
ck('ergonomic maximum and negative old datum controls',all(c['y_mm']<=b['maximum_'+c['kind']+'_y_mm'] and abs(c['z_mm']-270)>1 for c in centers) and b['final_bore_mm'] is None and b['final_recess_mm'] is None)
# Exact V33.6 board, including rear window and strain slots, is the starting solid.
base=old['PF_BasePlywood'];local=inv(base);bb=local.BoundBox
study['WrongV336Base']=base;study['PreviousCleanBase']=load(R/C['playfield']['clean_source'])['PF_BasePlywood'];study['CurrentHornedBase']=load(R/'exports/generated/structural-v335/play.FCStd')['PF_BasePlywood']
source_study=load(R/'exports/generated/monitor-support-v336/study.FCStd')
for n,s in source_study.items():
 if n.startswith(('PF_MainServiceWindow','PF_StrainSlot','PF_GenericConnector')):study[n]=s
# Design family: a straight inset from the open front, one tangent quarter arc,
# straight rear shoulder and convex outer edge. No bridge, reverse curve or horn.
rel=C['playfield']['front_relief'];clear=rel['service_clearance_mm'];radius=rel['transition_radius_mm'];step=rel['parameter_rounding_mm']
probes={n:inv(s) for n,s in new.items() if n.startswith(('Leaf','Button')) and n.endswith('_L')}
# Project only envelopes at the board thickness plus a clearance-distance halo.
# Far-below bracket material cannot set an unnecessary XY cut.
slab=box(-20,-100,bb.ZMin-clear,640,1300,bb.ZLength+2*clear);reach={}
for n,s in probes.items():
 q=s.common(slab)
 if q.Volume>1e-5 and q.BoundBox.XMax+clear>bb.XMin:reach[n]=q
assert reach
roundup=lambda v:math.ceil((v-1e-9)/step)*step
depth=roundup(max(q.BoundBox.XMax for q in reach.values())+clear-bb.XMin);x=bb.XMin+depth
assert depth>=radius and radius>=2
q=math.sqrt(.5)
def cutter(yend):
 z=bb.ZMin-1;p=lambda x,y:V(x,y,z);yarc=yend-radius
 edges=[Part.makeLine(p(bb.XMin-10,bb.YMin-1),p(x,bb.YMin-1)),Part.makeLine(p(x,bb.YMin-1),p(x,yarc)),Part.Arc(p(x,yarc),p(x-radius+radius*q,yarc+radius*q),p(x-radius,yend)).toShape(),Part.makeLine(p(x-radius,yend),p(bb.XMin-10,yend)),Part.makeLine(p(bb.XMin-10,yend),p(bb.XMin-10,bb.YMin-1))]
 return Part.Face(Part.Wire(edges)).extrude(V(0,0,bb.ZLength+2))
def candidate(yend):return local.cut(cutter(yend)).removeSplitter()
def feasible(yend):
 s=candidate(yend)
 return all(s.distToShape(p)[0]>=clear-1e-7 for p in probes.values())
lo=bb.YMin+radius;hi=max(p.BoundBox.YMax for p in reach.values())+clear+radius
assert feasible(hi)
for i in range(25):
 mid=(lo+hi)/2
 if feasible(mid):hi=mid
 else:lo=mid
end=roundup(hi);cutL=tf(cutter(end));cutR=mirror(cutL);base=base.cut(cutL).cut(cutR).removeSplitter();new['PF_BasePlywood']=base
study['PF_FrontReliefL']=cutL;study['PF_FrontReliefR']=cutR
removed=old['PF_BasePlywood'].cut(base).removeSplitter();features={n:s for n,s in new.items() if n.startswith(('PF_StrapScrew','PF_CommercialStrap')) or n in ['PF_WoodDowel','PF_VESAEnvelope','PLAYFIELD_ENVELOPE']};near={n:removed.distToShape(s)[0] for n,s in features.items()}
rl={'profile':rel['profile'],'classification':rel['classification'],'depth_mm':depth,'length_mm':end-bb.YMin,'transition_radius_mm':radius,'local_y_start_mm':bb.YMin,'local_y_arc_start_mm':end-radius,'local_y_end_mm':end,'local_left_inset_x_mm':x,'local_right_inset_x_mm':600-x,'minimum_transverse_width_mm':bb.XLength-2*depth,'minimum_section_area_mm2':(bb.XLength-2*depth)*bb.ZLength,'thickness_mm':bb.ZLength,'minimum_target_service_clearance_mm':clear,'unrounded_minimum_y_end_mm':hi,'previous_0_1mm_shorter_fails':not feasible(end-step),'previous_0_1mm_shallower_fails':'Depth is X reach plus2mm; 0.1mm shallower gives1.9mm tool separation','remaining_transverse_section_fraction':(bb.XLength-2*depth)/bb.XLength,'nearest_VESA_mm':near['PF_VESAEnvelope'],'nearest_strap_mm':min(v for n,v in near.items() if n.startswith('PF_CommercialStrap')),'nearest_fastener_mm':min(v for n,v in near.items() if n.startswith('PF_StrapScrew')),'nearest_dowel_mm':near['PF_WoodDowel'],'TV_envelope_clearance_mm':base.distToShape(new['PLAYFIELD_ENVELOPE'])[0],'removed_volume_mm3':removed.Volume,'mass_removed_kg_at650':removed.Volume*650/1e9,'source_reach_bounds':{n:[s.BoundBox.XMax,s.BoundBox.YMax] for n,s in reach.items()},'dogbones':False,'structural_certification':False}
x-=step
shallower_gap=min(candidate(end).distToShape(p)[0] for p in probes.values())
x+=step
rl['previous_0_1mm_shallower_minimum_gap_mm']=shallower_gap
rl['previous_0_1mm_shallower_fails']=shallower_gap<clear-1e-5
data['relief']=rl
ck('M025 one valid symmetric 18mm stock solid',base.isValid() and len(base.Solids)==1 and abs(inv(base).BoundBox.ZLength-18)<1e-5 and diff(base,mirror(base))<1e-5)
# Cross-section at open front must begin at inset X, and width must only increase
# across the transition. This rejects the former short front bridge/horn.
loc=inv(base);widths=[]
for yy in [bb.YMin+.001,end-radius-.001,end-radius/2,end-.001,end+.001]:
 s=loc.common(box(0,yy,-15,600,.0001,20));widths.append({'local_y_mm':yy,'width_mm':s.BoundBox.XLength})
ck('PLAYFIELD_BASE_HORN_ABSENT open front monotone widening',abs(widths[0]['width_mm']-rl['minimum_transverse_width_mm'])<1e-5 and all(a['width_mm']<=b['width_mm']+1e-5 for a,b in zip(widths,widths[1:])),widths)
ck('minimum simple profile derived from restored service envelopes',rl['previous_0_1mm_shorter_fails'] and feasible(end),rl)
phys=actual(new);obs={n:s for n,s in phys.items() if not n.startswith(('Leaf','Button')) and n not in ['SIDE_L','SIDE_R','CandidateGlass']};rows=[]
for n,s in new.items():
 if n.startswith(('Leaf','Button')):
  hh=hits(s,obs);rows.append({'name':n,'hits':hh,'base_separation_mm':s.distToShape(base)[0]})
data['buttons']=rows
ck('restored buttons and wire/tool reserves clear installed structures',not any(r['hits'] for r in rows),[r for r in rows if r['hits']])
ck('all restored button envelopes retain2mm base clearance',min(r['base_separation_mm'] for r in rows)>=clear-1e-5,rows)
ck('VESA straps screws dowel and TV unchanged',all(diff(old[n],s)<1e-5 for n,s in features.items()) and min(v for n,v in near.items() if n!='PLAYFIELD_ENVELOPE')>10)
# Preserve exact prior holes and all wood behind the relief, not just their label.
back=box(0,end+.001,-15,600,1100,20)
ck('V336 rear service window and paired strain slots exact',diff(inv(old['PF_BasePlywood']).common(back),loc.common(back))<1e-5)
ck('backbox monitor carriers and M067 exact',all(diff(old[n],new[n])<1e-5 for n in old if n.startswith('BB_')))
data['openings']=json.loads((R/'exports/generated/monitor-support-v336/geometry-validation.json').read_text())['openings'];data['playfield_structural_screen']={**rl,'certification':False,'rear_service_window_transverse_width_mm':320,'rear_window_side_band_mm':160,'remaining_hold':'Full-load stiffness, actual plywood, selected leaf/adapter fasteners and ergonomic/physical qualification; unchanged VESA load reserve.'}
wood={p['source_component'] for p in json.loads((R/'exports/generated/monitor-support-v336/manufacturing-register.json').read_text())['parts']};changed=[n for n in old if diff(old[n],new[n])>1e-4];added=[];allowed={'SIDE_L','SIDE_R','PF_BasePlywood'}|{n for n in old if n.startswith(('Leaf','Button'))}
ck('only authorized3wood and32reference shapes changed',set(changed)==allowed,changed)
ck('all unrelated shapes retain exact native geometry',all(new[n] is s for n,s in old.items() if n not in allowed))
coll=[]
for n in changed:
 if n not in wood:continue
 for k,s in phys.items():
  if k==n or k.startswith(('Leaf','Button')):continue
  if not new[n].BoundBox.intersect(s.BoundBox):continue
  before=old[n].common(old[k]).Volume;after=new[n].common(s).Volume
  if after>before+1e-4:coll.append([n,k,before,after])
ck('no new changed wood penetration',not coll,coll)
hornfront=inv(study['CurrentHornedBase']).common(box(0,bb.YMin+.001,-15,600,.0001,20)).BoundBox.XLength
negative={'historical_horn_front_width_mm':hornfront,'accepted_front_width_mm':widths[0]['width_mm'],'historical_horn_rejected':abs(hornfront-rl['minimum_transverse_width_mm'])>1,'Y255_Y310_rejected':255>b['maximum_primary_y_mm'] and 310>b['maximum_secondary_y_mm'],'Z270_rejected':all(abs(c['z_mm']-270)>1 for c in centers),'shallower_relief_rejected':rl['previous_0_1mm_shallower_fails'],'shorter_relief_rejected':rl['previous_0_1mm_shorter_fails']}
data['negative_controls']=negative
ck('historical horn and wrong old datums rejected by active rules',all(negative[k] for k in ['historical_horn_rejected','Y255_Y310_rejected','Z270_rejected','shallower_relief_rejected','shorter_relief_rejected']),negative)
for label,ss in [('play',new),('study',study)]:
 d=A.newDocument('V3361'+label)
 for n,s in ss.items():
  o=d.addObject('PartDesign::Feature',n);o.Shape=s;o.addProperty('App::PropertyString','GeometryAuthority');o.GeometryAuthority='config/button_relief_v3361.json' if n in changed or label=='study' else 'V33.6 unchanged: config/monitor_support_v336.json'
 d.recompute();d.saveAs(str(O/(label+'.FCStd')));A.closeDocument(d.Name)
for n in changed:new[n].exportBrep(str(O/'brep'/(n+'.brep')))
for file,ss in [('changes-mesh',{n:new[n] for n in changed}),('study-mesh',study)]:
 (O/(file+'.json.gz')).write_bytes(gzip.compress(json.dumps({n:mesh(s) for n,s in ss.items()}).encode(),mtime=0))
data.update(changed=[{'name':n,'before_mm3':old[n].Volume,'after_mm3':new[n].Volume,'symmetric_difference_mm3':diff(old[n],new[n])} for n in changed],added=added,removed=[],checks=checks,release=False,source_sha256=hashlib.sha256((R/C['source']).read_bytes()).hexdigest(),clean_source_sha256=hashlib.sha256((R/C['playfield']['clean_source']).read_bytes()).hexdigest());data['pass']=all(c['pass'] for c in checks);data['base_volume_mm3']=base.Volume;(O/'geometry-validation.json').write_text(json.dumps(data,indent=2)+'\n');print('V3361_GEOMETRY_DONE',data['pass'],len(checks),flush=True)
