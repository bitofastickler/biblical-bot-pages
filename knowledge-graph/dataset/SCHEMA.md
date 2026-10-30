# Data contract 0.5.0

## Passage and entity identity

`GEN.chapter.verse` is a passage identity within this WEB source snapshot. Navigation uses `book_id`, `chapter`, `verse`; do not assume another translation has identical wording or segmentation. Entity IDs `bg:*` are stable editorial IDs, not universal identifiers. Never merge two IDs merely because their aliases match.

Entity types: `person`, `place`, `deity`, `animal`, `object`, `genealogical_referent`. The last leaves individual/eponym/people ontology unresolved. Labels may contain editorial qualifiers; aliases are source forms scoped by the curation code, not universal regex rules. No modern coordinates are supplied.

## Mentions

A mention connects one entity to one exact source substring. `start` is inclusive and `end` exclusive, measured in **Unicode code points**, as Python string offsets. JavaScript uses UTF-16 code units: use `Array.from(text).slice(start,end).join('')` to honor this contract. `surface` must equal that slice. Offsets are within one verse, not the full corpus. Overlapping mentions across entities are permitted by the format but require editorial justification; this pilot avoids global substring matching. `resolution: curated_name_scope` means selected literal form in an explicitly reviewed scope, not independently benchmarked confidence.

## Relations

Every relation has subject/object IDs, a typed predicate, one or more evidence verse IDs, and an assertion context. Evidence order follows editorial citation order. Evidence is full-verse, not a minimal quote span; read all cited verses and relevant antecedents. No inverse or transitive edges are materialized. An absent edge is **unknown/not curated**, not false.

| Predicate | Direction and meaning |
| --- | --- |
| `parent_of` | Text explicitly presents subject as parent of object; not inferred from sibling/spouse links. |
| `genealogical_parent_of` | Textual genealogical parent presentation where ontology is unresolved; not a stronger biological claim. |
| `spouse_of` | Symmetric marriage relation, stored once in the recorded direction. |
| `sibling_of` | Symmetric sibling relation, stored once; does not imply full/shared parentage. |
| `killed` | Subject kills object in narrative. |
| `resided_in` | Subject resides in object place in cited passage; not lifetime residence. |
| `flows_through` | River subject flows through named land object in text. |
| `rested_on` | Object subject comes to rest on place object. |
| `built` | Subject constructs object, supported by command/compliance/context. |
| `died_in` | Subject dies in cited place. |
| `addressed` | Subject speaks to object; content is not otherwise asserted by this edge. |
| `pronounced_curse_on` | Speaker subject pronounces a curse on object; does not assert objective cursed status. |

`assertion.scope` is always `in_text`. `mode: narration` identifies narrative attribution; `speaker` is null. `mode: speech` requires a speaker ID. This distinguishes Noah’s curse on Canaan from an objective property of Canaan (and from a curse on Ham). It does not make all quoted propositions true.

## Uncertainty

Uncertainty records carry source passages, issue and handling. They are kept separate from accepted relations; they are not scored competing truth claims. No guessed probability is supplied. Some topics are omitted rather than invented. `graph-view.json` is only a UI projection: use canonical `graph.json` and these uncertainty records in details panels. Each projected link preserves assertion and note fields; do not display a claim stripped of that context.

## Validation boundary

The JSON Schema describes shape and allowed types/predicates. `validate.py` adds identity, source hashes, verse fidelity, referential integrity, exact offset and projection checks without third-party dependencies. Neither a schema pass nor tests prove semantic accuracy or completeness. Build output is reproducible for the included blob and curation rules.

## Description fields (added in 0.2.0)

Each entity requires a nonempty `description`, nonempty `description_evidence` array of valid source verse IDs, and `editorial_note` (which may be empty). The description is a concise reader-facing summary bounded to the pilot passages. Its claims come from the cited text, not necessarily from materialized edges. Evidence also supports explicit namesake contrasts when another passage is cited. Editorial absences and scope policies are curation decisions, not propositions proven by a verse.

`editorial_note` preserves the earlier technical identity/coverage cautions separately from friendly prose. Node projections retain description, evidence and note together. A UI can show the description first, followed by passage links and the editorial note. Preserve these fields instead of synthesizing a biography solely from the limited edge set.

Migration from 0.1.0: entity IDs, verse IDs, mention spans, relation IDs and relation semantics are unchanged. The former `description` values are moved to `editorial_note`; new evidence-grounded prose occupies `description`. The schema version changes to 0.2.0 because entity records now require these additional fields.

## 0.3.0 expansion contract

Record shapes are unchanged; the version and allowed predicate vocabulary expand. Source passage coverage is now Genesis 1–25. Existing IDs persist, including `bg:abram` and `bg:sarai`. Alias strings alone are never a global resolution rule: curated scopes and exceptions are maintained in `curation/genesis12-25.json`, and explicit renaming evidence is retained in the descriptions and uncertainty record `u:name-changes`.

| Added predicate | Direction / reading |
| --- | --- |
| `king_of` | Person → textual place/kingdom, as identified in evidence. |
| `allied_with` | Symmetric alliance, stored once. |
| `rescued` | Person → person recovered from captivity in cited narrative. |
| `buried` | Agent → deceased person; not the burial location. |
| `buried_at` | Deceased person → burial place. |
| `acquired` | Person → named property in narrated transaction, not modern title. |
| `covenant_with` | Symmetric covenant-making presentation, stored once; narrative reports act, not independent fulfillment of all terms. |
| `promised_land_to` | Deity → recipient person; object is the recipient, not land. Requires attributed speech; details and offspring scope are in cited text/note. |
| `claimed_half_sibling_of` | Speaker → alleged half-sibling; requires speaker attribution. Does not establish unqualified genealogy. |
| `bound` | Person → person tied in cited action; does not imply death. |
| `sold_birthright_to` | Seller → recipient in narrated transaction. |
| `servant_of` | Person → household superior as described; not endorsement or a modern status. |
| `army_captain_of` | Person → ruler whose army they command. |
| `traveled_to` | Person → place of narrated arrival/passage; not permanent residence or full route reconstruction. |

