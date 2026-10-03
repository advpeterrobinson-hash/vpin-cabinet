"""V33.6.1 review scenes from exact native B-reps. CERN-OHL-S-2.0.
No scene grants CNC release. Held adapter window is never shown as current.
"""
from pathlib import Path
import gzip,json,sys,math
import FreeCAD as A,Part,MeshPart
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,transform,pf_names,PF,V
O=R/'exports/generated/button-relief-v3361';old=load(R/'exports/generated/monitor-support-v336/play.FCStd');new=load(O/'play.FCStd');st=load(O/'study.FCStd');historical=load(R/'exports/generated/structural-v335/play.FCStd')
C=json.loads((R/'config/button_relief_v3361.json').read_text());a=json.loads((R/'exports/generated/notch-floor-fans-v32/validation.json').read_text())['review']['closed_slope_deg'];bz=400.05+45*math.tan(math.radians(a))-12-55*math.cos(math.radians(a))
scenes=[];cache={}
def inv(s):q=s.copy();q.translate(V(0,-45,-bz));q.rotate(V(),V(1,0,0),-a);return q
def sub(d,names):return {n:d[n] for n in names if n in d}
def select(d,*starts):return {n:s for n,s in d.items() if n.startswith(starts)}
def slice(s,axis,low,high):
 b=s.BoundBox;pos=[b.XMin-1,b.YMin-1,b.ZMin-1];size=[b.XLength+2,b.YLength+2,b.ZLength+2];pos[axis]=low;size[axis]=high-low;return s.common(Part.makeBox(*size,V(*pos)))
def col(n):
 if 'HELD' in n or 'Held_' in n:return '#bb6352'
 if 'Cable' in n or 'Connector' in n:return '#15717e'
 if n.startswith(('LeafButton','LeafNut')):return '#984524'
 if n.startswith(('Leaf','ButtonAccess','Button')):return '#446e80'
 if 'VESA' in n or 'Clamp' in n:return '#6a879c'
 if 'Stop' in n:return '#b27b28'
 if 'Slot' in n or 'Thread' in n:return '#267568'
 if 'Display' in n or n in ['TV_ENVELOPE','PLAYFIELD_ENVELOPE']:return '#354858'
 if 'Glass' in n:return '#a9c0c9'
 if 'Screw' in n or 'Bolt' in n:return '#555b61'
 return '#c8ae8c'
def panel(label,parts,view=(1,-2,1.5),colors=None,alpha=None,limits=None,annotations=None,edges=None):
 meshes=[]
 for n,s in parts.items():
  if s.isNull():continue
  mm=MeshPart.meshFromShape(Shape=s,LinearDeflection=.45,AngularDeflection=.5,Relative=False);vv,ff=mm.Topology;meshes.append({'name':n,'vertices':[list(p) for p in vv],'faces':ff,'color':(colors or {}).get(n,col(n)),'alpha':(alpha or {}).get(n,1)})
 return {'label':label,'meshes':meshes,'view':view,'limits':limits,'annotations':annotations or [],'edges':edges or []}
def line_wire(s,y=None):
 # True native edges, projected by renderer; no traced/invented silhouette.
 out=[]
 for e in s.Edges:
  pts=e.discretize(Deflection=.12)
  if len(pts)>1:out.append([list(p) for p in pts])
 return out
