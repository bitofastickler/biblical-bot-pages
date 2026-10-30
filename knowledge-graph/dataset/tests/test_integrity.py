import unittest,json,sys,tempfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from validate import validate
class Integrity(unittest.TestCase):
 def test_all_integrity(self):self.assertEqual(validate()['status'],'PASS')
 def test_namesakes_and_collective(self):
  g=json.loads((ROOT/'data/graph.json').read_text()); m=g['mentions'];e={x['id'] for x in g['entities']}
  for a,b in [('enoch-cain','enoch-seth'),('lamech-cain','lamech-seth'),('nahor-serug','nahor-terah'),('haran-person','haran-place'),('canaan-genealogical','canaan-land')]:self.assertTrue('bg:'+a in e and 'bg:'+b in e)
  self.assertFalse(any(x['entity_id']=='bg:adam' and x['verse_id']=='GEN.5.2' for x in m))
  self.assertFalse(any(x['predicate']=='same_as' for x in g['relations']))
  self.assertFalse(any(x['entity_id']=='bg:cain' and x['verse_id']=='GEN.4.22' for x in m))
  h=[x for x in m if x['verse_id']=='GEN.11.31' and x['surface']=='Haran'];self.assertEqual({x['entity_id'] for x in h},{'bg:haran-person','bg:haran-place'})
 def test_rejects_bad_offsets(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);shutil.copytree(ROOT/'schema',p/'schema');shutil.copytree(ROOT/'data',p/'data');shutil.copytree(ROOT/'source',p/'source')
   f=p/'data/graph.json';g=json.loads(f.read_text());g['mentions'][0]['start']+=1;f.write_text(json.dumps(g))
   with self.assertRaises(AssertionError):validate(p)
 def test_rejects_schema_and_references(self):
  for mutation in ('version','resolution','entity','evidence','speaker'):
   with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as d:
    p=Path(d)
    for folder in ('data','source','schema'):shutil.copytree(ROOT/folder,p/folder)
    f=p/'data/graph.json';g=json.loads(f.read_text())
    if mutation=='version':g['schema_version']='nonsense'
    if mutation=='resolution':g['mentions'][0]['resolution']='unsupported'
    if mutation=='entity':g['mentions'][0]['entity_id']='bg:missing'
    if mutation=='evidence':g['relations'][0]['evidence']=['GEN.99.99']
    if mutation=='speaker':next(r for r in g['relations'] if r['assertion']['mode']=='speech')['assertion']['speaker']=None
    f.write_text(json.dumps(g))
    with self.assertRaises(AssertionError):validate(p)
 def test_description_coverage(self):
  g=json.loads((ROOT/'data/graph.json').read_text());d=json.loads((ROOT/'curation/entity-descriptions.json').read_text())
  for name in ('genesis12-25.json','genesis26-36.json','genesis37-50.json','gaps-early.json','gaps-later.json'):
   x=json.loads((ROOT/('curation/'+name)).read_text());d.update({'bg:'+i['key']:{k:i[k] for k in ('description','description_evidence')} for i in x['entities']});d.update(x['description_updates'])
  self.assertEqual(set(d),{e['id'] for e in g['entities']})
  for e in g['entities']:
   self.assertEqual(e['description'],d[e['id']]['description'])
   self.assertEqual(e['description_evidence'],d[e['id']]['description_evidence'])
   self.assertTrue(e['description'].strip() and e['description_evidence'])
 def test_rejects_description_corruption(self):
  for mutation in ('blank','evidence','view'):
   with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as d:
    p=Path(d)
    for folder in ('data','source','schema'):shutil.copytree(ROOT/folder,p/folder)
    f=p/'data/graph.json';g=json.loads(f.read_text())
    if mutation=='blank':g['entities'][0]['description']=' '
    if mutation=='evidence':g['entities'][0]['description_evidence']=['GEN.99.99']
    f.write_text(json.dumps(g))
    if mutation=='view':
     f=p/'data/graph-view.json';v=json.loads(f.read_text());v['nodes'][0]['description']='lost context';f.write_text(json.dumps(v))
    with self.assertRaises(AssertionError):validate(p)
 def test_abraham_expansion_boundaries(self):
  g=json.loads((ROOT/'data/graph.json').read_text());e={e['id']:e for e in g['entities']};m=g['mentions'];r=g['relations']
  self.assertTrue({'Abram','Abraham'}<=set(e['bg:abram']['aliases']))
  self.assertTrue({'Sarai','Sarah'}<=set(e['bg:sarai']['aliases']))
  self.assertFalse(any(x['entity_id']=='bg:ham' and x['verse_id']=='GEN.14.5' for x in m))
  self.assertFalse(any(x['entity_id']=='bg:nahor-terah' and x['verse_id']=='GEN.24.10' for x in m))
  self.assertFalse(any(x['entity_id']=='bg:havilah-land' and x['verse_id']=='GEN.25.18' for x in m))
  self.assertFalse(any(x['entity_id']=='bg:eliezer-damascus' and x['verse_id'].startswith('GEN.24.') for x in m))
  self.assertFalse(any(x['entity_id']=='bg:ishmael' and x['verse_id'].startswith('GEN.21.') for x in m))
  self.assertTrue(any(x['entity_id']=='bg:esau' and x['surface']=='Edom' and x['verse_id']=='GEN.25.30' for x in m))
  self.assertEqual(len([x for x in m if x['entity_id']=='bg:deity-god' and x['verse_id']=='GEN.22.14']),1)
  self.assertTrue({'bg:mamre-person','bg:mamre-place'}<=set(e))
  self.assertTrue(any(x['entity_id']=='bg:mamre-person' and x['verse_id']=='GEN.14.13' for x in m))
  self.assertTrue(any(x['entity_id']=='bg:mamre-place' and x['verse_id']=='GEN.13.18' for x in m))
  self.assertFalse(any(x['predicate']=='killed' and x['object']=='bg:isaac' for x in r))
  claim=next(x for x in r if x['predicate']=='claimed_half_sibling_of');self.assertEqual(claim['assertion']['speaker'],'bg:abram');self.assertEqual(claim['assertion']['mode'],'speech')
  self.assertFalse(any(x['predicate']=='sibling_of' and {x['subject'],x['object']}=={'bg:abram','bg:sarai'} for x in r))
 def test_all_description_evidence_scope(self):
  g=json.loads((ROOT/'data/graph.json').read_text());self.assertGreaterEqual(len(g['entities']),128)
  self.assertTrue(all(1<=int(v.split('.')[1])<=50 for e in g['entities'] for v in e['description_evidence']))
 def test_speech_is_not_status(self):
  g=json.loads((ROOT/'data/graph.json').read_text());r=next(r for r in g['relations'] if r['predicate']=='pronounced_curse_on')
  self.assertEqual(r['assertion']['speaker'],'bg:noah');self.assertEqual(r['object'],'bg:canaan-genealogical')
if __name__=='__main__':unittest.main()
