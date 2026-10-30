"""Hard accounting for the explicitly commissioned v0.4 coverage-gap repair."""
import hashlib,json
from pathlib import Path
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def record_hash(record):return hashlib.sha256(json.dumps(record,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def check_gaps(root,graph,verses,add):
 emit=add;failures=[]
 def add(code,severity,message,**context):
  if severity=='error':failures.append(code)
  emit(code,severity,message,**context)
 root=Path(root);path=root/'quality/gap-resolution-ledger.json'
 summary={'status':'NOT_APPLICABLE','total':0,'resolved':0,'partial':0,'residual':0,'unreviewed':0,'ledger_sha256':None}
 if tuple(map(int,graph['schema_version'].split('.'))) < (0,5,0):return summary
 if not path.exists():add('gap_ledger_missing','error','Commissioned gap resolution requires its source-reviewed ledger.');summary['status']='FAIL';return summary
 ledger=json.loads(path.read_text());summary['ledger_sha256']=sha(path)
 basepath=root/'quality/baselines/v0.4.0.json';reportpath=root/'quality/baselines/v0.4.0-quality.json';manifest=json.loads((root/'quality/baselines/v0.4.0.provenance.json').read_text())
 if sha(basepath)!=manifest['sha256'] or sha(basepath)!=ledger['baseline_graph_sha256']:add('gap_baseline_graph_changed','error','Gap ledger baseline graph differs from canonical pinned v0.4.')
 if sha(reportpath)!=manifest['quality_report_sha256'] or sha(reportpath)!=ledger['baseline_report_sha256']:add('gap_baseline_report_changed','error','Original gap inventory differs from the frozen v0.4 quality report.')
 prior=json.loads(reportpath.read_text());old=json.loads(basepath.read_text());oldrels={r['id']:r for r in old['relations']};rels={r['id']:r for r in graph['relations']}
 originals={i['fingerprint']:i for i in prior['issues'] if i['code'] in {'isolated_node','separate_component'}}
 items=ledger.get('items',[]);ids=[i['original_issue_fingerprint'] for i in items]
 if len(originals)!=43 or len(ids)!=len(set(ids)) or set(ids)!=set(originals):add('gap_inventory_mismatch','error','Ledger must account exactly once for all 43 commissioned coverage findings; metadata changes are not coverage gaps.',missing=sorted(set(originals)-set(ids)),unexpected=sorted(set(ids)-set(originals)),records=len(ids))
 summary['total']=len(originals)
 for item in items:
  key=item['original_issue_fingerprint'];original=originals.get(key)
  if original is None:continue
  targets=set(original['context'].get('nodes',[original['context'].get('id')]))
  if set(item.get('entities',[]))!=targets:add('gap_target_mismatch','error','Ledger targets no longer match the original finding.',fingerprint=key)
  status=item.get('status')
  if status not in {'resolved','partial','residual'}:add('gap_invalid_status','error','Gap status must explicitly distinguish resolved, partial and residual.',fingerprint=key);continue
  summary[status]+=1
  review=item.get('review',{})
  reviewed=review.get('status')=='approved' and isinstance(review.get('reviewer'),str) and bool(review['reviewer'].strip())
  if not reviewed:summary['unreviewed']+=1;add('gap_unreviewed','error','Gap closure has not received explicit independent source review.',fingerprint=key)
  if not item.get('reason','').strip() or not item.get('evidence') or not all(v in verses for v in item['evidence']):add('gap_rationale_invalid','error','Each resolution/residual needs a specific rationale and valid source evidence.',fingerprint=key)
  supports=item.get('supporting_relations',[]);rids=[r['id'] for r in supports]
  if len(rids)!=len(set(rids)) or rids!=item.get('added_relation_ids',[]):add('gap_support_inventory','error','Gap edge ID list and reviewed snapshots must agree exactly.',fingerprint=key)
  external=False
  for support in supports:
   rid=support['id'];expected=support.get('expected_record');actual=rels.get(rid)
   if actual is None or actual!=expected:add('gap_support_changed','error','A gap-closing edge is missing or changed relative to its source-reviewed record.',fingerprint=key,relation=rid)
   if expected is None:continue
   if review.get('relation_hashes',{}).get(rid)!=record_hash(expected):add('gap_review_stale','error','Reviewed edge fingerprint no longer matches the ledger claim.',fingerprint=key,relation=rid)
   if oldrels.get(rid)==expected:add('gap_support_not_new','error','An unchanged pre-existing edge cannot count as a newly filled connection.',fingerprint=key,relation=rid)
   endpoints={expected['subject'],expected['object']}
   if endpoints & targets and endpoints-targets:external=True
   if not set(expected['evidence'])<=set(item['evidence']):add('gap_support_evidence','error','Ledger evidence must include the supporting edge evidence.',fingerprint=key,relation=rid)
  if status=='resolved' and (not supports or not external):add('gap_no_supported_bridge','error','Resolved connection gap requires an actual new/changed supported edge linking an original target outside its old component.',fingerprint=key)
  if status!='resolved':add('gap_residual','review','Commissioned gap is not fully closed; a precise remaining ambiguity must stay visible, not be counted as fixed.',fingerprint=key,status=status,reason=item.get('reason'),evidence=item.get('evidence'))
 summary['complete']=summary['resolved']==summary['total'] and not summary['unreviewed'] and not failures
 summary['status']='FAIL' if failures else 'COMPLETE' if summary['complete'] else 'INCOMPLETE'
 return summary
