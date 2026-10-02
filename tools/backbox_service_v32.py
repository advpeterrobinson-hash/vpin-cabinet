"""Original parametric backbox service study. CERN-OHL-S-2.0.
Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
No purchased hinge, latch, glass, fan, or fastener is manufacturing-qualified.
"""
from pathlib import Path
import json, math, sys
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(R/'tools'))
from pivot_cradle_integration_v32 import load, transform, actual, pf_names, mesh, WPC, PF
from backbox_structure_review_v32 import box, hits, minimum, face, bounds
V=A.Vector
C=json.loads((R/'config/backbox_service_v32.json').read_text())
O=R/C['output_directory']

def cylinder_y(x,y,z,r,h): return Part.makeCylinder(r,h,V(x,y,z),V(0,1,0))
def shifted(s,x=0,y=0,z=0):
    t=s.copy();t.translate(V(x,y,z));return t
def mirror(s):
    m=A.Matrix();m.A11=-1;m.A14=600;t=s.copy();t.transformShape(m,True);return t
def drill_y(s,points,r,y=1000,h=500):
    for x,z in points:s=s.cut(cylinder_y(x,y,z,r,h))
    return s.removeSplitter()
def slot_y(x,y,z,r,length,thickness):
    return cylinder_y(x,y,z-length/2,r,thickness).fuse(cylinder_y(x,y,z+length/2,r,thickness)).fuse(box(x-r,y,z-length/2,2*r,thickness,length)).removeSplitter()
def ring(x,y,z,w,d,h,border):return box(x,y,z,w,d,h).cut(box(x+border,y-1,z+border,w-2*border,d+2,h-2*border)).removeSplitter()
def door_pose(ss,side,angle):
    out={n:s.copy() for n,s in ss.items()};x,y=C['rear']['hinge_axis_xy_mm'][0 if side=='L' else 1]
    for s in out.values():s.rotate(V(x,y,0),V(0,0,1),angle if side=='L' else -angle)
    return out

