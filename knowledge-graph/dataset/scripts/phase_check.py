#!/usr/bin/env python3
"""Reproducible, offline phase gate. Never invents or edits graph semantics."""
import argparse,collections,hashlib,json,subprocess,sys
from pathlib import Path
from validate import validate
from gap_check import check_gaps
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def analyze(root=ROOT,baseline=None):
 root=Path(root);issues=[]
 def add(code,severity,message,**context):
  item=dict(code=code,severity=severity,message=message,context=context)
  item['fingerprint']=hashlib.sha256(json.dumps(item,sort_keys=True).encode()).hexdigest()[:20];issues.append(item)
 def read(p):return json.loads((root/p).read_text())
 g=read('data/graph.json');verses=read('data/verses.json');p=read('data/provenance.json');ex=read('quality/expectations.json')
 try:validate(root)
 except Exception as e:add('integrity','error','Integrity validation failed: '+(str(e) or type(e).__name__))
 E={e['id']:e for e in g['entities']};V={v['id']:v for v in verses};R=g['relations'];M=g['mentions'];adj={k:set() for k in E};degree=collections.Counter()
 for r in R:
  a,b=r['subject'],r['object']
  if a in E and b in E:adj[a].add(b);adj[b].add(a);degree[a]+=1;degree[b]+=1
  else:add('dangling_relation','error','Relation endpoint is absent.',relation=r['id'],subject=a,object=b)
  for v in r['evidence']:
   if v not in V:add('bad_evidence','error','Relation evidence verse absent.',relation=r['id'],verse=v)
 for m in M:
  if m['entity_id'] not in E or m['verse_id'] not in V:add('dangling_mention','error','Mention target absent.',mention=m['id']);continue
  if V[m['verse_id']]['text'][m['start']:m['end']]!=m['surface']:add('bad_offset','error','Mention text does not match source slice.',mention=m['id'])
 active=skipped=0;major=set()
 for e in ex['entities']:
  if not all(v in V for v in e['evidence']):skipped+=1;continue
  active+=1;major.add(e['id'])
  if e['id'] not in E:add('major_character_missing','error' if e.get('required') else 'review','Source-anchored major character is missing.',expected=e);continue
  missing=set(e['aliases'])-set(E[e['id']]['aliases'])
  if missing:add('major_alias_missing','error' if e.get('required') else 'review','Expected explicit alias missing.',entity=e['id'],aliases=sorted(missing),evidence=e['evidence'])
  if not any(m['entity_id']==e['id'] and m['verse_id'] in e['evidence'] for m in M):add('major_anchor_unmentioned','review','Major character lacks a selected mention at this anchor.',expected=e)
 for e in ex['relations']:
  if not all(v in V for v in e['evidence']):skipped+=1;continue
  active+=1
  matches=[r for r in R if r['subject']==e['subject'] and r['object']==e['object'] and r['predicate']==e['predicate'] or e['predicate'] in {'spouse_of','sibling_of','allied_with','covenant_with'} and r['subject']==e['object'] and r['object']==e['subject'] and r['predicate']==e['predicate']]
  if not matches:add('key_relationship_missing','error' if e.get('required') else 'review','Explicit source relationship is absent from selected graph.',expected=e)
  elif not any((any(set(vs)<=set(r['evidence']) for vs in e['reviewed_evidence_sets']) if e.get('reviewed_evidence_sets') else bool(set(r['evidence'])&set(e['evidence']))) and r['assertion']['mode']==e['mode'] for r in matches):add('key_relationship_evidence','review','Relationship exists but needs evidence/attribution comparison with source anchor.',expected=e,actual=[r['id'] for r in matches])
 for expected in ex.get('forbidden_relations',[]):
  if all(v in V for v in expected['evidence']):
   for r in R:
    if all(r[k]==expected[k] for k in ('subject','predicate','object')) or expected['predicate'] in {'spouse_of','sibling_of','allied_with','covenant_with'} and r['predicate']==expected['predicate'] and (r['subject'],r['object'])==(expected['object'],expected['subject']):add('contradicted_source_guard','error','A curated source guard forbids this unqualified relationship.',expected=expected,relation=r['id'])
 for expected in ex.get('forbidden_mentions',[]):
  for m in M:
   if m['entity_id']!=expected['entity_id']:continue
   if 'verse_id' in expected and m['verse_id']!=expected['verse_id']:continue
   if 'chapter' in expected and int(m['verse_id'].split('.')[1])!=expected['chapter']:continue
   if 'surface' in expected and m['surface']!=expected['surface']:continue
   add('namesake_scope_guard','error','Mention violates a specifically reviewed namesake/collective scope guard.',mention=m['id'],expected=expected)
 components=[];left=set(E)
 while left:
  start=min(left);component=set();stack=[start]
  while stack:
   n=stack.pop()
   if n in component:continue
   component.add(n);stack.extend(adj[n]-component)
  left-=component;components.append(sorted(component))
 components.sort(key=lambda a:(-len(a),a))
 nodes=[]
 for k in sorted(E):
  e=E[k];mentions=[m for m in M if m['entity_id']==k]
  info=dict(id=k,label=e['label'],type=e['type'],degree=degree[k],neighbors=len(adj[k]),mentions=len(mentions),evidence=e['description_evidence'])
  nodes.append(info)
  if not mentions:add('no_mentions','review','Entity has no selected passage mentions.',entity=k,evidence=e['description_evidence'])
  if not adj[k]:add('isolated_node','review','No curated relationship connects this node. Isolation is not proof of error; inspect cited description and decide whether a supported link or an intentional omission is appropriate.',priority='high' if k in major else 'medium' if e['type']=='person' else 'low',**info)
 for comp in components[1:]:
  if len(comp)>1:add('separate_component','review','This connected subgraph is separate from the largest component; do not fabricate a bridge.',nodes=comp,labels=[E[k]['label'] for k in comp],major_characters=sorted(set(comp)&major),priority='high' if set(comp)&major else 'medium',size=len(comp))
 regression={'baseline':str(Path(baseline).relative_to(root)) if baseline and Path(baseline).is_relative_to(root) else str(baseline) if baseline else None,'status':'not_run'}
 if baseline:
  bp=Path(baseline)
  if not bp.exists():add('baseline_missing','error','Requested baseline file does not exist.',path=str(bp))
  else:
   manifest=bp.with_suffix('.provenance.json')
   if manifest.exists():
    bm=json.loads(manifest.read_text())
    if bm.get('source_sha256') and bm['source_sha256']!=sha(root/'source/web.json'):add('source_snapshot_changed','error','Source differs from the frozen phase baseline; an explicit source migration is required.')
    if bm['sha256']!=sha(bp):add('baseline_hash_mismatch','error','Frozen baseline differs from provenance hash.')
   else:add('baseline_unpinned','error','Baseline has no provenance manifest; verify its origin before approving regressions.',path=str(bp))
   old=json.loads(bp.read_text());regression.update(status='compared',sha256=sha(bp),changes={})
   for kind in ('entities','mentions','relations','uncertainties'):
    before={a['id']:a for a in old[kind]};after={a['id']:a for a in g[kind]}
    removed=sorted(set(before)-set(after));changed=[k for k in sorted(set(before)&set(after)) if before[k]!=after[k]]
    regression['changes'][kind]={'added':sorted(set(after)-set(before)),'removed':removed,'changed':changed}
    for k in removed:add('removed_'+kind,'review','Previously released record removed; review migration or correction.',id=k)
    for k in changed:
     a,b=before[k],after[k]
     if kind=='entities':
      if a['type']!=b['type'] or not set(a['aliases'])<=set(b['aliases']):add('entity_identity_changed','review','Existing type/alias identity changed.',id=k,before=a,after=b)
      else:add('entity_metadata_changed','review','Label/description/evidence or aliases expanded; review meaning despite stable ID.',id=k,before=a,after=b)
     else:add('changed_'+kind,'review','Previously released record changed; verify reassignment, evidence and attribution.',id=k,before=a,after=b)
 else:add('baseline_unavailable','review','No prior-phase baseline supplied: regression comparison was not run.')
 gap_resolution=check_gaps(root,g,V,add)
 dispositions=read('quality/review-dispositions.json') if (root/'quality/review-dispositions.json').exists() else {}
 for i in issues:
  d=dispositions.get(i['fingerprint'])
  if i['severity']=='review' and d and d.get('decision') in {'accepted_omission','accepted_after_source_review'} and isinstance(d.get('reason'),str) and d['reason'].strip() and isinstance(d.get('reviewer'),str) and d['reviewer'].strip() and isinstance(d.get('evidence'),list) and d['evidence'] and all(v in V for v in d['evidence']):
   i['disposition']=d
 stale=set(dispositions)-{i['fingerprint'] for i in issues}
 for fingerprint in sorted(stale):add('stale_disposition','review','Prior approval no longer matches an active finding; remove or re-review it.',fingerprint=fingerprint)
 unresolved=[i for i in issues if i['severity']=='review' and 'disposition' not in i];errors=[i for i in issues if i['severity']=='error']
 return dict(report_version=1,dataset_version=p.get('dataset_version',g['schema_version']),dataset_sha256=sha(root/'data/graph.json'),source_sha256=p['sha256'],dispositions_sha256=sha(root/'quality/review-dispositions.json') if (root/'quality/review-dispositions.json').exists() else None,expectations_sha256=sha(root/'quality/expectations.json'),scope=p['scope'],status='FAIL' if errors else 'REVIEW_NEEDED' if unresolved or gap_resolution.get('total') and not gap_resolution.get('complete') else 'PASS',counts=dict(entities=len(E),mentions=len(M),relations=len(R),verses=len(V),components=len(components),isolated=sum(not adj[k] for k in E),errors=len(errors),review_items=sum(i['severity']=='review' for i in issues),unresolved_review=len(unresolved),accepted_review=sum('disposition' in i for i in issues)),gap_resolution=gap_resolution,expectations=dict(active=active,out_of_scope=skipped,method=ex['method']),components=components,nodes=nodes,regression=regression,issues=issues,limitations=['Checks validate structure and a small editorial checklist, not complete recall, historical truth or semantic precision.','Evidence existence and anchor overlap do not prove every claim; source reading remains required.','Only relationship edges count toward connectivity; shared verses are not fabricated edges.'])
