"""Bilingual V33.8 review entry points from authoritative evidence.
CERN-OHL-S-2.0; no manufacturing release.
"""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/service-productization-v338'
def read(n):return json.loads((O/n).read_text())
g=read('geometry-validation.json');a=read('adjustment-validation.json');v=read('validation.json');reg=read('manufacturing-register.json');m=read('mass-budget.json');mat=read('material-utilization.json');pack=read('packaging.json');hw=read('hardware-dashboard.json');load=read('SW02-load-screen.json');mod=read('modularity-validation.json');safety=read('safety-validation.json')
plan=next(q for q in pack['candidates'] if q['target_kg']==pack['preferred_target_kg']);worst=load['scenarios'][-1]
stockrows='\n'.join(f"| {s['thickness_mm']} mm | {s['pieces']} | {s['outer_contour_area_mm2']/1e6:.6f} | {s['improved_study_sheets']} | {s['utilization_percent_net']:.2f}% |" for s in mat['stocks'])
packrows='\n'.join(f"| {b.get('id',b.get('package_id','Bundle'))} | {' × '.join(str(round(x,1)) for x in b['external_LWH_mm'])} | {b['wood_mass_kg']:.3f} | {b['gross_high_density_kg']:.3f} |" for b in plan['bundles'])
txt=f'''# V33.8 — solid front landings and service/modularity review

**Design candidate promoted; full-sheet CNC remains BLOCKED.** Only the two landing bodies and their obsolete binder screws change in CURRENT. Other geometry, all18/12 plywood interfaces and the underfront module remain protected. Raised-playfield service is a geometric pose only until its primary support is defined and physically qualified.

HEAD BEFORE: `cdd21333ca0382cd8e99f9a96872f994136306e5`  
HEAD AFTER: the commit containing this report on `feat/cabinet-review-v32`; exact commit is returned with delivery.  
Native SHA256: `{g['native_sha256']}`

[22 native CAD views](review.html) · [CURRENT native](play.FCStd) · [Offline viewer](../viewer-v32/index.html) · [English manual](../../../docs/ASSEMBLY_MANUAL.md) · [PT-BR manual](../../../docs/ASSEMBLY_MANUAL.pt-BR.md)

## Decisions

| Item | Decision / evidence |
|---|---|
| SW02 | **PROMOTE** two shop-made solid blocks, exactly68 ×70 ×54 mm |
| Front supports | X72/X528,Y245 preserved; sameØ24 contact pads, rear dowel seated |
| Slope |9.906669° nominal preserved; not a user-selectable angle |
| Retention | **A retained:** two captive M6 ×100 tool-operated bolts |
| Hand knob | Ø30/35/40 ×21 reference grips pass packaging, hand and10.5mm release sweeps; no selected equally captive100mm commodity assembly |
| Quick pin | Rejected for current blind M6 receiver: no ball-lock capture shoulder |
| Secondary straps | Two studied; **0 promoted**, no qualified independent restraint or stow |
| Permanent accessory stations | **0**; existing shelves/crossmembers retained |
| Optional board | ACC01,100 ×120 ×12 mm;2 removable commodity clamps per user-selected board; not minimum BOM |
| Cable geometry | Preserve slots/passages; add documented routing zones, no mandatory connector/harness |

## SW02 functional and manufacturing comparison

Six18 mm plywood layers become two solid blanks. Four F60 binder screws and glue-up operations retire. The canonical counts change108→104 wood pieces,104→98 CNC plywood pieces,4→6 solid blocks,66→61 families. SW01 and its jig remain unchanged.

Each original landing union contains243,577.373726 mm³ of wood. SW02 contains245,252.628008 mm³: **1,675.254283 mm³ per side is added only inside obsolete binder bores**. No original functional wood is removed. External bounds, wall mating planes, adjuster/retention paths and side-screw axes remain exact. Manufacturing members reconstruct their final installed B-reps with0 mm³ difference. This is an explicitly equivalent interface, not a false zero-difference claim for filled holes.

The shop supplies dry, stable, straight, knot-free68 ×70 ×54 blocks. Preferred grain follows the68 mm cantilever direction. A scale-verified paper template, clamped commercial perpendicular portable drilling guide, depth stop and same-wood coupon replace lamination. Templates are reference-only until hardware is purchased; hand-held paper marks alone do not establish perpendicular54/68 mm bores. SW02 is shop-made solid wood, not a third plywood stock or a two-face CNC job.

The reaction/load geometry is unchanged. At the existing15 kg display/HIGH mass sensitivity ({worst['moving_mass_kg']:.3f} kg complete moving assembly), the factor2 planning demand is{worst['factor2_front_each_N']:.3f} N per front support, {worst['factor2_upper_screw_pullout_demand_each_N']:.3f} N per upper attachment screw, and{worst['factor2_four_side_screw_shear_demand_each_N']:.3f} N average shear per side screw. These are **demands, not capacities**. The simplified root section has{load['same_root_net_section_as_original_mm2']:.3f} mm² net area and{worst['elastic_root_bending_stress_demand_MPa']:.4f} MPa calculated bending demand. Local insert/head stress, anisotropy, splitting and screw pullout remain unqualified. The9 mm center-to-end /4.5 mm head-recess ligament and12 mm plywood embedment require a real coupon/load test. Solid wood is not assumed stronger than plywood.

Wood orientation and qualification rationale is informed by the [USDA Wood Handbook](https://research.fs.usda.gov/fpl/wood-handbook); it supplies no selected-species allowable for this design. Original simplified hardware studies reference [manufacturer sources](landing-sources.json); no vendor CAD or proprietary geometry was imported.

## Adjustment: travel is not the installed range

Mechanical hardware travel remains **−3…+3 mm**. With rear dowel fully seated, the actual common front-height clearance screen includes the installed main glass, matrix, display and side buttons. The first physical contacts are approximately−2.837633 mm at the primary leaf-button envelope and+1.781117 mm at the main glass. A continuous native CAD certificate supports the conservatively rounded **−1.9…+0.9 mm setup window with≥1 mm modeled clearance**.

Use the adjusters to reproduce the accepted nominal plane and equal pad contact. Do not twist the rigid base by independent contrary settings or use this range to select a playing angle. Release the captive retainers for setup, then reset stops for6–8 mm receiver engagement. Real stock, deflection and component fit still need physical checks. Earlier±3 mm wording describes mechanical travel only and is superseded by [adjustment-validation.json](adjustment-validation.json).

## Normal retention and safety

Normal sequence: open coin door → release left and right captive M6 retainers with the existing tool → remove main playfield glass/matrix as required → raise using a defined and qualified primary support procedure. The same110° coin-door access is preserved by SW02. A future purchased hand unit may replace tool operation only after grip captivity, metal thread, anti-release and nudge qualification. A catalogue press-fit grip is not proof of equal safety.

**CURRENT contains no fully defined/qualified primary support for the50° raised playfield.** The accepted rear dowel/open cradles and front landings do not hold that service angle. Historical props cannot silently be restored. Therefore the native0–50° clearance PASS is not permission to work below a raised display. No safety strap is inserted as a substitute.

The strap study considered{ safety['route_count'] } direct route cases. Front-low routes have the wrong length-change sign for closure arrest; rear-high routes cross moving wood/display; rear-tail routes have poor leverage and late take-up. A single remaining strap must take the full failure load, not half. Commodity cargo lashing is not automatically fall-arrest hardware. [Safety report](safety-report.md) records energy/load sensitivity, failed paths and sources. Decision: **NONE**, with primary-support definition, short rated assembly, independent anchors, arrest distance and stow all unresolved. No permanent anchor holes or minimum strap quantities were invented.

## Optional modules, routing and dry fit

ACC01 sample boards sit on S2 right and S3 left, using rear-edge and front-edge clamps respectively. Native checks preserve shelf screw access, extraction and playfield movement. The minimum nonbearing sample gap is6 mm. Actual clamp jaw/throat/handle, retained payload and vibration still require qualification; a controller board fit does not qualify a contactor/chime. Remove the board/clamps before its shelf. Optional samples stay outside minimum stock, mass and packing.

Cable grammar: CABLE_PASSAGE, STRAIN_RELIEF_PAIR, SERVICE_LOOP_ANCHOR, POWER_ROUTE, SIGNAL_ROUTE and MOVING_HARNESS_ROUTE. Preferred existing slots are6 ×22 R3,34 mm pair pitch; protected compact6 ×16 R3 backbox and4 ×12 R2 underfront exceptions remain. No slot is added merely for visual consistency. Left low signal and right low extra-low-voltage power planning zones are420 mm apart, with24.677 mm minimum modeled clearance. Mains stays separately enclosed; this is not electrical routing certification.

The existing400 mm playfield loop passes63 PLAY/service/lift samples, minimum sampled curvature radius39.270 mm against35 mm planning reference. No routine50° disconnect is needed by that geometric example. **Backbox universal moving-harness route remains HOLD**, because a generic loop trial crossed floor geometry or violated bend curvature. Existing passage/carrier slots and service planes remain unchanged; no normal disconnection workaround is imposed. Qualify the actual supported cable loop before use. [Modularity/routing report](modularity-report.md).

Captured shell joints, floor supports, rear bearing shelf, M067 and the underfront shoulder provide positive dry-fit datums. Fixed shelf supports/cradles retain their matching locators. Unresolved kit-datum work remains at T-guide wall positions, backbox monitor rail cleats and rear hinge-cleat drilling. These are explicit template/placement holds, not hidden tape-measure instructions. All104 final pieces have canonical IDs and orientation records. Commercial flatpack references inform dry-fit/service/modularity principles only; no proprietary joinery,5-axis dependence or large mounting panels are adopted.

## Material, mass and packing

Exactly **18 /12 mm plywood** remains active; forbidden CURRENT plywood pieces:0. Four SW01 and two SW02 blocks are explicitly solid wood. The one-face status counts are43 CNC ready +55 CNC plus manual finish +6 shop-made solid parts. All physical manufacturing gates remain held.

| Stock | CNC pieces | Finished outer-contour area m² | Preliminary2500 ×1600 sheets | Net utilization |
|---|---:|---:|---:|---:|
{stockrows}

Nesting is PRELIMINARY, NOT FOR CNC, with20 mm border/15 mm spacing. No new sheet family or full-sheet requirement is introduced by SW02; six small18 mm cutouts are removed from the nesting demand.

Delivered wood LOW/NOMINAL/HIGH: **{m['wood_flatpack_kg'][0]:.3f} /{m['wood_flatpack_kg'][1]:.3f} /{m['wood_flatpack_kg'][2]:.3f} kg**. Finished-reference wood nominal:{m['wood_finished_reference_kg'][1]:.3f} kg. Delivered nominal mass is unchanged because the two solid blanks equal the six former plywood shipping blanks at the planning650 kg/m³. SW02 density is separately configurable500/650/850 kg/m³; unknown actual wood/hardware masses are not zero.

Preferred packing: **{plan['bundle_count']} wood bundles**, target{pack['preferred_target_kg']} kg, allHIGH-density gross values≤25 kg. Glass/electronics remain separate; hardware has its own box. Optional boards and straps are excluded.

| Bundle | External L ×W ×H mm | Wood mass kg | Gross HIGH kg |
|---|---|---:|---:|
{packrows}

Required Fxx minimum is **{hw['known_required_Fxx_minimum']} known pieces +{len(hw['formula_driven_Fxx'])} formula-dependent families +{len(hw['TBD_Fxx'])} genuinely TBD families**. F60×4 is retired. No other unknown hardware quantity is guessed. [Manufacturing BOM](manufacturing-register.json) · [Hardware dashboard](hardware-dashboard.json) · [Mass](mass-budget.json) · [Packing](packaging.json).

## Validation and remaining release gates

{len(v['checks'])} regression/evidence checks and{v['browser_checks']} browser checks pass. Native differential certificates cover SW02 against0–50° playfield opening,48 mm lift and populated0–90° backbox fold; all other interactions inherit the exact protected V33.7 geometry. Hand/knob packaging is not hardware acceptance; strap evidence completion is not a strap safety PASS.

Side buttonsY89/Y127: PASS. Horn absent/front relief: PASS. Front support contacts/slope: PASS. Geometric service/lift/fold: PASS. SW01/M067/underfront160 ×116 ×12,5BTN+USB, six-button alternate,2 mm shoulder,70 mm USB reserve and null device cuts: unchanged. Unrelated geometry: unchanged.

Release remains BLOCKED for actual stock, coupon, purchased hardware/display/button/USB/landing dimensions, SW02 species/drilling/load qualification, structural/ergonomic proof, unresolved dry-fit templates, primary raised support and actual moving-harness qualification. No G-code, production nesting or manufacturing approval is supplied.

Original material: CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
'''
def readable(t):
 # Preserve hashes, IDs in code, Markdown destinations and raw source URLs.
 tokens=re.split(r'(`[^`]*`|\]\([^)]*\)|https?://\S+)',t)
 return ''.join(x if i%2 else re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-z])|(?<=[a-z])(?=[−±])',' ',x) for i,x in enumerate(tokens))