def build(source):
    """Return occupied parts and independent service/reserve geometry with groups."""
    p={n:s.copy() for n,s in source.items() if n.startswith('BB_') and not n.startswith('BB_Rear')};groups={};meta={}
    def add(n,s,g,material='plywood',note='explicit design decision'):
        n='BB_'+n;p[n]=s.removeSplitter();groups[n]=g;meta[n]={'material':material,'authority':note};return n
    for n in p:groups[n]='fixed';meta[n]={'material':'plywood','authority':'validated WPC wood; glass rebates are subtractions only'}
    rear=C['rear'];gx0,gx1,gz0,gz1=rear['aperture_xz_mm']; y0,y1=rear['frame_y_mm']
    frame=box(-90,y0,596.9,780,y1-y0,723.9)
    for s in p.values():frame=frame.cut(s)
    frame=frame.cut(box(gx0,y0-1,gz0,gx1-gx0,y1-y0+2,gz1-gz0))
    pad=box(*C['fan_flex']['fixed_integral_pad_left_box_mm'])
    frame=frame.fuse(pad).fuse(mirror(pad)).removeSplitter()
    add('RearFrame',frame,'fixed')
    # Side grooves do not reduce the 744 mm display insertion throat. Outside
    # 12 mm of each side stays continuous; no change to lower-side/floor geometry.
    gl=C['glass'];gy0,gy1=gl['channel_y_mm'];gz=gl['box_mm'][2]
    for side,x in [('L',-78),('R',672)]:
        cutter=box(x,gy0,gz,6,gy1-gy0,1321-gz)
        p['BB_Side'+side]=p['BB_Side'+side].cut(cutter).removeSplitter()
        # Three sides of a soft U liner; inner lips end exactly at inner side plane.
        liner=box(x,gy0,gz,6,2,1320.8-gz).fuse(box(x,gy1-2,gz,6,2,1320.8-gz)).fuse(box(x if side=='L' else x+4,gy0+2,gz,2,4,1320.8-gz))
        add('GlassLiner'+side,liner,'fixed','replaceable EPDM/felt reserve')
    split=p['BB_Top'].cut(box(-78,gy0,1302.8,756,gy1-gy0,19)).removeSplitter()
    top_solids=sorted(split.Solids,key=lambda t:t.CenterOfMass.y)
    assert len(top_solids)==2
    p['BB_Top']=top_solids[1]
    add('TopFrontRail',top_solids[0],'fixed')
    add('Backglass',box(*gl['box_mm']),'glass','tempered glass envelope','owner nominal 3–4 mm; supplier confirmation required')
    lower=box(-72,gy0-4,gz-18,744,18,18).cut(box(-76,gy0,gz-2,752,8,3))
    add('GlassLowerRail',lower,'fixed')
    add('GlassLowerPad',box(-76,gy0,gz-2,752,8,2),'fixed','replaceable EPDM/felt reserve')
    cap=box(*gl['top_retainer_box_mm']).fuse(box(-72,gy0,1307,744,8,13.8))
    for x,y in gl['retainer_fastener_xy_mm']:cap=cap.cut(Part.makeCylinder(3.25,15,V(x,y,1320)))
    add('GlassTopRetainer',cap,'retainer')
    add('GlassTopPad',box(-72,gy0,1305,744,8,2),'retainer','replaceable EPDM/felt reserve')
    for i,(x,y) in enumerate(gl['retainer_fastener_xy_mm']):
        add('GlassRetainerFastenerReserve'+str(i),Part.makeCylinder(3,30,V(x,y,1306)),'retainer','reference fastener envelope')
    # Fixed full-width rails + removable plywood ladder. End cleats are fixed to
    # full-thickness sides; shoulders carry shear, positive bolts retain all poses.
    d=C['display']
    for i,z in enumerate(d['rail_z_mm']):
        rail=box(-72,d['rail_y_mm'],z,744,18,d['rail_height_mm'])
        for x in d['adjustment_bolt_x_mm']:rail=rail.cut(Part.makeCylinder(3.25,d['rail_height_mm']+2,V(x,1277,z-1)))
        add('MonitorRail'+str(i),rail,'fixed')
        for side,x in [('L',-72),('R',654)]:add('MonitorRailCleat'+side+str(i),box(x,1248,z-30,18,38,30),'fixed')
    for i,x in enumerate(d['carrier_x_mm']):
        carrier=box(x,d['carrier_y_mm'],d['carrier_z_mm'][0],50,18,d['carrier_z_mm'][1]-d['carrier_z_mm'][0])
        for z in d['adjustment_bolt_z_mm']:carrier=carrier.cut(slot_y(x+25,1229,z,3.25,10,20))
        add('MonitorCarrier'+str(i),carrier,'carrier')
        for j,z in enumerate([858,1230]):
            shoe=box(x,1230,z,50,50,18).cut(carrier)
            for yy in [1251,1267]:shoe=shoe.cut(Part.makeCylinder(3.25,20,V(x+25,yy,z-1)))
            add('MonitorDepthShoe'+str(i)+str(j),shoe,'carrier')
            add('MonitorDepthBoltReserve'+str(i)+str(j),Part.makeCylinder(3,72,V(x+25,1267,810 if j==0 else 1224)),'carrier','reference fastener envelope')
    adapter=box(*d['plate_box_mm'])
    for x in d['adjustment_bolt_x_mm']:
        for z in d['adjustment_bolt_z_mm']:
            # Horizontal 30 mm slots for smaller displays. A 740 mm chassis is
            # limited to +/-1 mm centering by the shell, independently checked.
            cutter=slot_y(x,1217,z,3.25,30,14);cutter.rotate(V(x,1217,z),V(0,1,0),90)
            adapter=adapter.cut(cutter)
            add('MonitorClampReserve'+str(x)+str(z),cylinder_y(x,1218,z,9,36),'adapter','washer/through-bolt installation reserve')
    add('ReplaceableVESAPlate',adapter,'adapter')
    add('Display32',box(*d['envelope_box_mm']),'display','maximum occupied service envelope')
    bezel=box(-70,1106,842,740,6,457).cut(box(-50,1105,871,700,8,396))
    add('DisplayReplaceableBezel',bezel,'bezel','replaceable plywood; window customized to selected display')
    # Captive screw stop supports the plate through vertical adjustment. Through
    # bolts retain normal-to-screen loads during fold; no gravity-only hooks.
    for i,x in enumerate([205,377]):
        stop=box(x,1220,899,18,28,30).fuse(box(185 if i==0 else 377,1230,899,38,18,18))
        add('MonitorStopBlock'+str(i),stop,'carrier')
        add('MonitorStopScrewReserve'+str(i),Part.makeCylinder(3,46,V(x+9,1225,899)),'carrier','threaded adjuster/locknut reserve; ordinary hardware')
        add('MonitorStopContact'+str(i),box(x,1218,945,18,12,4),'adapter','plywood stop contact pad')
    # Lower front: a removable frame carries three replaceable adapters. Openings
    # are generic rectangles. No speaker diameter is cut into permanent wood.
    ca=C['lower_cassette'];cs=box(*ca['frame_box_mm'])
    for xx,w,h in [(-55,136,140),(100,400,160),(519,136,140)]:cs=cs.cut(box(xx,1103,720-h/2,w,20,h))
    add('LowerCassetteFrame',cs,'cassette')
    for side,xx in [('L',-70),('R',510)]:add('SpeakerBaffle'+side,box(xx,1092,620,160,12,200),'cassette')
    bezel=ring(90,1092,626,420,12,180,16)
    add('DMDReplaceableBezel',bezel,'cassette')
    # Opaque face adapters are blanks, not simulated working speaker cones.
    add('DMDEnvelope',box(*ca['dmd_box_mm']),'cassette','maximum occupied service envelope')
    for side,b in zip(['L','R'],ca['speaker_boxes_mm']):
        bb=list(b);recess=ca['speaker_recess_through_frame_mm'];bb[1]-=recess;bb[4]+=recess
        add('SpeakerEnvelope'+side,box(*bb),'cassette','occupied speaker envelope including passage through cassette frame')
    add('DMDRearAdapter',box(80,1167,704,440,12,96),'cassette','replaceable plywood VESA/non-VESA adapter')
    for i,x in enumerate([80,502]):add('DMDDepthTie'+str(i),box(x,1122,710,18,45,70),'cassette')
    for side,x in [('L',-72),('R',650)]:
        for i,z in enumerate(ca['attachment_z_mm']):
            add('CassetteFixedCleat'+side+str(i),box(x,1122,z-12,22,32,24),'fixed')
            add('CassetteBoltReserve'+side+str(i),cylinder_y(x+11,1098,z,ca['attachment_reference_diameter_mm']/2,65),'cassette','positive through-fastener reserve')
    # Door leaves, common fan stations and low intakes. Interchangeable modules
    # use the exact same holes; a blank has no ventilation or wire requirement.
    ve=C['ventilation'];z0,z1=rear['door_z_mm'];dy=rear['door_inner_y_mm'];dt=rear['door_thickness_mm']
    for i,side in enumerate(['L','R']):
        xa,xb=rear['door_x_mm'][i];fx,fz=ve['fan_centers_xz_mm'][i];ix=ve['intake_centers_x_mm'][i];iz0,iz1=ve['intake_z_mm'];iw=ve['intake_width_mm'];hx,hy=rear['hinge_axis_xy_mm'][i]
        door=box(xa,dy,z0,xb-xa,dt,z1-z0).cut(cylinder_y(fx,dy-1,fz,ve['opening_diameter_mm']/2,dt+2))
        pts=[(fx+sx*ve['pitch_mm']/2,fz+sz*ve['pitch_mm']/2) for sx in [-1,1] for sz in [-1,1]]
        door=drill_y(door,pts,ve['station_pilot_reference_mm']/2)
        door=door.cut(box(ix-iw/2,dy-1,iz0,iw,dt+2,iz1-iz0))
        add('Door'+side,door,'door'+side)
        # Fan is a full packaging envelope (rotor omitted), always optional.
        add('Fan'+side,box(fx-60,dy-25,fz-60,120,25,120),'door'+side,'optional fan occupied envelope','owner common 120x120x25 / 105 pitch family; no manufacturer selected')
        guard=ring(fx-64,dy+dt,fz-64,128,3,128,7)
        for zz in [fz-42,fz-21,fz,fz+21,fz+42]:guard=guard.fuse(box(fx-57,dy+dt,zz-1.5,114,3,3))
        add('FanGuard'+side,guard,'door'+side,'removable accessory reserve; finger-probe qualification pending')
        # Closed top and sides; downward mouth. Mesh/filter slides out from below
        # after two ordinary screws. Nothing faces upward while off.
        hood=box(fx-70,dy+dt+3,fz-70,140,19,140).cut(box(fx-67,dy+dt+2,fz-71,134,17,138))
        add('FanDustHood'+side,hood,'optional','optional downward-facing cover packaging')
        add('FanMeshReserve'+side,box(fx-57,dy+dt+2,fz-57,114,1,114),'door'+side,'replaceable mesh/filter envelope; not an impermeable physical sheet')
        intakeframe=ring(ix-iw/2-10,dy+dt,iz0-10,iw+20,6,iz1-iz0+20,10)
        add('IntakeFilterFrame'+side,intakeframe,'door'+side)
        add('IntakeMeshReserve'+side,box(ix-iw/2,dy+dt,iz0,iw,1,iz1-iz0),'door'+side,'replaceable mesh/filter envelope')
        baffle=box(ix-iw/2-6,dy-42,iz0-12,iw+12,6,iz1-iz0+18).fuse(box(ix-iw/2-6,dy-42,iz1+6,iw+12,42,6))
        for xx in [ix-iw/2-6,ix+iw/2]:baffle=baffle.fuse(box(xx,dy-42,iz0-12,6,42,iz1-iz0+18))
        add('IntakeDownBaffle'+side,baffle,'door'+side)
        # A separate fixed hinge cleat carries hinge screws, not the door gasket.
        xx=-78 if side=='L' else 655
        add('HingeCleat'+side,box(xx,1308.1,z0,23,14,z1-z0),'fixed')
        add('PianoHingeReserve'+side,Part.makeCylinder(rear['hinge_radius_reserve_mm'],z1-z0,V(hx,hy,z0)),'fixed','continuous hinge knuckle reserve; measured hinge required')
        for typ,x in [('Fixed',-78 if side=='L' else 655),('Door',-52 if side=='L' else 632)]:
            add('PianoLeaf'+typ+side,box(x,1322.1,z0,23 if typ=='Fixed' else 20,1.5,z1-z0),'fixed' if typ=='Fixed' else 'door'+side,'continuous hinge leaf reference')
        # Perimeter gasket leaves the moving hinge clear. Frame compression lands
        # are continuous; center is sealed by the passive-leaf astragal instead.
        gasket=box(gx0-8 if side=='L' else gx1,1308.1,gz0-8,8,2,gz1-gz0+16)
        for zz in [gz0-8,gz1]:gasket=gasket.fuse(box(gx0 if side=='L' else 300,1308.1,zz,342,2,8))
        add('DoorPerimeterGasket'+side,gasket,'fixed','replaceable compressed gasket envelope')
        # Strain relief and clamp attachment areas, without any connector holes.
        anchor=C['fan_flex']['door_anchor_left_mm'];aa=anchor if side=='L' else [600-anchor[0],anchor[1],anchor[2]]
        add('FanStrainReliefReserve'+side,box(aa[0]-6,aa[1]-3,aa[2]-8,12,dy-(aa[1]-3),16),'door'+side,'low-voltage clamp attachment reserve')
    add('CenterAstragal',box(*rear['astragal_box_mm']),'doorL')
    add('CenterGasket',box(282,1308.1,654,36,2,608),'doorL','replaceable compressed gasket envelope')
    # Hardware is shown in closed and retracted states. Body positions are design
    # envelopes. Their final mounting holes are intentionally not CNC released.
    add('CamLockBodyReserve',box(329,1284.1,946,22,26,28),'doorR','keyed lock body reserve')
    add('CamLockBarrelReserve',cylinder_y(340,1310.1,960,8,15),'doorR','key barrel reserve; final bore awaits selected lock')
    add('CamTongueClosedReserve',box(286,1290.1,957,54,4,6),'lockedR','keyed cam tongue reserve')
    add('CamTongueRetractedReserve',box(337,1290.1,904,6,4,54),'unlockedR','keyed cam tongue reserve')
    for i,z in enumerate([656,1198]):
        add('PassiveBoltBodyReserve'+str(i),box(246,1288.1,z,30,22,60),'doorL','internal slide-bolt body reserve')
        add('PassiveBoltClosedReserve'+str(i),Part.makeCylinder(3,40,V(261,1299.1,642 if i==0 else 1234)),'lockedL','retaining bolt reserve')
        add('PassiveBoltRetractedReserve'+str(i),Part.makeCylinder(3,40,V(261,1299.1,670 if i==0 else 1206)),'unlockedL','retaining bolt reserve')
    for side,b in zip(['L','R'],C['toy_zones']['upper_boxes_mm']):add('ToyZoneUpper'+side,box(*b),'zone','reserved free volume')
    for side,b in zip(['L','R'],C['toy_zones']['lower_boxes_mm']):add('ToyZoneLower'+side,box(*b),'zone','reserved free volume')
    add('OptionalToyShelfStudy',box(*C['toy_zones']['optional_shelf_box_mm']),'optional','accessory study, not installed')
    blanks={}
    for side,(x,z) in zip(['L','R'],ve['fan_centers_xz_mm']):
        blanks['BB_FanBlank'+side]=drill_y(box(x-64,dy+dt,z-64,128,6,128),[(x+dx*52.5,z+dz*52.5) for dx in [-1,1] for dz in [-1,1]],ve['station_pilot_reference_mm']/2)
    for n in p:
        ins=C['front_layout_insets_mm']
        dy=ins['cassette'] if groups[n]=='cassette' or n.startswith('BB_CassetteFixedCleat') else ins['display_carrier'] if groups[n] in ['display','adapter','carrier'] else ins['bezel'] if groups[n]=='bezel' else 0
        if dy:p[n]=shifted(p[n],y=dy)
    return p,groups,meta,blanks

