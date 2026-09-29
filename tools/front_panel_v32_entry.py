"""Saved-solid front layout proposal; source V32 is read-only. CERN-OHL-S-2.0."""
import json, math
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];C=json.loads((R/'config/front_panel_v32.json').read_text());O=R/'exports/generated/front-panel-v32';O.mkdir(parents=True,exist_ok=True)
def box(v):return Part.makeBox(*v[3:],A.Vector(*v[:3]))
def bore(x,z,r):return Part.makeCylinder(r,20,A.Vector(x,-1,z),A.Vector(0,1,0))
bas=A.openDocument(str(R/C['source_geometry']));d=A.newDocument('FrontPanelV32Proposal')
for old in bas.Objects:
 if not hasattr(old,'Shape'):continue
 obj=d.addObject('PartDesign::Feature',old.Name);obj.Shape=old.Shape.copy();obj.Label=old.Label
 for prop in ['PartCode','LegacyId','PartStatus','NameEN','NamePTBR','Category']:
  obj.addProperty('App::PropertyString',prop);setattr(obj,prop,getattr(old,prop))
f=C['front'];panel=box([f['x'],0,0,f['width'],f['thickness'],f['height']]);x,z,w,h=C['coin_opening'];panel=panel.cut(box([x,-1,z,w,20,h]))
for x,z in C['coin_fasteners_xz']:panel=panel.cut(bore(x,z,C['coin_fastener_radius']))
for b in C['buttons']:panel=panel.cut(bore(b['x'],b['z'],C['button_bore_diameter']/2))
d.getObject('FRONT').Shape=panel
d.getObject('FRONT').Label='Front - control layout PROPOSAL / nominal holes only'
# The pre-existing plunger reservation is part of the proposed change, not a bore.
x,z=C['plunger_center_xz'];d.getObject('PLUNGER_RESERVED').Shape=box([x-18,18,z-18,36,202,36])
d.recompute();path=O/'front-layout-proposal.FCStd';d.saveAs(str(path));A.closeDocument(d.Name)
d=A.openDocument(str(path));d.recompute()
def validate(doc):
 obs={o.Name:o for o in doc.Objects if hasattr(o,'Shape')};old={o.Name:o for o in bas.Objects if hasattr(o,'Shape')};p=obs['FRONT'].Shape;checks=[]
 def ck(n,v):checks.append({'check':n,'pass':bool(v)})
 ck('same 45 object identities',set(obs)==set(old) and len(obs)==45)
 ck('all shapes valid single solids and recomputed',all(o.Shape.isValid() and len(o.Shape.Solids)==1 and not any('Invalid' in str(s) for s in o.State) for o in obs.values()))
 changed={n for n,o in obs.items() if o.Shape.cut(old[n].Shape).Volume+old[n].Shape.cut(o.Shape).Volume>1e-5}
 ck('only front and plunger reservation change',changed=={'FRONT','PLUNGER_RESERVED'})
 ck('front dimensions retained',all(abs(a-b)<1e-6 for a,b in zip([p.BoundBox.XMin,p.BoundBox.XLength,p.BoundBox.YLength,p.BoundBox.ZLength],[18,564,18,400.05])))
 x,z,w,h=C['coin_opening'];ck('coin aperture retained',p.common(box([x,-1,z,w,20,h])).Volume<1e-6)
 for i,b in enumerate(C['buttons']):
  ck('button bore '+b['name'],p.common(bore(b['x'],b['z'],C['button_bore_diameter']/2)).Volume<1e-6)
  # Probe surrounding annulus: rejects an enlarged hole or a missing panel region.
  ann=bore(b['x'],b['z'],C['button_bore_diameter']/2+2).cut(bore(b['x'],b['z'],C['button_bore_diameter']/2))
  ck('wood around '+b['name'],abs(p.common(ann).Volume-math.pi*((C['button_bore_diameter']/2+2)**2-(C['button_bore_diameter']/2)**2)*18)<1e-4)
 for x,z in C['coin_fasteners_xz']:ck('coin fastener '+str((x,z)),p.common(bore(x,z,C['coin_fastener_radius'])).Volume<1e-6)
 x,z=C['plunger_center_xz'];ck('plunger reserve new center',abs(obs['PLUNGER_RESERVED'].Shape.BoundBox.XMin-(x-18))<1e-6 and abs(obs['PLUNGER_RESERVED'].Shape.BoundBox.ZMin-(z-18))<1e-6)
 ck('plunger panel deliberately uncut',abs(p.common(box([x-18,0,z-18,36,18,36])).Volume-36*18*36)<1e-4)
 return checks
checks=validate(d);assert all(c['pass'] for c in checks),checks
items=[o for o in d.Objects if hasattr(o,'Shape')]
collisions=[{'a':a.Name,'b':b.Name,'mm3':a.Shape.common(b.Shape).Volume} for i,a in enumerate(items) for b in items[i+1:] if a.Shape.common(b.Shape).Volume>.01]
assert not collisions,collisions
checks.append({'check':'saved proposal has no positive-volume solid overlaps','pass':True})
# Screen assumed hardware volumes against saved V32 neighbors. Findings remain open.
envs={b['name']:Part.makeCylinder(C['button_internal_radius'],C['button_internal_depth_with_cable'],A.Vector(b['x'],18,b['z']),A.Vector(0,1,0)) for b in C['buttons']}
envs['Plunger']=box(C['plunger_internal_box'])
x,z,w,h=C['coin_opening'];m=C['coin_screening_flange_margin'];envs['Coin door screening']=box([x-m,18,z-m,w+2*m,C['coin_screening_depth'],h+2*m])
findings=[]
for label,s in envs.items():
 for o in d.Objects:
  if o.Name in ['FRONT','PLUNGER_RESERVED'] or not hasattr(o,'Shape'):continue
  v=s.common(o.Shape).Volume
  if v>.01:findings.append(dict(envelope=label,object=o.Name,intersection_mm3=v))
# Negative controls prove missing holes, oversized holes, neighbor changes and plunger drift reject.
neg=[]
for label,name,mutate in [
 ('filled launch','FRONT',lambda s:s.fuse(bore(520,210,12.7).common(box([18,0,0,564,18,400.05])))),
 ('oversize button','FRONT',lambda s:s.cut(bore(90,310,16))),
 ('shelf drift','SHELF_1',lambda s:s.translated(A.Vector(0,1,0))),
 ('plunger drift','PLUNGER_RESERVED',lambda s:s.translated(A.Vector(0,0,1)))]:
 o=d.getObject(name);original=o.Shape.copy();o.Shape=mutate(original.copy());d.recompute();failed=[c['check'] for c in validate(d) if not c['pass']];assert failed,label;neg.append(dict(case=label,rejected_by=failed));o.Shape=original;d.recompute()
assert all(c['pass'] for c in validate(d))
report=dict(status=C['status'],manufacturing_ready=False,checks=checks,negative_controls=neg,assumed_envelope_conflicts=findings,front_depth_to_S1_mm=d.getObject('SHELF_1').Shape.BoundBox.YMin-18,source_geometry_unchanged=True)
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
A.closeDocument(d.Name);A.closeDocument(bas.Name)
print('FRONT_STUDY_PASS',len(checks),'checks;',len(neg),'negative controls; OPEN_SCREENING_CONFLICTS',findings)
