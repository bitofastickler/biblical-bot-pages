# Bible Graph — Genesis 1–50 foundation

**Version 0.5.0 · selective AI-assisted editorial pilot, not an exhaustive or expert-certified knowledge graph.**

This is a new annotation layer built against the actual WEB corpus from `bitofastickler/biblical-bot-pages/data/web.json`. It does not modify the application, publish a repository, or deploy anything. The full source snapshot is included; only Genesis 1–50 has pilot annotations.

## Contents

- `source/web.json`: exact original corpus bytes, Git blob hash verified.
- `data/verses.json`: all **1,533 verses** of Genesis 1–50, verbatim, with stable passage IDs.
- `data/graph.json`: **193 selected entities, 2,435 explicit scoped mentions, 293 selected relations**, and 40 editorial uncertainty records.
- `data/graph-view.json`: ready-to-consume nodes/links and passage-navigation IDs. Includes assertion context on each link. No layout coordinates are invented.
- `data/provenance.json`: source identity, byte count, SHA256, Git blob SHA1, curation method, scope and counts.
- `curation/entity-descriptions.json`: the original Genesis 1–11 description curation.
- `curation/genesis12-25.json`: new entities, descriptions, aliases, relations, uncertainties and updates to existing summaries. The additional `genesis26-36.json` and `genesis37-50.json` assets extend coverage to all 190 selected entities.
- `schema/graph.schema.json`: JSON Schema draft 2020-12 for graph structure.
- `scripts/build.py`: deterministic generation from inspectable, manually selected curation rules.
- `scripts/validate.py`, `tests/test_integrity.py`: standard-library checks and regression tests.
- `SCHEMA.md`: semantics and renderer rules.

## Run

Python 3.9+; no packages, credentials, API calls or model downloads required.

```sh
python scripts/phase_check.py --build --release
```

The build requires the exact included source snapshot. It refuses a different blob rather than silently shifting offsets or mixing editions. To adopt a new corpus, explicitly re-curate affected mentions and record a new provenance version. IDs are editorial identifiers, not labels or offsets; retain entity IDs across revisions. Mention IDs may change when source spans change.

## Reader-friendly descriptions

Every entity now has a concise one- or two-sentence `description` and nonempty `description_evidence` passage IDs. These are source-grounded editorial summaries, not automatically generated from the graph. They give a useful identity and role even when the pilot contains few edges. Earlier technical cautions remain separately available as `editorial_note`; the navigation export carries all three fields. Namesake distinctions and unresolved readings remain explicit.

Descriptions may summarize cited facts that are not yet modeled as relations. The selected graph remains non-exhaustive: do not mistake the summary for a complete biography or the graph for the sole source of its facts. All descriptions are bounded to Genesis 1–50; later stories, traditional identities, and modern geographic equivalences are not imported.

## What was curated

All 1,533 supplied Genesis verses were read across the initial work and bounded source-reading curation/review passes. Selected personal names, named places, the Eden serpent, Noah’s ship, two trees, and a subset of genealogical referents were assigned explicit verse/chapter scopes. Literal matches are then expanded within those scopes, with reviewed exceptions for namesakes and substrings. This is **not** a general-purpose entity extractor; high counts do not imply exhaustive recall. Every relation is separately selected and carries verse evidence. Assertions mean *the text narrates or a character says this*, not that archaeology, theology, or history independently establishes it.

The pilot preserves separate Cain-line and Seth-line Enoch/Lamech, two Nahors, person/place Haran, and person-or-genealogical versus land Canaan/Cush. Generic “man” and collective “Adam” (5:2) are not automatically the person Adam. The serpent is not equated with Satan. Table of Nations identities are not forcibly resolved to individual people. No modern geography, denominational doctrine, or numerically calibrated confidence is invented.

## Deliberate omissions / limitations

- No annotations beyond Genesis 50, despite inclusion of the full corpus.
- Not every named entity in these fifty chapters is annotated; much of Genesis 10 is omitted.
- No general pronoun, “man”, “woman”, wife, unnamed-person, or group coreference layer. Parent edges can therefore be supported by contextual evidence without both endpoint names appearing in that same verse.
- No complete event ontology, timeline, ages, themes, miracles, doctrines, quotations, bibliographic cross-references or entity embeddings.
- All aliases are local source forms, not globally valid matches. For example, `God` inside possessive phrases identifies the named referent, not a separately resolved Spirit or sons-of-God entity.
- No claim of precision/recall metrics or expert approval. Integrity tests verify references and offsets, not all meanings. Independent AI review is useful but not equivalent to scholarly review.
- The source is the repository’s WEB-labelled snapshot; its entire text has not been compared with a particular official WEB release. Do not claim an exact official edition/date beyond the recorded repository blob.

## Rights and provenance

