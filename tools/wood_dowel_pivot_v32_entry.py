"""Owner final wooden lift-out pivot only. CERN-OHL-S-2.0."""
import FreeCAD as A
import Part
import json, math, hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]; O=R/'exports/generated/wood-dowel-pivot-v32'; O.mkdir(parents=True,exist_ok=True)
c=json.loads((R/'config/wood_dowel_pivot_v32.json').read_text()); V=A.Vector
source=R/'exports/generated/service-correction-v32/play.FCStd'
d=A.openDocument(str(source));d.recompute()
original={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')}
old=json.loads((R/'exports/generated/service-correction-v32/validation.json').read_text())['review']
retired=[n for n in original if n.startswith('PF_') and n!='PF_BackboxCheckEnvelope' or n.startswith('MONITOR_')]
scene={n:s.copy() for n,s in original.items() if n not in retired}
def box(x,y,z,dx,dy,dz):return Part.makeBox(dx,dy,dz,V(x,y,z))
def cyl(x,y,z,r,h):return Part.makeCylinder(r,h,V(x,y,z),V(1,0,0))
def diff(a,b):return a.cut(b).Volume+b.cut(a).Volume
# Remove only holes owned by rejected pivot; preserve buttons and all other cuts.
for side,x in [('L',0),('R',582)]:
 s=scene['SIDE_'+side]
 for y,z,r in [(*old['pivot_xyz_mm'][1:],5.25),(*old['receiver_yz_mm'],4.25)]:s=s.fuse(cyl(x,y,z,r,18)).removeSplitter()
 scene['SIDE_'+side]=s
alpha=math.radians(old['closed_slope_deg']); bz=400.05+45*math.tan(alpha)-12-55*math.cos(alpha)
def tf(s):
 s=s.copy();s.rotate(V(),V(1,0,0),math.degrees(alpha));s.translate(V(0,45,bz));return s
r=c['wood_dowel_diameter_mm']/2; ay=c['axis_local_y_mm']; az=c['base_bottom_local_z_mm']-r
pivot=tf(Part.Vertex(V(300,ay,az))).Vertexes[0].Point
py,pz=pivot.y,pivot.z
scene['PF_BasePlywood']=tf(box(c['base_x_mm'],20,c['base_bottom_local_z_mm'],c['base_width_mm'],c['base_length_mm'],18))
scene['PF_WoodDowel']=cyl(20,py,pz,r,560)
# VESA reference envelope directly on the single flat base, not pivot hardware.
scene['PF_VESAEnvelope']=tf(box(200,360,4,200,250,8))
# Actual fixed obstacles define the narrow floor-bearing foot and the wider upper ear.
rr=r+c['cradle_radial_clearance_mm'];w=c['cradle_width_y_mm'];floor_top=scene['FLOOR'].BoundBox.ZMax
top_z=pz+c['cradle_top_above_axis_mm'];seat_cz=pz+c['cradle_radial_clearance_mm'];seat_bottom=seat_cz-rr
foot_front=scene['SHELF_SUPPORT_3L'].BoundBox.YMax+c['cradle_edge_clearance_mm']
shoulder_z=scene['CROSS_GUIDE_3L'].BoundBox.ZMax+c['cradle_guide_clearance_mm']
rear_y=py+w/2
assert foot_front<py-rr and shoulder_z<top_z
points=[V(18,foot_front,floor_top),V(18,rear_y,floor_top),V(18,rear_y,top_z),V(18,py-w/2,top_z),V(18,py-w/2,shoulder_z),V(18,foot_front,shoulder_z)]
raw=Part.Face(Part.makePolygon(points+[points[0]])).extrude(V(18,0,0))
raw=raw.cut(cyl(17,py,seat_cz,rr,20)).cut(box(17,py-rr,seat_cz,20,2*rr,top_z-seat_cz+1)).removeSplitter()
exciter=scene['SSF_Exciter2L'].BoundBox;gap=c['cradle_edge_clearance_mm']
raw=raw.cut(box(17,exciter.YMin-gap,exciter.ZMin-gap,20,exciter.YLength+2*gap,exciter.ZLength+2*gap)).removeSplitter()
f=c['fixing'];edge=f['edge_distance_mm'];z_low=max(floor_top+edge,scene['PC_ENVELOPE'].BoundBox.ZMax+8+c['cradle_edge_clearance_mm']);z_high=seat_bottom-edge
screw_z=[z_low,(z_low+z_high)/2,z_high];screw_rows=[]
for i,z in enumerate(screw_z):
 section=raw.common(box(17,py-w, z-.001,20,2*w,.002)).BoundBox
 # Stagger the low/mid/high centres over the available section, preserving edge distance.
 y=[section.YMin+edge,(section.YMin+section.YMax)/2,section.YMax-edge][i]
 assert section.YMin+edge<=y<=section.YMax-edge
 screw_rows.append((y,z))
cs_depth=(f['head_diameter_mm']-f['clearance_diameter_mm'])/(2*math.tan(math.radians(f['head_angle_deg']/2)))
support=raw.copy();mount_screws=[];fixing_positions=[]
for i,(y,z) in enumerate(screw_rows,1):
 support=support.cut(cyl(17,y,z,f['clearance_diameter_mm']/2,20))
 support=support.cut(Part.makeCone(f['clearance_diameter_mm']/2,f['head_diameter_mm']/2,cs_depth,V(36-cs_depth,y,z),V(1,0,0)))
 tip_x=36-f['screw_length_mm'];head_depth=(f['head_diameter_mm']-f['screw_diameter_mm'])/2
 screw=Part.makeCone(0,f['screw_diameter_mm']/2,2,V(tip_x,y,z),V(1,0,0)).fuse(cyl(tip_x+2,y,z,f['screw_diameter_mm']/2,36-head_depth-tip_x-2))
 screw=screw.fuse(Part.makeCone(f['screw_diameter_mm']/2,f['head_diameter_mm']/2,head_depth,V(36-head_depth,y,z),V(1,0,0))).removeSplitter()
 # Cross/Torx-like recess is a visual drive cue, not a vendor model.
 screw=screw.cut(cyl(35,y,z,1.5,2)).removeSplitter()
 mirror=A.Matrix();mirror.A11=-1;mirror.A14=600
 for side in ('L','R'):
  sh=screw.copy()
  if side=='R':sh.transformShape(mirror,True)
  name=f'PF_SupportMountScrew{side}{i}';scene[name]=sh;mount_screws.append(name)
  sx=18-f['cnc_pilot_depth_mm'] if side=='L' else 582
  scene['SIDE_'+side]=scene['SIDE_'+side].cut(cyl(sx,y,z,f['pilot_diameter_mm']/2,f['cnc_pilot_depth_mm'])).removeSplitter()
  fixing_positions.append({'id':name,'head_xyz_mm':[36 if side=='L' else 564,y,z],'tip_xyz_mm':[tip_x if side=='L' else 600-tip_x,y,z],'side_pilot_xyz_mm':[18 if side=='L' else 582,y,z],'axis':[-1,0,0] if side=='L' else [1,0,0]})
scene['PF_OpenCradleL']=support.removeSplitter();right=support.copy();right.transformShape(mirror,True);scene['PF_OpenCradleR']=right
# Recess only the approved rear door/hardware; the upper fixed fans and I/O remain untouched.
rear_plane=scene['REAR'].BoundBox.YMax;door_before=scene['REAR_DOOR'].copy();door_delta=rear_plane-c['rear_door_outer_recess_mm']-door_before.BoundBox.YMax
rear_ids=[n for n in scene if n=='REAR_DOOR' or n.startswith(('CandidateRearHandle','CandidateHandleBolt','CandidateHinge','CandidateKeyLock','CandidateLockKeeper'))]
rear_original={n:scene[n].copy() for n in rear_ids}
for n in rear_ids:scene[n].translate(V(0,door_delta,0))
# Reuse the existing flat strike keeper on the underside of the rear header.
# Its unchanged 20 x 24 x 2 envelope is rotated, not replaced by a new part.
keeper=scene['CandidateLockKeeper'];kc=keeper.BoundBox.Center;keeper.rotate(kc,V(1,0,0),-90)
kb=keeper.BoundBox;keeper.translate(V(0,1285.1+door_delta+1-kb.YMin,385-kb.ZMin))
keeper_expected=keeper.copy()
door_bounds=scene['REAR_DOOR'].BoundBox
scene['REAR']=scene['REAR'].cut(box(door_bounds.XMin-1,scene['REAR'].BoundBox.YMin-1,door_bounds.ZMin-1,door_bounds.XLength+2,scene['REAR'].BoundBox.YLength+2,door_bounds.ZLength+2)).removeSplitter()
# Existing inset opening and hinge mounting seats; remove only wood occupied by the existing parts.
rear_removed=[]
for n in rear_ids:
 vol=scene['REAR'].common(scene[n]).Volume
 if vol>.01:
  scene['REAR']=scene['REAR'].cut(scene[n]).removeSplitter();rear_removed.append({'part':n,'removed_mm3':vol})
# Four purchased saddle straps, each two ears and a lower semicircular band.
for i,x in enumerate(c['strap_x_mm'],1):
 band=cyl(x,ay,az,r+1.5,12).cut(cyl(x-1,ay,az,r,14)).common(box(x-1,ay-r-2,az-r-2,14,2*r+4,r+2))
 strap=band
 for sign in (-1,1):
  ey=ay+sign*(r+8)-7
  strap=strap.fuse(box(x,ey,az,12,14,r)).fuse(box(x,ey,az+r-1.5,12,14,1.5))
  # screw clearances through ears, screws extend into plywood only.
  sy=ay+sign*(r+8)
  hole=Part.makeCylinder(2,5,V(x+6,sy,az+r-3),V(0,0,1));strap=strap.cut(hole)
  screw=Part.makeCylinder(1.7,12,V(x+6,sy,az+r-2),V(0,0,1))
  screw=screw.fuse(Part.makeCylinder(3.2,2,V(x+6,sy,az+r-4),V(0,0,1))).removeSplitter()
  scene[f'PF_StrapScrew{i}_{sign+2}']=tf(screw)
 scene[f'PF_CommercialStrap{i}']=tf(strap.removeSplitter())
moving=[n for n in scene if n.startswith('PF_') and n not in ('PF_OpenCradleL','PF_OpenCradleR','PF_BackboxCheckEnvelope') and not n.startswith('PF_SupportMountScrew')]+['PLAYFIELD_ENVELOPE']
def rot(s,angle):
 s=s.copy();s.rotate(pivot,V(1,0,0),-angle);return s
reservations={n for n in scene if any(t in n for t in ('Reserve','RESERVED','CandidatePayload'))}
fixed={n:s for n,s in scene.items() if n not in moving and n not in reservations and n!='CandidateGlass'}
def hits(parts,obs):
 out=[]
 for n,s in parts.items():
  for k,t in obs.items():
   if s.BoundBox.intersect(t.BoundBox):
    vol=s.common(t).Volume
    if vol>0.01:out.append([n,k,round(vol,4)])
 return out
checks=[]
def check(n,v):checks.append({'check':n,'pass':bool(v)});print(n,v,flush=True)
sweep=[]
for angle in range(0,int(c['service_angle_deg'])+1,2):
 h=hits({n:rot(scene[n],angle) for n in moving},fixed);sweep.append({'angle':angle,'hits':h})
check('configured opening sweep no collisions at 2 degree samples',not any(s['hits'] for s in sweep))
raised={n:rot(scene[n],c['service_angle_deg']) for n in moving}
lift=[]
for dz in range(0,int(c['lift_out_mm'])+1,2):
 parts={n:scene[n].copy() for n in moving}
 for s in parts.values():s.translate(V(0,0,dz))
 lift.append({'dz':dz,'hits':hits(parts,fixed)})
check('vertical lift out of open cradles no collisions',not any(s['hits'] for s in lift))
check('dowel clears cradle upper edges after lift',pz-r+c['lift_out_mm']>top_z)
support_conflicts=hits({n:scene[n] for n in ('PF_OpenCradleL','PF_OpenCradleR')},{n:s for n,s in fixed.items() if n not in ('PF_OpenCradleL','PF_OpenCradleR') and n not in mount_screws})
print('SUPPORT_CONFLICTS',support_conflicts,flush=True)
check('two floor supported cradles clear unchanged cabinet',not hits({n:scene[n] for n in ('PF_OpenCradleL','PF_OpenCradleR')},{n:s for n,s in fixed.items() if n not in ('PF_OpenCradleL','PF_OpenCradleR') and n not in mount_screws}))
# Fixing geometry and assembly checks; contact loads go straight to the floor.
check('six internal support mounting screws only',len(mount_screws)==6)
check('floor bearing exists on both supports',all(abs(scene['PF_OpenCradle'+side].BoundBox.ZMin-floor_top)<1e-6 for side in ('L','R')))
check('nominal screw engagement and exterior skin',f['screw_length_mm']-18>=10 and 36-f['screw_length_mm']>=4)
check('pilot stops short of outside face',0<f['cnc_pilot_depth_mm']<f['pilot_finished_depth_mm']<=f['pilot_max_depth_mm']<=18-3)
check('countersink preserves useful thickness',18-cs_depth>=15 and f['head_diameter_mm']>f['clearance_diameter_mm'])
check('screw centres spaced and below weakened U',all(math.hypot(a[0]-b[0],a[1]-b[1])>=f['minimum_spacing_mm'] for a,b in zip(screw_rows,screw_rows[1:])) and max(z for y,z in screw_rows)<=seat_bottom-edge)
check('no pilot penetrates exterior skin',all(scene['SIDE_'+side].isInside(V(x,y,z),1e-6,True) for side,x in [('L',3),('R',597)] for y,z in screw_rows))
check('support mounting screw and head geometry clear other components',not hits({n:scene[n] for n in mount_screws},{n:s for n,s in scene.items() if n not in mount_screws and n not in ('SIDE_L','SIDE_R','PF_OpenCradleL','PF_OpenCradleR') and n not in reservations}))
tool_probes={}
for row in fixing_positions:
 x,y,z=row['head_xyz_mm'];direction=V(-row['axis'][0],0,0)
 tool_probes[row['id']]=Part.makeCylinder(8,150,V(x,y,z),direction)
tool_hits=hits(tool_probes,{n:s for n,s in scene.items() if n not in mount_screws and n not in ('PF_OpenCradleL','PF_OpenCradleR') and n not in reservations and n!='CandidateGlass'})
check('direct interior driver access to all six screws',not tool_hits)
check('rear door outer wood face flush or recessed',scene['REAR_DOOR'].BoundBox.YMax<=rear_plane+1e-6)
check('approved rear hardware preserved by rigid placements',all(diff(scene[n],(lambda q:(q.translate(V(0,door_delta,0)),q)[1])(rear_original[n].copy()))<1e-5 for n in rear_ids if n!='CandidateLockKeeper') and abs(keeper.Volume-rear_original['CandidateLockKeeper'].Volume)<1e-5)
# Confirm the approved keyed door still opens downward with the same hinges.
rear_moving=[n for n in rear_ids if not n.startswith(('CandidateHingeFixed','CandidateHingePin','CandidateLockKeeper'))]
rear_obs={n:s for n,s in scene.items() if n not in rear_moving and n not in reservations}
lock_axis=V(450,1285.1+door_delta,350)
unlocked={n:scene[n].copy() for n in rear_moving};unlocked['CandidateKeyLockCam'].rotate(lock_axis,V(0,1,0),-90)
rear_axis=V(300,1324.1+door_delta,54);rear_sweep=[]
locked_cam=scene['CandidateKeyLockCam'].copy();locked_cam.rotate(rear_axis,V(1,0,0),-2)
check('same lock keeper blocks opening while cam remains locked',bool(hits({'locked_cam':locked_cam},{'keeper':scene['CandidateLockKeeper']})))
for angle in range(0,111,2):
 pose={n:s.copy() for n,s in unlocked.items()}
 for sh in pose.values():sh.rotate(rear_axis,V(1,0,0),-angle)
 rear_sweep.append({'angle':angle,'hits':hits(pose,rear_obs)})
check('flush downward door sweep 0..110 degrees clear',not any(row['hits'] for row in rear_sweep))
print('REAR_COLLISIONS',[row for row in rear_sweep if row['hits']][:5],flush=True)

check('all solids valid',all(s.isValid() and len(s.Solids)==1 for s in scene.values()))
preserved=[n for n in original if n not in retired+['SIDE_L','SIDE_R','REAR']+rear_ids]
check('all subsystems other than authorized support pilots and rear door correction preserved',all(diff(original[n],scene[n])<1e-5 for n in preserved))
poses={'PLAY':scene,'SERVICE':{n:(raised[n] if n in raised else s) for n,s in scene.items() if n!='CandidateGlass'}}
poses['LIFT-OUT']={n:s.copy() for n,s in scene.items() if n!='CandidateGlass'}
for n in moving:poses['LIFT-OUT'][n].translate(V(0,0,c['lift_out_mm']))
# Exploded mechanism contains only requested pivot pieces (TV/VESA omitted).
mechanism=[n for n in moving if n not in ('PLAYFIELD_ENVELOPE','PF_VESAEnvelope')]+['PF_OpenCradleL','PF_OpenCradleR']+mount_screws
exploded={n:scene[n].copy() for n in mechanism}
for n,s in exploded.items():
 if n in mount_screws:s.translate(V(60 if 'ScrewL' in n else -60,0,0))
 dz=160 if n=='PF_BasePlywood' else 105 if 'Strap' in n else 50 if n=='PF_WoodDowel' else 0
 s.translate(V(0,0,dz))
poses['EXPLODED']=exploded
(O/'diagnostic.json').write_text(json.dumps({'checks':checks,'sweep':sweep,'lift':lift,'rear_sweep':rear_sweep,'support_conflicts':support_conflicts,'tool_hits':tool_hits,'fixing_positions':fixing_positions},indent=2))
assert all(x['pass'] for x in checks),checks
saved={}
for state,pose in poses.items():
 out=A.newDocument('WoodPivot_'+state.replace('-','_'));out.Comment='CERN-OHL-S-2.0; Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet; owner final pivot correction; manufacturing not approved'
 sheet=out.addObject('Spreadsheet::Sheet','PivotParameters');sheet.set('A1',str(c['wood_dowel_diameter_mm']));sheet.setAlias('A1','DowelDiameter')
 for n,s in pose.items():
  if n=='PF_WoodDowel':
   o=out.addObject('Part::Cylinder',n);o.Height=560;o.setExpression('Radius','PivotParameters.DowelDiameter / 2');o.Placement=A.Placement(V(20,py,pz+(50 if state=='EXPLODED' else c['lift_out_mm'] if state=='LIFT-OUT' else 0)),A.Rotation(V(0,0,1),V(1,0,0)))
  else:o=out.addObject('PartDesign::Feature',n);o.Shape=s
  o.addProperty('App::PropertyString','PartID');o.PartID=n
 out.recompute();path=O/(state.lower()+'.FCStd');out.saveAs(str(path));A.closeDocument(out.Name)
 out=A.openDocument(str(path));out.recompute()
 check(state+' saved CAD recompute and solid equivalence',all(o.Shape.isValid() and diff(o.Shape,pose[o.Name])<1e-4 for o in out.Objects if hasattr(o,'Shape')))
 if state=='PLAY':Part.export([o for o in out.Objects if hasattr(o,'Shape') and o.Name!='PF_BackboxCheckEnvelope'],str(O/'current-v32.step'))
 saved[state]=str(path.relative_to(R));A.closeDocument(out.Name)
step=O/'current-v32.step';step.write_text('\n'.join(line.rstrip() for line in step.read_text().splitlines())+'\n')
def mesh(n,s):
 vs,fs=s.tessellate(.7);return {'name':n,'vertices':[[v.x,v.y,v.z] for v in vs],'faces':[list(f) for f in fs]}
review={k:old[k] for k in ('buttons','closed_slope_deg','structural_proof','manufacturing_ready')};review.update({'pivot_xyz_mm':[300,py,pz],'opening_deg':c['service_angle_deg'],'wood_dowel_diameter_mm':2*r,'cradle_coordinates_mm':[[18,py,36],[564,py,36]],'cradle_seat_axis_xyz_mm':[[27,py,pz],[573,py,pz]],'lift_out_mm':c['lift_out_mm'],'lift_out_clearance_mm':c['lift_out_mm']-r-c['cradle_top_above_axis_mm'],'support_profile_width_before_mm':24,'support_profile_width_after_mm':w,'cradle_depth_before_mm':5.176,'cradle_depth_after_mm':top_z-seat_bottom,'support_mounting':{'positions':fixing_positions,'screw':f,'countersink_depth_mm':cs_depth,'side_engagement_mm':f['screw_length_mm']-18,'side_remaining_beyond_tip_mm':36-f['screw_length_mm'],'minimum_lift_to_clear_mm':r+c['cradle_top_above_axis_mm'],'foot_y_min_mm':foot_front,'foot_y_max_mm':rear_y,'shoulder_z_mm':shoulder_z},'rear_flush':{'before_outer_y_mm':door_before.BoundBox.YMax,'after_outer_y_mm':scene['REAR_DOOR'].BoundBox.YMax,'plane_y_mm':rear_plane,'translation_y_mm':door_delta,'wood_recesses':rear_removed},'custom_metal_parts_required':0,'commodity_metal_parts':18,'commodity_metal_ids':[n for n in scene if 'Strap' in n or n in mount_screws],'counts':{'PLAYFIELD PIVOT CUSTOM METAL PARTS':0,'PLAYFIELD PIVOT BEARINGS':0,'PLAYFIELD PIVOT BUSHINGS':0,'PLAYFIELD PIVOT STEEL RODS':0,'PLAYFIELD PIVOT WOOD DOWELS':1,'PLAYFIELD PIVOT CNC WOOD SUPPORTS':2,'PLAYFIELD BASE PLYWOOD PANELS':1,'COMMERCIAL STRAPS':4,'STRAP SCREWS':8,'SUPPORT MOUNTING SCREWS':6,'TOTAL METAL PARTS IN PLAYFIELD PIVOT SYSTEM':18},'limits':'Sampled geometry only; no load proof. Commercial strap envelope provisional. Owner final architecture supersedes previous prop requirements.'})
# 40 mm lift clears tangent dowel bottom at z+24: equality, add margin below.
bundle={'parts':[mesh(n,s) for n,s in scene.items()],'states':{},'review':review}
for state,pose in poses.items():bundle['states'][state]={n:mesh(n,pose[n]) if n in pose else None for n in scene if n not in pose or diff(scene[n],pose[n])>1e-5}
(O/'mesh.json').write_text(json.dumps(bundle))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'checks':checks,'review':review,'saved_poses':saved,'retired_objects':retired,'preserved_solids':preserved,'source_sha256':sha(source),'mesh_sha256':sha(O/'mesh.json'),'manufacturing_ready':False}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
for n in ('LICENSE','NOTICE.md'):(O/n).write_bytes((R/n).read_bytes())
assert all(x['pass'] for x in checks)
print('WOOD_PIVOT_PASS',flush=True)
