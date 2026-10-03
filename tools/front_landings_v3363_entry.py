"""V33.6.3 native front landings; nominal hardware, not CNC release.
Original source, CERN-OHL-S-2.0. Existing B-reps are never cut by this script.
"""
from pathlib import Path
import gzip, hashlib, json, math, sys
import FreeCAD as A, Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,pf_names,PF,V,transform
C=json.loads((R/'config/front_landings_v3363.json').read_text());L=C['landing'];T=C['retention'];S=C['search']
O=R/C['output'];O.mkdir(parents=True,exist_ok=True);(O/'brep').mkdir(exist_ok=True)
source=R/C['source'];sourcehash=hashlib.sha256(source.read_bytes()).hexdigest();old=load(source)
base=old['PF_BasePlywood'];bottom=max([f for f in base.Faces if type(f.Surface).__name__=='Plane' and f.normalAt(0,0).z<-.5],key=lambda f:f.Area)
n=bottom.normalAt(0,0);up=-n;c=bottom.CenterOfMass
def z(y):return c.z-n.y/n.z*(y-c.y)
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def cyl(x,y,z,r,h,axis=V(0,0,1)):return Part.makeCylinder(r,h,V(x,y,z),axis)
def ring(x,y,z,ro,ri,h):return cyl(x,y,z,ro,h).cut(cyl(x,y,z,ri,h))
def mirror(s):
 m=A.Matrix();m.A11=-1;m.A14=600;q=s.copy();q.transformShape(m,True);return q
def bb(s):b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def plane_z(face,y,x):
 no,cc=face.normalAt(0,0),face.CenterOfMass;return cc.z-(no.x*(x-cc.x)+no.y*(y-cc.y))/no.z
def near(s,obs,threshold=8):
 rows=[]
 for name,t in obs.items():
  a,b=s.BoundBox,t.BoundBox
  lb=math.sqrt(sum(max(0,getattr(a,k+'Min')-getattr(b,k+'Max'),getattr(b,k+'Min')-getattr(a,k+'Max'))**2 for k in 'XYZ'))
  if lb>threshold:continue
  d=s.distToShape(t)[0]
  if d<=threshold:rows.append({'part':name,'distance_mm':d,'penetration_mm3':s.common(t).Volume if d<1e-6 else 0})
 return sorted(rows,key=lambda a:a['distance_mm'])
def hexagon(x,y,z,across,h,bore=0):
 r=across/math.sqrt(3);v=[V(x+r*math.cos(i*math.pi/3),y+r*math.sin(i*math.pi/3),z) for i in range(6)]
 s=Part.Face(Part.makePolygon(v+[v[0]])).extrude(V(0,0,h));return s.cut(cyl(x,y,z,bore,h)) if bore else s
obs={name:s for name,s in actual(old).items() if name not in ['SIDE_L','SIDE_R','CandidateGlass','PF_BasePlywood']}
obs.update({name:s for name,s in old.items() if name.startswith(('Leaf','Button')) or name=='PLUNGER_RESERVED'})
access={}
for f in (R/'exports/generated/button-relief-v3361/brep').glob('Access_*.brep'):
 q=Part.Shape();q.read(str(f));access[f.stem]=q
obs.update(access)
search=[]
for h in S['body_heights_compared_mm']:
 for y in range(S['pad_center_y_range_mm'][0],S['pad_center_y_range_mm'][1]+1):
  top=z(y)-L['nominal_base_to_body_top_mm'];body=box(18,y-20,top-h,68,70,h)
  pad=Part.makeCylinder(12,3,V(72,y,z(y))-up*3,up)
  disk=Part.Face(Part.Wire(Part.makeCircle(12,V(72,y,z(y)),up)))
  area=disk.common(bottom).Area;edge=disk.distToShape(bottom.OuterWire)[0]
  envelope=Part.makeCompound([body,pad,cyl(72,y,z(y)-43,4,40),cyl(72,y+30,top-h-14,13,14)])
  envelope=Part.makeCompound([envelope,mirror(envelope)])
  closest=near(envelope,obs);fail=[a for a in closest if a['distance_mm']<S['minimum_obstacle_clearance_mm']-1e-7]
  search.append({'body_height_mm':h,'pad_y_mm':y,'body_bounds_mm':bb(body),
                 'contact_area_mm2':area,'pad_area_mm2':disk.Area,'contact_edge_gap_mm':edge,
                 'nearby_obstacles':closest,'rejected_by':fail,
                 'pass':not fail and abs(area-disk.Area)<1e-5 and edge>=S['minimum_contact_to_base_edge_mm']-1e-6})
