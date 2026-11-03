# Independent Reviewer Guidance

## Purpose

This evaluation examines whether publication-level defects in the 28 frozen LEAP dossier cases can be identified independently of the released checker outputs.

Complete the evaluation in two phases, in this order.

## Phase A — Unaided Review

1. Review every case C01–C28 using either `cases_html/` or the matching file in `cases_text/`.
2. Use your normal software-documentation judgment.
3. For each case, complete one row in `manual_review_form.csv`.
4. Record:
   - whether you found a publication problem;
   - a short description;
   - the visible evidence/location supporting the judgment;
   - confidence from 1–5;
   - review time in seconds.
5. Complete and save Phase A before opening Phase B guidance.

## Phase B — Obligation-Guided Review

Review the same 28 cases using the four questions below and complete `obligation_review_form.csv`.

### 1. Source-role accuracy
Does the reader-facing explanation assign each visible source element its actual source role?

### 2. Condition disclosure
Where a visible condition materially qualifies the displayed behavior or formula, are the condition and the governed variable represented faithfully?

### 3. Disagreement preservation
Where visible evidence contains an explicit formula/source conflict, mismatch, or inversion, does the publication keep the disagreement visible in review routing?

### 4. Review-authority consistency
Does reader-facing authority or certification language agree with the displayed review state?

For each obligation enter only `PASS`, `FAIL`, or `NA`, then cite the visible evidence supporting the labels and record review time.

## Independence controls

Before both phases are finished, do not inspect:
- released checker outputs;
- audit CSV/JSON results;
- manuscript result tables;
- reviewer-response documents;
- the organizer key;
- completed forms from other reviewers.

Each reviewer should complete the work independently.

## Submission back to the organizer

Return exactly these two completed files:

- `manual_review_form.csv`
- `obligation_review_form.csv`

Do not rename case IDs or reorder rows.

If you add notes, place them in a separate file named `reviewer_notes.txt`.

## Labeling rule

Base every label only on evidence visible in the supplied case. Do not infer hidden implementation details. Use `NA` when the obligation has no applicable visible condition/state in that case.

## Completion criterion

All 28 cases must be completed in both phases.
