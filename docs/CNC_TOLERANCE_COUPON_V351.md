# CNC tolerance coupon — V35.1

Status: **required physical qualification; not a manufacturing release**.

V35.1 uses the supplier profile already recorded in `config/manufacturing/profiles/peter_supplier_v1.json`: one-face machining, controlled-depth pockets, Ø4 mm cutter with natural R2, 20 mm perimeter hold-down and 15 mm minimum finished-part spacing. Generic CNC capability is therefore no longer an open design question.

The remaining release evidence is physical: the actual 18 mm and 12 mm plywood lots, the selected fit clearance, and the real 03-7135-1-class side-glass channel.

## Two stock coupons

Generate and cut one coupon from the actual **18 mm production lot** and one from the actual **12 mm production lot**, on the same machine, cutter and CAM setup that will cut the cabinet.

Each coupon tests total slot clearances:

- T − 0.20 mm
- T − 0.10 mm
- T + 0.00 mm
- T + 0.10 mm
- T + 0.20 mm
- T + 0.30 mm

The same fit series is represented at **4 mm** and **6 mm** pocket depth because current V35.1 geometry contains both shallow captured-joinery and 6 mm-class guide/pocket interfaces.

Select fit from the physical mating edge of the same production lot. Record insertion force, veneer damage, lateral play and dry-assembly practicality. Do not select clearance from nominal plywood thickness.

## 03-7135-1 side-channel test

This test belongs on the 18 mm structural coupon only.

First measure the **real purchased profile**:

- tongue width;
- tongue depth;
- free glass-channel opening;
- overall section;
- several points along the extrusion.

Then generate slot trials from those measured values. The V35.1 generator tests:

- width = measured tongue + 0.00 / +0.10 / +0.20 / +0.30 mm;
- depth = measured tongue depth + 0.00 / +0.50 / +1.00 mm.

Any width narrower than the confirmed Ø4 cutter is automatically omitted.

After machining, test with the actual plastic channel **and a real 5 mm glass sample**. Reject a slot that visibly squeezes the extrusion, reduces the glass opening, allows rocking, or permits the profile to pull out too easily. Final production width/depth remain NULL until this physical test passes.

The rear 03-8091-2-class channel is not part of this coupon because its screw positions are dry-fit after CNC.

## Generate

Example for an 18 mm lot measured at 17.82 mm, before the side profile arrives:

```bash
python3 tools/generate_cnc_coupon_v351.py \
  --stock-class 18 \
  --stock-mm 17.82
```

After measuring a real side channel, for example only:

```bash
python3 tools/generate_cnc_coupon_v351.py \
  --stock-class 18 \
  --stock-mm 17.82 \
  --channel-tongue-mm <MEASURED> \
  --channel-depth-mm <MEASURED>
```

And separately for the 12 mm production lot:

```bash
python3 tools/generate_cnc_coupon_v351.py \
  --stock-class 12 \
  --stock-mm <MEASURED>
```

Outputs go to `.work/cnc_coupon_v351/<stock-class>mm/` as SVG, feature CSV and metadata JSON.

## Release record

Before full-sheet release, record:

- lot/sheet IDs for 18 mm and 12 mm stock;
- thickness measurements and range;
- selected total fit clearance for each stock class;
- measured pocket depths;
- finished through-hole errors;
- accepted local T-bone/radius behavior;
- 03-7135-1 measured section;
- selected side-channel slot width/depth;
- physical 5 mm glass/channel result;
- machine/cutter/CAM identity;
- date and operator.

Changing plywood lot, cutter or materially changing CAM compensation invalidates the corresponding coupon evidence.
