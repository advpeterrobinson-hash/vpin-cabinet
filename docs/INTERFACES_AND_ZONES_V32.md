# V32 interface and zone planning

[English](INTERFACES_AND_ZONES_V32.md) · [Português (Brasil)](pt-BR/INTERFACES_AND_ZONES_V32.md)

Status: **PROVISIONAL — CNC BLOCKED — physical sessions PAUSED**. Resumed 2026-09-28 from `0398d16857e66e415805b7154b0df7e37e7964a6` after the power outage. This is the next planning package from the [Pinscape review](PINSCAPE_ACCELERATION_REVIEW.md), using the [lighting intent](LIGHTING_INTENT_V32.md), [part registry](PART_CODES.md) and [V32 package](../exports/generated/cabinet-v32/README.md). No geometry, purchased hardware, measurements or electrical ratings are approved here.

Update 2026-09-29: the owner selected the CSD LED kit. [Selected kit and nominal dimensions](LIGHTING_INTENT_V32.md) supersede the unknown product and earlier MX-DONNY assumption below. IF-05 remains unmeasured; order variant, connectors, fit and operating limits remain open.

## Interface register

These `IF-*` identifiers track requirements; they are not permanent part codes. All interfaces remain `BLOCKED_UNMEASURED`. An existing model or a nominal dimension is not a hardware fit certificate.

| ID / interface | Recorded baseline | Missing evidence | Next deliverable / acceptance |
|---|---|---|---|
| IF-01 Legs and brackets | Real pinball legs; 600 mm body | Exact bracket/bolt/washer envelopes, holes, tool access and load zones | Measured drawing; compare with SideL/SideR and proposed grooves before an original CNC coupon |
| IF-02 Plunger | Arnoz plunger intent; final interface pending | Exact revision, stroke, body/connector envelope and mounting pattern | Replaceable mounting proposal; full stroke and front-panel/access check |
| IF-03 Glass and lockdown | Custom-width lockdown allowed; nominal plywood 18 mm | Glass thickness/edges, channel profile, lockdown receiver, retention and removal path | Section drawing with measured stock and hardware; test coupon before final panel cuts |
| IF-04 Rear fans and guards | Two fan envelopes in V32; 120 mm nominal frame reference | Selected fan/guard/filter, cutout, hole pitch, cable exit and service access | Replaceable interface drawing plus removal check; thermal proof remains separate |
| IF-05 Matrix | Six provisional 16×16 panels; 1,536 pixels | Model/revision, width/height/depth, pitch, mounting, connector access, arrangement, chipset, voltage and rated current | Panel record and mapping first; removable carrier proposal and motion review afterwards |
| IF-06 Speaker/cabinet/gap LEDs | Speaker and cabinet lighting intended; gap lighting optional | Selected strips/rings, lengths/pixels, dimensions, ratings and connector envelopes | Separate zone records; speaker lighting removes with speaker; preserve display clearance |
| IF-07 Backbox and playfield service | BBBase and monitor-support identities; two captive props required | Hinge/fixing and cable envelopes; prop receivers, keepers, stowage and full-load retention | Separate motion/access study and one-prop load-proof plan; no completed physical test implied |
| IF-08 Service modules | S1/S2/S3, T1/T2/T3 and PCBase appear in V32 | Fastener/tool envelopes, disconnect points, restraint and removal paths | Access sequence with dependencies and measured connectors; resolve PC architecture discrepancy below first |
| IF-09 Power, network and feedback | One grounded cord; enclosed distribution; independent feedback disable | Selected devices, enclosure, strain relief, service access, protection and load records | Functional zone map and qualified electrical review before wiring or cutouts |

### PC architecture discrepancy

The supplied session instructions require a rear full-extension PC drawer, while the saved V32 package records a low PCBase without a drawer. This worksheet does not choose between them. Mark the PC service interface **BLOCKED_OWNER_DECISION** before designing its removal path or changing geometry. Existing V32 files are preserved as evidence; do not silently propagate their no-drawer choice as the new instruction.

