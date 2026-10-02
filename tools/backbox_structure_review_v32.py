"""Candidate V32 backbox structural geometry and collision helpers. CERN-OHL-S-2.0.
Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
Reference axis is design authority; no final hardware drilling is generated.
"""
from pathlib import Path
import json,math
import FreeCAD as A
import Part
from wpc_reference_v32 import reference_axis
R=Path(__file__).resolve().parents[1];V=A.Vector
C=json.loads((R/'config/backbox_structure_review_v32.json').read_text())
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def prism(x,w,points):
 p=[V(x,y,z) for y,z in points];return Part.Face(Part.makePolygon(p+[p[0]])).extrude(V(w,0,0))
def bounds(s):
 b=s.BoundBox;return [b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax]
def face(s,z):return Part.makeCompound([f for f in s.Faces if abs(f.CenterOfMass.z-z)<1e-7 and abs(f.normalAt(0,0).z)>.999])
def passage():
 p=C['service_passage'];return box(p['x_position']-p['width']/2,p['y_position']-p['depth']/2,570,p['width'],p['depth'],60)
def axis():
 r=C['kinematic_reference'];v=V(300,r['rear_y_mm']-r['from_rear_mm'],r['z_mm'])
 assert list(v)==r['axis_xyz_mm']==reference_axis(), 'Incorrect active WPC longitudinal datum'
 return v
def pose(ss,a):
 out={n:s.copy() for n,s in ss.items()}
 for s in out.values():s.rotate(axis(),V(1,0,0),a)
 return out
def physical(ss):return {n:s for n,s in ss.items() if n!='PF_BackboxCheckEnvelope' and not any(k in n.upper() for k in ['ENVELOPE','RESERVE','RESERVED','CANDIDATEPAYLOAD'])}
def hits(ss,tt):
 out=[]
 for n,s in ss.items():
  for m,t in tt.items():
   if s.BoundBox.intersect(t.BoundBox):
    vol=s.common(t).Volume
    if vol>1e-6:out.append({'part':n,'obstacle':m,'volume_mm3':vol})
 return out
def minimum(ss,tt):
 pairs=[]
 for n,s in ss.items():
  for m,t in tt.items():
   b,c=s.BoundBox,t.BoundBox
   lb=math.sqrt(sum(max(0,getattr(b,k+'Min')-getattr(c,k+'Max'),getattr(c,k+'Min')-getattr(b,k+'Max'))**2 for k in 'XYZ'))
   pairs.append((lb,n,m,s,t))
 best=math.inf;pair=None
 for lb,n,m,s,t in sorted(pairs,key=lambda q:q[0]):
  if lb>=best:break
  d=s.distToShape(t)[0]
  if d<best:best=d;pair=[n,m]
 return {'mm':best,'pair':pair}
