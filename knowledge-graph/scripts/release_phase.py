#!/usr/bin/env python3
"""Build and validate vendored dataset before publishing any runtime data.
Run with Sites source helper commands: [["python3", "scripts/release_phase.py"]].
Nonzero gate/test results propagate: the source helper must not commit/push/package.
"""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATASET=ROOT/'dataset'
def main():
 gate=DATASET/'scripts/phase_check.py'
 if not gate.is_file(): raise SystemExit('Release blocked: missing full dataset source/gate')
 report_path=DATASET/'reports/phase-quality.json'
 report_path.unlink(missing_ok=True)
 subprocess.run([sys.executable,str(gate),'--build','--release'],cwd=DATASET,check=True)
 report=json.loads(report_path.read_text())
 provenance=json.loads((DATASET/'data/provenance.json').read_text())
 expectations_digest=hashlib.sha256((DATASET/'quality/expectations.json').read_bytes()).hexdigest()
 dispositions_digest=hashlib.sha256((DATASET/'quality/review-dispositions.json').read_bytes()).hexdigest()
 ledger_digest=hashlib.sha256((DATASET/'quality/gap-resolution-ledger.json').read_bytes()).hexdigest()
 digest=hashlib.sha256((DATASET/'data/graph.json').read_bytes()).hexdigest()
 if report['status']!='PASS' or report['counts']['errors'] or report['counts']['unresolved_review'] or report['dataset_sha256']!=digest or report['expectations_sha256']!=expectations_digest or report['dispositions_sha256']!=dispositions_digest or report['dataset_version']!=provenance['dataset_version'] or report.get('gap_resolution',{}).get('ledger_sha256')!=ledger_digest or not report.get('gap_resolution',{}).get('complete'):
  raise SystemExit('Release blocked: gate did not pass or report is stale')
 # Reports can include checkout-local paths; refresh the vendored checksum inventory after rebuilding.
 inventory=[p for p in DATASET.rglob('*') if p.is_file() and p.name!='CHECKSUMS.sha256' and '__pycache__' not in p.parts and p.suffix!='.pyc']
 (DATASET/'CHECKSUMS.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(DATASET).as_posix()+'\n' for p in sorted(inventory)))
 # No runtime asset changes occur until tests and release gate have succeeded.
 for name in ('graph.json','graph-view.json','verses.json','provenance.json'):
  shutil.copy2(DATASET/'data'/name,ROOT/'dist'/name)
 for name in ('phase-quality.json','phase-quality.md'):
  shutil.copy2(DATASET/'reports'/name,ROOT/'dist'/name)
 shutil.copy2(DATASET/'quality/gap-resolution-ledger.json',ROOT/'dist/gap-resolution-ledger.json')
 shutil.copy2(DATASET/'reports/gap-resolution.md',ROOT/'dist/gap-resolution.md')
 shutil.copy2(DATASET/'quality/expectations.json',ROOT/'dist/expectations.json')
 subprocess.run(['node','--check',str(ROOT/'dist/app.js')],check=True)
 subprocess.run(['node','--check',str(ROOT/'dist/quality.js')],check=True)
 print(json.dumps({'release_gate':'PASS','dataset_sha256':digest,'counts':report['counts']}))
if __name__=='__main__':
 subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'tests'),'-v'],cwd=ROOT,check=True)
 main()
