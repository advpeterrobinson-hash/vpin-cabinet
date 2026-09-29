"""Isolated owner-layout visualization; never modifies V32 CAD. CERN-OHL-S-2.0."""
from pathlib import Path
import json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exports/generated/lighting-study-v32';OUT.mkdir(parents=True,exist_ok=True)
G=json.loads((ROOT/'exports/generated/cabinet-v32/geometry.json').read_text())
A=math.atan2(596.9-400.05,1127.125);B=A+math.radians(15)
# Owner direction: parallel screen/glass. LED angle and offsets are proposals.
Z0=400.05+45*math.tan(A)-12-55*math.cos(A)
def screen(x,y):return np.array([x,45+y*math.cos(A)-55*math.sin(A),Z0+y*math.sin(A)+55*math.cos(A)])
def glass(x,y):return np.array([x,y,400.05+y*math.tan(A)+5])
P=79.375;LED_Y=1015;LED_Z=glass(300,LED_Y)[2]-P*math.sin(B)-12
# Top edge stays below the proposed glass; front edge tips down toward player.
def led(x,y):return np.array([x,LED_Y+y*math.cos(B),LED_Z+y*math.sin(B)])
def quad(fn,x,y,w,h):return np.array([fn(x,y),fn(x+w,y),fn(x+w,y+h),fn(x,y+h)])
def poly(ax,v,c,alpha=1,edge=None,lw=.5):
 ax.add_collection3d(Poly3DCollection([v],facecolor=c,edgecolor=edge or c,linewidth=lw,alpha=alpha,zorder=10))
def plane_rect(ax,fn,x,y,w,h,c):poly(ax,quad(fn,x,y,w,h),c)
BG='#f2f0ea';INK='#253440'
fig=plt.figure(figsize=(17,11),facecolor=BG)
ax=fig.add_axes([.01,.12,.61,.78],projection='3d',computed_zorder=False);ax.set_facecolor(BG)
for p in G['parts']:
 if p['id'] not in ['SIDE_L','SIDE_R','FRONT','REAR','BACKBOX_BASE']:continue
 v=np.array(p['vertices']);c='#c5aa81' if p['id']!='BACKBOX_BASE' else '#a98b63'
 ax.add_collection3d(Poly3DCollection([v[f] for f in p['faces']],facecolor=c,edgecolor='none'))
# Screen panel and an original abstract pinball graphic (no game assets).
plane_rect(ax,screen,20,0,560,970,'#111b27')
plane_rect(ax,screen,30,10,540,950,'#12313e')
for x in [48,548]:plane_rect(ax,screen,x,35,4,890,'#299aab')
for x,y,rad in [(165,650,39),(305,720,39),(435,620,39),(300,440,25)]:
 t=np.linspace(0,2*np.pi,60);v=np.array([screen(x+rad*np.cos(q),y+rad*np.sin(q)) for q in t]);poly(ax,v,'#efb453')
for x,sgn in [(235,1),(365,-1)]:
 poly(ax,np.array([screen(x,115),screen(x+sgn*65,145),screen(x+sgn*60,159),screen(x-6*sgn,132)]),'#f6e8ca')
for x in [110,480]:
 v=np.array([screen(x+30*math.sin(q),250+q*75) for q in np.linspace(0,5,60)])
 ax.plot(v[:,0],v[:,1],v[:,2]+.5,color='#ea805d',lw=3,zorder=15)
# Matrix dark carrier with 6 visible modules. No added gaps in nominal panel footprint.
plane_rect(ax,led,18,0,564,P,'#18232b')
start=(600-6*P)/2
for k in range(6):
 plane_rect(ax,led,start+k*P,0,P,P,'#0d1720')
 dots=[];cols=[]
 for iy in range(16):
  for ix in range(16):
   dots.append(led(start+k*P+(ix+.5)*P/16,(iy+.5)*P/16))
   cols.append(plt.cm.turbo((k*16+ix+iy*1.5)/120))
 v=np.array(dots);ax.scatter(v[:,0],v[:,1],v[:,2]+.8,c=cols,s=2.7,depthshade=False,zorder=20)
# Glass outline only, so the playfield and matrix remain readable.
v=quad(glass,18,45,564,1080)
for i in range(4):
 a,b=v[i],v[(i+1)%4];ax.plot([a[0],b[0]],[a[1],b[1]],[a[2],b[2]],color='#60b5c3',lw=1.3,alpha=.7)
