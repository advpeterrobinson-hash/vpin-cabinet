"""Eighteen engineering views from saved CAD tessellations only."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'exports/generated/simplification-v28'
def main():
 r=json.loads((OUT/'geometry.json').read_text());old=json.loads((ROOT/'exports/generated/owner-change-v28/review-analysis.json').read_text())
 p={o['name']:o for o in old['inventory']};p.update({o['name']:o for o in r['inventory']});dest=OUT/'review';dest.mkdir(exist_ok=True)
 def pref(*s):return [n for n in p if n.startswith(s)]
 omit={'CabinetRightSide','PlayfieldGlassTargetV20','GenericPlayfieldDisplayClosedV18','RearPanelWithCPUHatchV24','SRearPanel','SRearDoor'}
 current=[n for n in r['current_names'] if n not in omit]
 proposed=[n for n in r['proposed_names'] if n not in omit]
 floor=['CapturedBottomV20','STie1','STie2']
 boards=pref('SBoard','SPayload','SBracket')
 holder=pref('SBeam','SBridge','SCrossAxis','SShaftClamp','SPivot','SLanding')
 rear=['SRearPanel','SRearDoorOpen','SPCBase','SPCCase','UtilityAMainsEnclosureV26','UtilityAEthernetCarrierV26']
 raised=['SFrameOpen','GenericPlayfieldDisplayOpenGhostV18']+pref('SStrap','SStop','SPivot')
 rows=[
 ('01','CURRENT INTERIOR',current,'Current active design; inspection omissions only.'),
 ('02','SIMPLIFIED INTERIOR',proposed,'One floor PC base; three boards; three-piece holder. Shell/holder qualification remains open.'),
 ('03','CURRENT vs SIMPLIFIED EXPLODED',[], 'Exploded meshes compare physical arrangements, not assembly tolerances or a production BOM.'),
 ('04','SIMPLIFIED PLAYFIELD SUPPORT',holder+['GenericPlayfieldDisplayClosedV18'],'Two beams + one wood VESA bridge + stock cross-axis concept. No final bores.'),
 ('05','PLAYFIELD SERVICE POSITION',raised+pref('BackboxLeftSide','BackboxRightSide','BackboxFloor','BackglassDisplay'),'Restraints to locked backbox; stop UNRESOLVED. Inherited display-envelope overlaps still require resolution.'),
 ('06','SIMPLE REAR ACCESS',rear+['CabinetLeftSide','CabinetRightSide'],'Existing jambs; investigated opening 340 x 293. Ordinary outward hinge/latch; shear proof required.'),
 ('07','OPEN-FRAME PC LOCATION',floor+['SPCBase','SPCCase']+pref('ClassicLegBracket','BottomFilter'),'Existing case envelope lowered onto one base board. Third low tie removed provisionally; no slides.'),
 ('08','PC REMOVAL PATH',floor+rear+['SPCLift','SPCOut'],'Disconnect; unbolt base; lift above sill; hand-support rear removal. No extended cantilever load case.'),
 ('09','BOARD A / FRONT',pref('SBoardA','SPayloadA','SBracketA','SCableA')+['STie1']+pref('CoinDoor','Plunger'),'Simple board, two ordinary bracket reserves; top removal, not through coin door.'),
 ('10','BOARD B / DISTRIBUTION',pref('SBoardB','SPayloadB','SBracketB','SCableB')+floor,'DC distribution/control; protective earth stays in fixed touch-safe enclosure.'),
 ('11','BOARD C / POWER / AUDIO',pref('SBoardC','SPayloadC','SBracketC','SCableC')+floor,'Supplies/amplifiers that fit. Impact devices need a qualified rigid coupling, not assumed tray capacity.'),
 ('12','BOARD REMOVAL PATHS',boards+pref('SLift','SExtract')+raised,'Independent unplug/lift/forward removal. Normal tools; final cable and hand trials remain paused.'),
 ('13','CABLE CORRIDORS',boards+floor+pref('SCable','CentralService','MovingHarness')+['SPCCase'],'Central route retained; PC no longer needs a moving harness. Display loop still required.'),
 ('14','POWER LOCATION COMPARISON',floor+rear+pref('ReviewInletMid','ReviewPlugMid'),'Rear preferred: easier reach and less handling exposure. Underside reserve is comparison only.'),
 ('15','RJ45 LOCATION',rear+pref('UtilityAEthernetInternal','UtilityAEthernetPlug','ReviewRJ45Rear'),'Rear female/female panel coupler; ordinary patch cable. Existing small adapter only if grip requires it.'),
 ('16','VENTILATION COMPARISON',[], 'LEFT: retained 18 slots / ribs. RIGHT: two generic circular openings, not released fan cutouts.'),
 ('17','FLOOR / PENETRATION MAP',floor+pref('DefinedIntake','DefinedFilterMount','ClassicLegBracket')+['SPCBase'],'Retain intake/filter. Delete rail-clamp penetrations and CM3; base restraint positions still unresolved.'),
 ('18','PARTS REMOVED MAP',[n for n in current if n in r['removed_names'] and n not in ('LowCrossmember1V20','LowCrossmember2V20','RearCPUShelfStowedV24','RearCPUServiceDoorClosedV24')], 'Drawer assembly, old carriers/supports and old holder/props removed from proposal; retained source is history.')]
 def plot(ax,names,explode=False,red=False,top=False):
  faces=[];colors=[];points=[]
  for i,n in enumerate(dict.fromkeys(names)):
   o=p[n];v=np.array(o['vertices']).copy();tri=np.array(o['triangles'],dtype=int);kind=o.get('kind','')
   if explode:
    center=v.mean(0);v[:,0]+=(center[0]-300)*.35;v[:,1]+=(center[1]-650)*.2;v[:,2]+=i*12
   col='#c4a16e' if o['role']=='STRUCTURAL_WOOD' or kind=='WOOD' else '#8b9ca6';alpha=.8
   if kind=='BOARD':col='#138f95'
   if kind=='PAYLOAD':col='#69b293';alpha=.28
   if kind=='ACCESS':col='#5889cd';alpha=.18
   if kind=='COMMODITY':col='#627b91'
   if kind=='RESTRAINT':col='#f49820';alpha=1
   if kind=='UNRESOLVED':col='#d74646';alpha=.8
   if n.startswith('SSF'):col='#b677a8'
   if n.startswith('Defined'):col='#eeeeee'
   if n in ('GenericPlayfieldDisplayClosedV18','GenericPlayfieldDisplayOpenGhostV18'):alpha=.12
   if n.startswith('ReviewInlet'):col='#d39937'
   if red:col='#d95143';alpha=.8
   faces.extend(v[tri]);colors.extend([to_rgba(col,alpha)]*len(tri));points.extend(v)
  ax.add_collection3d(Poly3DCollection(faces,facecolors=colors,edgecolors=(.1,.15,.2,.12),linewidths=.1))
  pts=np.array(points);lo=pts.min(0);hi=pts.max(0)
  for setter,a,b in zip((ax.set_xlim,ax.set_ylim,ax.set_zlim),lo,hi):setter(a-20,b+20)
  ax.set_box_aspect(np.maximum(hi-lo,70));ax.view_init(90 if top else 35,-90 if top else -55)
  ax.set_xlabel('X mm');ax.set_ylabel('Y mm');ax.set_zlabel('Z mm')
  for n in names:
   if n.startswith('SBoard') and not explode:
    b=p[n]['bounds'];ax.text((b[0]+b[1])/2,(b[2]+b[3])/2,b[5]+10,n[-1],fontsize=13,weight='bold')
 for key,title,names,note in rows:
  fig=plt.figure(figsize=(15,10))
  if key=='03':
   for idx,(ns,label) in enumerate([(current,'CURRENT'),(proposed,'PROPOSED')],1):
    ax=fig.add_subplot(1,2,idx,projection='3d');plot(ax,ns,explode=True);ax.set_title(label)
  elif key=='16':
   for idx,(ns,label) in enumerate([(['CapturedBottomV20']+pref('DefinedIntake'),'RETAIN'),(['SAlternativeVentFloor'],'ALTERNATIVE / NOT SELECTED')],1):
    ax=fig.add_subplot(1,2,idx,projection='3d');plot(ax,ns,top=True);ax.set_title(label)
  else:
   ax=fig.add_subplot(projection='3d');plot(ax,names,red=key=='18',top=key=='17')
   if key in ('06','15'):ax.view_init(25,55)
   annotations={
    '04':[('SBridge','Wood VESA bridge'),('SCrossAxis','Stock-axis reserve')],
    '05':[('SStrapL','Captive restraint L'),('SStrapR','Captive restraint R'),('SStopL','STOP UNRESOLVED')],
    '07':[('SPCBase','One detachable base'),('SPCCase','Existing case envelope')],
    '14':[('UtilityAMainsEnclosureV26','REAR preferred'),('ReviewInletMidLeft','Underside candidate only')],
    '15':[('UtilityAEthernetCarrierV26','Rear RJ45 / sample required')],
    '17':[('STie1','CM1 retained'),('STie2','CM2 retained'),('SPCBase','Base / NO CM3 / NO rails')]}
   for n,label in annotations.get(key,[]):
    b=p[n]['bounds'];ax.text(b[1],(b[2]+b[3])/2,b[5]+8,label,fontsize=9)
  fig.suptitle(key+' — '+title+'\nDESIGN-PROVISIONAL • PHYSICAL EXECUTION PAUSED • MANUFACTURING BLOCKED',fontsize=15)
  fig.text(.035,.045,note,fontsize=10)
  fig.text(.035,.02,'Saved CAD only. Tan: wood; teal: removable boards; grey: hardware; orange: restraint; red: unresolved stop / removed parts.',fontsize=9)
  fig.savefig(dest/(key+'.png'),dpi=130);plt.close(fig)
 (dest/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>V28 architecture convergence</title><style>body{font:16px sans-serif;max-width:1400px;margin:auto}img{width:100%}</style><h1>Architecture convergence — provisional</h1><p>Physical sessions paused. No production or safety acceptance.</p>'+''.join(f'<h2>{k} — {t}</h2><p>{note}</p><img src="{k}.png" alt="{t}">' for k,t,_,note in rows)+'\n')
 print('SIMPLIFICATION_RENDER_PASS: 18 saved-CAD views')
if __name__=='__main__':main()
