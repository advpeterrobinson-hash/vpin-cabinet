"""Consolidated V32 drawing scene with Cleveland4.1 + subwoofer. CERN-OHL-S-2.0."""
import json,hashlib,math,shutil
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/consolidated-v32';O.mkdir(parents=True,exist_ok=True)
cp=R/'config/consolidated_audio_v32.json';c=json.loads(cp.read_text());rp=R/c['source_report'];r=json.loads(rp.read_text());sp=R/'exports/generated/floor-detail-v32/floor-detail.FCStd';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(sp)==r['saved_cad_sha256'] and all(v['pass'] for v in r['checks'])
inputs={str(p.relative_to(R)):sha(p) for p in (cp,rp,sp,Path(__file__).resolve())};d=A.openDocument(str(sp));d.recompute();scene={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};old={n:s.copy() for n,s in scene.items()};V=A.Vector;checks=[];new={};envelopes={};operations=[]
def check(n,v):checks.append({'check':n,'pass':bool(v)})
def box(a):return Part.makeBox(*a[3:],V(*a[:3]))
def cyl(x,y,z,rad,h,axis=(0,0,1)):return Part.makeCylinder(rad,h,V(x,y,z),V(*axis))
def conflicts(parts,obstacles,ignore=()):
 out=[]
 for n,s in parts.items():
  for k,t in obstacles.items():
   if n==k or k in ignore:continue
   if s.BoundBox.intersect(t.BoundBox):
    v=s.common(t).Volume
    if v>.01:out.append({'part':n,'obstacle':k,'mm3':v})
 return out
# Subwoofer front face downward; mounting flange supported on inner floor faceZ36.
s=c['subwoofer'];sx,sy=s['center_xy_mm'];scene['FLOOR']=scene['FLOOR'].cut(cyl(sx,sy,17,s['design_cutout_mm']/2,20));sholes=[]
for i in range(s['hole_count']):
 a=math.radians(s['first_hole_angle_deg_design']+360*i/s['hole_count']);x=sx+s['bolt_circle_mm']/2*math.cos(a);y=sy+s['bolt_circle_mm']/2*math.sin(a);sholes.append([x,y]);scene['FLOOR']=scene['FLOOR'].cut(cyl(x,y,17,s['wood_hole_diameter_mm_candidate']/2,20));operations.append({'part':'Floor','operation':'through_drill','center_xy_mm':[x,y],'diameter_mm':s['wood_hole_diameter_mm_candidate'],'status':'candidate_M5_on_reference_PCD'})
operations.append({'part':'Floor','operation':'through_cut','center_xy_mm':[sx,sy],'diameter_mm':s['design_cutout_mm'],'status':'143drawing_plus0.5design_clearance'})
# Conservative simplified hardware reservation, not copied third-party CAD.
new['SSF_Subwoofer_DCS165_Reference']=cyl(sx,sy,36,83.5,4).fuse(Part.makeCone(71.5,55,86,V(sx,sy,40)))
for x,y in sholes:new['SSF_Subwoofer_DCS165_Reference']=new['SSF_Subwoofer_DCS165_Reference'].cut(cyl(x,y,35,2.75,6))
envelopes['SSF_SubwooferService']=cyl(sx,sy,36,90,110)
# Local replaceable rigid carrier: no cross-cabinet tie, reference BST hardware inside.
b=c['bass_shaker'];bx,by=b['center_xy_mm'];px,py,pw,ph=b['mounting_plate_xywh_mm'];pt=b['mounting_plate_thickness_mm'];plate=box([px,py,36,pw,ph,pt])
for x,y in b['floor_anchor_holes_xy_mm']:
 cut=cyl(x,y,17,2.75,pt+20);plate=plate.cut(cut);scene['FLOOR']=scene['FLOOR'].cut(cut);operations.append({'part':'Floor','operation':'through_drill','center_xy_mm':[x,y],'diameter_mm':5.5,'status':'candidate_M5_carrier_anchor'})
