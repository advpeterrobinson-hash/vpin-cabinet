"""Preliminary layered packing; physical protection qualification remains open."""
import json
from pathlib import Path
O=Path(__file__).resolve().parents[1]/'exports/generated/widebody-v35'
r={a['instance_id']:a for a in json.loads((O/'manufacturing-register.json').read_text())['parts']};p=json.loads((O/'packaging.json').read_text())
for b in p['bundles']:
 b['W']=max(b['W'],400);layers=[]
 for a in sorted(b['parts'],key=lambda a:-(r[a['id']]['finished_xy_bounds_mm'][2]-r[a['id']]['finished_xy_bounds_mm'][0])*(r[a['id']]['finished_xy_bounds_mm'][3]-r[a['id']]['finished_xy_bounds_mm'][1])):
  q=r[a['id']]['finished_xy_bounds_mm'];w,h=q[2]-q[0],q[3]-q[1];rot=w<h;w,h=max(w,h),min(w,h);placed=False
  for layer in layers:
   for row in layer['rows']:
    if h<=row['h'] and row['x']+w<=b['L']+.00001:x,y=row['x'],row['y'];row['x']+=w+15;placed=True;break
   if not placed:
    yy=sum(v['h']+15 for v in layer['rows'])
    if yy+h<=b['W']+.00001:x,y=0,yy;layer['rows'].append({'x':w+15,'y':yy,'h':h});placed=True
   if placed:break
  if not placed:layer={'rows':[{'x':w+15,'y':0,'h':h}],'parts':[],'height':0};layers.append(layer);x,y=0,0
  a.update(packing_x_mm=x,packing_y_mm=y,rotated=rot,packing_L_mm=w,packing_W_mm=h);layer['parts'].append(a);layer['height']=max(layer['height'],a['thickness_envelope_mm'])
 z=0
 for i,l in enumerate(layers):
  for a in l['parts']:a.update(stack_z_mm=z,layer=i+1)
  z+=l['height']+3
 b['H']=z;b['external_mm']=[b['L']+40,b['W']+40,z+40];b['estimated_CG_mm']=[20+sum((a['packing_x_mm']+a['packing_L_mm']/2)*a['mass_nominal_kg'] for a in b['parts'])/b['nominal_wood_kg'],20+sum((a['packing_y_mm']+a['packing_W_mm']/2)*a['mass_nominal_kg'] for a in b['parts'])/b['nominal_wood_kg'],20+sum((a['stack_z_mm']+a['thickness_envelope_mm']/2)*a['mass_nominal_kg'] for a in b['parts'])/b['nominal_wood_kg']];b['CG_basis']='B-rep mass with per-piece bounding-center proxy; packaging engineering estimate';b['separator']='3mm continuous separator above each occupied layer; local padding/edge guards in1kg allowance, unqualified';b['layer_count']=len(layers)
(O/'packaging.json').write_text(json.dumps(p,indent=2)+'\n')
