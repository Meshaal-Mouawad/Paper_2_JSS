#!/usr/bin/env python3
"""Independent reimplementation from preserved CSVs; never alters input files."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,re
BASE=Path(__file__).resolve().parents[1]
EV=BASE/'evaluation_r15/LEAP_Paper2_IST_R15_REVISION_PACKAGE/Independent_Evaluation_R15/independent_evaluation'
TECH=BASE/'evidence'; OUT=BASE/'audit'
def rows(p):return list(csv.DictReader(p.open(newline='')))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def writecsv(name,data):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
criteria=['source_role_accuracy','condition_disclosure','disagreement_preservation','review_authority_consistency']
forms={r:{x['case_id']:x for x in rows(EV/f'normalized/{r}_obligation_review_form_normalized.csv')} for r in ['R1','R2','R3']}
key={x['case_id']:x['original_dossier_filename'] for x in rows(EV/'analysis/case_mapping_key.csv')}
checker={x['dossier']:x for x in rows(EV/'checker/dossier_obligation_matrix.csv')}
label_rows=[]
for case,doc in key.items():
 for crit in criteria:
  labs=[forms[r][case][crit+'_PASS_FAIL_NA'] for r in forms]
  assert all(x in ['PASS','FAIL','NA'] for x in labs)
  label,cnt=Counter(labs).most_common(1)[0]
  c=checker[doc]['representation_disagreement_preservation' if crit=='disagreement_preservation' else crit].replace('N/A','NA')
  label_rows.append(dict(case=case,document=doc,criterion=crit,R1=labs[0],R2=labs[1],R3=labs[2],majority=label if cnt>=2 else 'UNRESOLVED',checker=c))
def agreement(data):
 n=len(data); counts=Counter(x for row in data for x in row)
 obs=sum(sum(a==b for a,b in [(row[0],row[1]),(row[0],row[2]),(row[1],row[2])])/3 for row in data)/n
 chance=sum((c/(3*n))**2 for c in counts.values())
 return dict(items=n,ratings=n*3,average_pair_agreement=obs,expected_chance_agreement=chance,fleiss_kappa=(obs-chance)/(1-chance),label_counts=dict(counts))
def matrix(data,ref='majority'):
 d=[x for x in data if x[ref]!='UNRESOLVED'];tp=sum(x['checker']=='FAIL' and x[ref]=='FAIL' for x in d);fp=sum(x['checker']=='FAIL' and x[ref]!='FAIL' for x in d);fn=sum(x['checker']!='FAIL' and x[ref]=='FAIL' for x in d);tn=sum(x['checker']!='FAIL' and x[ref]!='FAIL' for x in d)
 return dict(n=len(d),TP=tp,FP=fp,FN=fn,TN=tn,precision=tp/(tp+fp) if tp+fp else None,recall=tp/(tp+fn) if tp+fn else None,three_state_exact=sum(x['checker']==x[ref] for x in d),checker_na=sum(x['checker']=='NA' for x in d),reference_na=sum(x[ref]=='NA' for x in d))
summary={'provenance':'R15 normalized labels, with separate original-return reconciliation below','overall':agreement([[x[r] for r in forms] for x in label_rows]),'criteria':{},'unresolved':[x for x in label_rows if x['majority']=='UNRESOLVED']}
for crit in criteria:
 d=[x for x in label_rows if x['criterion']==crit]; applicable=[x for x in d if all(x[r]!='NA' for r in forms)]
 summary['criteria'][crit]={'agreement':agreement([[x[r] for r in forms] for x in d]),'common_applicability_agreement':agreement([[x[r] for r in forms] for x in applicable]),'matrix_fail_vs_nonfail':matrix(d)}
cond=[x for x in label_rows if x['criterion']=='condition_disclosure' and x['checker']!='NA']
summary['condition_eligible']={r:matrix(cond,r) for r in forms};summary['condition_eligible']['R1_R2_identical']=all(x['R1']==x['R2'] for x in cond)
reconcile=[]
for rid,n in [('R1',1),('R2',2),('R3',3)]:
 p=BASE/'reporting_correction/original_responses'/f'{rid}_obligation_review_form.csv'
 for row in rows(p):
  for crit in criteria:
   field=crit+'_PASS_FAIL_NA'; old=row[field].strip().upper(); new=forms[rid][row['case_id']][field]
   reconcile.append(dict(reviewer=rid,case=row['case_id'],criterion=crit,original=old,normalized=new,equal=old==new,source=str(p.relative_to(BASE))))
summary['original_reconciliation']={'checked_labels':len(reconcile),'equal':sum(x['equal'] for x in reconcile),'explicit_na':sum(x['original']=='NA' for x in reconcile),'original_identity_hashes':{x['reviewer']:digest(BASE/'reporting_correction/original_responses'/f"{x['reviewer']}_obligation_review_form.csv")==x['sha256'] for x in json.loads((BASE/'reporting_correction/ORIGINAL_RETURN_IDENTITIES.json').read_text())}}
summary['raw_derivatives']={r:sum(x[crit+'_PASS_FAIL_NA']=='' for x in rows(EV/f'raw/{r}_obligation_review_form.csv') for crit in criteria) for r in forms}
summary['normalized_na']={r:sum(x[crit+'_PASS_FAIL_NA']=='NA' for x in forms[r].values() for crit in criteria) for r in forms}
phasea={r:{x['case_id']:x['issue_found_yes_no'].upper() for x in rows(EV/f'raw/{r}_manual_review_form.csv')} for r in forms}
pa={case:sum(phasea[r][case]=='YES' for r in forms)>=2 for case in key};pb={case:sum(any(forms[r][case][c+'_PASS_FAIL_NA']=='FAIL' for c in criteria) for r in forms)>=2 for case in key}
summary['phases']={'A_majority':sum(pa.values()),'B_majority':sum(pb.values()),'added':[c for c in key if pb[c] and not pa[c]]}
# Independently inspect manifest bytes, rather than reading reported success.
manifest={}
for name,root in [('technical',TECH),('evaluation',EV)]:
 bad=[];num=0
 for line in (root/'SHA256SUMS.txt').read_text().splitlines():
  if not line.strip():continue
  h,rel=line.split(None,1); p=root/rel.strip().lstrip('*');num+=1
  if not p.exists() or digest(p)!=h:bad.append(rel)
 manifest[name]={'entries':num,'bad':bad}
summary['manifest_integrity']=manifest
# Build reproduction inventory from original source documents and archived filenames.
summary['technical_primary_documents']=len(list((TECH/'primary/artifact_28/dossiers').glob('*.html')))
summary['source_role_majority_fail_cases']=[x['case'] for x in label_rows if x['criterion']=='source_role_accuracy' and x['majority']=='FAIL']
summary['source_role_matching_fail_documents']=[x['case'] for x in label_rows if x['criterion']=='source_role_accuracy' and x['majority']==x['checker']=='FAIL']
summary['source_role_reference_discordant_alerts']=[x['case'] for x in label_rows if x['criterion']=='source_role_accuracy' and x['majority']=='PASS' and x['checker']=='FAIL']
writecsv('independent_labels_and_checker.csv',label_rows);writecsv('original_label_reconciliation.csv',reconcile)
(OUT/'independent_recompute.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
