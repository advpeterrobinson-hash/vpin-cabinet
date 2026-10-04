"""Evidence-linked V34.2 report. CERN-OHL-S-2.0."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/backbox-v342'
def read(n):return json.loads((O/(n+'.json')).read_text())
g=read('geometry-validation');i=read('independent-validation');m=read('mass-counts');r=read('manufacturing-register');b=read('browser-validation');space=i['space']
s=f'''# V34.2 — simplified backbox and glazing interface

HEAD BEFORE: `8d951bc37a38d5e3820cbde93700f1161ff32fb1`

HEAD AFTER: the commit containing this report (`git log -1 --format=%H -- docs/BACKBOX_HARDENING_V342.md`).

**Design candidate only. Full-sheet CNC release BLOCKED. Physical hardware/material/structural qualification is not implied by collision checks.**

[30 native CAD views](index.html) · [Offline viewer](../viewer-v32/index.html) · [Native candidate](candidate.FCStd) · [Manufacturing register](manufacturing-register.json) · [EN BOM](manufacturing-bom.md) · [PT-BR BOM](manufacturing-bom.pt-BR.md)

## Tukkari-first and source authority

The [public assembly guide](https://www.tukkari.com/advisor/assembly-guide-widebody-vpin-cabinet-premium-flat-pack) documents a single monitor plate, combined lower display/speaker panel and ordinary side/rear plastic playfield-glass channels. The [Ultra-Widebody public product page](https://www.tukkari.com/p/ultra-widebody-virtual-pinball-cabinet-vpin-premium-flat-pack-kit) specifies3mm clear acrylic, routed channels and120mm fan interfaces. Those functional architectures are the starting point. No proprietary CAD/drawing/assets were imported.

Five explicit adaptations are recorded in [tukkari-first-audit.json](tukkari-first-audit.json): owner-mandated top-captured plate replaces the public bracket arrangement; one-face plywood replaces bent-metal DMD construction; front-removable acrylic retains one strip; lower fan stations fit our existing doors; fixed side channels end before the folding rear U to avoid sweep interference. No new carrier, shelf, duct, depth shoe or custom clamp.

[Official TCL NZ specification](https://tclelectronics.co.nz/downloads/brochures/32S5K_Product_Specification_NZ.pdf):715×422×75mm without stand,3.15kg,VESA100×100,M4 screw family. Official indexed PDF text was inspected; direct retrieval timed out. Manufacturer M4×10 reference does not establish the cabinet bolt length. Actual purchased/local variant, VESA offset/boss plane, active image and connector locations are **unmeasured**. See [sources.json](sources.json).

## Monitor

- One18mm plate; front plane **Y1209**, rearY1227. Plate remains permanently captured by4mm side guides, two12mm stops and the top. Top joint unchanged: glue plus4 direct screws; no Kreg dimensions invented.
- Four PRIMARY VESA100 slots. Reference5mm clearance +30mm movement =35mm total slot length. **±15mm** body movement passes at LOW/NOMINAL/HIGH. Final slot width, washers and drilling are NULL/HOLD. VESA75 removed from minimum plate.
- Two-region TV geometry: thin main/VESA body plus a full-width lower125mm-high thick region. This is an explicit sensitivity construction, not a traced TCL rear drawing.
- TCL-like75mm lower body /65mm boss depth and generic80/70 both pass with12mm spacers. Selected front planesY1132 andY1127; maxrearY1207 leaves2mm to plate. All0/3/6/9/12mm stacks are evaluated in [geometry-validation.json](geometry-validation.json).
- **80mm body /55mm boss case FAILS**, including12mm spacers: lower body intersects plate. Do not claim universal thick-TV compatibility or purchased-TCL fit. Final actual-TCL fit remains HOLD.
- Reference connector reserve100×80×60mm passes through the existing400×100mm plate opening; actual connector positions/straight insertion remain hardware-dependent.
- Monitor front insertion/removal passes at HIGH+15mm before moving to selected height. Acrylic/strip removed; rear VESA screws accessible; plate and top stay fixed. No wooden depth mechanism.

## Acrylic front

3mm reference selected, compared with4mm.752×459mm nominal sheet, final cut/thickness NULL. Four-edge simply-supported self-weight screen at horizontal fold (E=3GPa, density1180kg/m³, ν0.35) gives **{i['acrylic_screen'][0]['selfweight_horizontal_deflection_mm']:.3f}mm for3mm** versus **{i['acrylic_screen'][1]['selfweight_horizontal_deflection_mm']:.3f}mm for4mm**. This supports a provisional3mm choice under a2mm cosmetic screen, not flatness/creep certification. Actual acrylic/liner, temperature and handling qualification remain pending.

Two padded side rebates, padded bottom U and **one12mm upper strip with2 screws**. Strip removal → lift1mm → tilt10° forward → lift6mm → remove front. Six-axis translational and small rotational escape tests meet modeled stops; all retaining parts fold with the acrylic. No gravity/friction-only retention; no shell-top removal.

Paint/mask rear face. The provisional **687×356mm clear window** remains within an assumed697×392mm active image throughout±15mm travel. This **crops approximately36mm of image height**; fixed masks cannot simultaneously expose the full image and hide everything through30mm adjustment. Final paint aperture is NULL and should follow actual alignment/image preference. The model does not claim that697×392 is a measured TCL active area. No wooden display bezel.

## Ventilation, shelves and routing

Two lowerØ116 reference openings directly in existing12mm doors, atX155/445,Z738;105mm mounting square. Default passive commodity grilles; optional120×120×25mm intake fans. Upper2exhausts/fan-blank option unchanged. Maximum2 intake+2 exhaust. F66×8 passive fixings are replaced by F67×8 in active mode; never double-count. H28 identifies the optional intake fans (H18 remains the pre-existing leg family). Actual grill finger protection, hole size/stack and thermal adequacy remain pending.

Both door sweeps0–100° pass for passive/active occupied envelopes; upright-lock access preserved. Fan wiring is user-routed and needs physical full-sweep qualification; no universal loop anchors are asserted.

Retired wood: M058×2 filter frames; M059×2 face pieces; M060×2 tops; M061×4 side returns. No current universal backbox wood shelf existed, so shelves/supports remain0; **S1/S2/S3 and their main-cabinet supports unchanged**. Removed projected fan strain-relief and loop reserves plus obsolete toy-zone display references; side space remains free for user mounting. No actual backbox zip-tie grooves/hooks were present or added. Essential monitor, DMD/speaker and common floor/shelf harness passages retained. Retired identifiers are listed below and in native delta.

## DMD / speaker space

One18mm panel unchanged, DMD occupied envelope unchanged, direct speaker mounting retained. Reference rear speaker depth **60→90mm**, a30mm gain. Actual rear frame contacts at93.1mm;90mm leaves **{space['speaker_to_frame_mm']:.1f}mm**. Fan lateral clearance is17mm for the modeledØ130 speakers. Actual basket, magnet, terminals and screw pattern remain PURCHASE_BEFORE_FINAL_CUT.

Plate rear to upper-fan front: **58.1mm**; to closed door inside: **83.1mm**. Conservative common interior domain minus modeled occupied B-reps: prior **{space['before_free_litre']:.3f}L**, new passive **{space['after_passive_free_litre']:.3f}L**, active **{space['after_active_free_litre']:.3f}L**. The difference includes the smaller TCL-like body and moved plate, not only retired wood. Deleted baffle/frame wood itself occupied **{m['removed_backbox_wood_volume_litre']:.3f}L**. This is geometric free volume, not qualified hand/cable space. No shelves added to fill it.

## Main playfield glass / backbox-base interface

**5mm TEMPERED glass**, reference575×1142mm; final ordering size NULL until actual channels, liner, thermal/service tolerances and lockdown selected. Side channels and glass plane are derived from the accepted B-rep: **{g['glass_angle_derived_deg']:.9f}°**, matching the current playfield slope as a result, not an input assumption.

Left/right lined channels retain their1100mm continuous profiles. Rear U opens toward the player, supports/captures the rear edge and moves with the backbox. Local rear plane t=1142mm; rear U starts t=1132, leaving a32mm side-edge transition after fixed rails. Extending fixed rails into the rear-U region was rejected because it interferes during WPC fold. This narrow unsupported side-edge transition and corner loads require physical glass/channel qualification.

Front: **lockdown bar only**. The new solid is a containment contact envelope, **not a selected latch/bar or released metal design**. Six-direction rigid glass containment and forward continuous insertion/removal pass. Actual positive lockdown attachment is still HOLD. Rear-channel attachment F68 is formula-dependent on the purchased profile; fastener engagement into the relieved floor must be qualified. The containment test assumes the rear channel is positively attached; it does not validate an unselected fixing.

Rear: local TOP-face angled rebate inBB_Floor, no whole-base tilt and no extra wooden rail. Derived angle above; minimum front residual skin **{i['local_bevel_min_skin_mm']:.3f}mm**. Full bottom bearing footprint unchanged. The relieved nose does not replace the broad floor/shelf load path. Structural strength, R2 corner fit and surface finish need supplier/coupon qualification. Variable-depth one-face tool access is documented; no CNC flip/G-code.

Normal service: release lockdown → slide main glass forward. Normal fold: open rear doors → release/park both locks → close/latch doors → remove MAIN glass and matrix → fold0–90°. Acrylic, monitor and lower panel remain installed. No normal electronics disconnect or cassette removal. Rare hinge service retains its separate prerequisites. Raised-playfield prop is untouched and remains its existing operational HOLD.

## Simplification / materials

|Measure|Before|After|
|---|---:|---:|
|Wood manufacturing pieces|76|66|
|CNC plywood pieces|70|60|
|Solid SW01/SW02 pieces|6|6|
|Canonical wood families|48 (contained ID collision)|45|
|Finished wood mass at650kg/m³|{m['previous_wood_kg']:.6f}kg|{m['wood_kg']:.6f}kg|

V34 reusedM074 for both12mm Underfront_Plate and18mm monitor plate. V34.2 retainsM074 for the protected user module and assignsM078 to BB_MONITOR_PLATE. This corrects an inherited catalog collision; no physical part is added. Four obsolete families are retired, while the correction adds one distinct identifier.

Delta **{m['delta_kg']:.6f}kg**. Density550–750 gives{m['LOW550_kg']:.3f}–{m['HIGH750_kg']:.3f}kg. Acrylic reference{m['acrylic3mm_kg']:.3f}kg and main tempered glass{m['playfield_glass5mm_kg']:.3f}kg are separate. Unknown hardware mass is not zero. Only12/18mm plywood. No new stock family. [Reconstruction](manufacturing-delta.json): maxchanged-member difference **0mm³**; independent reassembly checks every present wood member.

## Validation and limits

- {len(g['checks'])} native checks: valid solids, differential protected geometry, wood nonpenetration, reference monitor/service cases, acrylic retention/removal, fans/locks/speakers, main-glass containment/forward travel, mandatory fold angles plus continuous bounds.
- {len(i['checks'])} independent checks: reconstruction, stock/face policy, protected geometry, plate capture/insertion, rear tools, acrylic screen, continuous doors, preserved floor bearing. Flexible lock tether B-rep serializations differ, but vertices/tessellation/area/volume are identical; no design change.
- Fold continuous proof uses OCC midpoint separation exceeding each part's maximum arc displacement over adaptive intervals; AABB only rejects distant pairs. Candidate-specific proof plus unchanged predecessor evidence; it is not certification of unmodeled hardware.
- {len(b['checks'])} offline browser checks, no network or JavaScript errors; desktop and emulated touch, EN/PT-BR, palettes, native states,66 real manufacturing pieces, all59 manual steps. Physical tablet performance not certified.
-30 native CAD review images. No success claim for rejected80/55 sensitivity case. No physical thermal, structural, glass-edge or electrical qualification claimed.

See [geometry-validation](geometry-validation.json), [independent-validation](independent-validation.json), [browser-validation](browser-validation.json), and [small wood purpose/attachment audit](small-wood-audit.json).

## Retired native identifiers

'''+ '\n'.join('- `'+n+'`' for n in g['retired'])+'''

## Release blockers

Actual monitor/bosses/ports/VESA engagement; acrylic thickness/flatness/liner/mask; fans/grilles; DMD/speakers; main plastic side/rear channels and5mm tempered glass; actual lockdown; plywood/coupon/tool finish; WPC purchased hardware; physical retention/load/thermal qualification. Final fit/drilling fields remain NULL/HOLD. **FULL-SHEET CNC RELEASE BLOCKED.**
'''
(O/'README.md').write_text(s);(R/'docs/BACKBOX_HARDENING_V342.md').write_text(re.sub(r'\]\(([^)]+)\)',lambda m:']('+('.. /'.replace(' ','')+'exports/generated/backbox-v342/'+m[1] if not m[1].startswith(('http','#','../')) else '../exports/generated/viewer-v32/index.html' if m[1]=='../viewer-v32/index.html' else m[1])+')',s))
print('V342_REPORT')
