"""Front controls review, source geometry and assumed hardware kept distinct."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
R=Path(__file__).resolve().parents[1];C=json.loads((R/'config/front_panel_v32.json').read_text());O=R/'exports/generated/front-panel-v32';G=json.loads((R/'exports/generated/cabinet-v32/geometry.json').read_text());BG='#f1eee6';INK='#283740'
fig=plt.figure(figsize=(16,10),facecolor=BG);a=fig.add_axes([.045,.22,.57,.66]);a.set_facecolor(BG)
a.add_patch(Rectangle((0,0),600,400.05,facecolor='#b89669',edgecolor=INK,lw=1.5))
a.add_patch(Rectangle((18,0),564,400.05,fill=False,edgecolor='#e6d7bf',ls='--'))
# Receiver remains a reserve, represented separately from custom outer bar.
a.add_patch(Rectangle((18,380),564,20.05,facecolor='#dfac62',alpha=.5,hatch='///'))
a.add_patch(FancyBboxPatch((-3,394),606,23,boxstyle='round,pad=0,rounding_size=5',facecolor='#bdc7ce',edgecolor='#73818b'))
x,z,w,h=C['coin_opening'];m=C['coin_door']['frame_margin_mm']
a.add_patch(FancyBboxPatch((x-m,z-m),w+2*m,h+2*m,boxstyle='round,pad=0,rounding_size=12',facecolor='#30393e',edgecolor='#101c23',lw=2))
a.add_patch(Rectangle((x,z),w,h,fill=False,edgecolor='#bdc7ce',ls='--',lw=.8))
for xx in [315,368]:
 a.add_patch(Rectangle((xx,292),36,45,facecolor='#a76231',edgecolor='#e4b067'))
 a.add_patch(Rectangle((xx+11,300),14,27,facecolor='#edc778'))
a.add_patch(Circle((428,198),9,facecolor='#bdc7ce',edgecolor='#737e85'))
a.text(300,210,'COIN DOOR',ha='center',color='white',weight='bold',fontsize=14)
a.text(300,184,'Existing reference opening',ha='center',color='#d4dce0',fontsize=9)
a.text(300,166,'311.15 × 264.32 mm',ha='center',color='#d4dce0',fontsize=10)
a.text(300,120,'Actual door + flange to be confirmed',ha='center',color='#d4dce0',fontsize=8)
for b,col in zip(C['buttons'],['#edc447','#eb8c38','#c94f49','#d74e4e']):
 xx,zz=b['x'],b['z'];rad=b['face_diameter']/2
 a.add_patch(Circle((xx,zz),rad+3,facecolor='#303a42'));a.add_patch(Circle((xx,zz),rad,facecolor=col,edgecolor='#f5d6b5'))
 a.text(xx,zz,{'Start':'START','Extra Ball':'EXTRA','Exit / Back':'EXIT','Launch Ball':'LAUNCH'}[b['name']],ha='center',va='center',fontsize=6.5,weight='bold',color='#202a30')
 if xx==90:a.text(29,zz,f'Z{zz}',va='center',fontsize=8,color=INK)
 else:a.text(xx,zz-40,f'Z{zz}',ha='center',fontsize=8,color=INK)
xx,zz=C['plunger_center_xz'];a.add_patch(Rectangle((xx-30,zz-30),60,60,facecolor='#adb7bc',edgecolor='#4d5e6a'))
a.add_patch(Circle((xx,zz),13,facecolor='#202d36'));a.text(xx,zz+41,'PLUNGER',ha='center',fontsize=9,weight='bold',color=INK);a.text(xx+34,zz,f'Z{zz}',ha='left',va='center',fontsize=8,color=INK)
a.annotate('',xy=(0,-27),xytext=(600,-27),arrowprops={'arrowstyle':'<->','color':INK});a.text(300,-46,'600 mm cabinet outside width',ha='center',fontsize=11,color=INK)
a.set(xlim=(-20,620),ylim=(-65,435));a.set_aspect('equal');a.axis('off')
fig.text(.05,.94,'V32 / FRONT PANEL REVIEW',fontsize=24,weight='bold',color=INK)
fig.text(.05,.90,'Photo-inspired controls · custom lockdown · dimensions measured from cabinet bottom',fontsize=11,color='#65747b')
# Side view using source bounds for shelf, screen and monitor rail.
s=fig.add_axes([.68,.44,.28,.38]);s.set_facecolor(BG)
s.add_patch(Rectangle((0,0),18,400.05,facecolor='#b89669',edgecolor=INK))
s.add_patch(Rectangle((8,170),95,135,facecolor='#bb7953',alpha=.4,edgecolor='#b3523a',ls='--'))
for name,col in [('SHELF_1','#287f7b'),('PLAYFIELD_ENVELOPE','#567e9c'),('MONITOR_RAIL_R','#73816a')]:
 p=next(p for p in G['parts'] if p['id']==name);v=p['vertices'];faces=p['faces']
 # silhouette from convex hull-free projected tessellation triangles
 from matplotlib.patches import Polygon
 for f in faces:
  yz=[(v[i][1],v[i][2]) for i in f];s.add_patch(Polygon(yz,facecolor=col,edgecolor='none',alpha=.2))
s.plot([120,120],[70,235],color='#287f7b',ls='--');s.annotate('',xy=(18,62),xytext=(120,62),arrowprops={'arrowstyle':'<->'});s.text(69,41,'102 mm',ha='center',fontsize=9)
s.text(190,192,'S1',color='#287f7b',weight='bold');s.text(25,345,'Optional mechanism only\nCandidate 95 mm depth',fontsize=8,color='#a84635')
s.set(xlim=(-15,300),ylim=(0,430),xlabel='Y: front → rear (mm)',ylabel='Z (mm)');s.spines[['top','right']].set_visible(False);s.set_title('CHECK BEHIND THE PANEL',fontsize=12,weight='bold',loc='left')
fig.text(.68,.31,'Plunger: Z300 rejected (monitor rail clash).\nZ280 clears the tested provisional envelope.\nOutward door + localized mechanisms tested.\nOld full-depth prism retired; hardware unverified.',fontsize=10,color=INK,linespacing=1.65)
fig.text(.05,.135,'PROPOSED CENTERS',fontsize=10,weight='bold',color=INK)
fig.text(.05,.105,'Left: X90 / Z310, 260, 210     Right: X520 / plunger Z280, launch Z210',fontsize=11,color=INK)
fig.text(.05,.055,'Nominal button bores only · Door face and hardware envelopes illustrative · Leg/receiver hardware not qualified\nPROPOSAL — not a frozen CNC panel. Existing V32 CAD remains unchanged.',fontsize=10,color='#6b747a',linespacing=1.6)
fig.savefig(O/'01-front-review.png',dpi=160,facecolor=BG);plt.close(fig)
print('FRONT_RENDER_PASS')
