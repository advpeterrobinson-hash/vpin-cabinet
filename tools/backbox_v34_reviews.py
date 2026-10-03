"""26 original V34 CAD views. CERN-OHL-S-2.0. No vendor geometry."""
from pathlib import Path
import sys,json,gzip
import FreeCAD as A,Part,MeshPart
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,V,transform,WPC,actual
from backbox_service_v32 import door_pose
O=R/'exports/generated/backbox-v34';g=json.loads((O/'geometry-validation.json').read_text());assert g['pass']
p=load(O/'candidate.FCStd');old=load(R/'exports/generated/service-productization-v338/play.FCStd');hw=load(O/'study-hardware.FCStd');scenes=[]
def select(d,ns):return {n:d[n] for n in ns if n in d}
def shift(s,x=0,y=0,z=0):q=s.copy();q.translate(V(x,y,z));return q
def color(n):
 if 'PLATE' in n:return '#a78559'
 if 'STOP' in n:return '#c58c4a'
 if 'Tool' in n:return '#5aa3ad'
 if any(t in n for t in ['Bolt','Screw','Washer','Spacer','Dowel']):return '#738995'
 if any(t in n for t in ['Glass','Backglass']):return '#9dcbd4'
 if any(t in n for t in ['Display','Envelope']):return '#3c5868'
 if 'Side' in n:return '#c4ae82'
 return '#c9b88f'
def panel(label,d,view=(1,-2,1),alpha=None):
 ms=[]
 for n,s in d.items():
  if s.isNull():continue
  m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.6,AngularDeflection=.6,Relative=False);v,f=m.Topology
  if f:ms.append({'name':n,'vertices':[list(a) for a in v],'faces':f,'color':color(n),'alpha':(alpha or {}).get(n,1)})
 return {'label':label,'meshes':ms,'view':view}
def add(i,title,parts,note,view=(1,-2,1),alpha=None,extra=None):scenes.append({'id':f'{i:02d}','title':title,'note':note,'panels':[panel(title,parts,view,alpha)]+(extra or [])})
sides=select(p,['BB_SideL','BB_SideR']);stops=select(p,['BB_MONITOR_STOP_L','BB_MONITOR_STOP_R']);shell=sides|select(p,['BB_Floor','BB_Top']);plate=select(p,['BB_MONITOR_PLATE']);mon=select(p,['BB_Display32']);lower=select(p,['BB_DMD_SPEAKER_PANEL']);dmd=select(p,['BB_DMDEnvelope']);speakers=select(p,['BB_SpeakerEnvelopeL','BB_SpeakerEnvelopeR']);glass=select(p,['BB_Backglass']);glassparts={n:s for n,s in p.items() if n.startswith('BB_') and ('Glass' in n or n in ['BB_Backglass','BB_GLASS_BOTTOM_SEAT','BB_GLASS_TOP_RETAINER'])};simple=shell|stops|plate
add(1,'Previous CURRENT backbox', {n:s for n,s in old.items() if n.startswith('BB_') and not any(t in n for t in ['ToyZone','Display32','Backglass','Door','Fan','Flex','Reserve'])},'Historical V33.8 reference. Monitor rails, shoes, adjustable stop rail and multi-piece lower cassette are audited for retirement.',(1,2,1))
add(2,'Simplified shell',shell,'780 mm width / 723.9 mm shell height / accepted side depth and WPC interface preserved. One-face inside guides and front rebates only.')
add(3,'Two stops on bare side panels',sides|stops|{n:s for n,s in hw.items() if 'STOP' in n},'Two identical 12 x 40 x 30 mm offcuts screwed directly to inside side faces. Stop top Z854; no adjusters.',(1,2,.7))
add(4,'Floor and sides squared',sides|stops|select(p,['BB_Floor']),'Dry fit floor capture; square before final fixation. Permanent monitor plate has not yet been inserted.')
add(5,'Monitor plate enters from ABOVE',sides|stops|select(p,['BB_Floor'])|{n:shift(s,z=280) for n,s in plate.items()},'Assembly-only insertion. 4 mm side captures; guide width = measured plate thickness + coupon clearance. Top absent.')
add(6,'Plate seated on both stops',sides|stops|plate,'Plate is one flat 18 mm part. 12 mm was screened first and exceeded the stated planning deflection criterion.',(1,2,.7))
add(7,'Top closes the guide exits',simple,'The top is permanently assembled after seating the plate. No extra plate-retention brackets. Plate is not routinely removed.')
add(8,'Top joint: direct mechanical fastening',select(p,['BB_Top','BB_SideL'])|{n:s for n,s in hw.items() if n.startswith(('BB_Top','TopTool'))},'Existing shallow captured interface + glue + four direct side screws. Four pocket screws studied as an alternative; exact Kreg geometry unknown, so none is fabricated or assumed.',(1,2,1))
add(9,'Monitor approaches from FRONT',simple|{n:shift(s,y=-250) for n,s in mon.items()},'Top and plate stay installed. Insert monitor at +5 mm entry height through 744 mm clear throat (740 mm reference width). Rear access installs VESA bolts.')
add(10,'Rear VESA tool approach',simple|mon|{n:s for n,s in hw.items() if n.startswith('VesaTool_100')},'R10 x160 mm socket/driver corridors checked with rear doors open. All thread, washer, boss depth and screw engagement data await purchased monitor.',(1,2,.6),{'BB_MONITOR_PLATE':.3})
add(11,'Vertical VESA adjustment',plate|mon,'75/100 mm patterns; 5 mm reference slot width +10 mm centre travel =15 mm overall slot. +/-5 mm monitor height. Exact width remains HOLD.',(0,1,0),{'BB_Display32':.2},[panel('Slots close-up',{'PlateCenter':p['BB_MONITOR_PLATE'].common(Part.makeBox(160,30,160,V(220,1235,989)))},(0,1,0))])
stacks={}
for i,d in enumerate([0,3,6,9,12]):
 x=50+i*60
 stacks['Plate'+str(d)]=Part.makeBox(35,18,35,V(x,1240,1040))
 if d:stacks['Spacer'+str(d)]=Part.makeCylinder(5,d,V(x+17.5,1240-d,1057.5),V(0,1,0))
