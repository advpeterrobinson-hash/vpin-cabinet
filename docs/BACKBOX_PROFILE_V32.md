> **SUPERSEDED — INCORRECT LONGITUDINAL PIVOT INTERPRETATION.** Pivot-dependent results below are historical, not active engineering. Correct WPC reference: Y1066.8/Z508, 241.3 mm from rear. See [positive control](../studies/wpc-fold-v32/README.md) and [structural integration review](../studies/backbox-structure-v32/README.md). Other historical findings retain their original scope.

# V32 backbox side-profile study — OWNER STOP / NO SELECTION

HEAD BEFORE: `3b1bae78c5361ac0c80e644c9c1d748a506d0821`.
HEAD AFTER: commit containing this report; the delivery report provides the exact resulting hash.

**No requested profile can be selected under the fixed constraints.** The 210, 200 and 190 mm candidates fail upright 0° against the accepted glass channels. The 180 mm warning candidate passes upright but triggers the owner's explicit stop below 190 mm. No candidate fold sweep is run after these gates. The current accepted floor at Y1123.5 and all accepted cabinet systems remain unchanged.

A second, independent incompatibility exists between the fixed bearing surface and reference axis: a retained floor bearing point initially moves down into the unchanged rear shelf. Sloping the sides does not change that rigid-body velocity. This study reports the conflict rather than moving the axis, modifying the shelf, trimming the floor independently or adopting a shallow profile.

## Fixed geometry and actual CNC candidates

Every candidate uses outer width 780 mm, height 723.9 mm, top depth 254 mm, nominal stock 18 mm, rear plane Y1308.1 and floor bottom Z596.9. The cabinet remains 600 mm wide; shelf front is Y1127.125. Reference pivot remains (300,1270,508) mm with Ø12.7 reference hole and 59.8375 mm outer-edge hinge inset.

The eight source wood members are rebuilt from the V14 backbox-only definitions, with the established V25 nominal 6 mm joint captures and V27 floor passports/rear-frame cuts. Side panels are single CNC solids with vertical rear, horizontal top/bottom and one straight sloping front edge. Floor front follows the side's bottom front; the horizontal top front follows the side slope at its underside. Floor/top edges are square cuts, without invented bevel machining, horns, decorative curves or local channel reliefs. The topmost side depth remains 254 mm. No custom metal or additional hardware is generated.

The four FCStd files are **study candidates**, not replacements for CURRENT accepted CAD. No final joint CAM, cutter radius, dogbone or hole pattern is released. The nominal joint captures are inherited engineering geometry; actual stock/tool/tolerance and assembly-fit qualification remain open.

## Candidate comparison

Angles are measured from vertical. Negative shelf projection means the backbox front extends ahead of the shelf. Dimensions are mm unless specified.

| Metric | 210 | 200 | 190 | 180 WARNING |
| --- | ---: | ---: | ---: | ---: |
| Bottom outer depth | 210 | 200 | 190 | 180 |
| Front slope, degrees | 3.478266 | 4.266131 | 5.052384 | 5.836733 |
| Lower front Y | 1098.1 | 1108.1 | 1118.1 | 1128.1 |
| Joint-resolved floor depth | 204 | 194 | 184 | 174 |
| Internal lower depth before fascia/equipment | 192 | 182 | 172 | 162 |
| Upright 0° valid | NO | NO | NO | YES |
| Floor/channel separation | 0; penetration | 0; penetration | 0; penetration | 9.617752 |
| Shelf forward projection | −29.025 | −19.025 | −9.025 | +0.975 |
| Exact shelf bearing area, mm² | 84604.625877 | 84604.625877 | 84604.625877 | 84054.725877 |
| Bearing retained vs current floor | 100% | 100% | 100% | 99.350036% |
| Continuous bearing width | 564 | 564 | 564 | 564 |
| Floor/side joint length | 204 | 194 | 184 | 174 |
| Nominal 6 mm joint engagement area per side, mm² | 1224 | 1164 | 1104 | 1044 |
| Geometric screw positions per side before hinge exclusion | 4 | 3 | 3 | 3 |
| Positions per side outside reserved hinge band + buffer | 2 | 1 | 1 | 1 |
| Pitch of remaining positions | 50 | N/A: one point | N/A: one point | N/A: one point |
| Minimum longitudinal end distance | 25 | 25 | 25 | 25 |
| Edge-driven screw axis to top/bottom of 18 mm floor | 9 | 9 | 9 | 9 |
| Minimum floor planar ligament | 60 | 59.9 | 49.9 | 39.9 |
| Nominal skin behind 6 mm side capture | 12 | 12 | 12 | 12 |
| Available LEFT toy mounting area, mm² | 37593.203260 | 37557.284928 | 37521.204608 | 37484.962844 |
| Available RIGHT toy mounting area, mm² | 37593.203260 | 37557.284928 | 37521.204608 | 37484.962844 |
| Candidate fold performed | NO | NO | NO | NO |
| Fold result | Rejected before fold | Rejected before fold | Rejected before fold | Owner stop below 190 |
| First observed collision angle | 0° | 0° | 0° | None at 0°; no fold sampled |