# Custom full-width lockdown bar; wrap front lip, visual shape only.
plane_rect(ax,glass,-3,-4,606,49,'#bac3c9')
v=np.array([glass(-3,-4),glass(603,-4),glass(603,-4)-[0,0,23],glass(-3,-4)-[0,0,23]])
poly(ax,v,'#8b969f')
ax.set(xlim=(-30,630),ylim=(-30,1320),zlim=(0,670));ax.set_box_aspect((660,1350,670));ax.view_init(elev=49,azim=-64);ax.set_proj_type('ortho');ax.set_axis_off()
fig.text(.045,.92,'V32 / PLAYFIELD + LED MATRIX',fontsize=24,weight='bold',color=INK)
fig.text(.045,.885,'Owner layout direction · dimensional visual study',fontsize=12,color='#697680')
fig.text(.10,.16,'CUSTOM LOCKDOWN BAR',fontsize=12,weight='bold',color=INK)
fig.text(.10,.135,'Front / player end · width follows the 600 mm body',fontsize=10,color='#697680')
# Side profile, exactly matching the rendered coordinate transforms.
s=fig.add_axes([.64,.57,.33,.26]);s.set_facecolor(BG)
y=np.array([0,1127.125]);s.plot(y,400.05+y*math.tan(A)+5,color='#60b5c3',lw=2,label='Glass')
a,b=screen(300,0),screen(300,970);s.plot([a[1],b[1]],[a[2],b[2]],lw=5,color='#12313e',label='Playfield')
a,b=led(300,0),led(300,P);s.plot([a[1],b[1]],[a[2],b[2]],lw=5,color='#e79b3b',label='LED matrix')
s.set(xlim=(-20,1160),ylim=(355,655),xlabel='Front → rear (mm)',ylabel='Height (mm)');s.set_aspect('equal');s.spines[['top','right']].set_visible(False);s.tick_params(labelsize=8);s.legend(loc='upper left',frameon=False,fontsize=9)
s.set_title('PARALLEL PLAYFIELD & GLASS',fontsize=12,weight='bold',loc='left',pad=16)
fig.text(.65,.53,f'Glass / playfield: {math.degrees(A):.2f}°\nLED panel: {math.degrees(B):.2f}° — proposed +15° tilt',fontsize=11,color=INK,linespacing=1.7)
# Face-on six-panel strip to make the actual dimensions readable.
s=fig.add_axes([.65,.32,.31,.13]);s.set_facecolor(BG)
for k in range(6):
 s.add_patch(Rectangle((k*P,0),P,P,facecolor='#142c38',edgecolor=BG,lw=1))
 for iy in range(16):
  x=k*P+(np.arange(16)+.5)*P/16
  s.scatter(x,np.full(16,(iy+.5)*P/16),s=1.9,c=plt.cm.turbo((k*16+np.arange(16)+iy*1.5)/120))
s.set(xlim=(0,6*P),ylim=(0,P));s.set_aspect('equal');s.axis('off')
fig.text(.65,.45,'SIX CLEVELAND PANELS / DONNY CONTROL',fontsize=11,weight='bold',color=INK)
fig.text(.65,.285,'476.25 × 79.375 mm nominal panel sum\n6 × 16 × 16 = 1,536 pixels',fontsize=11,color=INK,linespacing=1.8)
fig.text(.65,.18,'LED angle, carrier, bezels and spacing remain open.\nGlass shown as an outline; backbox omitted for clarity.\nScreen artwork is illustrative, not a selected game.',fontsize=9,color='#697680',linespacing=1.7)
fig.text(.045,.055,'VISUAL PROPOSAL · Existing V32 CAD unchanged · Not a manufacturing drawing',fontsize=10,color='#697680')
fig.savefig(OUT/'01-layout.png',dpi=170,facecolor=BG);plt.close(fig)
# Basic numerical evidence for this view, not a mechanical qualification.
assert np.allclose((screen(300,970)-screen(300,0))[2]/(screen(300,970)-screen(300,0))[1],math.tan(A))
assert 0<start and start+6*P<600
assert led(300,P)[1]<1127.125
assert min(glass(300,led(300,q)[1])[2]-led(300,q)[2] for q in [0,P])>0
report=dict(status='VISUAL_PROPOSAL',glass_playfield_angle_deg=math.degrees(A),led_angle_deg=math.degrees(B),led_additional_tilt_deg=15,panel_array_nominal_mm=[6*P,P],assumptions=['single row of six panels','15 degree extra tilt','visual lockdown shape only','glass outline is not measured hardware'],checks={'parallel_planes':True,'array_within_body_width':True,'array_before_rear_flat':True,'led_face_below_glass_plane':True},manufacturing_ready=False)
(OUT/'layout.json').write_text(json.dumps(report,indent=2)+'\n')
print('LIGHTING_STUDY_RENDER_PASS',OUT/'01-layout.png')