def add(id,title,panels,note,legend=None):scenes.append({'id':id,'title':title,'panels':panels,'note':note,'legend':legend or []})
def lp(d):return {n:inv(s) for n,s in d.items()}
def buttonset(d):return {n:s for n,s in d.items() if n.startswith(('Leaf','Button')) and n.endswith('_L')}
localold=inv(historical['PF_BasePlywood']);localnew=inv(new['PF_BasePlywood'])
meta=json.loads((O/'button-metrology.json').read_text());geom=json.loads((O/'geometry-validation.json').read_text())
for id,d,label in [('01',old,'WRONG V33.6 · Y255 / Y310, Z270'),('02',new,'OWNER AUTHORITY · Y89 / Y127, local top −65')]:
 ann=[]
 for i,kind in enumerate(['primary','secondary']):
  c=d['LeafButton_'+kind+'_L'].BoundBox.Center
  ann.append({'point':[0,c.y,c.z],'text':f'Y{c.y:g} / Z{c.z:.3f}','offset':[-60,-40-35*i]})
 add(id,'Button comparison — '+label,[panel('Left side profile · front at right',{'SIDE_L':d['SIDE_L'],**buttonset(d)},(-1,0,0),annotations=ann)],'The front ergonomic centers were explicitly corrected in87d63825. V33.6 temporarily reinstated the superseded older layout. Hardware geometry is reference-only; final bores/recesses remain PURCHASE_BEFORE_CNC.')
add('03','Correct front buttons — interior service',[panel('Inside left front corner',{'SideSection':slice(new['SIDE_L'],1,0,285),'BaseSection':slice(new['PF_BasePlywood'],1,0,285),**buttonset(new)},(1,-.3,.35))],'Actual body, nut, leaf, contact, wire and driver reserves at the restored centers. The wood relief adapts to front ergonomics. No button is shifted to solve an interference.')
add('04','Historical horn — rejected contour',[panel('V33.5 M025 front-left',{'HistoricalHorn':localold},(0,0,1),limits=[35,145,0,180],edges=[{'lines':line_wire(localold),'color':'#7b3925','width':1.6}])],'Rounded local notch left a forward plywood lip. The current correction removes that bridge by opening the relief directly through the front edge.')
add('05','M025 — clean open-front relief',[panel('Front-left detail · one R8 return',{'M025':localnew},(0,0,1),limits=[35,145,0,180],edges=[{'lines':line_wire(localnew),'color':'#254856','width':1.2}]),panel('One 18 mm part · rear window retained',{'M025':localnew},(0,0,1),edges=[{'lines':line_wire(localnew),'color':'#254856','width':.7}])],'Straight narrowed front edges return to full width with simple R8 transitions. The relief is derived from current reference service envelopes with2 mm clearance. Rear180 ×110 R8 window and both strain slots remain exact.')
add('06','M025 historical/current overlay',[panel('Same local datum · front-left',{'M025':localnew},(0,0,1),colors={'M025':'#e8e1d5'},limits=[35,145,0,180],edges=[{'lines':line_wire(localold),'color':'#b44428','width':2,'style':'--'},{'lines':line_wire(localnew),'color':'#213e49','width':1.3}])],'Dashed: superseded horned contour. Solid: clean current open-edge contour. No forward bridge, finger or peninsula remains.',['Orange dashed: historical horn','Dark solid: V33.6.1'])
body={n:s for n,s in new.items() if n.startswith(('LeafButton','LeafNut','ButtonBody')) and n.endswith('_L')}
bodygap=min(r['nearest']['playfield_base']['distance_mm'] for r in meta['rows'] if r['role'] in ['occupied_button','occupied_nut','body_service'])
add('07','Button body / nut clearance',[panel('Front-left base and body reserves',{'BaseSection':slice(new['PF_BasePlywood'],1,0,280),**body},(1,-1,.65))],f'Exact native body/nut/service-reserve to base minimum: {bodygap:.3f} mm. Existing reference bore and pocket are not final machining dimensions. Fixed ergonomic centers remain Y89 / Y127.')
leaf={n:s for n,s in new.items() if n.startswith(('LeafBracket','LeafContacts','ButtonLeaf','ButtonWire','ButtonTool')) and n.endswith('_L')}
access={}
for role in ['palm','finger','driver']:
 path=O/'brep'/('Access_primary_L_'+role+'.brep');q=Part.Shape();q.read(str(path));access[role]=q
