"""Actual CAD mesh side section and exploded review. CERN-OHL-S-2.0."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/wood-dowel-pivot-v32';b=json.loads((O/'mesh.json').read_text());parts={p['name']:p for p in b['parts']};py,pz=b['review']['pivot_xyz_mm'][1:]
def color(n):return '#8c623c' if 'Dowel' in n else '#7899ad' if 'Strap' in n or 'MountScrew' in n else '#dec498'
def crop(poly,axis,limit):
 out=[]
 for a,z in zip(poly,poly[1:]+poly[:1]):
  ia,iz=a[axis]>=limit,z[axis]>=limit
  if ia:out.append(a)
  if ia!=iz:
   t=(limit-a[axis])/(z[axis]-a[axis]);out.append([a[i]+t*(z[i]-a[i]) for i in range(3)])
 return out
selected={n:p for n,p in parts.items() if n.startswith('PF_') and n not in ('PF_VESAEnvelope','PF_BackboxCheckEnvelope')}
fig=plt.figure(figsize=(14,9));ax=fig.add_axes([.08,.18,.4,.7]);inset=fig.add_axes([.52,.15,.45,.72],projection='3d')
for n in ['FLOOR','PF_OpenCradleL','PF_WoodDowel','PF_CommercialStrap1','PF_StrapScrew1_1','PF_StrapScrew1_3','PF_BasePlywood']:
 p=parts[n];vs=p['vertices'];polys=[[[vs[i][1],vs[i][2]] for i in f] for f in p['faces']]
 ax.add_collection(PolyCollection(polys,facecolor=color(n),edgecolor='none'))
ax.set(xlim=(py-80,py+70),ylim=(20,pz+95),xlabel='Y · mm',ylabel='Z · mm');ax.set_aspect('equal');ax.set_title('SIDE · actual CAD silhouette')
for text,y,z,ty,tz in [('PLYWOOD BASE',py-45,pz+30,py-75,pz+77),('4 STRAPS + 8 SCREWS',py+22,pz+12,py+42,pz+50),('WOOD DOWEL Ø32',py,pz,py+38,pz-40),('OPEN WOOD CRADLE',py,pz-70,py+40,pz-120),('CABINET FLOOR',py,36,py+40,90)]:ax.annotate(text,xy=(y,z),xytext=(ty,tz),fontsize=9,arrowprops={'arrowstyle':'->'})
for n,p in selected.items():
 vs=p['vertices'];polys=[]
 for f in p['faces']:
  poly=crop([vs[i] for i in f],1,py-70)
  if len(poly)>2:polys.append(poly)
 inset.add_collection3d(Poly3DCollection(polys,facecolor=color(n),edgecolor='none'))
inset.set(xlim=(0,600),ylim=(py-70,py+70),zlim=(pz-80,pz+60));inset.set_box_aspect((600,140,140));inset.view_init(elev=-35,azim=115);inset.set_title('UNDERSIDE · rear-end crop · all four straps');inset.set_axis_off()
fig.suptitle('V32 · WOODEN PIVOT · CLOSE SIDE REVIEW',fontsize=16)
fig.text(.04,.06,'CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet\nActual FreeCAD mesh · commercial strap envelopes provisional · no manufacturing approval',fontsize=9)
fig.savefig(O/'01-side-close.png',dpi=160);plt.close(fig)
fig=plt.figure(figsize=(14,10));ax=fig.add_axes([.25,.13,.72,.78],projection='3d')
for n,p in b['states']['EXPLODED'].items():
 if not p:p=parts.get(n) if n in ('PF_OpenCradleL','PF_OpenCradleR') else None
 if not p or n not in selected:continue
 vs=p['vertices'];ax.add_collection3d(Poly3DCollection([[vs[i] for i in f] for f in p['faces']],facecolor=color(n),edgecolor='none'))
# Cradles are unchanged and therefore absent from overrides.
for n in ('PF_OpenCradleL','PF_OpenCradleR'):
 if n not in b['states']['EXPLODED']:
  p=parts[n];vs=p['vertices'];ax.add_collection3d(Poly3DCollection([[vs[i] for i in f] for f in p['faces']],facecolor=color(n),edgecolor='none'))
ax.set(xlim=(0,600),ylim=(0,1100),zlim=(20,750));ax.set_box_aspect((600,1100,730));ax.view_init(elev=25,azim=130);ax.set_axis_off()
fig.suptitle('V32 · EXPLODED · ONLY THE REQUESTED MECHANISM',fontsize=16)
fig.text(.035,.8,'1 PLYWOOD BASE\n\n4 COMMERCIAL STRAPS\n+ 8 STRAP SCREWS\n\n1 WOOD DOWEL\n\n2 OPEN WOOD CRADLES\n+ 6 SUPPORT MOUNTING SCREWS\n\nCustom pivot metal: 0\nBearings: 0\nBushings: 0\nSteel rods: 0',fontsize=12,va='top')
fig.text(.035,.05,'CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet\nActual FreeCAD mesh · TV and VESA excluded from mechanism-only exploded review',fontsize=9)
fig.savefig(O/'02-exploded.png',dpi=160);plt.close(fig)
