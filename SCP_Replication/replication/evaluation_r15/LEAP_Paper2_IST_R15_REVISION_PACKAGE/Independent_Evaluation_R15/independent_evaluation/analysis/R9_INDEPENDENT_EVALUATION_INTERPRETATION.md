# R9 Independent-Evaluation Interpretation

This addendum reanalyzes the frozen R8 reviewer/checker data without changing any reviewer label or checker output.

- Blank-to-NA normalizations: 94/336 reviewer-obligation labels (28.0%).
- Condition blanks: 40/84; disagreement blanks: 54/84.
- Review-authority Fleiss' kappa: -0.285; the operationalization fails inter-reviewer reliability and is removed from the retained audit checklist in R9.
- All five guided-only majority cases (C03, C08, C11, C20, C21) are driven by majority review-authority FAIL labels, so the 18-to-23 case shift is not interpreted as improved detection.
- Authority majority failures outside the released status checker: C15, C22, C25.
- Disagreement sensitivity on the 7 triply explicit labels yields kappa=-0.167; R9 narrows this dimension to explicit-conflict routing rather than retaining a broad disagreement construct.

## Unconditional checker comparison
FAIL is treated as the positive class; PASS and NA are non-fail for TP/FP/FN/TN. Exact agreement remains the original three-state PASS/FAIL/NA comparison.

| obligation                   |   resolvable_items |   three_state_exact |   three_state_exact_rate |   reviewer_fleiss_kappa |   triply_explicit_items |   triply_explicit_fleiss_kappa |   TP |   FP |   FN |   TN |   precision |   recall |   specificity |   majority_failures |   checker_failures |
|:-----------------------------|-------------------:|--------------------:|-------------------------:|------------------------:|------------------------:|-------------------------------:|-----:|-----:|-----:|-----:|------------:|---------:|--------------:|--------------------:|-------------------:|
| source_role_accuracy         |                 28 |                  12 |                 0.428571 |                0.407059 |                      28 |                       0.407059 |    2 |    2 |   14 |   10 |         0.5 | 0.125    |      0.833333 |                  16 |                  4 |
| condition_disclosure         |                 27 |                  22 |                 0.814815 |                0.553398 |                      12 |                       0.446154 |    2 |    3 |    0 |   22 |         0.4 | 1        |      0.88     |                   2 |                  5 |
| disagreement_preservation    |                 28 |                  24 |                 0.857143 |                0.452471 |                       7 |                      -0.166667 |    0 |    0 |    4 |   24 |       nan   | 0        |      1        |                   4 |                  0 |
| review_authority_consistency |                 28 |                  19 |                 0.678571 |               -0.284706 |                      28 |                      -0.284706 |   19 |    0 |    3 |    6 |         1   | 0.863636 |      1        |                  22 |                 19 |

## Interpretation
Source-role reviewer agreement is positive, while the released checker misses 14 of 16 reviewer-majority FAIL cases and flags two majority-PASS cases. Condition disclosure has the strongest reviewer agreement; the checker captures both majority FAIL cases and adds three FAILs rejected by the majority reference. The original broad disagreement construct is normalization-sensitive and the released checker does not flag four broader reviewer-majority disagreement failures, so R9 retains only the narrower explicit-conflict-routing check. Review-authority consistency has negative chance-corrected agreement and is removed from the retained checklist.