def occupied(parts,groups,unlocked=False):
    exclude=['zone','optional','unlockedL','unlockedR'] if not unlocked else ['zone','optional','lockedL','lockedR']
    return {n:s for n,s in parts.items() if groups[n] not in exclude}

def door_scene(parts,groups,left=0,right=0):
    ss=occupied(parts,groups,True)
    for side,a in [('L',left),('R',right)]:
        mov={n:s for n,s in ss.items() if groups[n] in ['door'+side,'unlocked'+side]}
        ss.update(door_pose(mov,side,a))
    return ss

def flex(side,angle):
    """Constant-length spatial service loop within an explicit reserved corridor.
    Cable material/minimum dynamic bend radius still require builder confirmation.
    The centerline is sampled densely for length/curvature; OCC tubes certify space.
    """
    q=C['fan_flex'];aa=V(*q['fixed_anchor_left_mm']);bb=V(*q['door_anchor_left_mm'])
    if side=='R':aa.x=600-aa.x;bb.x=600-bb.x
    hx,hy=C['rear']['hinge_axis_xy_mm'][0 if side=='L' else 1]
    bb=A.Rotation(V(0,0,1),angle if side=='L' else -angle).multVec(bb-V(hx,hy,0))+V(hx,hy,0)
    def path(amp,count=80):
        out=[]
        for i in range(count+1):
            t=i/count
            out.append(V(aa.x*(1-t)+bb.x*t+(1 if side=='L' else -1)*amp*math.sin(math.pi*t),aa.y*(1-t)+bb.y*t,aa.z+(bb.z-aa.z)*(1-math.cos(math.pi*t))/2))
        return out
    lo,hi=0,100
    for _ in range(32):
        mid=(lo+hi)/2;vv=path(mid);length=sum((b-a).Length for a,b in zip(vv,vv[1:]))
        if length<q['length_mm']:lo=mid
        else:hi=mid
    vv=path((lo+hi)/2);radii=[]
    for a,b,c in zip(vv,vv[1:],vv[2:]):
        ab,bc,ac=b-a,c-b,c-a;cross=ab.cross(ac).Length
        if cross>1e-10:radii.append(ab.Length*bc.Length*ac.Length/(2*cross))
    # Union of short cylindrical/spherical swept segments is a conservative
    # tube around the sampled polyline, not a connector or electrical design.
    tt=path((lo+hi)/2,20);solids=[];rad=q['corridor_radius_mm']
    for a,b in zip(tt,tt[1:]):solids.append(Part.makeCylinder(rad,(b-a).Length,a,b-a))
    for a in tt:solids.append(Part.makeSphere(rad,a))
    return Part.makeCompound(solids),{'length_mm':sum((b-a).Length for a,b in zip(vv,vv[1:])),'minimum_centerline_bend_radius_mm':min(radii),'bow_mm':(lo+hi)/2}
