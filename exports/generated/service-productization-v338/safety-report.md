# V33.8 secondary safety straps — studied, not promoted

**Decision: NONE.** Two removable straps were studied; zero straps, anchors or holes are added to CURRENT. No strap carries normal service load. Independent secondary restraint has **not** been validated. The evidence checks passing means that the rejection/hold findings are reproducible, not that a safe strap system was approved.

The exact V33.7 native model contains the rear wooden dowel/cradles and closed front landings, but no modeled positive 50° primary prop/support. The current manual requires controlled support and warns against working beneath an unsupported playfield. Historical prop architectures are not current geometry. The normal support, its attachment/load path, independent-support proof and credible failure mode must be defined before a redundant restraint can be qualified. This study does not redesign that missing primary interface.

## Native route screen

The search contains 42 left/right cases: seven moving underside locations, three fixed anchor zones and two sides. These are point/route studies, **not drilling coordinates**. A 12 mm moving-anchor stand-off and R3 diagnostic route are explicit provisional display envelopes. No purchased eye, webbing thickness, buckle, mounting plate or fastener capacity is implied.

| Left diagnostic route | Length at 50° →49° | Finding |
|---|---:|---|
| Moving X78/Y300; fixed X32/Y300/Z100 |883.703 →872.375 mm|Wrong sign: slack increases as playfield closes. Also crosses SSF_Exciter 1L by 59.110 mm.|
| Moving X78/Y300; fixed X32/Y1100/Z550 |757.295 →758.870 mm|Correct closure-arrest sign, but tension line crosses 154.862 mm of M025 and 392.871 mm of the display envelope. Rejected.|
| Moving X78/Y1060; fixed X32/Y1100/Z420 |78.819 →78.950 mm|Clear centerline at 50°, but only 7.244 mm/rad effective lever at that pose. Anchor construction/rating and rear capture unqualified. Held.|
| Moving X78/Y1060; fixed X32/Y300/Z100 |845.493 →845.907 mm|Correct sign, but line crosses T3 by 20.046 mm. Rejected.|

The rear-high route slackens with further opening, so it cannot also be described as an overopening stop. A front-low strap has the opposite behavior. Neither two straps nor a high cargo capacity makes those directions interchangeable.

All four featured diagnostic endpoint spheres clear the sampled existing moving/fixed geometry at 51 opening poses (0–50°, 1° steps) and 13 lift poses (0–48 mm, 4 mm steps). That small endpoint screen does not validate the intervening route, the full fitting, mounting bores or a stowed strap. The native centerline intersection test rejects the routes even where the endpoints are clear. Both sides are included in the 42-case route search; endpoint sensitivity uses the left candidate only.

## Full single-strap load sensitivity

Native B-rep volumes and mass centers feed the existing 10/12/15 kg display scenarios. Total moving mass spans 16.419–22.604 kg; the 12 kg display nominal case is 18.879 kg. Actual saddle-strap, adapter and receiver masses remain unknown with visible planning allowances. Every independently surviving strap is evaluated for the **whole** moving assembly, never half.

For an illustrative 5 mm slack and 5 mm total arrest extension:

| Route | First taut | Conditional stop | Energy at 22.604 kg | Average tension from energy | Ideal linear-spring peak illustration |
|---|---:|---:|---:|---:|---:|
| Rear-high, already rejected for collision |46.812°|43.580°|8.799 J|1,760 N|3,520 N|
| Rear-tail / rear-low, held |27.608°|13.304°|59.908 J|11,982 N|23,963 N|

The report includes 1/5/10/20/40 mm slack and 1/5/10/20 mm extension sensitivity, with nine moving-mass cases. Energy is `sum(m g (z 50 − zstop))`; average demand is energy/extension. The linear-spring illustration is twice that value. It is **not a proven upper bound or allowable textile load**. Actual peak force needs measured stiffness, energy absorption, damping, anchor compliance and physical drop qualification. Some slack/extension cases do not take up before the normal PLAY pose at all.

The rigid-pivot calculation also cannot certify rear-dowel capture. An asymmetric one-strap arrest can twist/lift the playfield from its open cradles. Two attachments to the same unqualified plywood are not automatically independent. No acceptable wood anchor pull-out/shear capacity or single-restraint test has been established.

## Rated commodity evidence

Cargo tie-down ratings are insufficient authority here. SpanSet’s manufacturer instructions prohibit using its lashing equipment to stop movement; a generic ratchet/cam-buckle strap is therefore not accepted on cargo capacity alone. [SpanSet operating instructions, English page 2](https://www.spanset.com/uploads/default/PIMTree/ins-lashing-id-en-ssid.pdf).

A real dropped-object product category exists: Ergodyne Squids 3149 is a structure-attached tool tether with 36 kg maximum working capacity, fixed 1930 mm length and non-shock-absorbing construction. Its length exceeds the maximum 884 mm direct path in this bounded search, so it would not arrest the studied closure. Shortening, knots or a substitute buckle are not assumed permitted. No product is selected, and local Brazilian stock is not asserted. [Manufacturer product information](https://www.ergodyne.com/squids-3149-tool-lanyard-xl-locking-carabiner-swivel-carabiner-80lbs.html), [tool-lanyard certificate](https://www.ergodyne.com/sites/default/files/2025-06/squids-3149-ansi-isea-121-2023-certificate-of-compliance.pdf).

This does not claim that no suitable product or alternative geometry exists. A short rated restraint plus qualified anchors, primary support and rear capture would require a new targeted study. Proprietary reference geometry was not copied; vendor documents are linked only.

## Stow, wiring and protected motion

No internal stow feature is selected. No straps or anchors enter the mandatory hardware BOM. A future qualified removable pair should be detached and stored outside the cabinet before PLAY, lowering or complete removal unless a separate stowed-motion proof is provided. Merely dropping loose straps into the cabinet is not an accepted stow strategy.

CURRENT 0–50° controlled opening and 48 mm lift geometry are unchanged byte-for-byte at the source. They remain geometric clearance results, not evidence that an unsupported 50° pose is safe. The moving-harness route is validated for controlled service only; dynamic arrest, anchor distortion and motion beyond 50° remain unqualified. No wiring tautness guarantee is invented for the rejected routes.

## Reproducible evidence

- [Configuration](../../../config/safety_straps_v338.json) and [native study generator](../../../tools/safety_straps_v338_study.py).
- [Eight evidence checks and decision](safety-validation.json).
- [42-case native route screen](safety-route-search.json).
- [Diagnostic endpoint motion screen](safety-endpoint-motion.json).
- [Mass/energy sensitivity](safety-load-screen.json).
- [Source links and status](safety-sources.json); [local input hashes](safety-source-hashes.json).
- [Isolated native CAD](safety-study.FCStd); views 09–11 are explicitly rejected/held candidates.

**Manufacturing remains blocked.** No safety restraint, primary service support or CNC hole is released by this study.
