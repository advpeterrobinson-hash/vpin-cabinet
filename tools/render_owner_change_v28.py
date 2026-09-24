"""CAD mesh engineering review; no illustrative/invented cabinet geometry."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from owner_review_scenes_v27 import scenes
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exports/generated/owner-change-v28'

def main():
 r=json.loads((OUT/'review-analysis.json').read_text());p={o['name']:o for o in r['inventory']}
 dest=OUT/'review';dest.mkdir(exist_ok=True)
 def pref(*s):return [n for n in p if n.startswith(s)]
 floor=pref('CapturedBottom','LowCrossmember','RearCPUSupportRail','CPURailBacking','BottomFilter','ClassicLegBracket')
 controls=pref('Control','CoinDoor','Plunger','SSF')
 boards=pref('ReviewBoard','ReviewPayload','ReviewSupport')
 cpu=pref('RearCPUFixedSlide','RearCPUShelfStowed','RearCPUOpenCaseStowed')
 cradle=pref('CradleSide','CradleCrossmember','CradleRearBeam','PropRod','PropFixed')
 raised=pref('CradleOpenGhost','SafetyStayOpen','PropUpperLockPin','PropPinKeeper')
 current=scenes(p)[5][2]+scenes(p)[13][2]
 rows=[
 ('A','Current cabinet interior',current,35,-55,'CURRENT CAD. Right wall and playfield display omitted for inspection; current two carriers retained.'),
 ('B','Floor / penetration map',floor+pref('DefinedIntake','DefinedFilterMount','UtilityAMains','UtilityAEthernet'),90,-90,'TOP DOWN. Actual bottom slots / filter; three low ties; CPU rails/backing; corner reserves. No new cuts.'),
 ('C','Underside mains candidates',floor+pref('ReviewInlet','ReviewMainsMid','ReviewPlugMid','ReviewMainsFront'),90,-90,'Green: mid-left investigation zone. Orange: front alternative. Red: central reject. Floor clearance unknown.'),
 ('D','RJ45 candidate locations',pref('RearPanelWithCPU','CabinetRightSide','UtilityAEthernet','MovingHarness','ReviewRJ45'),30,45,'Rear adapter preferred. Side internal probe clashes with moving harness. Bottom access/exposure unverified.'),
 ('E','Usable electronics volumes',floor+boards+controls+cpu+pref('CentralService'),55,-55,'F front: 306 x 85 x 110 payload. G/P sides: 115 x 262 x 110 each. Nominal review volumes, not hardware fits.'),
 ('F','Three removable service boards',floor+boards+pref('CentralService'),42,-55,'F front, G left DC distribution, P right PSU/controllers. Six wood support STATIONS; profiles/bolts unresolved.'),
 ('G','Front board access',pref('ReviewBoardF','ReviewPayloadF','ReviewSupportF','ReviewLiftF','ReviewExtractF','CoinDoor','Plunger','ControlStart','ControlExit','ControlLaunch','LowCrossmember1'),30,-65,'Whole board exits through top after glass removal and positively supported playfield lift; not through coin door.'),
 ('H','Left distribution board access',floor+pref('ReviewBoardG','ReviewPayloadG','ReviewSupportG','ReviewCableG','ReviewLiftG','ReviewMainsMid'),40,-55,'DC/control distribution only. Protective earth / mains remain in dedicated fixed touch-safe enclosure.'),
 ('I','Right PSU / controller board access',floor+pref('ReviewBoardP','ReviewPayloadP','ReviewSupportP','ReviewCableP','ReviewLiftP')+cpu,40,-55,'Enclosed modules within envelope only. Heavy mechanical toys need their own shell load path; no allocation by guess.'),
 ('J','Independent board removal',boards+raised+pref('ReviewLift','ReviewExtract')+cpu,25,-55,'Lift then forward; unplug first. Glass removed, both props pinned. Other boards remain. Physical hand/cable trial required.'),
 ('K','Cable and service corridors',floor+boards+pref('ReviewCable','CentralService','MovingHarness')+cpu,50,-55,'43 mm under-board loop reservations; central and CPU corridors retained. Bend radii, connector access unmeasured.'),
 ('L','Conflicts / rejected alternatives',pref('ReviewRejected','CentralService','ReviewMainsFront','ReviewMainsLidFront','ReviewSupportF','ReviewBoardF','ReviewRJ45SideInside','MovingHarness','ControlLeftAction')+cradle,40,-55,'RED: full-depth raised side payload hits action button; spanning board blocks aisle. Front mains conflicts with support/lid. Side RJ45 hits harness.')]
 colors={'BOARD':'#138f95','PAYLOAD':'#52b998','SUPPORT':'#976326','CABLE':'#168fd1','REMOVAL':'#6c74da','REJECT_ZONE':'#df3038','INLET_ZONE':'#eea32e','MAINS_PROBE':'#eb993d','RJ45_ZONE':'#c45ead','ACCESS':'#b277cc','EXTERNAL_ACCESS':'#cbad6b'}
 for letter,title,names,elev,azim,note in rows:
  if letter in ('B','C'):
   fig,ax=plt.subplots(figsize=(12,10))
   layers=floor+pref('DefinedIntake','DefinedFilterMount')
   if letter=='C':layers+=pref('ReviewInlet')
   for n in dict.fromkeys(layers):
    o=p[n];v=np.array(o['vertices']);tri=np.array(o['triangles'],dtype=int)
    col='#c9b995';alpha=1
    if n.startswith('LowCross'):col='#88683b'
    elif n.startswith('RearCPU'):col='#5989ac'
    elif n.startswith('CPURailBacking'):col='#804759'
    elif n.startswith('ClassicLeg'):col='#909090'
    elif n.startswith('BottomFilter'):col='#83aece';alpha=.3
    elif n.startswith('Defined'):col='white'
    elif n.startswith('ReviewInlet'):col='#25ac6b' if 'MidLeft' in n else ('#db4149' if 'Central' in n else '#edaa38');alpha=.65
    polys=[a[:,:2] for a in v[tri] if abs(np.cross(a[1]-a[0],a[2]-a[0])[2])>.001]
    ax.add_collection(PolyCollection(polys,facecolors=to_rgba(col,alpha),edgecolors='none'))
   labels=[('LowCrossmember1V20','CM1'),('LowCrossmember2V20','CM2'),('LowCrossmember3V20','CM3'),('BottomFilterCarrierV27','18 slots + removable filter'),('RearCPUSupportRailLeftV24','CPU rails / backing'),('ClassicLegBracketFLV21','Leg reserve')]
   if letter=='C':labels += [('ReviewInletMidLeft','MID-LEFT: investigate'),('ReviewInletFront','FRONT: board/support conflict'),('ReviewInletCentral','CENTER: reject / service aisle')]
   labels.sort(key=lambda item:(p[item[0]]['bounds'][2]+p[item[0]]['bounds'][3])/2,reverse=True)
   for i,(n,label) in enumerate(labels):
    b=p[n]['bounds'];x=(b[0]+b[1])/2;y=(b[2]+b[3])/2
    ax.annotate(label,(x,y),xytext=(690,1220-i*120),arrowprops={'arrowstyle':'-','color':'#333'},fontsize=10)
   ax.set_xlim(-30,1200);ax.set_ylim(-30,1330);ax.set_aspect('equal');ax.set_xlabel('X / mm');ax.set_ylabel('Y / mm');ax.grid(alpha=.15)
   fig.suptitle(letter+' — '+title+'\nSaved CAD mesh projection / DESIGN-PROVISIONAL / no new cuts',fontsize=15)
   fig.text(.05,.035,note,fontsize=10);fig.savefig(dest/(letter+'.png'),dpi=140);plt.close(fig);continue
  fig=plt.figure(figsize=(14,10));ax=fig.add_subplot(projection='3d');faces=[];cs=[];points=[]
  for n in dict.fromkeys(names):
   o=p[n];v=np.array(o['vertices']);tri=np.array(o['triangles'],dtype=int)
   kind=r['candidates'].get(n,{}).get('kind','')
   col=colors.get(kind,'#a9aeb3');alpha=.45 if kind in ('PAYLOAD','REMOVAL','CABLE','ACCESS','EXTERNAL_ACCESS') else .9
   if n.startswith('ReviewInletMid'):col='#26a86a'
   if not kind:
    if o['role']=='STRUCTURAL_WOOD':col='#c8aa7a'
    if letter=='D' and n.startswith(('Cabinet','RearPanel')):alpha=.15
    elif n.startswith('SSF'):col='#bc699a'
    elif n.startswith(('Control','Plunger')):col='#e17c32'
    elif n.startswith('CentralService'):col='#468fcb';alpha=.25
   faces.extend(v[tri]);cs.extend([to_rgba(col,alpha)]*len(tri));points.extend(v)
  ax.add_collection3d(Poly3DCollection(faces,facecolors=cs,edgecolors=(.15,.2,.23,.12),linewidths=.12))
  pts=np.array(points);lo=pts.min(0);hi=pts.max(0);span=hi-lo
  for setter,a,b in zip((ax.set_xlim,ax.set_ylim,ax.set_zlim),lo,hi):setter(a-15,b+15)
  ax.set_box_aspect(np.maximum(span,50));ax.view_init(elev,azim)
  ax.set_xlabel('X / mm');ax.set_ylabel('Y / mm');ax.set_zlabel('Z / mm')
  for n in names:
   if n.startswith('ReviewBoard'):
    b=p[n]['bounds'];ax.text((b[0]+b[1])/2,(b[2]+b[3])/2,b[5]+10,n[-1],fontsize=13,color='black',weight='bold')
  if letter=='D':
   for n,label in [('ReviewRJ45Rear','Rear adapter'),('ReviewRJ45Side','Side candidate'),('ReviewRJ45Bottom','Bottom candidate'),('MovingHarnessKeepoutV18','Moving harness')]:
    b=p[n]['bounds'];ax.text(b[1],b[3],b[5],label,fontsize=9)
  fig.suptitle(letter+' — '+title+'\nV28 DESIGN-PROVISIONAL • NOT ACTIVE • NO MACHINING AUTHORITY',fontsize=15)
  fig.text(.04,.04,note,fontsize=10,wrap=True)
  fig.text(.04,.015,'Saved CAD meshes • tan: wood / teal: boards / green: payload / brown: support stations / blue-purple: service reservations',fontsize=9)
  fig.savefig(dest/(letter+'.png'),dpi=140);plt.close(fig)
 (dest/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>V28 CAD review</title><style>body{font:16px sans-serif;max-width:1400px;margin:auto}img{width:100%}</style><h1>V28 CAD-derived owner change review</h1><p>Provisional volumes only. Manufacturing remains blocked. Rebuild: bash tools/run_owner_change_v28.sh</p>'+''.join(f'<h2>{k} — {title}</h2><p>{note}</p><img src="{k}.png" alt="{title}">' for k,title,_,_,_,note in rows)+'\n')
 print('OWNER_CHANGE_RENDER_PASS: 12 CAD-derived views')
if __name__=='__main__':main()
