import hashlib,importlib.util,json,subprocess,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
SPEC=importlib.util.spec_from_file_location('release_phase',Path(__file__).resolve().parents[1]/'scripts/release_phase.py');release=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(release)
class ReleaseBoundary(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name);self.ds=self.root/'dataset'
  for d in ['scripts','data','reports','quality']:(self.ds/d).mkdir(parents=True)
  (self.root/'dist').mkdir();(self.ds/'scripts/phase_check.py').write_text('# fixture')
  for f in ['graph.json','graph-view.json','verses.json','provenance.json']:(self.ds/'data'/f).write_text('{"dataset_version":"0.4.0"}')
  (self.ds/'quality/expectations.json').write_text('{}');(self.ds/'quality/review-dispositions.json').write_text('{}');(self.ds/'reports/phase-quality.md').write_text('report');(self.ds/'reports/gap-resolution.md').write_text('gaps');(self.ds/'quality/gap-resolution-ledger.json').write_text('{}')
  self.report={'status':'PASS','gap_resolution':{'complete':True,'ledger_sha256':hashlib.sha256(b'{}').hexdigest()},'dataset_version':'0.4.0','dataset_sha256':hashlib.sha256((self.ds/'data/graph.json').read_bytes()).hexdigest(),'expectations_sha256':hashlib.sha256(b'{}').hexdigest(),'dispositions_sha256':hashlib.sha256(b'{}').hexdigest(),'counts':{'errors':0,'unresolved_review':0}}
 def run_case(self,change=None,exit_failure=False,write=True):
  if change:change(self.report)
  def command(cmd,**kwargs):
   if cmd[0]==release.sys.executable:
    self.assertTrue(kwargs['check'])
    if exit_failure:raise subprocess.CalledProcessError(1,cmd)
    if write:(self.ds/'reports/phase-quality.json').write_text(json.dumps(self.report))
   return subprocess.CompletedProcess(cmd,0)
  with patch.object(release,'ROOT',self.root),patch.object(release,'DATASET',self.ds),patch.object(release.subprocess,'run',side_effect=command):release.main()
 def blocked(self,**kwargs):
  with self.assertRaises((SystemExit,subprocess.CalledProcessError,FileNotFoundError)):self.run_case(**kwargs)
  self.assertEqual(list((self.root/'dist').iterdir()),[])
 def test_subprocess_nonzero_blocks(self):self.blocked(exit_failure=True)
 def test_stale_report_removed(self):
  (self.ds/'reports/phase-quality.json').write_text(json.dumps(self.report));self.blocked(write=False)
 def test_hard_error_blocks(self):self.blocked(change=lambda r:r['counts'].update(errors=1))
 def test_unresolved_review_blocks(self):self.blocked(change=lambda r:r['counts'].update(unresolved_review=1))
 def test_stale_graph_blocks(self):self.blocked(change=lambda r:r.update(dataset_sha256='stale'))
 def test_stale_expectations_blocks(self):self.blocked(change=lambda r:r.update(expectations_sha256='stale'))
 def test_stale_dispositions_blocks(self):self.blocked(change=lambda r:r.update(dispositions_sha256='stale'))
 def test_stale_ledger_blocks(self):self.blocked(change=lambda r:r['gap_resolution'].update(ledger_sha256='stale'))
 def test_incomplete_gap_review_blocks(self):self.blocked(change=lambda r:r['gap_resolution'].update(complete=False))
 def test_wrong_phase_blocks(self):self.blocked(change=lambda r:r.update(dataset_version='0.3.0'))
 def test_pass_copies_after_gate(self):
  self.run_case();self.assertTrue((self.root/'dist/graph.json').is_file());self.assertTrue((self.root/'dist/phase-quality.json').is_file())
if __name__=='__main__':unittest.main()