(O/'README.md').write_text(readable(txt))
en='''# V33.8 — serviceability and modularity

The two front landing bodies are now SW02 solid shop blocks,68 ×70 ×54 mm. Six CNC plywood layers and four binder screws retire; all other accepted geometry remains unchanged. Plywood stock remains exactly18/12 mm.

Current captive M6×100 tool retainers remain. The geometric setup window is−1.9…+0.9 mm with1 mm modeled clearance; mechanical travel is±3 mm, and nominal9.906669° remains unchanged. No strap is promoted. The primary support for a raised50° playfield is unresolved; geometry clearance is not approval to work beneath it.

Optional100 ×120 ×12 mm boards use removable clamps; zero permanent hardpoints. Existing cable slots/passages are retained, with preferred route zones documented. The PF reference loop passes its sampled screen; a universal backbox loop remains HOLD.

- [Full report and decisions](../exports/generated/service-productization-v338/README.md)
- [22 native CAD review views](../exports/generated/service-productization-v338/review.html)
- [Offline viewer](../exports/generated/viewer-v32/index.html)
- [English assembly manual](ASSEMBLY_MANUAL.md)
- [Portuguese assembly manual](ASSEMBLY_MANUAL.pt-BR.md)

Minimum product:104 wood pieces /98 CNC plywood /6 solid blocks /61 families. Delivered wood nominal61.277 kg; four preferred bundles, each below25 kg at HIGH density. Manufacturing and physical operation remain held as detailed in the report.
'''
(R/'docs/SERVICE_PRODUCTIZATION_V338.md').write_text(readable(en))
pt='''# V33.8 — manutenção e modularidade

Os dois apoios dianteiros passam a blocos maciços SW02 de68 ×70 ×54 mm. Saem seis lâminas CNC e quatro parafusos de união. A posição dos apoios e toda a geometria não relacionada permanecem iguais. Compensado: somente18/12 mm.

Permanecem os dois retentores M6×100 cativos operados com ferramenta. O intervalo geométrico de ajuste é−1,9…+0,9 mm, com1 mm de folga modelada; o curso mecânico é±3 mm. A inclinação nominal de9,906669° não muda e não é regulagem de ângulo de jogo.

Nenhuma cinta foi promovida. Falta definir e qualificar o suporte primário do playfield elevado a50°: a trajetória CAD livre não autoriza trabalhar sob um display sem sustentação. O estudo registra as interferências, a pequena alavanca de algumas rotas e as cargas condicionais de retenção.

As placas opcionais ACC01 de100 ×120 ×12 mm usam grampos removíveis, sem novos furos permanentes. A rota de referência do playfield passou nas amostras; a rota universal do chicote do backbox continua pendente. Não foi especificado sistema elétrico ou conector obrigatório.

- [Relatório completo e evidências](../exports/generated/service-productization-v338/README.md)
- [22 vistas CAD](../exports/generated/service-productization-v338/review.html)
- [Visualizador offline](../exports/generated/viewer-v32/index.html)
- [Manual PT-BR](ASSEMBLY_MANUAL.pt-BR.md)

Produto mínimo:104 peças de madeira /98 peças CNC de compensado /6 blocos maciços /61 famílias. Massa nominal entregue61,277 kg; quatro volumes preferidos, todos abaixo de25 kg na densidade HIGH. Material real, cupom, ferragens e qualificação estrutural continuam pendentes. CNC de chapas completas BLOQUEADO.
'''
(R/'docs/SERVICE_PRODUCTIZATION_V338.pt-BR.md').write_text(readable(pt))
print('V338_REPORT_PASS')
