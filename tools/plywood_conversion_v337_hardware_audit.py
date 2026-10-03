"""Read-only explicit hardware/reserve audit with rejected no-rebate control.
CERN-OHL-S-2.0. https://github.com/advpeterrobinson-hash/vpin-cabinet
"""
from pathlib import Path
import sys,json,hashlib
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,box
O=R/'exports/generated/two-stock-user-module-v337';C=json.loads((R/'config/plywood_conversion_v337.json').read_text());old=load(R/C['source']);new=load(O/'conversion.FCStd');g=json.loads((O/'conversion-validation.json').read_text());hh=[]
for n in g['promoted_breps']:
 delta=new[n].cut(old[n])
 if delta.Volume<1e-6:continue
 for k,t in old.items():
  if k==n or not delta.BoundBox.intersect(t.BoundBox):continue
  v=delta.common(t).Volume
  if v>1e-5:hh.append({'converted_part':n,'preserved_part':k,'volume_mm3':v})
no_rebate=new['BB_IntakeDownBaffleL'].fuse(box(244,1274.1,686,3,36,32));negative=no_rebate.common(old['BB_PassiveBoltBodyReserve0']).Volume
gap=new['BB_IntakeDownBaffleL'].distToShape(old['BB_PassiveBoltBodyReserve0'])[0]
report={'pass':not hh and abs(negative-660)<1e-5 and abs(gap-2)<1e-5,'conversion_sha256':hashlib.sha256((O/'conversion.FCStd').read_bytes()).hexdigest(),'current_added_wood_hits':hh,'scope':'Every preserved source B-rep including ALL reserve names; only changed component itself excluded','negative_control':{'name':'Remove lower-edge rebate','expected':'FAIL','overlap_mm3':negative,'parts':['BB_IntakeDownBaffleL','BB_PassiveBoltBodyReserve0']},'final_passive_bolt_body_gap_mm':gap,'manufacturing_release':False}
(O/'conversion-reserve-audit.json').write_text(json.dumps(report,indent=2)+'\n');assert report['pass'],report;print('V337_HARDWARE_RESERVE_PASS',flush=True)
