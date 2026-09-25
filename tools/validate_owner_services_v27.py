"""Owner decision constraints and project geometry screens; not load certification."""
import csv,json,math,copy
from pathlib import Path
from owner_features_v27 import config,features
ROOT=Path(__file__).resolve().parents[1]
def lift_estimate(c=None):
 c=c or config();m=json.loads((ROOT/'config/playfield_mechanics_v18.json').read_text());h=m['hinge_axis'];load=m['load_policy']['moving_mass_design_kg'];dm=m['display_envelope']['mass_limit_kg'];cm=m['cradle']['estimated_cradle_mass_kg'];a=math.atan2(596.9-400.05,1308.1-180.975);v=c['props']['manual_lift']
 cg=[(dm*x+cm*y)/load for x,y in zip(v['display_cg_local_yz_mm'],v['cradle_cg_local_yz_mm'])];hy,hz=h['local_y_from_display_front_mm'],h['local_z_from_display_base_mm'];gy,gz=v['grip_local_yz_mm'];samples=[]
 for deg in range(int(h['relative_service_open_angle_deg'])+1):
  t=a-math.radians(deg);arm=abs((cg[0]-hy)*math.cos(t)-(cg[1]-hz)*math.sin(t));grip=abs((gy-hy)*math.cos(t)-(gz-hz)*math.sin(t));samples.append(load*9.81*arm/grip)
 return dict(moving_mass_kg=load,assumed_cg_local_yz_mm=cg,vertical_hand_force_peak_n=max(samples),vertical_hand_force_closed_n=samples[0],vertical_hand_force_open_n=samples[-1],kgf_equivalent=max(samples)/9.81,status='ESTIMATE ONLY: uniform display/cradle mass assumptions; bearing friction and handling overhead excluded; measure actual manual effort before use')
def validate(c=None,hardware=None):
 c=c or config();p=c['props'];v=c['bottom_intake'];e=c['electronics'];b=c['backbox'];m=json.loads((ROOT/'config/playfield_mechanics_v18.json').read_text());a=json.loads((ROOT/'config/playfield_fixed_anchors_v19.json').read_text())
 assert 'gas_struts' not in m and 'gas_strut_fixed_anchor' not in a,'baseline gas dependency'
 assert p['count']==2 and p['lower_pivot_captive'] and p['each_rod_supports_full_moving_load'],'two independent props'
 assert p['upper_receiver_lock']=='transverse captive pin with positive keeper' and not p['friction_support'],'positive retention not friction'
 assert p['stow']=='rearward from fixed pivot; positive closed clip','positive stow'
 assert c['ssf']['solid_panel_required'] and not c['ssf']['bottom_subwoofer_opening'],'solid exciter backing'
 assert c['controls']['final_holes']=='BLOCKED_MEASURE_HARDWARE','control holes must stay blocked'
 assert len(e['tray_x_mm'])==2 and not e['bridge'],'minimal two carrier system'
 assert e['tray_x_mm'][0]+e['tray_size_mm'][0]<e['central_access_box_mm'][0],'left central aisle'
 assert e['tray_x_mm'][1]>e['central_access_box_mm'][0]+e['central_access_box_mm'][3],'right central aisle'
 assert e['tray_y_mm']+e['tray_size_mm'][1]<825,'CPU rail/service clearance'
 assert b['door_outward_deg']>=100 and not b['door_primary_shear'],'outward non-structural closure'
 # Slot-to-slot, crossmember and structural perimeter webs; material changes trigger review.
 t=json.loads((ROOT/'config/cabinet_structure_v20.json').read_text())['cabinet']['nominal_wood_mm']
 assert v['minimum_web_mm']>=t,'minimum slot web'
 assert min(y-x for x,y in zip(v['row_center_y_mm'],v['row_center_y_mm'][1:]))-v['slot_width_mm']>=v['minimum_web_mm'],'intake slot ligament'
 assert v['bank_center_x_mm'][1]-v['bank_center_x_mm'][0]-v['slot_length_mm']>=v['minimum_web_mm'],'intake center spine'
 assert min(v['row_center_y_mm'])-v['slot_width_mm']/2-278>=v['minimum_perimeter_ligament_mm'],'front intake ligament'
 assert 650-max(v['row_center_y_mm'])-v['slot_width_mm']/2>=v['minimum_perimeter_ligament_mm'],'rear intake ligament'
 assert min(v['bank_center_x_mm'])-v['slot_length_mm']/2-18>=v['minimum_perimeter_ligament_mm'],'side intake ligament'
 assert min(e['crossmember_mount_z_mm']-36,116-e['crossmember_mount_z_mm'])>=4*6,'M6 crossmember edge screen'
 assert min(min(e['crossmember_mount_x_mm'])-12,588-max(e['crossmember_mount_x_mm']))>=7*6,'M6 loaded end screen'
 hw=hardware if hardware is not None else list(csv.DictReader((ROOT/'bom/HARDWARE_FREEZE_V25.csv').open()))
 assert not any(r['item_id']=='HF-011' or ('gas strut' in r['item'].lower() and r['freeze_class']=='MEASURE_BEFORE_CNC') for r in hw),'gas CNC requirement'
 assert next(r for r in hw if r['item_id']=='HF-030')['freeze_class']=='MEASURE_BEFORE_CNC','plunger measurement'
 assert all(next(r for r in hw if r['item_id']==i)['freeze_class']=='ADAPTER_ONLY' for i in ('HF-031','HF-032','HF-033')),'late adapters'
 assert c['manufacturing_ready'] is False,'manufacturing gate'
 return lift_estimate(c)
def negatives():
 base=config()
 for name,mutate in [('friction support',lambda c:c['props'].update(friction_support=True)),('single prop',lambda c:c['props'].update(count=1)),('SSF opening',lambda c:c['ssf'].update(bottom_subwoofer_opening=True)),('weak vent web',lambda c:c['bottom_intake'].update(slot_width_mm=25)),('released controls',lambda c:c['controls'].update(final_holes='FROZEN')),('central obstruction',lambda c:c['electronics'].update(tray_size_mm=[250,355,6]))]:
  c=copy.deepcopy(base);mutate(c)
  try:validate(c)
  except AssertionError:print('OWNER_CONFIG_NEGATIVE_PASS',name)
  else:raise AssertionError('Accepted '+name)
 hw=list(csv.DictReader((ROOT/'bom/HARDWARE_FREEZE_V25.csv').open()));hw.append(dict(item_id='HF-011',item='Gas struts',freeze_class='MEASURE_BEFORE_CNC'))
 try:validate(hardware=hw)
 except AssertionError:print('OWNER_CONFIG_NEGATIVE_PASS gas release blocker')
 else:raise AssertionError('Accepted gas blocker')
if __name__=='__main__':print('OWNER_CONFIG_PASS',validate());negatives()