add('08','Leaf / wire / tool clearance and access',[panel('PLAY · reference clearance volumes',{'BaseSection':slice(new['PF_BasePlywood'],1,0,280),**leaf},(1,-1,.65)),panel('SERVICE50 · hand and driver approach',{'SideSection':slice(new['SIDE_L'],1,0,240),**body,**access},(1,-.3,.35),colors={'palm':'#79a6ad','finger':'#79a6ad','driver':'#496d84'},alpha={'palm':.35,'finger':.5,'driver':.4})],'Operational references pass the clean relief. Conservative hand/driver entry is checked with playfield at50° and main glass/matrix removed. Not a universal ergonomic qualification; final leaf hardware remains unselected.')
pf={n:s for n,s in actual(new).items() if n in pf_names(new)};context=sub(new,['SIDE_L','FLOOR','FRONT','SHELF_1','SHELF_2','SHELF_3','PF_OpenCradleL','PF_OpenCradleR'])
cables={}
for state in ['PLAY','SERVICE50','LIFT48']:
 path=O/'brep'/('CableLoop_'+state+'.brep');q=Part.Shape();q.read(str(path));cables[state]=q
add('09','Playfield PLAY — clean relief',[panel('Interior inspection · display envelope transparent',context|pf|buttonset(new)|{'FlexibleCableLoop':cables['PLAY']},(1,-2,1.3),alpha={'PLAYFIELD_ENVELOPE':.08})],'Restored front buttons and new open-edge clearance in the closed pose. VESA load region, wooden dowel, four saddle straps and eight strap screws remain in their accepted positions.')
p50=transform(pf,angle=-50,axis=PF)
add('10','Playfield 50° service',[panel('Main glass and matrix removed',context|p50|buttonset(new)|{'FlexibleCableLoop':cables['SERVICE50']},(1,-2,1.25),alpha={'PLAYFIELD_ENVELOPE':.12})],'Exact native rotation about the unchanged wooden-dowel axis. Continuous differential clearance certificates and whole-assembly samples check the corrected base and front-button reserves.')
lift={}
for n,s in pf.items():q=s.copy();q.translate(V(0,0,48));lift[n]=q
add('11','48 mm lift-out — cable route retained',[panel('Lifted base underside · display hidden for inspection',sub(new,['PF_OpenCradleL','PF_OpenCradleR','SHELF_3'])|{n:s for n,s in lift.items() if n!='PLAYFIELD_ENVELOPE'}|{'FlexibleCableLoop':cables['LIFT48']},(1,-1,-1))],'Full48 mm lift-out preserved. Flexible400 mm cable loop is a sampled packaging study; actual cable and clamp remain HOLD. Release the S3 clamp before removing that shelf.')
physical=actual(new);physical.update(select(new,'Plunger'))
for id,label,view in [('12','Player-left',(-1.5,-2,1.0)),('13','Player-right',(1.5,-2,1.0)),('14','Front oblique',(.65,-2,1.0))]:
 add(id,label+' — CURRENT V33.6.1',[panel('Front ergonomic buttons restored',physical,view,alpha={n:.12 for n in physical if n=='CandidateGlass' or 'Backglass' in n})],'Y89 / Y127, both65 mm below local side top. V33.6 monitor openings and backbox strain slots retained; M067, WPC, captured shell, SW01, shelves, glass and matrix unchanged. CNC release remains blocked.')
for s in scenes:
 for oldtxt,newtxt in [('in87','in 87'),('with2','with 2'),('Rear180','Rear 180'),('at50','at 50'),('Full48','Full 48'),('Flexible400','Flexible 400'),('both65','both 65')]:s['note']=s['note'].replace(oldtxt,newtxt)
(O/'review-scenes.json.gz').write_bytes(gzip.compress(json.dumps(scenes,separators=(',',':')).encode(),mtime=0))
print('V3361_REVIEW_SCENES_PASS',len(scenes),flush=True)
