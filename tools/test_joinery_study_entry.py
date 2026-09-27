"""Saved-solid negative controls; no mutation of published V32 or study files."""
import os,sys,tempfile
from pathlib import Path
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import FreeCAD as App
from joinery_study import OUT,BASE,box,verify

def deep(doc):
    o=doc.getObject('SIDE_L');o.Shape=o.Shape.cut(box(11,18,17.9,7,1272.1,18.2))
def unchanged_part(doc):
    o=doc.getObject('SHELF_1');s=o.Shape.copy();s.translate(App.Vector(0,0,1));o.Shape=s
def fill_hole(doc):
    o=doc.getObject('FRONT');o.Shape=o.Shape.fuse(box(144.425,0,92.840625,311.15,18,264.31875)).removeSplitter()
def missing_capture(doc):
    base=App.openDocument(str(BASE));doc.getObject('SIDE_L').Shape=base.getObject('SIDE_L').Shape.copy();App.closeDocument(base.Name)
with tempfile.TemporaryDirectory(prefix='vpin-joinery-negative-') as td:
    for name,mutation,target in [('thin-skin',deep,'minimum nominal residual is 12 mm'),('changed-shelf',unchanged_part,'remaining forty objects unchanged'),('filled-coin-hole',fill_hole,'FRONT mating width 576 mm and original holes retained'),('missing-groove',missing_capture,'SIDE_L actual Floor capture void exists')]:
        doc=App.openDocument(str(OUT/'captured-shell-proposal.FCStd'));mutation(doc);doc.recompute()
        path=Path(td)/(name+'.FCStd');doc.saveAs(str(path));App.closeDocument(doc.Name)
        try:verify(path,write=False)
        except AssertionError as e:assert target in str(e),(name,str(e));print('JOINERY_NEGATIVE_PASS',name)
        else:raise AssertionError('Accepted mutant '+name)
print('JOINERY_NEGATIVE_TESTS_PASS')
