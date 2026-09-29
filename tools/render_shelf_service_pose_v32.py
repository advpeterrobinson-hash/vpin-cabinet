"""Side-view projection of saved kinematic-screen vertices. CERN-OHL-S-2.0."""
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

R = Path(__file__).resolve().parents[1]
O = R / 'exports/generated/side-panel-v32'
r = json.loads((O / 'shelf-service-pose-screen.json').read_text())
s = json.loads((O / 'simple-shelves-validation.json').read_text())
for name, digest in r['source_hashes'].items():
    assert hashlib.sha256((R / name).read_bytes()).hexdigest() == digest, name

def hull(points):
    points = sorted(set(tuple(p) for p in points))
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    halves = []
    for ordered in (points, list(reversed(points))):
        half = []
        for p in ordered:
            while len(half) >= 2 and cross(half[-2], half[-1], p) <= 0:
                half.pop()
            half.append(p)
        halves.extend(half[:-1])
    return halves

fig, axes = plt.subplots(1, 2, figsize=(12, 8), sharex=True, sharey=True)
for ax, angle in zip(axes, (80, 100)):
    pose = next(p for p in r['poses'] if p['opening_deg'] == angle)
    ax.plot([0,1308.1,1308.1,1127.125,0,0], [0,0,596.9,596.9,400.05,0], color='#8693a0', lw=1)
    for name, vertices in pose['projected_profiles_yz'].items():
        ax.add_patch(Polygon(hull(vertices), facecolor='#4c91bf' if name == 'PLAYFIELD_ENVELOPE' else '#324b63', alpha=.55))
    blocked = {x['moving'] for x in pose['tool_column_conflicts']}
    for i, spec in enumerate(s['config']['shelves'], 1):
        z = {1:160,2:180,3:240}[i]
        ax.add_patch(Rectangle((spec['y_mm'],z),150,12,facecolor='#bd8a53'))
        ax.text(spec['y_mm']+75,z-24,f'S{i}',ha='center',fontsize=10)
        for a in s['axes']:
            if a['shelf'] == f'SHELF_{i}' and 'L' in a['bolt']:
                y = a['xyz_mm'][1]
                ax.plot([y,y],[a['head_top_z_mm'],1600],':',lw=1,color='#c54b4b' if a['bolt'] in blocked else '#228665')
    ax.scatter([r['pivot_xyz_mm'][1]], [r['pivot_xyz_mm'][2]],color='black',s=25,zorder=10)
    ax.set_title(f'Abertura relativa: {angle}°\n'+('Acesso vertical ainda obstruído' if blocked else 'Acesso e retirada livres no cenário testado'),fontsize=11)
    ax.set_aspect('equal'); ax.set_xlim(-20,1360); ax.set_ylim(-40,1630)
    ax.set_xlabel('Y — frente → traseira (mm)'); ax.grid(alpha=.15)
axes[0].set_ylabel('Z (mm)')
fig.suptitle('Prateleiras simples — acesso com o display levantado',fontsize=16)
fig.text(.06,.055,'S3 avança para Y820. Eixo proposto: não é uma dobradiça selecionada. Perfil cinza: referência da lateral.',fontsize=10)
fig.text(.06,.032,'Escoras, ferragens, cabos e backbox superior não representados. Sem aprovação estrutural ou para CNC.',fontsize=10)
fig.text(.06,.011,'CERN-OHL-S-2.0 · github.com/advpeterrobinson-hash/vpin-cabinet',fontsize=8)
fig.tight_layout(rect=(0,.15,1,.95))
fig.savefig(O/'08-shelf-raised-display.png',dpi=150)
print('SHELF_POSE_RENDER_PASS')
