"""Generate convenience queue/checklists only; never write engineering sources/results."""
import hashlib
import json
from pathlib import Path

from owner_workflow_v27 import BUY_NOW, GATE, PACK, PLAN, REFERENCE_IDS, SESSIONS, specification

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / 'bom/PHYSICAL_VALIDATION_RESULTS_V27.json'
QUEUE = ROOT / 'bom/PHYSICAL_VALIDATION_OWNER_QUEUE_V27.json'
DOCS = ['OWNER_PHYSICAL_CHECKLIST_V27.md', 'HARDWARE_ARRIVAL_INSPECTION_V27.md',
        'OWNER_MEASUREMENT_SHEETS_V27.md', 'OWNER_EVIDENCE_PLAN_V27.md']
NOTICE = 'CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet'
TRIAL_COMPONENTS = {
    'PV-PLUNGER': [30], 'PV-PROP-L': [10], 'PV-PROP-R': [10], 'PV-PROP-MOTION': [10],
    'PV-MASS': [24], 'PV-ERGONOMICS': [24], 'PV-CONTROLS-SSF': [20,30,31],
    'SV-01': [], 'SV-02': [], 'SV-03': [13,14,15,16,26,28], 'SV-04': [29],
    'SV-05': [25], 'PV-AIRFLOW': [32], 'PV-THERMAL': [32], 'PV-STOCK-TOOL': [1,2],
    'PV-LOADS': [3,4,6,7,8,9,22], 'PV-ELECTRICAL': [17,27], 'PV-CNC-PACKAGE': [],
}
TOOLS = {
    'dimensional': 'Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.',
    'survey': 'Steel rule/tape, straightedge, feeler gauges, pencil and labeled sheet sketch.',
    'mockup': 'Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains.',
    'motion': 'Reviewed supported fixture, actual hardware, ruler/feeler gauges and camera; independent support as specified in the plan.',
    'proof': 'Reviewer-specified fixture, independent support/catch, approved loads and displacement instruments. Do not assemble a test from this tool list alone.',
    'shop': 'CNC shop supplies its tooling/runout/depth/registration instruments and identified physical coupon.',
    'reference': 'Maker or approved adapter document with part number/revision; no measuring instrument or inferred readings.',
    'mass': 'Suitable scale with recorded uncertainty and stable supports/assistance; no unsafe balancing.',
    'force': 'Force gauge, angle measurement, approved fixture and independent backup; actual intended grip.',
    'commission': 'Instruments and protected setup specified in the reviewed commissioning plan; none selected here.',
    'review': 'Evidence records, original freeze gate and qualified reviewers; no physical operation authorized.',
    'preparation': 'Pen, labels/masking tape, marker, blank sheets, phone/camera, ruler/square; available caliper/micrometer for identification and zero checks.',
}


def units(mid, wording):
    if mid in REFERENCE_IDS:
        return 'reference document / maker-stated units; NOT a measured value'
    if mid in {'HF-010-M07', 'HF-005-M01'}:
        return 'reviewed test report; units from approved procedure'
    if mid == 'HF-024-M03':
        return 'kg and N; grip coordinates mm; angle deg'
    low = wording.lower()
    if 'mass' in low:
        return 'kg'
    if any(x in low for x in ('revision', 'batch id', 'defects', 'grain direction', 'record all four')):
        return 'text / instance IDs (grain also mark on sketch)'
    if 'angle' in low or 'sweep' in low or 'swing' in low:
        return 'deg and mm clearance; note state'
    if any(x in low for x in ('access', 'engagement', 'retention', 'travel/release', 'protected entry')):
        return 'mm plus observed condition/state'
    return 'mm; notes for condition/identity'


