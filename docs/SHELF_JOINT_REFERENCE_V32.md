# V32 shelf joint and plunger references — 2026-09-29

Owner supplied a shelf video, two images and VirtuaPin product/manual links. Sources and local-file inventory are in [the library](../library/README.md). The YouTube page could not be retrieved; the assessment uses the supplied shelf screenshot and owner explanation, not a claimed viewing of the full video.

## Shelf construction

The first image shows an equipment board across the cabinet, local wood supports and visible fasteners. Hidden joint details, wood grade, fastener sizes, payload and service history cannot be established from it. It supports the owner's intended simple assembly concept, not a load rating.

Continue the current direction: a shelf bears on fixed local supports and is retained by two top-access screws per side. The supports carry downward bearing load into the side structure; their attachment still carries shear and eccentric moment. Top screws restrain lift/slip and maintain clamping, so they are not mechanically irrelevant. Use retained metal threads for repeated service, subject to qualifying their anchorage in the support.

**Assessment:** this is a reasonable architecture to develop for electronics shelves. Long-term adequacy cannot yet be asserted for the actual V32 stack. Required inputs are complete loaded mass and center of gravity, shelf stiffness, measured plywood properties/condition, support geometry, wall attachment, fastener engagement and vibration/handling demand. Four screws alone are not evidence of capacity. Heavy impact-producing devices need their own verified cabinet mounts; do not transfer a light electronics-shelf conclusion to contactors, shakers, the playfield or PC assembly.

## Furniture cam connector in the second image

The image resembles an eccentric cam, connecting dowel and plastic socket furniture fitting; exact manufacturer/model and performance are unverified. Do not identify it as a Hettich product from appearance. Some manufacturer-defined cam systems incorporate anti-loosening features: [Hettich Rastex 25](https://shop.hettich.com/de_EN/Further-products/Connecting-technology/Connecting-fittings-for-cabinet-bodies/Rastex-eccentric-connecting-fitting/Rastex-25-without-rim%2C-bright/p/13116) describes latching/serrated features. That does not qualify the pictured generic fitting for cabinet vibration or establish its load rating.

Keep cams out of the baseline shelf retention for now: the existing top screws already provide simple visible release. A cam alternative would need matched cam/dowel/socket data, compatible board thickness, edge/face machining access and proof of its release path. Large cam pockets must not be copied into the 12 mm shelf without checking residual wood. A horizontal connecting dowel can also constrain removal after the cam is released; it does not automatically preserve the approved shelf route.

## Predrilling and qualification

Owner explicitly wants shop-made holes. The eventual CNC package must locate shelf clearance holes, support receiver pockets/pilots and support-to-wall holes with depth/face information and common datums. Select diameters from the actual fastener, receiver and plywood; a clearance hole and a thread-gripping pilot have different functions. Confirm the shop can perform required edge/second-face operations. No precision marking or drilling should be delegated to the home builder by default.

General fastening reference: [US Forest Products Laboratory Wood Handbook](https://research.fs.usda.gov/fpl/wood-handbook). Do not substitute solid-wood equations or furniture marketing for tests of the actual plywood/insert assembly.

Before rating the shelf: define service/proof loads from measured equipment and dynamics; test a representative support-wall coupon for pullout, shear and splitting; test the loaded shelf for deflection and retention under representative vibration/nudging; repeat removal/refitting and inspect loosening, hole wear, cracking and permanent movement. Acceptance thresholds and test duration remain to be set; no test or lifetime certification is claimed here. Physical testing remains paused.

## VirtuaPin plunger reference

The linked product is the VirtuaPin Digital Plunger Kit v3, not an owner purchase confirmation. The seven-page v3.12 manual was downloaded; installation pages 1–2 were visually inspected and text extracted for all pages. It calls for three 10-32 machine screws and washers for installation, illustrates a separate sensor tube/controller and gives controller orientation/setup guidance. It does not establish a complete dimensioned V32 mounting pattern or the full swept/cable envelope. Treat the plunger, tube, fasteners and connectors as one future fit check; keep the current front cut provisional. Do not replace existing controller choices solely because this reference was supplied.

No geometry changes or new structural passes result from this assessment. Current simple-shelf stationary-scene evidence remains 90 checks; actual raised-playfield/props/harness integration remains open.

Original assessment: CERN-OHL-S-2.0. Preserve LICENSE and NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.
