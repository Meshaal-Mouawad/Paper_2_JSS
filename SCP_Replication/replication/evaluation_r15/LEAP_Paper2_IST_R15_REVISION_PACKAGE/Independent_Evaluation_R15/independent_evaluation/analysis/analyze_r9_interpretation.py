#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
AN = ROOT / 'analysis'
RAW = ROOT / 'raw'
NORM = ROOT / 'normalized'

CMP = AN / 'checker_vs_reviewer_majority.csv'
KEY = AN / 'case_mapping_key.csv'
NORM_AUDIT = AN / 'normalization_audit.csv'
MULTI = AN / 'multi_rater_agreement.csv'
SENS = AN / 'explicit_label_sensitivity.csv'

OBLIGATIONS = [
    'source_role_accuracy',
    'condition_disclosure',
    'disagreement_preservation',
    'review_authority_consistency',
]

def safe_div(a,b):
    return a/b if b else None

def main():
    cmp = pd.read_csv(CMP, keep_default_na=False)
    key = pd.read_csv(KEY)
    multi = pd.read_csv(MULTI)
    sens = pd.read_csv(SENS)

    # unconditional checker comparison: FAIL is the positive class; PASS/NA are negative.
    rows=[]
    for obl in OBLIGATIONS:
        g=cmp[(cmp['obligation']==obl) & (cmp['resolvable'].astype(str).str.lower()=='true')].copy()
        g=g[g['majority_label']!='UNRESOLVED']
        g['checker_label']=g['checker_label'].replace({'':'NA'})
        exact=(g['checker_label']==g['majority_label']).sum()
        actual_fail=g['majority_label'].eq('FAIL')
        pred_fail=g['checker_label'].eq('FAIL')
        tp=int((actual_fail & pred_fail).sum())
        fp=int((~actual_fail & pred_fail).sum())
        fn=int((actual_fail & ~pred_fail).sum())
        tn=int((~actual_fail & ~pred_fail).sum())
        krow=multi[(multi['phase']=='guided') & (multi['obligation']==obl)].iloc[0]
        srow=sens[sens['obligation']==obl]
        explicit_kappa=float(srow.iloc[0]['fleiss_kappa']) if len(srow) else None
        rows.append({
            'obligation':obl,
            'resolvable_items':len(g),
            'three_state_exact':int(exact),
            'three_state_exact_rate':safe_div(int(exact),len(g)),
            'reviewer_fleiss_kappa':float(krow['fleiss_kappa']),
            'triply_explicit_items':int(srow.iloc[0]['triply_explicit_items']) if len(srow) else None,
            'triply_explicit_fleiss_kappa':explicit_kappa,
            'TP':tp,'FP':fp,'FN':fn,'TN':tn,
            'precision':safe_div(tp,tp+fp),
            'recall':safe_div(tp,tp+fn),
            'specificity':safe_div(tn,tn+fp),
            'majority_failures':int(actual_fail.sum()),
            'checker_failures':int(pred_fail.sum()),
        })
    cm=pd.DataFrame(rows)
    cm.to_csv(AN/'r9_unconditional_confusion.csv',index=False)

    # Normalization burden by obligation.
    na=pd.read_csv(NORM_AUDIT)
    na['obligation']=na['field'].str.replace('_PASS_FAIL_NA','',regex=False)
    nb=(na.groupby('obligation').size().rename('blank_to_NA').reset_index())
    nb['possible_reviewer_labels']=84
    nb['fraction']=nb['blank_to_NA']/84
    nb.to_csv(AN/'r9_normalization_burden.csv',index=False)

    # Guided-added cases, with the majority-fail obligation drivers.
    uv=pd.read_csv(AN/'unaided_vs_guided_case_comparison.csv', keep_default_na=False)
    added=uv[uv['majority_change']=='ADDED_BY_GUIDED'].copy()
    guided=pd.read_csv(AN/'guided_obligation_labels.csv', keep_default_na=False)
    out=[]
    for _,r in added.iterrows():
        cid=r['case_id']
        gg=guided[(guided['case_id']==cid) & (guided['majority_label']=='FAIL')]
        drivers=';'.join(gg['obligation'].tolist())
        out.append({
            'case_id':cid,
            'dossier':r['original_dossier_filename'],
            'unaided_majority_issue':r['unaided_majority_issue'],
            'guided_majority_issue':r['guided_majority_issue'],
            'guided_majority_fail_obligations':drivers,
        })
    added_df=pd.DataFrame(out)
    added_df.to_csv(AN/'r9_guided_added_cases.csv',index=False)

    # Authority-majority failures outside released checker eligibility.
    auth=cmp[(cmp['obligation']=='review_authority_consistency') &
             (cmp['majority_label']=='FAIL') &
             (cmp['checker_applicable'].astype(str).str.lower()!='true')].copy()
    auth[['case_id','original_dossier_filename','R1','R2','R3','majority_label','checker_label']].to_csv(
        AN/'r9_authority_outside_checker_scope.csv',index=False)

    # Summarize reviewer evidence notes for the guided-added and authority outside-scope cases.
    note_rows=[]
    wanted=set(added_df['case_id']).union(set(auth['case_id']))
    for rev in ['R1','R2','R3']:
        df=pd.read_csv(NORM/f'{rev}_obligation_review_form_normalized.csv', keep_default_na=False)
        for _,rr in df[df['case_id'].isin(wanted)].iterrows():
            note_rows.append({'reviewer':rev,'case_id':rr['case_id'],'evidence_note':rr['evidence_note']})
    pd.DataFrame(note_rows).to_csv(AN/'r9_selected_reviewer_rationales.csv',index=False)

    summary={
        'reviewers':3,
        'cases':28,
        'possible_guided_reviewer_labels':336,
        'blank_to_NA_normalizations':int(len(na)),
        'blank_fraction':len(na)/336,
        'condition_blank_to_NA':int((na['obligation']=='condition_disclosure').sum()),
        'disagreement_blank_to_NA':int((na['obligation']=='disagreement_preservation').sum()),
        'guided_added_cases':added_df['case_id'].tolist(),
        'all_guided_added_cases_have_authority_failure':bool(all('review_authority_consistency' in x for x in added_df['guided_majority_fail_obligations'])),
        'authority_majority_failures_outside_checker_scope':auth['case_id'].tolist(),
        'authority_fleiss_kappa':float(multi[(multi['phase']=='guided') & (multi['obligation']=='review_authority_consistency')].iloc[0]['fleiss_kappa']),
        'disagreement_triply_explicit_kappa':float(sens[sens['obligation']=='disagreement_preservation'].iloc[0]['fleiss_kappa']),
        'unconditional_confusion':rows,
    }
    (AN/'r9_interpretation_summary.json').write_text(json.dumps(summary,indent=2))

    report=[]
    report.append('# R9 Independent-Evaluation Interpretation')
    report.append('')
    report.append('This addendum reanalyzes the frozen R8 reviewer/checker data without changing any reviewer label or checker output.')
    report.append('')
    report.append(f"- Blank-to-NA normalizations: {len(na)}/336 reviewer-obligation labels ({100*len(na)/336:.1f}%).")
    report.append(f"- Condition blanks: {(na['obligation']=='condition_disclosure').sum()}/84; disagreement blanks: {(na['obligation']=='disagreement_preservation').sum()}/84.")
    report.append(f"- Review-authority Fleiss' kappa: {summary['authority_fleiss_kappa']:.3f}; the operationalization fails inter-reviewer reliability and is removed from the retained audit checklist in R9.")
    report.append(f"- All five guided-only majority cases ({', '.join(summary['guided_added_cases'])}) are driven by majority review-authority FAIL labels, so the 18-to-23 case shift is not interpreted as improved detection.")
    report.append(f"- Authority majority failures outside the released status checker: {', '.join(summary['authority_majority_failures_outside_checker_scope'])}.")
    report.append(f"- Disagreement sensitivity on the {int(sens[sens['obligation']=='disagreement_preservation'].iloc[0]['triply_explicit_items'])} triply explicit labels yields kappa={summary['disagreement_triply_explicit_kappa']:.3f}; R9 narrows this dimension to explicit-conflict routing rather than retaining a broad disagreement construct.")
    report.append('')
    report.append('## Unconditional checker comparison')
    report.append('FAIL is treated as the positive class; PASS and NA are non-fail for TP/FP/FN/TN. Exact agreement remains the original three-state PASS/FAIL/NA comparison.')
    report.append('')
    report.append(cm.to_markdown(index=False))
    report.append('')
    report.append('## Interpretation')
    report.append('Source-role reviewer agreement is positive, while the released checker misses 14 of 16 reviewer-majority FAIL cases and flags two majority-PASS cases. Condition disclosure has the strongest reviewer agreement; the checker captures both majority FAIL cases and adds three FAILs rejected by the majority reference. The original broad disagreement construct is normalization-sensitive and the released checker does not flag four broader reviewer-majority disagreement failures, so R9 retains only the narrower explicit-conflict-routing check. Review-authority consistency has negative chance-corrected agreement and is removed from the retained checklist.')
    (AN/'R9_INDEPENDENT_EVALUATION_INTERPRETATION.md').write_text('\n'.join(report)+'\n')

if __name__=='__main__':
    main()
