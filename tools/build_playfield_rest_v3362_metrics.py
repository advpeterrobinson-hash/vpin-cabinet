"""V33.6.2 accounting with exact changed B-rep volumes and inherited authorities.

CERN-OHL-S-2.0. Reuse the established mass/packing algorithm without running an
old output builder. Every redirected input is asserted exactly once; fail closed
if the reused implementation changes. These are non-production study outputs.
"""
from pathlib import Path
import hashlib
import json

R = Path(__file__).resolve().parents[1]
BASE = R / 'exports/generated/button-relief-v3361'
O = R / 'exports/generated/playfield-rest-v3362'


def read(path):
    return json.loads(Path(path).read_text())


def dump(name, value):
    (O / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


audit = read(O / 'manufacturing-audit.json')
assert audit['pass'] and audit['manufacturing_release'] is False
assert audit['native_geometry_sha256'] == hashlib.sha256((O / 'play.FCStd').read_bytes()).hexdigest()
reg = read(O / 'manufacturing-register.json')
parts = reg['parts']
assert (len(parts), len(reg['families']), reg['CNC_plywood_pieces']) == (101, 59, 97)
assert not reg['manufacturing_release']
prior_metrics = {p['instance_id']: p for p in read(BASE / 'packing-metrics.json')}
changed_metrics = {p['instance_id']: p for p in read(O / 'changed-piece-metrics.json')}
assert set(changed_metrics) == {a['instance_id'] for a in audit['changed_audits']}
metrics = {**prior_metrics, **changed_metrics}
assert set(metrics) == {p['instance_id'] for p in parts}
for p in parts:
    if p.get('manufacturing_class') == 'SHOP_MADE_SOLID_WOOD_PART':
        continue  # Shipping blank is intentionally distinct from the drilled B-rep.
    m = metrics[p['instance_id']]
    assert abs(m['volume_mm3'] - p['volume_mm3']) < 1e-4, p['instance_id']
    assert m['outer_area_mm2'] + 1e-4 >= m['projected_material_area_mm2'] > 0
    length, width = sorted(p['finished_xy_size_mm'], reverse=True)
    assert length <= 2460 and width <= 1560, ('STOP: individual sheet-fit failure', p['instance_id'])

# The physical hardware catalog and quantities do not change in this task.
# Assembly stage metadata is used only to keep related parts in the same bundle.
manual = O / 'assembly-manual.json'
if not manual.is_file():
    manual = BASE / 'assembly-manual.json'
engine = R / 'tools/build_solid_leg_metrics_v334.py'
source = engine.read_text()


def replace_once(old, new):
    global source
    assert source.count(old) == 1, ('Accounting reuse anchor changed', old)
    source = source.replace(old, new)


replace_once("O=R/'exports/generated/solid-leg-v334'", "O=R/'exports/generated/playfield-rest-v3362'")
replace_once("reg=read('exports/generated/solid-leg-v334/manufacturing-register.json')",
             "reg=read('exports/generated/playfield-rest-v3362/manufacturing-register.json')")
replace_once("metrics={p['instance_id']:p for p in read('exports/generated/assembly-v333/brep-metrics.json') if p['instance_id'] in byid}",
             "metrics={p['instance_id']:p for p in read('exports/generated/button-relief-v3361/packing-metrics.json') if p['instance_id'] in byid}\n"
             "metrics.update({p['instance_id']:p for p in read('exports/generated/playfield-rest-v3362/changed-piece-metrics.json')})")
replace_once("cat=read('config/hardware_catalog_v33.json')", "cat=read('config/hardware_catalog_v335.json')")
replace_once("manual=read('exports/generated/solid-leg-v334/assembly-manual.json')",
             f"manual=read({str(manual.relative_to(R))!r})")
replace_once("read('exports/generated/flatpack-v331/hardware-quantity-closure.json')",
             "read('exports/generated/structural-v335/hardware-quantity-closure.json')")
replace_once("v=vols.get(h['id']);q=h['quantity']",
             "v=vols.get(h['id']) if h['id'] not in ['F27','F57','F58','I10','I11'] else None;q=h['quantity']")
replace_once("print('V334_METRICS_PASS',summary)", "print('V3362_METRICS_ACCOUNTING',summary)")
exec(compile(source, str(engine), 'exec'), {'__file__': str(__file__)})

# The accounting engine's historical V33.1 comparison remains useful for audit,
# but current/prior fields must refer to the immediate V33.6.1 baseline.
material = read(O / 'material-utilization.json')
previous_material = read(BASE / 'material-utilization.json')
old_stocks = {s['thickness_mm']: s for s in previous_material['stocks']}
for stock in material['stocks']:
    old = old_stocks[stock['thickness_mm']]
    stock['historical_v331_row_layout_sheets'] = stock.pop('current_preliminary_sheets')
    stock['current_preliminary_sheets'] = old['improved_study_sheets']
    stock['previous_v3361_sheets'] = old['improved_study_sheets']
    stock['previous_v3361_outer_contour_area_mm2'] = old['outer_contour_area_mm2']
    stock['previous_v3361_projected_material_area_mm2'] = old['projected_material_area_mm2']
    stock['outer_contour_area_change_mm2'] = stock['outer_contour_area_mm2'] - old['outer_contour_area_mm2']
    stock['projected_material_area_change_mm2'] = stock['projected_material_area_mm2'] - old['projected_material_area_mm2']
material['version'] = 'V33.6.2'
material['previous_authority'] = 'exports/generated/button-relief-v3361/material-utilization.json'
dump('material-utilization.json', material)

old_mass = read(BASE / 'mass-budget.json')
new_mass = read(O / 'mass-budget.json')
comparison = {
    'version': 'V33.6.2',
    'baseline': 'V33.6.1',
    'manufacturing_release': False,
    'unchanged_counts': {'wood': 101, 'CNC_plywood': 97, 'SW01_shop_solids': 4, 'families': 59},
    'wood_volume_before_mm3': old_mass['wood_volume_mm3'],
    'wood_volume_after_mm3': new_mass['wood_volume_mm3'],
    'wood_volume_change_mm3': new_mass['wood_volume_mm3'] - old_mass['wood_volume_mm3'],
    'wood_shipping_mass_before_kg': old_mass['wood_flatpack_kg'],
    'wood_shipping_mass_after_kg': new_mass['wood_flatpack_kg'],
    'wood_shipping_mass_change_kg': [b-a for a, b in zip(old_mass['wood_flatpack_kg'], new_mass['wood_flatpack_kg'])],
    'scenario_order': new_mass['scenario_order'],
    'note': 'Actual B-rep volumes for CNC plywood; unchanged SW01 undrilled shipping blanks. Density assumptions are configurable. Unknown hardware remains unknown.',
}
dump('manufacturing-metrics-comparison.json', comparison)
dump('plywood-savings.json', {
    'version': 'V33.6.2', 'baseline': 'V33.6.1', 'retired_CNC_pieces': 0,
    'new_CNC_pieces': 0,
    'net_plywood_volume_change_mm3': comparison['wood_volume_change_mm3'],
    'outer_contour_area_change_mm2': sum(s['outer_contour_area_change_mm2'] for s in material['stocks']),
    'projected_material_area_change_mm2': sum(s['projected_material_area_change_mm2'] for s in material['stocks']),
    'preliminary_full_sheet_count_change': sum(s['improved_study_sheets']-s['previous_v3361_sheets'] for s in material['stocks']),
    'note': 'Signed changes: negative means less material than V33.6.1. No retired leg laminations or monitor stops are counted again. No production nesting.',
})

dependencies = [engine, BASE/'manufacturing-register.json', BASE/'packing-metrics.json',
                O/'manufacturing-register.json', O/'changed-piece-metrics.json', manual,
                R/'config/hardware_catalog_v335.json', R/'config/assembly_planning_v333.json',
                R/'config/solid_leg_blocks_v334.json', R/'config/manufacturing/profiles/peter_supplier_v1.json']
dump('metrics-authority.json', {
    'version': 'V33.6.2', 'production_authorized': False,
    'method': 'Previous exact unchanged metrics plus freshly audited changed B-reps; established deterministic rectangle packing with actual contour overlays.',
    'sources': [{'path': str(p.relative_to(R)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in dependencies],
    'no_geometry_modification': True, 'no_G_code': True,
})
assert read(O/'hardware-dashboard.json') == read(BASE/'hardware-dashboard.json')
assert all(b['gross_high_density_kg'] <= row['target_kg'] + 1e-6
           for row in read(O/'packaging.json')['candidates'] for b in row['bundles'])
print('V3362_METRICS_PASS', read(O/'project-metrics.json'))
