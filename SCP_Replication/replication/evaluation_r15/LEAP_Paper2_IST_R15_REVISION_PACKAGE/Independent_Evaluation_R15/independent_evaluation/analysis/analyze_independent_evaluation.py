#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'raw'
NORM = ROOT / 'normalized'
AN = ROOT / 'analysis'
CHECKER = ROOT / 'checker' / 'dossier_obligation_matrix.csv'
KEY = AN / 'case_mapping_key.csv'

OB_COLS = {
    'source_role_accuracy_PASS_FAIL_NA':'source_role_accuracy',
    'condition_disclosure_PASS_FAIL_NA':'condition_disclosure',
    'disagreement_preservation_PASS_FAIL_NA':'disagreement_preservation',
    'review_authority_consistency_PASS_FAIL_NA':'review_authority_consistency',
}
CHECKER_COLS = {
    'source_role_accuracy':'source_role_accuracy',
    'condition_disclosure':'condition_disclosure',
    'representation_disagreement_preservation':'disagreement_preservation',
    'review_authority_consistency':'review_authority_consistency',
}
REVIEWERS = ['R1','R2','R3']


def norm_label(v):
    if pd.isna(v) or str(v).strip() == '':
        return 'NA'
    v = str(v).strip().upper()
    if v not in {'PASS','FAIL','NA'}:
        raise ValueError(f'Unexpected label: {v}')
    return v


def majority(vals):
    c = Counter(vals)
    label,count = c.most_common(1)[0]
    return label if count >= 2 else 'UNRESOLVED'


def fleiss(arr, categories):
    arr=np.asarray(arr)
    n=arr.shape[1]; N=arr.shape[0]
    counts=np.array([[np.sum(row==cat) for cat in categories] for row in arr])
    P_i=(np.sum(counts**2,axis=1)-n)/(n*(n-1))
    Pbar=P_i.mean()
    p_j=counts.sum(axis=0)/(N*n)
    Pe=np.sum(p_j**2)
    k=(Pbar-Pe)/(1-Pe) if (1-Pe)>0 else np.nan
    return float(k),float(Pbar),dict(zip(categories,p_j.tolist()))


def cohen(a,b,categories):
    a=np.asarray(a); b=np.asarray(b)
    po=float(np.mean(a==b))
    pe=sum(np.mean(a==c)*np.mean(b==c) for c in categories)
    k=float((po-pe)/(1-pe)) if (1-pe)>0 else np.nan
    return po,k


