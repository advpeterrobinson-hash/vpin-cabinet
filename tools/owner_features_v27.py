"""Project-designed generic wood interfaces, independent of purchased hole patterns."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def config():return json.loads((ROOT/'config/owner_services_v27.json').read_text())
def features(c=None):
 c=c or config();cab=json.loads((ROOT/'config/cabinet_structure_v20.json').read_text());t=cab['cabinet']['nominal_wood_mm'];bottom=cab['cnc_joinery']['bottom_panel_bottom_z_mm'];out=[]
 def add(part,key,typ,axis,origin,size,r=0,diameter=None):
  out.append(dict(part=part,key=key,type=typ,axis=axis,origin=origin,size=size,radius=r,diameter=diameter,through=True,status='DEFINED_PARAMETRIC',source='owner_services_v27: project-designed interface; measured stock/tool coupon still required'))
 v=c['bottom_intake']
 for i,x in enumerate(v['bank_center_x_mm']):
  for j,y in enumerate(v['row_center_y_mm']):
   w,h=v['slot_length_mm'],v['slot_width_mm']
   add('CapturedBottomV20',f'Intake{i+1}_{j+1}','VENT','Z',[x-w/2,y-h/2,bottom-1],[w,h,t+2],h/2)
 for i,(x,y) in enumerate(v['filter_mount_xy_mm']):
  add('CapturedBottomV20',f'FilterMount{i+1}','THROUGH_HOLE','Z',[x,y,bottom-1],[0,0,t+2],diameter=v['mount_clearance_diameter_mm'])
 e=c['electronics']
 for j,y in enumerate(cab['cnc_joinery']['crossmember_y_mm'][:2]):
  for i,x in enumerate(e['crossmember_mount_x_mm']):
   add(f'LowCrossmember{j+1}V20',f'CarrierMount{j+1}_{i+1}','THROUGH_HOLE','Y',[x,y-1,e['crossmember_mount_z_mm']],[0,t+2,0],diameter=e['mount_clearance_diameter_mm'])
 p=c['passages']
 for name,z in [('RearShelfV14',596.9-t),('BackboxFloorV14',596.9)]:
  for i,(x,y) in enumerate(p['centers_xy_mm']):
   w,h=p['size_xy_mm'];add(name,f'{name}Passage{i+1}','CABLE_PASS','Z',[x-w/2,y-h/2,z-1],[w,h,t+2],p['corner_radius_mm'])
 for i,(x,z) in enumerate(c['exhaust']['centers_xz_mm']):
  w,h=c['exhaust']['opening_size_mm']
  add('BackboxRearFrameTopV14',f'Exhaust{i+1}','VENT','Y',[x-w/2,1308.1-t-1,z-h/2],[w,t+2,h],c['exhaust']['corner_radius_mm'])
  for j,(dx,dz) in enumerate([(-60,-45),(60,-45),(-60,45),(60,45)]):
   add('BackboxRearFrameTopV14',f'ExhaustMount{i+1}_{j+1}','THROUGH_HOLE','Y',[x+dx,1308.1-t-1,z+dz],[0,t+2,0],diameter=4.5)
 return out
