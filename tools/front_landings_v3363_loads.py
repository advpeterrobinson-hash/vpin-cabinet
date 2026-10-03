"""Explicit planning reactions and relative bending screen, not certification.
Original CERN-OHL-S-2.0. Unknown purchased masses remain visible assumptions.
"""
from pathlib import Path
import json,sys,hashlib,math
import FreeCAD as A, Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,PF
O=R/'exports/generated/front-landings-v3363';C=json.loads((R/'config/front_landings_v3363.json').read_text())
source=R/C['source'];p=load(source);g=9.80665
def com(s):
 v=sum(q.Volume for q in s.Solids)
 return [sum(q.Volume*getattr(q.CenterOfMass,k) for q in s.Solids)/v for k in 'xyz']
mass=json.loads((R/'exports/generated/playfield-rest-v3362/mass-budget.json').read_text())
fm=next(q['mass_kg'] for q in mass['estimated_hardware_items'] if q['id']=='F02')
dowel=next(q['mass_kg'] for q in mass['estimated_hardware_items'] if q['id']=='H01')
base=p['PF_BasePlywood'];display=p['PLAYFIELD_ENVELOPE'];front=C['search']['selected_pad_y_mm'];rear=PF.y
parts=[{'name':'M025','mass_kg':base.Volume*650/1e9,'center_xyz_mm':com(base),'status':'ESTIMATED_FROM_ACTUAL_BREP_VOLUME','density_kg_m3':650},
       {'name':'H01 wood dowel','mass_kg':dowel,'center_xyz_mm':com(p['PF_WoodDowel']),'status':'ESTIMATED_EXISTING_H01_MODEL_DENSITY700'},
       {'name':'F02 eight strap screws','mass_kg':fm,'center_xyz_mm':[300,PF.y,PF.z],'status':'ESTIMATED_EXISTING_F02_NOMINAL_MODELS'}]
allowances={'four_straps_kg':[.20,.40,.60],'display_adapter_kg':[.25,.50,1.00],'new_receiver_pair_kg':[.015,.025,.05]}
scenarios=[]
for payload in [10,12,15]:
 for i,label in enumerate(['LOW','NOMINAL','HIGH']):
  # Unknown strap mass sits at rear; unknown adapter at native VESA envelope
  # center. Receiver allowance sits at the specified retention center.
  case=parts+[{'name':'display','mass_kg':payload,'center_xyz_mm':com(display)},
      {'name':'straps allowance','mass_kg':allowances['four_straps_kg'][i],'center_xyz_mm':[300,PF.y,PF.z]},
      {'name':'adapter allowance','mass_kg':allowances['display_adapter_kg'][i],'center_xyz_mm':com(p['PF_VESAEnvelope'])},
      {'name':'receiver allowance','mass_kg':allowances['new_receiver_pair_kg'][i],'center_xyz_mm':[300,front+30,365]}]
  total=sum(q['mass_kg'] for q in case)
  rf=sum(q['mass_kg']*g*(rear-q['center_xyz_mm'][1])/(rear-front) for q in case);rr=total*g-rf
  side=rf/2;lever=C['landing']['pad_left_x_mm']-18;row=36
  scenarios.append({'display_payload_kg':payload,'hardware_scenario':label,'moving_mass_kg':total,'front_pair_vertical_N':rf,'front_each_vertical_N':side,'rear_line_vertical_N':rr,'rear_each_symmetric_N':rr/2,
    'factor2_front_each_N':side*2,'factor2_rear_line_N':rr*2,
    'inclined_contact_horizontal_pair_N':rf*math.tan(math.radians(9.906669253650632)),
    'factor2_body_wall_moment_Nm':side*2*lever/1000,
    'factor2_upper_screw_pullout_demand_each_N':side*2*lever/row/2,
    'factor2_four_side_screw_shear_demand_each_N':side*2/4,
    'T1_front_pair_vertical_N_same_payload':sum(q['mass_kg']*g*(rear-q['center_xyz_mm'][1])/(rear-380) for q in case)})
overhangs={}
for name,y in [('T1_shoes',380),('front_side_landings',front)]:
 a=y-base.BoundBox.YMin; ad=y-display.BoundBox.YMin
 overhangs[name]={'support_y_mm':y,'base_front_overhang_mm':a,'display_front_overhang_mm':ad,
  'tip_load_moment_per_N_Nmm':a,'tip_deflection_coefficient_L3_over_3':a**3/3,
  'uniform_line_load_moment_coefficient_L2_over_2':a*a/2,'uniform_deflection_coefficient_L4_over_8':a**4/8}