new['SSF_BST_Carrier']=plate;new['SSF_BST1_Reference']=cyl(bx,by,48,80.5,62);envelopes['SSF_BSTService']=cyl(bx,by,48,85,65)
# Side-coupled IMS reservations. No mounting pilot dimensions invented.
e=c['exciters']
for i,(y,z) in enumerate(e['positions_yz_mm'],1):
 for side,face,axis in [('L',18,(1,0,0)),('R',582,(-1,0,0))]:
  tag=f'SSF_Exciter{i}{side}';mount=cyl(face,y,z,30,6,axis);body=cyl(face+axis[0]*6,y,z,29.55,29,axis);new[tag]=mount.fuse(body);envelopes[tag+'Service']=cyl(face,y,z,40,45,axis)
# Explicit supplier-size-independent reserves on frozen shelves.
scene.pop('AUDIO_STARTECH');scene.pop('SHELF_2_CandidatePayload');scene.pop('SHELF_3_CandidatePayload')
for name,key in [('SSF_AmplifierReserve','amplifier'),('SSF_PSUReserve','power_supply'),('SSF_USBReserve','sound_card')]:new[name]=box(c[key]['envelope_xyzwhd_mm'])
envelopes['SSF_AmpControlsService']=box(c['amplifier']['controls_service_xyzwhd_mm'])
# Generic base anchors only; chassis hardware belongs to the replaceable base.
p=c['pc_base']
for x,y in p['anchor_holes_xy_mm']:
 through=cyl(x,y,17,p['through_diameter_mm']/2,38);scene['FLOOR']=scene['FLOOR'].cut(through);scene['PC_BASE']=scene['PC_BASE'].cut(through)
 cs=Part.makeCone(p['through_diameter_mm']/2,p['countersink_diameter_mm']/2,p['countersink_depth_mm'],V(x,y,54-p['countersink_depth_mm']));scene['PC_BASE']=scene['PC_BASE'].cut(cs)
 operations.append({'part':'Floor+PCBase','operation':'through_drill_and_PCBase_top_countersink','center_xy_mm':[x,y],'diameter_mm':5.5,'countersink_mm':[10.5,2.5],'status':'candidate_M5_remove_chassis_for_access'})
scene.update(new)
installed=conflicts(new,scene);check('new audio shapes clear installed scene',not installed)
# Service envelopes may contain their own hardware; exclude these and carrier touching its top.
service={}
for n,shape in envelopes.items():
 own='SSF_Subwoofer_DCS165_Reference' if n=='SSF_SubwooferService' else 'SSF_BST1_Reference' if n=='SSF_BSTService' else n.removesuffix('Service')
 service[n]=conflicts({n:shape},scene,(own,))
