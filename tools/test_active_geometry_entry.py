"""Negative controls: reject saved CAD defects that old marker checks missed."""
import os
import sys
import tempfile
from pathlib import Path
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import FreeCAD as App
from verify_active_geometry import verify,ROOT
import json
source=ROOT/'cad/active/vpin-active.FCStd'

def wrong_door(doc):
    o=doc.getObject('RearCPUServiceDoorOpenGhostV24')
    s=doc.getObject('RearCPUServiceDoorClosedV24').Shape.copy()
    s.rotate(App.Vector(482,1323.1,98),App.Vector(0,0,1),105)
    o.Shape=s

def wrong_height(doc):
    o=doc.getObject('RearCPUShelfStowedV24');s=o.Shape.copy();s.translate(App.Vector(0,0,70));o.Shape=s

def harness(doc):
    o=doc.addObject('PartDesign::Feature','RearCPUHarnessLoopGhostV24');o.Shape=doc.getObject('RearCPUShelfStowedV24').Shape.copy()

def high_door(doc):
    o=doc.getObject('RearCPUServiceDoorClosedV24');s=o.Shape.copy();s.translate(App.Vector(0,0,70));o.Shape=s

def joint_collision(doc):
    import Part
    doc.getObject('UtilityAMainsOpeningV26').Shape=Part.makeBox(70,22,50,App.Vector(200,1288.1,20))

def leg_collision(doc):
    import Part
    doc.getObject('UtilityAMainsOpeningV26').Shape=Part.makeBox(70,22,50,App.Vector(30,1288.1,60))

def separation(doc):
    o=doc.getObject('UtilityAEthernetCarrierV26');s=o.Shape.copy();s.translate(App.Vector(-350,0,0));o.Shape=s

def register_mismatch(doc):
    doc.getObject('RearCPUShelfStowedV24').PartID='WRONG-ID'

def restored_usb(doc):
    import Part
    o=doc.addObject('PartDesign::Feature','RearUSBServiceCut');o.Shape=Part.makeBox(20,22,20,App.Vector(250,1288.1,400))
    o.addProperty('App::PropertyString','EngineeringRole');o.EngineeringRole='CANDIDATE_CUT'

def floating_rail(doc):
    o=doc.getObject('RearCPUSupportRailLeftV24');s=o.Shape.copy();s.translate(App.Vector(0,0,1));o.Shape=s

cases=[('inward-door',wrong_door,'open door entirely exterior'),
       ('high-shelf',wrong_height,'shelf 285 x 460 x 18 at Z135'),
       ('harness',harness,'historical systems absent'),
       ('raised-door',high_door,'closed door 364 x 264 at Z98'),
       ('bottom-joint-cut',joint_collision,'A utility openings clear bottom joint and rear leg reserves'),
       ('leg-zone-cut',leg_collision,'A utility openings clear bottom joint and rear leg reserves'),
       ('mains-signal-spacing',separation,'A mains/signal carriers and internal access separated'),
       ('wood-register',register_mismatch,'wood register exactly reconciles with CAD'),
       ('rear-usb',restored_usb,'only four intended utility candidate cut solids'),
       ('floating-rail',floating_rail,'Left support rail valid and bottom seated')]
with tempfile.TemporaryDirectory(prefix='vpin-negative-') as td:
    for name,mutate,target in cases:
        doc=App.openDocument(str(source));mutate(doc);doc.recompute()
        path=Path(td)/(name+'.FCStd');doc.saveAs(str(path));App.closeDocument(doc.Name)
        try:verify(path)
        except RuntimeError:pass
        else:raise RuntimeError('Verifier accepted mutant '+name)
        report=json.loads((ROOT/'exports/generated/active-geometry-report.json').read_text())
        if not any(r['check']==target and not r['pass_'] for r in report['checks']):raise RuntimeError('Wrong rejection reason '+name)
        print('NEGATIVE_CONTROL_PASS',name)
verify(source)
print('ACTIVE_NEGATIVE_TESTS_PASS')
