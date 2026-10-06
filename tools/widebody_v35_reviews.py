"""48 native CAD review scenes; original meshes, commercial envelopes explicitly provisional."""
from widebody_v35_common import *
p=load(O/'candidate.FCStd');v=load(O/'variants.FCStd');reg=json.loads((O/'manufacturing-register.json').read_text());nest=json.loads((O/'nesting.json').read_text());scenes=[]
woodnames={a['source_component'] for a in reg['parts']}
def pick(d,fun):return {n:q for n,q in d.items() if fun(n)}
def names(d,ns):return {n:d[n] for n in ns if n in d}
def color(n):
 if 'Negative' in n:return '#b64742'
 if 'Glass' in n or 'Acrylic' in n:return '#a7dce2'
 if any(t in n for t in ['Channel','Siderail','Receiver','Retainer','Plunger','LegPlate']):return '#6c7882'
 if any(t in n for t in ['ENVELOPE','LG42','Samsung','TCL','Display']):return '#294c69'
 if 'LED' in n:return '#dfaa36'
 if n.startswith('BB_'):return '#caa16a'
 return '#d9c99d'
def panel(d,view,label):return {'label':label,'view':view,'meshes':[{'name':n,**mesh(q),'color':color(n),'alpha':.28 if n=='CandidateGlass' else 1} for n,q in d.items()]}
def add(i,title,d,note='',view=(1,-2,1),extra=[]):scenes.append({'id':f'{i:02}','title':title,'note':note+' REFERENCE DESIGN STUDY — purchased hardware/physical qualification/CNC HOLD.','panels':[panel(d,view,title)]+extra})
def core(d):return pick(d,lambda n:n in woodnames or n in ['PLAYFIELD_ENVELOPE','CandidateGlass','CandidateGlassChannelL','CandidateGlassChannelR','PF_WoodDowel','CommercialSiderailL','CommercialSiderailR','PF_RearGlassChannel','PF_LockdownGlassRetainer','BB_Display32','BB_AcrylicFront','BB_AcrylicMask','BB_DMDEnvelope'] or n.startswith(('BB_SpeakerEnvelope','BB_LowerGrill')))
new=core(p);old=core(p0)
for i,title,view in [(1,'600 versus628.65 front',(0,-1,0)),(2,'Old/new rear',(0,1,0)),(3,'780mm backbox /75.675mm overhang',(0,-1,.15))]:add(i,title,new,'Old90mm; new75.675mm each side. Backbox shape unchanged.',view,[panel(old,view,'V34.2 — historical600mm')])
add(4,'Nominal592.65mm inside',names(p,['SIDE_L','SIDE_R','FLOOR','FRONT']),'18mm nominal stock;628.65 exact outside. Actual thickness controls joints.',(0,-1,.2))
stack=names(p,['SIDE_L','SIDE_R','CandidateGlass','CandidateGlassChannelL','CandidateGlassChannelR','CommercialSiderailL','CommercialSiderailR','PF_LockdownGlassRetainer','LockdownReceiverReference','PLAYFIELD_ENVELOPE'])
add(5,'Commercial A-17996 width screen',stack,'635mm catalog inside width;3.175mm nominal allowance per side before actual trims/finish. Profile/tab fit NOT verified.')
add(6,'A-16773-1 receiver packaging reserve',names(p,['FRONT','LockdownReceiverReference','PLAYFIELD_ENVELOPE','PF_LockdownGlassRetainer']),'520x42x25mm is a conservative study box, NOT vendor CAD. Actual lever/shaft/tab reach and screw access HOLD.')
add(7,'Commercial siderail termination study',names(p,['SIDE_L','CommercialSiderailL','BB_Floor','BB_DMD_SPEAKER_PANEL']),'Full1198.5625mm constant-profile reserve fails.1116.325mm trimmed reference fits;82.2375mm tail adaptation requires actual part review.',(1,0,0))
for i,title in [(8,'603.25mm standard glass width'),(9,'Channel / siderail / glass / high TV')]:
 sec=box(-10,480,300,W+20,2,200);add(i,title,{n:q.common(sec) for n,q in stack.items() if q.common(sec).Volume>.001},'5.30mm nominal edge engagement beyond each inside face, not production groove depth.',(0,-1,0))
