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
