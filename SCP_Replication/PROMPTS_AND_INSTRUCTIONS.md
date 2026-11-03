# Experimental prompts, reviewer questions, and analysis instructions

The Editor-in-Chief requested all data, **prompts**, outcomes, and analysis. In this research, the relevant experimental prompts were the written tasks given to code reviewers and the fixed specifications supplied to the deterministic checker. The evaluated LEAP generation path recorded deterministic detail preparation. An LLM prompt was not part of the evaluated generator's output path.

## Original reviewer task instructions (preserved verbatim)

1. `replication/reporting_correction/REVIEWER_GUIDANCE.md`: the actual independent-review task instructions. Phase A asks for free-form observations; Phase B specifies four questions about source roles, conditions, disagreement, and review authority.
2. `replication/reporting_correction/REVIEWER_PACKET_README.md`: distributed packet's instructions and exclusions.
3. `replication/reporting_correction/COLLECTION_AND_ANALYSIS_GUIDANCE.md`: organizer instructions and planned aggregation; it differs from the packet about reviewer count and the agreement statistic. Both originals are preserved.
4. `replication/evaluation_r15/LEAP_Paper2_IST_R15_REVISION_PACKAGE/Independent_Evaluation_R15/independent_evaluation/INDEPENDENT_EVALUATION_PACKET/INDEPENDENT_EVALUATION_PACKET/README.md`: preserved blank packet's task text and phase ordering.
5. `replication/evaluation_r15/LEAP_Paper2_IST_R15_REVISION_PACKAGE/Independent_Evaluation_R15/independent_evaluation/INDEPENDENT_EVALUATION_PACKET/INDEPENDENT_EVALUATION_PACKET/ANALYSIS_PLAN.md`: original planned analysis text.

## Checker inputs and executable criteria

- `replication/evidence/method/AUDIT_PROTOCOL_R3.md`, `AUDIT_PROTOCOL_R4.md`, `AUDIT_PROTOCOL_R5.md`: successive historical specification documents.
- `replication/evidence/method/CHECKER_CONTROL_ORACLE.csv` and `ARTIFACT_MUTATION_ORACLE.csv`: the test inputs and expected outcomes, specified separately from checker output.
- `replication/evidence/method/audit_rules.py`: the programmed rules that apply those checks.
- `replication/evidence/external_fastapi/source/`: pinned public source files for the additional adapter exercise.

## Distinction from manuscript-preparation prompts

The AI-assistance declaration in the manuscript concerns literature discovery, source checking, language editing, and retrospective reanalysis. Those preparation activities are separate from the original code-reviewer study and deterministic experimental tests. The exact 325-line task prompt submitted for the subsequent ChatGPT Work scientific recovery was recovered from the user’s archived file and is provided at `prompts/Work_scientific_recovery_task_prompt.txt`. Individual messages or subagent prompts that may have occurred during that Work task were not present in the recovered experimental archive. The package does not claim to reproduce those private interactions. The executable analyses and exact reviewer task instructions needed to recalculate the reported measurements are included.

If the journal asks for the full sequence of AI-assistant interactions beyond the initiating task prompt, an author export of the Work conversation and any subagent logs would be required. Do not fabricate a replacement prompt or describe a later reconstruction as the original instruction.
