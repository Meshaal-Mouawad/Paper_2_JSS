# R8 Independent Reviewer Evaluation

## Design

Three independent reviewers evaluated the same 28 blinded LEAP dossier cases in two sequential phases.

- Phase A: unaided review (`YES`/`NO` issue flag, free-text description, evidence location, confidence, review time).
- Phase B: obligation-guided review of source-role accuracy, condition disclosure, disagreement preservation, and review-authority consistency.
- Reviewer packets excluded checker outputs, manuscript result tables, the organizer mapping key, and other reviewers' responses.
- Majority reference label: at least 2 of 3 reviewers.
- One three-way split remained unresolved: C17 condition disclosure (`NA` / `PASS` / `FAIL`).
- Checker exact-match calculations exclude that unresolved cell.

## Raw-form normalization

Reviewers used blank cells in the applicability-dependent condition/disagreement columns where `NA` was intended or no applicable evidence was recorded.

- R1 blank -> NA normalizations: 32
- R2 blank -> NA normalizations: 32
- R3 blank -> NA normalizations: 30
- Total: 94

No explicit `PASS` or `FAIL` label was changed. Exact raw forms and a cell-level normalization audit are preserved. A sensitivity table restricted to triply explicit labels is also supplied.

## Unaided baseline

Majority issue identification: **18/28** cases.

Average pair agreement: **0.762**.
Fleiss' kappa: **0.443**.

Reviewer-level issue counts:
- R1: 19/28
- R2: 15/28
- R3: 24/28

## Guided review

Majority issue identification (at least one majority-FAIL obligation in a case): **23/28** cases.

Five cases changed from no unaided majority issue to a guided majority issue:
C03, C08, C11, C20, C21.

Across all 112 obligation cells:
- average pair agreement: **0.634**
- Fleiss' kappa: **0.446**
- unanimous cells: **51/112**
- majority labels: 44 FAIL, 34 PASS, 33 NA, 1 unresolved.

Per obligation:
- condition_disclosure: average pair agreement 0.726; Fleiss' kappa 0.553.
- disagreement_preservation: average pair agreement 0.714; Fleiss' kappa 0.452.
- review_authority_consistency: average pair agreement 0.381; Fleiss' kappa -0.285.
- source_role_accuracy: average pair agreement 0.714; Fleiss' kappa 0.407.

## Checker versus reviewer-majority reference

Exact checker/reviewer-majority match across resolvable obligation cells: **77/111 (69.4%)**.

Within each checker eligibility set:
- condition_disclosure: 7/10 exact (70.0%); reviewer-majority applicable outside checker scope: 2.
- disagreement_preservation: 6/6 exact (100.0%); reviewer-majority applicable outside checker scope: 4.
- review_authority_consistency: 19/19 exact (100.0%); reviewer-majority applicable outside checker scope: 9.
- source_role_accuracy: 12/28 exact (42.9%); reviewer-majority applicable outside checker scope: 0.

The source-role rule has the largest direct mismatch: reviewer majority marks 16/28 source-role failures, while the released checker flags four cases, yielding 12/28 exact three-state labels. The disagreement and authority rules align with reviewer majority on every checker-eligible case (6/6 and 19/19 respectively), while reviewers also identify broader disagreement/authority concerns outside those checker eligibility sets. Condition disclosure matches 7/10 checker-eligible cases.

## Review-time observations

The two phases were sequential, so timing is descriptive rather than a controlled speed comparison.
- R1: unaided median 70.0s (IQR 60.0-80.0); guided median 70.0s (IQR 60.0-80.0).
- R2: unaided median 64.5s (IQR 46.0-81.2); guided median 72.0s (IQR 56.8-88.2).
- R3: unaided median 64.5s (IQR 57.8-75.0); guided median 55.5s (IQR 49.0-63.5).

## Interpretation

The independent evaluation closes the absence-of-reviewer-evidence gate by supplying an unaided baseline and obligation-guided labels from three reviewers. The results support rule-specific rather than global checker claims. Disagreement preservation and review-authority consistency align with reviewer-majority labels throughout their released checker eligibility sets. Source-role accuracy shows substantial undercoverage relative to reviewer judgments. Condition disclosure shows three checker-majority disagreements within ten checker-eligible cases. Reviewer agreement also varies materially by obligation, especially for review-authority consistency, so the manuscript reports the numerical agreement rather than treating majority labels as a definitive gold standard.