Descriptions can change as coverage grows; this is not an identity change. Five prior descriptions are expanded in 0.3.0. No full-Bible completeness, event ontology, modern coordinates or historical verification is implied.

Mention exception in 0.3.0: the first “Yahweh” in Genesis 22:14 is inside the named place “Yahweh Will Provide” and is not annotated as a deity mention. The separate possessive “Yahweh’s mountain” remains a deity reference. This is an explicit local exception, not a general automatic coreference rule.

## 0.4.0: Genesis 1–50

Record shapes remain stable; three predicates are added:

- `appointed_to_rule`: person → person appointed to an administrative/ruling role in the cited narrative; does not imply kingship.
- `interpreted_dream_for`: interpreter → dreamer; records the interpretive act, not independent fulfillment or truth of each prediction.
- `provided_food_for`: provider → recipient person; cited household provision can include others without synthesizing every recipient.

Identity remains scoped: Jacob/Israel personal uses are separate from collective Israel; Joseph’s Egyptian name and Benjamin/Benoni use explicit naming verses. Distinct IDs are retained for Shelah son of Judah versus the earlier Shelah; Pharaoh Genesis12 versus Joseph-story Pharaoh; Potiphar versus Potiphera; and chapter26 Abimelech/Phicol versus their earlier namesakes. Anonymous role-labeled people are not given invented personal names.

Quality reports are separate from canonical graph data. They do not add edges or make a source claim true. Degree is relationship count, neighbors are unique undirected adjacent IDs, and components are calculated only from stored relations. See `quality/README.md` for acceptance rules and report provenance.

## 0.5.0: evidence-backed connection repair

Entity/mention/relation shapes remain stable. Added precise predicate definitions live in `schema/phase-predicates.json`, including endpoint types, symmetry and required speech attribution. The validator applies these constraints. A naming edge is not a construction edge; a prospective-heir statement is not a completed inheritance; route-relative burial is not containment inside the named town.

| Added predicate | Meaning |
| --- | --- |
| `branch_of` | Named river subject is one of the rivers sourced by the divided river object in the textual account; no modern hydrological reconstruction. |
| `buried_on_way_to` | Route-relative burial; explicitly not burial inside the destination town. |
| `camped_at` | Temporary encampment at the cited textual place, including explicit group participation. |
| `camped_west_of` | Person’s narrated tent location west of place object; not residence within the place. |
| `chose_region` | Narrated selection of the region object; does not establish land ownership. |
| `crossed` | Narrated crossing of a named watercourse/ford; no modern route reconstructed. |
| `destroyed` | Destruction narrated of a place/object; no claim beyond the text. |
| `flows_from` | River subject flows out of textual place object. |
| `flows_in_front_of` | River relative to named land using the supplied WEB phrase; not flow through or a modern cardinal bearing. |
| `friend_of` | Explicitly named friendship, stored once; not inferred from proximity. |
| `gave_tenth_to` | Narrated transfer of a tenth to recipient; no universal obligation inferred. |
| `kingdom_includes` | Place object explicitly listed in subject’s kingdom; does not assert a modern title. |
| `located_in` | Textual containment/location; not equivalence or modern coordinates. |
| `military_opponent_of` | Named rulers in explicitly opposing military coalitions; not a personal duel or separate bilateral war. |
| `military_victory_over` | Narrated military leader subject returns victorious over opponent object with respective forces; not personal killing. |
| `named` | Narrated naming of a place or object; the assigned name is in entity aliases and evidence. Does not imply sole construction. |
| `named_as_prospective_heir` | Speaker subject identifies object as anticipated heir; attributed speech required and not actual inheritance. |
| `nurse_of` | Explicit nurse/household-care role; does not infer biological motherhood. |
| `on_route_to` | Location subject explicitly or contextually on the way to place object; not a reconstructed modern route. |
| `paid` | Payer subject transfers the payment to recipient object; amount/property retained in evidence and note. |
| `participated_in_campaign_at` | Subject participates in the stated military campaign at place object; does not individually attribute every collective action. |
| `placed_guards_for` | Subject arranges guards for access to object/place; not necessarily personally guarding. |
| `planted` | Narrated planting of the named garden or plant; not independent historical verification. |
| `priest_of` | Person serving as priest of the named place; no identification of the worshipped deity is implied. |
| `prohibited_eating_from` | Speaker subject prohibits eating from named object in attributed command; addressee and scope in evidence/note. |
| `pronounced_blessing_on` | Speaker subject utters blessing over person object, not a fulfillment/status claim. |
| `sent_messengers_to` | Sender dispatches messengers toward named location; does not establish sender arrival. |
| `sold_to` | Seller subject transfers property for payment to buyer object in cited transaction; object is buyer, not property. |
| `waited_at` | Person sits/waits at named place; not permanent residence or an occupation. |
| `waters` | River subject supplies water to garden/place object in narrative. |

`quality/gap-resolution-ledger.json` is a separate source-review artifact, not a source text or set of graph edges. It pins the v0.4 graph and report hashes, accounts for all43 original coverage finding fingerprints, and gives expected canonical records for its supporting new edges. Each approval hashes the reviewed record. Any change requires a new review; generation does not automatically update approvals.

The phase report includes `gap_resolution` with total/resolved/partial/residual/unreviewed counts, status, complete boolean, and ledger SHA256. A hard gap-check error forces status FAIL and complete false even if someone labels all items resolved. Release additionally requires complete true.