All internal wood pairs are non-intersecting; each member is one valid solid. Intentional floor/shelf surface bearing has zero intersection volume. No structural certification follows from area or valid-solid checks.

Exact unintended intersections at 0°:

| Candidate | Offending floor / obstacle | Volume, mm³ |
| --- | --- | ---: |
| 210 | BackboxFloorV14 / CandidateGlassChannelL | 529.636040 |
| 210 | BackboxFloorV14 / CandidateGlassChannelR | 529.636040 |
| 210 | BackboxFloorV14 / CandidateGlass | 54886.088300 |
| 200 | BackboxFloorV14 / CandidateGlassChannelL | 319.963892 |
| 200 | BackboxFloorV14 / CandidateGlassChannelR | 319.963892 |
| 200 | BackboxFloorV14 / CandidateGlass | 27375.553538 |
| 190 | BackboxFloorV14 / CandidateGlassChannelL | 2.221762 |
| 190 | BackboxFloorV14 / CandidateGlassChannelR | 2.221762 |
| 180 | None among modeled physical PLAY components | 0 |

Candidate documents retain source member names for traceability; their enclosing document and `ApprovalStatus` identify their depth and rejected/warning status. This does not make the candidate floor a current V14 or V32 production part.

## Why the depth rule stops the study

With a straight floor front following the lower side profile, actual channel-distance calculations give:

| Required clearance | Minimum floor-front Y | Maximum bottom outer depth |
| --- | ---: | ---: |
| Absolute 3 mm | 1121.383564 | **186.716436 mm** |
| Preferred 5 mm | 1123.413837 | **184.686163 mm** |

These are feasibility bounds, not new adopted floor trims. Even the 3 mm requirement is incompatible with a bottom depth ≥190 mm at the accepted rear/floor/channel datums. Therefore the deepest-valid selection rule has no eligible result.

Reducing 210→180 mm would lose 30 mm of lower internal depth, 30 mm of side/floor joint length (14.706% of its 204 mm length), 180 mm² of nominal captured bearing per side, and 10,858.5 mm² of gross side-wall area per side. The net reserved toy area falls less, by 108.240416 mm² per side, because most of the removed front area was already excluded by display/tool reserves. This smaller net change must not be mistaken for no volume or joint penalty. The 180 mm floor loses 549.9 mm² of shelf bearing. It is not adopted.

## Rear shelf / reference-axis incompatibility

The following uses local rigid-body kinematics at 0°, not a fold sweep of an invalid candidate. All four CAD floors contain the same wood above point **P=(300,1220,596.9)**. The exact accepted shelf contains wood immediately below P. This point is between/behind the unchanged cable passages, so it is not an empty-hole artifact.

For positive X-axis rotation that folds the top forward, around **A=(300,1270,508)**:

`dY/dθ = −(Z−508) = −88.9 mm/rad`

`dZ/dθ = Y−1270 = −50 mm/rad`

The bearing point starts moving downward into the shelf. Continuity makes this an immediate contact incompatibility for positive rotation, independently of the sloping front or chosen bottom depth. A shallower front that still retains this bearing region does not fix it. This also explains why the prior floor-only solution encountered the shelf at its first 1° sample.

**STOP: the rear shelf / floor height / rigid reference-axis relationship is limiting.** No shelf, hinge datum or cabinet geometry is changed. A valid architecture needs this relationship resolved using physical WPC geometry and an explicit decision on any incompatible fixed reference. Selecting another slope alone cannot resolve it.

