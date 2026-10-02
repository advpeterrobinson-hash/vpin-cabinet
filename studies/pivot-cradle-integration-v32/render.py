"""Original review images from actual OCC tessellation. CERN-OHL-S-2.0."""
from pathlib import Path
import json,math,textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[2];O=R/'exports/generated/pivot-cradle-integration-v32';D=json.loads((O/'detail-mesh.json').read_text());B=json.loads((O/'mesh.json').read_text());Q=json.loads((O/'validation.json').read_text());parts={p['name']:p for p in B['parts']};P=D['dowel_axis'];W=D['wpc_axis'];files=[]
plt.rcParams.update({'font.size':10,'figure.facecolor':'#f8fafc','axes.facecolor':'#f8fafc','font.family':'DejaVu Sans'})
def col(n):
 for k,c in [('OpenCradle','#c6a466'),('Dowel','#815624'),('BasePlywood','#5485a6'),('WPC_','#9563b4'),('Hinge','#566987'),('Screw','#485868'),('BB_','#7198ad'),('FLOOR','#8d9c8a'),('SIDE_','#a5adb2'),('Shelf','#88a797')]:
  if k in n:return c
 return '#ae9272'
def verts(m,a=0,axis=W):
 v=np.array(m['vertices']);t=math.radians(a);rot=np.array([[1,0,0],[0,math.cos(t),-math.sin(t)],[0,math.sin(t),math.cos(t)]]);ax=np.array(axis);return (v-ax)@rot.T+ax

def plot(ax,items,dims=(1,2),alpha=.65,color=None):
 for m in items:
  v=verts(m);ax.add_collection(PolyCollection(v[np.array(m['faces'])][:,:,dims],facecolors=color or col(m['name']),edgecolors=color or col(m['name']),linewidth=.22,alpha=alpha))
 ax.set_aspect('equal');ax.grid(alpha=.16);ax.set_xlabel('XYZ'[dims[0]]+' / mm');ax.set_ylabel('XYZ'[dims[1]]+' / mm')
def named(role,*names):return [p for p in D[role] if p['name'] in names]
def axes(ax):
 ax.plot(P[1],P[2],'o',color='#815624',ms=5);ax.plot(W[1],W[2],'x',color='#922842',ms=8)
def zoom(ax,items,limits=((990,1100),(445,535))):plot(ax,items);axes(ax);ax.set(xlim=limits[0],ylim=limits[1])
def text(ax,s):
 s='\n'.join('\n'.join(textwrap.wrap(line,width=48,break_long_words=False)) if line else '' for line in s.split('\n'));ax.axis('off');ax.text(0,.97,s,va='top',linespacing=1.45,fontsize=10.5)
def finish(fig,n,title,diagnostic=False):
 fig.suptitle(f'{n:02}  '+title,x=.04,ha='left',fontweight='bold',fontsize=16)
 fig.text(.04,.025,('REJECTED / COMPARISON GEOMETRY • ' if diagnostic else 'CURRENT DESIGN CANDIDATE • ' )+'actual CAD • WPC hardware reserves provisional • manufacturing BLOCKED • CERN-OHL-S-2.0',fontsize=9,color='#934237');fig.subplots_adjust(top=.85,bottom=.12,left=.075,right=.97,wspace=.28);p=O/f'{n:02}-review.png';fig.savefig(p,dpi=155);plt.close(fig);files.append({'file':p.name,'title':title,'diagnostic_only':diagnostic})
def profile(r):return [p for p in D['radii'][str(r)] if p['name'].endswith('L')]
def scene(ax,state='PLAY',a=None):
 ss={**parts,**B['states'][state]}
 for n,m in ss.items():
  if m is None or n in ['SIDE_L','FRONT'] or any(k in n.upper() for k in ['RESERVE','RESERVED','CHECKENVELOPE','CANDIDATEPAYLOAD']):continue
  v=verts(m,a if a is not None and n.startswith('BB_') else 0)
  ax.add_collection3d(Poly3DCollection(v[np.array(m['faces'])],facecolor=col(n),edgecolor='#39434d',linewidth=.08,alpha=.55 if n.startswith('BB_') else .3))
 ax.set(xlim=(-110,710),ylim=(-80,1350),zlim=(0,1450),xlabel='X / mm',ylabel='Y / mm',zlabel='Z / mm');ax.set_box_aspect((820,1430,1450));ax.view_init(elev=24,azim=-53);ax.set_title('Left side / front hidden for inspection; glass and matrix removed in service states',fontsize=9)
