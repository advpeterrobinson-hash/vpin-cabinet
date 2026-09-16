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

with tempfile.TemporaryDirectory(prefix='vpin-negative-') as td:
    for name,mutate,target in [('inward-door',wrong_door,'open door entirely exterior'),('high-shelf',wrong_height,'shelf 285 x 460 x 18 at Z135'),('harness',harness,'historical systems absent')]:
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