| Required motion category | Result in this task |
| --- | --- |
| A. Structural wood / cabinet wood | No candidate sweep; 210–190 rejected at zero |
| B. Floor / rear shelf | Intentional upright contact; analytical initial downward penetration under fixed axis |
| C. Wood / glass channels | Exact zero failures above; 180 warning clear at zero only |
| D. Stationary matrix supports | No new-conflict fold conclusion: no valid baseline; unchanged |
| E. Backglass/service envelope / cabinet | Fold NOT EVALUATED |
| F. DMD/service envelope / cabinet | Fold NOT EVALUATED |
| G. Harness/pinch keepout | Complete moving harness absent; NOT VERIFIED |

GLASS REMOVED and MATRIX REMOVED remain explicit prerequisites for any later authorized fold test. `PF_BackboxCheckEnvelope` remains **REFERENCE ONLY**. The physical purchased hinge is not replaced by an invented bracket or hole pattern.

## Joint and fastener planning limits

Coordinates in `validation.json` are planning axis points, not drilled holes or selected SKUs. Longitudinal end allowance is 25 mm; minimum pitch is 50 mm. The current outboard hinge material reserve is Y1197…1302.1. This study conservatively excludes that entire unmeasured band plus 20 mm, leaving two side-fastener points for 210 and one for each smaller candidate. The unexcluded counts are shown to distinguish available wood from unresolved hardware constraints.

Remaining planning points, mirrored in X, are X−81 / X681 and Z605.9: Y1123.1,1173.1 for 210; Y1133.1 for 200; Y1143.1 for 190; Y1153.1 for 180. These are side-driven floor-edge axis locations. Only 9 mm lies above/below the axis in the floor thickness. **They are not qualified structural screw groups.** Actual screw diameter, edge-grain suitability, pull-out, splitting and hinge-zone compatibility belong to the V33 fastener library and measured hinge design. No dense screw pattern or extra reinforcement is introduced to disguise insufficient certainty.

All candidates preserve the existing rear hinge-band wood and leave lock corridors at X120/480. Candidate lock-center Y corridors are 1157.825…1259.4 for 210–190, and 1158.8…1259.4 for 180. Existing floor cable passports remain open; the unchanged shelf still lacks matched passages. The inherited reference hinge row still leaves only 3.525 mm beyond a reference Ø6.35 bore to the joint-resolved rear floor edge. No such bore is cut or accepted as final. Hardware-zone preservation means existing material is retained, not that unmeasured hardware fits or final fasteners are certified.

## Future toy / electronics infrastructure

Both sides have explicit available-area solids after subtracting conservative projected reserves for current display, speakers/DMD, display rails, harness, hinge and service-tool access. Boundaries start 20 mm inside the usable perimeter beyond floor/top/rear stock. A 40 mm inward toy-depth assumption is checked against the modeled payload. The side areas are generic mounting capacity; fitting a particular chime or bell remains dependent on actual purchased dimensions, access and load. No permanent component hole pattern is generated.

The display reserve uses the existing located 740 × 100 × 450 mm backglass envelope with a 10 mm service margin. DMD/speaker projections use the existing located V27 payloads with the same margin. The larger future FullDMD envelope still lacks a confirmed placement. Projected display/rail exclusions are intentionally conservative even where their X extents do not physically occupy the side itself; they preserve tool and replacement access. The rail corridor is a **provisional planning reserve**, not a new installed rail system. Existing payload reserves are not redesigned or claimed to fit a finalized bezel/fascia.

Generic rear removable-board service reserve: **X180…420, Y1240…1272, Z850…1150 mm** (240 × 32 × 300). A 240 × 300 × 12 mm replaceable panel is a planning assumption within it. Generic lower service/toy reserve: **X220…380, Y1220…1270, Z675…750 mm** (160 × 50 × 75). Both reserves clear the modeled wood and source display/speaker payloads in all candidates. Their mounting and independent removal are not released designs because no backbox profile is selected.

Architecture remains: permanent wood → generic removable board → component or printed holder, with detachable wiring. Optional chimes, bells, contactors, strobes, sirens, beacons, controllers, relays and distribution modules are **future purchases, not mandatory flatpack BOM items**. No complete moving harness is invented; harness/pinch reserve remains separate from verified geometry.

