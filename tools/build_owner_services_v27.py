"""Owner-selected manual props, modular carriers, airflow, controls and rear access.
All purchased hardware patterns remain blocked. Shapes with ENVELOPE or REVIEW
roles are service packaging, not production metal or drill specifications.
"""
import json,math,csv
from pathlib import Path
import FreeCAD as A
import Part
from owner_features_v27 import config,features
ROOT=Path(__file__).resolve().parents[1]

def box(spec):return Part.makeBox(*spec[3:],A.Vector(*spec[:3]))
def rod(a,b,r):
 a,b=A.Vector(*a),A.Vector(*b);v=b-a;return Part.makeCylinder(r,v.Length,a,v)
def rounded_xy(w,h,t,r):
 s=Part.makeBox(w-2*r,h,t,A.Vector(r,0,0)).fuse(Part.makeBox(w,h-2*r,t,A.Vector(0,r,0))) if h>2*r else Part.makeBox(w-2*r,h,t,A.Vector(r,0,0))
 for x in (r,w-r):
  for y in (r,h-r):s=s.fuse(Part.makeCylinder(r,t,A.Vector(x,y,0)))
 return s.removeSplitter()
def cut_shape(f):
 p=f['origin'];s=f['size']
 if f['diameter']:
  axis=A.Vector(0,0,1) if f['axis']=='Z' else A.Vector(0,1,0)
  return Part.makeCylinder(f['diameter']/2,sum(s),A.Vector(*p),axis)
 if f['axis']=='Z':
  sh=rounded_xy(s[0],s[1],s[2],f['radius']);sh.translate(A.Vector(*p));return sh
 sh=rounded_xy(s[0],s[2],s[1],f['radius']);sh.rotate(A.Vector(),A.Vector(1,0,0),90);sh.translate(A.Vector(p[0],p[1]+s[1],p[2]));return sh

