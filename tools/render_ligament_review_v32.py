"""Close-up of corrected actual CAD support mesh. CERN-OHL-S-2.0."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/wood-dowel-pivot-v32'
b=json.loads((O/'mesh.json').read_text());p={s['name']:s for s in b['parts']};m=b['review']['support_mounting'];py,pz=b['review']['pivot_xyz_mm'][1:];cz=pz+.5
fig,ax=plt.subplots(figsize=(11,8))
for name,col in [('CROSS_GUIDE_3L','#98a7af'),('PF_OpenCradleL','#dec498'),('PF_WoodDowel','#997046')]:
 s=p[name];vs=s['vertices'];polys=[[(vs[i][1],vs[i][2]) for i in f] for f in s['faces']]
 ax.add_collection(PolyCollection(polys,facecolor=col,edgecolor='none'))
 ax.plot([],[],color=col,lw=8,label=name)
a=m['local_front_y_mm'];e=py-16.5
ax.annotate('',xy=(a,cz),xytext=(e,cz),arrowprops=dict(arrowstyle='<->',color='#ac1818',lw=2))
ax.annotate(f"MINIMUM WOOD LIGAMENT {m['minimum_upper_ligament_mm']:.2f} mm\nPreviously 1.75 mm",xy=((a+e)/2,cz),xytext=(1035,461),fontsize=12,color='#ac1818',arrowprops=dict(arrowstyle='->',color='#ac1818'))
ax.annotate('Fixed crossmember: 0.50 mm clearance',xy=(1010.25,476),xytext=(997,451),fontsize=10,arrowprops=dict(arrowstyle='->'))
ax.annotate('Open U unchanged\nØ32 dowel / Ø33 seat',xy=(1052,501),xytext=(1040,519),fontsize=10,arrowprops=dict(arrowstyle='->'))
ax.set(xlim=(990,1082),ylim=(445,528),xlabel='Y · mm (front → rear)',ylabel='Z · mm');ax.set_aspect('equal');ax.grid(alpha=.2);ax.legend(loc='upper left',fontsize=9)
fig.suptitle('V32 · LOCAL SUPPORT LIGAMENT CORRECTION · LEFT / RIGHT MIRRORED',fontsize=13)
fig.text(.07,.02,'Actual FreeCAD mesh · one CNC plywood solid per side · screws / axis / floor bearing unchanged\nCERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet',fontsize=8)
fig.savefig(O/'03-corrected-ligament-close.png',dpi=160);plt.close(fig)