## Provisional mass and load model

All values below are assumptions or calculations from candidate CAD, not vendor-specific published masses. Eight structural wood volumes use assumed density **650 kg/m³**. A 520 × 460 × 15 mm nominal removable rear-door allowance uses that density; additional front wood is 1.5 kg. Payload allowances: backglass 7 kg; DMD 1.2 kg; speakers 1.6 kg total; display mount 1.5 kg; wiring 1 kg; electronics 1 kg; future backbox fans 0.4 kg; future toys 4 kg total, equally split between side-zone centroids. Budget allowances add no mandatory BOM components.

The accepted matrix is a separate cabinet cassette and is removed before folding; its moving backbox mass contribution is **0 kg**. The accepted four cabinet fans also contribute **0 kg** to backbox mass. The 0.4 kg allowance is for possible additional backbox equipment, not a relocation or thermal redesign of accepted fans.

| Mass/load metric | 210 | 200 | 190 | 180 WARNING |
| --- | ---: | ---: | ---: | ---: |
| Total planning mass, kg | 32.386452 | 32.212543 | 32.038634 | 31.864726 |
| CG X, mm | 300 | 300 | 300 | 300 |
| CG Y, mm | 1189.788287 | 1190.548927 | 1191.273002 | 1191.959913 |
| CG Z, mm | 963.052009 | 964.289189 | 965.539588 | 966.803419 |
| CG relative to pivot ΔX, mm | 0 | 0 | 0 | 0 |
| CG relative to pivot ΔY, mm | −80.211713 | −79.451073 | −78.726998 | −78.040087 |
| CG relative to pivot ΔZ, mm | 455.052009 | 456.289189 | 457.539588 | 458.803419 |
| Upright gravity shelf reaction, N | 317.602600 | 315.897137 | 314.191675 | 312.486212 |
| Gravity-only locking-bolt tension, N each | 0 | 0 | 0 | 0 |
| Example 0.3g horizontal load: lock tension, N each | 91.948004 | 90.699315 | 89.536914 | 90.873909 |
| Maximum quasi-static reference hinge force, N each | 99.803040 | 99.823588 | 99.811522 | 99.766841 |
| Maximum unbalanced gravity torque, N·m | 146.753796 | 146.308917 | 145.866417 | 145.426297 |

Upright weight is assigned to shelf bearing, with CG projected inside the bearing interval. Zero gravity-only bolt tension does **not** eliminate locking bolts or their preload/retention duty. For the example 0.3g horizontal case, two bolts share tensile reaction after overturning moment exceeds gravity restoring moment about either bearing edge; their provisional Y is the midpoint of the available lock corridor (1208.6125 or 1209.1). Prying, local contact pressure, vibration and selected hardware capacities are not certified. A factor-2 sensitivity doubles the reported reactions, not the hardware rating.

Folding loads are **hypothetical free-space static equilibrium only**, independently of geometry validity. A vertical operator force acts at the top-front center (300,1054.1,1320.8) to balance gravity torque. Hinges share the residual vertical reaction equally; a free pivot is not assumed to carry a resisting moment. These are not collision-tested 45°/90° poses. Without hand force, gravity torque would accelerate the assembly; no static fold equilibrium exists.

| Reference load angle | Hinge reaction per side across candidates, N | Gravity torque across candidates, N·m |
| --- | --- | --- |
| 0° just off bearing, hypothetical | 99.767…99.824 | 24.386…25.475 |
| Early 1°, hypothetical | 97.811…97.959 | 26.885…27.994 |
| 45°, hypothetical | 74.705…76.172 | 118.622…120.209 |
| 90°, hypothetical | 68.048…69.895 | 143.370…144.526 |

Gravity torque grows strongly toward horizontal as CG moves forward. Floor/side joints must transfer load into the arms after bearing unloads, and fastener-group leverage matters more than simply increasing screw count. In this geometry the shelf does not unload cleanly: the local derivative proves penetration instead. Consequently these load estimates are budgeting information only, not a functional fold approval or final structural sizing.

## Selection and preservation report

