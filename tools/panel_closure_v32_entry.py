"""V32 closure interfaces; original geometry. CERN-OHL-S-2.0. Not manufacturing release."""
import hashlib,json,math
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/panel-closure-v32';O.mkdir(parents=True,exist_ok=True)
cp=R/'config/panel_closure_v32.json';c=json.loads(cp.read_text());rp=R/c['source_report'];r=json.loads(rp.read_text());sp=R/r['saved_proposal']['path']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(sp)==r['saved_proposal']['sha256'];assert all(i['pass'] for i in r['checks'])
inputs={str(p.relative_to(R)):sha(p) for p in [cp,rp,sp,Path(__file__).resolve(),R/'config/shelf_layout_freeze_v32.json',R/'exports/generated/side-panel-v32/simple-shelves-validation.json',R/'exports/generated/side-panel-v32/shelf-service-pose-screen.json']}
d=A.openDocument(str(sp));d.recompute();scene={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};base={n:s.copy() for n,s in scene.items()};checks=[];new={}
def check(n,v): checks.append({'check':n,'pass':bool(v)})
def box(x,y,z,dx,dy,dz):return Part.makeBox(dx,dy,dz,A.Vector(x,y,z))
def hits(parts,obs):
 out=[]
 for n,s in parts.items():
  for k,t in obs.items():
   if s.BoundBox.intersect(t.BoundBox):
    v=s.common(t).Volume
    if v>.01:out.append({'part':n,'obstacle':k,'mm3':v})
 return out
b=c['body'];g=c['glass_study'];angle=math.atan2(b['rear_height_mm']-b['front_height_mm'],b['slope_end_y_mm']);y0=g['front_y_mm'];z0=b['front_height_mm']+y0*math.tan(angle);width=b['width_mm'];gx=(width-g['width_mm'])/2;length=g['length_on_slope_mm'];gz=g['bottom_normal_offset_mm']
def tf(s):
 s=s.copy();s.rotate(A.Vector(),A.Vector(1,0,0),math.degrees(angle));s.translate(A.Vector(0,y0,z0));return s
new['CandidateGlass']=tf(box(gx,0,gz,g['width_mm'],length,g['thickness_mm']))
# Replaceable surface channel section. No side-wall pocket or additional shell hole.
edge=gx-g['channel_clearance_each_side_mm'];inner=b['plywood_mm'];height=gz+g['thickness_mm']+1
rail=box(0,0,0,inner,length,2).fuse(box(edge,0,2,inner-edge,length,gz-2)).fuse(box(edge-2,0,2,2,length,height-1)).fuse(box(edge,0,height,inner-edge,length,1)).removeSplitter()
new['CandidateGlassChannelL']=tf(rail)
reflection=A.Matrix();reflection.A11=-1;reflection.A14=width
new['CandidateGlassChannelR']=new['CandidateGlassChannelL'].transformGeometry(reflection)
installed=hits(new,scene)
for n,s in new.items():installed+=hits({n:s},{k:t for k,t in new.items() if k>n})
check('glass and channel installed candidate clearance',not installed)
check('glass channel right mirrors left',new['CandidateGlassChannelL'].transformGeometry(reflection).cut(new['CandidateGlassChannelR']).Volume<1e-6)
check('channel engagement each side',abs(inner-gx-g['channel_engagement_each_side_mm'])<1e-6)
# Continuous conservative union for a rectangular glass sheet translated along its plane.
travel=length+50;sweep=tf(box(gx,-travel,gz,g['width_mm'],length+travel,g['thickness_mm']))
glass_route=hits({'glass_forward_sweep':sweep},{**scene,**{n:s for n,s in new.items() if n!='CandidateGlass'}})
check('continuous glass forward withdrawal without lockdown',not glass_route)
# Negative: lowering the same glass five normal mm must intersect shell/channel.
wrong=tf(box(gx,0,gz-5,g['width_mm'],length,g['thickness_mm']))
check('reject lowered glass stack',bool(hits({'lowered_glass':wrong},{**scene,**{n:s for n,s in new.items() if n!='CandidateGlass'}})))
shelf=json.loads((R/'exports/generated/side-panel-v32/simple-shelves-validation.json').read_text());routes=[]
for route in shelf['routes']:
 moving={n:scene[n].copy() for n in route['moving']}
 for xyz in route['translations_mm']:
  v=A.Vector(*xyz)
  for n,s in moving.items():
   bb=s.BoundBox;sw=box(bb.XMin+min(v.x,0),bb.YMin+min(v.y,0),bb.ZMin+min(v.z,0),bb.XLength+abs(v.x),bb.YLength+abs(v.y),bb.ZLength+abs(v.z));routes+=hits({n:sw},{k:t for k,t in new.items() if 'Channel' in k});s.translate(v)
