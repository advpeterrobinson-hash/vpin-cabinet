# V35.1 — standard widebody, conservative refinement

HEAD BEFORE: `11822cb2dc9c7c7b511348df860cb76196d641be`. HEAD AFTER: the commit containing this report (Git is authoritative).

Reference architecture passes the recorded geometric gates. This is not purchased-part compatibility certification or a manufacturing release. CNC remains BLOCKED. V35/V34.3 unpromoted outputs are study evidence only.

## Dimensional and commercial decision

- Body **628.65 mm**, nominal inside **592.65 mm**. Length **1308.10 mm** retained; no hard commercial length conflict established. Backbox **780 × 723.9 mm**, depth and local internal shapes unchanged; assembly translation X+14.325 mm. Side overhang **75.675 mm**. WPC Y1066.8/Z508 unchanged.
- Commercial lockdown **A-17996 / A-16055** remains the reference class, but the lockdown bar itself is **DRY FIT after CNC**: preserve its envelope and do not use purchased-bar holes as CNC authority. Receiver **A-16773-1**, compatible historical alternative **A-9174-4**, remains a separate unresolved interface until its installation strategy is closed. No custom lockdown/receiver.
- Available receiver body reserve **520 × 42 × 40 mm**, additional operating space **388.65 × 42 × 15 mm**, hand/tool approach **90 × 42 × 85 mm** clear modeled occupied objects. These are independently modeled available volumes, NOT measured vendor geometry or a guessed latch trajectory. Actual receiver withdrawal, tab engagement and latch travel must be measured before CNC.
- Siderails are OPTIONAL, zero in minimum BOM. Original slim envelope stops before backbox; a purchased long SKU may require verified trimming (82.2375 mm in the reference study). Glass works without rail. No integral-rail architecture.
- Primary glass is locally cut **5 mm tempered**; reference603.25 ×1092.20 mm, final cutNULL. Actual side-channel profile must accept5mm;3/16in compatibility is not assumed. Side slot reference7.05mm deep leaves10.95mm outer skin; production slot width/depthNULL.
- Rear **03-8091-2 class** channel uses ordinary screws on the existing horizontal RearBearingShelf with local angled support. The channel is **DRY FIT after CNC**: preserve the envelope and bearing surface, then locate its screws from the real part during assembly. Two integral R2 lands remain in the existing member; no separate wood rail and no channel-specific CNC pilot pattern is required.
- Rear support angle **9.90666925365°** derived from glass faces; whole backbox floor remains horizontal. Display parallel to glass:0° difference, **7.5 /7.5 /7.5 mm** front/center/rear planning gap. M025528.65mm retains22mm landing edge distance; dowel588.65mm; SW02X72/556.65,Y245.

### Playfield display target

- Owner-selected purchase target: **Samsung QN43QN90FAGXZD (QN90F 43-inch)**.
- Samsung official chassis reference: **960.8 × 558.9 × 26.9 mm**, **9.4 kg**, **VESA 200 × 200 mm**, 120 Hz panel with PC input up to **4K/165 Hz**.
- Status: **purchase target selected; V35.1 CAD/kinematic validation still pending**. Do not claim the QN90F as validated until the existing PLAY / 0–50° / 48 mm lift-out and interference checks are rerun against this exact envelope.
- The cabinet remains a replaceable 42/43-inch-class architecture rather than a TV-specific shell.

## Retained structure and small-part audit

All three CROSS members, all three SHELF members, guides, shelf supports, M006, SW01×4, SW02×2, open cradles and PC_BASE retained. Protected fixed-section parts compare exactly after inverse placement. Crossmember/shelf lateral spans regenerate without section reduction. No drawer added. Backbox simplified internals remain rigidly unchanged.

No part-count target. **66 wood /60 CNC plywood /6 solid /45 families**, unchanged count. **33 small pieces KEEP**. Integrated0; retired0; added0. The optional fan blanks have a sealing/dust role for unused upper stations; they are not required in passive-grille mode. Old integral-siderail requirement is retired from the promotion path, not a wood part.

