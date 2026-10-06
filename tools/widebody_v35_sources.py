"""Public functional-interface evidence, no proprietary files imported."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/widebody-v35'
sources=[
('TUKKARI','https://tukkaricz.s2.cdn-upgates.com/6/669767d6279c87-cabinet-parts-usa-ver-01-2026.pdf','Official2026 sourcing guide links commercial widebody glass, Williams rails, plastic channels, leg brackets, coin door and shooter. Functional architecture only; no third-party CAD copied.'),
('LOCKDOWN','https://www.pinballlife.com/williamsbally-widebody-lockdown-bar-raw.html','A-17996 family,25in inside nominal; supplier lists A-16773-1 compatibility.635mm inside minus628.65mm cabinet leaves6.35mm total before finish/rails. Cross-section, tabs, coating and fit unmeasured.'),
('RECEIVER','https://www.pinballlife.com/williamsbally-lockdown-bar-lever-guide-receiver-assembly-wpcwpc-95.html','A-16773-1 compatible with A-17996. CAD520×42×25 reserve is PROVISIONAL, not published dimensions; actual lever travel/tab geometry and hole pattern held.'),
('SIDERAIL','https://www.pinballlife.com/47-316-williamsbally-wpc-stainless-steel-side-rails-set-of-2.html','A-12359-3 /01-8993-2;47-3/16in overall reference. Full constant-section envelope collides with protected backbox. Candidate studies rear trimming82.2375mm; actual flange termination must be measured before any cut. Not a custom fabricated rail.'),
('GLASS','https://www.pinballlife.com/widebody-tempered-playfield-glass-shippable-2-pack.html','08-7028-1 family; commercial603.25×1092.20×4.7625mm tempered. Local5mm is0.2375mm thicker; profile fit cannot be inferred.'),
('GLASS CHANNEL','https://www.pinballlife.com/playfield-glass-side-rail-plastic-channel.html','03-7135-1;42-3/8in=1076.325mm. Vendor gives length and compatible families, not a machining cross-section. Reference U is an original fit envelope, no custom extrusion or final groove release.'),
('REAR CHANNEL','https://www.pinballlife.com/widebody-playfield-glass-rear-plastic-channel.html','03-8091-2;22-15/16in=582.6125mm. Supported rear edge on existing shelf reference rebate. Mounting method and profile are purchase-dependent.'),
('LEG BRACKETS','https://www.pinballlife.com/williamsbally-leg-bracket.html','01-11400-1 fits cabinet inside corner. Existing SW01 retained because body/block corner stack has not been measured against this bracket. Commercial bracket is preferred to fabricated plate; replacement not proven.'),
('LEGS','https://www.pinballlife.com/sternsega-black-legs-set-of-4.html','Commercial pinball legs per Tukkari source; exact leg length/bolts/bracket geometry remain purchase-dependent. No fabricated leg system.'),
('SHOOTER','https://www.pinballlife.com/stern-ball-shooter-assembly-2021-present.html','500-2604-XX ordinary shooter includes rod/springs/housing; mounting plate535-5027-00 and3 mounting screws separate. Existing location is a reserve; selected pitch/body fit remains HOLD.'),
('COIN DOOR','https://www.pinballlife.com/stern-coin-door-without-wiring-harness.html','Commercial coin door reference linked by Tukkari. Opening recenters; existing reserve is not purchased-door proof.'),
('BACKBOX HINGE','config/wpc_kinematics_v32.json','Validated transverse Y1066.8/Z508 kinematics;01-9011-L/R,02-4352,4322-01139-12B. X pivot placement follows wider sides; unchanged local backbox floor attachment requires physical arm/bushing stack measurement.'),
('42-INCH','https://www.lg.com/content/dam/channel/wcms/jp/catalog/pdf/2025_tv_dimension.pdf','LG OLED42C5 reference932×540×41.1mm without stand; portrait transverse width540. Reference only; actual boss/ports still held.'),
('43-INCH','https://www.samsung.com/ie/tvs/qled-tv/qn93d-43-inch-neo-qled-4k-tizen-os-smart-tv-qe43qn93datxxu/','Samsung43QN93D manufacturer960.8×558.9×26.9mm without stand. Thin43-inch case, not all43-inch TVs.'),
('NARROW TV','https://static-obg.tcl.com/content/dam/brandsite/region/nz/product/tvs/s-series/s5k/40S5K_Product_Specification_NZ.pdf','TCL40S5K892×507×77mm without stand. Width passes; thick body is a negative depth case for this high-plane/base configuration.'),
('LENGTH','https://www.tukkari.com/p/widebody-virtual-pinball-cabinet-vpin-flat-pack-kit','Public51.6in overall length is rounded reference, not reason to change1308.10mm. No hard overall cabinet-length mismatch established; rail rear termination is a separate local conflict.')]
rows=[]
for item,url,evidence in sources:
 rows.append({'item':item,'public_source':url,'evidence':evidence,'purchased':False,'final_drilling_released':False,'fit':'REFERENCE_SCREEN_ONLY_PURCHASE_BEFORE_CNC','standard_commercial_exists':item not in ['LENGTH','TUKKARI'],'source_geometry_imported':False})
(O/'standard-compatibility.json').write_text(json.dumps(rows,indent=2)+'\n')
(R/'config/standard_parts_v35.json').write_text(json.dumps({'version':'V35','status':'REFERENCE_NOT_PURCHASED','interfaces':rows,'release':False},indent=2)+'\n')
lines=['# V35 standard-parts-first public evidence','', 'Public pages reviewed2026-10-05. Descriptions below are original assessments; no proprietary CAD/drawings/files imported. No quoted listing establishes final drilling.','']
for a in rows:lines+=['## '+a['item'],'',a['public_source'],'',a['evidence'],'']
(R/'library/references/v35-standard-parts.md').write_text('\n'.join(lines))