def build_wood():
 b=C['backbox'];rear=C['kinematic_reference']['rear_y_mm'];w=b['width_mm'];h=b['height_mm'];t=b['stock_mm'];z=b['bottom_z_mm'];zt=z+h;x=(600-w)/2;front=rear-b['side_lower_depth_mm'];cap=b['capture_mm'];k=(b['top_depth_mm']-b['side_lower_depth_mm'])/h
 wood={'BB_SideL':prism(x,t,[(front,z),(rear,z),(rear,zt),(rear-b['top_depth_mm'],zt)]),'BB_SideR':prism(x+w-t,t,[(front,z),(rear,z),(rear,zt),(rear-b['top_depth_mm'],zt)]),
       'BB_Floor':box(x,b['floor_front_y_mm'],z,w,rear-b['floor_front_y_mm'],t),'BB_Top':box(x,front-k*(h-t),zt-t,w,rear-(front-k*(h-t)),t)}
 # Same V14 rear service opening, generated from authoritative parameters.
 old=json.loads((R/'config/structure_geometry_v14.json').read_text())['backbox']['service_door'];dw=old['opening_width_mm'];dh=old['opening_height_mm'];dx=(600-dw)/2;dz=z+old['lower_clearance_above_floor_mm']
 wood.update({'BB_RearL':box(x,rear-t,z,dx-x,t,h),'BB_RearR':box(dx+dw,rear-t,z,x+w-dx-dw,t,h),'BB_RearBottom':box(dx,rear-t,z,dw,t,dz-z),'BB_RearTop':box(dx,rear-t,dz+dh,dw,t,zt-dz-dh)})
 def cut(n,s):wood[n]=wood[n].cut(s).removeSplitter()
 for n in ['BB_Floor','BB_Top']:
  q=wood[n].BoundBox
  cut(n,box(q.XMin-1,q.YMin-1,q.ZMin-1,t-cap+1,q.YLength+2,q.ZLength+2))
  cut(n,box(q.XMax-(t-cap),q.YMin-1,q.ZMin-1,t-cap+1,q.YLength+2,q.ZLength+2))
  for side in ['BB_SideL','BB_SideR']:cut(side,wood[n])
 for n in ['BB_RearL','BB_RearR','BB_RearBottom','BB_RearTop']:
  for m in ['BB_Floor','BB_Top','BB_SideL','BB_SideR']:
   ov=wood[n].common(wood[m])
   if ov.Volume<1e-6:continue
   q=ov.BoundBox;limit=q.YMax-cap
   cut(n,box(q.XMin-1,q.YMin-1,q.ZMin-1,q.XLength+2,max(.001,limit-q.YMin+1),q.ZLength+2));cut(m,wood[n])
 # Retain only existing backbox rear-frame owner cutouts; floor passage is generic.
 from owner_features_v27 import features
 from build_owner_services_v27 import cut_shape
 mapping={'BackboxRearFrameLeftV14':'BB_RearL','BackboxRearFrameRightV14':'BB_RearR','BackboxRearFrameBottomV14':'BB_RearBottom','BackboxRearFrameTopV14':'BB_RearTop'}
 for f in features():
  if f['part'] in mapping:cut(mapping[f['part']],cut_shape(f))
 cut('BB_Floor',passage())
 return wood

def update_fixed(ss):
 out={n:s.copy() for n,s in ss.items() if n!='PF_BackboxCheckEnvelope'}
 if 'BACKBOX_BASE' in out:out['BACKBOX_BASE']=out['BACKBOX_BASE'].cut(passage()).removeSplitter()
 # Retire the obsolete drilled reference, without cutting a new hardware hole.
 for n,x in [('SIDE_L',0),('SIDE_R',582)]:
  if n not in out:continue
  plug=Part.makeCylinder(6.35,18,V(x,1270,508),V(1,0,0)) # HISTORICAL repair location, never a motion datum.
  out[n]=out[n].fuse(plug).removeSplitter()
 return out

def reserves():
 p=C['hinge_reserve'];res={};a=axis();b=C['backbox'];z=b['bottom_z_mm']
 for side,x,sign in [('L',-90+p['floor_row_inset_outer_mm'],-1),('R',690-p['floor_row_inset_outer_mm'],1)]:
  # Separate arm, flange and top access; a Y-only blanket exclusion is invalid.
  xx=-8 if sign<0 else 600
  res['BB_HingeArmReserve'+side]=prism(xx,8,[(a.y-22,a.z-22),(a.y+22,a.z-22),(1295,z),(1156,z)])
  res['BB_HingeFlangeReserve'+side]=box(-60 if sign<0 else 600,1156,z-6,60,139,6)
  for i,y in enumerate(p['floor_reference_centers_y_mm']):res['BB_HingeAccessReserve'+side+str(i+1)]=Part.makeCylinder(p['floor_access_radius_mm'],p['floor_access_top_z_mm']-z,V(x,y,z))
  res['BB_PivotAccessReserve'+side]=Part.makeCylinder(p['pivot_access_radius_mm'],p['pivot_internal_reach_mm'],V(0 if sign<0 else 600-p['pivot_internal_reach_mm'],a.y,a.z),V(1,0,0))
 for i,(x,y) in enumerate(C['locks']['centers_xy_mm'],1):
  res['BB_LockWoodReserve'+str(i)]=Part.makeCylinder(C['locks']['wood_reserve_radius_mm'],36,V(x,y,z-18))
  res['BB_LockToolReserve'+str(i)]=Part.makeCylinder(C['locks']['tool_radius_mm'],C['locks']['tool_height_mm'],V(x,y,z+18))
 return res
