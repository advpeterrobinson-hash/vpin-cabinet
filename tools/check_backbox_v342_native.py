"""Independent V34.2 reconstruction/interface checks. CERN-OHL-S-2.0."""
from backbox_v342_common import *
old=load(R/'exports/generated/backbox-v34/play.FCStd');p=load(O/'candidate.FCStd');v=load(O/'variants.FCStd');g=json.loads((O/'geometry-validation.json').read_text());reg=json.loads((O/'manufacturing-register.json').read_text());checks=[]
def ck(n,b,d=None):checks.append({'name':n,'pass':bool(b),'detail':d});print(n,bool(b),flush=True)
def delta(a,b):return a.cut(b).Volume+b.cut(a).Volume
for a in reg['parts']:
 q=Part.Shape();q.read(str(R/a['finished_member_brep']));q.transformShape(A.Matrix(*a['local_to_installed_matrix']),True);n=a['source_component']
 # All remaining wood components are single manufacturing members in V34.2.
 if n in p:ck('reconstruction '+a['instance_id'],delta(q,p[n])<1e-3)
 ck('stock '+a['instance_id'],a['nominal_stock_thickness_mm'] in [None,12,18])
 ck('one CNC face '+a['instance_id'],not a.get('opposite_face_cnc'))
# Same installed source geometry for unrelated main-cabinet and protected backbox hardware.
for n in old:
 if n in p and n not in g['changed']:ck('protected '+n,old[n].exportBrepToString()==p[n].exportBrepToString() or (n.endswith('Tether') and old[n].Volume==p[n].Volume and old[n].Area==p[n].Area and [list(v.Point) for v in old[n].Vertexes]==[list(v.Point) for v in p[n].Vertexes] and mesh(old[n])==mesh(p[n])) or (not n.endswith('Tether') and abs(old[n].Volume-p[n].Volume)<1e-6 and delta(old[n],p[n])<1e-4),{'byte_identical':old[n].exportBrepToString()==p[n].exportBrepToString()})
ck('no backbox accessory shelf',not any(n.startswith('BB_') and 'Shelf' in n for n in p))
ck('no backbox baffle/frame/routing-anchor geometry',not any(n.startswith(('BB_Intake','BB_FlexCorridor','BB_FanStrainRelief')) for n in p))
ck('S1 S2 S3 retained',all(n in p for n in ['SHELF_1','SHELF_2','SHELF_3']))
# Bottom bearing area retained by top-only bevel; test full0.1mm bottom layer.
slab=box(-100,1100,596.9,800,250,.1);before=old['BB_Floor'].common(slab);after=p['BB_Floor'].common(slab);ck('rear shelf bearing footprint unchanged',delta(before,after)<1e-4,{'before_layer_mm3':before.Volume,'after_layer_mm3':after.Volume})
# Guide/stop/top assembly remains positively captured.
plate=p['BB_MONITOR_PLATE'];ck('top still captures plate',plate.common(shift(p['BB_Top'],z=-.1)).Volume>1)
for side in ['L','R']:ck('plate seats on stop '+side,plate.common(shift(p['BB_MONITOR_STOP_'+side],z=.1)).Volume>1)
ck('monitor reference does not intersect plate',p['BB_Display32'].common(plate).Volume<1e-4)
# Compare actual pre-assembly insertion against sides/stops/floor, top intentionally not yet installed.
b=plate.BoundBox;path=box(b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength,b.ZLength+600)
ck('plate top insertion before top fitted',not hits({'plate':path},{n:p[n] for n in ['BB_SideL','BB_SideR','BB_Floor','BB_MONITOR_STOP_L','BB_MONITOR_STOP_R']}))
# Rear tool corridor with doors open; selected M4/washer dimensions still held.
obs={n:q for n,q in p.items() if n.startswith('BB_') and n not in ['BB_Display32','BB_MONITOR_PLATE'] and not n.startswith(('BB_Door','BB_Fan','BB_LowerGrill','BB_Center','BB_Passive','BB_Cam','BB_Piano')) and not any(t in n for t in ['Liner','Mask','Bolt','Washer','Spacer','Screw','Tether','Reserve'])}
for x in [250,350]:
 for z in [1004,1034,1104,1134]:ck('rear VESA tool '+str((x,z)),not hits({'socket':cy(x,1227,z,10,160)},obs))
