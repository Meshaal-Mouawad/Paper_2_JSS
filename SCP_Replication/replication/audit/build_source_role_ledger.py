from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
import csv,json,re
B=Path(__file__).resolve().parents[1]; E=B/'evaluation_r15/LEAP_Paper2_IST_R15_REVISION_PACKAGE/Independent_Evaluation_R15/independent_evaluation';T=B/'evidence';O=B/'audit'
def rows(p):return list(csv.DictReader(p.open(newline='')))
forms={r:{x['case_id']:x for x in rows(E/f'normalized/{r}_obligation_review_form_normalized.csv')} for r in ['R1','R2','R3']}
labelrows=rows(O/'independent_labels_and_checker.csv')
hits={x['dossier']:x['errors'] for x in json.loads((T/'primary/audit/lineage_defect_details_r3.json').read_text())}
classes={
'C01':('formula meaning; documentary comment role','Cross-field formula/source correspondence and conflict-comment classification exceed the two released patterns.'),
'C05':('metric meaning; executable-statement role','Business meaning versus eval/system execution is outside comment-executable and CAST-alias tests.'),
'C06':('documentary comment role; metric meaning','KPI-marker is excluded from executable-role prefixes; no semantic formula/business test.'),
'C09':('ownership correspondence; comment/executable role','Checker catches ABAP comments described as executable/alias; R1/R2 judge owner fields.'),
'C10':('documentary comment role','KPI-marker misclassification is outside executable-role prefixes.'),
'C12':('docstring/executable role','Checker catches docstring described as an output alias; R3 identifies the same alias error, while R1/R2 record Pass.'),
'C27':('cast-type/output-alias role','Checker catches FLOAT cast type described as output alias; R3 identifies the same discrepancy, while R1/R2 record Pass.'),
'C13':('documentary comment role; metric meaning','KPI-marker misclassification and export-procedure versus metric meaning exceed the patterns.'),
'C14':('documentary comment role; metric meaning','KPI-marker misclassification and length-versus-latency meaning exceed the patterns.'),
'C15':('documentary comment role','KPI-marker misclassification is outside executable-role prefixes.'),
'C16':('source-system correspondence; documentary comment role','Source-system meaning and documentary roles exceed the two patterns.'),
'C17':('formula provenance; documentary comment role','Declared versus inferred formula and descriptive/governance commentary exceed the patterns.'),
'C18':('formula/source correspondence; comment/executable role','Checker catches ABAP comment described as calculation; R1/R2 judge formula-variable correspondence.'),
'C19':('data-domain/owner correspondence; documentary comment role','Domain/ownership meaning and documentary roles exceed the patterns.'),
'C23':('metric/formula correspondence','Variable meaning versus metric title is outside syntactic patterns.'),
'C24':('documentary comment role; output/calculation role','Marker and executable print-as-calculation comparisons exceed comment-executable and CAST-alias patterns.'),
'C25':('documentary comment role','Audit-control comments as KPI markers exceed executable-role prefixes.'),
'C28':('documentary comment role; metric meaning','Unsigned-trace annotation as KPI marker and completeness meaning exceed the patterns.')}
ledger=[]
for row in labelrows:
 if row['criterion']!='source_role_accuracy' or not (row['majority']=='FAIL' or row['checker']=='FAIL'):continue
 cid=row['case'];doc=row['document'];p=T/'primary/artifact_28/dossiers'/doc
 xs=list(BeautifulSoup(p.read_text(),'html.parser').stripped_strings)
 pairs=[]
 for i,x in enumerate(xs[:-1]):
  if re.match(r'^\d+\s*\|',x) and re.match(r'^[A-Z][A-Za-z -]+:',xs[i+1]):
   pair={'source_excerpt':x,'published_description':xs[i+1]}
   if pair not in pairs:pairs.append(pair)
 entry={**row,'set_membership':'majority-Fail document' if row['majority']=='FAIL' else 'additional checker alert on majority-Pass document','observed_rationale_topics':classes[cid][0],'rule_coverage_explanation':classes[cid][1],'source_file':str(p.relative_to(B)),'source_description_pairs':pairs,'checker_hits':hits.get(doc,[]),'reviewer_rationales':{r:forms[r][cid]['evidence_note'] for r in forms},'exact_defect_match_assessment':'Checker error overlaps R3 rationale; R1/R2 majority Fail concerns distinct owner/formula mismatch. Document-level match only.' if cid in ['C09','C18'] else ('Checker error overlaps R3 rationale and directly inspected source; majority Pass does not make this an objectively false alert.' if cid in ['C12','C27'] else 'Checker has no alert; no exact-error detection claimed.')};ledger.append(entry)
(O/'source_role_failure_ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
assert len(ledger)==18
assert sum(x['majority']=='FAIL' for x in ledger)==16
assert sum(x['checker']=='FAIL' for x in ledger)==4
assert {x['case'] for x in ledger if x['majority']=='PASS'}=={'C12','C27'}
flat=[]
for x in ledger:
 flat.append({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in x.items()})
with (O/'source_role_failure_ledger.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
md=['# Source-role comparison ledger: majority-Fail documents and checker alerts','', 'This ledger contains 18 unique documents: all 16 majority-Fail documents and all four checker alerts. Two alerts (C09 and C18) belong to the majority-Fail set; the additional alerts C12 and C27 have majority-Pass labels. A matching document label does not establish that two reviewers identified the specific error flagged by the checker. Reviewer rationales are preserved in the JSON ledger alongside source text and generated descriptions. Classification below is the recovery auditor’s synthesis, not a new adjudicated reference.','', '| Case | Document | Votes R1/R2/R3 | Majority | Checker | Rationale topics | Why covered or missed |','|---|---|---|---|---|---|---|']
for x in ledger:md.append('| '+ ' | '.join([x['case'],x['document'],f"{x['R1']}/{x['R2']}/{x['R3']}",x['majority'],x['checker'],x['observed_rationale_topics'],x['rule_coverage_explanation']])+' |')
md += ['','## Matching labels at C09 and C18','', 'At C09, R1/R2 cite HSE-versus-Finance ownership; R3 cites comment-role errors caught by the checker. At C18, R1/R2 cite formula/variable mismatch; R3 cites the comment/executable-role error caught by the checker. Therefore the result is **2 of 16 majority-Fail documents flagged**, not two of sixteen adjudicated individual errors detected.','', '## Reference-discordant alerts','', 'C12 (Yield) and C27 (On-Spec) are checker Fail / majority Pass. R3 identifies the checker’s same concrete error: a Python docstring mapped to output alias `a`, and SQL cast type `FLOAT` mapped to output alias rather than `on_spec_percentage`. Source inspection supports these errors. The FP designation means discordance with the majority label; it does not establish that the alert is objectively false.','', '## Interpretation','', 'The reference criteria were applied broadly: some votes concern ownership, formula meaning, data domains, output meaning, or formula provenance. Those judgments should remain reported judgments until independently adjudicated at the defect level. Positive source-role kappa does not validate all underlying rationales.']
md += ['', '## Complete additional alert records', '', 'The following records retain the same fields as the majority-Fail cases in the JSON and CSV ledger.']
for entry in ledger:
 if entry['case'] in ['C12','C27']:
  md += ['', '### '+entry['case']+' — '+entry['document'], '', '```json', json.dumps(entry,indent=2,ensure_ascii=False), '```']
(O/'source_role_failure_ledger.md').write_text('\n'.join(md)+'\n')
print('Saved 18-document ledger: 16 majority-Fail documents, 4 checker alerts, 2 overlapping documents.')
