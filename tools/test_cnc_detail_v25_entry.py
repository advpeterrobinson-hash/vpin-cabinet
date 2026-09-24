import os,sys,tempfile
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import FreeCAD as A
import Part
from verify_cnc_detail_v25 import verify,ROOT
source=ROOT/'exports/generated/cnc-detail/vpin-cnc-detail-preview.FCStd'
def overlap(doc):
 o=doc.getObject('CabinetLeftSide');o.Shape=o.Shape.fuse(Part.makeBox(6,18,100,A.Vector(12,0,0)))
def rail(doc):
 o=doc.getObject('RearCPUSupportRailLeftV24');s=o.Shape.copy();s.translate(A.Vector(-14,0,0));o.Shape=s
with tempfile.TemporaryDirectory(prefix='vpin-detail-negative-') as td:
 for name,change,target in [('restore-overlap',overlap,'overlap'),('move-rail',rail,'CPU geometry changed')]:
  doc=A.openDocument(str(source));change(doc);doc.recompute();path=os.path.join(td,name+'.FCStd');doc.saveAs(path);A.closeDocument(doc.Name)
  try:verify(path)
  except AssertionError as exc:
   assert target in str(exc),(name,str(exc))
   print('CNC_DETAIL_NEGATIVE_PASS',name)
  else:raise AssertionError('Accepted '+name)
  for n in list(A.listDocuments()):A.closeDocument(n)
 try:verify(omitted_joint=True)
 except AssertionError as exc:
  assert 'unregistered/missing contact pair' in str(exc)
  print('CNC_DETAIL_NEGATIVE_PASS missing contact')
 else:raise AssertionError('Accepted missing joint')
 for n in list(A.listDocuments()):A.closeDocument(n)
verify();print('\nCNC_DETAIL_NEGATIVE_TESTS_PASS')
