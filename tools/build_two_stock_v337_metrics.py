"""V33.7 accounting with exact changed B-rep volumes and inherited authorities.

CERN-OHL-S-2.0. Reuse the established mass/packing algorithm without running an
old output builder. Every redirected input is asserted exactly once; fail closed
if the reused implementation changes. These are non-production study outputs.
"""
from pathlib import Path
import hashlib
import json

R = Path(__file__).resolve().parents[1]
BASE = R / 'exports/generated/front-landings-v3363'
O = R / 'exports/generated/two-stock-user-module-v337'


def read(path):
    return json.loads(Path(path).read_text())


def dump(name, value):
    (O / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


audit = read(O / 'manufacturing-audit.json')
assert audit['pass'] and audit['manufacturing_release'] is False
assert audit['native_geometry_sha256'] == hashlib.sha256((O / 'play.FCStd').read_bytes()).hexdigest()
assert audit['native_configuration_sha256'] == hashlib.sha256((R/'config/underfront_user_module_v337.json').read_bytes()).hexdigest()
assert audit['geometry_validation_sha256'] == hashlib.sha256((O/'geometry-validation.json').read_bytes()).hexdigest()
reg = read(O / 'manufacturing-register.json')
parts = reg['parts']
assert (len(parts), len(reg['families']), reg['CNC_plywood_pieces']) == (108, audit['canonical_families'], 104)
assert not reg['manufacturing_release']
assert {p['nominal_stock_thickness_mm'] for p in parts if p.get('manufacturing_class')!='SHOP_MADE_SOLID_WOOD_PART'}=={12,18}
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

# Existing hardware stays unchanged; scoped underfront module hardware is append-only.
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


replace_once("O=R/'exports/generated/solid-leg-v334'", "O=R/'exports/generated/two-stock-user-module-v337'")
replace_once("reg=read('exports/generated/solid-leg-v334/manufacturing-register.json')",
             "reg=read('exports/generated/two-stock-user-module-v337/manufacturing-register.json')")
replace_once("metrics={p['instance_id']:p for p in read('exports/generated/assembly-v333/brep-metrics.json') if p['instance_id'] in byid}",
             "metrics={p['instance_id']:p for p in read('exports/generated/front-landings-v3363/packing-metrics.json') if p['instance_id'] in byid}\n"
             "metrics.update({p['instance_id']:p for p in read('exports/generated/two-stock-user-module-v337/changed-piece-metrics.json')})")
replace_once("cat=read('config/hardware_catalog_v33.json')", "cat=read('config/hardware_catalog_v337.json')")
replace_once("manual=read('exports/generated/solid-leg-v334/assembly-manual.json')",
             f"manual=read({str(manual.relative_to(R))!r})")
replace_once("read('exports/generated/flatpack-v331/hardware-quantity-closure.json')",
             "read('exports/generated/two-stock-user-module-v337/hardware-quantity-closure.json')")
replace_once("v=vols.get(h['id']);q=h['quantity']",
             "v=vols.get(h['id']) if h['id'] not in ['F27','F57','F58','I10','I11'] else None;q=h['quantity']")
# Preserve actual CNC-stage volumes when manual finishing remains; other reference
# B-rep volumes are inherited. Never substitute bounding-box volume.
replace_once("return metrics[p['instance_id']]['volume_mm3']*density/1e9",
             "return metrics[p['instance_id']].get('shipping_volume_mm3',metrics[p['instance_id']]['volume_mm3'])*density/1e9")
replace_once("woodvol=sum(p['volume_mm3'] for p in metrics.values())",
             "woodvol=sum(p.get('shipping_volume_mm3',p['volume_mm3']) for p in metrics.values())")
replace_once("print('V334_METRICS_PASS',summary)", "print('V337_METRICS_ACCOUNTING',summary)")
replace_once("stagemap={i:s['id'] for s in manual['stages'] for i in s['pieces']}",
             "stagemap={i:s['id'] for s in manual['stages'] for i in s['pieces']}\nstagemap.update({p['instance_id']:p.get('assembly_stage','05') for p in ps if p['instance_id'] not in stagemap})")
exec(compile(source, str(engine), 'exec'), {'__file__': str(__file__)})

# The accounting engine's historical V33.1 comparison remains useful for audit,
# but current/prior fields must refer to the immediate V33.6.3 baseline.
material = read(O / 'material-utilization.json')
previous_material = read(BASE / 'material-utilization.json')
old_stocks = {s['thickness_mm']: s for s in previous_material['stocks']}
for stock in material['stocks']:
    old = old_stocks[stock['thickness_mm']]
    stock['historical_v331_row_layout_sheets'] = stock.pop('current_preliminary_sheets')
    stock['current_preliminary_sheets'] = old['improved_study_sheets']
    stock['previous_v3363_sheets'] = old['improved_study_sheets']
    stock['previous_v3363_outer_contour_area_mm2'] = old['outer_contour_area_mm2']
    stock['previous_v3363_projected_material_area_mm2'] = old['projected_material_area_mm2']
    stock['outer_contour_area_change_mm2'] = stock['outer_contour_area_mm2'] - old['outer_contour_area_mm2']
    stock['projected_material_area_change_mm2'] = stock['projected_material_area_mm2'] - old['projected_material_area_mm2']
material['retired_plywood_stock_families_mm']=[6,8]
material['previous_total_preliminary_sheets']=sum(s['improved_study_sheets'] for s in previous_material['stocks'])
material['active_plywood_stock_families_mm']=[12,18]
material['version'] = 'V33.7'
material['previous_authority'] = 'exports/generated/front-landings-v3363/material-utilization.json'
dump('material-utilization.json', material)

old_mass = read(BASE / 'mass-budget.json')
new_mass = read(O / 'mass-budget.json')
planning=read(R/'config/assembly_planning_v333.json')
densities=planning['densities_kg_m3']['plywood']
all_metrics={m['instance_id']:m for m in read(O/'packing-metrics.json')}
manual_stock=sum(m.get('shipping_volume_mm3',m['volume_mm3'])-m['volume_mm3'] for m in all_metrics.values())
new_mass['manual_stock_allowance_mm3']=manual_stock
new_mass['manual_stock_allowance_kg']=[manual_stock*d/1e9 for d in densities]
solid_removed_volume=sum(all_metrics[p['instance_id']]['volume_mm3']-p['volume_mm3'] for p in parts if p.get('manufacturing_class')=='SHOP_MADE_SOLID_WOOD_PART')
new_mass['solid_blank_to_finished_removal_mm3']=solid_removed_volume
new_mass['wood_finished_reference_volume_mm3']=new_mass['wood_volume_mm3']-manual_stock-solid_removed_volume
new_mass['plywood_shipping_kg']=new_mass['plywood_only_kg']
new_mass['plywood_finished_reference_kg']=[m-a for m,a in zip(new_mass['plywood_only_kg'],new_mass['manual_stock_allowance_kg'])]
for key in ('installed_wood_kg','mechanical_scenario_kg','full_planning_build_kg'):
 new_mass[key]=[m-a for m,a in zip(new_mass[key],new_mass['manual_stock_allowance_kg'])]
new_mass['wood_finished_reference_kg']=new_mass['installed_wood_kg']
new_mass['wood_status']='PLANNING: actual finished B-reps and actual CNC-stage shipping B-reps where manual finishing remains; SW01 shipping blanks remain separate from finished drilled volume'
new_mass['packing_mass_rule']='Hardware-dependent manual-removal stock retained in all packing scenarios; no omitted allowance near bundle mass target'
dump('mass-budget.json',new_mass)
baseline_finished_volume=sum(p['volume_mm3'] for p in read(BASE/'manufacturing-register.json')['parts'])
assert abs(new_mass['wood_finished_reference_volume_mm3']-sum(p['volume_mm3'] for p in parts))<1e-4
finished_delta=new_mass['wood_finished_reference_volume_mm3']-baseline_finished_volume
shipping_delta=new_mass['wood_volume_mm3']-old_mass['wood_volume_mm3']
comparison = {
    'version': 'V33.7',
    'baseline': 'V33.6.3',
    'manufacturing_release': False,
    'counts_before': {'wood': 107, 'CNC_plywood': 103, 'SW01_shop_solids': 4, 'families': 65},
    'counts_after': {'wood':len(parts), 'CNC_plywood':reg['CNC_plywood_pieces'], 'SW01_shop_solids':4, 'families':len(reg['families'])},
    'finished_reference_volume_change_mm3':finished_delta,
    'delivered_volume_change_mm3':shipping_delta,
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
    'version': 'V33.7', 'baseline': 'V33.6.3', 'retired_CNC_pieces': 0,
    'new_CNC_pieces': 1,
    'net_plywood_volume_change_mm3': finished_delta,
    'net_finished_plywood_volume_change_mm3': finished_delta,
    'net_delivered_plywood_volume_change_mm3':shipping_delta,
    'outer_contour_area_change_mm2': sum(s['outer_contour_area_mm2'] for s in material['stocks'])-sum(s['outer_contour_area_mm2'] for s in previous_material['stocks']),
    'projected_material_area_change_mm2': sum(s['projected_material_area_mm2'] for s in material['stocks'])-sum(s['projected_material_area_mm2'] for s in previous_material['stocks']),
    'preliminary_full_sheet_count_change': sum(s['improved_study_sheets'] for s in material['stocks'])-sum(s['improved_study_sheets'] for s in previous_material['stocks']),
    'note': 'Signed changes: negative means less material than V33.6.3. No retired leg laminations or monitor stops are counted again. No production nesting.',
})

