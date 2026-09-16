"""Explicit wooden-part register; local sizes are measured from generated solids.
No row in this register is authorization to machine an engineering envelope.
"""
import csv
import math
from pathlib import Path
import FreeCAD as App
ROOT=Path(__file__).resolve().parents[1]

def load_path(name):
    if name.startswith('Cabinet'):return 'Captured shell -> compact steel leg brackets -> legs/levelers'
    if name=='CapturedBottomV20':return 'PC rail bearing + clamp/backing -> bottom -> captured edges/low ties -> shell/legs'
    if name.startswith('LowCrossmember'):return 'Shell shear/torsion and bottom restraint -> captured side joints -> shell/legs'
    if name.startswith(('CapturedFront','RearPanel')):return 'End-panel shear -> captured side/bottom joints -> shell/legs; preserve hatch ligaments'
    if name.startswith('RearShelf'):return 'Backbox floor/locks -> rear shelf -> side/rear shell -> legs'
    if name.startswith('BackboxServiceDoor'):return 'Door self-weight -> measured hinge/frame; not primary backbox bracing'
    if name.startswith('Backbox'):return 'Display rail cage/box shear -> perimeter/floor -> rear shelf and independent upright locks'
    if name.startswith('Cradle'):return 'Display adapter -> cradle rails/ties -> local pivot laminations and closed supports -> shell'
    if name.startswith('ClosedSupportDoubler'):return 'Closed cradle landing/positive latch -> steel seat/strike -> combined doubler -> cabinet side'
    if name.startswith('SafetyStayDoubler'):return 'Raised cradle -> independent positive stay -> captive plate/doubler -> cabinet side'
    if name.startswith('GasStrutDoubler'):return 'Lift-assist reaction -> captive plate/doubler -> side; not a safety restraint'
    if name.startswith('RearCPUSupport'):return 'Fixed slide -> rail web -> bottom bearing + bolted angle clamps -> backed bottom -> shell'
    if name.startswith('RearCPUShelf'):return 'PC bolts -> replaceable board -> two slides -> fixed rails -> bottom/shell'
    if name.startswith('RearCPUServiceDoor'):return 'Door self-weight/latch -> measured hinge/rear panel; carries no mains hardware'
    raise ValueError('Missing load path '+name)

