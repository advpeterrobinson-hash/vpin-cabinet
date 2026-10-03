"""Actual B-rep review scenes; no invented success renderings. CERN-OHL-S-2.0."""
from pathlib import Path
import json,gzip,sys
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from pivot_cradle_integration_v32 import load
O=R/'exports/generated/structural-v335';old=load(R/'exports/generated/backbox-lock-integration-v32/play.FCStd');new=load(O/'play.FCStd');study=load(O/'study.FCStd');V=A.Vector
scenes=[]
def subset(d,names):return {n:d[n] for n in names if n in d}
def moved(s,v):q=s.copy();q.translate(V(*v));return q
def scene(id,title,parts,view=(1,-2,1.5),note='',colors=None):
 meshes=[]
 for i,(n,s) in enumerate(parts.items()):
  if s.isNull():continue
  v,f=s.tessellate(.4);meshes.append({'name':n,'vertices':[list(p) for p in v],'faces':f,'color':(colors or {}).get(n,['#be9875','#587b8d','#c49d4e','#8f9d8b','#b77366'][i%5])})
 scenes.append({'id':id,'title':title,'meshes':meshes,'view':view,'note':note})
def section(s,axis,lo,thick):
 b=s.BoundBox;xyz=[b.XMin-1,b.YMin-1,b.ZMin-1];sz=[b.XLength+2,b.YLength+2,b.ZLength+2];xyz[axis]=lo;sz[axis]=thick;return s.common(Part.makeBox(*sz,V(*xyz)))
scene('01','CURRENT baseline floor and M006',subset(old,['FLOOR','FLOOR_CLEAT_18','FLOOR_CLEAT_552']),(1,-1,-2),'M006 is directly under the floor; 30mm-wide continuous bearing per side.')
scene('02','Captured floor: 4mm nominal side engagement',subset(new,['SIDE_L','FLOOR','FRONT','REAR']),(2,-2,2),'SIDE_R omitted for inspection. 14mm nominal exterior skin. Width = measured stock + coupon clearance.')
scene('03','Floor underside pocket stations', {**subset(new,['FLOOR']),**{n:s for n,s in study.items() if n.startswith('FLOOR_Screw') or n.startswith('FLOOR_Pocket')}},(0,0,-1),'12 reference stations; M006 absent during drilling. Kreg model, drill and screws TBD.')
scene('04','Pocket screw section — reference geometry',{'Floor':section(new['FLOOR'],1,159.9,.2),'SideL':section(new['SIDE_L'],1,159.9,.2),'Pocket':study['FLOOR_PocketL1'],'Screw':study['FLOOR_ScrewL1']},(0,-1,0),'15° / 28mm / R2 shank are STUDY assumptions. Exact jig/drill/length not selected.')
scene('05','Optional transverse offcut supports — TOOLING',subset(study,['OptionalTemporarySupport1','OptionalTemporarySupport2']),(1,-2,2),'Two564×50×18mm offcuts. Not permanent cabinet parts; not selected as replacement for retained M006.')
scene('06','Lower captured shell dry-fit',subset(new,['SIDE_L','SIDE_R','FLOOR','FRONT','REAR','BACKBOX_BASE']),(1,-2,2),'Floor/ends/shelf enter before SideR closes. Dry-fit, measure diagonals/600mm width, then glue and clamp.')
scene('07','Baseline rear bearing shelf',subset(old,['BACKBOX_BASE']),(1,-2,2),'Bearing topZ596.9; baseline564mm width.')
scene('08','Rear bearing shelf with side captures',subset(new,['BACKBOX_BASE'])|{'LeftSideSection':section(new['SIDE_L'],1,1127.125,180.975),'RightSideSection':section(new['SIDE_R'],1,1127.125,180.975)},(1,-2,2),'Open-top side rabbets, not closed dados. Top and original backbox contact footprint unchanged.')
scene('09','Rear shelf underside pocket reference',{**subset(new,['BACKBOX_BASE']),**{n:s for n,s in study.items() if n.startswith('BACKBOX_BASE_Screw') or n.startswith('BACKBOX_BASE_Pocket')}},(0,0,-1),'Y1155 /1220 each side. Manual underside work; FACE_A remains top. No CNC flip.')
scene('10','Shelf pockets and WPC/lock service reserves',{**subset(new,['BACKBOX_BASE','PF_OpenCradleL','PF_OpenCradleR']),**{n:s for n,s in new.items() if n.startswith('WPC_') or 'UprightLock' in n and 'Thread' in n},**{n:s for n,s in study.items() if n.startswith('BACKBOX_BASE_Driver')}},(1,-2,1),'Reference drivers clear current reserves; purchased hardware/tool envelopes remain HOLD.')
for id,title,d,newer in [('11','Historical rear fan through-bolt stack',old,False),('12','Rear fan: wood → fan → grill → screw head',new,True)]:
 p={'RearWood':section(d['REAR'],0,150,155),'Fan':moved(d['FAN_230'],[0,-65,0]),'InnerGrill':moved(d['CandidateFanGuard230Inner'],[0,-105,0])}
 if newer:p.update({n:moved(s,[0,-145,0]) for n,s in d.items() if n.startswith('RearFanWoodScrew230')})
 else:p.update({n:moved(s,[0,-45 if 'Nut' in n else -25,0]) for n,s in d.items() if n.startswith('CandidateFanBolt230')})
 scene(id,title,p,(1,-1,.8),'INTERIOR → WOOD (+Y). Wood screw pilot and length HOLD.' if newer else 'Superseded stack shown for audit only; not current assembly instructions.')
