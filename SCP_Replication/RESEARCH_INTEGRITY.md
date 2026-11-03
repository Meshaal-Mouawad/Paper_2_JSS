# Scope, interpretation, privacy, and preserved records

**Original labels.** The original returned Phase B forms record 112 PASS, 130 FAIL and 94 literal NA labels (336 total, zero missing). In an intermediate R15 file, those 94 NA cells appear as blanks. `replication/reporting_correction/LABEL_RECONCILIATION.csv` records the original-to-derivative relationship. The original returns remain intact.

**Units.** The source-role checker and the reviewer majority assign labels to whole documents, not individually matched errors. Both shared Fail cases (C09 and C18) refer to different underlying problems in the majority explanation versus the checker rule. The 2/16 number is a document-label comparison, not a verified defect-level detection rate.

**Condition judgments.** The 40% and 100% numbers are agreement with A/B and C's recorded decisions over the same five alerts. The original notes do not show a controlled experiment with two systematically applied disclosure definitions.

**Reviewers.** The three reviewers are labeled A/B/C or R1/R2/R3. Their actual professions and experience were not recorded in the original forms. Individual names must not be inferred from unrelated archive filenames.

**Prompts.** Human reviewer instructions and checker criteria are archived. The evaluated generator path was deterministic; no LLM-based prompting was used to generate the reported data. Manuscript preparation with AI tools was declared separately.

**Incomplete reproduction boundary.** This package reexecutes the archived technical checks, statistical scripts, and two selected generator functions, **not the entire end-to-end LEAP construction pipeline**. Historical and alternative-input results are from the same implementation and do not establish independent generator replication.

**Privacy / source provenance.** A small number of historical generated HTML files contain developer-machine links (e.g., `vscode://file/Users/...` and `pycharm://open?...`). They are retained because the archive is meant to preserve byte-exact historical evidence. Before public release, the author should confirm permission to expose these paths. Original reviewer records should also be checked for personal or confidential content before their release. All identified non-author email addresses in the available source examples use the synthetic `enterprise.example` domain.

**Licensing.** No public redistribution license is granted merely by preparing this ZIP. The author should select a suitable license for original code/data and retain upstream third-party notices for included FastAPI examples. Publishing the existing GitHub repository also exposes its older JSS archives, which must be reviewed separately. This package has not been publicly released by ChatGPT.