| Part / family | Decision and reason |
|---|---|
| M010 · SHELF_SUPPORT_1L | KEEP — Broad42x150 support; spreads load without further thinning side; service screws remain accessible. |
| M011 · SHELF_SUPPORT_1R | KEEP — Broad42x150 support; spreads load without further thinning side; service screws remain accessible. |
| M010 · SHELF_SUPPORT_2L | KEEP — Broad42x150 support; spreads load without further thinning side; service screws remain accessible. |
| M011 · SHELF_SUPPORT_2R | KEEP — Broad42x150 support; spreads load without further thinning side; service screws remain accessible. |
| M012 · SHELF_SUPPORT_3L | KEEP — Broad42x150 support; spreads load without further thinning side; service screws remain accessible. |
| M013 · SHELF_SUPPORT_3R | KEEP — Broad42x150 support; spreads load without further thinning side; service screws remain accessible. |
| M015 · CROSS_GUIDE_1L | KEEP — 145x60 backing; repeatable location and removable transverse members. Retain rather than deeper side routing. |
| M016 · CROSS_GUIDE_1R | KEEP — 145x60 backing; repeatable location and removable transverse members. Retain rather than deeper side routing. |
| M015 · CROSS_GUIDE_2L | KEEP — 145x60 backing; repeatable location and removable transverse members. Retain rather than deeper side routing. |
| M016 · CROSS_GUIDE_2R | KEEP — 145x60 backing; repeatable location and removable transverse members. Retain rather than deeper side routing. |
| M015 · CROSS_GUIDE_3L | KEEP — 145x60 backing; repeatable location and removable transverse members. Retain rather than deeper side routing. |
| M016 · CROSS_GUIDE_3R | KEEP — 145x60 backing; repeatable location and removable transverse members. Retain rather than deeper side routing. |
| M029 · MX_WoodSeatL | KEEP — Preserves accepted rocking/forward/lift path; attachment pilots follow centered matrix. |
| M029 · MX_WoodSeatR | KEEP — Preserves accepted rocking/forward/lift path; attachment pilots follow centered matrix. |
| M062 · BB_HingeCleatL | KEEP — 23mm bearing width and14mm finished depth; preserves hinge axis and avoids driving into a weak edge. |
| M062 · BB_HingeCleatR | KEEP — 23mm bearing width and14mm finished depth; preserves hinge axis and avoids driving into a weak edge. |
| M064 · BB_UprightLockLParkingPad0 | KEEP — 36mm stack keeps parked shaft above floor;18mm floor alone loses this depth. No reduced blind thread reserve. |
| M065 · BB_UprightLockLParkingPad1 | KEEP — 36mm stack keeps parked shaft above floor;18mm floor alone loses this depth. No reduced blind thread reserve. |
| M064 · BB_UprightLockRParkingPad0 | KEEP — 36mm stack keeps parked shaft above floor;18mm floor alone loses this depth. No reduced blind thread reserve. |
| M065 · BB_UprightLockRParkingPad1 | KEEP — 36mm stack keeps parked shaft above floor;18mm floor alone loses this depth. No reduced blind thread reserve. |
| M066 · BB_FanBlankL | KEEP — Real dust/closed-station role for unpopulated build; not needed for grille-only airflow. Retain OPTIONAL, not required assembly. |
| M066 · BB_FanBlankR | KEEP — Real dust/closed-station role for unpopulated build; not needed for grille-only airflow. Retain OPTIONAL, not required assembly. |
| SW01 · CandidateLegBlockFL | KEEP — SW01 protected; load distribution and drill-jig architecture retained. |
| SW01 · CandidateLegBlockFR | KEEP — SW01 protected; load distribution and drill-jig architecture retained. |
| SW01 · CandidateLegBlockRL | KEEP — SW01 protected; load distribution and drill-jig architecture retained. |
| SW01 · CandidateLegBlockRR | KEEP — SW01 protected; load distribution and drill-jig architecture retained. |
| M074 · Underfront_Plate | KEEP — 12mm replaceable module, shared bay and four machine attachments; final controls held. |
| SW02 · FrontLandingL_Block | KEEP — SW02 protected, side-relative location; no merged plywood substitute. |
| SW02 · FrontLandingR_Block | KEEP — SW02 protected, side-relative location; no merged plywood substitute. |
| M075 · BB_MONITOR_STOP_L | KEEP — 12x18 actual plate overlap216mm2 per stop; integral4mm guide stop only72mm2. Separate block is replaceable without repairing side. |
| M075 · BB_MONITOR_STOP_R | KEEP — 12x18 actual plate overlap216mm2 per stop; integral4mm guide stop only72mm2. Separate block is replaceable without repairing side. |
| M077 · BB_GLASS_TOP_RETAINER | KEEP — One simple removable strip; needed to remove acrylic from FRONT without shell-top removal. |
| M037 · BB_GLASS_BOTTOM_SEAT | KEEP — 744x18 seat is replaceable and keeps acrylic separate from removable DMD panel; no thinner structural side pocket. |

