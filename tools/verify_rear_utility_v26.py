"""Saved-solid collision, load-path contact and clear-rectangle evidence for v26."""
import csv
import json
from pathlib import Path
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[1]

def empty_rectangles(bounds,obstacles):
    """Enumerate maximal axis-aligned empty rectangles at obstacle boundaries.
    Rectangles describe a mounting plane only; separate 3D checks prove packaging.
    """
    x0,x1,y0,y1=bounds
    xs=sorted({x0,x1}|{max(x0,min(x1,v)) for o in obstacles for v in o[:2]})
    ys=sorted({y0,y1}|{max(y0,min(y1,v)) for o in obstacles for v in o[2:]})
    candidates=[]
    for i,a in enumerate(xs):
        for b in xs[i+1:]:
            for j,c in enumerate(ys):
                for d in ys[j+1:]:
                    if any(min(b,q)>max(a,p)+1e-6 and min(d,t)>max(c,s)+1e-6 for p,q,s,t in obstacles):continue
                    candidates.append((a,b,c,d))
    candidates.sort(key=lambda r:(r[1]-r[0])*(r[3]-r[2]),reverse=True)
    maximal=[]
    for r in candidates:
        if not any(q[0]<=r[0] and q[1]>=r[1] and q[2]<=r[2] and q[3]>=r[3] for q in maximal):maximal.append(r)
    return [dict(bounds=list(r),width=r[1]-r[0],height=r[3]-r[2],area=(r[1]-r[0])*(r[3]-r[2])) for r in maximal]