def register(doc):
    rules={}
    def add(names,decision,reason,thickness,orientation,operations):
        for name in names.split():rules[name]=(decision,reason,thickness,orientation,operations)
    add('CabinetLeftSide CabinetRightSide','KEEP','Primary shell and leg/pivot load path',18,'YZ; inside face; front arrow','side profile; captured dados; measured leg/bearing/button holes')
    add('CapturedFrontPanelV20 RearPanelWithCPUHatchV24','KEEP','Captured end panels preserve shell stiffness',18,'XZ; inside face; up arrow','captured edges; measured coin door or CPU aperture; rear only: generic utility apertures 70x50 and 24x24; component patterns/CNC release BLOCKED')
    add('CapturedBottomV20','KEEP','Bottom shear panel and local equipment supports',18,'XY; inside up; front arrow','four-edge capture; measured support mounts; vents TBD')
    add('LowCrossmember1V20 LowCrossmember2V20 LowCrossmember3V20','KEEP','Low shell ties; retain until stiffness/load tests support deletion',18,'XZ; front arrow','side capture; support connections TBD')
    add('RearShelfV14','KEEP','Backbox load support and upright lock interface',18,'XY; top; rear arrow','matched floor/lock/passport patterns BLOCKED')
    add('BackboxFloorV14 BackboxTopV14','KEEP','Backbox perimeter load path',18,'XY; inside face','joint topology pending; measured hinges/locks/passports')
    add('BackboxLeftSideV14 BackboxRightSideV14','KEEP','Backbox perimeter load path',18,'YZ; inside face','matched captured joints pending')
    add('BackboxRearFrameLeftV14 BackboxRearFrameRightV14 BackboxRearFrameBottomV14 BackboxRearFrameTopV14','COMBINE','Candidate single rear frame after nesting and shear/joint verification; retain present frame until proven',18,'XZ; inside face','joint resolution; guarded fan windows; hinge/latch holes BLOCKED')
    add('BackboxServiceDoorV14','KEEP','Keyed gasketed rear service access',15,'XZ; inside face; up arrow','measured hinge/latch/gasket interface BLOCKED')
    add('CradleSideRailLeftV18 CradleSideRailRightV18','KEEP','Independent display load path',18,'playfield local YZ; front arrow','rail/tie joinery; measured mounting patterns BLOCKED')
    add('CradleCrossmember1V18 CradleCrossmember2V18 CradleCrossmember3V18','KEEP','Three narrow ties; retain stiffness without broad shelf',18,'playfield local XY; front arrow','rail joints; replaceable adapter mount holes BLOCKED')
    add('CradlePivotDoublerLeftV18 CradlePivotDoublerRightV18 CradleRearBeamV18','KEEP','Local 36 mm pivot load structure',36,'playfield local axes; rear arrow','split into two measured-stock laminations at release; metal interface holes BLOCKED')
    add('ClosedSupportDoublerLeftV19 ClosedSupportDoublerRightV19','COMBINE','Implemented one union per side retaining both original reinforcement zones',18,'YZ; inside face','combined union profile; matched hardware patterns pending')
    add('SafetyStayDoublerLeftV19 SafetyStayDoublerRightV19 GasStrutDoublerLeftV19 GasStrutDoublerRightV19','KEEP','Local safety/assist reaction load path; do not remove',18,'YZ; inside face','measured through-bolts and captive nut plates BLOCKED')
    add('RearCPUServiceDoorClosedV24','KEEP','One outward service door',15,'XZ; rear view left hinge; up arrow','measured hinge/latch patterns BLOCKED')
    add('RearCPUShelfStowedV24','KEEP','One replaceable case board; no second sled',18,'XY; case up; rear arrow','measured case/slide/retainer holes BLOCKED')
    add('RearCPUSupportRailLeftV24 RearCPUSupportRailRightV24','KEEP','18 mm bottom-seated rails; four identical local angle clamps with underside bolt backing',18,'YZ; rear arrow','measured slide and cabinet anchor patterns BLOCKED')
    rows=[]
    for i,(name,(decision,reason,t,orientation,ops)) in enumerate(rules.items(),1):
        o=doc.getObject(name)
        if o is None:raise RuntimeError('Missing registered wood '+name)
        if 'PartID' not in o.PropertiesList:o.addProperty('App::PropertyString','PartID')
        if not o.PartID:o.PartID='WOOD-'+name.removesuffix('V24').removesuffix('V19').removesuffix('V18').removesuffix('V09').upper()+'-R1'
        for prop,value in [('EngineeringRole','STRUCTURAL_WOOD'),('Material','marine plywood'),('Disposition',decision),('MachiningStatus','BLOCKED'),('AssemblyReference','docs/ACTIVE_ENGINEERING.md'),('Orientation',orientation)]:
            if prop not in o.PropertiesList:o.addProperty('App::PropertyString',prop,'Build Package')
            setattr(o,prop,value)
        local=o.Shape.copy()
        if name.startswith('Cradle'):local.rotate(App.Vector(0,0,0),App.Vector(1,0,0),-math.degrees(math.atan2(596.9-400.05,1308.1-180.975)))
        b=local.BoundBox
        rows.append(dict(part_id=o.PartID,object_name=name,current_function=reason,load_path=load_path(name),decision=decision,reason=reason,material=o.Material,nominal_thickness_mm=t,quantity=1,orientation=orientation,nominal_local_envelope_xyz_mm=' x '.join(f'{v:.3f}' for v in [b.XLength,b.YLength,b.ZLength]),finished_dimensions='BLOCKED: stock/joints/hardware unresolved',pockets_dados_through_cuts=ops,pilot_holes='BLOCKED: measured hardware',insert_tnut_positions='BLOCKED: measured hardware',engraving_alignment=o.PartID+'; '+orientation,assembly_reference=o.AssemblyReference,release_status='BLOCKED'))
    out=ROOT/'exports/generated';out.mkdir(parents=True,exist_ok=True)
    with (out/'active-parts.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    return rows
