"""48 native CAD review scenes; original meshes, commercial envelopes explicitly provisional."""
from widebody_v351_common import *
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
def core(d):return pick(d,lambda n:n in woodnames or n in ['PLAYFIELD_ENVELOPE','CandidateGlass','CandidateGlassChannelL','CandidateGlassChannelR','PF_WoodDowel','PF_RearGlassChannel','PF_LockdownGlassRetainer','BB_Display32','BB_AcrylicFront','BB_AcrylicMask','BB_DMDEnvelope'] or n.startswith(('BB_SpeakerEnvelope','BB_LowerGrill')))
# Optional blank members are in the manufacturing register, not occupied PLAY.
for a in reg['parts']:
 if a['source_component'] not in p:
  q=Part.Shape();q.read(str(R/a['finished_member_brep']));q.transformShape(A.Matrix(*a['local_to_installed_matrix']),True);p[a['source_component']]=q
prior=load(R/'exports/generated/widebody-v35/candidate.FCStd');fix=load(O/'fixing-reserves.FCStd');audit=json.loads((O/'small-part-audit.json').read_text())
add(1,'CURRENT V34.2 — reference before promotion',core(p0),'600mm body; source11822cb. This view preserves source architecture.')
add(2,'Previous V35 — study only',core(prior),'628.65mm candidate; integral rail and receiver/rear fixing unresolved. Not CURRENT.')
front=names(p,['FRONT','SIDE_L','SIDE_R','PF_LockdownGlassRetainer','LockdownReceiverReference','CandidateGlass','CandidateGlassChannelL','CandidateGlassChannelR','PLAYFIELD_ENVELOPE'])
add(3,'Standard widebody front system',front,'628.65mm; commercial A-17996/A-16055 +A-16773-1 class.5mm locally cut tempered reference.')
add(4,'Purchased lockdown architecture',names(p,['FRONT','PF_LockdownGlassRetainer','CandidateGlass']),'No custom bar. Family selected; underside engagement/holes remain PURCHASE_BEFORE_CNC.')
add(5,'Receiver body, operation and hand/tool reserves',names(p,['FRONT','LockdownReceiverReference','ReceiverLatchReserve','ReceiverToolReserve','PF_BasePlywood'])|pick(p,lambda n:n.startswith('CoinStudy_Mechanism')),'520x42x40 body reserve; separate free space below and left hand approach. No precise latch trajectory invented.',(1,-2,1))
sec=box(310,-60,220,4,260,260);add(6,'Glass / lockdown / receiver front section',{n:q.common(sec) for n,q in front.items() if q.common(sec).Volume>.001},'Glass retained by purchased bar; receiver transfers latch reaction to front. Final profiles held.',(1,0,0))
add(7,'Fully functional cabinet WITHOUT siderails',core(p),'Polymer channels carry glass; no rail in minimum BOM.')
add(8,'Optional purchased siderail envelope',core(p)|names(p,['CommercialSiderailL','CommercialSiderailR']),'Optional reference stops before backbox. PURCHASED-PART MODIFICATION / VERIFY SKU if trimming is needed.')
rear=names(p,['BACKBOX_BASE','PF_RearGlassChannel','CandidateGlass','MatrixCarrier']);add(9,'Commercial rear channel — ordinary screws',rear,'Angled support follows measured glass plane; horizontal shelf/floor retained. No auxiliary wooden rail.')
add(10,'Rear-channel screw land and flush-head reserve',names(p,['BACKBOX_BASE','PF_RearGlassChannel'])|fix,'Two local integral R2 lands: test10mm edge margins /12mm embedment. Exact screw quantity and centers HOLD. Heads must stay below glass.',(1,-2,1))
for i,tt,fn,note in [(11,'Protected three crossmembers',lambda n:n.startswith(('CROSS_','CROSS_GUIDE')),'No deletion, merge or section reduction.'),(12,'Crossmember attachment and bearing',lambda n:n.startswith(('CROSS_','CROSS_GUIDE','CROSS_BRACKET')),'Guides locate and distribute reactions; supports remain discrete repairable parts.'),(13,'Protected three shelves',lambda n:n.startswith(('SHELF_','SHELF_SUPPORT')),'All three remain removable equipment supports.'),(14,'Separate shelf supports retained',lambda n:n.startswith('SHELF_SUPPORT'),'42x150mm backing avoids deeper side-panel routing.'),(15,'Shelf gravity path',lambda n:n.startswith(('SHELF_','SHELF_SUPPORT')) or n=='SIDE_R','Equipment → shelf → side supports → side structure. Not replaced by shallow tabs.'),(16,'M006 continuous floor supports',lambda n:n.startswith('FLOOR_CLEAT') or n=='FLOOR','Protected ledges, unchanged sections and load path.'),(17,'SW01 leg load path',lambda n:n.startswith('CandidateLeg') or n=='FRONT','Four solid blocks retained; no thin plywood substitute.'),(18,'SW02 closed playfield load path',lambda n:n.startswith('FrontLanding') or n=='PF_BasePlywood','Two solid blocks + rear dowel support the playfield; T1/T2/T3 do not carry its closed gravity load.'),(19,'Upright-lock parking pads retained',lambda n:n.startswith('BB_UprightLock') or n=='BB_Floor','Four pad laminations provide36mm local parking depth; independent locks unchanged.')]:add(i,tt,pick(p,fn),note)
shaft=Part.makeCylinder(4,28,V(199.325,1268,614.9),V(0,0,-1))
add(20,'Direct-floor parking — NOT selected',names(p,['BB_Floor','BACKBOX_BASE'])|{'NegativeParkingShaft':shaft},'Reference28mm parking depth in18mm floor protrudes into the bearing shelf. Keep36mm pads; final shaft/insert measured later.')
add(21,'Two replaceable monitor stops',names(p,['BB_SideL','BB_MONITOR_STOP_L','BB_MONITOR_PLATE']),'Measured bearing216mm² per stop. Separate screw-fixed offcut protects side and is replaceable.',(1,-2,.5))
alt=box(-61.675,1209,851,4,18,3);add(22,'Blind-guide stop alternative — rejected',names(p,['BB_SideL','BB_MONITOR_PLATE'])|{'NegativeIntegralStop':alt},'Only72mm² projected bearing with4mm capture; one third of retained stop. No piece-count-driven integration.',(1,-2,.5))
add(23,'Fan blanks — optional sealing function',names(p,['BB_DoorL','BB_DoorR','BB_FanBlankL','BB_FanBlankR']),'Retain optional12mm blank to seal an unused upper station; grille-only mode does not require it.')
add(24,'Acrylic seats and removable strip retained',names(p,['BB_AcrylicFront','BB_GLASS_BOTTOM_SEAT','BB_GLASS_TOP_RETAINER','BB_SideL','BB_SideR']),'Continuous padded lower support and one positive top strip; front service remains simple.')
add(25,'Hinge cleats retained',names(p,['BB_HingeCleatL','BB_HingeCleatR','BB_RearFrame','BB_DoorL']),'Retain bearing/alignment and screw engagement; do not attach hinge to a poor edge.')
small={};by={a['instance_id']:a for a in reg['parts']}
for i,a in enumerate(audit):
 r=by[a['instance']];q=Part.Shape();q.read(str(R/r['finished_member_brep']));b=q.BoundBox;q.translate(V((i%6)*700-b.XMin,(i//6)*220-b.YMin,-b.ZMin));small[a['ID']+'_'+a['name']]=q
add(26,'All33 small wood members',small,'Actual manufacturing members. Small means outer area<20000mm² OR maximum dimension<150mm; no automatic deletion.',(0,0,1))
add(27,'KEEP map — no target part count',small,'33/33 small members KEEP. Separate supports and replaceable locators have structural/service value; no unjustified deletion.',(0,0,1))
exp={}
for a in reg['parts']:
 n=a['source_component'];q=p[n];dx=-100 if n.endswith('L') else 100 if n.endswith('R') else 0;dz=300 if n.startswith('BB_') else 150 if n.startswith('SHELF') else 80 if n.startswith(('CROSS','PF_')) else 0
 exp[n]=shift(q,x=dx,z=dz)
add(28,'Refined exploded wood architecture',exp,'66 pieces retained. One local rear-shelf machining refinement; no additional rail or mechanism.')
add(29,'Assembly complexity —59 steps retained',core(p),'Same retained support sequence and dry-fit datums. Existing glass-interface step updated, no new mechanism.',extra=[panel(core(p0),(1,-2,1),'Before:59 steps /66wood')])
for i,t in [(30,'18'),(31,'12')]:
 d={}
 for si,sh in enumerate(nest[t]['sheets']):
  for a in sh['parts']:
   q=Part.Shape();q.read(str(R/by[a['instance']]['finished_member_brep']))
   if a['rotated']:q.rotate(V(),V(0,0,1),90)
   b=q.BoundBox;q.translate(V(a['x']+si*2600-b.XMin,a['y']-b.YMin,-b.ZMin));d[a['instance']]=q
 add(i,t+'mm preliminary nesting',d,'MaxRects deterministic search, long-axis grain alignment;20mm border /15mm spacing. NOT FOR CNC.',(0,0,1))
add(32,'Complete V35.1 standard-widebody candidate',core(p),'No mandatory siderail; high parallel playfield; simplified backbox unchanged locally. Purchased fit and CNC remain held.',(1,-3,1.8))
(O/'review-scenes.json.gz').write_bytes(gzip.compress(json.dumps(scenes,separators=(',',':')).encode(),mtime=0));print('V351_SCENES',len(scenes))
