# V33.6 backbox support study

Native source: `exports/generated/structural-v335/play.FCStd`. The current carriers are Y1240–1258, adapter Y1228–1240, display rear Y1228; historical backbox-service config is 10 mm forward of these accepted B-reps. No existing part is repositioned.

Proposed current change: two 6 × 16 mm R3 through slots per monitor carrier, above the adapter. Minimum outer web 10 mm; between slots 18 mm; net transverse width 38 / 50 mm (76%). Four slots remove 6355.752 mm³ / 0.00413124 kg at 650 kg/m³. The nearest depth-bolt reserve is 25.624 mm away; upper monitor clamp reserve 48.208 mm away. Both carriers remain one solid. Capture lands, M067 and all adjustment/retention interfaces remain exact. This is a geometry screen, not strength certification.

The existing carrier FACE_A faces front (-Y), because the M067 capture is machined from that face. New slots are through-cut from that same face; FACE_B receives no CNC. Minimum corner radius R3 exceeds the supplier R2 limit. A 12 mm-wide / 2 mm-thick flexible-strap threading reserve and 60 ×24 mm rear finger corridor were checked with doors open. Actual tie/strap selection remains optional and user configurable.

Existing open space beside the adapter accepts a generic 50 ×30 mm connector cross-section,65 mm body planning envelope, with 205 mm rear removal sweep. This is not a connector SKU or universal fit claim. Two illustrative flexible 5 mm cable routes include R20 bends and retain 2.5 mm minimum modeled clearance. The selected cable bend requirement and display connector positions remain unknown. Rigid backbox fold of these internal routes passes a continuous OCC separation-bound test over 0–90° plus all 13 requested sample angles. A real service loop must be qualified with selected cables; no electronics disconnection is introduced.

A 180 ×70 mm R12 central adapter service window was constructed and quantified. Existing peripheral clamp reserves clear it by 56.801 mm; outer frame webs are 90 /80 mm. Its rear service corridor works. **NOT PROMOTED:** actual VESA load points are absent, and a centered 100 mm row example leaves only 15 mm to the window before bore/washer allowance. Unknown future hole positions can lie within it. The unchanged replaceable VESA adapter remains current until the selected display supports the opening. Retaining a rectangular perimeter alone does not prove the VESA load path.

No new adjustment slots are justified. Existing vertical ±5 mm, depth choices 0 /16 mm, max-width centering ±1 mm and smaller-display centering ±15 mm remain unchanged. Display retention stays four positive clamps; M067 lower adjusters remain unchanged.

`validation.json` includes 29 checks, true B-rep volume and nearest-hardware distances. `brep/BB_MonitorCarrier*.brep` are the only proposed replacements. `brep/CURRENT_*` preserves references; `HELD_AdapterServiceWindow.brep` is isolated and must never be promoted by a glob.

Manufacturing remains blocked pending actual plywood, coupon, purchased hardware and display-specific adapter qualification. No full-sheet or CAM files are generated.
