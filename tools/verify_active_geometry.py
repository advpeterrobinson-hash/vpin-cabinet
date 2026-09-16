"""Geometric saved-file checks; reports evidence, never manufactures approval."""
from pathlib import Path
import json
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[1]

def verify(path=None):
    path=Path(path or ROOT/'cad/active/vpin-active.FCStd')
    doc=App.openDocument(str(path));doc.recompute()
    cfg=json.loads((ROOT/'config/cabinet_rear_cpu_shelf_v24.json').read_text())
    c=json.loads((ROOT/'config/cabinet_structure_v20.json').read_text())['cabinet']
    rear=c['side_length_mm'];results=[]
    def check(name,passed,detail=''):
        results.append(dict(check=name,pass_=bool(passed),detail=detail))
        print(('PASS ' if passed else 'FAIL ')+name+' '+str(detail))
    def shape(name):
        o=doc.getObject(name)
        if o is None or not hasattr(o,'Shape') or o.Shape.isNull():raise RuntimeError('Missing geometry '+name)
        return o.Shape
    def clear(a,b):return a.common(b).Volume < 1e-5
    check('all intended shapes valid',all(o.Shape.isValid() and len(o.Shape.Solids)>0 for o in doc.Objects if o.TypeId == 'PartDesign::Feature'))
    check('no recompute errors',all('Invalid' not in o.State for o in doc.Objects))
    check('historical systems absent',not any(doc.getObject(n) for n in ['PlayfieldServiceV04','PlayfieldServiceV05','OLED_Fit_Check','PCServiceSledV21','PCTrayStowedV20','WheelKeepoutRLV20','LegSideDoublerRLV20','RearCPUHarnessLoopGhostV24']))
    left,right=shape('CabinetLeftSide'),shape('CabinetRightSide')
    check('600 mm outer / 564 mm clear / 18 mm sides',abs(right.BoundBox.XMax-left.BoundBox.XMin-600)<1e-6 and abs(right.BoundBox.XMin-left.BoundBox.XMax-564)<1e-6 and abs(left.BoundBox.XLength-18)<1e-6)
    translated=left.copy();translated.translate(App.Vector(582,0,0))
    check('side symmetry',translated.cut(right).Volume<1e-5 and right.cut(translated).Volume<1e-5)
    check('1308.1 length / front and rear profile',abs(left.BoundBox.YLength-1308.1)<1e-6 and abs(left.BoundBox.ZLength-596.9)<1e-6)
    opening=shape('RearCPUHatchOpeningGhostV24');ob=opening.BoundBox
    check('lower 340 x 240 hatch at X130 Z110',all(abs(a-b)<1e-6 for a,b in zip([ob.XMin,ob.XLength,ob.ZMin,ob.ZLength],[130,340,110,240])))
    panel=shape('RearPanelWithCPUHatchV24')
    check('hatch is actually cut',clear(panel,opening))
    shelf=shape('RearCPUShelfStowedV24');case=shape('RearCPUOpenCaseStowedV24');sb=shelf.BoundBox;cb=case.BoundBox
    check('shelf 285 x 460 x 18 at Z135',all(abs(a-b)<1e-6 for a,b in zip([sb.XLength,sb.YLength,sb.ZLength,sb.ZMin],[285,460,18,135])))
    check('case 265 x 440 x 128 and 10 mm board margins',all(abs(a-b)<1e-6 for a,b in zip([cb.XLength,cb.YLength,cb.ZLength,cb.XMin-sb.XMin,cb.YMin-sb.YMin,cb.ZMin-sb.ZMax],[265,440,128,10,10,0])))
    ext=shape('RearCPUOpenCaseServiceGhostV24');eb=ext.BoundBox
    check('450 mm actual rearward travel',abs(eb.YMin-cb.YMin-450)<1e-6)
    fraction=max(0,eb.YMax-max(rear,eb.YMin))/eb.YLength
    check('PC essentially outside EXTERIOR plane',fraction>=0.95,{'fraction':fraction,'remaining_inside_mm':rear-eb.YMin})
    door=shape('RearCPUServiceDoorClosedV24');db=door.BoundBox
    check('closed door 364 x 264 at Z98',abs(db.ZMin-98)<1e-6 and abs(db.XLength-364)<1e-6 and abs(db.ZLength-264)<1e-6)
    opened=shape('RearCPUServiceDoorOpenGhostV24')
    check('open door entirely exterior',opened.BoundBox.YMin>=rear-1e-6,opened.BoundBox.YMin)
    expected=door.copy();pivot=App.Vector(db.XMax,rear+cfg['rear_service_door']['hinge_axis_y_offset_mm'],db.ZMin)
    expected.rotate(pivot,App.Vector(0,0,1),-105)
    check('saved open door matches 105 degree outward transform',expected.cut(opened).Volume<1e-5 and opened.cut(expected).Volume<1e-5)
    fixed_names=['RearPanelWithCPUHatchV24','RearCPUSupportRailLeftV24','RearCPUSupportRailRightV24','RearCPUFixedSlideLeftV24','RearCPUFixedSlideRightV24','ClassicLegBracketRLV21','ClassicLegBracketRRV21']
    fixed=[shape(n) for n in fixed_names]
    bad=[]
    for angle in range(0,106):
        sweep=door.copy();sweep.rotate(pivot,App.Vector(0,0,1),-angle)
        for name,s in zip(fixed_names,fixed):
            if not clear(sweep,s):bad.append((angle,name))
    check('door sweep 0..105 degrees clears rear hardware (1 degree samples)',not bad,bad[:8])
    check('open door clears full extraction',clear(opened,ext) and clear(opened,shape('RearCPUShelfServiceGhostV24')))
    # Linear swept boxes are exact for these rectangular translated components.
    bad=[]
    for name in ['RearCPUShelfStowedV24','RearCPUOpenCaseStowedV24','RearCPUFixedSlideLeftV24','RearCPUFixedSlideRightV24']:
        b=shape(name).BoundBox
        swept=Part.makeBox(b.XLength,b.YLength+450,b.ZLength,App.Vector(b.XMin,b.YMin,b.ZMin))
        for other in ['RearPanelWithCPUHatchV24','ClassicLegBracketRLV21','ClassicLegBracketRRV21','RearCPUSupportRailLeftV24','RearCPUSupportRailRightV24']:
            if not clear(swept,shape(other)):bad.append((name,other))
    check('exact linear service sweep clears fixed rear structure',not bad,bad)
    check('support rails clear rear panel',all(clear(shape(n),panel) for n in ['RearCPUSupportRailLeftV24','RearCPUSupportRailRightV24']))
    check('two independent positive safety stays retained',all(doc.getObject('SafetyStayOpen'+s+'V18') for s in ['Left','Right']))
    from verify_rear_utility_v26 import verify as verify_utility
    verify_utility(doc,check)
    inventory=[]
    for o in doc.Objects:
        if o.TypeId == 'PartDesign::Feature' and not o.Shape.isNull():
            b=o.Shape.BoundBox
            vertices,triangles=o.Shape.tessellate(2.0)
            inventory.append(dict(mesh_vertices=[[v.x,v.y,v.z] for v in vertices],mesh_triangles=triangles,role=getattr(o,'EngineeringRole','LOCAL_METAL' if o.Name.startswith(('CPURailAngle','CPURailBacking')) else ''),name=o.Name,label=o.Label,part_id=getattr(o,'PartID',''),bounds=[b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax],volume=o.Shape.Volume))
    out=ROOT/'exports/generated';out.mkdir(parents=True,exist_ok=True)
    (out/'active-geometry-report.json').write_text(json.dumps(dict(checks=results,inventory=inventory),indent=2)+'\n')
    App.closeDocument(doc.Name)
    if not all(r['pass_'] for r in results):raise RuntimeError('Active geometry verification failed; see report')
    print('ACTIVE_GEOMETRY_PASS')
