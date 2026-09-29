"""Render saved CAD component meshes, never invented source-hardware drawings."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/front-panel-v32'
M=json.loads((O/'coin-door-meshes.json').read_text());C=json.loads((R/'config/front_panel_v32.json').read_text());c=C['coin_door']
BG='#f2efe8';INK='#253640';colors={'frame':'#667680','leaf':'#303e49','return':'#efb750','light':'#e3b450','lock':'#a9b7c1','mechanism':'#bb7953','tray':'#388e84','support':'#7d969f','mount':'#849299'}
def polygons(ax,parts,axes):
 for p in parts:
  v=np.array(p['vertices'])
  for f in p['faces']:ax.add_patch(Polygon(v[f][:,axes],facecolor=colors[p['kind']],edgecolor='none',alpha=.9))
def save(fig,name):
 fig.text(.035,.025,'V32 / PROPOSAL · Dimensions are candidate space reservations, not verified hardware · CNC BLOCKED',fontsize=9,color='#657680')
 fig.savefig(O/name,dpi=160,facecolor=BG);plt.close(fig)
fig=plt.figure(figsize=(16,9),facecolor=BG);fig.text(.04,.94,'OUTWARD COIN DOOR / TWO CONFIGURATIONS',fontsize=22,weight='bold',color=INK)
fig.text(.04,.895,'Basic illuminated door now · removable mechanisms and compact tray as an optional upgrade',fontsize=12,color='#687781')
a=fig.add_axes([.05,.22,.40,.60]);a.set_facecolor(BG)
a.add_patch(Rectangle((0,0),600,400.05,facecolor='#bfa176',edgecolor=INK))
polygons(a,M['coin-basic-closed'],[0,2])
for b,color in zip(C['buttons'],['#e3b450','#db873e','#bd5549','#bd5549']):
 a.add_patch(Circle((b['x'],b['z']),b['face_diameter']/2+2,facecolor=INK));a.add_patch(Circle((b['x'],b['z']),b['face_diameter']/2,facecolor=color))
a.add_patch(Rectangle((490,250),60,60,facecolor='#abb8c0',edgecolor=INK));a.add_patch(Circle((520,280),12,facecolor=INK));a.add_patch(Rectangle((-3,394),606,22,facecolor='#bdc7ce',edgecolor='#748590'))
a.text(290,250,'BASIC',color='white',ha='center',fontsize=14,weight='bold');a.text(290,225,'Illuminated coin-return buttons',color='white',ha='center',fontsize=9);a.text(290,205,'Press for credit',color='#edc36a',ha='center',fontsize=10)
a.set(xlim=(-10,610),ylim=(-15,430));a.set_aspect('equal');a.axis('off')
fig.text(.05,.15,'No acceptors or cashbox required in the default build.\nSame front aperture retained for both configurations.',fontsize=11,color=INK,linespacing=1.7)
a=fig.add_axes([.50,.17,.47,.68],projection='3d');a.set_facecolor(BG)
for p in M['coin-upgrade-open']:
 v=np.array(p['vertices']);a.add_collection3d(Poly3DCollection([v[f] for f in p['faces']],facecolor=colors[p['kind']],edgecolor='#465762',linewidth=.3,alpha=.95))
a.set(xlim=(20,500),ylim=(-340,145),zlim=(60,380));a.set_box_aspect((480,485,320));a.view_init(elev=28,azim=-52);a.set_proj_type('ortho');a.set_axis_off();a.set_title('UPGRADE / OPEN 110°',fontsize=13,weight='bold',color=INK)
fig.text(.53,.12,'Orange: door-mounted mechanism reservations\nGreen: stationary removable collection tray\nGray: local tray supports; no shell holes released',fontsize=10,color=INK,linespacing=1.7)
save(fig,'02-coin-door-configurations.png')
# True plan and side projections; state overlays intentionally differentiated.
fig,axs=plt.subplots(1,2,figsize=(16,8),facecolor=BG);fig.subplots_adjust(left=.06,right=.97,bottom=.16,top=.80,wspace=.25)
fig.suptitle('DOOR MOTION ≠ INTERNAL HARDWARE DEPTH',fontsize=22,weight='bold',color=INK,y=.95)
for a in axs:a.set_facecolor(BG);a.spines[['top','right']].set_visible(False)
a=axs[0];a.add_patch(Rectangle((18,0),564,18,facecolor='#bfa176',alpha=.4));polygons(a,M['coin-upgrade-open'],[0,1])
leaf=next(p for p in M['coin-basic-closed'] if p['kind']=='leaf');v=np.array(leaf['vertices']);a.plot([v[:,0].min(),v[:,0].max()],[-4,-4],ls='--',color='#4b606e',label='Closed leaf')
hx,hy,_=c['hinge_axis_mm'];t=np.radians(np.linspace(0,-110,111));a.plot(hx+308*np.cos(t),hy+308*np.sin(t),ls=':',color='#c2774b',label='Outer-corner arc')
a.text(340,115,'Inside cabinet (+Y)',fontsize=10,ha='center');a.text(320,-280,'Player / outside (−Y)',fontsize=10,ha='center')
a.annotate('',xy=(365,-160),xytext=(365,25),arrowprops={'arrowstyle':'->','color':'#25877e'})
a.text(470,45,'Tray removal\nthrough opening',color='#216b63',ha='center',fontsize=9)
a.set(xlim=(0,600),ylim=(-340,160),xlabel='X (mm)',ylabel='Y (mm)',title='Plan / left hinge / outward rotation');a.set_aspect('equal');a.legend(loc='lower left',fontsize=8,frameon=False)
a=axs[1];parts=[p for p in M['coin-upgrade-closed'] if p['kind']!='frame'];polygons(a,parts,[1,2]);a.add_patch(Rectangle((0,0),18,400.05,facecolor='#bfa176',alpha=.25))
a.add_patch(Rectangle((120,160),150,12,facecolor='#368e86'));a.text(200,182,'S1 unchanged',fontsize=10,color='#287b73',ha='center')
a.annotate('',xy=(103,152),xytext=(120,152),arrowprops={'arrowstyle':'<->','color':INK});a.text(135,140,'17 mm candidate gap\nto S1 leading plane',fontsize=9,color=INK)
a.text(48,235,'Mechanism\nreservation',fontsize=9,ha='center',color='white');a.text(160,325,'Light/switch bodies\nmodeled separately',fontsize=10,color=INK)
a.set(xlim=(-40,300),ylim=(40,405),xlabel='Y (mm)',ylabel='Z (mm)',title='Side / closed upgrade');a.set_aspect('equal')
fig.text(.06,.075,'Sweeps sampled at 1°; tray withdrawal at 5 mm. Actual hinge, mechanisms, wiring, legs and receiver remain UNVERIFIED.',fontsize=10,color=INK)
save(fig,'03-coin-door-clearances.png')
print('COIN_DOOR_RENDERS_PASS 2 views from saved component meshes')