def write_reports(report,root):
 out=Path(root)/'reports';out.mkdir(exist_ok=True)
 (out/'phase-quality.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 lines=['# Phase quality report', '', '**'+report['status']+'** — dataset '+report['dataset_version'],'', 'Graph SHA256: `'+report['dataset_sha256']+'`','', '## Summary','']+[f'- {k.replace("_"," ")}: {v}' for k,v in report['counts'].items()]
 lines+=['','## Acceptance policy','','Integrity errors block release. Unresolved review findings require source review and documented decisions before release. Isolation is a review item, not an automatic error. Do not create links to improve a score.','','## Findings','']
 labels={n['id']:n['label'] for n in report['nodes']}
 for i in report['issues']:
  c=i['context'];d=i.get('disposition');state='ACCEPTED AFTER REVIEW' if d else 'PENDING' if i['severity']=='review' else 'BLOCKER'
  lines+=['### '+i['code'].replace('_',' ')+' · '+state,i['message'],'']
  target=c.get('id') or c.get('entity') or c.get('relation') or c.get('mention')
  if target:lines+=['**Item:** '+labels.get(target,target)]
  expected=c.get('expected',{})
  if expected.get('subject'):lines+=['**Expected:** '+labels.get(expected['subject'],expected['subject'])+' → '+expected['predicate'].replace('_',' ')+' → '+labels.get(expected['object'],expected['object'])]
  if expected.get('id'):lines+=['**Expected character:** '+labels.get(expected['id'],expected['id'])]
  if c.get('nodes'):lines+=['**Members:** '+', '.join(labels.get(k,k) for k in c['nodes'])]
  if 'degree' in c:lines+=['**Connections / mentions:** '+str(c['degree'])+' / '+str(c['mentions'])]
  if c.get('priority'):lines+=['**Priority:** '+c['priority']]
  evidence=c.get('evidence') or expected.get('evidence') or []
  if evidence:lines+=['**Source passages:** '+', '.join(evidence)]
  if d:lines+=['**Decision:** '+d['reason'], '**Reviewed by:** '+d['reviewer'], '**Review passages:** '+', '.join(d['evidence'])]
  lines+=['Finding ID: `'+i['fingerprint']+'`','']
 gap=report.get('gap_resolution',{})
 if gap.get('total'):
  lines+=['## Commissioned gap accounting','',f"{gap['resolved']} resolved / {gap['total']} original findings; {gap['partial']} partial; {gap['residual']} residual; {gap['unreviewed']} unreviewed.",'','Full source-by-source closure records: `gap-resolution.md` and `../quality/gap-resolution-ledger.json`.','']
 if gap.get('total') and (Path(root)/'quality/gap-resolution-ledger.json').exists():
  ledger=json.loads((Path(root)/'quality/gap-resolution-ledger.json').read_text())
  detail=['# Documented Genesis gap repairs','',f"{gap['resolved']} of {gap['total']} prior connection findings resolved; {gap['partial']} partial; {gap['residual']} residual.",'','This is closure of the listed connection tasks, not exhaustive Genesis extraction or resolution of the retained interpretive uncertainties.','']
  for item in ledger['items']:
   names=', '.join(labels.get(k,k) for k in item['entities'])
   detail+=['## '+names+' — '+item['status'],'','**Before:** '+item['original_issue'].get('disposition',{}).get('reason',item['original_issue']['message']),'','**Now:** '+item['reason'],'']
   for support in item['supporting_relations']:
    r=support['expected_record'];assertion=r['assertion'];qualifier=' [attributed speech by '+labels.get(assertion['speaker'],assertion['speaker'])+']' if assertion['mode']=='speech' else ' [narrated action/relationship]'
    detail+=['- '+labels.get(r['subject'],r['subject'])+' → **'+r['predicate'].replace('_',' ')+'** → '+labels.get(r['object'],r['object'])+qualifier+'; '+', '.join(r['evidence'])+'. '+r['note']]
   detail+=['','**Review:** '+item['review']['status']+' — '+item['review']['reviewer'],'','Original finding: `'+item['original_issue_fingerprint']+'`','']
  (out/'gap-resolution.md').write_text('\n'.join(detail)+'\n')
 lines+=['Full old/new record details and graph metrics are in `phase-quality.json`.','']
 lines+=['## Limits','']+['- '+s for s in report['limitations']]
 (out/'phase-quality.md').write_text('\n'.join(lines)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=ROOT);ap.add_argument('--baseline',type=Path);ap.add_argument('--build',action='store_true');ap.add_argument('--release',action='store_true');args=ap.parse_args()
 # Fail closed: a failed/incomplete run must never leave a previous PASS artifact behind.
 failure=dict(report_version=1,dataset_version='unverified',dataset_sha256='unverified',source_sha256='unverified',expectations_sha256='unverified',dispositions_sha256=None,scope={},status='FAIL',counts={'errors':1,'unresolved_review':0},expectations={},components=[],nodes=[],regression={'status':'not_run'},issues=[dict(code='phase_run_incomplete',severity='error',message='The current phase command has not completed successfully; release is blocked.',context={},fingerprint='phase-run-incomplete')],limitations=['This failure report does not make claims about unread or unchecked dataset counts.'])
 write_reports(failure,args.root)
 if args.build:
  for command in ([sys.executable,str(args.root/'scripts/build.py')],[sys.executable,'-m','unittest','discover','-s',str(args.root/'tests'),'-v']):
   r=subprocess.run(command,cwd=args.root)
   if r.returncode:
    failure['issues'][0]['message']='Build/test subprocess failed with exit '+str(r.returncode)
    failure['issues'][0]['context']={'command':command};write_reports(failure,args.root);return r.returncode
 baseline=args.baseline or args.root/'quality/baselines/v0.4.0.json'
 try:report=analyze(args.root,baseline)
 except Exception as e:
  failure['issues'][0]['message']='Phase analysis failed: '+type(e).__name__+': '+str(e);write_reports(failure,args.root);print(failure['issues'][0]['message']);return 1
 write_reports(report,args.root)
 print(json.dumps({'status':report['status'],**report['counts'],'report':'reports/phase-quality.md'},indent=2))
 return 1 if report['counts']['errors'] else 2 if args.release and (report['counts']['unresolved_review'] or report.get('gap_resolution',{}).get('total') and (not report['gap_resolution'].get('complete') or report['gap_resolution'].get('status')!='COMPLETE')) else 0
if __name__=='__main__':sys.exit(main())
