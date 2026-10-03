"""Read-only exact B-rep distances for new side landings. CERN-OHL-S-2.0."""
from pathlib import Path
import hashlib,json,math,sys
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,V
C=json.loads((R/'config/front_landings_v3363.json').read_text());O=R/C['output'];p=load(O/'play.FCStd');g=json.loads((O/'geometry-validation.json').read_text());rows=[]
opening_study=load(R/'exports/generated/monitor-support-v336/study.FCStd')
openings={n:s for n,s in opening_study.items() if n.startswith(('PF_MainServiceWindow','PF_StrainSlot'))}
def closest(shape,group):
 out=[{'name':n,'distance_mm':shape.distToShape(s)[0]} for n,s in group.items()]
 return min(out,key=lambda q:q['distance_mm']) if out else None
for side in ['L','R']:
 body=Part.makeCompound([p[f'FrontLanding{side}_Layer{j}'] for j in [1,2,3]])
 pad=p[f'FrontLanding{side}_ContactPad'];panel=p['SIDE_'+side]
 names={
  'button_occupied':{n:s for n,s in p.items() if n.startswith('Leaf')},
  'button_service':{n:s for n,s in p.items() if n.startswith('Button')},
  'shelf1':{n:s for n,s in p.items() if n.startswith(('SHELF_1','SHELF_SUPPORT_1'))},
  'SSF':{n:s for n,s in p.items() if n.startswith('SSF_')},
  'front_joinery':{'FRONT':p['FRONT']},
  'front_leg':{n:s for n,s in p.items() if n.startswith('CandidateLegBlockF')},
  'plunger_service':{'PLUNGER_RESERVED':p['PLUNGER_RESERVED']}}
 anchors=[]
 for j in range(1,5):
  sh=p[f'FrontLanding{side}_SideScrew{j}'];y,z=sh.BoundBox.Center.y,sh.BoundBox.Center.z
  line=Part.makeLine(V(-1,y,z),V(19,y,z)) if side=='L' else Part.makeLine(V(581,y,z),V(601,y,z))
  face=max([f for f in panel.Faces if type(f.Surface).__name__=='Plane' and abs(abs(f.normalAt(0,0).x)-1)<1e-6 and abs(f.CenterOfMass.x-(18 if side=='L' else 582))<1e-5],key=lambda f:f.Area)
  center=Part.Vertex(V(18 if side=='L' else 582,y,z))
  anchors.append({'index':j,'side_inside_center_xyz_mm':[18 if side=='L' else 582,y,z],
    'actual_side_stock_along_axis_mm':panel.common(line).Length,
    'side_outer_boundary_center_distance_mm':center.distToShape(face.OuterWire)[0],
    'nearest_button_occupied':closest(sh,names['button_occupied']),
    'remaining_exterior_skin_mm':6,'reference_pilot_status':'UNCUT_IN_CURRENT; hardware/depth stop hold'})
 rows.append({'side':side,'body_nearest':{k:closest(body,v) for k,v in names.items()},
  'pad_to_VESA_mm':pad.distToShape(p['PF_VESAEnvelope'])[0],
  'pad_to_documented_opening_edges':{n:pad.distToShape(s)[0] for n,s in openings.items()},
  'pad_to_front_relief_edges_mm':min(pad.distToShape(e)[0] for e in p['PF_BasePlywood'].Edges if e.BoundBox.YMax<180 and e.BoundBox.YMin>140),
  'pad_foremost_world_y_mm':pad.BoundBox.YMin,'pad_rearmost_world_y_mm':pad.BoundBox.YMax,
  'base_foremost_world_y_mm':p['PF_BasePlywood'].BoundBox.YMin,
  'front_overhang_to_pad_center_mm':C['search']['selected_pad_y_mm']-p['PF_BasePlywood'].BoundBox.YMin,
  'front_overhang_to_pad_front_mm':pad.BoundBox.YMin-p['PF_BasePlywood'].BoundBox.YMin,
  'attachment_axes':anchors})
result={'rows':rows,'source_sha256':hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest(),
 'side_hardware_holes_not_released':True,'base_blind_receiver_holes_not_released':True,
 'intentional_interfaces':'Only new support pads carry front gravity load. Side screws engage12 mm of18 mm nominal structural sides. Embedded receiver envelopes are reference-only and do not modify current wood machining.',
 'manufacturing_release':False}
(O/'metrology.json').write_text(json.dumps(result,indent=2)+'\n');print('V3363_METROLOGY_DONE',len(rows),flush=True)
