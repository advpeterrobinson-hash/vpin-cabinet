import FreeCAD as A, Part, math, json, os
OUT=os.path.dirname(os.path.abspath(__file__))
d=A.newDocument('VPinV32'); records=[]; shapes={}
PART_CODES={
'SIDE_L':'SideL','SIDE_R':'SideR','FRONT':'Front','REAR':'Rear','REAR_DOOR':'RearDoor','FLOOR':'Floor',
'SHELF_1':'S1','SHELF_SUPPORT_1L':'S1SupL','SHELF_SUPPORT_1R':'S1SupR',
'SHELF_2':'S2','SHELF_SUPPORT_2L':'S2SupL','SHELF_SUPPORT_2R':'S2SupR',
'SHELF_3':'S3','SHELF_SUPPORT_3L':'S3SupL','SHELF_SUPPORT_3R':'S3SupR',
'CROSS_1':'T1','CROSS_GUIDE_1L':'T1GuideL','CROSS_GUIDE_1R':'T1GuideR',
'CROSS_2':'T2','CROSS_GUIDE_2L':'T2GuideL','CROSS_GUIDE_2R':'T2GuideR',
'CROSS_3':'T3','CROSS_GUIDE_3L':'T3GuideL','CROSS_GUIDE_3R':'T3GuideR',
'MONITOR_RAIL_L':'MonRailL','MONITOR_RAIL_R':'MonRailR','MONITOR_BRIDGE':'MonBridge',
'PC_BASE':'PCBase','BACKBOX_BASE':'BBBase'}
NAMES_EN={
'SIDE_L':'Left side','SIDE_R':'Right side','FRONT':'Front panel','REAR':'Rear panel',
'REAR_DOOR':'Rear service door','FLOOR':'Bottom panel','PC_BASE':'PC base','PC_ENVELOPE':'PC envelope',
'BACKBOX_BASE':'Backbox support','PLAYFIELD_ENVELOPE':'Display envelope','MONITOR_BRIDGE':'VESA bridge',
'AUDIO_STARTECH':'Sound card','PLUNGER_RESERVED':'Plunger reserve','MAINS_RESERVED':'Mains inlet reserve',
'RJ45_RESERVED':'Network reserve'}
NAMES_PTBR={
'SIDE_L':'Lateral esquerda','SIDE_R':'Lateral direita','FRONT':'Painel frontal','REAR':'Painel traseiro',
'REAR_DOOR':'Porta traseira de serviço','FLOOR':'Piso','PC_BASE':'Base do PC','PC_ENVELOPE':'Envelope do PC',
'BACKBOX_BASE':'Base/apoio do backbox','PLAYFIELD_ENVELOPE':'Envelope do display','MONITOR_BRIDGE':'Ponte VESA',
'AUDIO_STARTECH':'Placa de som','PLUNGER_RESERVED':'Reserva do plunger','MAINS_RESERVED':'Reserva da entrada elétrica',
'RJ45_RESERVED':'Reserva de rede'}
PREFIX_NAMES=[
 ('SHELF_SUPPORT_','Shelf support','Apoio da prateleira'),
 ('SHELF_','Transverse shelf','Prateleira transversal'),
 ('CROSS_GUIDE_','Grooved guide','Guia ranhurada'),
 ('CROSS_BRACKET_','Support angle','Cantoneira de apoio'),
 ('CROSS_','Upright crossmember','Travessa vertical'),
 ('MONITOR_RAIL_','Monitor rail','Régua do monitor'),
 ('FLOOR_CLEAT_','Floor support','Apoio do piso'),
 ('FAN_','Rear exhaust fan','Ventoinha traseira')]
def localized_name(n,lang='en'):
 table=NAMES_EN if lang=='en' else NAMES_PTBR
 if n in table:return table[n]
 for prefix,en,pt in PREFIX_NAMES:
  if n.startswith(prefix):return (en if lang=='en' else pt)+' '+n[len(prefix):]
 return n
def name_en(n):return localized_name(n,'en')
def name_ptbr(n):return localized_name(n,'pt')


W=600.;L=1308.1;H=400.05;HR=596.9;R=1127.125;t=18.
def box(x,y,z,dx,dy,dz):return Part.makeBox(dx,dy,dz,A.Vector(x,y,z))
def cyl(x,y,z,r,length,axis=(0,0,1)):return Part.makeCylinder(r,length,A.Vector(x,y,z),A.Vector(*axis))
def add(n,s,kind,note=''):
 assert s.isValid() and len(s.Solids)==1,n
 code=PART_CODES.get(n,'')
 en=name_en(n);pt=name_ptbr(n)
 o=d.addObject('PartDesign::Feature',n);o.Shape=s
 o.Label=((code+' - ') if code else '**PROVISIONAL** - ')+en
 o.addProperty('App::PropertyString','PartCode');o.PartCode=code
 o.addProperty('App::PropertyString','LegacyId');o.LegacyId=n
 o.addProperty('App::PropertyString','PartStatus');o.PartStatus='PERMANENT_CODE' if code else 'PROVISIONAL'
 o.addProperty('App::PropertyString','NameEN');o.NameEN=en
 o.addProperty('App::PropertyString','NamePTBR');o.NamePTBR=pt
 o.addProperty('App::PropertyString','Purpose');o.Purpose=note
 o.addProperty('App::PropertyString','Category');o.Category=kind
 shapes[n]=s
 verts,faces=s.tessellate(1.5)
 records.append(dict(id=n,part_code=code,part_status=('PERMANENT_CODE' if code else 'PROVISIONAL'),name_en=en,name_pt_br=pt,kind=kind,note=note,vertices=[[v.x,v.y,v.z] for v in verts],faces=faces,volume=s.Volume,bounds=[s.BoundBox.XMin,s.BoundBox.XMax,s.BoundBox.YMin,s.BoundBox.YMax,s.BoundBox.ZMin,s.BoundBox.ZMax]))
 return o