## Power, data and service zones

The [machine-readable worksheet](../config/interface_zones_v32.json) keeps unknown ratings as `null`, never zero. Zone IDs are planning identifiers, not circuit numbers or a selected controller allocation.

| Zone | Power boundary / data relationship to resolve | Service boundary |
|---|---|---|
| MATRIX | Panel power versus controller data outputs; panel order/orientation and controller revision | Removable matrix carrier; accessible keyed disconnect; check playfield/backbox motion |
| SPEAKER_LED / CABINET_LED / GAP_LED | Separate pixel maps and brightness settings; gap zone optional | Speaker assembly / removable trim; no loss of display replacement envelope |
| AUDIO | Music/Bluetooth path and amplifiers; selected StarTech channel mapping | Individually replaceable audio devices; document each connector |
| SSF | Four spatial zones; channel → amplifier → exciter assignment pending | Local mounts and terminals; avoid broad shelf bracing of active walls |
| FEEDBACK | Device → driver → protection → independent disable; duty ratings pending | Positive mechanical mounting and independently disabled service state |
| PC / DISPLAYS | Device input ratings and data connectors; internal signal routing pending | PC architecture decision; display adapter and connector access |
| COOLING / CONTROL | Fan/control supply and operating-mode dependencies pending | Guards/filter access; deliberate offline setup and service access |

Functional mode targets, **not a switch-wiring design**:

- **OFF:** powered loads off. The service isolation method must be documented and verified; a mode label is not proof of safe isolation.
- **AUDIO ONLY/Bluetooth:** intended music path available, PC/displays and mechanical feedback off. Required receiver/amplifier/control/cooling dependencies remain to be selected. Decorative lighting policy is open.
- **FULL PINBALL:** game subsystems available. Feedback retains its independent disable; lighting retains effects-off and per-zone brightness controls.

Protective earth, DC returns and signal references need separate identified records in the eventual design; this worksheet prescribes no bonding topology. Mains remain enclosed and inaccessible in normal service. No fuse, conductor, supply size or connector pinout is selected.

## Calculation-ready load records

Create one device row per actual model and supply rail in each zone. Record quantity, manufacturer/source revision, voltage, maximum input current (or sourced input power), startup demand, duty conditions, connector ratings and measurement evidence. Distinguish controller/data capacity from power distribution capacity.

For a DC row with a sourced current rating: `I_row = quantity × I_unit`; `P_row = voltage × I_row`. Sum currents only within the same supply rail. An unknown required row leaves that rail's total **UNKNOWN**; exclude neither unknown loads nor startup/duty conditions silently. Do not add downstream DC power to its upstream PSU input as independent cabinet loads. AC input, conversion losses and protection require their own device data and review.

Matrix arithmetic currently establishes only `6 × 16 × 16 = 1536` pixels. No physical matrix arrangement or data-port allocation is selected. The old 60 mA/pixel example in the Pinscape review is a sensitivity scenario, not a rating to fill into this worksheet.

## Next input and completion evidence

1. Use the selected CSD kit listing; confirm its order variant, physical dimensions and desired arrangement/location. Record source and revision; do not import vendor files into the repository without license clearance.
2. Fill IF-05 and each lighting zone from that evidence, keeping unconfirmed values open. Clarify the PC requirement before its service study.
3. Add remaining device rows, then review mode dependencies, mapping, power totals, service connectors and motion envelopes.
4. Propose visible carrier/interface geometry only after the inputs support it. Physical sessions remain paused; fit, electrical, thermal, motion and load tests are future evidence.

This pass is documentation and a blank planning dataset. Source geometry and master dimensions are unchanged, so no CAD regeneration is required. It does not replace the existing V32 solid checks or close manufacturing gates.

Original project material: CERN-OHL-S-2.0. Preserve [LICENSE](../LICENSE), [NOTICE.md](../NOTICE.md) and Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.