def arrival(c):
    cid = c['component_id']
    if cid == 'HF-014':
        return 'HAVE / OWNER-SUPPLIED', 'Already-owned open case explicitly documented; confirm identity at bench.'
    if cid == 'HF-028':
        return 'HAVE / OWNER-SUPPLIED', 'Bundled measurement task using legs/brackets/slides/clamps; not another purchase. Arrival unknown.'
    if cid == 'HF-002':
        return 'HAVE / OWNER-SUPPLIED', 'Immediate shop consultation/coupon task, not a hardware purchase. Shop tooling/evidence not confirmed.'
    if cid in BUY_NOW:
        return 'BUY NOW', 'Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.'
    if c['procurement_group'] == 'LOCAL FAB':
        return 'HAVE / OWNER-SUPPLIED', 'Required local prototype/drawing; not confirmed present. HF-009 follows bearing measurements; HF-021/022 prototype now per existing pack.'
    return 'WAIT', 'BUY LATER / optional adapter: no new purchase authorization. Actual arrival unknown.'


def make_queue(ledger):
    components = {c['component_id']: c for c in ledger['components']}
    measurements = {m['measurement_id']: (ci, mi, c, m)
                    for ci, c in enumerate(ledger['components']) for mi, m in enumerate(c['measurements'])}
    trials = {t['test_id']: (i, t) for i, t in enumerate(ledger['physical_trials'])}
    ops = specification()
    # Thermal measurements are later commissioning, after electrical review.
    thermal = next(o for o in ops if o['operation_id'] == 'THERMAL')
    thermal['session'] = 11
    thermal['dependencies'].append('ELECTRICAL')
    ordered = []
    while ops:
        completed = {o['operation_id'] for o in ordered}
        ready = [o for o in ops if set(o['dependencies']) <= completed]
        if not ready:
            raise ValueError('Cyclic or unknown owner dependencies')
        chosen = min(ready, key=lambda o: o['session'])
        ops.remove(chosen)
        ordered.append(chosen)
    for o in ordered:
        mids = o['measurement_ids']
        cids = {mid[:6] for mid in mids}
        for tid in o['trial_ids']:
            cids.update(f'HF-{n:03d}' for n in TRIAL_COMPONENTS[tid])
        o['component_ids'] = sorted(cids)
        o['component'] = '; '.join(components[cid]['component'] for cid in sorted(cids)) or o['title']
        o['measurements'] = [dict(measurement_id=mid, exact_measurement=measurements[mid][3]['required'],
                                  preferred_instrument=measurements[mid][2]['recommended_tool'],
                                  units=units(mid, measurements[mid][3]['required']),
                                  ledger_pointer=f'/components/{measurements[mid][0]}/measurements/{measurements[mid][1]}',
                                  reference_only=mid in REFERENCE_IDS) for mid in mids]
        o['trials'] = [dict(trial_id=tid, exact_test=trials[tid][1]['purpose'],
                            ledger_pointer=f'/physical_trials/{trials[tid][0]}') for tid in o['trial_ids']]
        o['linked_feature_groups'] = [dict(part_id=g['part_id'], feature_id=g['feature_id'], component_id=g['component_id'])
                                      for g in ledger['feature_groups'] if g['component_id'] in cids or o['operation_id'] == 'PACKAGE']
        o['preferred_instrument'] = TOOLS[o['mode']]
        if o['operation_id']=='STOCK-THICK':
            o['preferred_instrument'] = components['HF-001']['recommended_tool']
        if any(m['units']=='kg' for m in o['measurements']):
            o['preferred_instrument'] += ' Use a suitable scale for actual mass, with stable support/assistance.'
        if o['mode']=='preparation':
            o['samples'] = 'One preparation/handoff record; no specimen repetitions.'
        if o['mode']=='reference':
            o['samples'] = 'Document revision for each distinct delivered part/adapter; no physical reading or repeated measurement.'
        o['units'] = 'Per measurement row; trials record units specified by the original procedure; narrative observations as text.'
        o['samples'] = o['samples'] or 'Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.'
        o['acceptance'] = o['acceptance'] or ('Reference only; cannot supply a physical measured_value or pass a fit.' if o['mode']=='reference' else 'Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate.')
        o['views'] = o['views'] if o['views'] is not None else ['identity','datum','mount-face']
        o['evidence_requirements'] = dict(views=o['views'],
            rule='Reuse a labeled identity/datum/context photo across entries from the same part/setup. Photograph a representative reading or difficult/critical clearance; do not photograph every routine repeat. Always retain written raw readings; reference-only operations need the document revision rather than redundant photos.',
            filename=f"PV27_S{o['session']:02d}_{o['operation_id']}_<view>_<sequence>.jpg")
        o['gate'] = 'Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.'
        o['status'] = 'NOT_STARTED'
        o['execution_hold'] = ('REVIEWED_CRITERIA_REQUIRED' if o['category']=='B' else
                               'REFERENCE_ONLY' if o['mode']=='reference' else 'VERIFY_SAMPLE_AND_DEPENDENCIES')
    arrivals = []
    for c in ledger['components']:
        category, state = arrival(c)
        related = [o for o in ordered if c['component_id'] in o['component_ids']]
        arrivals.append(dict(component_id=c['component_id'], item=c['component'],
            source_procurement_group=c['procurement_group'], category=category, acquisition_state=state,
            measurement_ids=[m['measurement_id'] for m in c['measurements']],
            operation_ids=[o['operation_id'] for o in related],
            trial_ids=sorted({t for o in related for t in o['trial_ids']}),
            feature_ids=[g['feature_id'] for g in ledger['feature_groups'] if g['component_id']==c['component_id']],
            physical_sample_required='Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.',
            catalogue_policy='REFERENCE ONLY; never substitute for physical measurements.'))
    return dict(schema_version=1, convenience_only=True, authoritative_ledger='bom/PHYSICAL_VALIDATION_RESULTS_V27.json',
                ledger_sha256=hashlib.sha256(LEDGER.read_bytes()).hexdigest(), manufacturing_ready=False,
                automatic_unlock=False, measurement_count=len(measurements), trial_count=len(trials),
                practical_operation_count=len(ordered), session_count=len(SESSIONS),
                sessions=[dict(session=i,title=t) for i,t in enumerate(SESSIONS)],
                arrivals=arrivals, operations=ordered)


