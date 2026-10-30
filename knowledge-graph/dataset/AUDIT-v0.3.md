# Independent AI-assisted audit — v0.3.0

**Verdict: PASS for the stated selective Genesis 1–25 dataset scope.**

Reviewed 2026-10-29. This is a separate assistant's source-based review, not human scholarly certification or independent historical verification. No remaining material semantic blocker was identified in the audited build.

## Review coverage

- Read all 394 actual supplied WEB verses in Genesis 12–25 (earlier Genesis 1–11 review is retained in `AUDIT.md`). Total source passage coverage is now 693 verses.
- Reviewed all 53 new entity definitions/descriptions, five updated descriptions, all 68 new relations, 11 new uncertainty records, scoped alias extensions, and the complete new mention listing.
- Inspected builder logic, JSON Schema, validator, tests, migration notes, and predicate definitions.
- Final totals: **128 selected entities, 1,108 mentions, 135 relations, 18 uncertainty records**. These are selected annotations, not exhaustive extraction.

## Corrections requested and verified

1. Zohar → Ephron parenthood initially cited only Abraham's speech in 23:8 while labeled narration. Added narrator evidence 25:9; the relation is now supported as narration.
2. Isaac and Rebekah descriptions now include 25:21 to establish the named mother antecedent for the twins' birth in 25:24–26.
3. Pharaoh description changed from implying he expressly orders Sarai taken to the source-supported passive account: she is taken into his house after the princes praise her.
4. Mamre place description narrowed to the appearance of Yahweh and three men, matching its cited evidence rather than an uncited welcome sequence.
5. The first “Yahweh” in 22:14, inside the place name “Yahweh Will Provide,” is excluded from the deity-mention layer. The separate possessive “Yahweh's mountain” is retained; this local editorial exception is documented and tested.
6. Added expansion-specific regression coverage for aliases, namesakes, unasserted servant identity, the attributed Sarah kinship claim, and the absence of a killing edge for Isaac.

The three later-added `traveled_to` edges (Abram → Shechem, Abram → Bethel, Lot → Zoar) were also read against their evidence and have the correct direction. Travel is distinguished from permanent residence.

## Identity and assertion safeguards

- Abram/Abraham and Sarai/Sarah retain the existing `bg:abram` and `bg:sarai` IDs with explicit renaming evidence and scoped literal aliases. Esau's Edom alias is limited to 25:30.
- Ham in 14:5 is not assigned to Noah's son. “City of Nahor” in 24:10 is not assigned to a person or automatically equated with Haran. The Havilah in 25:18 is not silently merged with Eden's land.
- Mamre's ally/person and place/landmark mentions are separated. Royal titles remain scoped; unnamed Pharaoh is not given an invented personal identity.
- Eliezer is not equated with Genesis 24's unnamed servant. Angels/visitors are not forcibly equated across scenes or with deity entities.
- Abraham's half-sibling explanation concerning Sarah remains attributed speech, not unqualified genealogy. Land promises remain attributed and do not assert modern title. Isaac is bound, not killed.
- Genealogical referents and sensitive origin narratives are not transformed into claims about modern peoples. Geographic names are textual, not modern archaeological identifications.

## Independent checks

- Compared with the retained v0.2.0 ZIP: all Genesis 1–11 mention records, all 67 earlier relations, all seven earlier uncertainty records, and all earlier IDs/types remain intact. Earlier aliases remain present; label changes for Abraham/Sarah do not change identity.
- `python scripts/validate.py`: PASS.
- `python -m unittest discover -s tests -v`: all **9 tests** passed.
- All mention surfaces and offsets, source hashes, evidence references, entity description projection fields, and relation assertion projection fields pass integrity checks.
- Rebuilding a temporary copy produced byte-identical JSON assets.
- Independently changed the half-sibling relation to narration in a temporary copy: validator rejected the lost attribution.
- Audited graph SHA256: `d50671fc08c891900772c984831460ca4a0002890dce3681ee0cc558e6bdf033`.

## Limits and integration handoff

Coverage is intentionally selective: many names, unnamed persons, coreferences, events and relationships remain omitted. Absence of an edge means not curated, not false. Evidence is full-verse with contextual antecedents, not minimal claim spans. No precision/recall benchmark or human editorial approval is claimed. Passing schema/tests cannot establish semantic correctness for arbitrary future annotations.

Private preview integration may consume this audited build, preserving descriptions, evidence, editorial notes and per-edge attribution. This verdict concerns data readiness, not UI correctness, accessibility, deployment success or a permission to change the live GitHub application. The dataset audit itself made no live application or repository changes.
