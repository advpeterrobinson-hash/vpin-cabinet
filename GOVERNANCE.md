# Project Governance

## Project model

Virtual Pinball Cabinet is an open-source hardware project maintained in public through GitHub.

The maintainer is responsible for accepting changes into the official project, protecting the engineering baseline, and deciding when a design state is ready for prototype, CNC release, or tagged release.

Contributors are encouraged to propose alternatives, measurements, tests, fixes, fabrication experience, and complete subsystems.

## Decision making

Engineering decisions are made primarily from:

1. safety;
2. manufacturability;
3. reproducibility;
4. structural/mechanical evidence;
5. serviceability;
6. compatibility with the project's flat-pack goals;
7. simplicity and part-count reduction where strength is not compromised.

Major decisions should be recorded in project documentation or issue/PR discussion so later contributors can understand why a geometry or constraint exists.

## Maintainer discretion

Acceptance of a contribution is not guaranteed solely because it is functional. The official project may choose a different approach when it is safer, simpler, easier to manufacture, more reusable, or better supported by measurements.

Forks and alternative implementations are permitted under `LICENSE`, subject to the reciprocal and Notice obligations.

## No proprietary fork requirement

Commercial participation is welcome. Companies and individuals may sell products and services based on the project.

If Covered Source or Products are conveyed, the reciprocal obligations of CERN-OHL-S-2.0 apply. Improvements cannot be converted into a closed proprietary derivative merely because the implementation is commercial.

## Contributions

Inbound contributions use the same CERN-OHL-S-2.0 licence as the project. See `CONTRIBUTING.md`.

The project does not currently require copyright assignment or a contributor licence agreement.


## Mandatory STANDARD-PARTS-FIRST — owner V35

For physical interfaces use this priority: (1) commercial standard pinball part; (2) Tukkari-style established functional architecture; (3) conventional woodworking; (4) commodity hardware; (5) simple CNC custom part; (6) custom mechanism only as a last resort. This rule takes precedence over Tukkari-first when a commercial interface exists. Tukkari-first otherwise remains mandatory. Independently dimension geometry; never import proprietary/non-licensed manufacturing files.

Before a custom substitute record: **STANDARD COMMERCIAL PART EXISTS; PART/FAMILY; PUBLIC SOURCE; STANDARD INTERFACE; OUR GEOMETRIC CONFLICT; WHY STANDARD PART CANNOT BE USED (measured evidence); MINIMUM CUSTOM DEVIATION**. Modularity, universality, future-proofing, adjustability or cleaner CAD do not justify complexity.

V35 owner target is exactly628.65mm outside / nominal592.65mm inside, not630mm or25in. Preserve1308.10mm length unless a documented hard commercial incompatibility requires owner review. Backbox780×723.9mm and local internal geometry stay fixed; use a centerline assembly placement. High display parallel to glass is mandatory; no deliberately sunken screen. Main glass primary candidate603.25×1092.20×4.7625mm; local5mm is conditional on purchased channel fit. Final hardware/drilling, actual stock/coupon and CNC release remain held. V35 is not CURRENT until all promotion gates pass; read config/current_v32.json for active authority. Raised service prop is outside V35 scope.

## V35.1 structure-first refinement

No piece-count target. Preserve useful load distribution, bearing, dry-fit and service parts even when another cabinet has fewer pieces. Standard commercial widebody lockdown/receiver is mandatory; siderails are optional. Main crossmembers, three shelves, M006, SW01/SW02 and wooden pivot architecture are protected. Purchased dimensions and physical qualification are separate from architectural promotion. Consult CURRENT manifest; study artifacts do not promote themselves. Actual hardware, stock/coupon and CNC release remain held.
