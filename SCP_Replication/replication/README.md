# Reproducibility companion

Preserved inputs are evidence/, evaluation_r15/, reporting_correction/, and generator_source/. Audit outputs and new reanalysis are in audit/. Original manifest files remain unchanged. The 18-document ledger includes all sixteen majority-Fail documents and all four checker alerts, with two overlaps. Reviewer-reference condition evidence is in audit/condition_reference_evidence.json.

Use Python 3.12 and install requirements_audit.txt. From this directory run `python run_packaged_audit.py`. The runner checks the preserved manifests, independently recomputes categorical results, reconstructs the case ledger, reexecutes two unchanged generator functions, and runs the ten released technical commands and four statistical commands in temporary copies. It never runs the entire LEAP generator. It writes audit/packaged_rerun.json and logs.

The independent reanalysis produces derived output files; it does not edit original reviewer forms. The original collection guidance contains differing versions and does not establish their distribution chronology. Majority labels are not adjudicated defect labels. See the separate scientific audit for interpretation and limitations.
