# Independent audit — Genesis first-product phase (v0.4.0)

**Verdict: PASS for the declared selective Genesis 1–50 scope, with 43 explicitly reviewed connection/coverage omissions and three reviewed metadata expansions.** No unresolved finding or material semantic blocker remains in the reviewed dataset. This is AI-assisted source review, not human scholarly certification.

## What the quality check caught and improved

The previous graph kept Eve and Cain's family separate from Adam's family. We did not invent a bridge: the source supports Adam/Eve as spouses (3:17, 3:20, 4:1) and Eve as Seth's mother by contextual identification (4:1, 4:25). Those two reviewed relationships now connect the family branches.

The checker also exposes real limits instead of hiding them:
- **Melchizedek** is linked to Salem, but the blessing of Abram and gift of a tenth are not yet graph edges.
- **Ephron** is linked to his father, but his role as seller in Abraham's transaction remains a missing connection.
- **Hirah, Ahuzzath, Eliezer, and the Genesis12 Pharaoh** remain without edges because their friendship, household, or episode actions are not yet modeled.
- Some rivers, wells, landmarks and trees have passage references but no selected relationship edges.

These omissions are visible in `reports/phase-quality.md` with individual reasons and source passages. They were not silently repaired with guessed connections. A “PASS” means required checks passed and every review item was adjudicated—not that every biblical person or relation was extracted.

## Source and semantic review

The audit team read all **840 newly added supplied WEB verses in Genesis 26–50**. A separate source reviewer handled 26–36; the lead reviewer handled 37–50 and the integrated gate. Earlier reviews of 1–25 remain in the audit history.

Reviewed all 62 new entity descriptions, expanded summaries, added relation claims, scoped alias rules, and uncertainty records. Two chapter-range curations contained 57 and 45 relation claims; the integrated graph merges evidence for their shared addressed-Jacob relation and adds the two source-reviewed early-family corrections. All 135 previous relation records remain intact, with 103 additional relations overall.

Key safeguards verified:
- Jacob/Israel, Benjamin/Benoni, Joseph/Zaphenath-Paneah and Bethel/Luz aliases are source-supported and scoped. Collective Israel and poetic collective Jacob are not globally assigned to the individual.
- Potiphar and Potiphera are separate; Judah's Shelah is not Arpachshad's Shelah; Tamar's Zerah is not merged with Esau's family name. Joseph-era Pharaoh is separate from Genesis12. Abimelech/Phicol in Isaac's story are not silently equated with earlier namesakes.
- Esau's wife-name discrepancies remain unresolved rather than forcibly harmonized. Shechem person/place and Edom person/land are distinguished.
- The unnamed wrestler is not forcibly equated with God. Dinah is not modeled as married merely because Shechem requests marriage. Joint violent actions are not falsely split into unsupported individual actor/victim assignments.
- Joseph's supposed death, sexual accusations, spy allegations, and planted cup are not asserted as objective events from characters' claims. Jacob's blessing metaphors do not create animal identities or fulfilled-prophecy edges.
- Jacob's adoption-like words about Joseph's sons do not become biological parenthood. Joseph's “father to Pharaoh” wording does not create a biological relationship. Future transport of Joseph's bones is not treated as fulfilled within Genesis.

Source-evidence refinements verified include 34:2 for descriptions referencing the Dinah violation, 46:19 for Joseph's parents, 35:23 for Judah's parents, and 38:24 as the named Tamar antecedent for her twins. No modern geographical, historical, ethnic or political entitlement is inferred.

## Repeatable gate reviewed

Command: `python scripts/phase_check.py --build --release`

The gate rebuilds, runs tests, validates source/structure/spans/attribution, checks a source-anchored major-character and relationship checklist, compares the pinned canonical v0.3 baseline, computes isolates and connected components, and requires an explicit disposition for each review finding. Required major entities, aliases and relationships are hard checks; genuine optional omissions remain visible review findings. Decisions are tied to finding fingerprints and file hashes; stale decisions cannot silently approve changed findings.

The independent expectations were authored from source before checking current graph membership. The checklist is deliberately selective, not an exhaustive gold standard. Connectivity uses actual curated relationships, not shared-verse co-occurrence or invented edges.

Mutation tests include structurally valid missing characters/aliases/edges, valid-text namesake reassignment, source changes, false killing, reversed symmetric sibling claims, lost attribution, disconnected major components, and release with missing review decisions. Tests that initially relied on unrelated integrity failures were strengthened to prove the semantic gate adds protection beyond ordinary JSON/reference validation.

## Integrated verification

- Canonical restored v0.3 graph SHA256: `d50671fc08c891900772c984831460ca4a0002890dce3681ee0cc558e6bdf033`.
- Independently compared all previous mentions, relations and uncertainty records: retained unchanged. Prior IDs remain stable. Reviewed metadata expansions are Bethel's Luz alias, Jacob/Israel's summary/alias and Laban's expanded summary.
- All source passages total **1,533 verses**; selected graph has **190 entities, 2,423 mentions, 238 relations and 38 uncertainty records**.
- Topology: **35 isolated nodes, 44 components**. Every isolated node and eight non-main multi-node components has a specific reviewed omission explanation. No required major character is hidden by those acceptances.
- Final data graph SHA256: `7539ee9f4da24a68ee5cf287bf263cc710031f0f79d225e47a45eb8ce5118cf5`.
- Final release-gate run and test count are recorded below after the last guard update.

## Remaining limits

No quantified precision/recall or expert approval is claimed. Full Genesis verse coverage is not exhaustive annotation coverage. The checker cannot establish semantic truth merely from valid verse IDs or anchor overlap; new phases still require source review. Accepted omission decisions identify useful future curation work, not evidence that those relationships do not exist.

The audit approves data and gate readiness for the authorized private preview. It does not certify UI behavior or deployment success, and does not authorize changes to the live GitHub application. The private Site's Quality page should keep hard passes, reviewed omissions, and unresolved findings visibly distinct.

## Final release verification

Independently reran the settled `--build --release` command: **23 tests passed; release gate PASS; zero hard errors; zero unresolved reviews; 46 explicit reviewed decisions**. The command now overwrites any previous PASS with a fail-closed in-progress/failure report before building, so an early failed build or parse cannot leave a stale successful artifact. A dedicated regression test verifies this behavior.

- Expectations SHA256: `6bfb705279d67c71fecc36ee3f122de812ddf50f0185f801bd4f4b154a6b7fe9`.
- Review decisions SHA256: `87fb3e9568b6f6b682d83f97a219b43d5be33e63a38a01e09758a5b6bde5805d`.
- Required active checklist: 97 entries (43 identity/alias expectations and 54 selected relationship expectations).
- Final known-scope guards additionally cover collective Israel48:20, poetic Jacob49:7, Judah-line Shelah, Tamar-line Zerah, and the Genesis12 Pharaoh outside its phase.

**Approved as ready for the authorized private-preview data update, with the reviewed limitations displayed.** UI/deployment verification remains the preview owner's separate responsibility.
