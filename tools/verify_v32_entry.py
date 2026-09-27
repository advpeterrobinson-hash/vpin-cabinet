"""Verify saved V32 geometry and metadata; never certify manufacturing readiness."""
import json
import os
from pathlib import Path
import FreeCAD as App

root = Path(__file__).resolve().parents[1]
out = root / 'exports/generated/cabinet-v32'
g = json.loads((out / 'geometry.json').read_text())
doc = App.openDocument(os.environ.get('VPIN_V32_DOCUMENT', str(out / 'vpin-central-v32.FCStd')))
doc.recompute()
objects = {o.Name: o for o in doc.Objects if hasattr(o, 'Shape')}
assert len(objects) == len(g['parts']) == 45
assert not g['manufacturing_ready'] and g['collisions'] == []
codes = []
for p in g['parts']:
    o = objects[p['id']]
    assert o.Shape.isValid() and len(o.Shape.Solids) == 1, o.Name
    assert not any('Invalid' in str(s) for s in o.State), o.Name
    assert o.LegacyId == p['id'] and o.PartCode == p['part_code']
    assert o.NameEN == p['name_en'] and o.NamePTBR == p['name_pt_br']
    assert o.NameEN and o.NamePTBR and o.PartStatus == p['part_status']
    assert o.Label == ((o.PartCode + ' - ') if o.PartCode else '**PROVISIONAL** - ') + o.NameEN
    assert abs(o.Shape.Volume - p['volume']) < 1e-5
    b = o.Shape.BoundBox
    assert all(abs(a-b) < 1e-6 for a,b in zip(p['bounds'], [b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax]))
    if o.PartCode: codes.append(o.PartCode)
assert len(codes) == len(set(codes))
assert {'S1','S2','S3','T1','T2','T3','PCBase'} <= set(codes)
collisions = []
items = list(objects.items())
for i,(a,sa) in enumerate(items):
    for b,sb in items[i+1:]:
        volume = sa.Shape.common(sb.Shape).Volume
        if volume > .01: collisions.append({'a':a, 'b':b, 'mm3':volume})
assert not collisions, collisions
baseline = os.environ.get('VPIN_V32_BASELINE')
assert baseline, 'VPIN_V32_BASELINE must name the saved pre-build FCStd'
old = App.openDocument(baseline)
previous = {o.Name:o for o in old.Objects if hasattr(o,'Shape')}
assert set(objects) == set(previous), 'Object set changed'
changes = []
for name,o in objects.items():
    other = previous[name].Shape
    difference = o.Shape.cut(other).Volume + other.cut(o.Shape).Volume
    if difference > 1e-5: changes.append({'id':name, 'symmetric_difference_mm3':difference})
assert not changes, 'GEOMETRY CHANGE REQUIRES REVIEW: ' + str(changes)
result = dict(version='V32', solid_count=45, valid_solids=True,
              positive_volume_intersections=collisions, intersection_threshold_mm3=.01,
              shelves=sum(o.Category=='shelf' for o in objects.values()),
              crossmembers=sum(o.Category=='brace' for o in objects.values()),
              fans=sum(o.Category=='fan' for o in objects.values()),
              bilingual_labels=True, manufacturing_ready=False,
              metadata_verified_in_saved_fcstd=True, geometry_changes_from_baseline=changes,
              tests_not_performed=['load analysis','physical assembly','monitor and backbox opening sweep',
                                   'thermal testing','CSD mounting fit','machining validation'])
assert (result['shelves'], result['crossmembers'], result['fans']) == (3,3,2)
(out/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
App.closeDocument(old.Name)
App.closeDocument(doc.Name)
print('V32_VERIFIED 45 valid solids; collisions=[]; geometry_changes=[]; metadata verified')
