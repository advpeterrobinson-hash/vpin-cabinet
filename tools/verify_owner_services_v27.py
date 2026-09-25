"""Saved-solid owner-review checks, including deliberate adversarial mutations."""
import json,csv,math
from pathlib import Path
import FreeCAD as A
import Part
from owner_features_v27 import config,features
from build_owner_services_v27 import cut_shape,box,rod
from validate_owner_services_v27 import validate,lift_estimate
ROOT=Path(__file__).resolve().parents[1]

def verify(doc,check):
 c=config();validate(c)
 def s(n):
  o=doc.getObject(n)
  if not o or not hasattr(o,'Shape') or o.Shape.isNull():raise RuntimeError('Missing owner geometry '+n)
  return o.Shape
 def clear(a,b):return a.common(b).Volume<1e-4
 def same(a,b):return a.cut(b).Volume+b.cut(a).Volume<1e-4
 check('no baseline gas geometry',not any('gasstrut' in o.Name.lower() or 'gasanchor' in o.Name.lower() for o in doc.Objects))
 pattern=list(csv.DictReader((ROOT/'bom/CNC_FEATURES_V25.csv').open()))
 check('no gas CNC dependency',not any('HF-011' in r['hardware_dependency'] for r in pattern))
 check('controls and plunger holes remain measured-hardware blocked',all(r['status']=='BLOCKED_MEASURE_HARDWARE' and all(not r[k] for k in ('x','y','diameter_or_width','depth')) for r in pattern if r['hardware_dependency'] in ('HF-020','HF-030')) and any(r['hardware_dependency']=='HF-030' for r in pattern))
 carrier_names=['ElectronicsCarrierLeftV27','ElectronicsCarrierRightV27'];payload=['ElectronicsLeftPayloadEnvelopeV27','ElectronicsRightPayloadEnvelopeV27'];central=s('CentralServiceKeepoutV27')
 check('two narrow carriers preserve central service volume',all(clear(s(n),central) for n in carrier_names+payload) and not c['electronics']['bridge'])
 obstacles=[o.Name for o in doc.Objects if o.Name.startswith(('CradleSide','CradleCross','CradlePivot','CradleRear','ClassicLeg','SSF','ClosedSupportDoubler','SafetyStayDoubler','RearCPUFixedSlide','RearCPUSupportRail'))]
 controls=[o.Name for o in doc.Objects if (o.Name.startswith('Control') and any(k in o.Name for k in ('Internal','Cable'))) or o.Name.startswith(('PlungerBody','PlungerCable'))]
 bad=[(n,m) for n in controls for m in obstacles if not clear(s(n),s(m))]
 check('button and plunger envelopes clear cradle legs anchors and SSF',not bad,bad)
 # Real front/side sheet stays solid: visible control envelopes are NOT drilled bores.
 check('front has no unmeasured coin/button/plunger cuts',same(s('CapturedFrontPanelV20'),box([12,0,0,576,18,400.05])))
 for side,x in [('Left',0),('Right',582)]:
  wall=s('Cabinet'+side+'Side')
  for p in ('Front','Rear'):
   zone=s('SSF'+p+side+'KeepoutV20').BoundBox
   skin=box([x,zone.YMin,zone.ZMin,18,zone.YLength,zone.ZLength])
   check(p+' '+side+' SSF retains full solid plywood',skin.cut(wall).Volume<1e-4)
  for y,z in c['controls']['side_positions_yz_mm']:
   skin=box([x,y-18,z-18,18,36,36])
   check(side+' button reserve has no released bore '+str(y),skin.cut(wall).Volume<1e-4)
 # Generic bottom profiles: actual wood, not just marked envelopes.
 original=box([12,12,18,576,1284.1,18]);expected=original
 for f in features(c):
  if f['part']=='CapturedBottomV20':expected=expected.cut(cut_shape(f))
 check('bottom intake matches generic slots and filter grid',same(s('CapturedBottomV20'),expected) and len(s('CapturedBottomV20').Solids)==1)
 fixed=[o.Name for o in doc.Objects if o.Name.startswith(('ClassicLeg','RearCPUSupport','CPURailBacking','CPURailAngle','SSF'))]
 intakecuts=[s('Defined'+f['key']+'CutV27') for f in features(c) if f['part']=='CapturedBottomV20']
 check('intake and filter fixings clear leg CPU and SSF zones',all(clear(cut,s(n)) for cut in intakecuts for n in fixed))
 check('filter cassette is externally serviceable below bottom',s('BottomFilterCarrierV27').BoundBox.ZMax<=18+1e-6 and all(clear(s('BottomFilterCarrierV27'),s(n)) for n in fixed))
 # Every standardized permanent cut is present and checked against the host wood.
 check('all generic carrier vent and passage cuts are real',all(clear(s(f['part']),cut_shape(f)) for f in features(c)))
 for i,y in [(1,260),(2,650)]:
  expected=box([12,y,36,576,18,80])
  for f in features(c):
   if f['part']==f'LowCrossmember{i}V20':expected=expected.cut(cut_shape(f))
  check('crossmember '+str(i)+' retains only standardized carrier holes',same(s(f'LowCrossmember{i}V20'),expected))
 check('third low crossmember retained intact',same(s('LowCrossmember3V20'),box([12,1040,36,576,18,80])))
 bad=[(n,m) for n in carrier_names+payload for m in obstacles if not clear(s(n),s(m))]
 check('carriers and payloads clear cradle legs SSF and rails',not bad,bad)
 bad=[]
 for n in ['RearCPUShelfStowedV24','RearCPUOpenCaseStowedV24','RearCPUFixedSlideLeftV24','RearCPUFixedSlideRightV24']:
  b=s(n).BoundBox;sweep=box([b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength+450,b.ZLength])
  for m in carrier_names+payload:
   if not clear(sweep,s(m)):bad.append((n,m))
 check('carriers clear full CPU extraction sweep',not bad,bad)
 # Prop geometry and keeper presence are required, not only descriptive labels.
 for side in ('Left','Right'):
  prop=doc.getObject('SafetyStayOpen'+side+'V18')
  hardware=['PropFixedClevis'+side+'V27','PropLowerPivotPin'+side+'V27','PropReceiver'+side+'OpenV27','PropUpperLockPin'+side+'OpenV27','PropPinKeeper'+side+'OpenV27','PropStowClip'+side+'V27','PropStowKeeper'+side+'V27','PropStowBracket'+side+'V27']
  present=prop is not None and all(doc.getObject(n) is not None for n in hardware)
  check(side+' prop has positive pins keepers and stow capture',present and getattr(prop,'SupportMode','')=='PINNED_POSITIVE' and getattr(prop,'FrictionSupport',True) is False)
  if present:
   check(side+' raised prop clears raised cradle',clear(prop.Shape,s('CradleOpenGhostV18')))
   check(side+' stowed prop clears closed mechanics and carriers',all(clear(s('PropRod'+side+'StowedV27'),s(n)) for n in obstacles+carrier_names+payload))
   check(side+' fixed prop hardware clears closed cradle',all(clear(s(m),s(n)) for m in ['PropFixedClevis'+side+'V27','SafetyStayNutPlate'+side+'V19','PropStowClip'+side+'V27','PropStowBracket'+side+'V27'] for n in obstacles if n.startswith('Cradle')))
   check(side+' prop receivers attach to outer cradle rail',s('PropReceiver'+side+'ClosedV27').distToShape(s('CradleSideRail'+side+'V18'))[0]<1e-5)
   check(side+' upper pin engages prop and receiver',s('PropUpperLockPin'+side+'OpenV27').distToShape(prop.Shape)[0]<1e-5 and s('PropUpperLockPin'+side+'OpenV27').distToShape(s('PropReceiver'+side+'OpenV27'))[0]<1e-5)
   check(side+' keeper intercepts withdrawal of upper pin',not clear(s('PropUpperLockPin'+side+'OpenV27'),s('PropPinKeeper'+side+'OpenV27')))
   # Sample the simple one-axis rod deployment only after the playfield is raised.
   b=s('PropLowerPivotPin'+side+'V27').BoundBox;axis=A.Vector(28 if side=='Left' else 572,(b.YMin+b.YMax)/2,(b.ZMin+b.ZMax)/2)
   rod0=s('PropRod'+side+'StowedV27');angle=math.degrees(math.atan2(s('SafetyStayOpen'+side+'V18').BoundBox.ZMax-axis.z,s('SafetyStayOpen'+side+'V18').BoundBox.YMax-axis.y))
   bad=[]
   for deg in range(0,int(angle)+1,2):
    moving=rod0.copy();moving.rotate(axis,A.Vector(1,0,0),deg)
    for n in ['CradleOpenGhostV18','RearShelfV14','RearCPUOpenCaseStowedV24']+carrier_names:
     if not clear(moving,s(n)):bad.append((deg,n))
   check(side+' prop deployment sweep clears raised structure (2 degree samples)',not bad,bad[:5])
 # Mandatory service door, actual outward transform and sampled sweep.
 door=doc.getObject('BackboxServiceDoorV14')
 check('backbox service door BB-DOOR-001-R1 retained',door is not None and getattr(door,'PartID','')=='BB-DOOR-001-R1')
 if door:
  db=door.Shape.BoundBox;axis=A.Vector(db.XMax,db.YMax,db.ZMin);expected=door.Shape.copy();expected.rotate(axis,A.Vector(0,0,1),-c['backbox']['door_outward_deg'])
  check('backbox door actual outward 105 degree transform',same(s('BackboxDoorOpenV27'),expected) and s('BackboxDoorOpenV27').BoundBox.YMin>=db.YMax-1e-6)
  bad=[]
  names=[o.Name for o in doc.Objects if o.Name.startswith(('BackboxRearFrame','BackboxExhaustCarrier'))]+['BackboxFloorV14','BackboxTopV14','BackboxLeftSideV14','BackboxRightSideV14','BackboxDoorStopV27']
  for deg in range(106):
   moving=door.Shape.copy();moving.rotate(axis,A.Vector(0,0,1),-deg)
   for n in names:
    if not clear(moving,s(n)):bad.append((deg,n))
  check('backbox door sampled outward sweep clears fixed structure',not bad,bad[:5])
  check('open backbox door clears rear service approach',clear(s('BackboxDoorOpenV27'),s('BackboxRearAccessEnvelopeV27')))
 check('fixed upper exhaust is independent of door',all(s('BackboxExhaustCarrier'+str(i)+'V27').BoundBox.ZMin>1110 for i in (1,2)))
 # Registers distinguish permanent structure, closures and carriers.
 rows=list(csv.DictReader((ROOT/'bom/ACTIVE_PARTS.csv').open()));carriers=list(csv.DictReader((ROOT/'bom/REMOVABLE_CARRIERS_V27.csv').open()))
 check('29 structural wood plus 2 closures and CPU board reconciled',len(rows)==32 and sum(r['construction_class']=='PERMANENT_STRUCTURE' for r in rows)==29 and {r['object_name'] for r in rows}=={o.Name for o in doc.Objects if getattr(o,'EngineeringRole','')=='STRUCTURAL_WOOD'})
 check('11 removable carriers separately registered',len(carriers)==11 and len({r['part_id'] for r in carriers})==11 and all(doc.getObject(r['object_name']) for r in carriers))
 v=c['bottom_intake'];area=len(v['bank_center_x_mm'])*len(v['row_center_y_mm'])*((v['slot_length_mm']-v['slot_width_mm'])*v['slot_width_mm']+math.pi*(v['slot_width_mm']/2)**2)
 out=ROOT/'exports/generated';(out/'owner-services-analysis.json').write_text(json.dumps(dict(lift=lift_estimate(c),intake_open_area_mm2=area,intake_bottom_area_fraction=area/(576*1284.1),minimum_slot_web_mm=v['minimum_web_mm'],permanent_structure=29,wood_assembly_records=32,removable_carriers=len(carriers),manufacturing_ready=False),indent=2)+'\n')