packing_policy=read(R/'config/packaging_v337.json');pack=read(O/'packaging.json')
assert sorted(c['target_kg'] for c in pack['candidates'])==packing_policy['study_targets_kg']
pack['preferred_target_kg']=packing_policy['preferred_target_kg']
pack['practical_handling_ceiling_kg']=packing_policy['practical_handling_ceiling_kg']
preferred=next(c for c in pack['candidates'] if c['target_kg']==pack['preferred_target_kg'])
previous_preferred=next(c for c in pack['candidates'] if c['target_kg']==25)
def footprint_area(candidate):return sum(b['external_LWH_mm'][0]*b['external_LWH_mm'][1] for b in candidate['bundles'])
def box_volume(candidate):return sum(__import__('math').prod(b['external_LWH_mm']) for b in candidate['bundles'])
pack['preference_review']={'authority':'config/packaging_v337.json','reason':packing_policy['reason'],'tradeoffs':packing_policy['tradeoffs'],
 'same_bundle_count_as25kg':preferred['bundle_count']==previous_preferred['bundle_count'],
 'minimum_margin_below25kg_kg':min(25-b['gross_high_density_kg'] for b in preferred['bundles']),
 'total_footprint_change_vs25kg_percent':100*(footprint_area(preferred)/footprint_area(previous_preferred)-1),
 'total_box_volume_change_vs25kg_percent':100*(box_volume(preferred)/box_volume(previous_preferred)-1)}