fig,ax=plt.subplots(1,2,figsize=(13,7));zoom(ax[0],named('current','PF_OpenCradleL','PF_WoodDowel'));ax[0].add_patch(Circle((W[1],W[2]),4.7625,fill=False,color='#ba3047',lw=2));text(ax[1],'Before relief: WPC pivot through rear-upper ear\n\nAxis Y1066.8 / Z508\nSmall 3 mm internal probe: 213.77 mm³ overlap\non each accepted cradle\n\nThe primary dowel seat is below and forward.\nNo pivot, dowel, TV or strap translation is needed.\n\nThis is the historical conflict, not the final profile.');finish(fig,1,'Original cradle / corrected WPC pivot conflict',True)
fig,ax=plt.subplots(1,2,figsize=(13,7));zoom(ax[0],named('current','PF_OpenCradleL','PF_WoodDowel'));ax[0].plot([P[1],W[1]],[P[2],W[2]],'k--');text(ax[1],f'Section normal to transverse axes\n\nDowel: Y{P[1]:.6f} / Z{P[2]:.6f}\nWPC: Y1066.8 / Z508\nCenter separation: 39.507418 mm\nSeat-circle center is 0.5 mm above dowel axis\nSeat-circle radius: 16.5 mm\n\nWPC to loaded semicircle: 27.720514 mm\nWPC to cradle rear edge: 8.450620 mm\nWPC to old top: 6.220330 mm');finish(fig,2,'Section through both pivot axes')
fig,ax=plt.subplots(1,2,figsize=(13,8));plot(ax[0],named('current','PF_OpenCradleL'));ax[0].set(xlim=(980,1100),ylim=(20,540));text(ax[1],'Original one-piece 18 mm plywood cradle\n\nØ32 dowel in R16.5 lower half-circle\n180° seat wrap; 33 mm open throat\nFront / rear seat wall: 8.2506 / 23.5 mm\nMinimum existing front web: 8.2506 mm\nFloor foot: 58.2506 × 18 mm\n\nThree existing screws are retained.\nOnly the rear ear top is relieved.');finish(fig,3,'Current cradle profile — before local relief',True)
for no,r in [(4,5),(5,10),(6,15),(7,12)]:
 row=next(q for q in Q['radius_study']['candidates'] if q['radius_mm']==r);fig,ax=plt.subplots(1,2,figsize=(13,7));zoom(ax[0],profile(r)+named('current','PF_WoodDowel'));ax[0].add_patch(Circle((W[1],W[2]),r,fill=False,color='#9563b4',lw=2));sel=r==12
 text(ax[1],f'R{r} coaxial packaging reserve + 2 mm allowance\nBroad top/rear opening; convex R3 corner\nRear-ear top: Z{row["rear_top_z_mm"]:.1f}\n\nSeat wrap: {row["seat_wrap_after_deg"]:.3f}°\nExisting load-path web: 8.2506 mm\nRear top above seat: {row["rear_top_above_seat_axis_mm"]:.3f} mm\nStraight rear guidance: {row["rear_straight_guide_height_mm"]:.3f} mm\n\n'+('SELECTED: largest passing conservative screen\nR12 through-cradle tool margin: 2 mm' if sel else 'NOT SELECTED\n'+('Rear guidance / top margin below screen' if r==15 else 'R12 tool envelope lacks required 2 mm margin')));finish(fig,no,('Selected largest viable relief' if sel else f'R{r} relief — diagnostic profile'),not sel)
