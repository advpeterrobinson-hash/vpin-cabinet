"""Local cradle relief and combined WPC integration. CERN-OHL-S-2.0.
Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
"""
from pathlib import Path
import json,math,sys
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from wpc_reference_v32 import reference_axis
from backbox_structure_review_v32 import hits,minimum,face,bounds,box
V=A.Vector;C=json.loads((R/'config/pivot_cradle_integration_v32.json').read_text());WPC=V(*reference_axis())
BASE=json.loads((R/'exports/generated/matrix-cassette-v32/validation.json').read_text())['review'];PF=V(*BASE['pivot_xyz_mm']);SEAT=V(27,PF.y,PF.z+.5);SR=16.5

def load(path):
 d=A.openDocument(str(path));d.recompute();assert not any('Invalid' in o.State for o in d.Objects)
 ss={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()};A.closeDocument(d.Name);return ss

def transform(ss,angle=0,lift=0,axis=PF):
 out={n:s.copy() for n,s in ss.items()}
 for s in out.values():
  if angle:s.rotate(axis,V(1,0,0),angle)
  if lift:s.translate(V(0,0,lift))
 return out

def relief(original,radius):
 """Remove the entire upper rear ear: no sliver above/behind a circular notch."""
 z=WPC.z-radius-C['radial_allowance_mm'];y=PF.y+SR;cr=C['external_corner_radius_mm']
 cut=box(17,PF.y,z,20,80,80)
 square=box(17,y,z-cr,20,cr,cr)
 circle=Part.makeCylinder(cr,20,V(17,y+cr,z-cr),V(1,0,0))
 cut=cut.fuse(square.cut(circle))
 left=original.cut(cut).removeSplitter();M=A.Matrix();M.A11=-1;M.A14=600;right=left.copy();right.transformShape(M,True)
 return {'PF_OpenCradleL':left,'PF_OpenCradleR':right},cut

def keepout(radius,reach=24):
 return {side:Part.makeCylinder(radius,18+reach,V(0 if side=='L' else 600-18-reach,WPC.y,WPC.z),V(1,0,0)) for side in ['L','R']}

def hardware():
 p=C['hardware_reserves'];out={}
 for name,r,reach in [('Axis',p['axis_radius_mm'],24),('Bushing',p['bushing_radius_mm'],p['bushing_internal_reach_mm']),('NutWasher',p['nut_washer_radius_mm'],p['installed_internal_reach_mm'])]:
  out.update({'WPC_'+name+side:s for side,s in keepout(r,reach).items()})
 # Two rigid exterior arm/flange corridors from validated reference packaging.
 from backbox_structure_review_v32 import reserves
 out.update({n:s for n,s in reserves().items() if 'HingeArm' in n or 'HingeFlange' in n})
 return out

def tools_for_pivot():
 p=C['hardware_reserves'];return {'WPC_Tool'+side:Part.makeCylinder(p['tool_radius_mm'],18+p['tool_length_mm'],V(x,WPC.y,WPC.z),V(sign,0,0)) for side,x,sign in [('L',18,1),('R',582,-1)]}

def actual(ss):
 # Include display and VESA envelopes as occupied volumes; omit only installation reserves.
 return {n:s for n,s in ss.items() if n!='PF_BackboxCheckEnvelope' and (n in ['PLAYFIELD_ENVELOPE','PF_VESAEnvelope'] or not any(k in n.upper() for k in ['ENVELOPE','RESERVE','RESERVED','CANDIDATEPAYLOAD']))}

def pf_names(ss):return [n for n in ss if (n.startswith('PF_') and n not in ['PF_OpenCradleL','PF_OpenCradleR','PF_BackboxCheckEnvelope'] and not n.startswith('PF_SupportMountScrew')) or n=='PLAYFIELD_ENVELOPE']

def seat_area(s):return sum(f.Area for f in s.Faces if isinstance(f.Surface,Part.Cylinder) and abs(f.Surface.Radius-SR)<1e-7)
def mesh(n,s):
 vs,fs=s.tessellate(.3);return {'name':n,'label':n,'vertices':[list(p) for p in vs],'faces':[list(f) for f in fs]}
