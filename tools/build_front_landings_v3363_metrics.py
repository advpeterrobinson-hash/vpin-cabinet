"""V33.6.3 accounting with exact changed B-rep volumes and inherited authorities.

CERN-OHL-S-2.0. Reuse the established mass/packing algorithm without running an
old output builder. Every redirected input is asserted exactly once; fail closed
if the reused implementation changes. These are non-production study outputs.
"""
from pathlib import Path
import hashlib
import json

R = Path(__file__).resolve().parents[1]
BASE = R / 'exports/generated/playfield-rest-v3362'
O = R / 'exports/generated/front-landings-v3363'


def read(path):
    return json.loads(Path(path).read_text())


def dump(name, value):
    (O / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


audit = read(O / 'manufacturing-audit.json')
assert audit['pass'] and audit['manufacturing_release'] is False
assert audit['native_geometry_sha256'] == hashlib.sha256((O / 'play.FCStd').read_bytes()).hexdigest()
assert audit['native_configuration_sha256'] == hashlib.sha256((R/'config/front_landings_v3363.json').read_bytes()).hexdigest()
assert audit['geometry_validation_sha256'] == hashlib.sha256((O/'geometry-validation.json').read_bytes()).hexdigest()
reg = read(O / 'manufacturing-register.json')
parts = reg['parts']
assert (len(parts), len(reg['families']), reg['CNC_plywood_pieces']) == (107, audit['canonical_families'], 103)
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

# Existing hardware stays unchanged; scoped landing hardware is append-only.
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


replace_once("O=R/'exports/generated/solid-leg-v334'", "O=R/'exports/generated/front-landings-v3363'")
replace_once("reg=read('exports/generated/solid-leg-v334/manufacturing-register.json')",
             "reg=read('exports/generated/front-landings-v3363/manufacturing-register.json')")
replace_once("metrics={p['instance_id']:p for p in read('exports/generated/assembly-v333/brep-metrics.json') if p['instance_id'] in byid}",
             "metrics={p['instance_id']:p for p in read('exports/generated/playfield-rest-v3362/packing-metrics.json') if p['instance_id'] in byid}\n"
             "metrics.update({p['instance_id']:p for p in read('exports/generated/front-landings-v3363/changed-piece-metrics.json')})")
replace_once("cat=read('config/hardware_catalog_v33.json')", "cat=read('config/hardware_catalog_v3363.json')")
replace_once("manual=read('exports/generated/solid-leg-v334/assembly-manual.json')",
             f"manual=read({str(manual.relative_to(R))!r})")
replace_once("read('exports/generated/flatpack-v331/hardware-quantity-closure.json')",
             "read('exports/generated/front-landings-v3363/hardware-quantity-closure.json')")
replace_once("v=vols.get(h['id']);q=h['quantity']",
             "v=vols.get(h['id']) if h['id'] not in ['F27','F57','F58','I10','I11'] else None;q=h['quantity']")
# The six new one-face CNC parts are delivered as exact outer-contour blanks.
# Reference hardware removals happen only after purchased-part qualification.
# Use their profile-extrusion volume for shipping/packing, never the bounding box.
replace_once("return metrics[p['instance_id']]['volume_mm3']*density/1e9",
             "return metrics[p['instance_id']].get('shipping_volume_mm3',metrics[p['instance_id']]['volume_mm3'])*density/1e9")
replace_once("woodvol=sum(p['volume_mm3'] for p in metrics.values())",
             "woodvol=sum(p.get('shipping_volume_mm3',p['volume_mm3']) for p in metrics.values())")
replace_once("cnc=[p for p in ps if p.get('manufacturing_class')!='SHOP_MADE_SOLID_WOOD_PART']",
             "cnc=[p for p in ps if p.get('manufacturing_class')!='SHOP_MADE_SOLID_WOOD_PART']\nfor p in ps:\n if p['source_component'].startswith('FrontLanding'):\n  metrics[p['instance_id']]['shipping_volume_mm3']=p['projected_area_mm2']*p['finished_reference_thickness_mm']\n  metrics[p['instance_id']]['shipping_geometry_authority']=p['cnc_stage_brep']")
replace_once("print('V334_METRICS_PASS',summary)", "print('V3363_METRICS_ACCOUNTING',summary)")
replace_once("stagemap={i:s['id'] for s in manual['stages'] for i in s['pieces']}",
             "stagemap={i:s['id'] for s in manual['stages'] for i in s['pieces']}\nstagemap.update({p['instance_id']:p.get('assembly_stage','05') for p in ps if p['instance_id'] not in stagemap})")
exec(compile(source, str(engine), 'exec'), {'__file__': str(__file__)})

# The accounting engine's historical V33.1 comparison remains useful for audit,
# but current/prior fields must refer to the immediate V33.6.2 baseline.
material = read(O / 'material-utilization.json')
previous_material = read(BASE / 'material-utilization.json')
old_stocks = {s['thickness_mm']: s for s in previous_material['stocks']}
for stock in material['stocks']:
    old = old_stocks[stock['thickness_mm']]
    stock['historical_v331_row_layout_sheets'] = stock.pop('current_preliminary_sheets')
    stock['current_preliminary_sheets'] = old['improved_study_sheets']
    stock['previous_v3362_sheets'] = old['improved_study_sheets']
    stock['previous_v3362_outer_contour_area_mm2'] = old['outer_contour_area_mm2']
    stock['previous_v3362_projected_material_area_mm2'] = old['projected_material_area_mm2']
    stock['outer_contour_area_change_mm2'] = stock['outer_contour_area_mm2'] - old['outer_contour_area_mm2']
    stock['projected_material_area_change_mm2'] = stock['projected_material_area_mm2'] - old['projected_material_area_mm2']
material['version'] = 'V33.6.3'
material['previous_authority'] = 'exports/generated/playfield-rest-v3362/material-utilization.json'
dump('material-utilization.json', material)

old_mass = read(BASE / 'mass-budget.json')
new_mass = read(O / 'mass-budget.json')
finished_added_volume=sum(m['volume_mm3'] for m in changed_metrics.values())
shipping_added_volume=sum(p['projected_area_mm2']*p['finished_reference_thickness_mm'] for p in parts if p['source_component'].startswith('FrontLanding'))
manual_stock=shipping_added_volume-finished_added_volume
planning=read(R/'config/assembly_planning_v333.json')
densities=planning['densities_kg_m3']['plywood']
new_mass['new_landing_finished_reference_volume_mm3']=finished_added_volume
new_mass['new_landing_delivered_blank_volume_mm3']=shipping_added_volume
new_mass['new_landing_manual_stock_allowance_mm3']=manual_stock
new_mass['new_landing_manual_stock_allowance_kg']=[manual_stock*d/1e9 for d in densities]
new_mass['wood_finished_reference_kg']=[m-a for m,a in zip(new_mass['wood_flatpack_kg'],new_mass['new_landing_manual_stock_allowance_kg'])]
new_mass['wood_finished_reference_volume_mm3']=new_mass['wood_volume_mm3']-manual_stock
new_mass['wood_status']='PLANNING: existing reference CNC volumes plus unchanged SW01 shipping blanks; new landing delivery uses actual CNC-stage profile-extrusion volume before hardware-dependent manual bores'
new_mass['packing_mass_rule']='New landing manual-removal stock retained in all packing scenarios; no omitted bore-removal allowance near bundle mass target'
dump('mass-budget.json',new_mass)
comparison = {
    'version': 'V33.6.3',
    'baseline': 'V33.6.2',
    'manufacturing_release': False,
    'counts_before': {'wood': 101, 'CNC_plywood': 97, 'SW01_shop_solids': 4, 'families': 59},
    'counts_after': {'wood':len(parts), 'CNC_plywood':reg['CNC_plywood_pieces'], 'SW01_shop_solids':4, 'families':len(reg['families'])},
    'new_landing_finished_reference_volume_mm3':finished_added_volume,
    'new_landing_delivered_blank_volume_mm3':shipping_added_volume,
    'wood_finished_reference_after_kg':new_mass['wood_finished_reference_kg'],
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
    'version': 'V33.6.3', 'baseline': 'V33.6.2', 'retired_CNC_pieces': 0,
    'new_CNC_pieces': 6,
    'net_plywood_volume_change_mm3': finished_added_volume,
    'net_finished_plywood_volume_change_mm3': finished_added_volume,
    'net_delivered_plywood_volume_change_mm3':shipping_added_volume,
    'outer_contour_area_change_mm2': sum(s['outer_contour_area_change_mm2'] for s in material['stocks']),
    'projected_material_area_change_mm2': sum(s['projected_material_area_change_mm2'] for s in material['stocks']),
    'preliminary_full_sheet_count_change': sum(s['improved_study_sheets']-s['previous_v3362_sheets'] for s in material['stocks']),
    'note': 'Signed changes: negative means less material than V33.6.2. No retired leg laminations or monitor stops are counted again. No production nesting.',
})