selected=next(r for r in search if r['body_height_mm']==L['body_height_mm'] and r['pass'])
assert selected['pad_y_mm']==S['selected_pad_y_mm'],selected
y=selected['pad_y_mm'];yy=y+T['axis_rearward_of_pad_mm'];x=L['pad_left_x_mm'];ztop=z(y)-22;zbot=ztop-L['body_height_mm']
wood={};hardware={};refs={};moving_receivers={};release_names=[];side_screws=[];lam_screws=[]
for side in ['L','R']:
 tf=(lambda s:s) if side=='L' else mirror
 # Holes in new wood are reference dimensions; all final purchased fits held.
 cuts=[cyl(x,y,zbot-1,4.5,56),cyl(x,yy,zbot-1,3.5,56),cyl(x,y,ztop-16,6,17)]
 for offy in L['side_screw_y_offsets_from_pad_mm']:
  for offz in L['side_screw_z_offsets_from_body_bottom_mm']:
   sy,sz=y+offy,zbot+offz;cuts.append(cyl(17,sy,sz,2.5,70,V(1,0,0)))
   cuts.append(Part.makeCone(4.5,2.25,2,V(86,sy,sz),V(-1,0,0)))
 for sx,sy in L['lamination_screw_left_xy_mm']:
  cuts.append(cyl(sx,sy,ztop-50,2.25,51));cuts.append(Part.makeCone(2.25,4.5,2,V(sx,sy,ztop-2)))
 for j in range(3):
  s=box(18,y-20,zbot+18*j,68,70,18)
  for cut in cuts:s=s.cut(cut)
  wood[f'FrontLanding{side}_Layer{j+1}']=tf(s.removeSplitter())
 for k,(offy,offz) in enumerate([(a,b) for a in L['side_screw_y_offsets_from_pad_mm'] for b in L['side_screw_z_offsets_from_body_bottom_mm']]):
  sy,sz=y+offy,zbot+offz
  s=cyl(6,sy,sz,2.25,80,V(1,0,0)).fuse(Part.makeCone(4.5,2.25,2,V(86,sy,sz),V(-1,0,0)))
  name=f'FrontLanding{side}_SideScrew{k+1}';hardware[name]=tf(s);side_screws.append(name)
  refs[f'FrontLanding{side}_SidePilot{k+1}']=tf(cyl(6,sy,sz,1.5,12,V(1,0,0)))
 for k,(sx,sy) in enumerate(L['lamination_screw_left_xy_mm']):
  s=cyl(sx,sy,ztop-50,2.25,50).fuse(Part.makeCone(2.25,4.5,2,V(sx,sy,ztop-2)))
  name=f'FrontLanding{side}_LaminationScrew{k+1}';hardware[name]=tf(s);lam_screws.append(name)
 hardware[f'FrontLanding{side}_AdjusterInsert']=tf(ring(x,y,ztop-16,6,4.05,16))
 hardware[f'FrontLanding{side}_AdjusterWasher']=tf(ring(x,y,ztop,8,4.05,1.6))
 hardware[f'FrontLanding{side}_AdjusterLocknut']=tf(hexagon(x,y,ztop+1.6,13,6.5,4.05))
 # Articulated foot is an original compact envelope, not vendor CAD. Pad
 # plane includes the three-mm contact thickness, aligned with actual base.
 padbase=V(x,y,z(y))-up*3
 hardware[f'FrontLanding{side}_ContactPad']=tf(Part.makeCylinder(12,3,padbase,up))
 footbase=V(x,y,z(y))-up*5
 hardware[f'FrontLanding{side}_SwivelDisc']=tf(Part.makeCylinder(11,2,footbase,up))
 ballcenter=V(x,y,z(y)-7)
 hardware[f'FrontLanding{side}_SwivelJoint']=tf(Part.makeSphere(4,ballcenter))
 hardware[f'FrontLanding{side}_AdjusterStem']=tf(cyl(x,y,z(y)-7-L['adjuster_stem_length_reference_mm'],4,L['adjuster_stem_length_reference_mm']))
 # Blind M6 receiver is a separate interface reference. M025 stays byte/shape
 # equivalent; its pilot/bore is explicitly not represented as released CNC.
 receiver=ring(x,yy,z(yy),5,3.05,10)
 moving_receivers[f'FrontLanding{side}_RetentionReceiver']=tf(receiver)
 refs[f'FrontLanding{side}_RetentionBlindBore']=tf(cyl(x,yy,z(yy),5,T['maximum_blind_drill_depth_mm']))
 toe=z(yy)+7;underhead=toe-T['underhead_reference_mm']
 ret={
  f'FrontLanding{side}_RetentionBolt':cyl(x,yy,underhead,3,100).fuse(hexagon(x,yy,underhead-4,10,4)),
  f'FrontLanding{side}_RetentionWasher':ring(x,yy,zbot-1.6,7,3.2,1.6),
  f'FrontLanding{side}_RetentionJamnut1':hexagon(x,yy,zbot-4.8,10,3.2,3.05),
  f'FrontLanding{side}_RetentionJamnut2':hexagon(x,yy,zbot-8,10,3.2,3.05),
  f'FrontLanding{side}_RetentionPushRing':ring(x,yy,ztop+10.5,4.5,3.0,1.0)}
 for name,s in ret.items():hardware[name]=tf(s);release_names.append(name)
 # The small ring stays on the bolt; on release its lower face lands on body.

