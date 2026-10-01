"""Reopen real saved study CAD and enforce accepted V32 regressions. CERN-OHL-S-2.0."""
from pathlib import Path
import FreeCAD as A,Part,json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/matrix-hinge-study-v32';report=json.loads((O/'validation.json').read_text());src=R/'exports/generated/notch-floor-fans-v32';d=A.openDocument(str(src/'play.FCStd'));old={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};checks=[]
def unchanged(a,b):return a.cut(b).Volume+b.cut(a).Volume<1e-5
for path in sorted(O.glob('gap-*.FCStd')):
 doc=A.openDocument(str(path));doc.recompute()
 for name,s in old.items():
  o=doc.getObject(name);assert o is not None and unchanged(s,o.Shape), (path.name,name)
 added=[o for o in doc.Objects if hasattr(o,'Shape') and o.Name not in old];assert len(added)==7 and all(o.Shape.isValid() and len(o.Shape.Solids)==1 for o in added), (path.name,len(added),[(o.Name,o.Shape.isValid(),len(o.Shape.Solids)) for o in added])
 checks.append({'check':path.name+' every accepted solid unchanged after reopening','pass':True});A.closeDocument(doc.Name)
for name in ['PF_BasePlywood','LeafButton_primary_L','FloorIntakeFanL','RemovableIntakeFilterL','FAN_230','PF_WoodDowel','PF_OpenCradleL','SHELF_2','PC_BASE','SSF_ExciterRearL']:
 if name not in old:
  if name=='SSF_ExciterRearL':name=next(n for n in old if 'Exciter' in n)
  else:raise KeyError(name)
 changed=old[name].copy();changed.translate(A.Vector(.1,0,0));assert not unchanged(old[name],changed), ('negative',name);checks.append({'check':'negative translated '+name+' is rejected','pass':True})
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in report['source_hashes'].items())
checks.append({'check':'accepted CAD, reviews, STEP and complete existing viewer bytes unchanged','pass':True})
fold=json.loads((R/'config/backbox_fold_v10.json').read_text());assert fold['cabinet']['outer_width_mm']==600 and fold['backbox']['outer_width_mm']==780 and fold['backbox']['hinge_floor_bolt_inset_each_side_mm']==59.8375
for key in ('final_hinge_hole_pattern','final_bushing_body_length_mm','final_bracket_bend_offsets_mm'):assert fold['backbox'][key] is None
for fn in ['docs/BACKBOX_FOLD_V10.md','docs/BACKBOX_HINGE_SHOPPING.md','docs/BACKBOX_MOUNTING_V12.md']:
 text=(R/fn).read_text();assert '580' not in text and '69.8375' not in text
for n,x in [('SIDE_L',0),('SIDE_R',582)]:
 ref=Part.makeCylinder(6.35,18,A.Vector(x,1308.1-38.1,508),A.Vector(1,0,0));vol=old[n].common(ref).Volume;assert vol>0.99*ref.Volume or vol<.01, ('pivot wood/hole partial',n,vol,ref.Volume)
 checks.append({'check':n+' WPC pivot reference is full wood or existing bore, not a partial edge overlap (no machining performed)','pass':True})
assert abs(old['PF_BackboxCheckEnvelope'].BoundBox.XLength-780)<1e-6
checks.append({'check':'current hinge widths/inset and null manufacturing authority audited','pass':True})
(O/'regression-validation.json').write_text(json.dumps({'checks':checks,'source_head':report['source_head'],'all_pass':True},indent=2)+'\n');print('MATRIX_REGRESSION_PASS',len(checks),flush=True)
