"""Schematic routes from saved-solid audit coordinates. CERN-OHL-S-2.0."""
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'exports/generated/side-panel-v32'
report = json.loads((OUT/'motion-validation.json').read_text())
assert all(c['pass'] for c in report['checks']), 'Motion audit failed'
for path, digest in report['source_hashes'].items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest, 'Stale evidence: '+path
bounds = report['scene_bounds_mm']
payload_height = report['config']['candidate_shelf_payload_height_mm']
routes = {r['name']:r for r in report['routes']}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(3,1,figsize=(14,12),sharex=True,sharey=True)
fig.patch.set_facecolor('#f6f8fb')
colors=['#176a9a','#167553','#a35d13']
for i,(ax,color) in enumerate(zip(axes,colors),1):
    name=f'SHELF_{i}'
    route=routes[name+'_staged_with_payload']
    assert route['status']=='CLEAR_FOR_MODELED_TRANSLATION_ONLY'
    b=bounds[name]
    dy=route['legs'][0]['translation_mm'][1]
    dz=route['legs'][1]['translation_mm'][2]
    ax.set_facecolor('white')
    # Side projection of existing occupied geometry; overlap in the picture
    # need not mean 3-D interference. No fabricated shaded structural sections.
    for n in ['CROSS_GUIDE_1L','CROSS_GUIDE_2L','CROSS_GUIDE_3L','BACKBOX_BASE']:
        bb=bounds[n]
        ax.add_patch(Rectangle((bb[2],bb[4]),bb[3]-bb[2],bb[5]-bb[4],facecolor='#dce1e8',edgecolor='#9aa5b1'))
        label='BBBase' if n=='BACKBOX_BASE' else 'T'+n.split('_')[2][0]+' guide'
        ax.text((bb[2]+bb[3])/2,bb[5]+12,label,ha='center',fontsize=9,color='#566473')
    ax.plot([0,1127.125,1308.1],[400.05,596.9,596.9],color='#778798',lw=1,ls=':')
    for j in (1,2,3):
        if j==i:continue
        bb=bounds[f'SHELF_{j}']
        ax.add_patch(Rectangle((bb[2],bb[4]),150,12,facecolor='#bfc8d2',edgecolor='none'))
    y,z=b[2],b[4]
    for yy,zz,alpha,style in [(y,z,1,'-'),(y+dy,z,.65,'--'),(y+dy,z+dz,.9,'-')]:
        ax.add_patch(Rectangle((yy,zz),150,12,facecolor=color,edgecolor=color,alpha=alpha,ls=style))
        ax.add_patch(Rectangle((yy,zz+12),150,payload_height,facecolor=color,edgecolor=color,alpha=.13,ls=style))
    ax.annotate('',xy=(y+dy+75,z+36),xytext=(y+75,z+36),arrowprops={'arrowstyle':'->','color':color,'lw':2})
    ax.annotate('',xy=(y+dy+75,z+dz-8),xytext=(y+dy+75,z+80),arrowprops={'arrowstyle':'->','color':color,'lw':2})
    ax.text(y+75,z-30,f'Y{y:g}',ha='center',color=color)
    ax.text(y+dy+75,z-30,f'Y{y+dy:g}',ha='center',color=color)
    ax.text(y+dy+170,620,'exit above modeled shell',fontsize=9,color=color)
    ax.set_title(f'S{i}: translate {dy:+.0f} mm in Y, then lift {dz:.1f} mm',loc='left',fontweight='bold',color=color)
    ax.set_ylabel('Z (mm)')
    ax.grid(alpha=.12)
    ax.set_ylim(90,740)
    ax.set_xlim(-20,1360)
axes[-1].set_xlabel('Y (mm) — front at left, rear at right')
fig.suptitle('V32 | Shelf removal routes',x=.08,y=.985,ha='left',fontsize=21,fontweight='bold',color='#20354b')
fig.text(.08,.953,'Monitor assembly and T1/T2/T3 removed; guides remain. Other shelves and their candidate payloads retained.',fontsize=10)
fig.text(.08,.927,f'Each moving shelf includes a provisional {payload_height:g} mm equipment envelope above its board. Continuous translation checked.',fontsize=10)
fig.text(.08,.036,'SCHEMATIC SIDE PROJECTION | source-derived bounds, not a fabrication drawing. Hardware, loads, glass and wiring service remain unverified.',fontsize=9,color='#5b6673')
fig.text(.08,.018,'CERN-OHL-S-2.0 | Source: github.com/advpeterrobinson-hash/vpin-cabinet | CNC BLOCKED',fontsize=9,color='#5b6673')
fig.subplots_adjust(left=.08,right=.97,top=.88,bottom=.085,hspace=.32)
fig.savefig(OUT/'04-shelf-service-routes.png',dpi=160,facecolor=fig.get_facecolor())
print('SIDE_MOTION_RENDER_PASS')
