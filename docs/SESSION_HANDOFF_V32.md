# Session handoff — 2026-09-29

## Resume here

Worktree: `/home/peter/Projetos/vpin-cabinet/.work/worktrees/cabinet-v32`
Branch: `feat/cabinet-review-v32`. Read `AGENTS.md`, `docs/RENDERS.md`, `docs/FRONT_PANEL_REVIEW_V32.md`, `docs/SIDE_PANEL_REVIEW_V32.md` and `docs/PANEL_CLOSURE_V32.md` first.

Owner wants front → sides → rear → bottom, settling shared interfaces to avoid redesign. Continue side hardware/service/load interfaces next; side machining is not frozen. Latest request also records possible custom reward coins and asks for this handoff. “Push it further” was treated as advancing the design; no remote push or PR merge was performed in this session.

Find the commit containing this handoff with `git log -1 --oneline -- docs/SESSION_HANDOFF_V32.md`. Previous HEAD: `8249566` (outward coin-door study). Before this session the branch was seven commits ahead of the locally recorded origin ref `0398d16857e66e415805b7154b0df7e37e7964a6`; remote was not freshly fetched. Earlier local commits: `78faaa6` front review; `ba72c7f` parallel-playfield lighting render; `7bb2645` Donny controller; `14f2d60` speaker rings/optional undercabinet; `77de8bb` lighting reference; `acdec21` interface planning.

## Protect owner state

Do not work in or reset the original checkout. It remains on `feat/active-build-cleanup-v25`, one ahead of its recorded origin, with modified `cad/master/vpin-master.FCStd` and deleted `cad/master/vpin-master.20260914-181346.FCBak`. Verified master SHA256: `98be2307dbe570d8719f385cc0062af56b0cecf85f4b97d2e4f9c340d908c9e3`. Keep deletion intact.

Retain local backup `backup/astra-v25-ff0977a` and stash `owner-state-before-v25-reconcile` (still listed). Earlier V25 reconciliation is historical; do not restart the rebase from the old conversation. Do not force push. Do not touch the separate github-landing worktree or reference assets.

## Selected direction and explicit assumptions

- Body 600 mm, nominal plywood 18 mm; V32 source contains 45 valid solids. Source: `exports/generated/cabinet-v32/build_v32.py`; saved `vpin-central-v32.FCStd` hash `ff973219bdc8bee6707bd29f6a44da74c895cbcbea9e0b1790d8e7723b9aa038`.
- Playfield parallel to glass; custom front lockdown. Cleveland LED matrix panels, Donny control, owner installs; speaker rings included and undercabinet optional. Six nominal 79.375 mm square panels form a 476.25 mm row; vendor approximate overall dimension differs, so fit remains open. The extra 15° LED angle is a render assumption, not final approval. See lighting intent and isolated lighting study.
- Default illuminated coin door with return-switch credits, opening outward. Optional two working mechanisms and compact removable collection tray. Custom reward coins are optional intent; no token dimensions or compatible acceptor selected. Validate token/acceptor pair before the custom order.
- Door study assumes left hinge and 110° outward travel. Component boxes are candidate reservations, not supplier dimensions. Retire the obsolete full-door 140 mm inward prism and its supposed collisions; do not move S1/display/audio because of it.
- Three proposed left front controls X90/Z310,260,210; plunger X520/Z280 and launch X520/Z210. Button function labels remain proposed. Nominal bores are not selected hardware; plunger remains uncut.
- V32 low PCBase/no-drawer architecture conflicts with the session-supplied instruction for a rear full-extension PC drawer. **BLOCKED_OWNER_DECISION** before rear architecture closure; do not silently choose or remodel it.
- Captured-shell joinery is a separate proposal, not adopted source geometry. Leg brackets, glass/lockdown receiver, captive props/load proof, SSF, actual coin/button/plunger hardware remain unresolved. Manufacturing remains blocked.

## Evidence and commands

Previous completed front validation: 20 layout checks +54 saved coin-configuration checks; eight negative controls total. Three saved configurations, outward sweep sampled every 1°, tray withdrawal sampled every 5 mm. Actual hardware, continuous sweep and structural performance are not certified. Run `bash tools/run_front_panel_v32.sh` when changing that geometry; the script requires pass sentinels because FreeCADCmd may exit zero after exceptions. It also renders with uv/numpy/matplotlib (cache permissions may require escalation).

This session: `freecadcmd tools/side_panel_v32_entry.py > /tmp/v32-side-review.log 2>&1`, then require `SIDE_REVIEW_PASS`. Result: 25 checks including one drift negative control, zero collisions for explicitly assumed side button bodies/cables. Report: `exports/generated/side-panel-v32/validation.json`. Source FCStd bytes unchanged. No geometry changes were made for reward tokens.