check('audio service reservations clear other parts',not any(service.values()))
check('four exciters and separate bass shaker and subwoofer',len([n for n in new if n.startswith('SSF_Exciter')])==4 and 'SSF_BST1_Reference' in new and 'SSF_Subwoofer_DCS165_Reference' in new)
check('subwoofer cutout grew beyond obsolete139.7',abs(s['design_cutout_mm']-143.5)<1e-6 and not scene['FLOOR'].isInside(V(sx+71,sy,27),1e-6,True))
for i,(x,y) in enumerate(sholes,1):check(f'subwoofer hole{i} through floor',not scene['FLOOR'].isInside(V(x,y,27),1e-6,True))
for i,(x,y) in enumerate(b['floor_anchor_holes_xy_mm'],1):check(f'shaker carrier anchor{i} through both boards',all(not shape.isInside(V(x,y,z),1e-6,True) for shape,z in [(scene['FLOOR'],27),(plate,42)]))
for i,(x,y) in enumerate(p['anchor_holes_xy_mm'],1):check(f'PCBase anchor{i} through both boards',all(not shape.isInside(V(x,y,z),1e-6,True) for shape,z in [(scene['FLOOR'],27),(scene['PC_BASE'],45)]))
check('frozen shelf positions and geometry retained',all(scene[n].cut(old[n]).Volume+old[n].cut(scene[n]).Volume<1e-6 for n in ['SHELF_1','SHELF_2','SHELF_3']))
check('rear sides and door unchanged',all(scene[n].cut(old[n]).Volume+old[n].cut(scene[n]).Volume<1e-6 for n in ['REAR','REAR_DOOR','SIDE_L','SIDE_R','FAN_230','FAN_370']))
check('PC envelope unchanged and base outline stays low',scene['PC_ENVELOPE'].cut(old['PC_ENVELOPE']).Volume<1e-6 and scene['PC_BASE'].BoundBox.ZMin==36 and scene['PC_BASE'].BoundBox.ZMax==54)
# Shelf service: at least vertical lift150 before planned staged routes, payload must be disconnected.
# Check only new fixed audio additions so existing staged service evidence remains distinct.
for i in (1,2,3):
 bb=scene[f'SHELF_{i}'].BoundBox;lift=box([bb.XMin,bb.YMin,bb.ZMin,bb.XLength,bb.YLength,bb.ZLength+150]);ignore=('SSF_AmplifierReserve','SSF_USBReserve') if i==2 else ('SSF_PSUReserve',) if i==3 else ()
 check(f'S{i} lift adds no conflict with fixed audio',not conflicts({'shelf_lift':lift},new,ignore))
# Shaker carrier service requires removingS1. Conservative bounding sweep up150.
bs=box([210,170,36,180,180,227]);remove=('SSF_BST_Carrier','SSF_BST1_Reference','SHELF_1','SHELF_1_CandidatePayload','AUDIO_STARTECH')
shaker_lift=conflicts({'shaker_lift':bs},scene,remove);check('shaker lifts with S1 removed',not shaker_lift)
check('reject shaker lift while S1 is installed',bool(conflicts({'shaker_lift':bs},{'SHELF_1':scene['SHELF_1']})))
# Subwoofer lift150 ends below playfield; screen actual unit reservation.
sub_lift=cyl(sx,sy,36,83.5,240);sub_service=conflicts({'subwoofer_lift':sub_lift},scene,('SSF_Subwoofer_DCS165_Reference',));check('subwoofer vertical service clear',not sub_service)
# Side exciters withdraw30mm inward without contacting the stationary cabinet.
for n in [x for x in new if x.startswith('SSF_Exciter')]:
 bb=new[n].BoundBox;x=bb.XMin if n.endswith('L') else bb.XMin-30
 check(n+' inward service30mm',not conflicts({'exciter_withdraw':box([x,bb.YMin,bb.ZMin,bb.XLength+30,bb.YLength,bb.ZLength])},scene,(n,)))
# Symmetry of exciters and new floor cuts.
mir=A.Matrix();mir.A11=-1;mir.A14=600
for i in (1,2):
 a=new[f'SSF_Exciter{i}L'].transformGeometry(mir);bshape=new[f'SSF_Exciter{i}R'];check(f'exciter pair{i} symmetric',a.cut(bshape).Volume+bshape.cut(a).Volume<1e-6)
check('all solids valid',all(s.isValid() and len(s.Solids)==1 for s in scene.values()))
# Save full consolidated source and reusable tessellation for original project drawings.
out=A.newDocument('V32ConsolidatedAudio');mesh=[]
for n,s in scene.items():
 o=out.addObject('PartDesign::Feature',n);o.Shape=s;o.addProperty('App::PropertyString','PartCode');o.PartCode=getattr(d.getObject(n),'PartCode','') if d.getObject(n) else n;o.addProperty('App::PropertyString','Status');o.Status='REFERENCE_OR_CANDIDATE_NOT_CNC_RELEASE'
 verts,faces=s.tessellate(1.0);mesh.append({'name':n,'vertices':[[v.x,v.y,v.z] for v in verts],'faces':[list(f) for f in faces]})