new={**old,**wood,**hardware,**moving_receivers}
released=dict(new)
for name in release_names:
 q=new[name].copy();q.translate(V(0,0,-T['release_drop_mm']));released[name]=q
checks=[]
def ck(name,value,details=None):
 checks.append({'name':name,'pass':bool(value),'detail':details});print(name,bool(value),flush=True)
ck('earliest simple body derived by full search',selected['pad_y_mm']==245,selected)
ck('all six new wood members valid single18mm solids',len(wood)==6 and all(s.isValid() and len(s.Solids)==1 and abs(s.BoundBox.ZLength-18)<1e-6 for s in wood.values()))
ck('all current source objects identical',all(new[name] is s for name,s in old.items()))
ck('old source file unchanged',hashlib.sha256(source.read_bytes()).hexdigest()==sourcehash)
ck('body sides directly contact structural sides',all(sum(f.common(sf).Area for f in wood[f'FrontLanding{side}_Layer{j}'].Faces for sf in old['SIDE_'+side].Faces)>100 for side in ['L','R'] for j in [1,2,3]))
contact=[]
for side in ['L','R']:
 pad=hardware[f'FrontLanding{side}_ContactPad'];area=sum(f.common(bottom).Area for f in pad.Faces)
 ringface=max([f for f in pad.Faces if type(f.Surface).__name__=='Plane' and f.normalAt(0,0).z>.5],key=lambda f:f.Area)
 contact.append({'side':side,'center_xyz_mm':[x if side=='L' else 600-x,y,z(y)],'area_mm2':area,'base_penetration_mm3':pad.common(base).Volume,'outer_edge_gap_mm':ringface.distToShape(bottom.OuterWire)[0]})
ck('two full intentional pads with zero penetration',all(abs(r['area_mm2']-math.pi*144)<1e-5 and r['base_penetration_mm3']<1e-5 for r in contact),contact)
report={'pass':all(q['pass'] for q in checks),'checks':checks,'manufacturing_release':False,
 'source':str(source.relative_to(R)),'source_sha256':sourcehash,'search':search,'selected':selected,
 'new_wood_names':list(wood),'new_hardware_names':list(hardware)+list(moving_receivers),
 'moving_receiver_names':list(moving_receivers),'retention_release_names':release_names,
 'current_shapes_changed':[],'reference_holes_not_cut_in_current':list(refs),
 'contacts':contact,'body_bounds':{side:bb(Part.makeCompound([s for name,s in wood.items() if name.startswith('FrontLanding'+side)])) for side in ['L','R']},
 'wood_volume_mm3':sum(s.Volume for s in wood.values()),'wood_mass_kg_at650':sum(s.Volume for s in wood.values())*650/1e9,
 'side_attachment':{'quantity':8,'embedment_mm':12,'remaining_exterior_skin_mm':6,'row_separation_mm':36,'longitudinal_pitch_mm':52,'minimum_body_center_edge_mm':9,'status':'PROVISIONAL_PHYSICAL_QUALIFICATION_REQUIRED'},
 'retention':{'receiver_axis_y_mm':yy,'receiver_z_mm':z(yy),'nominal_underhead_z_mm':underhead,'nominal_hex_head_z_range_mm':[underhead-4,underhead],
              'nominal_body_to_underhead_gap_mm':zbot-underhead,'jamnut_washer_stack_mm':8,'release_mm':10.5,'engagement_mm':7,
              'receiver_hole_depth_limit_mm':T['maximum_blind_drill_depth_mm'],'current_base_nominal_thickness_mm':18,'source_base_bore_status':'UNCUT_REFERENCE_PURCHASE_BEFORE_CNC',
              'minimum_nominal_skin_vertical_mm':18/up.z-5*abs(up.y/up.z)-T['maximum_blind_drill_depth_mm'],
              'jamnut_stop_must_be_reset_after_leveling':True},
 'adjustment':{},'holds':['actual foot articulation/diameters','actual inserts/pilots/side screws','actual retention stack and blind depth','coupon and lot thickness','physical load and ergonomic qualification']}