The important new side finding is the 5.3 mm annular button mounting web: 18 minus 7.9375 outside recess minus 4.7625 inside recess. Verify against actual hardware and stock, not a strength claim. Side bores Ø15.875 differ from front nominal Ø25.4. Side positions Y255/310 Z270. Reference pivot Ø12.7 at Y1270/Z508. See side review for limitations.

`make review-v32` belongs to original V32 evidence. Root `make validate` belongs to pre-V32 architecture and has a known immutable historical BOM guard mismatch; do not weaken/rebaseline it to make V32 pass. Generated exports are ignored: add only intended named artifacts with `git add -f`, never backup files. Keep LICENSE/NOTICE with generated distributions.

## Next work

1. Review side button mounting stack and actual selected hardware; keep existing cuts provisional. Define leg-bracket fastener access and front/lockdown/glass datums before final side outlines.
2. Define removable SSF/feedback mounts and display hinge/captive-prop zones with load and service paths; check both sides, shelf supports and wire clearance. Existing collision audit does not include missing hardware.
3. Resolve PC architecture discrepancy before rear closure. Preserve compact mains/Ethernet intent; no permanent HDMI/USB bank or integrated wheels.
4. Rear fan/door hardware then floor/subwoofer/intake/optional LED mounts. Four existing auxiliary floor holes have unassigned purpose; justify or propose removal. Do not infer manufacturing approval from renders.
5. Measured stock, tool diameter, relief/clearance, assembly proof, nesting, physical coupon and owner release remain required.

## References and availability

The two owner images show three left buttons, central coin door and right plunger/launch. They inform layout, not dimensions. Paths/hashes are recorded in `config/front_panel_v32.json`; do not import copyrighted artwork into the repository.

Attached Pinscape MHT is under `/tmp/codex-remote-attachments/01a0aadc-6bed-7c53-a20c-435ba360f604/20c89704-177e-4406-972f-3ba59a7f260c/1-The-New-Pinscape-Build-Guide_-A-comprehensive-how-to-guide-to-building-a-virtual-pinball-machine.mht`. Parse with Python email MIME parser, then HTML extraction; do not copy the book into source. Other previously mentioned hardware PDFs were not available. A SUZOHAPP drawing download timed out; no dimensions were adopted from it. Do not claim those PDFs were reviewed or search unrelated personal directories for replacements.

## Continuation — side interface planning

Read `docs/SIDE_INTERFACE_PLAN_V32.md` next. Added saved support-footprint extraction to the read-only side audit: seven mirrored shelf-support/guide/floor-cleat pairs and fourteen inner-face checks. Rerun produced `SIDE_REVIEW_PASS 46 checks; 0 candidate envelope conflicts`; saved source hash remains unchanged. The 25-check count above describes the earlier audit.

Documented shell datums, existing occupied side regions, unmodeled button-stack alternatives (5.3 / 13.2375 / 18 mm remaining wood at nominal stock) and proposed leg/glass/display-prop/feedback load and service paths. No hardware dimensions invented, no new machining or prop coordinates adopted, no structural approval. The 22 mm Y separation from the rear button's candidate radius to T1Guide is only a bounding separation, not tool clearance.

Asked owner for selected side buttons and leg/inner-plate models and the PC architecture decision; no answer had arrived when this continuation was recorded. These remain pending. Next dependent step is actual hardware stack and tool/motion-envelope modeling. Original checkout, reference assets and separate worktrees were not modified. No remote push or merge performed.

## Continuation — owner approved proceeding; guide service screen

Owner said “Aprovado. Prossiga”; continued the side study, without treating this as a selection of PC architecture or actual hardware. New `docs/SIDE_SERVICE_REVIEW_V32.md`, `config/side_service_v32.json` and `tools/side_service_v32_entry.py` screen the 24 guide side-anchor bores against two candidate axial tool cylinders in three explicit removal states. Saved report: `exports/generated/side-panel-v32/service-validation.json`.

`SIDE_SERVICE_PASS 29 audit checks`; 144 tool/state results. Compact Ø16 ×100: six upper-forward anchors blocked by monitor rails as assembled, zero after monitor assembly removal. Larger Ø30 ×150: all 24 blocked until monitor assembly and T1/T2/T3 are removed. These are obstructions discovered, not validation failures to suppress. Two collision controls detect an injected block and clear its translated counterpart. Source FCStd bytes unchanged; no permanent cuts or mounting coordinates changed. Next: actual tool/fastener stack and independently accessible monitor/crossmember release sequence. Leg/prop hardware and PC decision remain pending.

## Continuation — maximum autonomous functional progress

Owner requested maximum functional progress with minimal human input. Advanced from static removed-state assumptions to continuous translation checks, without choosing hardware or silently resolving the PC discrepancy.

Start with `docs/SIDE_MOTION_REVIEW_V32.md` (Portuguese companion available). New `tools/side_motion_v32_entry.py` and `config/side_motion_v32.json` use the original V32 plus the saved coin-upgrade closed study, current configured plunger/front-button envelopes and candidate side-button envelopes. The full-door inward prism and obsolete plunger position are excluded. A union of planar boundary-face extrusions covers continuous straight translations; curved moving shapes are rejected.

