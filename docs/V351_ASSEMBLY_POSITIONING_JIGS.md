# V35.1 — Assembly positioning policy for non-CNC hardware

Status: **assembly positioning resolved; no new full-sheet CNC geometry required**.

## T1/T2/T3 guide placement — M015/M016

The six guide pieces already have defined CAD geometry and installed transforms. Their remaining problem is repeatable placement, not guide shape.

V35.1 policy:

1. The CAD installed transforms are the positional authority.
2. Generate a **1:1 locator template / drill jig** from those transforms.
3. Clamp the guide and template to the finished side panel during dry assembly.
4. Use the selected F05 hardware only after its shank/head/engagement are known.
5. No new permanent side-panel hole is released merely to solve positioning.
6. If the final F05 family benefits from shallow locator dimples, those may be added only as a later manufacturing convenience after the screw family is physically qualified; they are not required for flatpack release.

F52/I14 belong to the guide/support-angle assembly. Their final hole/pilot dimensions follow the purchased M5 retention stack and can be drilled in the replaceable guide/angle assembly after purchase. They do not require redesign of the cabinet side.

## Backbox hinge cleats — M062

M062 left/right cleats are already one-side-CNC-ready. Their remaining placement problem is handled by a **CAD-derived 1:1 placement template** referenced from the finished backbox side/floor datums.

No permanent side-panel pilot pattern is required to locate M062.

Workflow:

**assemble backbox dry → place template against datums → clamp M062 → verify fold clearance → drill/install with selected fastener**.

## General rule

A placement problem must not be converted into permanent CNC geometry unless there is a clear repeatability, load-path or access benefit.

Prefer, in order:

1. self-locating CNC geometry already present;
2. CAD-derived disposable/reusable jig;
3. clamp/mark/drill during dry fit;
4. permanent CNC pilot only when the first three are inferior and the final purchased hardware is already frozen.