- Selected bottom depth / slope: **NONE / N/A**.
- DEEPEST VALID CANDIDATE SELECTED: **NO**; no eligible valid candidate.
- Selected backbox 0° valid / 0→90 valid: **NO selected structure / NOT VALIDATED**. Warning 180 passes zero only.
- Minimum structural clearance: 0 mm for rejected zero candidates; no valid fold minimum exists.
- Rear-shelf bearing: 100% retained in 210–190; 99.350036% in warning 180.
- Hinge / lock / floor-passport material zones preserved: **YES**, subject to measurement and matched-shelf gate.
- Future side zones / rear removable-board reserve available: **YES as provisional CAD reserves**, not released installations.
- Reference hinge datum unchanged: **YES**. Physical WPC hinge measurement required: **YES**.
- All accepted V32 systems preserved: **YES**. No accepted current floor, shelf, cabinet, playfield/pivot/buttons/notches, fans/filters, PCBase, SSF, rear door, power/RJ45, matrix architecture/route or viewer bytes are changed.

## CAD, review views and checks

Actual candidate assemblies: [210](../exports/generated/backbox-profile-v32/candidate-210.FCStd), [200](../exports/generated/backbox-profile-v32/candidate-200.FCStd), [190](../exports/generated/backbox-profile-v32/candidate-190.FCStd), [180 warning](../exports/generated/backbox-profile-v32/candidate-180.FCStd).

1. [Old V14 rectangular side](../exports/generated/backbox-profile-v32/01-old-v14-side.png)
2. [210 side](../exports/generated/backbox-profile-v32/02-candidate-210-side.png)
3. [200/190/180 comparison](../exports/generated/backbox-profile-v32/03-200-190-180-comparison.png)
4. [Profile overlay](../exports/generated/backbox-profile-v32/04-side-profile-overlay.png)
6. [Candidate floors — no selection](../exports/generated/backbox-profile-v32/06-candidate-floors-no-selection.png)
8. [Shelf relationship](../exports/generated/backbox-profile-v32/08-shelf-lower-backbox-relation.png)
9. [Hinge/bearing relationship](../exports/generated/backbox-profile-v32/09-hinge-bearing-relationship.png)
10. [Left toy zones](../exports/generated/backbox-profile-v32/10-l-future-toy-zones.png)
11. [Right toy zones](../exports/generated/backbox-profile-v32/11-r-future-toy-zones.png)
12. [Rear removable board](../exports/generated/backbox-profile-v32/12-rear-removable-board-zone.png)
13. [Mass/CG](../exports/generated/backbox-profile-v32/13-mass-cg-planning.png)
18. [Unselected architecture comparison](../exports/generated/backbox-profile-v32/18-architecture-comparison-no-selection.png)

Views 05, 07 and 17 require a selected assembly, which does not exist. Views 14–16 would imply an authorized candidate fold beyond the stop gates, so are not generated. Views 06 and 18 are explicitly candidate comparisons. Images derive from real CAD tessellation/sections; no AI artwork. Current viewer is untouched.

Reproduce from repository root:

```sh
freecadcmd tools/backbox_profile_v32_entry.py
freecadcmd tools/check_backbox_profile_v32.py
uv run --with matplotlib --with numpy python tools/render_backbox_profile_v32.py
```

Require explicit PASS markers, not just FreeCAD's exit status. [Geometry report](../exports/generated/backbox-profile-v32/validation.json), [independent regression checks](../exports/generated/backbox-profile-v32/regression-validation.json) and [review manifest](../exports/generated/backbox-profile-v32/review-images.json) contain detailed evidence. 26 build assertions and 1136 independent checks passed. Protected bytes from 568 pre-task engineering/artifact files are verified against the specified Git HEAD. Saved CAD is reopened for single-solid validity, bilateral symmetry, internal contacts, exact zero rejection volumes, 180 warning zero checks, joint lengths, floor ligaments, mass and force equilibrium. Negative controls reject false selection of 180, false approval of 190, folding an invalid-zero candidate and manufacturing release.

## Manufacturing

**BLOCKED** pending the incompatible bearing/reference-axis and depth/channel relationships, actual 01-9011-L/R measurements, actual 02-4352/pivot hardware measurements, matrix physical confirmation, CNC stock/tool/tolerance parameters, final fastener selection and remaining manufacturing freeze gates. No intermediate cabinet prototype is assumed. The correct final backbox architecture cannot be declared under these simultaneous fixed constraints.

CERN-OHL-S-2.0. Preserve LICENSE and NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.