dump('packaging.json',pack)
dashboard=read(O/'project-metrics.json');dashboard.update(wood_finished_reference_mass_kg=new_mass['wood_finished_reference_kg'][1],wood_shipping_mass_kg=new_mass['wood_flatpack_kg'][1],wood_mass_basis='ACTUAL_CNC_STAGE_WITH_MANUAL_FINISH_ALLOWANCE');dump('project-metrics.json',dashboard)

dependencies = [Path(__file__), engine, R/'tools/validate_plywood_stock_v337.py', R/'config/packaging_v337.json', O/'stock-policy-negative-control.json', O/'manufacturing-audit.json', O/'geometry-validation.json', R/'config/underfront_user_module_v337.json', R/'config/manufacturing/stock_policy_v337.json', BASE/'manufacturing-register.json', BASE/'packing-metrics.json',
                O/'manufacturing-register.json', O/'changed-piece-metrics.json', manual,
                R/'config/hardware_catalog_v337.json', R/'config/assembly_planning_v333.json',
                R/'config/solid_leg_blocks_v334.json', R/'config/manufacturing/profiles/peter_supplier_v1.json']
dump('metrics-authority.json', {
    'version': 'V33.7', 'production_authorized': False,
    'method': 'Previous exact unchanged metrics plus freshly audited changed B-reps; established deterministic rectangle packing with actual contour overlays.',
    'sources': [{'path': str(p.relative_to(R)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in dependencies],
    'no_geometry_modification_by_accounting': True, 'no_G_code': True,
})
assert read(O/'hardware-dashboard.json')['total_hardware_families'] > read(BASE/'hardware-dashboard.json')['total_hardware_families']
assert all(b['gross_high_density_kg'] <= row['target_kg'] + 1e-6
           for row in read(O/'packaging.json')['candidates'] for b in row['bundles'])
lines=['# V33.7 material, mass and packing study','','PRELIMINARY — NOT FOR CNC. No production nesting, CAM or G-code. Full-sheet release remains blocked by measured stock, coupon, selected fit, purchased hardware and physical qualification.','','Active plywood purchase families are nominal12 mm and18 mm only; actual production-lot thickness remains unknown. Four SW01 solid-wood leg blanks are separate. M045 retains its6 mm finished web through one-face reduction from12 mm stock, so it does not introduce a6 mm purchase family.','','| Nominal stock | Pieces | Outer area m² | Net projected area m² | Full sheets | Net utilization | Gross waste incl. offcuts | Reusable rectangular offcuts m² |','|---|---:|---:|---:|---:|---:|---:|---:|']
for q in material['stocks']:
 lines.append(f"| {q['thickness_mm']:g} mm | {q['pieces']} | {q['outer_contour_area_mm2']/1e6:.4f} | {q['projected_material_area_mm2']/1e6:.4f} | {q['improved_study_sheets']} | {q['utilization_percent_net']:.2f}% | {q['waste_percent_gross_including_offcuts']:.2f}% | {q['reusable_rectangular_offcut_area_mm2']/1e6:.4f} |")
lines+=['','The full-sheet projection is an accounting assumption. The deterministic layout tries three rectangle orderings with actual contour overlays; it is not an optimized or production nest. It preserves20 mm sheet borders and reserves15 mm between finished boundaries. Spacing allocation is not cutter kerf, and contour/cutout scraps are not automatically reusable. Nest small12 mm members into the same thickness batch first; use qualified premium offcuts/cut-to-size stock if available. Do not downgrade structural members or mix nominal thickness families.']
for q in material['stocks']:lines+=['',f"Practical procurement study for {q['thickness_mm']:g} mm: {q['practical_stock_rectangles_mm']} mm rectangles; supplier hold-down/defect approval still required."]
lines+=['','| Mass basis | LOW kg | NOMINAL kg | HIGH kg |','|---|---:|---:|---:|']
for key,label in [('wood_flatpack_kg','Delivered wood, including unfinished manual-removal stock'),('installed_wood_kg','Finished installed wood'),('mechanical_scenario_kg','Mechanical planning scenario incl. explicit unknown-hardware allowance'),('full_planning_build_kg','Full planning scenario incl. glass/future electronics')]:
 lines.append('| '+label+' | '+' | '.join(f'{v:.3f}' for v in new_mass[key])+' |')
lines+=['','Plywood density is configurable LOW/NOMINAL/HIGH; nominal650 kg/m³. Solid wood uses its separate material assumptions. New purchased hardware mass remains UNKNOWN, not zero or certified by a visual envelope.']
pack=read(O/'packaging.json');preferred=next(x for x in pack['candidates'] if x['target_kg']==pack['preferred_target_kg'])
lines+=['','Preferred20 kg-target wood bundles provide about5 kg allowance below the25 kg practical ceiling at HIGH density plus estimated protection, without increasing the four-bundle count. Long-panel footprints/protection are retained; total footprint grows1.61% and aggregate box volume4.21% versus the25 kg candidate. The mixed small-part bundle is taller/wider and requires stack-stability/identification qualification. This is a handling projection, not transit qualification. Hardware, glass and electronics remain separate.','','| Package | External dimensions mm | Wood nominal kg | Gross HIGH kg |','|---|---|---:|---:|']
for b in preferred['bundles']:
 lines.append(f"| {b.get('id',b.get('package_id'))} | {b['external_LWH_mm']} | {b['wood_mass_kg']:.3f} | {b['gross_high_density_kg']:.3f} |")
(O/'stock-mass-packing-report.md').write_text('\n'.join(lines)+'\n')
print('V337_METRICS_PASS', read(O/'project-metrics.json'))
