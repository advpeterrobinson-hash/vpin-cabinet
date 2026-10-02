# WPC fold positive control and isolated V32 study

The contradictory shelf collision came from the **longitudinal pivot datum**. The previous WPC datum used 1½ inches from the cabinet rear. Pinscape's dimensioned pivot drawing **and** its drilling instructions specify **9½ inches**. With the same cabinet rear at Y1308.1, that is **Y1066.8**, not Y1270. Height remains **Z508**. The documented assembly has one revolute joint on each side, coaxial across the cabinet; the rigid hinge arms are bolted to the backbox floor. No initial lift, sliding slot or extra link is required.

The reference control passes first. The isolated V32 proposal then passes with **210 mm lower side depth**, a **straight floor front at Y1146**, and the original shelf profile plus one generic passage. Accepted geometry, pivot configuration and viewer remain unchanged. This is a kinematic study, not manufacturing approval or a structural load qualification.

HEAD BEFORE: `772f85cc91c20336a0a24b6ec68ce24e866d8cb9`.

HEAD AFTER: the commit containing this report, on `feat/cabinet-review-v32`; the delivery message gives its exact hash. Resolve locally with `git log -1 --format=%H -- studies/wpc-fold-v32/README.md`.

## Evidence and authority

[Source register and parameter classifications](sources.json) records document identities, image URLs and SHA-256 hashes. Existing repository material was inspected first, including the owner-supplied Pinscape MHTML. Public diagrams were then read directly. No third-party images, manual pages or CAD have been imported into this release.

