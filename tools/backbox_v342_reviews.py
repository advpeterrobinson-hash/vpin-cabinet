"""Thirty native CAD review scenes, independent original geometry. CERN-OHL-S-2.0."""
from backbox_v342_common import *
p=load(O/'candidate.FCStd');old=load(R/'exports/generated/backbox-v34/play.FCStd');v=load(O/'variants.FCStd');G=json.loads((O/'geometry-validation.json').read_text());assert G['pass'];scenes=[]
def pick(d,fn):return {n:s for n,s in d.items() if fn(n)}
def names(d,ns):return {n:d[n] for n in ns if n in d}
def col(n):
 if 'Mask' in n:return '#171a1c'
 if 'ActiveImage' in n:return '#47919e'
 if 'Backglass' in n or 'Acrylic' in n or 'Glass' in n and not n.startswith('BB_GLASS'):return '#b0cdd5'
 if any(t in n for t in ['Fan','Grill','Channel','Bolt','Screw']):return '#71828d'
 if 'Display' in n or 'SpeakerEnvelope' in n or 'DMDEnvelope' in n:return '#364f66'
 if 'MONITOR_PLATE' in n:return '#b1814e'
 return '#c7b88e'
def panel(d,view=(1,-2,1),label='',alpha={}):return {'label':label,'view':view,'meshes':[{'name':n,**mesh(s),'color':col(n),'alpha':alpha.get(n,1)} for n,s in d.items()]}
def add(i,title,d,note,view=(1,-2,1),extras=[]):scenes.append({'id':f'{i:02d}','title':title,'note':note,'panels':[panel(d,view,title,{'BB_AcrylicFront':.2,'BB_Backglass':.2,'CandidateGlass':.3})]+extras})
bbnew=pick(p,lambda n:n.startswith('BB_') and not any(t in n for t in ['Reserve','Tether','Bolt','Screw','Washer','Spacer','Liner','CrossDowel']))
front=pick(bbnew,lambda n:not any(t in n for t in ['Door','RearFrame','Piano','Fan','Grill','Cam','Passive','Center']))
shell=names(p,['BB_SideL','BB_SideR','BB_Floor','BB_Top','BB_MONITOR_PLATE','BB_MONITOR_STOP_L','BB_MONITOR_STOP_R','BB_DMD_SPEAKER_PANEL'])
add(1,'CURRENT V34 front — historical',pick(old,lambda n:n.startswith('BB_') and not any(t in n for t in ['Reserve','Toy','Fan','Door','Tether'])),'Before:4mm glass, +/-5mm monitor slots and lower intake filter/baffle assemblies.')
add(2,'V34.2 front — acrylic and rear black mask',front,'One captured plate; one DMD/speaker panel.3mm acrylic reference, rear painted mask. Final screen/boss/mask dimensions HOLD.')
for i,dz in [(3,0),(4,-15),(5,15)]:
 q=dict(front);q['BB_Display32']=shift(p['BB_Display32'],z=dz);q['ActiveImage_reference']=box(-48.5,1131.9,873+dz,697,.1,392)
 add(i,'TCL-like '+('LOW -15mm' if dz<0 else 'HIGH +15mm' if dz>0 else 'NOMINAL'),q,'Published715x422x75mm,3.15kg,VESA100. Boss65mm and active697x392mm are sensitivity assumptions, not manufacturer drawings. Fixed687x356 mask crops image to cover full30mm adjustment.',(0,-1,0))
add(6,'Four primary VESA100 long slots',names(p,['BB_MONITOR_PLATE']), 'Slot length = reference5mm bolt clearance +30mm travel =35mm. Final width HOLD. VESA75 retired from minimum plate.',(0,1,0))
for i,dep,boss in [(7,75,65),(8,80,70)]:
 fronty=1209-12-boss;body=box(-57.5,fronty,858,715,boss,422).fuse(box(-57.5,fronty,858,715,dep,125));q=names(p,['BB_MONITOR_PLATE','BB_AcrylicFront']);q['TVBody_reference']=body;q['VESA_boss_reference']=box(240,1197,1010,120,.5,120);q['Spacer12mm_reference']=box(290,1197,1008,10,12,10);q['ConnectorReserve']=v['BB_ConnectorReserve']
 add(i,'Depth section '+str(dep)+'mm body / '+str(boss)+'mm boss',q,'Fixed plate FRONT Y1209;12mm spacers.75/65 and80/70 pass;80/55 fails because lower body intersects plate. Actual TV boss offsets, connectors and engaged screw length remain HOLD.',(1,0,0))