check('frozen shelf removal clears side channels after glass removal',not routes)
pose=json.loads((R/'exports/generated/side-panel-v32/shelf-service-pose-screen.json').read_text());display=[]
for a in range(0,101,2):
 moving={n:scene[n].copy() for n in shelf['config']['playfield_assembly']}
 for s in moving.values():s.rotate(A.Vector(*pose['pivot_xyz_mm']),A.Vector(1,0,0),-a)
 display+=hits(moving,{k:t for k,t in new.items() if 'Channel' in k})
check('sampled display opening clears channels with glass removed',not display)
# Rear cover preserves the existing opening for the owner-approved low fixed PC base.
rear=c['rear'];L=b['length_mm'];x,z,w,h=rear['cover_xzwh_mm'];th=rear['cover_thickness_mm']
def bore(x,y,z,r,depth):return Part.makeCylinder(r,depth,A.Vector(x,y,z),A.Vector(0,1,0))
cover=box(x,L,z,w,th,h)
for xx,zz in rear['cover_fasteners_xz_mm']:
 cover=cover.cut(bore(xx,L-1,zz,rear['fastener_clearance_mm']/2,th+2))
 # Receiving insert pilot intentionally uncut: exact SKU is deferred.
for xx,zz in rear['fan_centers_xz_mm']:
 cover=cover.cut(bore(xx,L-1,zz,rear['fan_opening_diameter_mm']/2,th+2))
 for dx in (-rear['fan_pitch_mm']/2,rear['fan_pitch_mm']/2):
  for dz in (-rear['fan_pitch_mm']/2,rear['fan_pitch_mm']/2):cover=cover.cut(bore(xx+dx,L-1,zz+dz,2.25,th+2))
 fan=scene['FAN_'+str(xx)].copy();fan.translate(A.Vector(0,18,0));scene['FAN_'+str(xx)]=fan
scene['REAR_DOOR']=cover
rear_group={n:scene[n] for n in ['REAR_DOOR','FAN_230','FAN_370']}
rear_obs={n:t for n,t in scene.items() if n not in rear_group}
rear_hits=hits(rear_group,rear_obs)
check('overlapping rear cover and fan frames clear installed scene',not rear_hits)
# Exact continuous fan/cover translation via extruded rearward boundary faces.
def swept_y(shape,travel):
 volumes=[shape]
 for f in shape.Faces:
  # Any nonzero face extrusion contributes to the swept union; side faces are skipped.
  try:
   v=f.extrude(A.Vector(0,travel,0))
   if v.Volume>1e-6:volumes.append(v)
  except Part.OCCError:pass
 return Part.makeCompound(volumes)
rear_route=hits({n:swept_y(t,rear['cover_withdrawal_mm']) for n,t in rear_group.items()},rear_obs)
check('rear cover continuous 150mm outward removal',not rear_route)
# PC route screens cover exceptional replacement only, not a routine removable tray.
def swept_box(shape,v):
 bb=shape.BoundBox
 return box(bb.XMin+min(v.x,0),bb.YMin+min(v.y,0),bb.ZMin+min(v.z,0),bb.XLength+abs(v.x),bb.YLength+abs(v.y),bb.ZLength+abs(v.z))
