# Public documentation audit — V35.1

Audit performed before editing the public entry points. Main baseline: `2eed36e4ff6e0871edc4d7d845288c5a629fd8b9`. Engineering evidence: [`aa3043cd172ed2bf0f05e0ef5ddcf1cbe9b53656`](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/aa3043cd172ed2bf0f05e0ef5ddcf1cbe9b53656/docs/STANDARD_WIDEBODY_V351.md) on `feat/v351-cncaudit-qn90f`.

| Location before correction | Contradiction | Documentary resolution |
|---|---|---|
| main README.md and README.pt-BR.md | V32 called current; 600 mm body / 564 mm interior; links to V32 gallery | Identify V35.1 as current engineering review, 628.65 / 592.65 mm; retain V32 as history |
| main README.md and README.pt-BR.md | Captive props described as current mechanism | Do not prescribe an unqualified support; V35.1 primary raised-playfield support remains HOLD |
| Engineering-branch README.md | Opening says CURRENT V35.1, later headings say current V32; active design still lists 600 mm, custom lockdown and sliding CPU shelf | Main entry points link directly to pinned V35.1 report/package rather than treating the mixed branch README as authority |
| Engineering-branch docs/RENDERS.md and docs/pt-BR/RENDERS.md | V35.1, V34, V33.8 and V32 all called current | Provide bilingual main gallery pages with a single current V35.1 entry and explicitly historical V32 links |
| main AGENTS.md | 580 mm, LG C5, mandatory gas struts, PC drawer and play-isolated wheels | Add explicit current-review precedence; preserve old baseline instructions as historical evidence |
| main docs/FUTURE_PROOFING.md, docs/requirements.md, docs/DESIGN_DECISIONS.md and docs/CNC_FLATPACK_PHILOSOPHY.md | Older width studies, gas struts and drawer references read as active requirements | Mark superseded architecture context; general safety/flat-pack principles remain applicable |
| V35.1 report: passing motion checks vs QN90F purchase selection | Modeled reference checks could be mistaken for exact QN90F validation | Preserve exact-envelope PLAY / 0–50° / 48 mm lift-out rerun requirement; purchase selection is not validation |

## Scope and precedence

This correction targets `main` with documentation only. Engineering-branch README/gallery contradictions remain recorded above; their contents are not imported or rewritten by this PR. The pinned V35.1 technical report and generated package provide revision-specific evidence. Existing V32 and earlier artifacts remain historical, including their original validation results; those results do not transfer to V35.1.

No geometry, parameters, BOM, CAD, generated views or manufacturing files are changed. No engineering branch is merged. V35.1 identifies the current review, not a CNC-approved product. CERN-OHL-S-2.0, notices and contribution rules remain unchanged.

## Gates preserved

Exact Samsung QN43QN90FAGXZD envelope and service-motion/interference validation; primary raised-playfield support; receiver strategy/fit where it controls machining; measured side-channel profile and slot coupon; plywood lot/tolerance coupon; provider/tooling and fit regeneration; remaining permanent hardware/control interfaces and attachment methods; physical load, nudge, glass-edge and thermal qualification. Full-sheet CNC release remains **BLOCKED**.

Lockdown-bar and rear-channel screw locations are dry-fit interfaces with protected envelopes, not full-sheet CNC gates in themselves. F06 reinforcement is required but its jig/screw qualification follows shell dry fit; final 5 mm glass cutting follows cabinet/channel dry fit. Do not broaden these into unnecessary pre-CNC purchasing gates.