def cell(value):
    return str(value).replace('|', '/').replace('\n', ' ')


def documents(q, ledger):
    cs = {c['component_id']: c for c in ledger['components']}
    header = ['Derived owner convenience copy. Authoritative values remain in [PHYSICAL_VALIDATION_RESULTS_V27.json](../bom/PHYSICAL_VALIDATION_RESULTS_V27.json). No measurements are filled; manufacturing stays **BLOCKED**. Regenerate with `python3 tools/generate_owner_execution_v27.py`; do not write bench results into generated files.', '', NOTICE, '']
    checklist = ['# Owner physical checklist — v27', ''] + header + [
        '## Start here — Session 0', '',
        '**First action: PREP.** Bring a pen, labels/masking tape, marker, phone/camera, steel rule/square, the available caliper/micrometer, and blank sheets or a device displaying this checklist. No cabinet hardware or ballast is needed. Identify/zero-check tools; sort whatever has arrived using the arrival sheet. Missing tools/samples can be noted now; do not buy all later electronics.', '',
        f"**186 authoritative measurements + 18 authoritative trials → {q['practical_operation_count']} practical owner operations in 12 sessions.** The count includes three preparation/handoff operations and deferred shop/reviewer tasks; it is not a claim that all operations can be performed today.", '',
        '**A — ordinary owner checks:** unpowered loose-part measurements and supported light mockups, using the source plan constraints. **B — STOP for review:** proof/load, supported heavy movement, shop work or commissioning requiring the existing reviewed setup/criteria. Both prop proofs are B. No load, safety factor, fixture design or acceptance limit is added here.', '',
        'Work down each session; skip unavailable WAIT items and return later. Dependencies name operations whose evidence/setup is needed, not permission to declare their results accepted. Session 11 accepts an incomplete evidence handoff now; final review/commissioning can remain pending. Photos are selective: reuse labeled setup views rather than photographing every reading.', '',
        'Print [measurement sheets](OWNER_MEASUREMENT_SHEETS_V27.md) for the next action only. See [arrival inspection](HARDWARE_ARRIVAL_INSPECTION_V27.md) and [photo plan](OWNER_EVIDENCE_PLAN_V27.md). On paper write the authoritative ID; JSON locations below are for later transcription, not instructions to interpret CAD.', '',
        '## Session index', '',
        *[f"- Session {entry['session']}: {entry['title']} — {sum(o['session']==entry['session'] for o in q['operations'])} operations" for entry in q['sessions']], '',
        '## Collection savings', '',
        f"{sum(bool(o['measurement_ids']) for o in q['operations'])} operations collect the 186 measurement records; all 18 trials are mapped once. Some measurement and trial work shares the same operation. Three preparation/handoff operations bring the total to {q['practical_operation_count']}.", '',
        '- Thickness min/max reuse the nine-point readings. Record all four leg instances without repeating them to fill the identity record.',
        '- Loose patterns, diameters and seating depths share a component setup; each original ID remains separate.',
        '- One rear-corner fixture supplies both HF-004 and HF-028 readings. One mains assembly supplies HF-017 and HF-027 entries.',
        '- Mass measurements feed the composite lift entry. Both prop proof reports feed the capacity entry; neither proof is omitted.',
        '- Four maker/attachment specification entries are reference-only collection steps; no invented physical reading is needed.', '',
        '## Ledger transcription key', '',
        'For measurement paths below, enter actual value, units, raw repeats, instrument, uncertainty, source_kind and repository-relative evidence paths; identify the part, date/operator and datums on its component record. Trial paths receive fixture revision, date/operator, physical IDs, criteria/reviewer, evidence, result/limitations and status. Preserve failed trials. A composite field may need separate left/right or sub-reading values with units. Never fill unknowns from the provisional context.', '',
        '**Reference mismatch:** HF-008-M08, HF-013-M02/M09 and HF-031-M02 ask for documented specifications. File reference text/revision in notes and return it for engineering review; keep measured_value null. The accepted ledger validator intentionally rejects catalogue promotion. This package does not change that schema or gate.', '']
    sheets = ['# Owner measurement sheets — v27', ''] + header + [
        'Print one operation section at a time. Copy a sheet for each handed instance/sample, and extra rows for multi-hole patterns or sub-readings; retain the original measurement ID with a sub-reading label. Header instrument/date/sample apply to all rows unless overridden in notes. Empty spaces are intentional. OPEN is the default: a blank result is not PASS.', '',
        'No direct geometry unlock. A check mark means collected, not accepted for machining. For B operations print the original reviewed procedure as well; these sheets do not authorize loading. [Detailed checklist](OWNER_PHYSICAL_CHECKLIST_V27.md) · [Evidence plan](OWNER_EVIDENCE_PLAN_V27.md)', '']
    for session in q['sessions']:
        s = session['session']
        session_ops = [o for o in q['operations'] if o['session']==s]
        checklist += [f"## Session {s} — {session['title']}", '']
        for o in session_ops:
            checklist.append(f"- [ ] **{o['operation_id']}** ({o['category']}) — {o['title']}")
        checklist.append('')
        for o in session_ops:
            oid = o['operation_id']
            checklist += [f'### {oid}', '', f"**Component:** {o['component']}", '', o['instructions'], '',
                f"**Before starting:** {', '.join(o['dependencies']) or 'None'}. **Hold:** {o['execution_hold']}.", '',
                f"**Instrument:** {o['preferred_instrument']} **Samples/repeats:** {o['samples']}", '']
            if o['measurements']:
                checklist += ['| Authoritative ID | Exact result to collect | Units | JSON location |', '|---|---|---|---|']
                for m in o['measurements']:
                    checklist.append(f"| {m['measurement_id']} | {cell(m['exact_measurement'])} | {cell(m['units'])} | `{m['ledger_pointer']}` |")
            for t in o['trials']:
                checklist += ['', f"**Trial {t['trial_id']}:** {t['exact_test']}. Record at `{t['ledger_pointer']}`; use the existing plan/procedure."]
            if not o['measurement_ids'] and not o['trial_ids']:
                checklist += ['Record preparation/handoff notes on paper; no authoritative result ID is invented for this housekeeping step.']
            ids = ', '.join(f"{g['feature_id']} ({g['part_id']})" for g in o['linked_feature_groups']) or 'No hardware-controlled CF group; global process/service gate or preparation only.'
            checklist += ['', f"**Linked blockers:** {ids}", '',
                f"**Evidence:** {', '.join(o['views']) or 'Written notes/reference document only; no extra photo required.'} Naming: `{o['evidence_requirements']['filename']}`.", '',
                f"**Existing criterion:** {o['acceptance']} [Source](../{o['acceptance_source']}).", '', f"**Geometry:** {o['gate']}", '']
            sheets += [f"## S{s:02d} / {oid} — {o['title']}", '',
                f"**{o['category']} — {'REVIEW REQUIRED BEFORE EXECUTION' if o['category']=='B' else 'OWNER CHECK / verify sample and support'}.** Dependencies: {', '.join(o['dependencies']) or 'none'}.", '',
                'Date: __________  Operator: __________  Sample ID / side / batch: ____________________', '',
                'Instrument / resolution / zero check: ____________________  Uncertainty: __________', '',
                'Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________', '',
                f"Tools: {o['preferred_instrument']}", '', f"Samples/repeats: {o['samples']}", '']
            if o['measurement_ids']:
                sheets += ['| Measurement ID / exact item | Units | Value / sub-readings | Repeat |', '|---|---|---|---|']
                for m in o['measurements']:
                    sheets.append(f"| **{m['measurement_id']}** — {cell(m['exact_measurement'])} | {cell(m['units'])} | ______ | ______ |")
                for cid in sorted({m[:6] for m in o['measurement_ids']}):
                    sheets += ['', f"{cid} datum: {cs[cid]['datum']}", '', f"{cid} recording target (not machining fit): {cs[cid]['recording_tolerance']}"]
            if oid=='STOCK-THICK':
                sheets += ['', 'HF-001-M01 raw point record (one labeled sheet):', '',
                    '| Point on sketch | Thickness mm | Repeat mm |', '|---|---|---|']
                sheets += [f'| {i} | __________ | __________ |' for i in range(1,10)]
                sheets += ['', 'HF-001-M02: minimum ______ mm; maximum ______ mm (from these same readings).']
            for t in o['trials']:
                sheets += ['', f"**{t['trial_id']} — {t['exact_test']}**", '',
                    'Approved criteria / reviewer / date: ______________________________________________', '',
                    '| Step / state / units | Reading | Repeat | Observation / evidence |', '|---|---|---|---|',
                    '| __________ | __________ | __________ | ____________________ |',
                    '| __________ | __________ | __________ | ____________________ |',
                    '| __________ | __________ | __________ | ____________________ |', '',
                    'Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________', '',
                    'Failure observations / limitations / retest: __________________________________________']
            sheets += ['', 'Notes / sub-reading IDs / photo references: __________________________________________', '',
                '________________________________________________________________________________', '',
                'Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____', '',
                f"Existing criterion: {o['acceptance']} [Source](../{o['acceptance_source']}).", '',
                'Collection alone does not release geometry. Unknown acceptance stays OPEN.', '',
                '<div style="break-after: page; page-break-after: always;"></div>', '']
    sheets += ['## Extra pattern / sub-reading sheet', '',
        'Parent authoritative measurement ID: __________  Operation: __________  Sample/side: __________', '',
        'Date/operator: __________  Instrument/uncertainty: __________  Datum sketch: __________', '',
        'Name horizontal and vertical datum axes on the sketch before measuring. Retain signed offsets; never infer a pattern from a photograph.', '',
        '| Hole/slot/sub-reading label | First datum offset mm | Second datum offset mm | Diameter/width/depth mm | Repeat / evidence |',
        '|---|---|---|---|---|']
    sheets += ['| ______ | ______ | ______ | ______ | ______ |' for _ in range(8)]
    sheets += ['', 'Notes: ______________________________________________________________________', '']
    arrivals = ['# Hardware arrival inspection — v27', ''] + header + [
        '**BUY NOW** below repeats existing authorization; no new purchasing category is introduced. **HF-030 remains the only previously new BUY NOW item.** Only HF-014 is confirmed owned. **HAVE / OWNER-SUPPLIED** can mean a required shop/prototype/assembled sample whose arrival is unknown; it never asserts ownership without evidence. **WAIT** means no current purchase instruction. **REFERENCE ONLY** means maker/drawing data, not a physical substitute.', '',
        'On delivery: identify item, variant, batch and handed side; check completeness and obvious damage, retain labels, and put mating bolts/nuts/backing together. These are arrival observations, not dimensional acceptance. Record arrival on this printed copy; do not populate physical measured values from invoices/catalogues.', '',
        'Shared acquisitions: legs/brackets HF-003/004; slides/clamps HF-013/026; door hardware HF-015/016/029 (separate installations); backbox hinges/locks HF-006/007; props/latches HF-010/012; mains module/enclosure HF-017/027. HF-028 reuses the corner stack; HF-002 is shop consultation. No electronics purchase is needed to start Session 0.', '',
        '## Arrival summary', '', '| ID | Item | Category | Arrival today |', '|---|---|---|---|']
    for a in q['arrivals']:
        arrivals.append(f"| {a['component_id']} | {cell(a['item'])} | {a['category']} | ______ |")
    for a in q['arrivals']:
        cid = a['component_id']; c = cs[cid]
        arrivals += ['',f'## {cid} — {a["item"]}', '',f"**{a['category']}.** {a['acquisition_state']}", '',
            'Sample/batch/side: __________  Received date: __________  Missing/damaged: __________', '',
            f"**Needed for:** {c['cad_update_targets']}. Physical tasks: {', '.join(a['operation_ids'])}.", '',
            '**Measurements required:** '+ '; '.join(m['measurement_id']+' '+m['required'] for m in c['measurements'])+'.', '',
            f"**Tests required:** {', '.join(a['trial_ids']) or 'Component fit/access checks in its operations; no separately named ledger trial.'}", '',
            f"**Related CF blockers:** {', '.join(a['feature_ids']) or 'No current hardware-blocked wood group; adapter/global gate only.'}", '',
            f"**Physical sample:** {a['physical_sample_required']}", '',
            f"**Catalogue/drawing data:** {a['catalogue_policy']} Existing datum: {c['datum']}"]
    arrivals += ['', '## REFERENCE ONLY — document envelope', '',
        'File maker identity, revision, rating conditions, clearance limits and attachment specifications alongside the physical sample. Specifically HF-008-M08, HF-013-M02/M09 and HF-031-M02 are reference-specification tasks. Do not change their measured_value from null in this cycle. Return references for engineering review. Do not infer geometry from a render, catalogue picture or CAD envelope.', '']
    evidence = ['# Owner evidence and photo plan — v27', ''] + header + [
        'Use `PV27_S<two-digit-session>_<operation-id>_<view>_<sequence>.jpg`, for example `PV27_S02_PLUNGER-FACE_mount-face_01.jpg`. Videos/raw sheets may use the same stem with their real extension. Sequence numbers increase within an operation/view; do not overwrite. Put sample ID/handed side and datum labels in frame or on the linked written sheet.', '',
        'Keep files under a repository-relative evidence folder such as `evidence/physical-v27/S02/` when submitting. The queue prescribes names only; it creates no evidence files. Return photos plus raw written readings. A photograph of a ruler is supporting evidence, not an inferred precision measurement.', '',
        'One full-component/label photo and one marked datum/mounting-face view can support many IDs from the same actual sample. Photograph representative critical readings, inaccessible offsets, tight clearance states, failures and assembly context. Do not require a photo of every routine caliper repeat or document revision. Keep reference PDFs/text in a REFERENCE subfolder with part/document revision; catalogue content never goes into measured values.', '',
        '| View family | Capture when useful |', '|---|---|',
        '| identity / datum / mount-face | Full actual component, label and handed side; mounting plane and datum axes; orthogonal face and side for offsets. |',
        '| reading / bore-reading / scale-reading / gauge-reading | Instrument display and contact location, sample ID; enough context to connect the reading to the sheet. Raw reading remains written separately. |',
        '| rest / full-pull / inward-limit / rear-clearance | Plunger/button internals and cable/nut/tool clearance at actual limiting states. |',
        '| deployed / stowed / keeper-engaged / stow-clip | Both prop positions, captive pins and positive keeper engagement; nearest obstacle. |',
        '| installed / extraction / cabling / removal-path | Carrier/CPU installed state, removal sequence, connectors and representative bundles. |',
        '| open / closed / front-extraction / bezel-off | Backbox rear service and actual front replacement route; distinguish dummy from final monitor. |',
        '| slots / filter-removal / passage-obstruction | Actual bottom/coupon webs, external filter route and occupied airflow passages. |',
        '| fixture / approved-load / deflection / after-unload | B tests only after review: fixture ID, approved case, gauges, opposite prop disengaged and residual condition. No person beneath an unproven load. |', '',
        '## Operation-specific views', '', '| Session / action | Views to retain or share | Filename stem |', '|---|---|---|']
    for o in q['operations']:
        evidence.append(f"| S{o['session']:02d} / {o['operation_id']} | {', '.join(o['views']) or 'Written/reference evidence only; no extra photo'} | `PV27_S{o['session']:02d}_{o['operation_id']}_<view>_<sequence>` |")
    evidence += ['', 'Before returning: check files open, IDs match the sheet, every claimed result has traceable evidence, left/right are distinguishable, and any failure/unknown remains visible. Do not publish third-party reference material without checking its licensing; a document identifier/link and owner notes can be retained instead.', '']
    return {DOCS[0]: '\n'.join(checklist).rstrip()+'\n', DOCS[1]: '\n'.join(arrivals).rstrip()+'\n',
            DOCS[2]: '\n'.join(sheets).rstrip()+'\n', DOCS[3]: '\n'.join(evidence).rstrip()+'\n'}


def generated_outputs():
    before = LEDGER.read_bytes()
    ledger = json.loads(before)
    queue = make_queue(ledger)
    outputs = {QUEUE: json.dumps(queue,indent=2,ensure_ascii=False)+'\n'}
    outputs.update({ROOT/'docs'/name: text for name,text in documents(queue, ledger).items()})
    assert LEDGER.read_bytes() == before, 'generator changed authoritative ledger'
    return outputs


def main():
    before = LEDGER.read_bytes()
    for path, text in generated_outputs().items():
        path.write_text(text)
    assert LEDGER.read_bytes() == before, 'generator changed authoritative ledger'
    queue = json.loads(QUEUE.read_text())
    print('OWNER_EXECUTION_GENERATED', queue['measurement_count'], 'measurements,',queue['trial_count'],
          'trials,',queue['practical_operation_count'],'operations,',queue['session_count'],'sessions')


if __name__ == '__main__':
    main()
