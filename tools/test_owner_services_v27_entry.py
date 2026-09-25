"""Saved-file negative controls for the owner-directed completeness pass."""
import os,sys,tempfile,json
from pathlib import Path
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import FreeCAD as A
import Part
from verify_owner_services_v27 import verify,ROOT
source=ROOT/'cad/active/vpin-active.FCStd'
def gas(d):
 o=d.addObject('PartDesign::Feature','GasStrutReturnedV27');o.Shape=Part.makeCylinder(5,200)
def one(d):d.removeObject('SafetyStayOpenRightV18')
def friction(d):
 o=d.getObject('SafetyStayOpenLeftV18');o.SupportMode='FRICTION';o.FrictionSupport=True
def keeper(d):d.removeObject('PropPinKeeperLeftOpenV27')
def ssf_hole(d):
 o=d.getObject('CabinetLeftSide');o.Shape=o.Shape.cut(Part.makeCylinder(40,20,A.Vector(-1,400,250),A.Vector(1,0,0)))
def weak_bottom(d):
 o=d.getObject('CapturedBottomV20');o.Shape=o.Shape.cut(Part.makeBox(190,275,22,A.Vector(205,315,16)))
def control_collision(d):d.getObject('ControlLeftFlipperInternalV27').Shape=Part.makeBox(60,35,70,A.Vector(18,150,280))
def plunger_hole(d):
 o=d.getObject('CapturedFrontPanelV20');o.Shape=o.Shape.cut(Part.makeCylinder(12,20,A.Vector(520,-1,215),A.Vector(0,1,0)))
def missing_door(d):d.removeObject('BackboxServiceDoorV14')
def inward_door(d):
 o=d.getObject('BackboxServiceDoorV14');b=o.Shape.BoundBox;s=o.Shape.copy();s.rotate(A.Vector(b.XMax,b.YMax,b.ZMin),A.Vector(0,0,1),105);d.getObject('BackboxDoorOpenV27').Shape=s
def cpu(d):d.getObject('ElectronicsLeftPayloadEnvelopeV27').Shape=Part.makeBox(110,300,110,A.Vector(180,830,153))
def central(d):d.getObject('ElectronicsLeftPayloadEnvelopeV27').Shape=Part.makeBox(110,300,110,A.Vector(230,300,131))
cases=[('gas geometry',gas,'no baseline gas geometry'),('one prop',one,'Right prop has positive pins keepers and stow capture'),('friction prop',friction,'Left prop has positive pins keepers and stow capture'),('missing positive keeper',keeper,'Left prop has positive pins keepers and stow capture'),('SSF through-hole',ssf_hole,'Front Left SSF retains full solid plywood'),('weakened bottom',weak_bottom,'bottom intake matches generic slots and filter grid'),('control collision',control_collision,'button and plunger envelopes clear cradle legs anchors and SSF'),('unmeasured plunger bore',plunger_hole,'front has no unmeasured coin/button/plunger cuts'),('missing backbox door',missing_door,'backbox service door BB-DOOR-001-R1 retained'),('inward backbox door',inward_door,'backbox door actual outward 105 degree transform'),('CPU obstruction',cpu,'carriers clear full CPU extraction sweep'),('central obstruction',central,'two narrow carriers preserve central service volume')]
with tempfile.TemporaryDirectory(prefix='vpin-owner-negative-') as td:
 for label,mutate,target in cases:
  d=A.openDocument(str(source));mutate(d);d.recompute();path=Path(td)/(label.replace(' ','-')+'.FCStd');d.saveAs(str(path));A.closeDocument(d.Name)
  d=A.openDocument(str(path));results={}
  verify(d,lambda name,passed,detail='':results.update({name:bool(passed)}));A.closeDocument(d.Name)
  assert target in results and not results[target],('wrong rejection',label,target)
  print('\nOWNER_GEOMETRY_NEGATIVE_PASS',label)
print('\nOWNER_GEOMETRY_NEGATIVE_TESTS_PASS')
