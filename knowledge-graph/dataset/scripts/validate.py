#!/usr/bin/env python3
"""Dependency-free integrity checks. Not a substitute for semantic review."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TYPES={'person','place','deity','animal','object','genealogical_referent'}
PREDICATES={'parent_of','genealogical_parent_of','spouse_of','sibling_of','killed','resided_in','flows_through','rested_on','built','died_in','addressed','pronounced_curse_on'}
PREDICATES.update({'appointed_to_rule','interpreted_dream_for','provided_food_for','traveled_to','king_of', 'bound', 'servant_of', 'army_captain_of', 'buried', 'claimed_half_sibling_of', 'allied_with', 'covenant_with', 'rescued', 'promised_land_to', 'acquired', 'sold_birthright_to', 'buried_at'})
def check_schema(value,schema,path='$'):
 """Validate the exact subset of JSON Schema used by our bundled schema."""
 if 'const' in schema:assert value==schema['const'],path+' const'
 if 'enum' in schema:assert value in schema['enum'],path+' enum'
 types={'object':dict,'array':list,'string':str,'integer':int,'null':type(None)}
 if 'type' in schema:
  allowed=schema['type'] if isinstance(schema['type'],list) else [schema['type']]
  assert any(type(value) is types[t] for t in allowed),path+' type'
 if isinstance(value,dict) and 'properties' in schema:
  assert set(schema.get('required',[]))<=set(value),path+' required'
  if schema.get('additionalProperties') is False:assert set(value)<=set(schema['properties']),path+' extra property'
  for k,v in value.items():
   if k in schema['properties']:check_schema(v,schema['properties'][k],path+'.'+k)
 if isinstance(value,list) and 'items' in schema:
  assert len(value)>=schema.get('minItems',0),path+' minItems'
  for i,v in enumerate(value):check_schema(v,schema['items'],path+f'[{i}]')
 if 'minimum' in schema:assert value>=schema['minimum'],path+' minimum'
def validate(root=ROOT):
 if not __debug__:raise RuntimeError('Validation requires assertions enabled; do not use python -O.')
 def read(p):return json.loads((root/p).read_text())
 extra_predicates=read('schema/phase-predicates.json')
 g=read('data/graph.json');check_schema(g,read('schema/graph.schema.json'));vs=read('data/verses.json');p=read('data/provenance.json');raw=(root/'source/web.json').read_bytes();source=json.loads(raw)
 assert hashlib.sha256(raw).hexdigest()==p['sha256'],'Source SHA256 mismatch'
 assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==p['git_blob_sha1'],'Source Git blob mismatch'
 assert len(raw)==p['byte_length']
 V={v['id']:v for v in vs};E={e['id']:e for e in g['entities']}
 assert len(V)==len(vs)==p['scope']['source_verse_count']
 assert len(E)==len(g['entities'])
 for collection in ('mentions','relations','uncertainties'):
  ids=[i['id'] for i in g[collection]];assert len(ids)==len(set(ids)),f'Duplicate {collection} IDs'
 for e in E.values():
  assert e['description'].strip() and e['description_evidence'] and all(v in V for v in e['description_evidence'])
  assert e['type'] in TYPES and e['label'] and e['aliases'] and e['id'].startswith('bg:')
 src=next(b for b in source['books'] if b['id']=='genesis')['chapters']
 assert set(V)=={f'GEN.{c}.{v}' for c,vs0 in src.items() if int(c)<=50 for v in vs0},'Pilot verse set mismatch'
 for v in vs:
  assert v['id']==f"GEN.{v['chapter']}.{v['verse']}"
  assert v['text']==src[str(v['chapter'])][str(v['verse'])]
  assert v['source_id']==p['source_id']
 for m in g['mentions']:
  assert m['entity_id'] in E and m['verse_id'] in V
  t=V[m['verse_id']]['text'];assert 0<=m['start']<m['end']<=len(t)
  assert t[m['start']:m['end']]==m['surface'],'Invalid mention offset'
  assert m['surface'] in E[m['entity_id']]['aliases']
 for r in g['relations']:
  assert r['subject'] in E and r['object'] in E
  assert r['predicate'] in PREDICATES|set(extra_predicates) and r['evidence']
  st,ot=E[r['subject']]['type'],E[r['object']]['type']
  if r['predicate'] in extra_predicates:
   spec=extra_predicates[r['predicate']];assert st in spec['subject_types'] and ot in spec['object_types']
   if spec.get('required_mode'):assert r['assertion']['mode']==spec['required_mode']
   if spec.get('speaker_is_subject'):assert r['assertion']['speaker']==r['subject']
  if r['predicate'] in {'parent_of','spouse_of','killed'}:assert (st,ot)==('person','person')
  if r['predicate'] in {'resided_in','died_in'}:assert (st,ot)==('person','place')
  if r['predicate']=='flows_through':assert (st,ot)==('place','place')
  if r['predicate']=='rested_on':assert (st,ot)==('object','place')
  if r['predicate'] in {'king_of','buried_at','acquired','traveled_to'}:assert (st,ot)==('person','place')
  if r['predicate'] in {'allied_with','rescued','buried','claimed_half_sibling_of','bound','sold_birthright_to','servant_of','army_captain_of','appointed_to_rule','interpreted_dream_for','provided_food_for'}:assert (st,ot)==('person','person')
  if r['predicate']=='promised_land_to':assert (st,ot)==('deity','person') and r['assertion']['mode']=='speech' and r['assertion']['speaker']==r['subject']
  if r['predicate']=='claimed_half_sibling_of':assert r['assertion']['mode']=='speech' and r['assertion']['speaker']==r['subject']
  if r['predicate']=='covenant_with':assert st in {'person','deity'} and ot=='person'
  if r['predicate']=='built':assert (st,ot)==('person','object')
  if r['predicate']=='genealogical_parent_of':assert st in {'person','genealogical_referent'} and ot in {'person','genealogical_referent'}
  assert all(v in V for v in r['evidence'])
  assert r['assertion']['scope']=='in_text'
  assert r['assertion']['mode'] in {'speech','narration'}
  assert r['assertion']['speaker'] in E if r['assertion']['mode']=='speech' else r['assertion']['speaker'] is None
 for u in g['uncertainties']:assert u['issue'] and u['handling'] and all(v in V for v in u['verses'])
 for key in ('entities','mentions','relations','uncertainties'):assert p['counts'][key]==len(g[key])
 view=read('data/graph-view.json');assert {n['id'] for n in view['nodes']}==set(E)
 assert {l['id'] for l in view['links']}=={r['id'] for r in g['relations']}
 for n in view['nodes']:
  assert n['verse_ids']==list(dict.fromkeys(m['verse_id'] for m in g['mentions'] if m['entity_id']==n['id']))
  e=E[n['id']]
  for field in ('description','description_evidence','editorial_note'):assert n[field]==e[field], 'Projection lost description context'
 assert len(view['links'])==len(g['relations']) and len(view['nodes'])==len(E)
 byid={r['id']:r for r in g['relations']}
 for link in view['links']:
  r=byid[link['id']]
  assert (link['source'],link['target'],link['type'],link['evidence'],link['assertion'],link['note'])==(r['subject'],r['object'],r['predicate'],r['evidence'],r['assertion'],r['note'])
 return {'status':'PASS','verses':len(V),**p['counts']}
if __name__=='__main__':print(json.dumps(validate(),indent=2))