The World English Bible is public domain; see the [publisher’s notice](https://ebible.org/engwebp/copyright.htm). The WEB name is a trademark; modified text should not be presented as the unchanged WEB. This does not establish that every other file in the user’s repository shares that status. Only the provided WEB corpus is copied here. Repository code/assets are not incorporated.

The owner selected licenses on 2026-10-30: **MIT for code, schema definitions and explanatory documentation; CC BY 4.0 for curated annotations, credited to bitofastickler.** WEB scripture remains public domain. See [license scope and attribution](../LICENSING.md). The original source had no selected annotation license; preserved historical provenance records that earlier status, while the current grant applies to the supplied annotation corpus.

## Suggested next acceptance gate

Have a human subject-matter reviewer approve entity distinctions, relationship semantics and coverage policy before broad expansion. Then expand one explicitly tracked passage range at a time, retain evidence and unresolved readings, and measure extraction accuracy against a separately curated evaluation set. The app can consume the current navigation export without treating the dataset as complete.

## Genesis 12–25 expansion (0.3.0)

Adds 53 entities and 68 relationships, while keeping every earlier entity ID, mention and relation. The 394 added verses are exact source text. Coverage emphasizes Abraham/Sarah, Hagar/Ishmael, Isaac/Rebekah, Esau/Jacob, Lot, selected rulers and burial/travel locations. Wider genealogies, unnamed characters, events, and many explicit occurrences remain uncurated.

- `bg:abram` now displays **Abraham (Abram)**; `bg:sarai` displays **Sarah (Sarai)**. Genesis 17:5 and 17:15 explicitly ground these aliases; curated scopes are in the extension asset. Old IDs are never replaced.
- Mamre person/place are separate. Ham in 14:5, Havilah in 25:18 and the city of Nahor in 24:10 are not automatically linked to earlier namesakes.
- Abraham’s statement that Sarah is his half-sister is stored as attributed speech, not an unqualified genealogy edge. Promised land is a speech-context relationship, not modern title or entitlement.
- No identification of the unnamed Genesis 24 servant with Eliezer, nor forced divine/angel/visitor identity links. Isaac’s binding is narrated; no killed edge is created.
- New `traveled_to` edges record arrival or passage through, not a reconstructed geographic route.

Nine test methods include added alias, namesake, quotation-attribution, no-Isaac-killing and description-evidence regressions. The independent review is recorded in `AUDIT-v0.3.md`; it is AI-assisted, not human scholarly certification.

## Whole-Genesis selective phase (0.4.0)

The text layer now includes all 50 Genesis chapters (1,533 verses); entity/relationship annotation remains selective, **not a complete Genesis knowledge graph**. Added Jacob’s household, Joseph’s story, Judah/Tamar and selected rulers, places and burial relationships. Jacob/Israel, Benjamin/Benoni and Joseph/Zaphenath-Paneah are explicitly scoped aliases. Collective names, prophetic metaphors, false accusations and later identity harmonizations are not silently converted into facts.

The phase gate independently surfaced two old gaps: Adam/Eve’s marriage and Eve’s parenthood of Seth. These were added only after separate source review, with contextual wife/man identity notes. Existing 0.3 entity IDs, mentions and relations remain preserved.

**Repeatable release check:** `python scripts/phase_check.py --build --release` rebuilds, runs all tests, checks integrity and the independent major-character checklist, compares the frozen prior release, and refuses unresolved review findings. See `quality/README.md` and `reports/phase-quality.md`. Connectivity diagnostics deliberately preserve legitimate isolated nodes instead of inventing edges. Reviewed omissions remain visible; PASS is not a completeness/precision claim. No scheduled daily task or external API is needed.

## Documented connection repairs (0.5.0)

All **43 named connection gaps** from the v0.4 report have been addressed with **55 source-backed relationships** and three necessary intermediates: the garden in Eden, the unnamed river flowing out of Eden, and Abraham’s unnamed Genesis24 servant. The old servant is not identified with Eliezer. No old entity IDs, mention records, relationships or uncertainty records were removed or changed.

There are now **zero isolated nodes and one connected component**. This is a diagnostic result, not the reason the repairs are accepted. Each previous gap has a frozen before-state, specific new relationship records, verse evidence and independent review hashes in `quality/gap-resolution-ledger.json`; readable account in `reports/gap-resolution.md`. Zero prior connection tasks remain partial or residual. The retained 40 uncertainty notes and selective text coverage remain: the dataset is not an exhaustive extraction of every Genesis action or doctrine.

Examples include Melchizedek’s blessing and receipt of a tenth, Ephron’s transaction with Abraham, Deborah’s nurse role, Potiphera’s priesthood at On, and explicit well/place naming. Precise predicates preserve limits: Rachel is buried **on the way to** Ephrath, Abram camps **west of** Ai, Eliezer is Abram’s **stated prospective** heir, and collective campaign participation is not personal killing.

The release gate now compares the frozen canonical v0.4, checks all43 ledger findings, binds their exact reviewed edge records, and rejects deleted, reassigned, unrelated or stale supporting claims. It does not accept a prior omission disposition as a repair. New source-role expectations and negative mutation tests protect the additions.