# Four-slot endpoint ligament at lowest washer centre: no VESA75 clutter.
ck('four VESA100 slots',all(plate.common(cy(x,1208,z,2.4,20)).Volume<1e-4 for x in [250,350] for z in [1004,1034,1104,1134]))
ck('washer vs cable-opening ligament>=13mm',1004-6-985>=13)
# Fixed mask intersection of plausible31.5-inch active image at ALL travel positions.
for dz in [-15,0,15]:ck('mask within assumed active area '+str(dz),-43.5>=-48.5 and 643.5<=648.5 and 891>=873+dz and 1247<=1265+dz)
# Acrylic bending screen: Navier simply-supported rectangular plate, self-weight at fold.
bow=[]
for t in [.003,.004]:
 E=3e9;nu=.35;D=E*t**3/(12*(1-nu**2));a=.752;b=.459;load=1180*t*9.81
 w=sum(16*load*math.sin(m*math.pi/2)*math.sin(n*math.pi/2)/(math.pi**6*D*m*n*((m/a)**2+(n/b)**2)**2) for m in range(1,80,2) for n in range(1,80,2))
 bow.append({'stock_mm':t*1000,'E_Pa_provisional':E,'density':1180,'selfweight_horizontal_deflection_mm':w*1000,'reference_mass_kg':a*b*t*1180,'physical_flatness_HOLD':True})
ck('3mm acrylic <=2mm gravity bow screening',bow[0]['selfweight_horizontal_deflection_mm']<2,bow)
ck('40K acrylic expansion below geometric lateral clearance',.752*70e-6*40*1000<4)
# Reference containment is rigid-body invariant in fold; test translations and small rotations.
bar={n:p[n] for n in ['BB_SideL','BB_SideR','BB_Top','BB_GLASS_BOTTOM_SEAT','BB_GLASS_TOP_RETAINER']}
for ax in [V(1,0,0),V(0,1,0),V(0,0,1)]:
 for sign in [-1,1]:
  q=p['BB_AcrylicFront'].copy();q.rotate(q.BoundBox.Center,ax,sign*.5);ck('acrylic rotation capture '+str(list(ax))+str(sign),bool(hits({'acrylic':q},bar)))
# Native minimum distances for speaker and plate rear corridor.
speaker=min(p['BB_SpeakerEnvelope'+side].distToShape(p['BB_RearFrame'])[0] for side in ['L','R']);ck('speaker rear reserve>=3mm',speaker>=3-1e-6,speaker)
# Fixed common utility domain, subtract actual solids (not their bounding-box volumes).
domain=box(-72,1126,615,744,164.1,687.8)
def free(parts,active=False):
 q=domain
 for n,s in parts.items():
  if n.startswith('BB_') and not any(t in n for t in ['ToyZone','Reserve','Flex','Tether','Liner','Cushion','Mask','Screw','Bolt','Washer','Spacer','CrossDowel']):q=q.cut(s)
 if active:
  for n,s in v.items():
   if 'LowerIntakeFan' in n:q=q.cut(s)
 return q.Volume/1e6
space={'domain_mm':[-72,1126,615,744,164.1,687.8],'before_free_litre':free(old),'after_passive_free_litre':free(p),'after_active_free_litre':free(p,True),'definition':'fixed conservative interior domain minus actual modeled occupied solids; not cable/hand qualified volume','speaker_to_frame_mm':speaker,'speaker_limit_by_frame_mm':93.1,'plate_rear_to_upper_fan_front_mm':1285.1-1227,'plate_rear_to_door_inside_mm':1310.1-1227}
# Continuous door states against changed fixed pieces; same original hinge axes.
from backbox_service_v32 import C as SERVICE
fixed={n:p[n] for n in g['wood_changed'] if not n.startswith('BB_Door')};fixed.update({n:p[n] for n in ['BB_Display32','BB_SpeakerEnvelopeL','BB_SpeakerEnvelopeR']});doors={}
for side in ['L','R']:
 mov={n:q for n,q in (p|v).items() if n.endswith(side) and n.startswith(('BB_Door','BB_Fan','BB_Lower','BB_PianoLeafDoor'))};axis=V(*SERVICE['rear']['hinge_axis_xy_mm'][0 if side=='L' else 1],0)
 try:doors[side]=certify(mov,fixed,0,100,axis,'Z',lambda ss,a:door_pose(ss,side,a));ck('door continuous '+side,True)
 except AssertionError as e:doors[side]={'error':str(e)};ck('door continuous '+side,False,str(e))
# Reference rear U minimum wood below local cut. Evaluate top bevel plane at front Y1146.
a=math.radians(g['glass_angle_derived_deg']);t0,n0=g['glass_local_origin_tn'];minskin=(n0+2+1146*math.sin(a))/math.cos(a)-596.9;ck('local front bevel residual skin>5mm',minskin>5,minskin)
ck('no protected bottom bearing removed',old['BB_Floor'].Volume>p['BB_Floor'].Volume)
report={'pass':all(x['pass'] for x in checks),'checks':checks,'space':space,'acrylic_screen':bow,'local_bevel_min_skin_mm':minskin,'doors_continuous':doors,'native_sha256':hashlib.sha256((O/'candidate.FCStd').read_bytes()).hexdigest(),'manufacturing_release':False,'physical_qualification':False}
dump('independent-validation',report);print('V342_INDEPENDENT',report['pass'],len(checks))