add(9,'Acrylic purchased sheet',names(p,['BB_AcrylicFront']),'752x459x3mm planning sheet. Compare4mm in report. Actual thickness/flatness, thermal clearance and final cut pending.',(0,-1,0))
add(10,'Rear-face black mask',names(p,['BB_AcrylicFront','BB_AcrylicMask']),'Clear687x356mm reference aperture. Mask on rear; no wooden bezel. Full +/-15mm needs image cropping; alternative final mask after actual alignment remains builder choice.',(0,-1,0))
ac=names(p,['BB_AcrylicFront','BB_GLASS_BOTTOM_SEAT','BB_GLASS_TOP_RETAINER','BB_SideL','BB_SideR'])
add(11,'Acrylic in padded channel seats',ac,'Reuse simple front rebates / lower U / one upper strip.3mm sheet supported in8mm reference lower seat by selected commodity liner; no gravity-only retention.')
q=shift(p['BB_AcrylicFront'],z=1);q.rotate(V(300,1116,841),V(1,0,0),10);q.translate(V(0,-120,6))
add(12,'Front acrylic service',shell|{'BB_AcrylicFront':q},'Strip off; lift1mm, tilt10deg, lift6mm, withdraw FRONT. Shell top and captured plate remain. Actual flexible sheet handling/flatness qualification pending.')
add(13,'Retired lower intake complexity',pick(old,lambda n:n.startswith(('BB_Intake','BB_Door'))),'Historical only:2 filter frames +8 baffle manufacturing pieces retired.',(1,-2,1))
rear=pick(bbnew,lambda n:n.startswith(('BB_Door','BB_Fan','BB_LowerGrill','BB_RearFrame','BB_Piano')))
add(14,'Two lower passive stations',rear,'TwoØ116 openings,105mm mounting pitch, ordinary commodity120mm grilles. Exact purchased finger-safe grille and fixing profile HOLD.',(1,2,1))
add(15,'Optional 2 intake +2 exhaust',rear|pick(v,lambda n:'LowerIntakeFan' in n),'No recutting for active mode. Fan bodies120x120x25mm; F67 replaces shorter F66 passive screws. Thermal qualification PENDING.',(1,2,1))
openrear=names(p,['BB_RearFrame','BB_MONITOR_PLATE','BB_DMD_SPEAKER_PANEL'])
for side in ['L','R']:openrear.update(door_pose(pick(p|v,lambda n:n.endswith(side) and n.startswith(('BB_Door','BB_Fan','BB_Lower','BB_PianoLeafDoor'))),side,100))
add(16,'Rear doors100deg / fan packaging',openrear,'Passive/active door sweeps tested. No universal service-loop anchors; builder routes selected flexible fan lead through open volume.',(1,2,1))
low=names(p,['BB_DMD_SPEAKER_PANEL','BB_DMDEnvelope','BB_SpeakerEnvelopeL','BB_SpeakerEnvelopeR','BB_RearFrame'])
add(17,'One lower panel, baffles removed',low,'Direct DMD and two speakers. No cassette, separate baffles or electronics shelves.',(1,2,1))
add(18,'Speaker depth90mm reference',low|pick(v,lambda n:'LowerIntakeFan' in n),'Prior60mm grows to90mm. Rear-frame contact at93.1mm limits reference;3.1mm nominal residual. Actual speaker magnet/body and screws HOLD.',(1,0,0))
add(19,'Open backbox utility space — no shelves',shell|names(p,['BB_RearFrame']),'No current backbox universal accessory shelves or shelf supports existed;0 retained/added. S1/S2/S3 main cabinet untouched.',(1,2,1))
add(20,'Only essential cable passages',names(p,['BB_MONITOR_PLATE','BB_DMD_SPEAKER_PANEL','BB_Floor']),'One monitor hand/connector opening, one covered DMD cable opening, one common main/backbox passage. Projected fan anchor/loop features retired.',(1,2,1))
add(21,'Main cabinet to backbox passage',names(p,['BB_Floor','BACKBOX_BASE','BB_DMD_SPEAKER_PANEL']),'Common generic cable passage preserved. No connector count, disconnect method or universal cable-management feature.',(1,-2,1))
gl=names(p,['CandidateGlass','CandidateGlassChannelL','CandidateGlassChannelR','BB_PFRearChannel','PF_LockdownGlassRetainer'])
section=Part.makeBox(35,5,300,V(0,300,350))
add(22,'Side plastic U-channel section',{n:s.common(section) for n,s in gl.items() if s.common(section).Volume>1e-5},'5mm nominal tempered glass,0.5mm side clearance; plastic channel separates wood/glass. Actual commodity profile and mounting/thermal fit HOLD.',(0,1,0))
add(23,'Front lockdown interface',names(p,['CandidateGlass','PF_LockdownGlassRetainer','CandidateGlassChannelL','CandidateGlassChannelR','FRONT']),'Only lockdown retains front. Shown containment envelope is not a selected bar/latch. Release bar and slide toward PLAYER; no extra front clamps.',(1,-2,1))
clip=box(40,1120,590,10,85,45)
rearsection={n:q.common(clip) for n,q in names(p,['BB_Floor','BB_PFRearChannel','CandidateGlass']).items() if q.common(clip).Volume>1e-5}
add(24,'Local angled rear glass seat — X40 section',rearsection,'Measured channel/glass plane9.90666925365deg. Local top rebate only; no BB_Floor tilt. Floor skin/bearing and one-face variable-depth cutter finish remain coupon-qualified.',(1,0,0))
add(25,'Complete glass support / containment',gl,'Unchanged continuous1100mm side profiles;42mm rear transition to new rear U avoids moving backbox/fixed-rail interference. Reference glass575x1142x5; final cut HOLD.',(1,-2,1))
a=math.radians(G['glass_angle_derived_deg']);q=shift(p['CandidateGlass'],y=-650*math.cos(a),z=-650*math.sin(a));add(26,'Glass removal toward player',names(p,['CandidateGlassChannelL','CandidateGlassChannelR','BB_PFRearChannel'])|{'CandidateGlass':q},'Lockdown released. Exact forward translation sweep tested; rear U and side channels stay installed. No backbox disassembly.')
fold=transform(pick(bbnew,lambda n:True),angle=90,axis=WPC);add(27,'Backbox fold — main glass removed',fold|names(p,['SIDE_L','SIDE_R','CandidateGlassChannelL','CandidateGlassChannelR']),'Main tempered glass and matrix removed; rear doors closed/latched; upright locks released/parked. Acrylic and lower panel remain installed.')
expl={}
for n,q in front.items():
 if 'Liner' in n:continue
 expl[n]=shift(q,x=-100 if n=='BB_SideL' else 100 if n=='BB_SideR' else 0,y=-260 if n in ['BB_AcrylicFront','BB_AcrylicMask'] else -140 if n.startswith(('BB_DMD','BB_Speaker')) else 0,z=150 if n=='BB_Top' else 50 if n=='BB_MONITOR_PLATE' else 0)
add(28,'Simplified exploded backbox',expl,'One plate,2 stops,one lower panel,one acrylic sheet/upper strip. Lower fans mount straight to doors. No accessory shelves, duct panels or cable rack.')
add(29,'Complete populated backbox',bbnew|pick(v,lambda n:'LowerIntakeFan' in n),'TCL-like depth case and selected nominal positions. Purchased boss location/connector access, grills, speakers and physical retention are HOLD.')
add(30,'76 to66 wood pieces;45 unique families',shell,'10 CNC pieces removed:2 filter frames +8 baffle members. Duplicate M074 corrected: monitor plate is M078; underfront remains M074. No piece added. Nominal wood61.182kg versus61.923kg; acrylic/electronics separate.')
(O/'review-scenes.json.gz').write_bytes(gzip.compress(json.dumps(scenes,separators=(',',':')).encode(),mtime=0));print('V342_REVIEWS',len(scenes))