scene('13','Baseline open-cradle profile',subset(old,['PF_OpenCradleL']),(1,0,0),'13 exterior edges; seat180°; rear limiting ligament6.280mm.')
scene('14','Trimmed cradle candidate — NOT PROMOTED',subset(new,['SHELF_3','CROSS_3','CROSS_GUIDE_3L'])|subset(study,['RejectedSimplification_PF_OpenCradleL']),(1,0,0),'11 exterior edges; root unchanged but upper guide wall narrows23.5 to8.251mm. Original retained pending structural evidence.')
scene('15','T3 −20mm diagnostic — REJECTED',subset(new,['PF_OpenCradleL','SHELF_3'])|{n:s for n,s in study.items() if n.startswith('Diagnostic_')},(1,0,0),'No meaningful simplification: seat/WPC/S3 constraints remain. CURRENT cradle and T3 do not move.')
scene('16','S3 retained — no move study selected',subset(new,['SHELF_3','PF_OpenCradleL','PF_OpenCradleR','FAN_230','FAN_370']),(1,-1,1),'S3±20mm not performed: no demonstrated benefit justifies reopening rear-service clearances.')
scene('17','Old monitor stop blocks and pads',subset(old,['BB_MonitorCarrier0','BB_MonitorCarrier1','BB_MonitorStopBlock0','BB_MonitorStopBlock1','BB_MonitorStopContact0','BB_MonitorStopContact1','BB_MonitorStopScrewReserve0','BB_MonitorStopScrewReserve1']),(1,2,1),'Six plywood pieces: two18mm bases +two12mm caps +two4mm pads.')
railnames=['BB_MonitorCarrier0','BB_MonitorCarrier1','BB_MonitorStopRail','BB_StopAdjuster0','BB_StopAdjuster1','BB_StopTip0','BB_StopTip1','BB_StopRailRetention0','BB_StopRailRetention1']
scene('18','One18mm transverse monitor-stop rail',subset(new,railnames),(1,2,1),'M067×1;6mm end captures +two rear retention screws; two adjustable M6-family supports.')
p=subset(new,railnames)
for i,x in enumerate([160,440]):p['RearDriver'+str(i)]=Part.makeCylinder(8,90,V(x,1261,926),V(0,1,0))
scene('19','Stop rail rear attachment and access',p,(1,2,1),'Driver envelopes R8×90mm checked with doors open. Final screws/inserts/stroke need physical qualification.')
scene('20','4mm plywood pads replaced by purchased contact tips',{'OldPadL':moved(old['BB_MonitorStopContact0'],[0,0,0]),'OldPadR':moved(old['BB_MonitorStopContact1'],[0,0,0]),'NewTipL':moved(new['BB_StopTip0'],[0,-40,0]),'NewTipR':moved(new['BB_StopTip1'],[0,-40,0])},(1,-2,1),'M049 retired; zero4mm plywood pieces. Polymer tip envelopes are provisional hardware.')
scene('21','Manufacturing-piece comparison: old six / new one',{'OldBlockL':old['BB_MonitorStopBlock0'],'OldBlockR':old['BB_MonitorStopBlock1'],'OldPadL':old['BB_MonitorStopContact0'],'OldPadR':old['BB_MonitorStopContact1'],'NewRail':moved(new['BB_MonitorStopRail'],[0,-140,0])},(1,-2,1),'106→101 permanent wood pieces;62→59 families. SW01×4 unchanged. M006 retained.')
wood={p['source_component'] for p in json.loads((O/'manufacturing-register.json').read_text())['parts']}
scene('22','V33.5 interior inspection', {n:s for n,s in new.items() if n in wood and n not in ['SIDE_R'] and not n.startswith(('PF_Base','BB_Door'))},(1,-2,2),'Inspection cutaway only. Exterior dimensions, playfield, WPC axis and SW01 remain unchanged.')
scene('23','Recovered conventional front-right plunger',subset(new,['FRONT','PLUNGER_RESERVED','PlungerFrontInterfaceProvisional','PlungerShaftProvisional','PlungerHandleProvisional']),(.8,-2,.7),'Latest authority X520/Z280. Body/travel reference preserved. Final plunger bore NOT CUT.')
# The owner confirms no final installed coordinates. A schematic panel follows
# in the renderer rather than an invented CAD placement or final drilled holes.
scenes.append({'id':'24','title':'Under-front controls — restored intent, unlocated','meshes':[],'view':[0,0,1],'note':'220×55mm intent. Volume / OFF-AUDIO-PINBALL / Bluetooth pair / optional USB-C. No final centers or bores.','schematic':True})
(O/'review-scenes.json.gz').write_bytes(gzip.compress(json.dumps(scenes).encode(),mtime=0));print('V335_REVIEW_SCENES_PASS',len(scenes),flush=True)
