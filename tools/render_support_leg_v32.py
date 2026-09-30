"""Render the saved planning mesh and verified height datums. CERN-OHL-S-2.0."""
import hashlib,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/support-leg-v32'
r=json.loads((O/'validation.json').read_text());assert all(c['pass'] for c in r['checks'])
for p,h in r['source_hashes'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
c=r['config'];mesh=json.loads((O/'detail-mesh.json').read_text())
fig=plt.figure(figsize=(13,8));ax=fig.add_subplot(121)
ys=[120,565,865]
for i,(y,z) in enumerate(zip(ys,c['shelf_underside_z_mm']),1):
 ax.add_patch(Rectangle((y,z),150,12,fc='#c9a06f',ec='#77542e'))
 ax.add_patch(Rectangle((y,z-18),150,18,fc='#e2c49c'))
 ax.text(y+75,z+30,f'S{i}: topo {z+12} mm',ha='center',fontsize=11)
ax.axhspan(18,36,color='#bbc5cd');ax.text(25,44,'Piso: face superior Z36',fontsize=10)
ax.axhline(0,color='#425567');ax.set_xlim(0,1120);ax.set_ylim(-10,330)
ax.set_xlabel('Y (mm)');ax.set_ylabel('Z a partir da base do gabinete (mm)');ax.grid(alpha=.15)
ax.set_title('Alturas mantidas e fixadas\nEspaçamento aprovado preservado',fontsize=12)
bx=fig.add_subplot(122,projection='3d')
for item in mesh:
 if not item['name'].startswith('CandidateLeg'):continue
 verts=np.array(item['vertices']);faces=verts[np.array(item['faces'])]
 color='#c9a06f' if 'Block' in item['name'] else '#7895ac'
 normals=np.cross(faces[:,1]-faces[:,0],faces[:,2]-faces[:,0]);norms=np.linalg.norm(normals,axis=1);normals/=np.maximum(norms[:,None],1e-12)
 from matplotlib.colors import to_rgb
 lighting=.55+.45*np.abs(normals @ np.array([.4,.5,.768]));colors=np.array(to_rgb(color))[None,:]*lighting[:,None]
 bx.add_collection3d(Poly3DCollection(faces,facecolors=colors,linewidth=0))
for z in (96,154):bx.plot([-8,90],[-8,90],[z,z],color='#b94737',ls='--',lw=1)
for z in range(72,180,18):bx.plot([18,72],[18,18],[z,z],color='#84623e',lw=.5)
bx.set_xlim(-10,100);bx.set_ylim(-10,100);bx.set_zlim(40,195);bx.set_box_aspect((110,110,155));bx.view_init(25,45)
bx.set_xlabel('X (mm)');bx.set_ylabel('Y (mm)');bx.set_zlabel('Z (mm)')
bx.set_title('Canto dianteiro: proposta de reforço\nMadeira + reserva de apoio metálico; eixos a 45°',fontsize=12)
fig.suptitle('Alturas das prateleiras e preparação das fixações',fontsize=18)
fig.text(.06,.12,'Pernas: estudo com entre-eixos de 58 mm. O STL recebido mede aproximadamente 57 mm.',fontsize=11)
fig.text(.06,.085,'Furos, chapa, laminação e ferragens ainda sujeitos a conferência e ensaio. Não é arquivo liberado para fabricação.',fontsize=10)
fig.text(.06,.045,'CERN-OHL-S-2.0 · github.com/advpeterrobinson-hash/vpin-cabinet',fontsize=9)
fig.tight_layout(rect=(.02,.17,.98,.94));fig.savefig(O/'01-heights-and-leg-corner.png',dpi=150)
print('SUPPORT_LEG_RENDER_PASS')
