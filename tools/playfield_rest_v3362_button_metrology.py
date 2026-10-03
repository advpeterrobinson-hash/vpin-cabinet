"""Read-only final button/package/wood distances. CERN-OHL-S-2.0.
Reference leaf hardware geometry only; no bore or purchased part release.
"""
from pathlib import Path
import json,hashlib,sys,math
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from pivot_cradle_integration_v32 import load,V
C=json.loads((R/'config/playfield_rest_v3362.json').read_text());O=R/C['output'];path=O/'play.FCStd';ss=load(path)

def group(test):return {n:s for n,s in ss.items() if test(n)}
groups={
 'playfield_base':group(lambda n:n=='PF_BasePlywood'),
 'S1_supports':group(lambda n:n.startswith('SHELF_SUPPORT_1')),
 'S1_shelf':group(lambda n:n=='SHELF_1'),
 'T1_guides':group(lambda n:n.startswith('CROSS_GUIDE_1')),
 'T1_crossmember':group(lambda n:n=='CROSS_1'),
 'SSF_front_exciters':group(lambda n:n.startswith('SSF_Exciter1')),
 'leg_blocks_and_hardware':group(lambda n:'Leg' in n),
 'plunger':group(lambda n:n=='PLUNGER_RESERVED' or n.startswith('Plunger')),
 'front_panel':group(lambda n:n=='FRONT'),
 'floor':group(lambda n:n=='FLOOR'),
 'glass_channels':group(lambda n:n.startswith('CandidateGlassChannel')),
}
report={'pass':False,'status':'PROVISIONAL_REFERENCE_PACKAGING_NOT_PURCHASED_HARDWARE','source':str(path.relative_to(R)),
 'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'groups':{k:list(v) for k,v in groups.items()},'rows':[],'wood':[],'checks':[],
 'manufacturing_release':False,'final_bore_mm':None,'final_recess_mm':None,
 'human_access_source':'button-metrology.json#human_access; top entry after main glass+matrix removal and playfield service50deg. Not a universal ergonomic qualification.'}

def closest(s,obs):
 values=[]
 for n,t in obs.items():
  d,points,info=s.distToShape(t);vol=s.common(t).Volume if s.BoundBox.intersect(t.BoundBox) else 0
  values.append({'part':n,'distance_mm':d,'penetration_mm3':vol,'witness_xyz_mm':[[list(a),list(b)] for a,b in points[:1]]})
 return min(values,key=lambda v:v['distance_mm']) if values else {'status':'NO_MODELED_ITEM_IN_THIS_GROUP'}

for kind,y in zip(['primary','secondary'],C['side_buttons']['candidate_y_mm']):
 for side in ['L','R']:
  for stem,role in [('LeafButton_','occupied_button'),('LeafNut_','occupied_nut'),('LeafBracket_','occupied_leaf_bracket'),('LeafContacts_','occupied_leaf_contacts'),('ButtonBodyServiceReserve_','body_service'),('ButtonLeafServiceReserve_','leaf_service'),('ButtonWireServiceReserve_','wire_service'),('ButtonToolServiceReserve_','tool_service')]:
   n=stem+kind+'_'+side;s=ss[n];z=ss['LeafButton_'+kind+'_'+side].BoundBox.Center.z
   report['rows'].append({'id':n,'role':role,'side':side,'center_yz_mm':[y,z], 'nearest':{k:closest(s,v) for k,v in groups.items()}})
  panel=ss['SIDE_'+side];x=0 if side=='L' else 600
  faces=[f for f in panel.Faces if type(f.Surface).__name__=='Plane' and abs(abs(f.normalAt(0,0).x)-1)<1e-7 and abs(f.CenterOfMass.x-x)<1e-7]
  face=max(faces,key=lambda f:f.Area);center=V(x,y,z);radius=C['side_buttons']['reference_nut_pocket_for_visualization_mm'][0]/2
  circle=Part.makeCircle(radius,center,V(1,0,0));outergap=circle.distToShape(face.OuterWire)[0]
  top=[]
  for e in face.OuterWire.Edges:
   if len(e.Vertexes)!=2:continue
   a,b=[v.Point for v in e.Vertexes]
   if abs(a.y-b.y)<1e-8 or abs(e.Length-(a-b).Length)>1e-7:continue
   if min(a.y,b.y)-1e-6<=y<=max(a.y,b.y)+1e-6:top.append(a.z+(y-a.y)*(b.z-a.z)/(b.y-a.y))
  topz=max(top);probe_offset=(radius+C['side_buttons']['reference_bore_for_visualization_mm']/2)/2
  line=Part.makeLine(V(-1 if side=='L' else 581,y+probe_offset,z),V(19 if side=='L' else 601,y+probe_offset,z))
  residual=panel.common(line).Length
  report['wood'].append({'side':side,'button':kind,'center_yz_mm':[y,z],
   'reference_bore_diameter_mm':C['side_buttons']['reference_bore_for_visualization_mm'],'reference_pocket_diameter_mm':2*radius,
   'nominal_stock_mm':18,'reference_nut_recess_depth_mm':3,'measured_nominal_annulus_residual_mm':residual,
   'side_outer_boundary_minimum_gap_from_reference_pocket_mm':outergap,
   'actual_side_top_z_at_center_y_mm':topz,'center_below_local_top_vertical_mm':topz-z,'reference_pocket_top_vertical_web_mm':topz-z-radius,
   'longitudinal_center_pitch_mm':38,'reference_pocket_to_pocket_web_mm':math.hypot(38,ss['LeafButton_secondary_'+side].BoundBox.Center.z-ss['LeafButton_primary_'+side].BoundBox.Center.z)-2*radius,
   'geometry_status':'Nominal candidate packaging. New holes/recesses remain PURCHASE_BEFORE_CNC; actual lot stock and selected button stack unknown.'})
