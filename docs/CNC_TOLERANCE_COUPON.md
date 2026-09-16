# CNC tolerance coupon v0.20

Status: **required pre-production test**.

The permanent cabinet is designed around nominal 18 mm plywood, but production toolpaths must use the **measured stock thickness** and the actual CNC provider's tooling/compensation behavior.

## Why this exists

Plywood sold as 18 mm may not measure exactly 18.00 mm. A small mismatch can make a captured flat-pack cabinet either impossible to assemble or too loose to remain square.

The coupon therefore tests the real combination of:

- actual sheet thickness;
- cutter diameter/runout;
- CAM compensation;
- pocket depth accuracy;
- internal-corner strategy;
- through-hole size;
- engraving process.

## Generate

After measuring the actual structural plywood and confirming the router bit with the CNC provider:

```bash
python3 tools/generate_cnc_coupon_v20.py --stock-mm 17.82 --cutter-mm 6.00
```

Replace `17.82` and `6.00` with the real measured values.

Outputs are written under:

`.work/cnc_coupon_v20/`

including:

- `cnc_coupon_v20.svg`
- `cnc_coupon_v20_features.csv`
- `README.txt`

The SVG contains operation-intent groups:

- `THROUGH_CUT`
- `POCKET_6MM`
- `ENGRAVE_WHITE`

These names do **not** substitute for CAM setup. Confirm the provider's interpretation and assign toolpaths/depths explicitly.

## Dado trials

The coupon produces four nominal groove-width trials based on the measured stock thickness:

- T - 0.20 mm
- T + 0.00 mm
- T + 0.20 mm
- T + 0.40 mm

Use a clean offcut of the actual production plywood as the mating edge. Evaluate:

- insertion force;
- whether the veneer crushes;
- lateral play;
- glue allowance;
- whether dry assembly remains practical without hammering.

The final cabinet clearance is selected from the physical test, not from a generic plywood rule.

## Through holes

The coupon includes nominal circular through-hole trials at:

- 4 mm
- 5 mm
- 6 mm
- 8 mm
- 9 mm
- 12.7 mm

Measure the finished diameters with calipers and record the provider/tool compensation result.

## Internal corners

The coupon contains a plain internal-corner pocket and a dogbone-intent sample sized around the confirmed cutter radius.

Use these to agree with the shop on where dogbones are actually required. Cosmetic external edges should remain clean; dogbone relief is only used where a square mating tab truly requires it.

## Engraving

The coupon includes line-weight trials around the current white-filled engraving target. During CAM, pair these with depth trials around the project target (approximately 0.4–0.8 mm).

The production release should use text converted to curves where the shop workflow requires it.

## Record results

Before production sheets are authorized, record:

- sheet ID/batch;
- measured thickness range;
- selected dado width/clearance;
- measured hole errors;
- selected dogbone/radius convention;
- engraving process and depth;
- bit/tool ID;
- CNC provider/CAM notes.

If production plywood or tooling changes materially, repeat the coupon.

## Release rule

**No cabinet production sheet should be cut before the coupon passes physical fit inspection.**
