# Quality-gated phase release

Full dataset source belongs in `dataset/`: source snapshot, curation, builders, schema, tests, quality expectations, prior baselines, review decisions, reports and audit notes. Do not replace this with only exported JSON. `dist/` contains only browser assets and selected data/report exports.

## One phase build command

```
python3 scripts/release_phase.py
```

This runs the release-boundary regression tests, invokes `dataset/scripts/phase_check.py --build --release` (which rebuilds and runs dataset tests), and requires a newly generated PASS report matching the current graph hash, expectations/review-dispositions/gap-ledger hashes and phase version. Hard failures, unresolved review findings, stale ledgers and incomplete gap review block the command. Runtime assets are copied only after the gate succeeds. AI-assisted review and documented omissions do not certify completeness or historical truth.

## Publication

Use the Sites source helper for this existing owner-private Site, retaining `.openai/hosting.json`. Pass the phase build as its ordered command:

```
commands: [["python3", "scripts/release_phase.py"]]
```

The helper must finish this command successfully before committing, pushing and packaging. Then publish the returned exact commit and archive through the native private deployment tool. Do not bypass a failed command with a packaging-only run. Preserve the private audience. Publication also requires the independent source review for the phase; a machine PASS alone is not an audit.