alpha=math.atan2(HR-H,R);bz=H+45*math.tan(alpha)-12-55*math.cos(alpha)
def tf(s):
 s=s.copy();s.rotate(A.Vector(),A.Vector(1,0,0),math.degrees(alpha));s.translate(A.Vector(0,45,bz));return s
# Cabinet shell: conventional butt joints; bottom on simple cleats. No invented joints.
for name,x in [('SIDE_L',0),('SIDE_R',582)]:
 pts=[A.Vector(x,0,0),A.Vector(x,L,0),A.Vector(x,L,HR),A.Vector(x,R,HR),A.Vector(x,0,H),A.Vector(x,0,0)]
 s=Part.Face(Part.makePolygon(pts)).extrude(A.Vector(t,0,0))
 for y in (255,310):
  s=s.cut(cyl(x-1,y,270,7.9375,20,(1,0,0)))
  outer=x if x==0 else x+18-7.9375
  inner=x+18-4.7625 if x==0 else x
  s=s.cut(cyl(outer,y,270,14.2875,7.9375,(1,0,0))).cut(cyl(inner,y,270,14.2875,4.7625,(1,0,0)))
 s=s.cut(cyl(x-1,1270,508,6.35,20,(1,0,0)))
 add(name,s,'shell','18 mm; Williams buttons and backbox pivot reference; leg holes pending exact mounting datum')
front=box(18,0,0,564,18,H)
front=front.cut(box(144.425,-1,92.840625,311.15,20,264.31875))
for z in (280,230):
 front=front.cut(cyl(90,-1,z,12.7,20,(0,1,0))).cut(cyl(90,0,z,17.4625,12.7,(0,1,0)))
# Coin fasteners, sourced center spacing, centered on door.
for x,z in [(136.4875,225),(463.5125,225),(300,84.903125),(300,365.096875)]:
 front=front.cut(cyl(x,-1,z,3.571875,20,(0,1,0)))
add('FRONT',front,'shell','Door reference opening; start/extra at x90; Arnoz plunger center x520 z250 RESERVED, not drilled')
rear=box(18,L-18,0,564,18,HR).cut(box(130,L-19,72,340,20,293))
add('REAR',rear,'shell','Rear access 340 x 293; fused inlet and RJ45 zones reserved; exact cutouts pending selected parts')
door=box(132,L-18,74,336,18,289)
for x in (230,370):
 door=door.cut(cyl(x,L-19,280,58,20,(0,1,0)))
 for dx in (-52.5,52.5):
  for dz in (-52.5,52.5):door=door.cut(cyl(x+dx,L-19,280+dz,2.25,20,(0,1,0)))
 fan=box(x-60,L-43,220,120,25,120).cut(cyl(x,L-44,280,56,27,(0,1,0)))
 add('FAN_'+str(x),fan,'fan','120 x 120 x 25 reference frame, exhaust; exact fan not selected; guards and detachable cable required')
add('REAR_DOOR',door,'door','Two 116 mm draft air openings; 105 mm mounting pitch and 4.5 mm holes; confirm selected fan and fasteners')
floor=box(18,18,18,564,L-36,18).cut(cyl(300,440,17,69.85,20))
floor=floor.cut(box(400,630,17,100,160,20))
for x in (185,245,305,365):floor=floor.cut(cyl(x,90,17,14,20))
add('FLOOR',floor,'floor','Sub opening 139.7 reference; intake 100 x 160; four nominal 28 mm auxiliary holes')
# Floor cleats, kept away from front auxiliary buttons and rear service path.
for x in (18,552):add('FLOOR_CLEAT_'+str(x),box(x,120,0,30,L-156,18),'support','Simple glued/screwed floor support')
for i,(y,z) in enumerate([(120,160),(600,180),(1080,240)],1):
 add('SHELF_'+str(i),box(20,y,z,560,150,12),'shelf','Transverse removable board; 150 mm deep; access from front and rear; 12 mm thickness proposal')
 for side,x in [('L',18),('R',564)]:add('SHELF_SUPPORT_'+str(i)+side,box(x,y,z-18,18,150,18),'support','Simple side cleat; screw fasteners to be detailed')