add(10,'V34.2 exposed plastic-fin negative control',names(p0,['SIDE_L','CandidateGlassChannelL','CandidateGlass','PLAYFIELD_ENVELOPE']),'Historical11.17mm vertical exposed plastic top; not V35 authority.',(0,-1,.2))
add(11,'High / glass-parallel target',names(p,['PLAYFIELD_ENVELOPE','CandidateGlass','PF_BasePlywood','PF_RearGlassChannel']),'7.5mm normal gap; no structural-support height change. Thin reference TV classes, not any43-inch chassis.',(1,0,0))
add(12,'Sunken TV — rejected negative control',names(p,['CandidateGlass','SIDE_R'])|{'SunkenNegativeControl':v['SunkenNegativeControl']},'Extra50mm recess is a regression failure; never selected.',(1,-2,1))
for i,y,label in [(13,150,'FRONT'),(14,550,'CENTER'),(15,930,'REAR')]:
 slab=box(-10,y,200,W+20,2,500);parts=names(p,list(stack)+['PF_BasePlywood'])
 add(i,label+' glass/display gap7.5mm',{n:q.common(slab) for n,q in parts.items() if q.common(slab).Volume>.001},'Glass/display nominal angular difference0 degrees. Chassis-to-image/flatness/flex remains hardware/physical HOLD.',(0,-1,0))
