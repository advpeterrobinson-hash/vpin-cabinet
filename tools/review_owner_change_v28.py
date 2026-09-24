"""Read current saved CAD; add DESIGN_PROVISIONAL review volumes in a separate file.
No hardware dimensions, cuts, patterns, active config or physical records are authored.
"""
import math
import hashlib
import json
from pathlib import Path
import FreeCAD as A
import Part

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exports/generated/owner-change-v28'
SOURCE=ROOT/'cad/active/vpin-active.FCStd'


def bounds(s):
    b=s.BoundBox
    return [b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax]


def box(b):
    return Part.makeBox(b[1]-b[0],b[3]-b[2],b[5]-b[4],A.Vector(b[0],b[2],b[4]))


def run():
    OUT.mkdir(parents=True,exist_ok=True)
    source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    d=A.openDocument(str(SOURCE))
    initial={o.Name:o.Shape.copy() for o in d.Objects if o.TypeId in ('PartDesign::Feature','Part::Feature') and not o.Shape.isNull()}
    bb=lambda n: bounds(initial[n])
    utility=json.loads((ROOT/'config/rear_utility_v26.json').read_text())
    owner=json.loads((ROOT/'config/owner_services_v27.json').read_text())
    margin=utility['joint_margin_mm'] # existing review margin; NOT a new fit tolerance
    bottom=bb('CapturedBottomV20'); t=bottom[5]-bottom[4]
    cm1=bb('LowCrossmember1V20');cm2=bb('LowCrossmember2V20')
    left=bb('ElectronicsCarrierLeftV27');right=bb('ElectronicsCarrierRightV27')
    aisle=bb('CentralServiceKeepoutV27');ssf=bb('SSFFrontLeftKeepoutV20')
    rail=bb('RearCPUSupportRailLeftV24');leg=bb('ClassicLegBracketFLV21')
    bt=left[5]-left[4]
    board_z=ssf[4]-margin-bt
    face=bb('CoinDoorEnvelopeV27');mounts=owner['electronics']['crossmember_mount_x_mm']
    front=[mounts[1]-t,mounts[2]+t,face[3]+margin,cm1[2]-margin,board_z,board_z+bt]
    side_front=math.ceil(bb('ControlLeftActionInternalV27')[3]+margin)
    board_specs={'F':front,'G':[left[0],left[1],side_front,left[3],board_z,board_z+bt],
                 'P':[right[0],right[1],side_front,right[3],board_z,board_z+bt]}
    # Existing payload inset/height reused as a conservative review envelope.
    oldpayload=bb('ElectronicsLeftPayloadEnvelopeV27')
    px=oldpayload[0]-left[0];py=oldpayload[2]-left[2];ph=oldpayload[5]-oldpayload[4]
    group=d.addObject('App::Part','OwnerChangeReviewV28')
    group.Label='V28 DESIGN-PROVISIONAL — NOT ACTIVE / NO CUTS'
    candidates={};info={}
    def add(name,b,kind,note):
        shape=box(b);o=d.addObject('PartDesign::Feature',name);o.Shape=shape;o.Label=name+' / '+note
        o.addProperty('App::PropertyString','EngineeringRole');o.EngineeringRole='DESIGN_PROVISIONAL'
        o.addProperty('App::PropertyString','ReviewKind');o.ReviewKind=kind
        o.addProperty('App::PropertyBool','ManufacturingReady');o.ManufacturingReady=False
        group.addObject(o);candidates[name]=shape;info[name]=dict(bounds=b,kind=kind,note=note)
        return shape
    for key,b in board_specs.items():
        add('ReviewBoard'+key,b,'BOARD','replaceable board envelope; no holes or fabricated profile')
        add('ReviewPayload'+key,[b[0]+px,b[1]-px,b[2]+py,b[3]-py,b[5],b[5]+ph],'PAYLOAD','unallocated usable device volume; existing planning height only')
        add('ReviewCable'+key,[b[0]+px,b[1]-px,b[2]+py,b[3]-py,left[5],b[4]],'CABLE','disconnect/loop reservation below board; bend radii unmeasured')
    # Six support stations, not final corbel/seat-strip profiles or fastener holes.
    for side,b in [('G',left),('P',right)]:
        for i,name in enumerate(('CarrierAngle'+('Left' if side=='G' else 'Right')+'1V27',
                                 'CarrierAngle'+('Left' if side=='G' else 'Right')+'2V27')):
            a=bb(name)
            if i==0:a[3]=side_front+(a[3]-a[2]) # longer station envelope, not final corbel profile
            add('ReviewSupport'+side+str(i+1),[a[0],a[1],a[2],a[3],a[4],board_z],'SUPPORT','CNC wood support station; reuse tie interface subject to stack/load review')
    for side,x in [('L',mounts[1]),('R',mounts[2])]:
        add('ReviewSupportF'+side,[x-t/2,x+t/2,front[2],cm1[2],cm1[4]+t,board_z],'SUPPORT','front corbel/seat station from first low tie; profile and bolts unresolved')
    # Main underside gap is derived from existing carrier, aisle, CM2 and CPU rail.
    mid=[left[0],aisle[0]-margin,cm2[3]+margin,rail[2]-margin,bottom[4],bottom[5]]
    frontzone=[leg[1]+margin,bb('ClassicLegBracketFRV21')[0]-margin,leg[3]+margin,cm1[2]-margin,bottom[4],bottom[5]]
    add('ReviewInletMidLeft',mid,'INLET_ZONE','preferred underside investigation zone; NOT cutout')
    add('ReviewInletFront',frontzone,'INLET_ZONE','secondary underside area; internal lid path competes with front board')
    add('ReviewInletCentral',[aisle[0],aisle[1],mid[2],mid[3],bottom[4],bottom[5]],'REJECT_ZONE','central access conflict; do not use')
    en=bb('UtilityAMainsEnclosureV26');ew,ed,eh=en[1]-en[0],en[3]-en[2],en[5]-en[4]
    # Rotate the CURRENT unmeasured enclosure reserve, never a supplier model.
    probes={'MidLeft':[mid[0],mid[0]+ew,mid[2],mid[2]+eh,bottom[5],bottom[5]+ed],
            'Front':[frontzone[0],frontzone[0]+ew,frontzone[2],frontzone[2]+eh,bottom[5],bottom[5]+ed],
            'Central':[aisle[0],aisle[0]+ew,mid[2],mid[2]+eh,bottom[5],bottom[5]+ed]}
    access=bb('UtilityAMainsPlugAccessV26');projection=access[3]-access[2]
    for key,b in probes.items():
        add('ReviewMains'+key,b,'MAINS_PROBE','rotated existing enclosure reservation only; sample may not fit')
        add('ReviewMainsLid'+key,[b[0],b[1],b[2],b[3],b[5],b[5]+projection],'ACCESS','reused access-depth probe for internal lid/tools; not approved clearance')
        add('ReviewPlug'+key,[b[0],b[1],b[2],b[3],bottom[4]-projection,bottom[4]],'EXTERNAL_ACCESS','existing plug-depth planning probe; floor/leg/transport clearance UNKNOWN')
    eth=bb('UtilityAEthernetCarrierV26');eint=bb('UtilityAEthernetInternalAccessV26')
    add('ReviewRJ45Rear',eth,'RJ45_ZONE','KEEP rear adapter location; physical coupler sample controls adapter hole')
    side_y=bb('ClassicLegBracketRRV21')[2]-margin-(eth[1]-eth[0])
    shell=bb('CabinetRightSide');plate_thickness=eth[3]-eth[2]
    add('ReviewRJ45Side',[shell[1],shell[1]+plate_thickness,side_y,side_y+eth[1]-eth[0],eth[4],eth[5]],'RJ45_ZONE','side alternative; inspect moving cable reserve conflict')
    add('ReviewRJ45SideInside',[shell[0]-(eint[3]-eint[2]),shell[0],side_y-px,side_y+eth[1]-eth[0]+px,eint[4],eint[5]],'ACCESS','rotated current internal plug reserve')
    add('ReviewRJ45Bottom',[right[0],right[0]+eth[1]-eth[0],mid[2],mid[2]+eth[5]-eth[4],bottom[4]-plate_thickness,bottom[4]],'RJ45_ZONE','bottom alternative; floor and plug access unmeasured')
    # All blockers use exact saved B-reps; broad envelope collisions remain conservative.
    replaced={n for n in initial if n.startswith(('ElectronicsCarrier','ElectronicsLeftPayload','ElectronicsRightPayload','CarrierAngle'))}
    def physical(n):
        if n.startswith(('Defined','Airflow','LeftJoinery','RightJoinery','Review')) or n in replaced:return False
        if any(x in n for x in ('Opening','HoleGhost','LockAxis','PivotAxis','KeepoutV26')):return False
        if ('OpenGhost' in n or 'ServiceGhost' in n or 'ServiceSlide' in n or n.startswith(('SafetyStayOpen','PropReceiverLeftOpen','PropReceiverRightOpen','PropUpperLockPin','PropPinKeeper','BackboxDoorOpen','BackboxDoorLatchOpen','GenericPlayfieldDisplayOpen'))):return False
        obj=d.getObject(n);role=getattr(obj,'EngineeringRole','')
        return role not in ('DEFINED_CNC_CUT','ACCESS_ZONE','REVIEW_STATE')
    obstacles={n:s for n,s in initial.items() if physical(n)}
    def hits(shape,targets):
        return [n for n,s in targets.items() if shape.BoundBox.intersect(s.BoundBox) and shape.common(s).Volume>0.01]
    report=dict(source_sha256=source_hash,manufacturing_ready=False,authority='DESIGN_PROVISIONAL; original saved solids unchanged; no hardware pattern or production cut',
                derivation=dict(joint_review_margin=margin,stock_nominal=t,board_z_rule='SSF front lower Z minus existing joint review margin minus existing carrier thickness',front_rule='inner CM1 generic bolt centers +/- nominal stock; coin-door rear + margin to CM1 front - margin'),
                boards={},checks={},candidates=info)
    allboard={n:s for n,s in candidates.items() if n.startswith(('ReviewBoard','ReviewPayload'))}
    for key,b in board_specs.items():
        shape=candidates['ReviewBoard'+key].fuse(candidates['ReviewPayload'+key])
        report['boards'][key]=dict(board_bounds=b,payload_bounds=info['ReviewPayload'+key]['bounds'],
            closed_conflicts=hits(shape,obstacles),central_conflicts=hits(shape,{'CentralServiceKeepoutV27':initial['CentralServiceKeepoutV27']}))
    supports={n:s for n,s in candidates.items() if n.startswith('ReviewSupport')}
    for key in probes:
        report['checks']['mains_'+key]=dict(body_conflicts=hits(candidates['ReviewMains'+key],obstacles),
            support_conflicts=hits(candidates['ReviewMains'+key],supports),
            aisle_conflicts=hits(candidates['ReviewMains'+key],{'CentralServiceKeepoutV27':initial['CentralServiceKeepoutV27']}),
            lid_board_conflicts=hits(candidates['ReviewMainsLid'+key],allboard),
            lid_fixed_conflicts=hits(candidates['ReviewMainsLid'+key],obstacles),floor_clearance='UNKNOWN_PHYSICAL_LEGS_AND_PLUG_REQUIRED')
    report['checks']['rj45_side_internal_conflicts']=hits(candidates['ReviewRJ45SideInside'],obstacles)
    # Raised-service removal: raise above whole main shell, then translate toward front.
    raised={n:s for n,s in obstacles.items() if not n.startswith(('Cradle','GenericPlayfieldDisplayClosed','VesaAdapter','PivotPlate','PivotJournal','PropReceiver','PropRod','PlayfieldGlass'))}
    for n,s in initial.items():
        if n.startswith(('CradleOpenGhost','GenericPlayfieldDisplayOpen','SafetyStayOpen','PropReceiverLeftOpen','PropReceiverRightOpen','PropUpperLockPin','PropPinKeeper')):raised[n]=s
    high=bb('CabinetLeftSide')[5]+margin
    for key,b in board_specs.items():
        top=info['ReviewPayload'+key]['bounds'][5]
        lift=[b[0],b[1],b[2],b[3],b[4],high+(top-b[4])]
        forward=[b[0],b[1],- (b[3]-b[2])-margin,b[3],high,high+(top-b[4])]
        add('ReviewLift'+key,lift,'REMOVAL','upward service sweep with playfield open, both props pinned; glass removed')
        add('ReviewExtract'+key,forward,'REMOVAL','frontward extraction after lift; cables unplug first')
        other={n:s for n,s in allboard.items() if not n.endswith(key)}
        report['boards'][key]['removal_conflicts']=hits(box(lift),raised|other)+hits(box(forward),raised|other)
    report['checks']['support_conflicts']={n:hits(s,obstacles) for n,s in candidates.items() if n.startswith('ReviewSupport')}
    add('ReviewRejectedSidePayload',[oldpayload[0],oldpayload[1],oldpayload[2],oldpayload[3],board_z+bt,board_z+bt+ph],'REJECT_ZONE','rejected original-depth raised payload: secondary button conflict')
    report['checks']['original_depth_payload_conflicts']=hits(candidates['ReviewRejectedSidePayload'],obstacles)
    # Compare to a broad elevated spanning board as a rejected volume, not architecture.
    add('ReviewRejectedSpan',[left[0],right[1],left[2],left[3],board_z,board_z+bt],'REJECT_ZONE','rejected: bridges the central service reserve')
    report['checks']['spanning_board_conflict']=hits(candidates['ReviewRejectedSpan'],{'CentralServiceKeepoutV27':initial['CentralServiceKeepoutV27']})
    d.recompute()
    for n,s in initial.items():
        now=d.getObject(n).Shape
        assert all(abs(a-b)<1e-7 for a,b in zip(bounds(now),bounds(s))) and abs(now.Volume-s.Volume)<1e-5, 'active shape changed '+n
        if getattr(d.getObject(n),'EngineeringRole','')=='STRUCTURAL_WOOD':
            assert now.cut(s).Volume<1e-5 and s.cut(now).Volume<1e-5, 'active wood changed '+n
    path=OUT/'vpin-owner-change-v28.FCStd';d.saveAs(str(path));A.closeDocument(d.Name)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==source_hash,'active file modified'
    d=A.openDocument(str(path));inventory=[]
    for o in d.Objects:
        if o.TypeId not in ('PartDesign::Feature','Part::Feature') or o.Shape.isNull():continue
        assert o.Shape.isValid(),o.Name
        verts,tris=o.Shape.tessellate(1)
        inventory.append(dict(name=o.Name,label=o.Label,role=getattr(o,'EngineeringRole',''),bounds=bounds(o.Shape),
                              vertices=[list(v) for v in verts],triangles=tris,provisional=o.Name in candidates))
    report['inventory']=inventory
    (OUT/'review-analysis.json').write_text(json.dumps(report,indent=2)+'\n')
    A.closeDocument(d.Name)
    print('\nOWNER_CHANGE_REVIEW_SAVED',path)
    print('BOARDS',json.dumps(report['boards']))
    print('CHECKS',json.dumps(report['checks']))


if __name__=='__main__':run()
