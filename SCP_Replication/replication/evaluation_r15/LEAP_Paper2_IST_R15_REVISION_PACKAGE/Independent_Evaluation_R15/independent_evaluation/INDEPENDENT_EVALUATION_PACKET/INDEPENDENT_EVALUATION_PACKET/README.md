# Independent Evaluation Packet

Purpose: collect evidence that is independent of the released checker outputs.

## Blinding
This packet contains the 28 frozen LEAP dossier pages in a fixed randomized order and blank annotation forms. It intentionally excludes checker outputs, expected labels, audit summaries, and the organizer mapping to original dossier filenames.

## Phase A — unaided manual review
1. Review each case in `cases_html/` or the corresponding plain-text rendering in `cases_text/`.
2. Record any reader-facing publication problem you identify in `manual_review_form.csv`.
3. Use your own software-documentation judgment. Do not use the four-obligation checklist during this phase.
4. Record review time per case.

## Phase B — obligation-guided review
After Phase A is complete, review the same cases using the four operational questions below and record the result in `obligation_review_form.csv`.

- Source-role accuracy: Does the reader-facing explanation assign each visible source element its actual source role?
- Condition disclosure: Where a visible condition materially qualifies the displayed behavior/formula, is that condition and its governed variable represented faithfully?
- Disagreement preservation: Where the visible evidence contains an explicit formula/source conflict, mismatch, or inversion, does the publication keep the disagreement visible in review routing?
- Review-authority consistency: Does reader-facing authority/certification language agree with the displayed review state?

Use PASS / FAIL / NA and cite the visible evidence that supports the label.

## Independence requirements
The reviewer should not inspect any released checker output, audit CSV/JSON, manuscript result table, reviewer-response file, or organizer key until both forms are complete.

## Recommended design
Two independent reviewers are preferred. Each reviewer completes Phase A and Phase B independently. Preserve each completed form separately. Resolve disagreements only after the independent forms are frozen.

## Planned analysis
For the obligation-guided review:
- report raw agreement between reviewers per obligation;
- report Cohen's kappa where both labels vary and the statistic is defined;
- list every checker-versus-human disagreement by case and obligation;
- report confusion counts against the post-review adjudicated labels;
- report median and interquartile range of review time.

For the unaided baseline:
- report the number of cases with at least one issue found;
- map free-text issues to the four obligations only after the unaided review is frozen;
- compare issue coverage and review time with the obligation-guided phase.

No manuscript claim should use these results until completed forms and the adjudication record are archived.