add(16,'Standard1092.20mm glass length',names(p,['SIDE_R','CandidateGlass','PF_RearGlassChannel','PF_LockdownGlassRetainer','BB_Floor']),'Front offset20mm in glass coordinates. Body length stays1308.10.',(1,0,0))
add(17,'Fixed rear channel on existing shelf',names(p,['BACKBOX_BASE','PF_RearGlassChannel','CandidateGlass','BB_Floor']),'Local TOP reference seat in main rear shelf; horizontal BB_Floor unchanged. Actual channel anchorage/edge bearing HOLD.',(1,-2,1))
for i,n in [(18,'SIDE_L'),(19,'SIDE_R'),(20,'FLOOR'),(21,'FRONT'),(22,'REAR')]:add(i,n,pick(p,lambda a:a==n),'No scale. Feature-free span extensions preserve nominal stock/hole sizes; final hardware cuts held.')
add(23,'T1 / T2 / T3 lateral spans',pick(p,lambda n:n.startswith('CROSS_')),'Structural crossmembers; NOT closed playfield gravity supports.')
add(24,'S1 / S2 / S3 shelf spans',pick(p,lambda n:n.startswith(('SHELF_','SimpleShelf'))),'Widths extend with side-supported joints. Y/Z equipment stations unchanged.')
for i,n in [(25,'LG42C5'),(26,'Samsung43QN93D'),(27,'TCL40S5K')]:add(i,n+' portrait fit',names(p,['PF_BasePlywood','SIDE_R','CandidateGlass'])|{n:v[n]},'Width gaps26.325/16.875/42.825mm respectively. TCL77mm body FAILS depth; no success claim.')
add(28,'Optional LED / diffuser clearance only',names(p,['PLAYFIELD_ENVELOPE','SIDE_R','CandidateGlass'])|pick(v,lambda n:'LED' in n),'Optional10mm envelope, no structural purpose, no mandatory BOM/slots/wiring.')
add(29,'Side buttons / leaf access',pick(p,lambda n:n.startswith(('Leaf','Button','PF_Base','SIDE_'))),'Y89/Y127, local top−65. Left follows left side; right follows right side.')
add(30,'588.65mm wooden dowel and open cradles',pick(p,lambda n:n.startswith(('PF_Wood','PF_Open','PF_Commercial','PF_Strap','PF_Support'))),'Ø32 wood. Four straps/eight strap screws/six cradle screws. No metal pivot.')
add(31,'SW02 landing pair',pick(p,lambda n:n.startswith(('FrontLanding','PF_Base'))),'X72 /556.65,Y245.68x70x54 solid blocks. Existing support height/plane preserved.')
add(32,'Centered floor equipment',pick(p,lambda n:n in ['FLOOR','PC_BASE','PC_ENVELOPE'] or n.startswith(('FloorIntake','SSF_'))),'PC285mm base unchanged width; fans/subwoofer/BST recentered, exciters follow sides.')
add(33,'SW01 and commercial leg-bracket audit',pick(p,lambda n:n.startswith('CandidateLeg')),'Commercial01-11400-1 preferred. Current SW01 remains until actual bracket corner/bolt-stack fit is measured; shown plates are reference reserves.')
add(34,'Commercial shooter reference',pick(p,lambda n:n.startswith(('Plunger','PLUNGER')) or n=='FRONT'),'Standard purchased shooter primary; old reserve is not selected shooter CAD. No final drilling.')
add(35,'Matrix centered, size unchanged',pick(p,lambda n:n.startswith(('Matrix','MX_'))),'Rigid X placement only; matrix removal remains prerequisite for service/fold.')
add(36,'Underfront module retained',pick(p,lambda n:n.startswith('Underfront') or n=='FLOOR'),'Same removable160x116mm12mm plate, centered on314.325; programmable controls / final hardware held.')
add(37,'Backbox unchanged local geometry',pick(new,lambda n:n.startswith('BB_')),'780x723.9mm, same depth/internal construction. One common placement transform.')
add(38,'Main/backbox anchor relationships',names(p,['BACKBOX_BASE','BB_Floor','PF_OpenCradleL','PF_OpenCradleR'])|pick(p,lambda n:n.startswith('UprightLock'))|pick(v,lambda n:'WPC_' in n),'Shelf lock receivers recentered with backbox; side pivot X follows body. Physical hinge arm offset remains HOLD.')
for i,fn in [(39,'fold-45'),(40,'fold-90'),(41,'play'),(42,'service'),(43,'lift-out')]:add(i,fn.upper(),core(load(O/(fn+'.FCStd'))),'Service/fold: main glass +matrix removed; fold locks parked, doors shut. Raised playfield support NOT qualified.')
for i,t in [(44,'18'),(45,'12')]:
 d={};by={a['instance_id']:a for a in reg['parts']}
 for si,sh in enumerate(nest[t]['sheets']):
  for a in sh['parts']:
   q=Part.Shape();q.read(str(R/by[a['instance']]['finished_member_brep']))
   if a['rotated']:q.rotate(V(),V(0,0,1),90)
   b=q.BoundBox;q.translate(V(a['x']+si*2600-b.XMin,a['y']-b.YMin,-b.ZMin));d[a['instance']]=q
 add(i,t+'mm PRELIMINARY NOT FOR CNC',d,'20mm perimeter /15mm spacing. Conservative rectangle placement, actual contours shown; grain approval pending.',(0,0,1))
add(46,'Complete player-eye target',new,'HIGH parallel display. Commercial reference stack requires actual part fit confirmation.',(1,-3,1.8))
add(47,'Complete cabinet side',new,'1308.10mm length preserved; no silhouette scaling.',(1,0,0))
exp={}
for n,q in stack.items():
 dx=-70 if n.endswith('L') else 70 if n.endswith('R') else 0;dz=90 if n=='CandidateGlass' else 50 if 'Siderail' in n else 25 if 'Channel' in n else 0
 exp[n]=shift(q,x=dx,z=dz)
add(48,'Exploded commercial interface stack',exp,'Wood side / purchased channel / optional commercial siderail / tempered glass / high display. No added wooden side trim.')
(O/'review-scenes.json.gz').write_bytes(gzip.compress(json.dumps(scenes,separators=(',',':')).encode(),mtime=0));print('V35 native scenes',len(scenes))
