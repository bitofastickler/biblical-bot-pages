#!/usr/bin/env python3
"""Build deterministic assets from hand-curated selections, not automatic extraction."""
import json,hashlib,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def dump(p,x): (ROOT/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
raw=(ROOT/'source/web.json').read_bytes()
expected='ee0fcd2a5779070a187dc91b6899adc701842663'
def gitsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
if gitsha(raw)!=expected and raw.endswith(b'\n') and gitsha(raw[:-1])==expected:
 raw=raw[:-1];(ROOT/'source/web.json').write_bytes(raw)
if gitsha(raw)!=expected:raise ValueError('Source blob mismatch')
src=json.loads(raw); book=next(b for b in src['books'] if b['id']=='genesis')
V={f'GEN.{c}.{v}':t for c,vs in book['chapters'].items() if int(c)<=50 for v,t in vs.items()}
def refs(s):return ['GEN.'+r.replace(':','.') for r in s.split()]
E=[];M=[];R=[]
def ent(key,label,typ,aliases,scope,note=''):
 eid='bg:'+key
 E.append(dict(id=eid,label=label,type=typ,aliases=aliases,description=note))
 # Scopes and aliases were individually selected after reading these chapters.
 # This does not resolve pronouns or unlisted occurrences; longest match wins.
 eligible=refs(scope) if ':' in scope else [v for v in V if int(v.split('.')[1]) in [int(n) for n in scope.split()]]
 for vid in eligible:
  occupied=set()
  for alias in sorted(aliases,key=len,reverse=True):
   for mt in re.finditer(r'(?<!\w)'+re.escape(alias)+r'(?!\w)',V[vid]):
    if occupied.intersection(range(mt.start(),mt.end())):continue
    occupied.update(range(mt.start(),mt.end()))
    M.append(dict(id=f'm:{key}:{vid}:{mt.start()}',entity_id=eid,verse_id=vid,start=mt.start(),end=mt.end(),surface=mt.group(),resolution='curated_name_scope'))
 return eid
# Names are not automatically aliases across the Bible. These IDs never depend on display labels.
ent('deity-god','God / Yahweh','deity',['Yahweh God','Yahweh','God'],'1 2 3 4 5 6 7 8 9 10 11','Narrative referent within this pilot only; no theological identity links. Possessive compounds God’s Spirit and God’s sons are not distinct mentions of those concepts here.')
ent('adam','Adam','person',['Adam'],'3:17 3:21 4:25 5:1 5:3 5:4 5:5','Generic man and collective Adam in 5:2 intentionally excluded.')
ent('eve','Eve','person',['Eve'],'3 4','woman/wife coreference omitted from mention layer.')
for key,label,scope in [('cain','Cain','4'),('abel','Abel','4'),('seth','Seth','4 5'),('enosh','Enosh','4 5'),('enoch-cain','Enoch (Cain’s son)','4:17 4:18'),('irad','Irad','4'),('mehujael','Mehujael','4'),('methushael','Methushael','4'),('lamech-cain','Lamech (Cain line)','4'),('adah','Adah','4'),('zillah','Zillah','4'),('jabal','Jabal','4'),('jubal','Jubal','4'),('tubal-cain','Tubal Cain','4'),('naamah','Naamah','4'),('kenan','Kenan','5'),('mahalalel','Mahalalel','5'),('jared','Jared','5'),('enoch-seth','Enoch (Jared’s son)','5'),('methuselah','Methuselah','5'),('lamech-seth','Lamech (Noah’s father)','5'),('noah','Noah','5 6 7 8 9 10'),('shem','Shem','5 6 7 9 10 11'),('ham','Ham','5 6 7 9 10'),('japheth','Japheth','5 6 7 9 10'),('nimrod','Nimrod','10'),('arpachshad','Arpachshad','10 11'),('shelah','Shelah','10 11'),('eber','Eber','10 11'),('peleg','Peleg','10 11'),('reu','Reu','11'),('serug','Serug','11'),('nahor-serug','Nahor (Serug’s son)','11:22 11:23 11:24 11:25'),('terah','Terah','11'),('abram','Abram','11'),('nahor-terah','Nahor (Terah’s son)','11:26 11:27 11:29'),('haran-person','Haran (Terah’s son)','11:26 11:27 11:28 11:29 11:31'),('lot','Lot','11'),('sarai','Sarai','11'),('milcah','Milcah','11'),('iscah','Iscah','11')]:
 alias=label.split(' (')[0]
 ent(key,label,'person',[alias],scope)
# Remove context-specific false substring/name matches: Cain within Tubal Cain;
# Enoch in 4:17 refers to the son (the city is named after him); Haran destination in 11:31 is a place.
M[:]=[m for m in M if not (m['entity_id']=='bg:cain' and V[m['verse_id']][max(0,m['start']-6):m['start']]=='Tubal ') and not (m['entity_id']=='bg:haran-person' and m['verse_id']=='GEN.11.31' and m['start']==V['GEN.11.31'].rfind('Haran'))]
for key,label,aliases,scope in [('eden','Eden',['Eden'],'2 3 4'),('nod','Nod',['Nod'],'4'),('pishon','Pishon',['Pishon'],'2'),('gihon','Gihon',['Gihon'],'2'),('hiddekel','Hiddekel',['Hiddekel'],'2'),('euphrates','Euphrates',['Euphrates'],'2'),('havilah-land','Havilah (land)',['Havilah'],'2'),('cush-land','Cush (land)',['Cush'],'2'),('assyria','Assyria',['Assyria'],'2 10'),('ararat-mountains','Ararat’s mountains',['Ararat’s mountains'],'8'),('shinar','Shinar',['Shinar'],'10 11'),('babel','Babel',['Babel'],'10 11'),('ur-chaldees','Ur of the Chaldees',['Ur of the Chaldees'],'11'),('canaan-land','Canaan (land)',['Canaan'],'11')]:
 ent(key,label,'place',aliases,scope,'Textual location only; no modern coordinates or geographic equivalence asserted.')
ent('haran-place','Haran (place)','place',['Haran'],'11:32')
# Explicit span for the second Haran in 11:31.
s=V['GEN.11.31'].rfind('Haran');M.append(dict(id=f'm:haran-place:GEN.11.31:{s}',entity_id='bg:haran-place',verse_id='GEN.11.31',start=s,end=s+5,surface='Haran',resolution='curated_name_scope'))
ent('serpent','Serpent in Eden','animal',['serpent'],'3','No equation with Satan or another entity.')
ent('ship-noah','Noah’s ship','object',['ship'],'6 7 8 9','WEB uses ship, not ark. Noah’s ship is a display label, not an asserted source alias.')
ent('tree-life','Tree of life','object',['tree of life'],'2 3')
ent('tree-knowledge','Tree of the knowledge of good and evil','object',['tree of the knowledge of good and evil'],'2')
# Selected Table of Nations entries are genealogical referents, not forced individual persons.
for key,label,scope in [('canaan-genealogical','Canaan','9 10'),('cush-genealogical','Cush','10'),('mizraim','Mizraim','10'),('put','Put','10'),('gomer','Gomer','10'),('magog','Magog','10'),('madai','Madai','10'),('javan','Javan','10'),('tubal','Tubal','10'),('meshech','Meshech','10'),('tiras','Tiras','10'),('joktan','Joktan','10')]:
 ent(key,label,'genealogical_referent',[label],scope,'Genealogical presentation in the text; individual/eponym/people interpretation is not resolved.')
def rel(a,p,b,e,note='',speaker=None):
 R.append(dict(id=f'r:{a}:{p}:{b}',subject='bg:'+a,predicate=p,object='bg:'+b,evidence=refs(e),assertion=dict(scope='in_text',mode='speech' if speaker else 'narration',speaker='bg:'+speaker if speaker else None),note=note))
# Explicit parenthood; not transitive ancestry or unspoken biological inference.
for a,b,e in [('eve','cain','4:1'),('eve','abel','4:1 4:2'),('adam','seth','5:3'),('seth','enosh','4:26 5:6'),('cain','enoch-cain','4:17'),('enoch-cain','irad','4:18'),('irad','mehujael','4:18'),('mehujael','methushael','4:18'),('methushael','lamech-cain','4:18'),('adah','jabal','4:20'),('zillah','tubal-cain','4:22'),('enosh','kenan','5:9'),('kenan','mahalalel','5:12'),('mahalalel','jared','5:15'),('jared','enoch-seth','5:18'),('enoch-seth','methuselah','5:21'),('methuselah','lamech-seth','5:25'),('lamech-seth','noah','5:28 5:29 5:30'),('noah','shem','5:32 6:10'),('noah','ham','5:32 6:10'),('noah','japheth','5:32 6:10'),('shem','arpachshad','11:10'),('arpachshad','shelah','10:24 11:12'),('shelah','eber','10:24 11:14'),('eber','peleg','10:25 11:16'),('peleg','reu','11:18'),('reu','serug','11:20'),('serug','nahor-serug','11:22'),('nahor-serug','terah','11:24'),('terah','abram','11:26 11:27'),('terah','nahor-terah','11:26 11:27'),('terah','haran-person','11:26 11:27'),('haran-person','lot','11:27'),('haran-person','milcah','11:29'),('haran-person','iscah','11:29')]:rel(a,'parent_of',b,e)
for a,b,e in [('lamech-cain','adah','4:19'),('lamech-cain','zillah','4:19'),('abram','sarai','11:29'),('nahor-terah','milcah','11:29')]:rel(a,'spouse_of',b,e)
for a,b,e in [('cain','abel','4:2 4:8'),('jabal','jubal','4:20 4:21'),('tubal-cain','naamah','4:22'),('peleg','joktan','10:25')]:rel(a,'sibling_of',b,e)
rel('cain','killed','abel','4:8')
rel('cain','resided_in','nod','4:16')
rel('pishon','flows_through','havilah-land','2:11')
rel('gihon','flows_through','cush-land','2:13')
rel('ship-noah','rested_on','ararat-mountains','8:4')
rel('noah','built','ship-noah','6:14 6:22 8:6','Command and reported compliance support construction; no claim about construction date.')
rel('terah','resided_in','haran-place','11:31 11:32')
rel('haran-person','died_in','ur-chaldees','11:28')
rel('terah','died_in','haran-place','11:32')
rel('deity-god','addressed','noah','6:13','Speech act only, not endorsement or independent historical verification.')
rel('noah','pronounced_curse_on','canaan-genealogical','9:24 9:25','Attributed speech, not an objective cursed status or a statement about Ham.',speaker='noah')
for a,children,e in [('japheth',['gomer','magog','madai','javan','tubal','meshech','tiras'],'10:2'),('ham',['cush-genealogical','mizraim','put','canaan-genealogical'],'10:6'),('eber',['joktan'],'10:25')]:
 for b in children:rel(a,'genealogical_parent_of',b,'9:18 10:6' if (a,b)==('ham','canaan-genealogical') else e,'Preserves genealogical wording without deciding individual/people ontology.')
rel('cush-genealogical','genealogical_parent_of','nimrod','10:8','Preserves genealogical wording without deciding individual/people ontology.')
uncertainties=[
 dict(id='u:adam-collective',verses=refs('1:26 1:27 5:2'),issue='Generic man and collective Adam are not assigned to individual Adam.',handling='Excluded from individual mention layer.'),
 dict(id='u:sons-god',verses=refs('6:2 6:4'),issue='Identity of God’s sons and relationship to Nephilim requires interpretation.',handling='No entity identity or genealogical edges asserted.'),
 dict(id='u:assyria-actor',verses=refs('10:11'),issue='Actor/translation issues in the Assyria passage and antecedent resolution.',handling='Place mention only; no builder or migration edge.'),
 dict(id='u:namesakes',verses=refs('4:17 4:18 5:18 5:25 11:22 11:26 11:31'),issue='Enoch, Lamech, Nahor and Haran have distinct scoped referents.',handling='Distinct stable IDs; no same_as relation.'),
 dict(id='u:serpent',verses=refs('3:1'),issue='Serpent identification with later figures is outside this passage.',handling='No Satan identity edge.'),
 dict(id='u:table-nations',verses=refs('10:1 10:5 10:20 10:31 10:32'),issue='Genealogies also describe families, lands, languages and nations.',handling='Selected entries typed genealogical_referent; ontology left unresolved.'),
 dict(id='u:babel-continuity',verses=refs('10:10 11:9'),issue='Babel place mentions use one narrative place ID; this is a pilot editorial continuity decision, not archaeological identification.',handling='No modern equivalence or coordinates assigned.')]
# Explicit extension curation. Preserve earlier identities, spans and relations.
chunks=[json.loads((ROOT/('curation/'+name)).read_text()) for name in ('genesis12-25.json','genesis26-36.json','genesis37-50.json','gaps-early.json','gaps-later.json')]
for X in chunks:
 for item in X['entities']:
  ent(item['key'],item['label'],item['type'],item['aliases'],item['scope'],item['editorial_note'])
 for item in X['extensions']:
  current=next(e for e in E if e['id']=='bg:'+item['key'])
  ent(item['key'],current['label'],current['type'],item['aliases'],item['scope'])
  E.pop()
  current['aliases']=list(dict.fromkeys(current['aliases']+item['aliases']))
 for item in X['relations']:
  rid=f"r:{item['subject']}:{item['predicate']}:{item['object']}"
  existing=next((r for r in R if r['id']==rid),None)
  if existing:
   if existing['assertion']['speaker']!=('bg:'+item['speaker'] if item['speaker'] else None):raise ValueError('Conflicting assertion contexts')
   existing['evidence']=list(dict.fromkeys(existing['evidence']+refs(item['evidence'])))
   if item['note'] and item['note']!=existing['note']:existing['note']+=' '+item['note']
  else:rel(item['subject'],item['predicate'],item['object'],item['evidence'],item['note'],item['speaker'])
 uncertainties.extend(X['uncertainties'])
for e in E:
 if e['id']=='bg:abram':e['label']='Abraham (Abram)'
 if e['id']=='bg:sarai':e['label']='Sarah (Sarai)'
 if e['id']=='bg:jacob':e['label']='Jacob (Israel)'
# Explicit source-backed gaps identified by independent phase expectations, reviewed before addition.
rel('adam','spouse_of','eve','3:17 3:20 4:1','Contextual man/wife identification from the naming passage; not a literal-name-only extraction.')
rel('eve','parent_of','seth','4:1 4:25','Contextual identification of Adam’s wife as Eve; mother is not newly named in 4:25.')
# Do not treat a divine-name component inside a named place as a deity mention.
M[:]=[m for m in M if not (m['entity_id']=='bg:deity-god' and m['verse_id']=='GEN.22.14' and m['start']==V['GEN.22.14'].index('Yahweh Will Provide'))]
# Reader-facing summaries are explicit reviewed curation, not prose generated from edges.
D=json.loads((ROOT/'curation/entity-descriptions.json').read_text())
for X in chunks:
 D.update({'bg:'+i['key']:{k:i[k] for k in ('description','description_evidence')} for i in X['entities']})
 D.update(X['description_updates'])
if set(D)!={e['id'] for e in E}:raise ValueError('Description coverage must match entities exactly')
for e in E:
 e['editorial_note']=e['description']
 e.update(D[e['id']])
 if not e['description'].strip() or not e['description_evidence'] or not all(v in V for v in e['description_evidence']):raise ValueError('Invalid entity description evidence')
M.sort(key=lambda m:(tuple(map(int,m['verse_id'].split('.')[1:])),m['start'],m['entity_id']))
graph=dict(schema_version='0.5.0',dataset_id='bible-graph-genesis-pilot',entities=E,mentions=M,relations=R,uncertainties=uncertainties)
dump('data/graph.json',graph)
dump('data/verses.json',[dict(id=k,book_id='GEN',chapter=int(k.split('.')[1]),verse=int(k.split('.')[2]),text=v,source_id='web-repo-snapshot') for k,v in V.items()])
dump('data/provenance.json',dict(dataset_version='0.5.0',annotation_updated_utc='2026-10-30',description_method='Explicit source-grounded editorial summaries with verse evidence; not generated from graph adjacency.',source_id='web-repo-snapshot',translation='WEB',repository='https://github.com/bitofastickler/biblical-bot-pages',path='data/web.json',retrieved_utc='2026-10-28',git_blob_sha1=expected,sha256=hashlib.sha256(raw).hexdigest(),byte_length=len(raw),source_url='https://github.com/bitofastickler/biblical-bot-pages/blob/main/data/web.json',upstream_public_domain_notice='https://ebible.org/engwebp/copyright.htm',transform='Exact UTF-8 source blob retained. Pilot text copied without normalization.',annotation_method='AI-assisted manual curation against the actual supplied text; deterministic scoped literal mention expansion; not expert-certified.',annotation_license='Not selected; user decision required. No new license is imposed.',scope=dict(book='Genesis',chapters=list(range(1,51)),source_verse_count=len(V),entity_coverage='selected, non-exhaustive',mention_coverage='selected explicit names/phrases only; not all coreference',relation_coverage='selected direct relationships only'),counts=dict(entities=len(E),mentions=len(M),relations=len(R),uncertainties=len(uncertainties))))
# View-model export: no invented 3D positions; renderer should compute layout.
dump('data/graph-view.json',dict(nodes=[dict(id=e['id'],label=e['label'],type=e['type'],description=e['description'],description_evidence=e['description_evidence'],editorial_note=e['editorial_note'],verse_ids=list(dict.fromkeys(m['verse_id'] for m in M if m['entity_id']==e['id']))) for e in E],links=[dict(id=r['id'],source=r['subject'],target=r['object'],type=r['predicate'],evidence=r['evidence'],assertion=r['assertion'],note=r['note']) for r in R],warning='Navigation view only. Consult graph.json for assertion context and uncertainty. Positions are intentionally not provided.'))
print(json.dumps(dict(verses=len(V),entities=len(E),mentions=len(M),relations=len(R))))
if __name__=='__main__':pass
