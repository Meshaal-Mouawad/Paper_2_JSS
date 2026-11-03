# Reporting clarifications — existing Paper 2 data

The two frozen evidence ZIPs remain byte-identical. These additional records explain the corrected account; they do not replace the archived analysis.

## Original rating labels
The original obligation-response files contain 112 PASS, 130 FAIL, and 94 literal NA values (336 total; zero missing labels). The intermediate files stored under `raw/` in the R15 analysis archive have blank strings at the 94 NA positions. The normalized analysis restores all 336 original values exactly. `LABEL_RECONCILIATION.csv` records every comparison; `ORIGINAL_RETURN_IDENTITIES.json` binds the copied original returns to their source bytes. This establishes the representation change, not the historical software operation that caused it.

Agreement restricted to seven disagreement cases is a comparison among cases all three reviewers judged applicable (PASS/FAIL). The whole-set result includes NA as a label. Both statistics are preserved.

## Review instructions and analysis
`REVIEWER_PACKET_README.md` contains both phases and instructs reviewers to complete Phase A using their own judgment before applying the checklist. Checker outputs and organizer mappings were withheld; availability of the phase instructions is stated explicitly in the manuscript.

`COLLECTION_AND_ANALYSIS_GUIDANCE.md` recommends three reviewers, Fleiss' kappa and majority agreement, with subsequent adjudication. The reviewer packet recommends two reviewers, Cohen's kappa, and post-review adjudicated comparison labels. The manuscript reports what the existing analysis used: three returned forms, Fleiss' kappa, and a majority reference. This revision records no new adjudication or participant collection.

## Evaluated generation path
`GENERATION_LOG_READONLY_COPY.txt` is a byte-exact copy of `primary/artifact_28/generation.log` in the frozen technical supplement. It records deterministic detail preparation for all 28 pages. Figure 2 now describes that evaluated path rather than labeling it as AI-assisted explanation.

## Reproduction
From the package root, `python3 verification/verify_preservation.py` verifies the archives, label reconciliation, agreement values, stored checker comparisons, phase counts, protected manuscript text, and unchanged numerical table entries. It performs no data collection and does not execute the complete LEAP/FastAPI pipeline.
