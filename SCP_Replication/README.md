# Replication materials — Science of Computer Programming, Paper 2

**Paper:** *Evaluating Checks for Generated KPI Documentation: Rule Coverage and Reference Criteria*  
**Author manuscript:** SCICO-D-26-00865  
**Authors:** Meshaal Obaid Mouawad and Bryan A. Jones  

This directory supplies the inputs, human-review instructions, scripts, original assessments, generated documents, checker outputs, intermediate comparisons, and analysis files supporting the paper. The primary study evaluates 28 generated KPI documents, 32 checker controls, and 336 ratings from three code reviewers.

## Start here

- [`REPRODUCTION.md`](REPRODUCTION.md) — how to reproduce the calculations and checks.
- [`INPUT_OUTPUT_MAP.md`](INPUT_OUTPUT_MAP.md) — locate every major input, processing script, output, and manuscript result.
- [`PROMPTS_AND_INSTRUCTIONS.md`](PROMPTS_AND_INSTRUCTIONS.md) — review questions and instructions used during the human evaluation, and the status of software/model prompts.
- [`RESEARCH_INTEGRITY.md`](RESEARCH_INTEGRITY.md) — original versus derived data, limitations, reviewer privacy, and revision history.
- [`replication/`](replication/) — exact preserved research records from the scientific recovery package, with a runnable independent analysis.

## Central verified findings

1. The checker returned all 32 prespecified outcomes on prepared controls. Those are **implementation conformance tests**, rather than an estimate of real-world diagnostic accuracy.
2. Among 16 documents receiving a source-role Fail from the reviewer majority, the checker assigned Fail to two. The checker and the majority gave different reasons in both overlapping cases; matching document labels is not confirmation of detecting the same defect.
3. For ten eligible condition documents, unchanged checker alerts align with 2 of 5 Fail decisions from reviewers A/B and 5 of 5 Fail decisions from reviewer C. These are recorded reviewer references; the original notes do not establish a controlled comparison of two uniformly applied disclosure rubrics.
4. The 336 original obligation ratings consist of 112 Pass, 130 Fail, and **94 explicit N/A**, with zero missing ratings. The archived R15 intermediate returns have blanks at the 94 N/A positions; reconciliation is documented.

## Availability and history

This repository directory is assembled for the SCP Editor-in-Chief's request to make the evidence publicly accessible. Earlier files bear JSS and R15 labels because they are the preserved historical inputs. The current scientific interpretation is the revised SCP paper and the documents in this directory, not a renamed copy of the earlier JSS manuscript.

**Release status:** Author approval and public GitHub accessibility must be confirmed before citing this folder as publicly available. See `RELEASE_CHECKLIST.md`.

## Manuscript

The only authoritative manuscript files are [`../main.tex`](../main.tex) and [`../main.pdf`](../main.pdf) at repository root.