a=overhangs['front_side_landings']['base_front_overhang_mm'];b=overhangs['T1_shoes']['base_front_overhang_mm']
ratio=a/b
face=max([f for f in base.Faces if type(f.Surface).__name__=='Plane' and f.normalAt(0,0).z<-.5],key=lambda f:f.Area)
up=-face.normalAt(0,0);ctr=face.CenterOfMass
zz=ctr.z-up.y/up.z*(front-ctr.y)
footprints={}
for radius in [12,14]:
 disk=Part.Face(Part.Wire(Part.makeCircle(radius,A.Vector(72,front,zz),up)))
 # Closed inner wires are actual cutout edges. Outer front-relief landmarks
 # use original vertices around localY107/installedY~150; side edge excluded.
 relief_edges=[e for e in face.OuterWire.Edges if e.BoundBox.YMin<160 and 145<e.BoundBox.YMax<165 and e.BoundBox.XMax<110]
 footprints[str(radius)]={'diameter_mm':radius*2,'actual_contact_area_mm2':disk.common(face).Area,'contact_disk_area_mm2':disk.Area,
  'outer_edge_clearance_mm':disk.distToShape(face.OuterWire)[0],
  'front_relief_transition_clearance_mm':min(disk.distToShape(e)[0] for e in relief_edges),
  'VESA_reserve_clearance_mm':disk.distToShape(p['PF_VESAEnvelope'])[0],
  'nearest_inner_opening_clearance_mm':min(disk.distToShape(w)[0] for w in face.Wires if not w.isSame(face.OuterWire))}
report={'source':str(source.relative_to(R)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'pass':all(x['front_pair_vertical_N']>0 and x['rear_line_vertical_N']>0 for x in scenarios),
 'scope':'Static vertical reactions from actual B-rep centers of volume and explicit mass assumptions. No allowable load, screw capacity, plywood modulus or structural certification is asserted.',
 'gravity_m_s2':g,'current_slope_deg':9.906669253650632,'front_support_y_mm':front,'rear_support_y_mm':rear,
 'known_model_items':parts,'unknown_actual_masses':{'straps':'UNKNOWN','display_adapter':'UNKNOWN','new_retention_receivers':'UNKNOWN'},'planning_allowances_LOW_NOMINAL_HIGH':allowances,
 'payload_scenarios':scenarios,'overhang_comparison':overhangs,
 'relative_front_vs_T1':{'tip_moment':ratio,'tip_deflection_tendency_same_EI':ratio**3,'uniform_moment':ratio**2,'uniform_deflection_tendency_same_EI':ratio**4},
 'compact_and_wider_contact_comparison':footprints,
 'contact_selection':'Two compact24mm articulated pads retain10mm base-edge margin.28mm pads provide more bearing but reduce edge margin to8mm; contact area is already generous for planning reactions, so no wider pad or full-width rail is required.',
 'transverse_rail':'NOT_NEEDED: same two adjustable contact functions would require a full564mm cross-cabinet member, longer load path and additional obstruction. No rail motion/strength PASS is claimed; compact independent side bodies already meet packaging.',
 'bending_screen':'Cantilever analogy for front overhang only, same load distribution and EI. Conservative minimum front strip width396mm and18mm nominal depth can be used for both; no actual E or plate stiffness is claimed. VESA load distribution and whole-board/torsional stiffness require physical proof.',
 'factor2_policy_source':'docs/STRUCTURE_MATERIALS_V13.md#structural-verification-envelope','factor2_status':'Provisional force multiplier; not a defined acceleration spectrum, impact/drop rating or arbitrary transport qualification.',
 'side_attachment':'Four screws per body transfer shear plus a tension/compression couple into full18mm side. No wall-friction support credited.36mm screw-row separation,12mm nominal embedment,6mm remaining exterior skin. Calculated demands are not screw capacities.',
 'retention':'Two positive threaded clamps separate from the landing contact. Captive retraction before opening. Specify receiver pull-out and closed uplift proof using at least the force sensitivity case; actual hardware and drilling guide remain held.',
 'adjustment':'Two adjusters compensate local stack/assembly tolerance to reproduce the same intended rigid pose. They do not authorize twisting a rigid board against a fixed rear axis; set matching front heights and full rear seating.',
 'required_physical_qualification':['actual plywood/adhesive/insert pilot coupon','side screw shear/pull-out at12mm embedment including cyclic/nudge load','M025 receiver pull-out and remaining skin','lamination shear and two binder screws','whole-base VESA load distribution and deflection','both closed clamps engaged; bounce/rattle and repeatable release','front/side angle setup using measured stock; no arbitrary opposite adjuster settings'],
 'manufacturing_release':False}
(O/'load-screen.json').write_text(json.dumps(report,indent=2)+'\n');print('V3363_LOAD_SCREEN_PASS',len(scenarios))
