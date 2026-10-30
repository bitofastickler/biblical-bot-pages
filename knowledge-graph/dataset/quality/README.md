# Repeatable phase quality gate

Run from the dataset directory, with Python 3.9+ and no network/packages:

```sh
# Read-only check of the current generated data (no semantic edits)
python scripts/phase_check.py
# Rebuild from explicit curation, run every test, then report
python scripts/phase_check.py --build
# Release gate: build + tests + integrity + required source checklist + reviewed warnings
python scripts/phase_check.py --build --release
```

Outputs: `reports/phase-quality.json` (machine-readable) and `.md` (readable). Reports contain current counts, degrees, connected components, source/graph/expectation/baseline/approval hashes, actual findings, decisions and limitations. A prior initial v0.3 run is retained under `reports/v0.3-quality-baseline.*`.

## Acceptance and exit codes

- **Exit 1 / FAIL:** structural integrity failure, missing required major person/alias/relationship, a specifically prohibited source contradiction or namesake assignment, source snapshot change, or untrusted baseline. Cannot be suppressed by a review disposition.
- **Exit 0 / REVIEW_NEEDED:** non-release diagnostic mode completed, but findings need review. This does **not** mean ready to publish.
- **Exit 2 / REVIEW_NEEDED:** `--release` refuses unresolved editorial findings.
- **Exit 0 / PASS:** integrity and required checklist pass, and all current review findings have explicit accepted decisions. Counts of accepted findings remain visible. PASS is not proof of complete or historically true content.
- A builder/test subprocess failure aborts the pipeline with its failure code. It is not a successful quality report.

## Independent expectations, not a self-confirming baseline

`expectations.json` is an independently source-checked editorial checklist, authored separately from graph adjacency. It includes known omissions in the previous dataset, major characters, explicit renaming anchors, parent/spouse relationships, and prohibited shortcuts. Requirements are activated only when all their source anchor verses are in declared coverage. New scopes must add expectations **before** accepting extraction results. Do not regenerate expectations from the candidate, remove failed expectations to get green, or conflate a partial checklist with exhaustive recall.

`required: true` makes missing identity/alias/relationship a blocker; source-mention anchor gaps and evidence differences still require source review. `reviewed_evidence_sets` allow specifically reviewed alternative source supports. Default evidence-anchor overlap is a screening check, not semantic proof. Description evidence and source IDs are validated, but reading the cited clauses remains essential.

The frozen `baselines/v0.4.0.json` is the verified previously released graph, with hash/source provenance in its companion file. It detects removed/reassigned annotations and changed identity/metadata, not correctness by itself. A faulty old edge does not become true because it is preserved. New releases do **not** automatically overwrite their comparison baseline; promotion requires explicit editorial review and a separately versioned baseline with provenance.

## Connectivity and review decisions

Degree counts stored relationship records; neighbor degree counts distinct adjacent entities. Components use undirected adjacency for navigation only. Shared passage mentions are **not** fabricated relationships. An isolated tree, river or place can be a legitimate selective omission. A major character isolated or stranded in a disconnected group is prioritized for review, but no edge is created merely to join components.

`review-dispositions.json` maps exact finding fingerprints to decisions. An accepted decision needs `decision` (`accepted_omission` or `accepted_after_source_review`), a nonblank specific `reason`, a nonblank `reviewer` describing the review method, and valid source verse IDs in `evidence`. Source-specific evidence and reasons are checked by the independent reviewer; existence validation alone cannot judge their quality. Stale/unmatched approvals are flagged. File hash is bound into the report; changed findings require new review. Human scholarly review is not implied by AI review labels.

## Regression/negative testing

Mutation tests keep projections and counts valid where possible so that semantic guards—not incidental corruption—catch removed required characters/aliases/edges, true namesake reassignment and misleading literal-name matches. Other tests cover source changes, dangling evidence, false killing, isolated major characters, invalid approvals and release refusal. Existing tests verify exact offsets, schema, explicit speech attribution and renderer projection.

## Current limitations

This is a selective Genesis graph and a selective source-derived checklist, not a complete Bible extraction benchmark. No precision/recall claim is made. The gate cannot establish theology, historical accuracy, all ambiguous identities, every implicit relationship, or whether a grammatically valid evidence reference really supports every clause. Independent textual review remains a release requirement; new issues should become explicit tests/expectations when appropriate.

## Commissioned 43-gap closure

The v0.5 release also checks the exact43 isolated-node/separate-component findings in the frozen canonical v0.4 quality report, excluding its three metadata reviews. The baseline report hash is pinned alongside the graph hash. `gap-resolution-ledger.json` must account once for every original fingerprint; each resolved item needs a newly added/changed canonical edge that actually links its original target outside the prior component, specific source evidence, and independently approved record hashes. Structural connectivity alone is insufficient.

Tests remove ledger rows, delete supporting edges with valid counts/projections, mutate support under the sameID, substitute unrelated pre-existing edges, tamper the frozen report, and invalidate approval hashes. Missing/deferred/accepted-omission labels cannot masquerade as a finished repair. A residual remains separately counted and blocks the commissioned-completion release; it is not silently converted to resolved.

Old accepted dispositions remain preserved in the frozen report as history, but the current disposition file is empty because every old connection task has a concrete reviewed repair. Empty dispositions do not themselves prove completion: the explicit ledger does.