add(12,'Hardware-only depth stacks: 0 /3 /6 /9 /12 mm',stacks,'No wooden depth shoes. Reference increments only. Screw length = plate + washer + spacer + selected engagement; must not bottom in VESA boss.',(1,-1,.8))
add(13,'Monitor installed',simple|mon|{n:s for n,s in hw.items() if n.startswith('BB_VESA')},'Monitor weight transfers via VESA plate to guides/stops and side shell. Fold normal-load screen is provisional; plywood properties and full load qualification remain required.')
add(14,'One DMD / speaker panel',lower,'One 18 mm panel; 12 mm failed the conservative folded-load deflection screen. Central region remains wood to receive rear-access VESA bolts. Display sits in FRONT, not behind a fascia cutout.',(0,-1,0))
add(15,'DMD fitted directly to panel',lower|dmd|{n:s for n,s in hw.items() if 'DMDVESA' in n},'VESA75 example, 400 x200 x45 mm body reserve. No rear plywood adapter. Actual monitor and VESA location must be selected before final machining.',(1,1,.5))
add(16,'Speakers fitted to SAME panel',lower|dmd|speakers,'Direct speaker mounting; reference diameter130 and <=60 mm rear depth. Old103 mm depth conflicts with protected intakes. Hardware-dependent, no universal speaker fit claim.',(1,1,.5))
add(17,'Completed lower panel enters from FRONT',shell|plate|stops|{n:shift(s,y=-210) for n,s in (lower|dmd|speakers).items()},'Four side-operated positive bolts into cross-dowels; no plywood cleat stacks. Side access and actual hardware qualification required.')
add(18,'Lower panel fixed',simple|lower|dmd|speakers|{n:s for n,s in hw.items() if n.startswith('BB_Panel')},'Side rebates locate front/rear. Four bolts prevent release in fold. Removable panel is independent of captured monitor plate.',(1,1,.6))
add(19,'Front glass rebates and padded lower seat',sides|select(p,['BB_GLASS_BOTTOM_SEAT'])|{n:s for n,s in glassparts.items() if 'Cushion' in n},'Inside FACE_A side cuts leave12 mm outside skin. Bottom seat is one18 mm part with 8 mm top groove;6 mm front capture lip; replaceable cushions prevent hard contact.',(1,-2,.8))
q=shift(p['BB_Backglass'],z=1);q.rotate(V(300,1116,841),V(1,0,0),10)
add(20,'Glass enters from FRONT',simple|lower|{'BB_Backglass':q}|select(p,['BB_GLASS_BOTTOM_SEAT']),'Lower edge into padded seat, then tilt glass rearward. Top remains fixed. Shown10-degree CAD path; keep upper strip off.',(1,-1,.5),{'BB_Backglass':.35})
add(21,'Glass seated',simple|lower|glassparts,'Nominal study glass752 x459 x4 mm; final size from opening, actual liner and fit. Earlier465 mm height is not the final cut authority.',(1,-2,.6),{'BB_Backglass':.3})
add(22,'One removable upper strip',select(p,['BB_Top','BB_Backglass','BB_GLASS_TOP_RETAINER'])|{n:s for n,s in hw.items() if 'GlassTop' in n},'12 mm stock strip, two upward screws from front/below. 8.2 mm overlap,3.8 mm top travel. Remove strip without removing shell top.',(1,-1,.8),{'BB_Backglass':.25})
add(23,'Laid-back glass retention',transform(shell|glassparts,angle=90,axis=WPC),'Bottom U lip, lateral/back side seats and upper strip provide geometric capture. No gravity-only or friction-only retention. Impact, liner compression and purchased fasteners remain physical holds.',(1,-2,-1),{'BB_Backglass':.35})
doors={n:s for n,s in p.items() if n.startswith(('BB_Door','BB_Fan','BB_Intake','BB_Center','BB_Cam','BB_Passive','BB_PianoLeafDoor'))}
opened={}
for side in ['L','R']:
 subset={n:s for n,s in doors.items() if n.endswith(side) or (side=='L' and n.startswith(('BB_Center','BB_Passive'))) or (side=='R' and n.startswith('BB_Cam'))};opened.update(door_pose(subset,side,100))
