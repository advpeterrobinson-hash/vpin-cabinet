"""Fresh engineering master; never reads or mutates the historical working FCStd."""
from pathlib import Path
import json
import FreeCAD as App
import Part

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'cad/active/vpin-active.FCStd'


def main():
    import build_cabinet_structure_v20 as cabinet
    import build_structure_v14 as backbox
    import build_playfield_mechanics_v18 as playfield
    import build_playfield_fixed_anchors_v19 as anchors
    import build_cabinet_service_v21 as legs
    import build_service_io_v09 as io
    import build_cabinet_rear_cpu_shelf_v24 as cpu
    doc = App.newDocument('VPinActive')
    c = json.loads((ROOT/'config/cabinet_structure_v20.json').read_text())['cabinet']
    shell = doc.addObject('App::Part','Shell')
    sheet = doc.addObject('Spreadsheet::Sheet','Parameters')
    for row,(key,value) in enumerate(c.items(),1):
        sheet.set('A'+str(row),key)
        sheet.set('B'+str(row),str(value)+' mm')
        sheet.setAlias('B'+str(row),key)
    w,t,l,hf,hr,flat = [c[k] for k in ('outer_width_mm','nominal_wood_mm','side_length_mm','front_height_mm','rear_height_mm','rear_top_flat_mm')]
    # Config-derived engineering profiles. All source dimensions retained in Parameters.
    for side,x in [('Left',0),('Right',w-t)]:
        vertices=[App.Vector(x,y,z) for y,z in [(0,0),(l,0),(l,hr),(l-flat,hr),(0,hf),(0,0)]]
        o=doc.addObject('PartDesign::Feature','Cabinet'+side+'Side')
        o.Shape=Part.Face(Part.makePolygon(vertices)).extrude(App.Vector(t,0,0));shell.addObject(o)
        o.addProperty('App::PropertyString','PartID');o.PartID='CAB-SIDE-001'+('L' if side=='Left' else 'R')+'-R1'
    for module in (cabinet,backbox,playfield,anchors,legs,io,cpu):
        if module in (cabinet, legs):
            module.main(doc, active_only=True)
        else:
            module.main(doc)
    marker=doc.addObject('App::FeaturePython','ActiveBuildV25')
    marker.addProperty('App::PropertyString','ManufacturingStatus')
    marker.ManufacturingStatus='BLOCKED: measured hardware, stock, joinery, load paths, coupon and physical proof tests'
    marker.Label='ACTIVE ENGINEERING - SOURCE GENERATED / NOT FOR CNC'
    from active_parts import register
    register(doc)
    doc.recompute()
    for o in doc.Objects:
        if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid():
            raise RuntimeError('Invalid shape: '+o.Name)
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    doc.saveAs(str(OUTPUT))
    App.closeDocument(doc.Name)
    print('FRESH_ACTIVE_SAVED',OUTPUT)