dashboard=read(O/'project-metrics.json');dashboard.update(wood_finished_reference_mass_kg=new_mass['wood_finished_reference_kg'][1],wood_shipping_mass_kg=new_mass['wood_flatpack_kg'][1],wood_mass_basis='DELIVERED_BLANK_ALLOWANCE_INCLUDED_FOR_NEW_LANDINGS');dump('project-metrics.json',dashboard)

dependencies = [Path(__file__), engine, O/'manufacturing-audit.json', O/'geometry-validation.json', R/'config/front_landings_v3363.json', BASE/'manufacturing-register.json', BASE/'packing-metrics.json',
                O/'manufacturing-register.json', O/'changed-piece-metrics.json', manual,
                R/'config/hardware_catalog_v3363.json', R/'config/assembly_planning_v333.json',
                R/'config/solid_leg_blocks_v334.json', R/'config/manufacturing/profiles/peter_supplier_v1.json']
dump('metrics-authority.json', {
    'version': 'V33.6.3', 'production_authorized': False,
    'method': 'Previous exact unchanged metrics plus freshly audited changed B-reps; established deterministic rectangle packing with actual contour overlays.',
    'sources': [{'path': str(p.relative_to(R)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in dependencies],
    'no_geometry_modification_by_accounting': True, 'no_G_code': True,
})
assert read(O/'hardware-dashboard.json')['total_hardware_families'] > read(BASE/'hardware-dashboard.json')['total_hardware_families']
assert all(b['gross_high_density_kg'] <= row['target_kg'] + 1e-6
           for row in read(O/'packaging.json')['candidates'] for b in row['bundles'])
print('V3363_METRICS_PASS', read(O/'project-metrics.json'))
