# Independent AI-assisted audit — Genesis 1–11 pilot

**Verdict: PASS for the stated selective pilot scope, with the limitations below.** Semantic corrections and final validation were independently checked on 2026-10-28. This is a useful, evidence-backed foundation, not a certified or exhaustive Bible graph.

## Scope and method

A separate assistant reviewed all 299 supplied WEB verses in Genesis 1–11, all initial 68 relation records (67 after deduplication), all entity definitions, every mention's assigned verse/offset listing, build logic, schema, and integrity tests. This is independent AI-assisted review, **not human scholarly certification**. Review is relative to this supplied English text, not a historical, archaeological, Hebrew-text, or theological verification.

## Findings corrected during review

1. **Enoch, Genesis 4:17:** the second occurrence is appositional to “his son”; excluding it as exclusively a city mention was incorrect. Restored to the son's entity, giving 448 selected literal mentions.
2. **Unresolved genealogical ontology:** `parent_of` for Ham → Canaan and Cush → Nimrod was inconsistent with their `genealogical_referent` types. Converted to `genealogical_parent_of`; merged duplicate Ham → Canaan evidence (9:18, 10:6). Final relation count: 67.
3. **Noah's construction evidence:** added the command (6:14) and reported compliance (6:22) to 8:6, avoiding dependence solely on the attachment of “which he had made.”

## Positive semantic checks

- Kinship directions and source evidence were reviewed, not inferred from co-occurrence. No unsupported relation remaining was identified in this pass.
- Cain-line and Seth-line Enoch/Lamech, the two Nahors, and Haran person/place have separate IDs and scoped mentions.
- Cain substrings within Tubal Cain are excluded. Collective Adam (5:2) is not assigned to the individual.
- Land and genealogical referents for Cush/Canaan are separated. Unselected Havilah/Sheba genealogical names are not accidentally attached to land/person entries.
- No serpent=Satan claim, invented individual “sons of God,” divine-trinity inference, or forced Nephilim genealogy is asserted.
- Noah's curse is attributed to Noah and targets Canaan, not Ham; it is not modeled as objective cursed status.
- Ararat is “Ararat's mountains,” not an asserted modern peak/coordinate. Place identities are textual, not archaeological.
- Genealogical uncertainty and the editorial continuity of Babel are disclosed.
- All initial 447 mention surfaces round-tripped exactly to source text; the restored Enoch mention is additionally checked in final validation.

## Final verification

- `python scripts/validate.py`: PASS — 299 verses, 75 entities, 448 mentions, 67 relations, 7 uncertainty records.
- `python -m unittest discover -s tests -v`: all 5 tests passed, including malformed offsets/schema/references and speech-attribution cases.
- Independent temporary-copy mutations of schema version and mention resolution now fail as expected. The validator checks the subset of JSON Schema keywords actually used by the bundled schema, rather than claiming to implement arbitrary JSON Schema.
- Exact pilot verse-set, source hashes, endpoint constraints, and ID-keyed view projection checks were added and inspected.
- All navigation links now retain assertion/speaker/note, verified by the validator.
- Rebuilding a temporary package copy produced byte-identical JSON assets. No production build files were mutated by this audit.
- Final graph SHA256: `d9dd7197828ded692d2f6f376226e53f6e2082f60c1fd5e87191996756e7614a`.
- Final source SHA256: `5408af7f9c0d2800f0099b26ca9f8e2a8b319beb180af88257c004126b767580`. The earlier inspection had a patch-added trailing newline; builder removed it to match the repository Git blob, without changing verse strings.

Remaining engineering limits: integrity checks use Python assertions and must run without `-O`/`PYTHONOPTIMIZE`; the schema validator supports only its documented bundled subset. Valid evidence references and valid entity types cannot establish that an edge's meaning is correct. A wrong same-name identity assignment can still have valid offsets and requires semantic regression cases/review. Do not treat passing tests as a general extraction-quality score.

## Honest limits / release interpretation

This is a **selected Genesis 1–11 pilot**, not a complete Genesis graph or a whole-Bible entity database. Important explicit relationships and many named referents are intentionally absent. Absence of an edge does not mean no relationship exists. Mention recall is not measured; pronouns, generic descriptions, and many coreferences are omitted. Precision here was reviewed qualitatively, not estimated against an independent gold standard.

Source integrity hashes establish a fixed repository snapshot, not independent verification against an official WEB release. Public-domain text status and any eventual annotation licensing should be kept distinct. IDs are stable within the pilot's editorial model; cross-book expansion will require a documented identity and migration policy. Literal span offsets must be consumed as Unicode code-point, half-open offsets, not UTF-8 bytes or JavaScript UTF-16 indices.

No application integration or deployment was performed. Before wider publication, obtain a human editorial review and build a representative adjudicated evaluation set, especially for cross-book namesakes, translation differences, and disputed identity/coreference decisions.

---

## v0.2.0 description-layer audit — 2026-10-29

**Verdict: PASS for the requested description update within the existing selective Genesis 1–11 scope.**

Reviewed all 75 new descriptions and their evidence references against the supplied WEB Genesis text, including the full source reading recorded above. No material unsupported interpretation, namesake conflation, or new theological identity claim was identified. The descriptions preserve narrative/speech attribution where important (Enoch taken by God, Lamech's reported killing, Noah's curse, and the narrative lifespan of Methuselah). Genealogical and geographic uncertainties remain explicit. They do not import later Abraham/Sarah narratives or modern ethnic/geographic equations.

### Evidence improvements requested and verified

- God: added 6:17 to support the explicit flood wording.
- Noah: added 7:13 to identify the family among the ship's survivors.
- Shinar: added 10:8–9 to establish Nimrod as the antecedent of “his kingdom” in 10:10.
- Arpachshad and Reu: added 11:26 as endpoint context for the genealogy leading toward Terah's family.
- Adah and Zillah: added 4:17–18 to establish the Cain-line Lamech context.

These were evidence-completeness improvements, not changes to the entity inventory or relation model. Description evidence may include contextual or disambiguating passages rather than only verses that literally name the entry.

### Verification

- Compared current graph with the retained v0.1.0 ZIP: all mentions, relations, and uncertainty structures are unchanged; entity IDs, labels, types, and aliases are unchanged. Every old description is preserved exactly as `editorial_note`.
- Schema requires `description`, nonempty `description_evidence`, and `editorial_note`. Validator checks nonblank prose, valid evidence IDs, and exact preservation of description/evidence/editorial-note fields in navigation nodes.
- `python scripts/validate.py`: PASS (299 verses, 75 entities, 448 mentions, 67 relations, 7 uncertainty records).
- `python -m unittest discover -s tests -v`: all 7 tests passed, including coverage parity with the curation asset and rejection of blank descriptions, dangling description references, and corrupted navigation descriptions.
- Temporary-copy rebuild: byte-identical JSON assets.
- Audited v0.2.0 graph SHA256: `0e4901403eef04775cdc6cf900d10de127e6f5d44893d51cf2d9378219d08299`.
- Validator now explicitly refuses optimized Python, closing the earlier `-O` caveat.

This remains an AI-assisted semantic review, not human scholarly certification or a measured precision/recall result. Valid citation IDs do not automatically prove prose entailment. Descriptions are concise contextual summaries, not exhaustive biographies; some describe relationships that are not separately materialized as graph edges. No corpus expansion, application edits, or deployment occurred in this audit.