out.recompute();fp=O/'cabinet-v32-consolidated.FCStd';out.saveAs(str(fp));Part.export([o for o in out.Objects if hasattr(o,'Shape')],str(O/'cabinet-v32-consolidated.step'));A.closeDocument(out.Name);out=A.openDocument(str(fp));check('saved scene reopens with exact valid shapes',all(o.Shape.isValid() and len(o.Shape.Solids)==1 and o.Shape.cut(scene[o.Name]).Volume+scene[o.Name].cut(o.Shape).Volume<1e-5 for o in out.Objects if hasattr(o,'Shape')));A.closeDocument(out.Name)
# Exact planar bottom-face export; all floor operations are through-cuts at this stage.
face=next(f for f in scene['FLOOR'].Faces if isinstance(f.Surface,Part.Plane) and abs(f.CenterOfMass.z-18)<1e-6 and f.normalAt(0,0).z<-.99)
lines=['0','SECTION','2','HEADER','9','$INSUNITS','70','4','0','ENDSEC','0','SECTION','2','ENTITIES'];counts={}
def ent(kind,layer,fields):
 lines.extend(['0',kind,'8',layer]);counts[kind]=counts.get(kind,0)+1
 for code,value in fields:lines.extend([str(code),str(value)])
for edge in face.Edges:
 curve=edge.Curve
 if isinstance(curve,Part.Line) or isinstance(curve,Part.LineSegment):
  a=edge.Vertexes[0].Point;bpt=edge.Vertexes[-1].Point;ent('LINE','FLOOR_THROUGH',[(10,a.x),(20,a.y),(11,bpt.x),(21,bpt.y)])
 elif isinstance(curve,Part.Circle):
  center=curve.Center;radius=curve.Radius;layer='DRILL_THROUGH' if edge.isClosed() and radius<4 else 'FLOOR_THROUGH'
  if edge.isClosed():ent('CIRCLE',layer,[(10,center.x),(20,center.y),(40,radius)])
  else:
   pa,pb=edge.ParameterRange;a=edge.valueAt(pa);bpt=edge.valueAt(pb);mid=edge.valueAt((pa+pb)/2)
   ang=lambda q:math.degrees(math.atan2(q.y-center.y,q.x-center.x))%360
   aa,bb,mm=ang(a),ang(bpt),ang(mid)
   if (mm-aa)%360>(bb-aa)%360:aa,bb=bb,aa
   ent('ARC',layer,[(10,center.x),(20,center.y),(40,radius),(50,aa),(51,bb)])
 else:raise ValueError('Unsupported floor profile curve: '+str(type(curve)))
lines+=['0','ENDSEC','0','EOF'];(O/'floor-draft-mm.dxf').write_text('\n'.join(lines)+'\n')
check('floor DXF exact planar edge inventory',sum(counts.values())==len(face.Edges) and counts.get('CIRCLE')==25 and counts.get('ARC')==8)
(O/'mesh.json').write_text(json.dumps(mesh));(O/'floor-operations.json').write_text(json.dumps(operations,indent=2)+'\n')
check('all sources preserved',all(sha(R/p)==h for p,h in inputs.items()))
for n in ('LICENSE','NOTICE.md'):shutil.copyfile(R/n,O/n)
report={'manufacturing_ready':False,'source_hashes':inputs,'config':c,'checks':checks,'new_parts':list(new),'removed_reservations':['AUDIO_STARTECH','SHELF_2_CandidatePayload','SHELF_3_CandidatePayload'],'installed_conflicts':installed,'service_conflicts':service,'shaker_lift_conflicts':shaker_lift,'subwoofer_lift_conflicts':sub_service,'solids':len(scene),'saved_cad_sha256':sha(fp),'floor_operations':operations,'floor_dxf_entities':counts};(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');assert all(v['pass'] for v in checks),[v for v in checks if not v['pass']];print('CONSOLIDATED_AUDIO_PASS',len(checks),'checks;',len(scene),'solids');A.closeDocument(d.Name)
