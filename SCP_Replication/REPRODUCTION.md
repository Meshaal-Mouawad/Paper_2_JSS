# Reproducing Paper 2 results

## Environment

- Python 3.12 recommended.
- Read [`replication/requirements_audit.txt`](replication/requirements_audit.txt) for archived tested dependency versions.
- Run from the root of `SCP_Replication/replication`.

```bash
cd replication
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements_audit.txt
python run_packaged_audit.py
```

The complete runner independently recomputes the principal statistics, constructs the 18-document source-role ledger, reproduces two preserved generator functions, runs the ten archived checker/technical commands and four archived statistical commands, and validates hashes. Logs and derived values are recorded under `replication/audit/`. The runner uses temporary copies of archived evidence for its longer checks.

**The runner does not rebuild the entire LEAP application output.** It tests preserved outputs and reexecutes the specifically identified code paths. This is the scope of reproducibility established by the study.

## Key outputs

- `replication/audit/independent_recompute.json`: independent label and statistic calculations.
- `replication/audit/source_role_failure_ledger.csv`: all 16 majority-Fail source-role documents and two additional checker alerts, with source evidence and reviewer explanations.
- `replication/audit/condition_reference_evidence.json`: reviewer-reference condition comparisons.
- `replication/audit/packaged_rerun.json`: results of full bundled reproduction; see linked logs.
- `replication/reporting_correction/LABEL_RECONCILIATION.csv`: every original rating compared with derived forms.
- `replication/evidence/method/CHECKER_CONTROL_ORACLE.csv`: archived expected results for prepared controls.

If you prefer to run each archived technical command separately, see `replication/evidence/README.md`, `replication/audit/rerun_commands.json`, and `replication/audit/evaluation_rerun_commands.json`.

## Manuscript-to-evidence mapping

Use `INPUT_OUTPUT_MAP.md` to find evidence for 28 documents, 336 ratings, 32 controls, the two 2/16 overlapping Fail documents, and the 2/5 vs 5/5 condition comparison. All paths are relative to this directory.
