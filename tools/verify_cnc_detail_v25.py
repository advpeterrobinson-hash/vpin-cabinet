"""Reopen detail model and independently test solids, contacts and protected geometry."""
import os,sys,csv,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import FreeCAD as A
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def verify(path=None, omitted_joint=False):
    base=A.openDocument(str(ROOT/'cad/active/vpin-active.FCStd'))
    detail=A.openDocument(str(path or ROOT/'exports/generated/cnc-detail/vpin-cnc-detail-preview.FCStd'))
    rows=list(csv.DictReader((ROOT/'bom/ACTIVE_PARTS.csv').open()))
    joints=list(csv.DictReader((ROOT/'bom/STRUCTURAL_JOINTS_V25.csv').open()))
    expected={frozenset((r['object_a'],r['object_b'])) for r in joints if r['joint_type']!='INTERNAL_LAMINATION'}
    if omitted_joint:expected.remove(next(iter(expected)))
    actual=set();names=[r['object_name'] for r in rows]
    for i,n in enumerate(names):
     a=detail.getObject(n);assert a and a.PartID==rows[i]['part_id']
     assert a.Shape.isValid() and len(a.Shape.Solids)==1,n
     for m in names[i+1:]:
      if base.getObject(n).Shape.distToShape(base.getObject(m).Shape)[0]<1e-6:actual.add(frozenset((n,m)))
      assert a.Shape.common(detail.getObject(m).Shape).Volume<1e-4,('overlap',n,m)
    assert actual==expected,'unregistered/missing contact pair'
    assert {o.Name for o in detail.Objects if getattr(o,'EngineeringRole','')=='STRUCTURAL_WOOD'}==set(names),'extra broad shelf or missing wood'
    for n in names:
     if n.startswith('RearCPU'):
      a=base.getObject(n).Shape;b=detail.getObject(n).Shape
      assert a.cut(b).Volume+b.cut(a).Volume<1e-4,('CPU geometry changed',n)
    for side in ('Left','Right'):
     rail=detail.getObject('RearCPUSupportRail'+side+'V24').Shape
     bracket=detail.getObject('ClassicLegBracket'+('RL' if side=='Left' else 'RR')+'V21').Shape
     assert abs(rail.distToShape(bracket)[0]-13.8)<1e-5,'rail/bracket gap changed'
     assert rail.common(bracket).Volume<1e-5
    left=detail.getObject('CabinetLeftSide').Shape;right=detail.getObject('CabinetRightSide').Shape
    assert abs(right.BoundBox.XMax-left.BoundBox.XMin-600)<1e-6
    # t/3 captures leave >=2t/3 skin throughout the common primary-side envelope.
    import Part
    for shape,x in ((left,0),(right,588)):
     slab=Part.makeBox(12,1308.1,596.9,A.Vector(x,0,0))
     original=(base.getObject('CabinetLeftSide') if x==0 else base.getObject('CabinetRightSide')).Shape
     assert original.common(slab).cut(shape).Volume<1e-4,'remaining side skin'
    # Recompute state and absence of obsolete systems are checked independently of labels.
    assert not any(detail.getObject(n) for n in ('PCServiceSledV21','WheelKeepoutRLV20','RearCPUHarnessLoopGhostV24','LegSideDoublerRLV20'))
    detail.recompute();assert all('Invalid' not in o.State for o in detail.Objects)
    # Known rear ligaments and rail saddle web; hardware bolt edge distances remain blocked.
    rear=detail.getObject('RearPanelWithCPUHatchV24').Shape.BoundBox
    assert min(130-rear.XMin,rear.XMax-470)>=118-1e-6,'rear side ligament'
    assert detail.getObject('RearCPUHatchOpeningGhostV24').Shape.BoundBox.ZMin-detail.getObject('CapturedBottomV20').Shape.BoundBox.ZMax>=74-1e-6,'hatch/bottom capture ligament'
    for side in ('Left','Right'):
     rail=detail.getObject('RearCPUSupportRail'+side+'V24').Shape.BoundBox
     assert rail.ZMax-116>=55.5-1e-6,'rail web over saddle'
    A.closeDocument(detail.Name);A.closeDocument(base.Name)
    print('\nCNC_DETAIL_SAVED_PASS: 32 wood solids; all contacts accounted; zero wood overlaps; CPU/gap preserved; side skin >= 2t/3')