# Vertical crossmembers with beveled top matching the existing monitor support plane.
def top_at(y):return bz+(y-45)*math.tan(alpha)-36/math.cos(alpha)
for i,cy in enumerate((380.,700.,980.),1):
 y0=cy-9; y1=cy+9; bottom=top_at(cy)-80
 pts=[A.Vector(30.2,y0,bottom),A.Vector(30.2,y1,bottom),A.Vector(30.2,y1,top_at(y1)),A.Vector(30.2,y0,top_at(y0)),A.Vector(30.2,y0,bottom)]
 add('CROSS_'+str(i),Part.Face(Part.makePolygon(pts)).extrude(A.Vector(539.6,0,0)),'brace','Upright 18 mm board; 80 mm center height; bevel follows monitor plane; CSD holes pending; slides upward out of guides')
 for side,x,gx,bx in [('L',18.,30.,36.),('R',564.,564.,524.)]:
  guide=box(x,cy-30,bottom-45,18,60,145)
  guide=guide.cut(box(gx,cy-9.2,bottom-25,6,18.4,130))
  # Guide anchoring holes: two columns clear of the groove, two levels.
  for yy in (cy-22,cy+22):
   for zz in (bottom+20,bottom+75):guide=guide.cut(cyl(x-1,yy,zz,2.75,20,(1,0,0)))
  # Three discrete support heights, nominal +/- 10 mm. M5 pilot interface is provisional.
  for yy in (cy-20,cy+20):
   for zz in (bottom-32,bottom-22,bottom-12):guide=guide.cut(cyl(x-1,yy,zz,2.75,20,(1,0,0)))
  add('CROSS_GUIDE_'+str(i)+side,guide,'guide','Replaceable 18 x 60 x 145 guide, 6 mm deep groove; 12 mm guide back retained; side wall not grooved; all hardware provisional')
  # L-shaped support envelopes: shelf under beam, vertical leg below it.
  foot=box(bx,cy-25,bottom-3,40,50,3)
  vx=bx if side=='L' else bx+37
  angle=foot.fuse(box(vx,cy-25,bottom-40,3,50,40)).removeSplitter()
  for yy in (cy-20,cy+20):angle=angle.cut(cyl(vx-1,yy,bottom-22,2.75,5,(1,0,0)))
  add('CROSS_BRACKET_'+str(i)+side,angle,'bracket','Generic 40 x 40 x 50 x 3 support-angle envelope; not a purchased SKU or rated part; positive support under beam')
for side,x in [('L',55),('R',515)]:add('MONITOR_RAIL_'+side,tf(box(x,60,-36,30,940,18)),'mount','Simple removable monitor support rail; service hinge/props not defined by this layout')
add('MONITOR_BRIDGE',tf(box(55,360,-18,490,250,18)),'mount','Replaceable VESA mounting board; display-specific holes pending')
add('PLAYFIELD_ENVELOPE',tf(box(20,0,0,560,970,55)),'envelope','Maximum retained display envelope; not a physical wooden part')
add('AUDIO_STARTECH',box(200,155,175,100,60,25),'audio','Owner-selected ICUSBAUDIO7D; official body 100 x 60 x 25; connectors and removable mount require clearance')
add('PC_BASE',box(157.5,830,36,285,460,18),'pcbase','Wood screwed directly over cabinet floor; no raised platform or drawer')
add('PC_ENVELOPE',box(167.5,840,54,265,440,128),'pc','Retained PC envelope, confirm actual GPU/cooler dimensions')
add('BACKBOX_BASE',box(18,R,HR-18,564,L-R-18,18),'shell','Existing backbox support height retained; genuine Williams hinge pair to be mounted on actual backbox floor')
# Zone markers deliberately not subtractive geometry.
add('PLUNGER_RESERVED',box(502,18,232,36,202,36),'reserved','Arnoz plunger reservation, center x520 z250, exact mechanism/template required')
add('MAINS_RESERVED',box(50,L-30,395,90,12,70),'reserved','Covered fused arcade mains inlet; cutout not confirmed')
add('RJ45_RESERVED',box(510,L-30,405,40,12,40),'reserved','Rear network panel connector; cutout not confirmed')
d.recompute()
assert len([r for r in records if r['kind']=='fan'])==2

assert len([r for r in records if r['kind']=='shelf'])==3
assert len([r for r in records if r['kind']=='brace'])==3
# Check positive-volume intersections among manufactured boards and key envelopes.
collisions=[]
items=list(shapes.items())
for i,(a,sa) in enumerate(items):
 for b,sb in items[i+1:]:
  v=sa.common(sb).Volume
  if v>0.01:collisions.append(dict(a=a,b=b,mm3=v))
json.dump(dict(parts=records,collisions=collisions,units='mm',manufacturing_ready=False),open(OUT+'/geometry.json','w'),indent=2)
assert not collisions, str(collisions)
d.saveAs(OUT+'/vpin-central-v32.FCStd')
Part.export([o for o in d.Objects if hasattr(o,'Shape') and o.Category not in ('envelope','reserved','pc','audio')],OUT+'/vpin-central-v32.step')
print('V32_SUCCESS',len(records),'objects; intersections',collisions)
