# R10 condition-disagreement audit

The three condition cells where the checker says FAIL and reviewer majority says PASS are all 2-1 splits (R1 PASS, R2 PASS, R3 FAIL). Evidence inspection shows that the split follows a definition boundary: R1/R2 count condition visibility in source as sufficient, whereas R3 and the checker require reader-facing condition semantics/binding. R10 therefore reports 40% precision relative to reviewer majority and treats these three cells as criterion-bound disagreements.

## C01 - gross_margin_percentage.html
- Votes: R1=PASS, R2=PASS, R3=FAIL; checker=FAIL.
- Evidence: Source guard is cost == 0; displayed business formula denominator is Revenue; Logic Safeguards says only generic zero denominator.
- Checker criterion: Checker requires the guarded variable to match the denominator displayed in the formal formula; this fails.
- Interpretation: Two reviewers count visible source guard plus safeguard prose as sufficient disclosure; one reviewer requires binding to the displayed representation. This is a criterion-bound 2-1 disagreement.

## C12 - ethylene_production_yield.html
- Votes: R1=PASS, R2=PASS, R3=FAIL; checker=FAIL.
- Evidence: Source contains feedstock_input_tons <= 0 with return 0.0; Logic Safeguards omits the non-positive-input branch.
- Checker criterion: Checker requires reader-facing safeguard text to communicate the branch and its governed denominator; this fails.
- Interpretation: Two reviewers count visible source code as disclosure; one reviewer requires the reader-facing safeguard layer to state the branch. This is a criterion-bound 2-1 disagreement.

## C26 - yield_percentage.html
- Votes: R1=PASS, R2=PASS, R3=FAIL; checker=FAIL.
- Evidence: Source contains IF total_input = 0 THEN RETURN 0; END IF; Logic Safeguards omits that zero-input branch.
- Checker criterion: Checker requires reader-facing safeguard text to communicate the branch and bind it to total_input; this fails.
- Interpretation: Two reviewers count visible source code as disclosure; one reviewer requires the reader-facing safeguard layer to state the branch. This is a criterion-bound 2-1 disagreement.

## Authority normalization sensitivity
All 84 authority labels were explicit; blank-to-NA normalizations in the authority column = 0. The authority Fleiss kappa of -0.285 is therefore unconditional with respect to the normalization rule.