def main():
    key=pd.read_csv(KEY)
    manuals={r:pd.read_csv(RAW/f'{r}_manual_review_form.csv') for r in REVIEWERS}
    obligations={r:pd.read_csv(RAW/f'{r}_obligation_review_form.csv') for r in REVIEWERS}

    # Normalize blank applicability cells to NA; preserve all explicit labels.
    audit=[]
    normalized={}
    for r,df0 in obligations.items():
        df=df0.copy()
        for col in OB_COLS:
            for idx,v in df[col].items():
                if pd.isna(v) or str(v).strip()=='':
                    audit.append({'reviewer':r,'case_id':df.loc[idx,'case_id'],'field':col,
                                  'raw_value':'','normalized_value':'NA',
                                  'normalization_reason':'blank obligation cell normalized to NA; no PASS/FAIL label imputed'})
                df.at[idx,col]=norm_label(v)
        normalized[r]=df
        df.to_csv(NORM/f'{r}_obligation_review_form_normalized.csv',index=False)
    pd.DataFrame(audit).to_csv(AN/'normalization_audit.csv',index=False)

    # Unaided matrix.
    manual=key[['case_id','original_dossier_filename']].copy()
    for r,df in manuals.items():
        s=df.set_index('case_id')['issue_found_yes_no'].astype(str).str.strip().str.upper()
        manual[r]=manual['case_id'].map(s)
    manual['majority_issue']=manual[REVIEWERS].apply(lambda x:'YES' if (x=='YES').sum()>=2 else 'NO',axis=1)
    manual['unanimous']=manual[REVIEWERS].nunique(axis=1)==1
    manual.to_csv(AN/'unaided_case_matrix.csv',index=False)

    # Guided labels.
    rows=[]
    for _,kr in key.iterrows():
        for col,ob in OB_COLS.items():
            rec={'case_id':kr.case_id,'original_dossier_filename':kr.original_dossier_filename,'obligation':ob}
            for r,df in normalized.items():
                rec[r]=df.loc[df.case_id==kr.case_id,col].iloc[0]
            cc=Counter(rec[r] for r in REVIEWERS)
            rec['majority_label']=majority([rec[r] for r in REVIEWERS])
            rec['unanimous']=len(cc)==1
            rec['rater_count_PASS']=cc.get('PASS',0); rec['rater_count_FAIL']=cc.get('FAIL',0); rec['rater_count_NA']=cc.get('NA',0)
            rows.append(rec)
    guided=pd.DataFrame(rows)
    guided.to_csv(AN/'guided_obligation_labels.csv',index=False)

    # Agreement.
    agr=[]
    k,p,dist=fleiss(manual[REVIEWERS].to_numpy(),['YES','NO'])
    agr.append({'phase':'unaided','obligation':'case_issue','n_items':28,'average_pair_agreement':p,'fleiss_kappa':k,'distribution':json.dumps(dist)})
    k,p,dist=fleiss(guided[REVIEWERS].to_numpy(),['PASS','FAIL','NA'])
    agr.append({'phase':'guided','obligation':'overall','n_items':112,'average_pair_agreement':p,'fleiss_kappa':k,'distribution':json.dumps(dist)})
    for ob,sub in guided.groupby('obligation'):
        k,p,dist=fleiss(sub[REVIEWERS].to_numpy(),['PASS','FAIL','NA'])
        agr.append({'phase':'guided','obligation':ob,'n_items':len(sub),'average_pair_agreement':p,'fleiss_kappa':k,'distribution':json.dumps(dist)})
    pd.DataFrame(agr).to_csv(AN/'multi_rater_agreement.csv',index=False)

    pair=[]
    for a,b in [('R1','R2'),('R1','R3'),('R2','R3')]:
        po,k=cohen(manual[a],manual[b],['YES','NO'])
        pair.append({'phase':'unaided','obligation':'case_issue','pair':f'{a}-{b}','n_items':28,'raw_agreement':po,'cohen_kappa':k})
        po,k=cohen(guided[a],guided[b],['PASS','FAIL','NA'])
        pair.append({'phase':'guided','obligation':'overall','pair':f'{a}-{b}','n_items':112,'raw_agreement':po,'cohen_kappa':k})
        for ob,sub in guided.groupby('obligation'):
            po,k=cohen(sub[a],sub[b],['PASS','FAIL','NA'])
            pair.append({'phase':'guided','obligation':ob,'pair':f'{a}-{b}','n_items':len(sub),'raw_agreement':po,'cohen_kappa':k})
    pd.DataFrame(pair).to_csv(AN/'pairwise_agreement.csv',index=False)

    # Sensitivity analysis restricted to cells with three explicit (nonblank) reviewer labels.
    raw_rows=[]
    for _,kr in key.iterrows():
        for col,ob in OB_COLS.items():
            rec={'case_id':kr.case_id,'obligation':ob}
            for r,df in obligations.items():
                v=df.loc[df.case_id==kr.case_id,col].iloc[0]
                rec[r]=None if pd.isna(v) or str(v).strip()=='' else str(v).strip().upper()
            raw_rows.append(rec)
    raw=pd.DataFrame(raw_rows)
    sens=[]
    for ob,sub in raw.groupby('obligation'):
        sub=sub.dropna(subset=REVIEWERS)
        cats=sorted(set(sub[REVIEWERS].to_numpy().ravel()))
        k,p,dist=fleiss(sub[REVIEWERS].to_numpy(),cats)
        sens.append({'obligation':ob,'triply_explicit_items':len(sub),'categories':','.join(cats),
                     'average_pair_agreement':p,'fleiss_kappa':k})
    pd.DataFrame(sens).to_csv(AN/'explicit_label_sensitivity.csv',index=False)

    # Reviewer-level phase counts and review-time summaries.
    rev=[]
    for r in REVIEWERS:
        m=manuals[r].copy()
        m['issue_found_yes_no']=m['issue_found_yes_no'].astype(str).str.strip().str.upper()
        g=normalized[r]
        rev.append({
            'reviewer':r,
            'unaided_issue_cases':int((m.issue_found_yes_no=='YES').sum()),
            'guided_issue_cases':int((g[list(OB_COLS)]=='FAIL').any(axis=1).sum()),
            'unaided_median_seconds':float(m.review_time_seconds.median()),
            'unaided_iqr_low':float(m.review_time_seconds.quantile(.25)),
            'unaided_iqr_high':float(m.review_time_seconds.quantile(.75)),
            'guided_median_seconds':float(g.review_time_seconds.median()),
            'guided_iqr_low':float(g.review_time_seconds.quantile(.25)),
            'guided_iqr_high':float(g.review_time_seconds.quantile(.75)),
            'unaided_total_seconds':int(m.review_time_seconds.sum()),
            'guided_total_seconds':int(g.review_time_seconds.sum()),
        })
    pd.DataFrame(rev).to_csv(AN/'reviewer_phase_summary.csv',index=False)

    # Checker comparison.
    checker=pd.read_csv(CHECKER)
    checker=key.merge(checker,left_on='original_dossier_filename',right_on='dossier',how='left')
    for c in CHECKER_COLS:
        checker[c]=checker[c].apply(lambda x:'NA' if pd.isna(x) else str(x).strip().upper())
    long=[]
    for _,row in checker.iterrows():
        for src,ob in CHECKER_COLS.items():
            long.append({'case_id':row.case_id,'original_dossier_filename':row.dossier,'obligation':ob,'checker_label':row[src]})
    cl=pd.DataFrame(long)
    cmp=guided.merge(cl,on=['case_id','original_dossier_filename','obligation'],how='left')
    cmp['resolvable']=cmp.majority_label!='UNRESOLVED'
    cmp['exact_match']=np.where(cmp.resolvable,cmp.majority_label==cmp.checker_label,False)
    cmp['checker_applicable']=cmp.checker_label!='NA'
    cmp['majority_applicable']=~cmp.majority_label.isin(['NA','UNRESOLVED'])
    cmp.to_csv(AN/'checker_vs_reviewer_majority.csv',index=False)
    cmp[(cmp.resolvable)&(~cmp.exact_match)].to_csv(AN/'checker_majority_mismatch_cells.csv',index=False)

    perf=[]
    rc=cmp[cmp.resolvable]
    perf.append({'obligation':'OVERALL','resolvable_items':len(rc),'exact_matches':int((rc.majority_label==rc.checker_label).sum()),
                 'exact_rate':float((rc.majority_label==rc.checker_label).mean())})
    for ob,sub in rc.groupby('obligation'):
        scope=sub[sub.checker_applicable]
        yt=sub.majority_label.eq('FAIL'); yp=sub.checker_label.eq('FAIL')
        tp=int((yt&yp).sum()); fp=int((~yt&yp).sum()); fn=int((yt&~yp).sum()); tn=int((~yt&~yp).sum())
        perf.append({'obligation':ob,'resolvable_items':len(sub),'exact_matches':int((sub.majority_label==sub.checker_label).sum()),
                     'exact_rate':float((sub.majority_label==sub.checker_label).mean()),
                     'checker_applicable_items':len(scope),'checker_scope_exact_matches':int((scope.majority_label==scope.checker_label).sum()),
                     'checker_scope_exact_rate':float((scope.majority_label==scope.checker_label).mean()) if len(scope) else None,
                     'TP':tp,'FP':fp,'FN':fn,'TN':tn,
                     'precision':tp/(tp+fp) if tp+fp else None,
                     'recall':tp/(tp+fn) if tp+fn else None,
                     'specificity':tn/(tn+fp) if tn+fp else None,
                     'checker_NA_reviewer_applicable':int(((sub.checker_label=='NA')&sub.majority_applicable).sum())})
    pd.DataFrame(perf).to_csv(AN/'checker_performance_summary.csv',index=False)

    # Unaided vs guided case-level discovery.
    guided_case=key[['case_id','original_dossier_filename']].copy()
    for r,df in normalized.items():
        vals=df.set_index('case_id')[list(OB_COLS)]
        guided_case[f'{r}_guided_issue']=[bool((vals.loc[cid]=='FAIL').any()) for cid in guided_case.case_id]
    guided_case['guided_majority_issue']=guided_case[[f'{r}_guided_issue' for r in REVIEWERS]].sum(axis=1)>=2
    base=manual.merge(guided_case,on=['case_id','original_dossier_filename'])
    base['unaided_majority_issue']=base.majority_issue=='YES'
    base['majority_change']=np.select([
        (~base.unaided_majority_issue)&base.guided_majority_issue,
        base.unaided_majority_issue&(~base.guided_majority_issue)
    ],['ADDED_BY_GUIDED','LOST_IN_GUIDED'],'UNCHANGED')
    base.to_csv(AN/'unaided_vs_guided_case_comparison.csv',index=False)

    summary={
        'reviewers':3,'cases':28,'guided_obligation_cells':112,
        'blank_to_NA_normalizations':len(audit),
        'majority_labels':guided.majority_label.value_counts().to_dict(),
        'unresolved_cells':guided.loc[guided.majority_label=='UNRESOLVED',['case_id','obligation','R1','R2','R3']].to_dict('records'),
        'unaided_majority_issue_cases':int(base.unaided_majority_issue.sum()),
        'guided_majority_issue_cases':int(base.guided_majority_issue.sum()),
        'cases_added_by_guided_majority':base.loc[base.majority_change=='ADDED_BY_GUIDED','case_id'].tolist(),
        'checker_exact_resolvable_cells':int((rc.majority_label==rc.checker_label).sum()),
        'checker_resolvable_cells':len(rc),
    }
    (AN/'independent_evaluation_summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))

if __name__ == '__main__':
    main()
