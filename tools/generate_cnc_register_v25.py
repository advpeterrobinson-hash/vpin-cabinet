"""Build feature and connection ledgers from source-generated detail evidence."""
import csv,json
from pathlib import Path
from generate_measurement_pack_v25 import write
ROOT=Path(__file__).resolve().parents[1]

def dependencies(n):
 out=[]
 if n.startswith('Cabinet'):out += [3,4,6,8,20,21]
 if n=='CapturedFrontPanelV20':out += [3,4,19,20,22]
 if n=='RearPanelWithCPUHatchV24':out += [3,4,15,16,17,27]
 if n=='CapturedBottomV20':out += [26]
 if n=='RearShelfV14':out += [7]
 if n=='BackboxFloorV14':out += [6,7]
 if n.startswith('Backbox') and ('Side' in n):out += [6]
 if n.startswith('BackboxRearFrame') or n=='BackboxServiceDoorV14':out += [29]
 if n.startswith('CradleSideRail'):out += [10,11,12]
 if n.startswith('CradlePivot') or n=='CradleRearBeamV18':out += [9]
 if n.startswith('ClosedSupportDoubler'):out += [12]
 if n.startswith('SafetyStayDoubler'):out += [10]
 if n.startswith('GasStrutDoubler'):out += [11]
 if n=='RearCPUServiceDoorClosedV24':out += [15,16]
 if n.startswith('RearCPUSupportRail'):out += [13,26,28]
 if n=='RearCPUShelfStowedV24':out += [13,14,26]
 return out

def classify(a,b,ops):
 pair={a,b};op=[x for x in ops if {x['part'],x['mate']}==pair]
 if a.startswith('Cabinet') and b.startswith('Backbox') or a=='RearPanelWithCPUHatchV24' and b.startswith('BackboxRear') or a=='RearShelfV14' and b.startswith('BackboxRear'):
  return 'INCIDENTAL_CONTACT','none','none','none','none','Clearance/interface contact; backbox retention uses hinge and locks, not glue to shell'
 if 'BackboxFloorV14' in pair and any(n in pair for n in ('RearShelfV14','RearPanelWithCPUHatchV24')):
  return 'REMOVABLE_BEARING','none','NO','HF-006;HF-007','BLOCKED_MEASURE_HARDWARE','Backbox floor bears on shelf; positive upright locks and hinge carry retention'
 if any('ServiceDoor' in n for n in pair):
  return 'REMOVABLE_CLOSURE','none','NO','HF-029' if any('Backbox' in n for n in pair) else 'HF-015;HF-016','BLOCKED_MEASURE_HARDWARE','No glue; hinge/catch CNC patterns require measured closure hardware'
 if any(n.startswith('RearCPUSupport') for n in pair):
  return 'BOTTOM_BEARING_CLAMP','none','NO','HF-026','BLOCKED_MEASURE_HARDWARE','Bottom compression; four angle/backing assemblies resist uplift; rail cannot rely on end-grain screws'
 if any('Doubler' in n for n in pair) and any(n.startswith('Cabinet') for n in pair):
  return 'FACE_LAMINATION','0','YES','HF-'+('010' if 'Safety' in b else '011' if 'Gas' in b else '012'),'BLOCKED_MEASURE_HARDWARE','Clamp full face; CNC alignment outline; through-bolts/backing carry concentrated loads'
 if op:
  return 'CAPTURE_OR_LAP','t/3; exact removed solid in detail model','YES','none','DESIGN_LOCATABLE','Dry fit; glue full bearing surfaces; clamp square. Supplemental screw locations must avoid load hardware zones; pilot diameter from selected screw/coupon'
 if a.startswith('BackboxRearFrame') and b.startswith('BackboxRearFrame'):
  return 'BUTT_FRAME_CORNER','0','YES','none','DESIGN_LOCATABLE','Frame strips captured by surrounding perimeter; glue butt plus perimeter captures; corner screw optional, not assumed to carry shear alone'
 if a=='CapturedBottomV20' and b.startswith('LowCrossmember'):
  return 'SEATED_BUTT','0','YES','none','DESIGN_LOCATABLE','Crossmember end dados locate member; full bottom bearing; glue and clamp; no extra blocking'
 if 'CradleRearBeamV18' in pair:
  return 'PIVOT_BEAM_BUTT','0','YES','HF-009','BLOCKED_MEASURE_HARDWARE','Beam joins laminated pivot ends; through-bolt reinforcement design remains coupled to cheek plates; proof test required'
 return 'REVIEW_INTERFACE','0','NO','none','BLOCKED_DESIGN','Explicit contact requires load-path review before release'