pc={n:scene[n].copy() for n in ['PC_BASE','PC_ENVELOPE']};pc_obs={n:t for n,t in scene.items() if n not in pc and n not in rear_group}
rejected=hits({n:swept_box(t,A.Vector(0,500,0)) for n,t in pc.items()},pc_obs)
check('reject straight rear withdrawal of current floor-level PC base',any(i['obstacle']=='REAR' for i in rejected))
pc_routes=[]
for xyz in [(0,0,38),(0,500,0)]:
 v=A.Vector(*xyz)
 pc_routes+=hits({n:swept_box(t,v) for n,t in pc.items()},pc_obs)
 for t in pc.values():t.translate(v)
check('current PC envelope lift38 then rear500 route screen',not pc_routes)
check('rear aperture and permanent shell unchanged',all(scene[n].cut(base[n]).Volume+base[n].cut(scene[n]).Volume<1e-6 for n in ['REAR','SIDE_L','SIDE_R','FRONT','FLOOR']))
scene.update(new)
check('all candidate and inherited solids valid',all(s.isValid() and len(s.Solids)==1 for s in scene.values()))
check('original panels and frozen shelves unchanged',all(scene[n].cut(s).Volume+s.cut(scene[n]).Volume<1e-6 for n,s in base.items() if n not in ['REAR_DOOR','FAN_230','FAN_370']))
out=A.newDocument('PanelClosureV32')
for n,s in scene.items():
 o=out.addObject('PartDesign::Feature',n);o.Shape=s;src=d.getObject(n);o.addProperty('App::PropertyString','PartCode');o.PartCode=getattr(src,'PartCode','') if src else '';o.Label=o.PartCode or n
 o.addProperty('App::PropertyString','ReviewStatus');o.ReviewStatus='STUDY - imported hardware and manufacturing checks deferred'
out.recompute();p=O/'panel-closure-study.FCStd';out.saveAs(str(p));A.closeDocument(out.Name);saved=A.openDocument(str(p));saved.recompute();actual={o.Name:o.Shape for o in saved.Objects if hasattr(o,'Shape')}
check('saved solids valid and identical',set(actual)==set(scene) and all(s.isValid() and len(s.Solids)==1 and s.cut(scene[n]).Volume+scene[n].cut(s).Volume<1e-5 for n,s in actual.items()))
check('preserved input hashes',all(sha(R/n)==h for n,h in inputs.items()))
mesh=[]
for n,s in actual.items():
 if n in new or n in ['SIDE_L','SIDE_R','FRONT','REAR','REAR_DOOR','PLAYFIELD_ENVELOPE','SHELF_1','SHELF_2','SHELF_3']:
  vs,fs=s.tessellate(1);mesh.append({'name':n,'vertices':[[v.x,v.y,v.z] for v in vs],'faces':fs})
(O/'mesh.json').write_text(json.dumps(mesh)+'\n')
report={'manufacturing_ready':False,'source_hashes':inputs,'config':c,'checks':checks,'installed_conflicts':installed,'glass_withdrawal_conflicts':glass_route,'shelf_conflicts':routes,'display_channel_conflicts':display,'rear_installed_conflicts':rear_hits,'rear_removal_conflicts':rear_route,'pc_lift38_then_rear500_conflicts':pc_routes,'pc_straight_exit_rejected':rejected,'glass_angle_deg':math.degrees(angle),'glass_withdrawal_mm':travel,'saved_proposal':{'path':str(p.relative_to(R)),'sha256':sha(p),'solids':len(actual)},'unverified':['Actual lockdown and receiver envelope, tongues, latch and mounting holes','Channel section fabrication, retention and glass edge finish; no glass order','Hinge and two captive props including load proof, harness and upper backbox','Low PC base selected; actual case/base fastening, positive restraint, cable and tool access remain unqualified', 'Rear cover threaded receivers, handles, fan guards/fastener bodies and tether not yet modeled','All original hardware and manufacturing qualifications remain open']}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
assert all(x['pass'] for x in checks),[x for x in checks if not x['pass']]
print('PANEL_CLOSURE_PASS',len(checks),'checks;',len(actual),'solids; NOT CNC RELEASE')
A.closeDocument(saved.Name);A.closeDocument(d.Name)