Final motion result: **99 checks, 16 routes; 10 clear candidate routes and six required obstructed controls**. Monitor vertical teardown packaging clears; T1/T2/T3 lift through their guides only after monitor removal. Direct shelf rise is obstructed. Alternative routes: S1 rearward +310 mm to Y430 then up 446.9; S2 forward −170 mm to Y430 then up 426.9; S3 forward −320 mm to Y760 then up 366.9. Other shelves stay installed. All three also pass with 560 ×150 ×60 mm candidate payloads above the boards; S1 audio moves with S1. These are occupancy envelopes, not mass ratings.

Three separate saved/reopened service-stage FCStd files each contain 65 valid single solids with permanent identities preserved. They depict the end of the horizontal leg. Candidate payload volumes intentionally enclose equipment and are not BOM parts. Files, hashes and route collisions are in `exports/generated/side-panel-v32/motion-validation.json`. The diagram `04-shelf-service-routes.png` was visually inspected. Sources: `tools/render_side_motion_v32.py`; saved-scene bounds, not a manufacturing drawing.

Run `bash tools/run_side_review_v32.sh` for all side audits (46 +29 +99 checks with mandatory sentinels); `uv run --with matplotlib python tools/render_side_motion_v32.py` for the diagram. The integrated runner passed before the final saved-pose additions; the changed motion stage separately passed all 99 final checks. Source/config/script hashes, saved-pose hashes and document links verified. Original FCStd hash remains `ff973219bdc8bee6707bd29f6a44da74c895cbcbea9e0b1790d8e7723b9aa038`. Do not add generated FreeCAD backups.

Next: detail independent monitor/crossmember retention and shelf release that preserves the proven candidate horizontal-first paths; incorporate actual hardware and harnesses as available. The vertical monitor study is major teardown packaging, not the routine hinged/dual-captive-prop service mode. Glass/lockdown/LEDs, props, hinges, fasteners, grips, loads and physical handling remain unverified. A drawer or adopted joinery requires rerunning affected routes. No permanent panels were changed; no remote push/merge performed.

## Continuation — modeled removable shelf retention

Owner requested continuation. New separate proposal: `docs/SHELF_RETENTION_REVIEW_V32.md` with Portuguese companion, `config/shelf_retention_v32.json`, `tools/shelf_retention_v32_entry.py` and renderer. No permanent source model changed. It reconstructs the installed scene from the verified S1 motion pose and original monitor/crossmembers, rejecting stale hashes.

Shelf supports widen from 18 to 42 mm locally; shelf outlines and elevations stay unchanged. Four nominal Ø5.5 bores per shelf at X48/552 and Y offsets25/100. Candidate Ø5 ×35 shafts, Ø9 ×4 heads, Ø12 ×1 washers and 10 ×10 ×5 square nuts; none are selected SKUs. Twelve underside nut pockets and six provisional 42 ×150 ×3 covers keep nuts captured; 24 cover-fixing positions are modeled, but actual cover screw bodies remain absent. Four Ø20 equipment-access wells per shelf reserve tool space in the 60 mm payload envelope, not large holes in the wood. Side-wall anchorage and loads remain unqualified.

Initial X42/558, Y25/125 layout was rejected: S1 driver hit side-button reservation; S2 driver hit T2 guide. Those failures remain executable controls. Final 12 top access probes and 40 mm screw/washer withdrawal paths pass; all three loaded shelf removal paths still clear with wider supports and retained nuts/covers. A retained bolt blocks 1 mm shelf translation. Nut 45° rotation and 1 mm drop controls hit the pocket/cover as intended. All 24 underside cover-driver probes clear, but actual screws/hand access still unverified. Square pocket cutter relief and physical tolerance remain open.

`bash tools/run_side_review_v32.sh` now runs all four stages and passed **46 +29 +99 +105 checks**. Retention CAD `exports/generated/side-panel-v32/shelf-retention-proposal.FCStd` reopens with 114 valid single solids (including candidate envelopes, not BOM count). Exact shapes and identities compared. Report `retention-validation.json`; schematic `05-shelf-retention.png` was visually inspected. Integrated execution regenerated the three earlier service-pose files and their recorded hashes without geometry changes. Prior evidence inputs were unchanged during the retention stage; original source hash remains `ff973219bdc8bee6707bd29f6a44da74c895cbcbea9e0b1790d8e7723b9aa038`.

Next: qualify real shelf-clamp/cover hardware and support-to-side anchorage, then independent monitor/crossmember retention and dual captive props; no closed loop requiring blocked guide anchors for initial release. Hardware thread/drive profiles, loads, vibration retention, measured stock, corner relief and manufacturing remain blocked. Keep the retention proposal separate from source V32; PC architecture discrepancy remains unresolved. No remote push or merge.