def main():
 rows=list(csv.DictReader((ROOT/'bom/ACTIVE_PARTS.csv').open()));by={r['object_name']:r for r in rows}
 g=json.loads((ROOT/'exports/generated/cnc-detail/geometry.json').read_text());features=[];joints=[]
 def add(n,typ,status,dependency='',x='',y='',size='',depth='',notes='',face='see part orientation',through='false',recipe=''):
  features.append(dict(part_id=by[n]['part_id'],feature_id='CF-%04d'%(len(features)+1),feature_type=typ,face=face,datum='part-local lower-left on indicated machining face; CAD global axes retained in recipe',x=x,y=y,diameter_or_width=size,depth=depth,through=through,hardware_dependency=dependency,status=status,recipe=recipe,notes=notes))
 for n,r in by.items():
  add(n,'PROFILE','DEFINED_PARAMETRIC',size=r['nominal_local_envelope_xyz_mm'],depth='t_door' if 'Door' in n else 't or laminated 2*t',through='true',recipe='detail_structure_v25:'+n,notes='Exact contour is saved detail solid, not bounding rectangle. Preview dimensions only; stock/tool/fit gate HF-001/002. Laminated 2*t records require two identified plies at nesting.')
  add(n,'ENGRAVING','DEFINED_PARAMETRIC',x='safe_interior_label_zone.x',y='safe_interior_label_zone.y',depth='shop_confirmed_shallow_mark',recipe=r['part_id']+'; '+r['orientation'],notes='Place clear of pockets/hardware zones at CAM; no final marking coordinates until nested orientation is fixed')
  for h in dependencies(n):
   typ='POCKET' if h==19 else 'PROFILE' if h==28 else 'THROUGH_HOLE'
   add(n,typ,'BLOCKED_MEASURE_HARDWARE',dependency='HF-%03d'%h,notes='Pattern group, not one physical hole. Coordinates/diameter/depth intentionally blank. No builder transfer drilling. See measurement pack.')
 for i,o in enumerate(g['operations']):
  n=o['part'];add(n,o['type'],'DEFINED_PARAMETRIC',depth='t/3 capture or mating profile trim; see exact solid',recipe='geometry.json:operations[%d]'%i,notes='Global removed-volume bounds '+','.join('%.3f'%x for x in o['bounds'])+'; no hardware coordinates; zero-clearance review, tool relief pending')
 for n in ('RearCPUSupportRailLeftV24','RearCPUSupportRailRightV24'):
  add(n,'POCKET','DEFINED_PARAMETRIC',x='crossmember_y - rail_y - clearance/2',y='0',size='t+clearance',depth='crossmember_height',through='true',recipe='build_rear_utility_v26 rail saddle',notes='Keep rail outline and bottom bearing; saddle spans crossmember at Y1040. Slide/clamp holes blocked; 13.8 mm gap retained.')
 for feature,x,z,w,h in [('CPU',130,110,340,240),('MAINS',60,405,70,50),('ETHERNET',518,413,24,24)]:
  add('RearPanelWithCPUHatchV24','CABLE_PASS' if feature!='CPU' else 'PROFILE','DEFINED_PARAMETRIC',x=str(x-12),y=str(z),size=f'{w} x {h}',depth='t',through='true',face='rear XZ, origin global X12 Z0',recipe=feature,notes='Existing generic aperture; hardware patterns separately blocked; local X follows measured capture offset at release')
 # Ensure ventilation and cable routes cannot silently disappear from release scope.
 for n in ('CapturedBottomV20','BackboxRearFrameTopV14','RearShelfV14','BackboxFloorV14'):
  add(n,'VENT' if 'Shelf' not in n and 'Floor' not in n else 'CABLE_PASS','BLOCKED_DESIGN',notes='Airflow/cable cross-section and guarded replaceable carrier interface must be designed before release; no electronics purchase required')
 for i,c in enumerate(g['contacts']):
  a,b=c['a'],c['b'];kind,depth,glue,hardware,fasteners,note=classify(a,b,g['operations'])
  joints.append(dict(joint_id='J-%03d'%(i+1),part_a=by[a]['part_id'],part_b=by[b]['part_id'],object_a=a,object_b=b,joint_type=kind,stock_dependency='t=measured main sheet; t_door=measured door sheet',depth=depth,glue=glue,fastener_requirement=fasteners,cnc_prelocation='YES design datum' if fasteners=='DESIGN_LOCATABLE' else 'BLOCKED measured pattern' if hardware!='none' else 'not applicable',hardware_dependency=hardware,baseline_overlap_mm3='%.3f'%c['overlap_mm3'],notes=note))
 for n in ('CradlePivotDoublerLeftV18','CradlePivotDoublerRightV18','CradleRearBeamV18'):
  joints.append(dict(joint_id='J-%03d'%(len(joints)+1),part_a=by[n]['part_id'],part_b=by[n]['part_id'],object_a=n,object_b=n,joint_type='INTERNAL_LAMINATION',stock_dependency='2*t from two measured plies',depth='0',glue='YES',fastener_requirement='HF-009 through-bolts after measured plate stack',cnc_prelocation='BLOCKED measured pattern',hardware_dependency='HF-009',baseline_overlap_mm3='0',notes='Two plies within one assembly record; full-face glue and clamps; separate ply IDs required at nesting; no 36 mm monolithic stock assumption'))
 write(ROOT/'bom/CNC_FEATURES_V25.csv',features);write(ROOT/'bom/STRUCTURAL_JOINTS_V25.csv',joints)
 print('CNC_REGISTER_GENERATED',len(features),'feature groups;',sum(f['status']=='DEFINED_PARAMETRIC' for f in features),'defined;',sum(f['status']=='BLOCKED_MEASURE_HARDWARE' for f in features),'hardware-blocked;',len(joints),'contacts classified')
if __name__=='__main__':main()
