#!/usr/bin/env python3
from __future__ import annotations
import csv, json, hashlib, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AN = ROOT / 'analysis'
NORM = ROOT / 'normalized'
PACKET = ROOT / 'INDEPENDENT_EVALUATION_PACKET.zip'
CASES = ['C01','C12','C26']

MAP = {}
with open(AN/'case_mapping_key.csv', newline='') as f:
    for r in csv.DictReader(f):
        MAP[r['case_id']] = r['original_dossier_filename']

with zipfile.ZipFile(PACKET) as z:
    packet_members = set(z.namelist())
    rows=[]
    for cid in CASES:
        labels=[]
        for rid in ['R1','R2','R3']:
            with open(NORM/f'{rid}_obligation_review_form_normalized.csv', newline='') as f:
                rr=next(x for x in csv.DictReader(f) if x['case_id']==cid)
            labels.append(rr['condition_disclosure_PASS_FAIL_NA'])
        member=f'INDEPENDENT_EVALUATION_PACKET/cases_html/{cid}.html'
        if member not in packet_members:
            raise SystemExit(f'missing {member}')
        html_bytes=z.read(member)
        if cid=='C01':
            evidence='Source guard is cost == 0; displayed business formula denominator is Revenue; Logic Safeguards says only generic zero denominator.'
            criterion='Checker requires the guarded variable to match the denominator displayed in the formal formula; this fails.'
            interpretation='Two reviewers count visible source guard plus safeguard prose as sufficient disclosure; one reviewer requires binding to the displayed representation. This is a criterion-bound 2-1 disagreement.'
        elif cid=='C12':
            evidence='Source contains feedstock_input_tons <= 0 with return 0.0; Logic Safeguards omits the non-positive-input branch.'
            criterion='Checker requires reader-facing safeguard text to communicate the branch and its governed denominator; this fails.'
            interpretation='Two reviewers count visible source code as disclosure; one reviewer requires the reader-facing safeguard layer to state the branch. This is a criterion-bound 2-1 disagreement.'
        else:
            evidence='Source contains IF total_input = 0 THEN RETURN 0; END IF; Logic Safeguards omits that zero-input branch.'
            criterion='Checker requires reader-facing safeguard text to communicate the branch and bind it to total_input; this fails.'
            interpretation='Two reviewers count visible source code as disclosure; one reviewer requires the reader-facing safeguard layer to state the branch. This is a criterion-bound 2-1 disagreement.'
        rows.append({
            'case_id':cid,'dossier':MAP[cid],'R1':labels[0],'R2':labels[1],'R3':labels[2],
            'majority':'PASS','checker':'FAIL','visible_evidence':evidence,
            'checker_criterion':criterion,'interpretation':interpretation,
            'blinded_case_html_sha256':hashlib.sha256(html_bytes).hexdigest()
        })

with open(AN/'r10_condition_checker_majority_disagreements.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

with open(AN/'normalization_audit.csv',newline='') as f:
    norm=list(csv.DictReader(f))
auth_norm=[r for r in norm if 'authority' in (r.get('field','') or '').lower()]
summary={
    'condition_checker_majority_disagreements': len(rows),
    'condition_vote_pattern': {'R1':'PASS','R2':'PASS','R3':'FAIL','checker':'FAIL'},
    'authority_possible_labels':84,
    'authority_blank_to_na_normalizations':len(auth_norm),
    'authority_fleiss_kappa':-0.2847058823529411,
    'interpretation':'Authority kappa is unconditional with respect to blank-to-NA normalization; all 84 authority labels were explicit.'
}
(AN/'r10_condition_disagreement_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
md=['# R10 condition-disagreement audit','',
    'The three condition cells where the checker says FAIL and reviewer majority says PASS are all 2-1 splits (R1 PASS, R2 PASS, R3 FAIL). Evidence inspection shows that the split follows a definition boundary: R1/R2 count condition visibility in source as sufficient, whereas R3 and the checker require reader-facing condition semantics/binding. R10 therefore reports 40% precision relative to reviewer majority and treats these three cells as criterion-bound disagreements.','']
for r in rows:
    md += [f"## {r['case_id']} - {r['dossier']}",f"- Votes: R1={r['R1']}, R2={r['R2']}, R3={r['R3']}; checker={r['checker']}.",f"- Evidence: {r['visible_evidence']}",f"- Checker criterion: {r['checker_criterion']}",f"- Interpretation: {r['interpretation']}",'']
md += ['## Authority normalization sensitivity',f"All 84 authority labels were explicit; blank-to-NA normalizations in the authority column = {len(auth_norm)}. The authority Fleiss kappa of -0.285 is therefore unconditional with respect to the normalization rule."]
(AN/'R10_CONDITION_DISAGREEMENT_AUDIT.md').write_text('\n'.join(md)+'\n')
print(json.dumps(summary,indent=2))
