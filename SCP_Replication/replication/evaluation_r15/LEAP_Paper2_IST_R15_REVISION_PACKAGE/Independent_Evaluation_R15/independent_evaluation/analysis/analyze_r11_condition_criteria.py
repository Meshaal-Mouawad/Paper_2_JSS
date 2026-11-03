#!/usr/bin/env python3
from pathlib import Path
import pandas as pd, json

root = Path(__file__).resolve().parents[1]
labels = pd.read_csv(root/'analysis'/'guided_obligation_labels.csv')
checker = pd.read_csv(root/'checker'/'dossier_obligation_matrix.csv')

cond = labels[labels['obligation']=='condition_disclosure'].copy()
cond = cond.merge(checker[['dossier','condition_disclosure']], left_on='original_dossier_filename', right_on='dossier', how='left')
elig = cond[cond['condition_disclosure'].notna()].copy()
assert len(elig)==10, f'Expected 10 checker-eligible condition cases, found {len(elig)}'
assert (elig['R1'].fillna('') == elig['R2'].fillna('')).all(), 'R1/R2 labels differ on eligible condition cases'
assert elig['R3'].notna().all(), 'R3 has missing labels on eligible condition cases'

# FAIL is positive class. Checker outputs PASS/FAIL.
def metrics(reference_col):
    ref=elig[reference_col].str.upper()
    pred=elig['condition_disclosure'].str.upper()
    tp=int(((pred=='FAIL') & (ref=='FAIL')).sum())
    fp=int(((pred=='FAIL') & (ref=='PASS')).sum())
    fn=int(((pred=='PASS') & (ref=='FAIL')).sum())
    tn=int(((pred=='PASS') & (ref=='PASS')).sum())
    precision=tp/(tp+fp) if tp+fp else None
    recall=tp/(tp+fn) if tp+fn else None
    exact=int((pred==ref).sum())
    return dict(tp=tp,fp=fp,fn=fn,tn=tn,precision=precision,recall=recall,exact=exact,n=len(elig))

src = metrics('R1')  # R1 and R2 identical here
pub = metrics('R3')

rows=[
    {'criterion':'source_visibility_R1_R2','reference':'R1/R2 identical labels on 10 eligible cases',**src},
    {'criterion':'reader_facing_publication_R3','reference':'R3 labels on the same 10 eligible cases',**pub},
]
out=pd.DataFrame(rows)
out.to_csv(root/'analysis'/'r11_condition_criterion_sensitivity.csv',index=False)

case_cols=['case_id','original_dossier_filename','R1','R2','R3','condition_disclosure']
elig[case_cols].to_csv(root/'analysis'/'r11_condition_eligible_labels.csv',index=False)

summary={
    'eligible_cases':10,
    'r1_r2_identical_on_eligible_cases':True,
    'source_visibility':src,
    'reader_facing_publication':pub,
    'interpretation':'Condition-rule precision is criterion-sensitive on the same fixed eligible set: 0.40 under source visibility and 1.00 under reader-facing disclosure; recall is 1.00 under both.'
}
(root/'analysis'/'r11_condition_criterion_summary.json').write_text(json.dumps(summary,indent=2)+'\n')

md=f'''# R11 condition-criterion sensitivity audit\n\nThe R10 review identified a criterion ambiguity in condition disclosure. This audit recomputes the released condition checker on the same ten checker-eligible cases under the two disclosure criteria actually observed in the independent reviewer data.\n\n- **Source visibility (R1/R2):** TP={src['tp']}, FP={src['fp']}, FN={src['fn']}, TN={src['tn']}, precision={src['precision']:.2f}, recall={src['recall']:.2f}.\n- **Reader-facing publication (R3):** TP={pub['tp']}, FP={pub['fp']}, FN={pub['fn']}, TN={pub['tn']}, precision={pub['precision']:.2f}, recall={pub['recall']:.2f}.\n\nR1 and R2 provide identical labels on all ten checker-eligible condition cases. R3 provides an explicit label on all ten. The calculation changes no reviewer label and no checker output. It isolates the effect of the disclosure definition on the reported condition-rule precision.\n'''
(root/'analysis'/'R11_CONDITION_CRITERION_SENSITIVITY.md').write_text(md)

print(json.dumps(summary,indent=2))
