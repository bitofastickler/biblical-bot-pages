import copy,json,sys,tempfile,unittest,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from phase_check import analyze,write_reports
from validate import validate
class PhaseQuality(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  for name in ('data','source','schema','quality','scripts'):shutil.copytree(ROOT/name,self.root/name,ignore=shutil.ignore_patterns('__pycache__'))
 def tearDown(self):self.tmp.cleanup()
 def runcheck(self):return analyze(self.root,self.root/'quality/baselines/v0.4.0.json')
 def mutate(self,fn):
  p=self.root/'data/graph.json';g=json.loads(p.read_text());fn(g);p.write_text(json.dumps(g))
  # Recompute legitimate projection/count metadata so semantic mutations cannot hide behind structural failures.
  v={'nodes':[dict(id=e['id'],label=e['label'],type=e['type'],description=e['description'],description_evidence=e['description_evidence'],editorial_note=e['editorial_note'],verse_ids=list(dict.fromkeys(m['verse_id'] for m in g['mentions'] if m['entity_id']==e['id']))) for e in g['entities']], 'links':[dict(id=r['id'],source=r['subject'],target=r['object'],type=r['predicate'],evidence=r['evidence'],assertion=r['assertion'],note=r['note']) for r in g['relations']]}
  (self.root/'data/graph-view.json').write_text(json.dumps(v))
  p=self.root/'data/provenance.json';prov=json.loads(p.read_text())
  for k in ('entities','mentions','relations','uncertainties'):prov['counts'][k]=len(g[k])
  p.write_text(json.dumps(prov))
 def codes(self):return {i['code'] for i in self.runcheck()['issues']}
 def test_missing_major_and_alias_are_not_silently_passed(self):
  def change(g):
   g['entities']=[e for e in g['entities'] if e['id']!='bg:noah'];g['mentions']=[m for m in g['mentions'] if m['entity_id']!='bg:noah'];g['relations']=[r for r in g['relations'] if 'bg:noah' not in (r['subject'],r['object'],r['assertion']['speaker'])]
  self.mutate(change);self.assertEqual(validate(self.root)['status'],'PASS')
  self.assertTrue(any(i['code']=='major_character_missing' and i['severity']=='error' for i in self.runcheck()['issues']))
 def test_missing_rename_alias(self):
  def change(g):
   next(e for e in g['entities'] if e['id']=='bg:abram')['aliases'].remove('Abraham');g['mentions']=[m for m in g['mentions'] if not(m['entity_id']=='bg:abram' and m['surface']=='Abraham')]
  self.mutate(change);self.assertEqual(validate(self.root)['status'],'PASS')
  self.assertIn('major_alias_missing',self.codes())
 def test_missing_key_edge(self):
  self.mutate(lambda g:g['relations'].__setitem__(slice(None),[r for r in g['relations'] if not(r['subject']=='bg:abram' and r['object']=='bg:isaac' and r['predicate']=='parent_of')]))
  self.assertEqual(validate(self.root)['status'],'PASS')
  self.assertTrue(any(i['code']=='key_relationship_missing' and i['severity']=='error' for i in self.runcheck()['issues']))
 def test_reassigned_mention(self):
  self.mutate(lambda g:next(m for m in g['mentions'] if m['entity_id']=='bg:enoch-cain').update(entity_id='bg:enoch-seth'))
  self.assertEqual(validate(self.root)['status'],'PASS')
  self.assertIn('changed_mentions',self.codes())
 def test_source_and_dangling_evidence(self):
  p=self.root/'source/web.json';p.write_bytes(p.read_bytes()+b' ')
  self.mutate(lambda g:g['relations'][0]['evidence'].append('GEN.99.1'))
  self.assertTrue({'source_snapshot_changed','bad_evidence','integrity'}<=self.codes())
 def test_namesake_guard(self):
  t=next(v['text'] for v in json.loads((self.root/'data/verses.json').read_text()) if v['id']=='GEN.14.5');start=t.index('Ham')
  self.mutate(lambda g:g['mentions'].append(dict(id='mutation:ham',entity_id='bg:ham',verse_id='GEN.14.5',start=start,end=start+3,surface='Ham',resolution='curated_name_scope')))
  self.assertEqual(validate(self.root)['status'],'PASS')
  self.assertIn('namesake_scope_guard',self.codes())
 def test_false_killing_guard(self):
  self.mutate(lambda g:g['relations'].append(dict(id='mutation:kill',subject='bg:abram',predicate='killed',object='bg:isaac',evidence=['GEN.22.10'],assertion={'scope':'in_text','mode':'narration','speaker':None},note='')))
  self.assertIn('contradicted_source_guard',self.codes())
 def test_isolation_is_review_not_synthetic_repair(self):
  self.mutate(lambda g:g['relations'].__setitem__(slice(None),[r for r in g['relations'] if 'bg:noah' not in (r['subject'],r['object'])]))
  findings=[i for i in self.runcheck()['issues'] if i['code']=='isolated_node' and i['context']['id']=='bg:noah'];self.assertEqual(len(findings),1);self.assertEqual(findings[0]['severity'],'review');self.assertEqual(findings[0]['context']['priority'],'high')
 def test_disconnected_major_group_is_reviewed_even_with_edges(self):
  self.mutate(lambda g:g['relations'].__setitem__(slice(None),[r for r in g['relations'] if not ((r['subject'],r['predicate'],r['object']) in {('bg:adam','spouse_of','bg:eve'),('bg:eve','parent_of','bg:seth')})]))
  self.assertEqual(validate(self.root)['status'],'PASS')
  self.assertTrue(any(i['code']=='separate_component' and 'bg:eve' in i['context']['nodes'] and i['context']['priority']=='high' for i in self.runcheck()['issues']))
 def test_speech_cannot_become_narrated_kinship(self):
  def change(g):
   r=next(r for r in g['relations'] if r['predicate']=='claimed_half_sibling_of');r['assertion']={'scope':'in_text','mode':'narration','speaker':None}
  self.mutate(change);self.assertIn('integrity',self.codes())
 def test_reversed_sibling_guard(self):
  self.mutate(lambda g:g['relations'].append(dict(id='mutation:reverse-sibling',subject='bg:sarai',predicate='sibling_of',object='bg:abram',evidence=['GEN.20.12'],assertion={'scope':'in_text','mode':'narration','speaker':None},note='')))
  self.assertEqual(validate(self.root)['status'],'PASS');self.assertIn('contradicted_source_guard',self.codes())
 def test_empty_disposition_cannot_hide_finding(self):
  self.mutate(lambda g:g['mentions'].__setitem__(slice(None),[m for m in g['mentions'] if not (m['entity_id']=='bg:noah' and m['verse_id']=='GEN.5.29')]))
  r=self.runcheck();i=next(i for i in r['issues'] if i['severity']=='review')
  (self.root/'quality/review-dispositions.json').write_text(json.dumps({i['fingerprint']:{'decision':'accepted_omission','reason':'','reviewer':'test','evidence':['GEN.1.1']}}))
  self.assertNotIn('disposition',next(a for a in self.runcheck()['issues'] if a['fingerprint']==i['fingerprint']))
 def test_failed_build_invalidates_old_pass_report(self):
  out=self.root/'reports';out.mkdir(exist_ok=True);(out/'phase-quality.json').write_text('{"status":"PASS"}')
  (self.root/'scripts/build.py').write_text('raise SystemExit(1)')
  r=subprocess.run([sys.executable,str(self.root/'scripts/phase_check.py'),'--root',str(self.root),'--build','--release'],capture_output=True)
  self.assertEqual(r.returncode,1);report=json.loads((out/'phase-quality.json').read_text());self.assertEqual(report['status'],'FAIL');self.assertEqual(report['issues'][0]['code'],'phase_run_incomplete')
 def test_release_refuses_unreviewed_findings(self):
  (self.root/'quality/review-dispositions.json').write_text('{}')
  self.mutate(lambda g:g['mentions'].__setitem__(slice(None),[m for m in g['mentions'] if not (m['entity_id']=='bg:noah' and m['verse_id']=='GEN.5.29')]))
  self.assertEqual(validate(self.root)['status'],'PASS')
  result=subprocess.run([sys.executable,str(self.root/'scripts/phase_check.py'),'--root',str(self.root),'--release'],capture_output=True)
  self.assertEqual(result.returncode,2)
if __name__=='__main__':unittest.main()