def main(doc):
 c=config();mech=json.loads((ROOT/'config/playfield_mechanics_v18.json').read_text())
 old=doc.getObject('OwnerServicesV27')
 if old:
  for o in list(old.Group):doc.removeObject(o.Name)
  doc.removeObject(old.Name)
 group=doc.addObject('App::Part','OwnerServicesV27');group.Label='OWNER REVIEW — MANUAL PROPS / CARRIERS / CONTROLS / AIRFLOW'
 carriers=[]
 def add(n,shape,role,label=None,pid=None):
  o=doc.addObject('PartDesign::Feature',n);o.Shape=shape;o.Label=label or n;group.addObject(o)
  o.addProperty('App::PropertyString','EngineeringRole');o.EngineeringRole=role
  if pid:
   o.addProperty('App::PropertyString','PartID');o.PartID=pid
   carriers.append(dict(part_id=pid,object_name=n,construction_class='REMOVABLE_CARRIER',material='replaceable plate; plywood/aluminum as documented',attachment='standardized bolts; no glue',electronics_holes='ADAPTER_ONLY',manufacturing_ready='false'))
  return o
 # Generic wood cuts have no purchased-hardware pattern dependencies.
 for f in features(c):
  o=doc.getObject(f['part'])
  if not o:raise RuntimeError('Missing receiver '+f['part'])
  cut=cut_shape(f);o.Shape=o.Shape.cut(cut).removeSplitter()
  add('Defined'+f['key']+'CutV27',cut,'DEFINED_CNC_CUT',f['type']+' / '+f['key'])
 # Two small carrier plates use project-fabricated end angles on low ties 1 and 2.
 e=c['electronics']
 for side,x in zip(('Left','Right'),e['tray_x_mm']):
  y,z=e['tray_y_mm'],e['tray_z_mm'];w,l,t=e['tray_size_mm']
  tray=box([x,y,z,w,l,t])
  # M4 tray holes are project-designed, not electronics patterns.
  for xx in (x+15,x+w-15):
   for yy in (295,632):tray=tray.cut(Part.makeCylinder(2.25,t+2,A.Vector(xx,yy,z-1)))
  add('ElectronicsCarrier'+side+'V27',tray,'REMOVABLE_CARRIER',side+' removable low-voltage electronics carrier / 125 × 355', 'ELEC-CARRIER-'+side.upper()+'-R1')
  for j,yy in enumerate((278,647),1):
   vertical=box([x,yy,75,w,3,50]);lip=box([x,278 if j==1 else 625,122,w,25,3])
   add('CarrierAngle'+side+str(j)+'V27',vertical.fuse(lip).removeSplitter(),'LOCAL_METAL','Project-fabricated M6 carrier angle; no supplier pattern')
  add('Electronics'+side+'PayloadEnvelopeV27',box([x+5,y+15,z+t,w-10,l-30,e['payload_envelope_height_mm']]),'ELECTRONICS_ZONE',('DC POWER / CONTROL' if side=='Left' else 'AMPLIFIERS / CONTROLLERS')+' — 3 kg carrier envelope')
 add('CentralServiceKeepoutV27',box(e['central_access_box_mm']),'ACCESS_ZONE','OPEN CENTRAL SERVICE / future toys; no bridging shelf')
 # Externally serviceable underside filter cassette; keep screw heads captive on inside.
 v=c['bottom_intake'];x,y,w,l=v['filter_outer_xy_mm'];z=18-v['filter_thickness_mm']
 frame=box([x,y,z,w,l,v['filter_thickness_mm']]).cut(box([x+12,y+12,z-1,w-24,l-24,v['filter_thickness_mm']+2]))
 for xx,yy in v['filter_mount_xy_mm']:frame=frame.cut(Part.makeCylinder(2.25,v['filter_thickness_mm']+2,A.Vector(xx,yy,z-1)))
 add('BottomFilterCarrierV27',frame,'REMOVABLE_CARRIER','OUTSIDE BOTTOM — removable dust-filter cassette','AIR-FILTER-CARRIER-R1')
 add('BottomFilterMediaEnvelopeV27',box([x+8,y+8,z+2,w-16,l-16,2]),'ELECTRONICS_ZONE','Replaceable mesh/filter; airflow unproven')
 # Strength-preserving exciter zones: intact wall, no speaker opening.
 for side in ('Left','Right'):
  for pos in ('Front','Rear'):
   o=doc.getObject('SSF'+pos+side+'KeepoutV20');b=o.Shape.BoundBox
   o.Shape=box([18 if side=='Left' else 582-c['ssf']['depth_mm'],b.YMin,b.ZMin,c['ssf']['depth_mm'],b.YLength,b.ZLength])
   o.Label=pos+' '+side+' SSF EXCITER — SOLID PLYWOOD / no through-hole'
   o.addProperty('App::PropertyString','EngineeringRole');o.EngineeringRole='SSF_ZONE'
 # Simple captive prop rods; retain independent fixed backed anchors.
 mg=doc.getObject('PlayfieldMechanicsV18');hy,hz=mg.HingeY.Value,mg.HingeZ.Value
 hinge=mech['hinge_axis'];st=mech['safety_stays'];alpha=mg.CabinetSlope.Value
 a=math.radians(alpha);ly,lz=hinge['local_y_from_display_front_mm'],hinge['local_z_from_display_base_mm']
 base=hz-ly*math.sin(a)-lz*math.cos(a);front=mech['display_envelope']['front_setback_mm']
 def local_point(x,y,z):return A.Vector(x,y*math.cos(a)-z*math.sin(a)+front,y*math.sin(a)+z*math.cos(a)+base)
 def open_shape(s):
  s=s.copy();s.rotate(A.Vector(0,hy,hz),A.Vector(1,0,0),-hinge['relative_service_open_angle_deg']);return s
 def open_point(p):return A.Placement(A.Vector(0,hy,hz),A.Rotation(A.Vector(1,0,0),-hinge['relative_service_open_angle_deg'])).multVec(p-A.Vector(0,hy,hz))
 lengths=[]
 for side,x in zip(('Left','Right'),c['props']['rod_plane_x_mm']):
  fixed=A.Vector(x,hy-st['fixed_mount_forward_from_hinge_mm'],hz-st['fixed_mount_below_hinge_mm'])
  closed=local_point(x,ly-st['moving_mount_forward_from_hinge_mm'],st['moving_mount_local_z_mm']);opened=open_point(closed)
  length=(opened-fixed).Length;lengths.append(length)
  rr=c['props']['rod_diameter_mm']/2
  o=add('SafetyStayOpen'+side+'V18',rod(tuple(fixed),tuple(opened),rr),'REVIEW_STATE','CAPTIVE PROP '+side.upper()+' — upper pin locked / service state')
  for prop,value in [('SupportMode','PINNED_POSITIVE'),('UpperLock','CAPTIVE_TRANSVERSE_PIN_WITH_KEEPER')]:o.addProperty('App::PropertyString',prop);setattr(o,prop,value)
  o.addProperty('App::PropertyBool','FrictionSupport');o.FrictionSupport=False
  stowed=A.Vector(x,fixed.y+length,fixed.z)
  add('PropRod'+side+'StowedV27',rod(tuple(fixed),tuple(stowed),rr),'LOCAL_METAL','Captive prop '+side+' / stowed rearward with positive clip')
  # Outboard corridor: 8 mm rod; 3 mm clevis ears; measured pattern remains blocked.
  x0=20 if side=='Left' else 560
  plate_x=36 if side=='Left' else 561
  fixed_clevis=box([x0,fixed.y-12,fixed.z-12,20,24,4])
  for xx in (x-8,x+5):fixed_clevis=fixed_clevis.fuse(box([xx,fixed.y-12,fixed.z-12,3,24,25]))
  fixed_clevis=fixed_clevis.fuse(box([plate_x,fixed.y-12,fixed.z-100,3,24,104]))
  add('PropFixedClevis'+side+'V27',fixed_clevis,'LOCAL_METAL','Front steel riser / combined landing-prop backing; HF-010 blocked')
  add('PropLowerPivotPin'+side+'V27',Part.makeCylinder(3,24,A.Vector(x-12,fixed.y,fixed.z),A.Vector(1,0,0)),'LOCAL_METAL','Captive lower pivot / pin envelope only')
  receiver=box([x0,closed.y-18,closed.z-12,20,36,4])
  for xx in (x-8,x+5):receiver=receiver.fuse(box([xx,closed.y-18,closed.z-12,3,36,25]))
  receiver=receiver.fuse(box([36 if side=='Left' else 560,closed.y-18,closed.z-12,4,36,35]))
  add('PropReceiver'+side+'ClosedV27',receiver,'LOCAL_METAL','Prop receiver on cradle outer rail; measured wood pattern blocked')
  add('PropReceiver'+side+'OpenV27',open_shape(receiver),'REVIEW_STATE','Upper prop receiver / captive pin engaged')
  pin=Part.makeCylinder(3,24,A.Vector(x-12,opened.y,opened.z),A.Vector(1,0,0))
  add('PropUpperLockPin'+side+'OpenV27',pin,'REVIEW_STATE','POSITIVE transverse receiver pin / retained keeper')
  add('PropPinKeeper'+side+'OpenV27',Part.makeCylinder(1,12,A.Vector(x+10,opened.y,opened.z-6),A.Vector(0,0,1)),'REVIEW_STATE','Captive positive keeper / conceptual envelope')
  clip=box([x-8,stowed.y-12,stowed.z-10,16,24,3])
  for xx in (x-8,x+5):clip=clip.fuse(box([xx,stowed.y-12,stowed.z-10,3,24,20]))
  add('PropStowKeeper'+side+'V27',Part.makeCylinder(1.5,20,A.Vector(x-10,stowed.y,stowed.z+6),A.Vector(1,0,0)),'LOCAL_METAL','Captive stow keeper across open U-clip; not friction')
  bx=18 if side=='Left' else 564
  add('PropStowBracket'+side+'V27',box([bx,stowed.y-12,stowed.z-14,18,24,4]).fuse(box([18 if side=='Left' else 579,stowed.y-12,stowed.z-30,3,24,40])),'LOCAL_METAL','Small stow clip wall bracket / HF-010 blocked')
  add('PropStowClip'+side+'V27',clip,'LOCAL_METAL','Positive stow clip; mounting pattern HF-010 blocked')
 # Human interfaces: visible bezels plus realistic nut/switch and cable reserves.
 k=c['controls'];radius=k['button_nut_radius_mm']
 for side,x,sign in [('Left',0,1),('Right',600,-1)]:
  for i,(y,z) in enumerate(k['side_positions_yz_mm']):
   tag=side+('Flipper' if i==0 else 'Action')
   add('Control'+tag+'BezelV27',Part.makeCylinder(16,7,A.Vector(x-sign*7,y,z),A.Vector(sign,0,0)),'CONTROL_ZONE',tag+' / ergonomic center; action optional')
   add('Control'+tag+'InternalV27',Part.makeCylinder(radius,k['side_internal_depth_mm'],A.Vector(18 if sign==1 else 582,y,z),A.Vector(sign,0,0)),'CONTROL_ZONE',tag+' nut/switch / HF-020 blocked')
   add('Control'+tag+'CableV27',Part.makeCylinder(12,k['button_cable_depth_mm'],A.Vector(78 if sign==1 else 522,y,z),A.Vector(sign,0,0)),'CONTROL_ZONE',tag+' cable reserve')
 for b in k['front_buttons']:
  tag=b['name'];x,z=b['x'],b['z']
  add('Control'+tag+'BezelV27',Part.makeCylinder(16,7,A.Vector(x,-7,z),A.Vector(0,1,0)),'CONTROL_ZONE',tag+' front control')
  add('Control'+tag+'InternalV27',Part.makeCylinder(radius,k['front_internal_depth_mm'],A.Vector(x,18,z),A.Vector(0,1,0)),'CONTROL_ZONE',tag+' nut/switch / HF-020 blocked')
  add('Control'+tag+'CableV27',Part.makeCylinder(12,20,A.Vector(x,83,z),A.Vector(0,1,0)),'CONTROL_ZONE',tag+' cable reserve')
 add('CoinDoorEnvelopeV27',box(k['coin_door_box_mm']),'CONTROL_ZONE','Coin door packaging; HF-019 cutout blocked')
 add('HiddenServiceControlsEnvelopeV27',box([210,50,140,90,15,35]),'CONTROL_ZONE','Hidden setup / mechanical-feedback kill controls inside coin door')
 add('PlungerBodyEnvelopeV27',box(k['plunger_body_box_mm']),'CONTROL_ZONE','RIGHT FRONT PLUNGER / HF-030 — no final bore')
 add('PlungerCableEnvelopeV27',box(k['plunger_cable_box_mm']),'CONTROL_ZONE','Plunger sensor/cable access')
 x,z=k['plunger_center_xz_mm']
 add('PlungerHandleEnvelopeV27',Part.makeCylinder(10,k['plunger_handle_projection_mm'],A.Vector(x,-k['plunger_handle_projection_mm'],z),A.Vector(0,1,0)),'CONTROL_ZONE','Plunger pull handle reserve')
 # Backbox service closure is retained and spaced off a positive stop/gasket.
 b=c['backbox'];door=doc.getObject('BackboxServiceDoorV14');db=door.Shape.BoundBox
 door.Shape=box([40,1308.1+b['door_spacer_mm'],650,520,15,460]);db=door.Shape.BoundBox
 stop=box([30,1308.1,640,540,2,480]).cut(box([50,1307.1,660,500,4,440]))
 gasket=box([35,1310.1,645,530,2,470]).cut(box([50,1309.1,660,500,4,440]))
 add('BackboxDoorStopV27',stop,'LOCAL_METAL','Fixed steel stop flange; door is not primary shear panel')
 add('BackboxDoorGasketV27',gasket,'LOCAL_METAL','Compressed gasket envelope; actual sample HF-029')
 opened=door.Shape.copy();axis=A.Vector(db.XMax,db.YMax,db.ZMin);opened.rotate(axis,A.Vector(0,0,1),-b['door_outward_deg'])
 add('BackboxDoorOpenV27',opened,'REVIEW_STATE','BB-DOOR-001-R1 OPEN OUTWARD 105°')
 add('BackboxDoorHingeEnvelopeV27',Part.makeCylinder(4,460,axis,A.Vector(0,0,1)),'LOCAL_METAL','Continuous robust hinge reserve / HF-029 blocked')
 latch=box([55,db.YMax,870,22,18,32]);add('BackboxDoorLatchClosedV27',latch,'LOCAL_METAL','Keyed/tool-controlled latch reserve')
 ls=latch.copy();ls.rotate(axis,A.Vector(0,0,1),-b['door_outward_deg']);add('BackboxDoorLatchOpenV27',ls,'REVIEW_STATE','Open door latch')
 add('BackglassDisplayEnvelopeV27',box(b['display_box_mm']),'ELECTRONICS_ZONE','740 × 450 × 100 replaceable backglass envelope / front removal')
 add('BackboxDMDEnvelopeV27',box(b['dmd_box_mm']),'ELECTRONICS_ZONE','DMD replaceable module')
 add('BackboxLightingEnvelopeV27',box(b['lighting_box_mm']),'ELECTRONICS_ZONE','Serviceable upper lighting / low voltage')
 for side,spec in zip(('Left','Right'),b['speaker_boxes_mm']):
  xx,yy,zz,w,d,h=spec
  add('BackboxSpeaker'+side+'EnvelopeV27',box(spec),'ELECTRONICS_ZONE','Conventional backbox speaker module — replaceable')
  add('BackboxSpeaker'+side+'CarrierV27',box([xx,yy-6,zz,w,6,h]),'REMOVABLE_CARRIER','Front-removable speaker baffle '+side,'BB-SPEAKER-'+side.upper()+'-R1')
  # Rearward carrier arms reach existing adjustable rail cage, not door.
  rx=150 if side=='Left' else 450
  add('BackboxSpeaker'+side+'ArmV27',box([rx-10,yy+d,zz+45,20,1215.1-(yy+d),20]),'LOCAL_METAL','Speaker bracket to fixed adjustable rail cage; adapter-only')
 add('BackboxRearAccessEnvelopeV27',box([60,1328.1,660,480,250,440]),'ACCESS_ZONE','Rear hands/tools access; front bezel removed for whole monitor')
 add('BackglassFrontRemovalEnvelopeV27',box([-70,754.1,780,740,300,450]),'ACCESS_ZONE','FULL DISPLAY REPLACEMENT — front bezel removed')
 for i,(xx,zz) in enumerate(c['exhaust']['centers_xz_mm'],1):
  w,h,t=c['exhaust']['adapter_size_mm'];plate=box([xx-w/2,1308.1,zz-h/2,w,t,h]);plate=plate.cut(Part.makeCylinder(43,t+2,A.Vector(xx,1307.1,zz),A.Vector(0,1,0)))
  for dx,dz in [(-60,-45),(60,-45),(-60,45),(60,45)]:plate=plate.cut(Part.makeCylinder(2.25,t+2,A.Vector(xx+dx,1307.1,zz+dz),A.Vector(0,1,0)))
  add('BackboxExhaustCarrier'+str(i)+'V27',plate,'REMOVABLE_CARRIER','Fixed upper exhaust adapter / fans purchased later','BB-EXHAUST-CARRIER-'+str(i)+'-R1')
  add('BackboxExhaustFanEnvelope'+str(i)+'V27',box([xx-60,1250.1,zz-60,120,40,120]),'ELECTRONICS_ZONE','120-class exhaust reserve; fan pattern only on adapter')
 # Airflow route is illustrative; no thermal performance or forced-flow claim.
 for route,points in enumerate(c['airflow_review_routes_mm'],1):
  for i,(p,q) in enumerate(zip(points,points[1:]),1):add('AirflowRoute'+str(route)+'Segment'+str(i)+'V27',rod(p,q,5),'AIRFLOW_ROUTE','Intake → cabinet → matched passages → backbox / upper exhaust')
 group.addProperty('App::PropertyString','PropRetention');group.PropRetention='TWO INDEPENDENT CAPTIVE LOWER PIVOTS + UPPER PINS/KEEPERS; NO FRICTION'
 group.addProperty('App::PropertyString','ManufacturingStatus');group.ManufacturingStatus='BLOCKED — stock, tool coupon, measured interfaces, proof and manual lift checks'
 doc.recompute()
 out=ROOT/'exports/generated';out.mkdir(exist_ok=True)
 # Include existing replaceable carriers explicitly; do not count them as added structure.
 for n,pid in [('RearCPUShelfStowedV24','PC-REAR-SHELF-002-R1'),('UtilityAMainsCarrierV26','IO-MAINS-CARRIER-R1'),('UtilityAEthernetCarrierV26','IO-ETHERNET-CARRIER-R1'),('VesaAdapterEnvelopeV18','PF-VESA-CARRIER-R1')]:
  carriers.append(dict(part_id=pid,object_name=n,construction_class='REMOVABLE_CARRIER',material='existing replaceable board/metal adapter',attachment='measured bolts; no glue',electronics_holes='ADAPTER_ONLY',manufacturing_ready='false'))
 with (out/'removable-carriers.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(carriers[0]),lineterminator='\n');w.writeheader();w.writerows(carriers)
 (out/'owner-services-design.json').write_text(json.dumps(dict(features=features(c),prop_lengths_mm=lengths,carriers=carriers),indent=2)+'\n')
 print('OWNER_SERVICES_GENERATED',len(carriers),'replaceable carriers; manual props and visible controls')
