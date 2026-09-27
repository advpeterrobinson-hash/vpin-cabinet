"""Negative saved-file controls; never alter the review package."""
import os
from pathlib import Path
import runpy
import tempfile
import FreeCAD as App
root = Path(__file__).resolve().parents[1]
source = root/'exports/generated/cabinet-v32/vpin-central-v32.FCStd'
with tempfile.TemporaryDirectory(prefix='vpin-v32-negative-') as td:
    for case in ('label','missing-language','changed-baseline'):
        doc = App.openDocument(str(source))
        if case == 'label': doc.getObject('SHELF_1').Label = 'P1'
        elif case == 'missing-language': doc.getObject('SHELF_1').NamePTBR = ''
        else:
            o=doc.getObject('SHELF_1');s=o.Shape.copy();s.translate(App.Vector(0,0,1));o.Shape=s
        path=Path(td)/(case+'.FCStd');doc.recompute();doc.saveAs(str(path));App.closeDocument(doc.Name)
        os.environ['VPIN_V32_DOCUMENT']=str(source if case=='changed-baseline' else path)
        os.environ['VPIN_V32_BASELINE']=str(path if case=='changed-baseline' else source)
        try: runpy.run_path(str(root/'tools/verify_v32_entry.py'))
        except AssertionError as e:
            if case=='changed-baseline': assert 'GEOMETRY CHANGE REQUIRES REVIEW' in str(e)
            print('V32_NEGATIVE_PASS',case)
        else: raise RuntimeError('Accepted mutant '+case)
        finally:
            for name in list(App.listDocuments()): App.closeDocument(name)
print('V32_NEGATIVE_TESTS_PASS')
