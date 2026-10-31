# LEAP Paper 2 — Science of Computer Programming revision

**Current manuscript:** *Evaluating Checks for Generated KPI Documentation: Rule Coverage and Reference Criteria*

**Authors:** Meshaal Obaid Mouawad and Bryan Jones, Mississippi State University.

**Target journal:** Science of Computer Programming (SCP). This is the revised manuscript after editorial pre-screening of the earlier Journal of Systems and Software submission (`JSSOFTWARE-D-26-02929`). The original JSS submission and coauthor edits remain preserved in the Git history, including commit `a89a79b8e66ed0bcdbff3cc54eb86d2c2b4e94b8`.

## Current files

- `main.tex` — current editable SCP manuscript; includes the preparation declaration.
- `main.pdf` — visually verified, size-optimized rendering of the approved 12-page SCP manuscript. The complete unoptimized approval copy is preserved in the author submission package.
- `references.bib`, `main.bbl` — bibliography and verified generated references.
- `figures/` — editable figure sources and matching rendered graphics.
- `build.sh` — reproducible LaTeX build.

Build locally using `bash build.sh` with a full LaTeX/BibTeX toolchain. The repository also includes a verified `main.bbl`; if BibTeX is unavailable, you can compile with `pdflatex -interaction=nonstopmode -halt-on-error main.tex` three times using that existing bibliography output.

## Evidence and evaluation

The empirical analysis covers 28 generated KPI documents, 32 prepared control outcomes, and 336 ratings from three code reviewers. Source-role document labels and specific underlying defects are distinguished. The checker matched the majority Fail label on 2 of 16 documents, but the majority reviewers and checker identified different underlying problems in those two overlapping documents. Condition-alert performance is reported separately against the recorded judgments of reviewers A/B and C.

The original evaluation source materials are maintained separately in the `Meshaal-Mouawad/LEAP-Paper2-Evidence` repository. That repository is currently private. The complete internal scientific recovery package, including reviewer rationales and preserved originals, is not included in this public manuscript repository.

## Publication status

The journal transfer initiated the SCP submission workflow; completion and editorial acceptance are separate events. This repository records the manuscript revision, not a publication acceptance.