for travel in [3,5]:
 # At fixed X/Y, the rear-axis rotation changes retention height slightly
 # less than pad height because its lever is30 mm shorter.
 ratio=(PF.y-yy)/(PF.y-y);minheadgap=zbot-underhead-travel*ratio
 report['adjustment'][str(travel)]={'plus_minus_mm':travel,'rear_axis_slope_delta_deg_approx':math.degrees(math.atan(travel/(PF.y-y))),
  'left_right_independent_level_delta_deg_approx':math.degrees(math.atan(2*travel/(600-2*x))),
  'minimum_head_to_jamnut_stack_gap_mm_approx':minheadgap-8,
  'stack_pass':minheadgap>=8+.2,'selected':travel==3,'hardware_hold':True}
ck('plusminus3 retained and5 rejected by100mm retentionstack',report['adjustment']['3']['stack_pass'] and not report['adjustment']['5']['stack_pass'],report['adjustment'])
report['pass']=all(q['pass'] for q in checks)
for label,ss in [('play',new),('released',released),('study',refs|access)]:
 d=A.newDocument('V3363_'+label);d.addProperty('App::PropertyString','Authority');d.Authority='DESIGN CANDIDATE; hardware measured before CNC; no manufacturing release'
 for name,s in ss.items():
  ob=d.addObject('PartDesign::Feature',name);ob.Shape=s
  if name not in old:ob.addProperty('App::PropertyString','HardwareAuthority');ob.HardwareAuthority='PROVISIONAL PACKAGING; PURCHASE_BEFORE_CNC; no final drilling'
 d.recompute();d.saveAs(str(O/(label+'.FCStd')));A.closeDocument(d.Name)
allnew=wood|hardware|moving_receivers
for name,s in (allnew|refs).items():s.exportBrep(str(O/'brep'/(name+'.brep')))
meshes={}
for name,s in allnew.items():
 vv,ff=s.tessellate(.25);meshes[name]={'vertices':[list(v) for v in vv],'faces':ff}
(O/'additions-mesh.json.gz').write_bytes(gzip.compress(json.dumps(meshes,separators=(',',':')).encode(),mtime=0))
report['part_properties']={name:{'bounds_mm':bb(s),'volume_mm3':s.Volume,'solid_count':len(s.Solids),'valid':s.isValid()} for name,s in allnew.items()}
(O/'geometry-validation.json').write_text(json.dumps(report,indent=2)+'\n')
viewer={'playfield_moving_names':list(pf_names(old))+list(moving_receivers),
        'fixed_landing_names':list(wood)+list(hardware),'retention_moving_names':release_names,
        'release_translation_xyz_mm':[0,0,-10.5],'released_native_file':'released.FCStd',
        'release_requires_rotation':True,'release_rotation_description':'Unscrew M6 bolt; coarse model displays axial travel without helical threads.',
        'closing':{'validated':False,'initial_open_angle_deg':2,'initial_lift_mm':48,'sequence':['SEAT_REAR','LOWER_FRONT','ENGAGE_RETENTION']},
        'status':'AWAITING_NATIVE_MOTION_VALIDATION'}
(O/'viewer-motion.json').write_text(json.dumps(viewer,indent=2)+'\n')
assert report['pass'],checks
print('V3363_NATIVE_DONE',len(checks),flush=True)
