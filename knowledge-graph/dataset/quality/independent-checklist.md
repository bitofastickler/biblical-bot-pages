# Independent quality-gate review checklist

Prepared from the actual supplied Genesis text, not inferred from current graph contents. This is a selective editorial acceptance policy, not an exhaustive extraction gold standard.

## Hard integrity/release checks
- Every declared phase has the exact source verse set; original snapshot hashes match. Source passages remain verbatim.
- Unique stable IDs, valid entity/evidence references, exact Unicode mention slices, allowed predicate endpoints, description evidence and projection attribution are enforced.
- Existing accepted IDs and previously curated annotations are retained except explicitly documented corrections. Compare to the restored canonical v0.3, not the reverted workspace v0.2.
- Missing **declared required** major entities/aliases/relationships fail, rather than silently changing expected counts to the new output.
- Speech-only, dream-only, conditional, metaphorical, and false-in-story statements cannot become unqualified factual edges.
- `--release` fails on unresolved editorial warnings; accepted warnings carry a specific reason, source passages where relevant, reviewer/method, and reviewed status. Acceptance is not a claim of human scholarly review.
- Test deliberate mutations: remove a major person; remove a required edge while leaving counts consistent; drop rename alias; change speech to narration; attach same-name span to wrong referent; introduce isolated major person; hide a disconnected major component; tamper accepted-warning reason; change source; drop projected attribution.

## Source-anchored major identity expectations
- Adam/Eve/Cain/Abel/Seth; Noah/Shem/Ham/Japheth; Abram/Abraham, Sarai/Sarah, Hagar/Ishmael/Isaac, Lot; Rebekah/Laban; Jacob/Israel, Esau/Edom.
- Leah/Rachel/Bilhah/Zilpah; Jacob's twelve sons and Dinah; Joseph and Benjamin; Judah/Tamar/Er/Onan/Shelah/Perez/Zerah; Asenath/Potiphera/Potiphar, Manasseh/Ephraim.
- Exact rename evidence:17:5,17:15,25:30,32:28,35:10,35:18,41:45. These retain one identity, but collective Israel/Edom usages do not become person mentions by string matching.
- Namesakes requiring distinctions: Cain-line/Seth-line Enoch and Lamech; two Nahors; person/place Haran; person/place Shechem; Mamre person/place; Arpachshad-line versus Judah-line Shelah; Zerah Judah-line versus Esau-line; Potiphar/Potiphera; Pharaoh12 versus Joseph-era Pharaoh; Abimelech/Phicol26 versus20–21 unresolved; Esau-wife name discrepancies not automatically harmonized.

## Selected relationship acceptance anchors
- Adam/Eve spouse:2:25+3:17,20/4:1 with explicit contextual identity handling. Eve→Seth4:25 with wife antecedent context; Adam→Cain/Abel4:1–2 if contextual parenthood is within editorial policy. Otherwise report a specific known gap, not silent completeness.
- Abraham/Sarah spouse11:29; Abraham/Hagar→Ishmael16:15; Abraham/Sarah→Isaac21:2–3; Isaac/Rebekah spouse24:67; Isaac/Rebekah→Jacob/Esau25:21–26; Bethuel→Rebekah24:15 and→Laban28:5; Rebekah/Laban siblings24:29.
- Laban→Leah/Rachel29:16. Jacob spouses Leah29:23–30, Rachel29:28, Bilhah30:4, Zilpah30:9. Parentage of12 sons35:22–26 plus Dinah34:1. Biological mothers retained rather than inferred from household status.
- Joseph/Asenath spouse41:45, both parents of Manasseh/Ephraim41:50–52/46:20; Potiphera→Asenath41:45. Judah→Er/Onan/Shelah46:12; Judah/Tamar→Perez/Zerah38:18,27–30/46:12.
- Joseph binds Simeon42:24; Jacob burial at Machpelah50:13; Joseph burial participation50:7,12–14. Joseph dies in Egypt50:22–26; promise to carry his bones is not fulfillment in Genesis.

## Explicit forbidden shortcuts
- No serpent=Satan; no unnamed Genesis24 servant=Eliezer.
- No Abraham killed Isaac; no Esau killed Jacob from27:41 threat.
- No unqualified Sarah half-sibling edge from Abraham20:12 speech.
- No Joseph killed/devoured from Jacob37:33 or42:36 belief; no Benjamin stole cup44:1–2,12; no Joseph biological father of Pharaoh45:8 metaphor.
- No Jacob biological parent of Ephraim/Manasseh from48:5 claim/adoption presentation.
- No zoological identities from49 blessing metaphors; no fulfillment/modern ethnic entitlement inferred from blessings.
- No forced seller identity from37:28 ambiguity; preserve45:4 as Joseph's attributed account if used.

## Topology is a diagnostic, not a truth target
Compute undirected connected components for navigation, degree with unique neighbors, and relation counts separately. A duplicate/reverse edge must not satisfy a missing-link check. Include isolated entities and major people stranded in small components even if their degree is nonzero. Distinguish physical disconnection from chapter scope or UI filters.

Canonical v0.3 baseline independently observed:20 isolated nodes,28 components; main81-node component, separate15-node Eve/Cain family, six2-node components. Major examples to explain to a reader:
- Eve and Cain's family are separate from Adam's family because bridging kinship/marriage links were not yet curated.
- Melchizedek links to Salem but not Abram despite14:18–20.
- Ephron links to Zohar but not the Abraham transaction in23:16–18.
- Pharaoh12 and Eliezer have no graph edges.

These are real selected-coverage limitations; they are not invitations to fabricate relations. An isolated river, tree, or selected place can be acceptable with a documented editorial omission. A major-character expectation should not be satisfied merely by one incidental place edge, nor should a missing expected relation be excused because a different path connects the same people.
