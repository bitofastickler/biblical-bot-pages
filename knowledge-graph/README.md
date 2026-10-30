# Bible graph integration

This is a private, repository-ready integration of the Genesis v0.5 source. See [integration guide](../docs/knowledge-graph.md) and [licensing status](LICENSING.md). The historical Site notes below describe the source release, not publication of this integration. The original hosting identity is deliberately absent.

# Genesis constellation pilot
Private standalone static preview. Does not modify the upstream application or pilot source data.

Serve `dist` with the Sites preview workflow. No dependencies, external CDN, or runtime service APIs. Source data copied intact from Bible graph v0.2.0.

## Verification
- JavaScript syntax: node --check dist/app.js passed.
- CUA Chrome desktop: data load, canvas node selection, drag orbit, zoom and reset, search, namesake separation, entity selection, type-filter empty state, inline evidence, verse navigation, dialog open/close verified.
- 390px embedded responsive viewport: visual layout and search/list entity selection verified. Fixed mobile flex collapse found during QA. This is responsive browser QA, not a physical Android-device test. Touch pinch code implemented but not device-tested.
- Source copy hashes and all relationship/description evidence references validated.
- Browser extension metadata warnings observed; no application error shown.

Spatial coordinates are generated for exploration, not geography or chronology. The graph is selective and not expert-certified. See dist/provenance.json.

## v0.3 update — 2026-10-29
Expanded selective coverage to Genesis 1–25: 128 entities, 135 relationships, 1,108 explicit mentions and 693 source verses. Data copied only after independent AI-assisted audit PASS (`/workspace/shared/bible-graph/AUDIT-v0.3.md`); not scholarly certification. Graph SHA256: d50671fc08c891900772c984831460ca4a0002890dce3681ee0cc558e6bdf033.

Added data-driven totals, chapter-scope filtering, alias labels and focus-connections view with a centered 3D neighborhood. Fixed crowded labels with collision suppression. Evidence/mention distinction and speech qualifiers preserved.

CUA QA: 128/135 loaded; chapter range filter; reset; focus; keyboard orbit/zoom; list selection; Abram/Abraham Gen17:5 dual highlight; next passage; Sarai alias lookup; attributed half-sibling note; modal open/close. At 390px, scope/focus/search and Hagar selection were verified visually. Physical Android/pinch remains untested. Full data-copy identity, evidence references, mention offsets and JS syntax passed.

## v0.4 — Genesis 1–50 and quality-gated releases
190 selected entities, 238 curated relationships, 2,423 explicit mentions and all 1,533 Genesis source verses. Coverage is selective, not exhaustive. Independent AI-assisted source audit: `dataset/AUDIT-v0.4.md`.

Full dataset builder, schema, curation, source snapshot, tests, expectations, baselines, review dispositions and audit notes are now durably stored under `dataset/` in this Site source repository. Rebuild/publish through the mandatory `python3 scripts/release_phase.py` command; see `RELEASE.md`.

Quality report exposes 0 hard errors / 0 unresolved findings, 46 reviewed findings including 43 accepted coverage omissions, 35 isolated nodes and 44 components. Isolation remains a review signal, never a reason to fabricate links. 23 dataset tests and 9 Site release-boundary tests pass. Report hashes bind current graph, expectations and review dispositions.

Browser QA verified quality report counts/decision distinctions, checklist-to-entity links, isolates table, Joseph focused 3D graph, chapter ranges, Genesis50 last-verse boundary/highlighting, previous-verse navigation, and Israel alias resolving Jacob. Responsive 390px quality layout verified; physical Android and pinch remain untested.

## v0.5 — source-backed gap resolution
The 43 documented v0.4 coverage gaps were individually reviewed and resolved with meaningful source-supported additions, recorded in `dataset/quality/gap-resolution-ledger.json` and `dataset/AUDIT-v0.5.md`. The selected graph now has 193 entities, 293 relationships and 2,435 mentions; source scope remains Genesis 1–50 / 1,533 verses. No isolated nodes remain and the selected graph is connected. None of these metrics imply exhaustive coverage.

The Quality page shows all 43 original findings, added relationships, attribution/notes, and exact source-passage links. The release wrapper additionally verifies the current ledger hash and complete-review state. Tests: 31 dataset and 11 release-boundary tests passed. Browser QA: ledger count/expansion and source link; Galeed/Jegar Sahadutha naming notes; focused newly connected graph; desktop and 390px mobile source navigation. Physical Android/pinch untested.