The full 66-row attachment audit records parent, attachment, load, assembly and service value. Parking pads retain36mm insert/shaft depth instead of forcing the parked shaft through18mm floor. Monitor stops retain216mm² bearing each versus72mm² for a blind4mm guide stop. Hinge cleats preserve backing and axis. Acrylic lower seat remains replaceable and independent of DMD removal; upper strip provides positive fold retention.

## Structural planning limit

No support or section was deleted. Increased nominal span ratio is1.050798. For an ideal same-section beam under the same central force, stress ratio1.0508, deflection ratio1.1603; at equal distributed load/length, ratios1.1042/1.2192. These are relative planning sensitivities, not load certification. It would be false to claim an unchanged numerical safety factor solely from B-rep validity. Retaining all supports is the conservative response; physical material/load qualification remains mandatory.

## Tukkari-first functional review

Public [premium assembly guide](https://www.tukkari.com/advisor/assembly-guide-widebody-vpin-cabinet-premium-flat-pack) reviewed2026-10-06: established shell/holder/front interfaces inform the design. The guide treats siderails as optional and illustrates screw-fixed rear glass channel. Its dimensions/counts were not copied. No proprietary geometry imported.

| Assembly | Our wood pieces | Functional comparison / justification |
|---|---:|---|
| Main shell | 12 | Captured shell assembly; ours keeps floor ledges and solid leg load spreaders. |
| Playfield support | 5 | Holder fitted parallel to glass; ours retains accepted open cradles, wooden dowel and SW02 landings. |
| Internal shelves | 9 | No equivalent three-shelf detail established in reviewed public guide; owner retains service shelves and broad supports. |
| Crossmembers | 9 | No equivalent three-crossmember detail established; owner protects transverse stiffness and guide bearing. |
| Backbox shell/supports | 9 | Planar floor/side/top assembly; ours retains one-face joints, rear access and accepted fold structure. |
| Monitor | 3 | Fixed plate/front monitor service adopted; separate stops retain three times the proposed blind-guide bearing. |
| DMD/speakers | 1 | Simple front panel adopted; actual display/speaker cuts held. |
| Acrylic seats/retainer | 2 | Simple edge seating and removable upper retention; acrylic follows owner decision. |
| Doors/fan blanks | 8 | Rear service access retained; ordinary hardware; hinge backing and optional upper blanks retain real functions. |

Counts are grouped functional subsets, not claimed Tukkari BOM counts. No public equivalence was invented for our shelves/crossmembers. Detailed source register: [V35.1 public references](../library/references/v351-standard-parts.md).

## Material, nesting and packing

Actual finished B-rep wood mass at550/650/750kg/m³: **52.767 /62.361 /71.955 kg**. Nominal change+1.179kg. Glass reference8.236kg separate. Hardware mass UNKNOWN, not zero. Only12/18mm plywood; solid blocks are separate.

| Stock | Pieces | Sheets preliminary | Outer area m² | Utilization | Unused full-sheet area m² |
|---|---:|---:|---:|---:|---:|
| 18mm | 43 | 2 | 5.556000 | 69.45% | 2.444000 |
| 12mm | 17 | 1 | 1.062104 | 26.55% | 2.937896 |

**2×18mm recovered;1×12mm.** Deterministic four-order MaxRects rectangle study, actual contours shown;2500×1600 sheets,20mm border,15mm spacing. Long piece axis aligned to sheet long grain. No strength reduction; small pieces occupy residual zones. Largest free rectangles are in nesting.json and may overlap, so their areas must not be summed. Unused area includes border/spacing/offcuts, not all reusable stock. This is not production nesting.

| Bundle | External mm | Nominal wood kg | HIGH +1kg allowance |
|---|---|---:|---:|
| PK01 | 820.0 × 763.9 × 139.0 | 17.135 | 20.771 |
| PK02 | 1355.9 × 640.7 × 243.8 | 20.774 | 24.970 |
| PK03 | 1355.9 × 636.9 × 129.8 | 20.787 | 24.985 |
| PK04 | 1192.1 × 440.0 × 226.0 | 3.665 | 5.229 |

All four bundles remain≤25kg HIGH planning including1kg packaging allowance. Hardware separate; no glass/electronics in wood bundles. Physical packaging qualification pending.

## Assembly, service and cost

Manual **59→59 steps**; explicit alignment/measurement action steps **11→11**. These are document counts, not measured labor time. Dry fit SAME; existing T-guide pilots/hinge-cleat templates and F06 reinforcement remain inherited qualification holds. No builder is instructed to improvise structural placement. Labor SAME planning; actual hardware-change/time count unresolved.

Commercial compatibility IMPROVED; plywood projection2×18+1×12; overall qualitative cost direction NEUTRAL/uncertain without quotations (avoids bespoke lockdown fabrication). No invented price.

Normal fold: remove main glass and matrix, release/park rear locks, close/latch doors, fold. Backbox acrylic and front DMD/speaker panel remain installed; no routine disconnection. Raised playfield support remains outside scope/HOLD. Historical 42C5 and 43QN93D thin reference envelopes pass; the owner-selected QN90F 43-inch is the new purchase target but still requires an exact-envelope rerun before it is called validated. The 77 mm-deep 40S5K remains an explicit failed sensitivity case.

## Validation

| Evidence | Passing checks |
|---|---:|
| geometry.json | 502/502 |
| validation.json | 82/82 |
| continuous-motion.json | 10/10 |
| conservative-validation.json | 39/39 |
| browser-validation.json | 26/26 |

Manufacturing reconstruction maximum difference **0.0 mm³**.32 native-CAD review images; offline desktop/tablet, EN/PT-BR and palettes retained. Collision/kinematic checks prove the modeled reference state only; purchased hardware and human/structural qualification remain open.

## Remaining release gates

Actual blockers are now narrower. **Lockdown-bar purchase and rear-channel screw locations are not full-sheet CNC gates** because both are dry-fit interfaces with protected envelopes. Remaining gates include: receiver strategy/fit if it controls permanent machining; measured **03-7135-1-class side-channel profile** and side-slot coupon; actual plywood lot and tolerance coupon; CNC-provider/tooling parameters and fit regeneration; exact QN90F envelope rerun; any permanent button/USB, leg/WPC/shooter, DMD/speaker or landing interfaces that still control CNC; T-guide attachment and hinge-cleat placement methods if they are promoted to permanent CNC pilots; physical load/nudge/glass-edge/thermal qualification; and the primary raised-playfield service support. Final 5 mm glass size is cut/tempered after cabinet/channel dry fit and is not itself a pre-CNC purchase gate. **CNC FULL-SHEET RELEASE REMAINS BLOCKED.**

F06 remains required mechanical reinforcement for the captured shell, but it is **not a full-sheet CNC gate**: the current manufacturing geometry contains no F06-specific pocket or pilot. The selected pocket-hole jig/screw family is qualified after shell dry fit and before assembly.
