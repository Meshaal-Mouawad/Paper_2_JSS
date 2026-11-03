# Independent Evaluation Supplement - R11

This supplement preserves the three-reviewer evaluation and the deterministic R9-R11 reinterpretation and criterion-sensitivity analyses used in the current manuscript.

## Design

Three independent reviewers evaluated 28 blinded LEAP dossier cases in two sequential phases:

1. **Unaided review** - case-level issue discovery with free-text rationale, evidence location, confidence, and review time.
2. **Candidate-guided review** - PASS / FAIL / NA labels for source-role accuracy, condition disclosure, representation disagreement, and review-authority consistency.

Reviewer packets excluded checker outputs, manuscript result tables, the organizer key, and other reviewer responses during collection.

## Raw and normalized data

`raw/` contains the exact reviewer CSV content under reviewer IDs R1-R3.

Reviewers left applicability-dependent condition/disagreement cells blank. The original primary analysis maps these blanks to `NA` while preserving every explicit `PASS` and `FAIL` label. `analysis/normalization_audit.csv` records every mapped cell.

- Blank-to-NA mappings: 94/336 reviewer-obligation labels (28.0%).
- Condition: 40/84.
- Disagreement: 54/84.

The sensitivity analysis restricted to triply explicit labels is retained in `analysis/explicit_label_sensitivity.csv`.

## Aggregation

- Majority reference: at least 2 of 3 matching reviewer labels.
- One cell has a three-way split and remains `UNRESOLVED`: C17 / condition disclosure.
- Reviewer majority is an independent comparison reference, not a definitive oracle.
- Fleiss' kappa and average pair agreement quantify multi-reviewer agreement.

## R9 reinterpretation

R9 adds an unconditional checker comparison and case-level diagnostics requested by the independent review:

- `analysis/r9_unconditional_confusion.csv` - exact three-state agreement plus TP/FP/FN/TN for each candidate, unconditioned on checker eligibility.
- `analysis/r9_guided_added_cases.csv` - the five cases that enter the majority issue set only in guided review.
- `analysis/r9_authority_outside_checker_scope.csv` - the three authority-majority failures outside the released unresolved-status rule.
- `analysis/r9_selected_reviewer_rationales.csv` - preserved reviewer rationales for those diagnostic cases.
- `analysis/r9_normalization_burden.csv` - blank-to-NA burden by candidate.
- `analysis/r9_interpretation_summary.json` - machine-readable R9 summary.
- `analysis/R9_INDEPENDENT_EVALUATION_INTERPRETATION.md` - readable interpretation.

The R9 interpretation makes no change to reviewer labels or released checker output.

## Reproduce

From this directory:

```bash
python analysis/analyze_independent_evaluation.py
python analysis/analyze_r9_interpretation.py
```

## R9 empirical disposition

- Source-role accuracy: reviewer Fleiss' kappa 0.407; checker TP=2, FP=2, FN=14, TN=10. The dimension is retained; the checker under-covers it.
- Condition disclosure: reviewer Fleiss' kappa 0.553; checker TP=2, FP=3, FN=0, TN=22. The dimension is retained; the checker over-flags three majority non-fail cases.
- Broad disagreement preservation: normalized kappa 0.452; triply explicit sensitivity kappa -0.167; four majority failures receive no checker FAIL. R9 narrows the retained check to explicit-conflict routing.
- Review-authority consistency: reviewer Fleiss' kappa -0.285. R9 removes this candidate from the retained checklist.
- All five guided-only majority cases are driven by review-authority FAIL labels from R1/R3 while R2 records PASS.

## Evidence linkage

`analysis/case_mapping_key.csv` maps blinded case IDs to frozen dossier filenames. `checker/dossier_obligation_matrix.csv` is the frozen released checker output used for comparison.

## R10 refinement

R10 keeps all reviewer labels and checker outputs unchanged and adds a targeted audit of the three condition cells where the checker records FAIL while reviewer majority records PASS:

- `analysis/r10_condition_checker_majority_disagreements.csv`
- `analysis/r10_condition_disagreement_summary.json`
- `analysis/R10_CONDITION_DISAGREEMENT_AUDIT.md`
- `analysis/analyze_r10_condition_disagreements.py`

All three cells are 2-1 reviewer splits (R1 PASS, R2 PASS, R3 FAIL). The dossier evidence shows a common definition boundary: two reviewers count visibility of the branch in retained source as disclosure, while one reviewer and the checker require reader-facing safeguard semantics/binding. R10 therefore reports condition precision relative to reviewer majority and treats these three cells as criterion-bound disagreements.

R10 also confirms that all 84 review-authority labels were explicit. The authority Fleiss' kappa of -0.285 is therefore unconditional with respect to blank-to-NA normalization.

### Reproduce the R10 addendum

```bash
python analysis/analyze_r10_condition_disagreements.py
```

## R11 criterion-sensitivity refinement

R11 keeps every raw reviewer label and every released checker output unchanged. It resolves the R10 condition-definition ambiguity by evaluating the same ten checker-eligible condition cases under the two criteria observed in the reviewer data:

- `analysis/r11_condition_criterion_sensitivity.csv`
- `analysis/r11_condition_eligible_labels.csv`
- `analysis/r11_condition_criterion_summary.json`
- `analysis/R11_CONDITION_CRITERION_SENSITIVITY.md`
- `analysis/analyze_r11_condition_criteria.py`

R1 and R2 provide identical labels on all ten checker-eligible condition cases and operationalize source visibility as sufficient disclosure. Against that criterion, the checker has precision 0.40 and recall 1.00. R3 operationalizes disclosure at the reader-facing publication layer; against those labels on the same ten cases, the checker has precision 1.00 and recall 1.00. The R11 analysis changes no reviewer label and no checker output.

### Reproduce the R11 addendum

```bash
python analysis/analyze_r11_condition_criteria.py
```