fig,ax=plt.subplots(1,2,figsize=(13,7));zoom(ax[0],profile(12)+named('current','PF_WoodDowel'),((1005,1083),(457,505)));text(ax[1],'R12 selected — loaded seat unchanged\n180° wrap before / after\n0.5 mm nominal radial seat clearance\nFront / rear seat wall: 8.2506 / 23.5 mm\n8.2506 mm minimum front load-path web\n\nRear guide: 6.2797 mm straight + R3 top rounding\nRear top: 9.2797 mm above seat-circle center\nNo new narrow ear or closed hole\nAll wood below seat center remains identical.');finish(fig,8,'Seat ligament and rear guidance close-up')
fig,ax=plt.subplots(1,2,figsize=(13,7));plot(ax[0],named('selected','PF_OpenCradleL'),dims=(0,2));plot(ax[0],named('tools','WPC_ToolL'),dims=(0,2),alpha=.22);plot(ax[0],named('hardware','WPC_BushingL','WPC_NutWasherL'),dims=(0,2),alpha=.35);ax[0].set(xlim=(0,200),ylim=(465,535));text(ax[1],'Separate provisional corridors\nAxis R5; bushing R8, 10 mm internal reach\nNut / washer R10, 24 mm internal reach\nTool R12, through cradle + 150 mm inward\n\nSelected relief gives R12 a 2 mm margin.\nTool path blocked in PLAY and 50° SERVICE.\nClear after 48 mm lift-out / assembly removal.\n\nMeasure real stack, flange, nut and socket.\nNo final cabinet-side hole or hardware SKU frozen.');finish(fig,9,'WPC installation / service corridor')
fig,ax=plt.subplots(1,2,figsize=(13,8));plot(ax[0],named('selected','PF_OpenCradleL')+named('screws','PF_SupportMountScrewL1','PF_SupportMountScrewL2','PF_SupportMountScrewL3'));ax[0].set(xlim=(990,1090),ylim=(20,540));text(ax[1],'All six current support screws unchanged\n\nPer-side Y / Z centers, mm:\n1037.000 / 192.000\n1042.500 / 320.110\n1055.251 / 448.220\n\n4.5 × 30 mm remains a candidate screw only.\nRelief stays above every screw / countersink.\nAll six existing driver corridors remain clear.\nNo added screws; no dense screw compensation.');finish(fig,10,'Support screw relationship')
fig,ax=plt.subplots(1,2,figsize=(13,8));plot(ax[0],named('selected','PF_OpenCradleL')+named('current','PF_WoodDowel'));ax[0].set(xlim=(980,1100),ylim=(20,540));ax[0].annotate('',(1046,55),(1046,450),arrowprops={'arrowstyle':'->','color':'#237b57','lw':3});text(ax[1],'Dowel → semicircular seat → continuous stem\n→ cabinet floor\n\nEntire region below seat center unchanged\nFoot bearing: 1,048.5112 mm² per support\nRear stem edge remains straight\nNo interrupted vertical load path\n\nSide screws retain against tipping / separation;\nthey are not primary vertical supports.\nNo stiffness or strength certification claimed.');finish(fig,11,'Direct floor-bearing load path preserved')
for no,state,title in [(12,'PLAY','Playfield closed'),(13,'PLAYFIELD SERVICE','Playfield 50° service'),(14,'LIFT-OUT','Complete playfield lift-out — 48 mm'),(16,'MATRIX REMOVED','Backbox 45°'),(17,'BACKBOX FOLD','Backbox 90°'),(18,'PLAY','Final combined architecture')]:
 fig=plt.figure(figsize=(12,10));scene(fig.add_subplot(111,projection='3d'),state,a=45 if no==16 else None);finish(fig,no,title)
fig,ax=plt.subplots(1,2,figsize=(13,7));bb=[parts['BB_Floor']];m={**bb[0],'vertices':verts(bb[0],1).tolist()};plot(ax[0],[parts['BACKBOX_BASE'],m]);ax[0].set(xlim=(1120,1200),ylim=(575,635));text(ax[1],'1° fold about Y1066.8 / Z508\n210 mm sides; floor front Y1146 unchanged\nShelf bearing releases immediately at 0°+\nNo wood penetration\n\nGLASS REMOVED + MATRIX REMOVED\nPlayfield stays closed for backbox folding.\n\nInstalled hardware envelopes remain provisional.');finish(fig,15,'Backbox early fold — clean floor release')
files.sort(key=lambda q:q['file']);(O/'review-images.json').write_text(json.dumps({'images':files,'source':'actual OCC tessellation; hardware reserves are explicitly provisional','upstream_assets_included':False},indent=2)+'\n');print('PIVOT_CRADLE_IMAGES_PASS',len(files))