report['checks']=[{'name':'all named obstacle groups populated','pass':all(bool(v) for v in groups.values())},
 {'name':'all button service and occupied references clear named structures','pass':all(q.get('penetration_mm3',0)<1e-4 and q.get('distance_mm',0)>1e-5 for r in report['rows'] for q in r['nearest'].values())},
 {'name':'both nominal reference annuli retain15mm wood','pass':all(abs(q['measured_nominal_annulus_residual_mm']-15)<1e-5 for q in report['wood'])},
 {'name':'native input unchanged','pass':hashlib.sha256(path.read_bytes()).hexdigest()==report['source_sha256']}]
# Conservative hand/tool approach from above the open front area. Occupied
# reference buttons themselves are intended contact/operation targets, not wood.
from backbox_lock_integration_v32 import actual,pf_names,transform,PF
neighbor_hardware={n:s for n,s in actual(ss).items() if n.startswith('Leaf')}
service=actual(ss);service.update(transform({n:s for n,s in service.items() if n in pf_names(ss)},angle=-50,axis=PF))
service={n:s for n,s in service.items() if n!='CandidateGlass' and not n.startswith(('Matrix','MX_Retainer','Leaf','Button')) and n not in ['MX_MovingConnectorReserve','MX_CableLoopReserve']}
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def mirror(s):
 m=A.Matrix();m.A11=-1;m.A14=600;q=s.copy();q.transformShape(m,True);return q
access=[];access_shapes={}
for kind,y in zip(['primary','secondary'],C['side_buttons']['candidate_y_mm']):
 z=ss['LeafButton_'+kind+'_L'].BoundBox.Center.z
 for side in ['L','R']:
  env={'palm':box(65,y-27,z-12,65,54,42),'top_entry':box(65,y-27,z+15,65,54,420),'finger':box(38,y-10,z-12,27,20,30),'driver':Part.makeCylinder(9,90,V(43,y,z),V(1,0,0))}
  for role,s in env.items():
   if side=='R':s=mirror(s)
   name='Access_'+kind+'_'+side+'_'+role;access_shapes[name]=s
   hh=[]
   obs={**service,**{n:t for n,t in neighbor_hardware.items() if not n.endswith('_'+kind+'_'+side)}}
   for n,t in obs.items():
    if s.BoundBox.intersect(t.BoundBox):
     v=s.common(t).Volume
     if v>1e-4:hh.append({'part':n,'penetration_mm3':v})
   access.append({'id':name,'role':role,'bounds_mm':[s.BoundBox.XMin,s.BoundBox.YMin,s.BoundBox.ZMin,s.BoundBox.XMax,s.BoundBox.YMax,s.BoundBox.ZMax],'hits':hh})
report['human_access']={'state':'PLAYFIELD_SERVICE_50','prerequisites':['MAIN_PLAYFIELD_GLASS_REMOVED','MATRIX_REMOVED'],'rows':access,'scope':'Conservative reference hand/driver approach, not universal ergonomic certification or purchased hardware fit.'}
report['checks'].append({'name':'front-button hand/tool approach clear at service50','pass':not any(r['hits'] for r in access)})
report['checks'].append({'name':'owner local-top-minus65 datum exact','pass':all(abs(r['center_below_local_top_vertical_mm']-65)<1e-6 for r in report['wood'])})
import gzip
meshes={}
for n,s in access_shapes.items():
 s.exportBrep(str(O/'brep'/(n+'.brep')));vv,ff=s.tessellate(.4);meshes[n]={'vertices':[list(v) for v in vv],'faces':ff}
(O/'button-access-mesh.json.gz').write_bytes(gzip.compress(json.dumps(meshes).encode(),mtime=0))
report['pass']=all(q['pass'] for q in report['checks']);(O/'button-metrology.json').write_text(json.dumps(report,indent=2)+'\n');print('V3362_BUTTON_METROLOGY',report['pass'],len(report['rows']),len(report['checks']));assert report['pass'],report['checks']