- **DOCUMENTED DIMENSION:** [Pinscape pivot drawing](https://head.pinscape-build-guide.pages.dev/images/side-wall-backbox-pivots.png): 9½-inch rear offset, 20-inch height, ½-inch cabinet bore. The local guide section 6.J.32 independently gives the same offset. [Assembly section](https://head.pinscape-build-guide.pages.dev/#hingeInstall), its [arm diagram](https://head.pinscape-build-guide.pages.dev/images/wpc-backbox-hinge.png), and [attachment diagram](https://head.pinscape-build-guide.pages.dev/images/install-backbox-hinge-6.png) establish the rigid arm / three fixed floor bolts / single side pivot topology.
- **CONFLICTING DOCUMENTED DIMENSION:** [jonaskello README](https://github.com/jonaskello/wpc-cabinet) gives 1½ inches from the rear. This is the source of the incorrect reference adopted locally. Its SKP/F3D geometry was not audited here; do not generalize the README error to those files. Applying that datum to the positive control reproduces immediate shelf collision.
- **MEASURED DIMENSION:** dimensions and distances extracted from local CAD are measurements of modeled geometry, not of physical parts. No physical hinge, bushing or bolt was measured in this task.
- **DERIVED DIMENSION:** inch conversions, placement from common rear/center datums, Y1066.8, contact areas, collision volumes and trajectories.
- **PROVISIONAL ASSUMPTION:** simplified metal silhouettes, nominal metal thickness, displayed bushing length, simplified reference joint partitions, the generic V32 opening and proposed Y1146 floor edge. These are not toolpaths or purchased-hardware specifications.

The reference uses the Pinscape 6½-inch lower side / 10-inch upper side and floor geometry; it does not mix these with the narrower lower-depth numbers in the conflicting README. Nominal reference stock is 19.05 mm, width 558.8 mm, backbox width 730.25 mm and height 723.9 mm. Shelf dimensions are 555.625 ×180.975 mm. The underside lap puts the reference side lower edge 9.525 mm below the bearing floor; those side edges are outboard of the cabinet. Noncritical joinery is simplified and partitioned to avoid internal overlaps. Reference shelf bevel is conservatively filled, without creating interference. The cabinet front height uses the existing 400.05 mm baseline, explicitly a simplification, not a new historical measurement.

## Hinge architecture and actual motion

**REFERENCE WPC MECHANISM — source geometry:** documented Pinscape dimensions and assembly relationships, rebuilt as original simplified parametric primitives, not copied CAD.

**Hinge architecture:** cabinet round side bore ↔ concentric 02-4352 barrel/pivot bushing ↔ 4322-01139-12B square-neck bolt keyed to 01-9011-L/R arm ↔ three fixed fasteners into the backbox floor, with the documented backing-plate relationship. The arm's bent flange creates a **fixed spatial offset** between its pivot and its mounting surface; it does not create another degree of freedom. The left/right arm topology is mirrored.

**Motion type: PURE ROTATION — YES.** In ideal rigid kinematics, every backbox point follows the same rotation around the transverse X axis at Y1066.8/Z508. The bushing/bolt retains the arm axially while allowing the documented pivot action. Exact bearing-fit, shank length, flange stack and purchased bracket bends are not inferred from the schematic cylinders. No source describes a purposeful initial lift or sliding clearance movement; assembly looseness is not used to make the model pass.

For a point initially at (y₀,z₀), with c=cos θ and s=sin θ:

```
y(θ) = yp + (y₀−yp)c − (z₀−zp)s
z(θ) = zp + (y₀−yp)s + (z₀−zp)c
```

The unchanged height of the pivot alone was not enough to reproduce WPC motion: its longitudinal location was essential. Physical 01-9011-L/R, 02-4352 and 4322-01139-12B remain mandatory before final CNC holes or offsets can be released.

## Reference gate and bearing release

**Reference upright valid: YES. Reference 0→90 valid: YES**, for this simplified wood control. All required samples plus 0.001°, 0.01°, 0.05°, 0.1° and each integer angle passed. A separate checker certifies the intervening motion with conservative distance bounds; this is not solely a 1° sampling claim.

**Shelf bearing release begins: 0°+**. **Shelf completely clear: every θ>0**, with infimum 0°. There is no finite release delay. At exactly 0° the bearing area is **69,304.296875 mm²**. For every positive angle it is zero, with positive floor/shelf distance and zero penetration.

**Final intended contact:** the complete upright planar bearing region releases simultaneously, not a rolling edge. Its reference footprint is the intersection of the floor underside and shelf top: X1.5875…557.2125, Y1143…1308.1, excluding the opening X138.1125…420.6875, Y1192.2125…1271.5875. These exact regions are present as the green CAD-derived bearing plot. An unloaded geometric contact region does not determine a real pressure distribution.

The geometric proof also explains why the passage is not the cure. At a rotated floor-bottom point whose current Y still overlaps the shelf,

```
z − z_shelf = (Y−yp) tan θ + (z_shelf−zp)(sec θ−1)
```

Both terms are positive for 0<θ<90° because shelf-front Y>yp and z_shelf>zp. At 90° the whole floor lies forward of the shelf. Thus even filling the service opening would not produce this former shelf collision. The opening serves infrastructure and removes no essential kinematic obstruction here.

The hinge/hand load replaces shelf support immediately on beginning the fold. Upright locks are released before folding; the reference and study are pose-clearance checks, not force, bolt strength, load-sharing or transport-rest designs.

|Angle °|Reference bearing mm²|Reference penetration mm³|Reference gap mm|V32 selected gap mm|
|---:|---:|---:|---:|---:|
|0|69304.296875|0.000000|0.000000|0.000000|
|0.25|0.000000|0.000000|0.331638|0.344728|
|0.5|0.000000|0.000000|0.661577|0.687757|
|1|0.000000|0.000000|1.316333|1.368691|
|2|0.000000|0.000000|2.605186|2.709885|
|5|0.000000|0.000000|6.302976|6.564443|
|10|0.000000|0.000000|11.903194|12.402345|
|15|0.000000|0.000000|18.642453|18.642453|
|30|0.000000|0.000000|42.072842|42.072842|
|45|0.000000|0.000000|68.694424|68.694424|
|60|0.000000|0.000000|96.692982|96.692982|
|75|0.000000|0.000000|124.160462|124.160462|
|90|0.000000|0.000000|149.225000|149.225000|

Distances are unsigned OCC minimum separations. Zero distance plus zero volume means contact; penetration is determined separately by Boolean common volume. No penetration depth is inferred from unsigned distance.

## Re-evaluation of P and the old conclusion

P=(300,1220,596.9) is **actual structural bearing material in the accepted V32 floor and shelf**. It was not an empty-hole artifact in that model. The old derivative −50 mm/rad and reproduced **88,825.888892 mm³** floor/shelf overlap at 1° are correct **for axis Y1270/Z508**.

Using the documented WPC axis gives **dZ/dθ=+153.2 mm/rad** at the same point. Re-running the **original accepted floor against the original accepted shelf**, changing only the isolated analysis axis, gives **zero penetration at 1°**. This counterfactual deliberately does not depend on a new opening or a trimmed floor.

**PREVIOUS “UNAVOIDABLE SHELF COLLISION” CONCLUSION: INCOMPLETE.** Its local calculation was valid for its assumed axis. Its extension to unavoidable WPC behavior is invalid because that axis interpretation was wrong.

In the new generic-passage proposal, P lies within the opening. That later fact is not used to invalidate the original witness: the original-wood test above already isolates the datum error. In the simplified reference opening, the central region around that point is also open.

**ROOT CAUSE OF CURRENT V32 1° COLLISION:** using a pivot 203.2 mm too far aft for the documented WPC architecture makes forward-of-pivot bearing wood move downward. Neither shallow side walls nor a hidden lift mechanism is needed to explain or fix that false architectural conclusion.

## V32 isolated proposal and remaining bottleneck

The initial deep-side candidate retained floor front Y1123.5 and changed the analysis axis. Shelf release passed. A different conflict remained: **floor ↔ both glass channels**, first sampled at **4°**, with 2.657704 mm³ per side. Bisection gives **3.6407833099…3.6407842636°** under the 1e−6 mm³ detection threshold. Later rejected diagnostic samples also hit the channels near the end of travel and cabinet sides at 86°. This candidate is not a valid 45°/90° fold sequence despite isolated middle-angle poses clearing.

The proposed correction is one straight broad floor edge at **Y1146 mm**. It preserves the deep side walls and does not subtract copied channel shapes. This is a simple feasible study dimension, not a globally optimized minimum removal or final production choice.

| Geometry | Isolated study value |
|---|---:|
| A. Backbox side lower depth | **210 mm**; front Y1098.1 |
| B. Floor front extent | **Y1146**; 47.9 mm behind side front |
| Floor rear / finished depth | Y1302.1 / **156.1 mm** |
| Floor width / thickness | 756 / 18 mm |
| C. Shelf front extent | **Y1127.125**, unchanged |
| Shelf rear extent | Y1290.1, unchanged |
| Shelf outer profile, side support, lock material | retained |
| Upright minimum glass-channel clearance | **27.442198 mm** |
| Minimum channel clearance among sweep samples | **5.117865 mm at 90°** |
| Generic passage | **260 ×60 mm**, centered X300/Y1218 |
| Passage-to-floor front / rear wood | **42 / 54.1 mm** |
| Shelf top area before / after opening | **91,917.9 / 76,317.9 mm²** |
| Shelf top area retained | **83.03%** |
| Floor/shelf bearing, selected upright | **65,672.4 mm²** |
| Bearing vs accepted 84,604.625877 mm² | **77.62%** |
| Front bearing band | full 564 mm width ×42 mm to opening |
| Rear bearing band | full 564 mm width ×42.1 mm after opening |
| Lateral bearing strips | 152 mm per side of opening |

Removing shelf wood below the new floor opening causes no additional loss of floor/shelf contact, because the floor is already absent there. The reduced bearing versus the accepted interface comes from the floor trim and larger floor opening. Material area is quantified here without claiming structural capacity. The final upright V32 contact region is X18…582, Y1146…1290.1, minus the rectangular passage X170…430, Y1188…1248; that complete region is the last intended contact at 0°, and it releases for every positive angle.

The established outboard floor hinge material bands X−78…18 /582…678, Y1197…1302.1 are retained. They are **wood retention checks**, not a validation of the old pivot-based keepout. The corrected arm sketch and source bolt-row arrangement extend forward of those historical bands. No final hardware collision envelope or hinge drilling is released. Upright lock material is checked around X120/480, Y1188 using 30.7 mm radius undrilled reserves. Nominal reference mounting diagrams also conflict with the old “approximately 12.7 mm from rear” floor-row shorthand; their row runs longitudinally. Purchased-part measurements must resolve final floor holes, not those old shorthand coordinates.

**Deepest side depth tested: 210 mm.** No new 200, 190 or 180 mm study was run. Existing historical artifacts remain unchanged.

**0° valid: YES. Early twist valid: YES. 0→90 valid: YES**, for the reconstructed moving wood and modeled stationary physical components, including remaining matrix supports. **First collision of the selected proposal: none.** The adaptive checker certifies positive separation throughout 0→90 after the analytical release interval. The quoted 5.117865 mm is the minimum among samples; the adaptive certificate proves collision freedom, not a continuous ≥5 mm tolerance margin.

**GLASS REMOVED and MATRIX REMOVED** are explicit fold prerequisites. Upright validation includes the installed glass and matrix. Located cabinet components are included; unlocated reserve boxes are not treated as wood. Electronics moving inside the backbox, future toys, wires, bought hinge outlines, fasteners, strength, hand forces and a final padded transport stop are not released by this wood-motion study.

## Cable passage and accepted geometry

**Generic cable passage involved: YES**, only as a matching physical route. `reference.service_passage` and `v32.service_passage` have separate width, depth, x_position and y_position parameters. They are independent of connector counts and cable termination choices. The rectangular study openings are provisional; cutter radius/tolerance and structural qualification remain manufacturing gates.

**Generic passage preserved: YES. Connector/disconnect system designed: NO — intentionally USER CONFIGURABLE.** No connector, gland, plate, harness architecture or electrical disconnection method is prescribed.

**PIVOT DATUM changed:** accepted production/configuration **NO**; isolated study interpretation **YES**, from Y1270 to Y1066.8, justified by the documented mechanism. Both values remain explicitly recorded. This report supersedes the old kinematic inference, without silently editing historical reports or accepted source configuration.

**ACCEPTED V32 PRODUCTION GEOMETRY changed: NO.** No cabinet, shelf, backbox, channel, matrix, playfield or viewer source/artifact from the starting HEAD was modified. The candidate lives in separate files for owner review. The initial checkout's unrelated owner changes were not touched.

## Review artifacts

All figures are original CAD-derived plots, with schematic metal labeled. Open the independent study CAD rather than interpreting schematic metal as a manufacturing part.

- [01  WPC reference — upright bearing and rigid arms](../../exports/generated/wpc-fold-v32/01-wpc-upright.png)
- [02  Hinge architecture — fixed offset, pure rotation](../../exports/generated/wpc-fold-v32/02-hinge-pivot.png)
- [03  WPC floor / shelf — 69,304.30 mm² upright bearing](../../exports/generated/wpc-fold-v32/03-reference-interface.png)
- [04  WPC initial twist — actual floor edge, shelf below](../../exports/generated/wpc-fold-v32/04-initial-twist.png)
- [05  Bearing release — immediate separation, no scraping](../../exports/generated/wpc-fold-v32/05-bearing-release.png)
- [06  WPC reference — 15°](../../exports/generated/wpc-fold-v32/06-reference-15.png)
- [07  WPC reference — 45°](../../exports/generated/wpc-fold-v32/07-reference-45.png)
- [08  WPC reference — 90°](../../exports/generated/wpc-fold-v32/08-reference-90.png)
- [09  Current V32 datum — reproduce the old failure](../../exports/generated/wpc-fold-v32/09-current-interpretation.png)
- [10  Correct WPC interpretation — axis ahead of bearing](../../exports/generated/wpc-fold-v32/10-corrected-interpretation.png)
- [11  Separate side / floor / shelf extents — broad straight floor](../../exports/generated/wpc-fold-v32/11-deep-side-floor.png)
- [12  V32 210 mm sides — clean early release](../../exports/generated/wpc-fold-v32/12-v32-early-twist.png)
- [13  Channel bottleneck — isolated floor correction](../../exports/generated/wpc-fold-v32/13-first-bottleneck.png)
- [14  V32 study — 45° / glass and matrix removed](../../exports/generated/wpc-fold-v32/14-v32-45.png)
- [15  V32 study — 90° / glass and matrix removed](../../exports/generated/wpc-fold-v32/15-v32-90.png)

- [Reference upright CAD](../../exports/generated/wpc-fold-v32/reference-0.FCStd)
- [Reference folded CAD](../../exports/generated/wpc-fold-v32/reference-90.FCStd)
- [V32 study upright CAD](../../exports/generated/wpc-fold-v32/v32-0.FCStd)
- [V32 study 45° CAD](../../exports/generated/wpc-fold-v32/v32-45.FCStd)
- [V32 study 90° CAD](../../exports/generated/wpc-fold-v32/v32-90.FCStd)
- [Rejected initial floor bottleneck CAD](../../exports/generated/wpc-fold-v32/v32-initial-bottleneck.FCStd)
- [Full angle/contact/collision report](../../exports/generated/wpc-fold-v32/validation.json)
- [Independent continuous-motion certificate](../../exports/generated/wpc-fold-v32/regression-validation.json)

## Reproduce and verify

From this worktree root:

```sh
freecadcmd studies/wpc-fold-v32/build.py
freecadcmd studies/wpc-fold-v32/check.py
uv run --with numpy --with matplotlib python studies/wpc-fold-v32/render.py
```

Require `WPC_STUDY_PASS`, `WPC_REGRESSION_PASS`, `WPC_IMAGES_PASS 15`; FreeCAD can return exit code zero after a Python exception. Source prerequisites are committed CAD artifacts at the stated starting HEAD. Only this study's own output directory is written. Study solids are script-parametric; saved FCStd poses are reproducible review products, not a replacement expression-driven production master.

The builder passed 47 checks. The independent checker passed 1,932 checks, including exact starting-Git-blob preservation for all **812** source-HEAD file entries, symmetry, valid solids, required angle coverage, wrong-axis negative controls, saved-pose transforms and continuous clearance. Its distance certificate subdivides the range until maximum possible point displacement is smaller than the exact midpoint separation. It required **213 reference evaluations and 231 V32 evaluations**, with an analytical initial bearing-release check for 0…0.001°. The collision engine is the same FreeCAD/OCC BRep common-volume and distToShape approach used in the prior V32 floor study, using 1e−6 mm³ collision threshold. Meshes are used only for illustration.

**KINEMATIC ARCHITECTURE VALIDATED. FINAL HOLES / OFFSETS MANUFACTURING-VALIDATED: NO. MANUFACTURING: BLOCKED.** Physical hardware, measured plywood, cutter diameter, tolerances, tool relief, coupon, strength/retention validation and owner manufacturing approval remain required. The isolated proposal is presented for review; it is not adopted into accepted geometry.

Original project material: CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet. Preserve LICENSE and NOTICE.md. Third-party source status remains its own; only links, identities and attributed engineering observations are included here.