add(24,'Rear service, both doors open100 degrees',simple|mon|lower|dmd|speakers|opened,'Rear lock approach, VESA access, existing fans/intakes and door architecture preserved. New smaller speaker-depth envelope is explicit.',(1,2,.8))
f=load(O/'backbox-fold.FCStd');full={n:s for n,s in actual(f).items() if not n.startswith('BB_') and 'ToyZone' not in n};bbparts={n:s for n,s in p.items() if n.startswith('BB_') and not any(k in n for k in ['ToyZone','Reserve','Flex','Tether'])};full.update({n:s for n,s in f.items() if n in bbparts})
add(25,'Populated90-degree fold',full,'Main playfield glass/matrix removed; rear locks parked; doors closed/latched. New geometry has required-angle samples plus continuous differential collision certificate.',(1,-2,1))
expl={}
for n,s in (simple|mon|lower|dmd|speakers|glassparts).items():
 if 'Cushion' in n:continue
 dx=-100 if n=='BB_SideL' else 100 if n=='BB_SideR' else 0
 dy=-360 if n=='BB_Backglass' else -260 if n=='BB_GLASS_TOP_RETAINER' else -160 if n in lower|dmd|speakers else -80 if n=='BB_Display32' else 0
 dz=200 if n=='BB_Top' else 80 if n=='BB_MONITOR_PLATE' else 0
 expl[n]=shift(s,x=dx,y=dy,z=dz)
add(26,'Complete simplified exploded backbox',expl,'Semantic exploded positions only: sides /2 stops /1 plate /top /monitor; one lower panel /DMD /2 speakers; glass /one strip. No rail, shoe, M067 or cassette frame.')
(O/'review-scenes.json.gz').write_bytes(gzip.compress(json.dumps(scenes,separators=(',',':')).encode(),mtime=0));print('V34_REVIEWS_NATIVE',len(scenes))