def verify(doc,check):
    c=json.loads((ROOT/'config/rear_utility_v26.json').read_text())
    pc=json.loads((ROOT/'config/cabinet_rear_cpu_shelf_v24.json').read_text())['pc_shelf']
    def shape(name):
        o=doc.getObject(name)
        if o is None or o.Shape.isNull():raise RuntimeError('Missing '+name)
        return o.Shape
    def clear(a,b):return a.common(b).Volume<1e-5
    def touch(a,b):return a.distToShape(b)[0]<1e-6
    protected=['BottomJointKeepoutV26','RearLegKeepoutRLV26','RearLegKeepoutRRV26']
    def member(option,function,kind):return shape('Utility'+option+function+kind+'V26')
    panel=shape('RearPanelWithCPUHatchV24');bottom=shape('CapturedBottomV20')
    check('no active decorative rear fascia or troubleshooting carrier',not any(doc.getObject(n) for n in ['RearPowerFasciaV09','RearServiceFasciaV09','RearServiceConnectorCarrierV09','RearPowerWindowGhostV09','RearServiceWindowGhostV09','RearMainsEnclosureGhostV09']))
    expected_cuts={f'Utility{o}{f}OpeningV26' for o in ('A',) for f in ('Mains','Ethernet')}
    actual_cuts={o.Name for o in doc.Objects if getattr(o,'EngineeringRole','')in ('UTILITY_CUT','CANDIDATE_CUT')}
    check('only two localized utility cut solids',actual_cuts==expected_cuts,sorted(actual_cuts))
    check('only mains and optional Ethernet functions',c['permanent_functions']==['AC_MAINS_MASTER_DISCONNECT','OPTIONAL_ETHERNET'])
    check('selected rear face only; underside alternative absent',c['selected_architecture']=='A' and 'B' not in c and not any(o.Name.startswith(('UtilityB','UtilityCandidate')) for o in doc.Objects))
    # Independently reconstruct approved rear wood; symmetric difference detects extra/missing cuts.
    original=Part.makeBox(576,18,596.9,App.Vector(12,1290.1,0)).cut(Part.makeBox(340,22,240,App.Vector(130,1288.1,110)))
    intended=original
    for spec in ([60,1288.1,405,70,22,50],[518,1288.1,413,24,22,24]):
        x,y,z,dx,dy,dz=spec
        intended=intended.cut(Part.makeBox(dx,dy,dz,App.Vector(x,y,z)))
    check('active rear panel has only approved localized apertures',panel.cut(intended).Volume+intended.cut(panel).Volume<1e-4)
    check('active bottom has zero utility removal',abs(bottom.Volume-576*1284.1*18)<1e-4,bottom.Volume)
    option_reports={}
    wood_names=[o.Name for o in doc.Objects if getattr(o,'EngineeringRole','')=='STRUCTURAL_WOOD']
    mechanical=[o.Name for o in doc.Objects if o.Name.startswith(('CPURailAngle','CPURailBacking','RearCPUFixedSlide','ClassicLegBracket','LegSpreader'))]
    fixed=[n for n in wood_names+mechanical if n not in ['RearCPUServiceDoorClosedV24']]
    for option in ('A',):
        cuts=[member(option,f,'Opening') for f in ('Mains','Ethernet')]
        target=original
        preview=panel
        bad=[(f,n) for f,s in zip(('Mains','Ethernet'),cuts) for n in protected if not clear(s,shape(n))]
        check(option+' utility openings clear bottom joint and rear leg reserves',not bad,bad)
        volumes=[target.common(s).Volume for s in cuts]
        check(option+' reserved cuts cross original rear panel',all(abs(v-e)<1e-4 for v,e in zip(volumes,[63000,10368])),volumes)
        check(option+' active panel subtracts only reserved apertures',abs(target.Volume-preview.Volume-sum(volumes))<1e-4)
        check(option+' active panel preserves valid connected panel',preview.isValid() and len(preview.Solids)==1)
        sep=member(option,'Mains','Carrier').distToShape(member(option,'Ethernet','Carrier'))[0]
        innersep=member(option,'Mains','Enclosure').distToShape(member(option,'Ethernet','InternalAccess'))[0]
        check(option+' mains/signal carriers and internal access separated',min(sep,innersep)>=c['minimum_mains_signal_gap_mm'],dict(exterior_mm=sep,internal_mm=innersep))
        # Carriers contact the intended panel; enclosure and access envelopes must not consume structure.
        bad=[]
        for f,k in [('Mains','Enclosure'),('Ethernet','InternalAccess'),('Mains','PlugAccess'),('Ethernet','PlugAccess')]:
            s=member(option,f,k)
            for n in fixed+protected:
                if not clear(s,shape(n)):bad.append((f+k,n))
        check(option+' enclosure and cable-access volumes clear fixed structure',not bad,bad)
        door=shape('RearCPUServiceDoorClosedV24');db=door.BoundBox
        bad=[]
        for angle in range(106):
            moving=door.copy();moving.rotate(App.Vector(db.XMax,1323.1,98),App.Vector(0,0,1),-angle)
            for f,k in [('Mains','Carrier'),('Ethernet','Carrier'),('Mains','PlugAccess'),('Ethernet','PlugAccess')]:
                if not clear(moving,member(option,f,k)):bad.append((angle,f+k))
        check(option+' complete sampled outward door sweep clears utility and plugs',not bad,bad[:5])
        bad=[]
        for n in ['RearCPUShelfStowedV24','RearCPUOpenCaseStowedV24','RearCPUFixedSlideLeftV24','RearCPUFixedSlideRightV24']:
            b=shape(n).BoundBox;swept=Part.makeBox(b.XLength,b.YLength+450,b.ZLength,App.Vector(b.XMin,b.YMin,b.ZMin))
            for f,k in [('Mains','Enclosure'),('Ethernet','InternalAccess'),('Mains','Carrier'),('Ethernet','Carrier'),('Mains','PlugAccess'),('Ethernet','PlugAccess')]:
                if not clear(swept,member(option,f,k)):bad.append((n,f+k))
        check(option+' PC swept service volume clear',not bad,bad)
        option_reports[option]=dict(candidate_removal_mm3=sum(volumes),candidate_area_mm2=sum(volumes)/18,exterior_separation_mm=sep,internal_separation_mm=innersep,active_removal_mm3=original.Volume-panel.Volume)
    # A structural connection claim must include actual contact, not a floating rail label.
    rail_leg_distances={}
    for side in ('Left','Right'):
        rail=shape('RearCPUSupportRail'+side+'V24')
        bracket=shape('ClassicLegBracket'+('RL' if side=='Left' else 'RR')+'V21')
        rail_leg_distances[side]=rail.distToShape(bracket)[0]
        check(side+' rail clears modeled rear leg bracket',clear(rail,bracket),rail_leg_distances[side])
        check(side+' support rail valid and bottom seated',rail.isValid() and len(rail.Solids)==1 and touch(rail,bottom))
        check(side+' rail saddle clears unmodified rear crossmember',clear(rail,shape('LowCrossmember3V20')))
        check(side+' slide bears on rail face',touch(rail,shape('RearCPUFixedSlide'+side+'V24')))
        for i in (1,2):
            angle=shape(f'CPURailAngle{side}{i}V26');back=shape(f'CPURailBacking{side}{i}V26')
            check(f'{side} clamp {i} connects rail / bottom / underside backing',touch(angle,rail) and touch(angle,bottom) and touch(back,bottom))
            check(f'{side} clamp {i} clears rear leg reserves',all(clear(s,shape(n)) for s in [angle,back] for n in protected[1:]))
    # Reinforcement combination must retain BOTH original load zones.
    import math
    mech=json.loads((ROOT/'config/playfield_mechanics_v18.json').read_text())
    anchor=json.loads((ROOT/'config/playfield_fixed_anchors_v19.json').read_text())
    fs=anchor['closed_front_support'];alpha=math.atan2(596.9-400.05,1308.1-180.975)
    hy=float(doc.getObject('PlayfieldMechanicsV18').HingeY.Value);hz=float(doc.getObject('PlayfieldMechanicsV18').HingeZ.Value)
    h=mech['hinge_axis'];base=hz-h['local_y_from_display_front_mm']*math.sin(alpha)-h['local_z_from_display_base_mm']*math.cos(alpha)
    def yz(y,z):return (y*math.cos(alpha)-z*math.sin(alpha)+mech['display_envelope']['front_setback_mm'],y*math.sin(alpha)+z*math.cos(alpha)+base)
    cy,cz=yz(fs['steel_seat_local_y_front_mm']+fs['steel_seat_length_y_mm']/2,fs['steel_seat_local_z_bottom_mm']-35)
    ly,lz=yz(mech['closed_support']['latch_front_y_mm']-mech['display_envelope']['front_setback_mm']+35,-105)
    for side,x in [('Left',18),('Right',564)]:
        old1=Part.makeBox(18,120,105,App.Vector(x,cy-60,cz-52.5));old2=Part.makeBox(18,100,100,App.Vector(x,ly-50,lz-50))
        combined=shape('ClosedSupportDoubler'+side+'V19')
        check(side+' combined doubler preserves both original load zones',old1.cut(combined).Volume<1e-5 and old2.cut(combined).Volume<1e-5 and len(combined.Solids)==1 and doc.getObject('LatchReceiverDoubler'+side+'V19') is None)
    with (ROOT/'exports/generated/active-parts.csv').open() as f:rows=list(csv.DictReader(f))
    actual={o.Name:getattr(o,'PartID','') for o in doc.Objects if getattr(o,'EngineeringRole','')=='STRUCTURAL_WOOD'}
    listed={r['object_name']:r['part_id'] for r in rows}
    check('wood register exactly reconciles with CAD',actual==listed and len(rows)==36 and len(set(listed.values()))==36,{'before':40,'after':len(rows)})
    # Clear rectangles derived from saved door, shelf, leg and support bounds.
    def projection(name,axes,margin=0):
        b=shape(name).BoundBox
        return [getattr(b,axes[0]+'Min')-margin,getattr(b,axes[0]+'Max')+margin,getattr(b,axes[1]+'Min')-margin,getattr(b,axes[1]+'Max')+margin]
    front_bounds=[38,562,56,shape('RearShelfV14').BoundBox.ZMin-20]
    rear_obstacles=[projection('RearCPUServiceDoorClosedV24',('X','Z'),20)]+[projection(n,('X','Z')) for n in protected[1:]]
    under_bounds=[38,562,shape('LowCrossmember3V20').BoundBox.YMax+20,1290.1-20]
    under_obstacles=[projection(n,('X','Y'),10) for n in ['RearCPUSupportRailLeftV24','RearCPUSupportRailRightV24']]+[projection(n,('X','Y')) for n in protected[1:]+[x for x in mechanical if x.startswith(('CPURailAngle','CPURailBacking'))]]
    rectangles={'rear_XZ':empty_rectangles(front_bounds,rear_obstacles),'underside_XY':empty_rectangles(under_bounds,under_obstacles)}
    # Quasi-static reactions: payload at full-extension board centre, two symmetric rails.
    board_mass=shape('RearCPUShelfStowedV24').Volume/1e9*pc['support_detail']['nominal_plywood_density_kg_m3']
    force=(pc['proof_test_payload_kg']+board_mass)*9.81
    f,r=pc['support_detail']['foot_center_y_mm'];cg=shape('RearCPUShelfServiceGhostV24').CenterOfMass.y
    rear_reaction=force*(cg-f)/(r-f);front_reaction=force-rear_reaction
    data=dict(options=option_reports,clear_rectangles=rectangles,release_limits={'rail_to_actual_modeled_leg_mm':rail_leg_distances,'rail_planning_margin_mm':c['leg_keepout_margin_mm'],'note':'13.8 mm actual bracket gap; rail intrudes 1.2 mm into conservative 15 mm reserve. Measured leg/bracket required before rail/support freeze; utility apertures and clamps do not enter the reserve.'},load_estimate=dict(payload_kg=20,board_mass_kg=board_mass,total_weight_N=force,load_y_mm=cg,front_anchor_y_mm=f,rear_anchor_y_mm=r,front_pair_reaction_N=front_reaction,rear_pair_reaction_N=rear_reaction,front_uplift_per_rail_N=-front_reaction/2,rear_downward_per_rail_N=rear_reaction/2,status='GEOMETRIC LOAD PATH ONLY: bolt bearing/rail deflection/bracket capacities and dynamic proof test NOT VERIFIED'))
    (ROOT/'exports/generated/rear-utility-study.json').write_text(json.dumps(data,indent=2)+'\n')
