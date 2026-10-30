import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from test_phase_quality import PhaseQuality
class GapResolution(PhaseQuality):
 # Reuse the valid-structure fixture, not the entire inherited test suite.
 def ledger(self,change):
  p=self.root/'quality/gap-resolution-ledger.json';x=json.loads(p.read_text());change(x);p.write_text(json.dumps(x))
 def test_gap_inventory_cannot_drop_record(self):
  self.ledger(lambda x:x['items'].pop());self.assertIn('gap_inventory_mismatch',self.codes())
 def test_accepted_omission_is_not_resolution(self):
  self.ledger(lambda x:x['items'][0].update(status='accepted_omission'))
  self.assertIn('gap_invalid_status',self.codes());self.assertFalse(self.runcheck()['gap_resolution']['complete'])
 def test_removed_gap_edge_is_caught_with_valid_counts(self):
  ledger=json.loads((self.root/'quality/gap-resolution-ledger.json').read_text());rid=ledger['items'][0]['added_relation_ids'][0]
  self.mutate(lambda g:g['relations'].__setitem__(slice(None),[r for r in g['relations'] if r['id']!=rid]))
  from validate import validate
  self.assertEqual(validate(self.root)['status'],'PASS');self.assertIn('gap_support_changed',self.codes())
 def test_gap_support_reassignment_under_same_id(self):
  ledger=json.loads((self.root/'quality/gap-resolution-ledger.json').read_text());rid=ledger['items'][0]['added_relation_ids'][0]
  self.mutate(lambda g:next(r for r in g['relations'] if r['id']==rid)['evidence'].append('GEN.1.1'))
  from validate import validate
  self.assertEqual(validate(self.root)['status'],'PASS');self.assertIn('gap_support_changed',self.codes());self.assertFalse(self.runcheck()['gap_resolution']['complete'])
 def test_unrelated_old_edge_is_not_repair(self):
  g=json.loads((self.root/'data/graph.json').read_text());old=next(r for r in g['relations'] if r['id']=='r:cain:killed:abel')
  from gap_check import record_hash
  def change(x):
   i=x['items'][0];i['added_relation_ids']=[old['id']];i['supporting_relations']=[{'id':old['id'],'expected_record':old}];i['evidence']=old['evidence'];i['review']['relation_hashes']={old['id']:record_hash(old)}
  self.ledger(change);self.assertIn('gap_support_not_new',self.codes())
 def test_frozen_inventory_report_tampering(self):
  p=self.root/'quality/baselines/v0.4.0-quality.json';x=json.loads(p.read_text());x['issues'].pop();p.write_text(json.dumps(x));self.assertIn('gap_baseline_report_changed',self.codes())
 def test_accepted_partial_still_blocks_commissioned_release(self):
  self.ledger(lambda x:x['items'][0].update(status='partial'))
  report=self.runcheck();finding=next(i for i in report['issues'] if i['code']=='gap_residual')
  (self.root/'quality/review-dispositions.json').write_text(json.dumps({finding['fingerprint']:{'decision':'accepted_omission','reason':'Test fixture acknowledges a residual but cannot claim completion.','reviewer':'test fixture','evidence':finding['context']['evidence']}}))
  from validate import validate
  self.assertEqual(validate(self.root)['status'],'PASS')
  import subprocess
  result=subprocess.run([sys.executable,str(self.root/'scripts/phase_check.py'),'--root',str(self.root),'--release'],capture_output=True)
  self.assertEqual(result.returncode,2);self.assertFalse(self.runcheck()['gap_resolution']['complete'])
 def test_review_hash_cannot_be_stale(self):
  self.ledger(lambda x:x['items'][0]['supporting_relations'][0]['expected_record'].update(note='edited after review'))
  self.assertIn('gap_review_stale',self.codes())
# Keep fixture inheritance without rerunning base tests in this class (they run in their own module).
for name in list(PhaseQuality.__dict__):
 if name.startswith('test_') and name not in GapResolution.__dict__:setattr(GapResolution,name,None)
del PhaseQuality
if __name__=='__main__':unittest.main()
