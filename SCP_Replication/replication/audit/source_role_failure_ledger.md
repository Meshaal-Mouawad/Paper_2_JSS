# Source-role comparison ledger: majority-Fail documents and checker alerts

This ledger contains 18 unique documents: all 16 majority-Fail documents and all four checker alerts. Two alerts (C09 and C18) belong to the majority-Fail set; the additional alerts C12 and C27 have majority-Pass labels. A matching document label does not establish that two reviewers identified the specific error flagged by the checker. Reviewer rationales are preserved in the JSON ledger alongside source text and generated descriptions. Classification below is the recovery auditor’s synthesis, not a new adjudicated reference.

| Case | Document | Votes R1/R2/R3 | Majority | Checker | Rationale topics | Why covered or missed |
|---|---|---|---|---|---|---|
| C01 | gross_margin_percentage.html | FAIL/FAIL/FAIL | FAIL | PASS | formula meaning; documentary comment role | Cross-field formula/source correspondence and conflict-comment classification exceed the two released patterns. |
| C05 | runtime_execution_latency.html | FAIL/FAIL/PASS | FAIL | PASS | metric meaning; executable-statement role | Business meaning versus eval/system execution is outside comment-executable and CAST-alias tests. |
| C06 | inventory_modification_gap.html | PASS/FAIL/FAIL | FAIL | PASS | documentary comment role; metric meaning | KPI-marker is excluded from executable-role prefixes; no semantic formula/business test. |
| C09 | flare_emission_recovery_rate.html | FAIL/FAIL/FAIL | FAIL | FAIL | ownership correspondence; comment/executable role | Checker catches ABAP comments described as executable/alias; R1/R2 judge owner fields. |
| C10 | compressor_vibration_index.html | FAIL/FAIL/FAIL | FAIL | PASS | documentary comment role | KPI-marker misclassification is outside executable-role prefixes. |
| C12 | ethylene_production_yield.html | PASS/PASS/FAIL | PASS | FAIL | docstring/executable role | Checker catches docstring described as an output alias; R3 identifies the same alias error, while R1/R2 record Pass. |
| C13 | eu_data_export_volume.html | FAIL/FAIL/FAIL | FAIL | PASS | documentary comment role; metric meaning | KPI-marker misclassification and export-procedure versus metric meaning exceed the patterns. |
| C14 | safe_execution_latency.html | FAIL/FAIL/FAIL | FAIL | PASS | documentary comment role; metric meaning | KPI-marker misclassification and length-versus-latency meaning exceed the patterns. |
| C15 | signed_lineage_audit_trail.html | FAIL/PASS/FAIL | FAIL | PASS | documentary comment role | KPI-marker misclassification is outside executable-role prefixes. |
| C16 | catalyst_replacement_frequency.html | FAIL/FAIL/FAIL | FAIL | PASS | source-system correspondence; documentary comment role | Source-system meaning and documentary roles exceed the two patterns. |
| C17 | procurement_contract_compliance_rate.html | FAIL/FAIL/FAIL | FAIL | PASS | formula provenance; documentary comment role | Declared versus inferred formula and descriptive/governance commentary exceed the patterns. |
| C18 | polymer_melt_flow_index_mfi_variance.html | FAIL/FAIL/FAIL | FAIL | FAIL | formula/source correspondence; comment/executable role | Checker catches ABAP comment described as calculation; R1/R2 judge formula-variable correspondence. |
| C19 | hse_safety_incident_rate.html | FAIL/FAIL/FAIL | FAIL | PASS | data-domain/owner correspondence; documentary comment role | Domain/ownership meaning and documentary roles exceed the patterns. |
| C23 | maintenance_to_operating_cost_ratio.html | FAIL/FAIL/PASS | FAIL | PASS | metric/formula correspondence | Variable meaning versus metric title is outside syntactic patterns. |
| C24 | customer_activity_index.html | FAIL/FAIL/FAIL | FAIL | PASS | documentary comment role; output/calculation role | Marker and executable print-as-calculation comparisons exceed comment-executable and CAST-alias patterns. |
| C25 | governed_inventory_modification.html | FAIL/PASS/FAIL | FAIL | PASS | documentary comment role | Audit-control comments as KPI markers exceed executable-role prefixes. |
| C27 | onspec_rate.html | PASS/PASS/FAIL | PASS | FAIL | cast-type/output-alias role | Checker catches FLOAT cast type described as output alias; R3 identifies the same discrepancy, while R1/R2 record Pass. |
| C28 | audit_trail_completeness.html | FAIL/FAIL/FAIL | FAIL | PASS | documentary comment role; metric meaning | Unsigned-trace annotation as KPI marker and completeness meaning exceed the patterns. |

## Matching labels at C09 and C18

At C09, R1/R2 cite HSE-versus-Finance ownership; R3 cites comment-role errors caught by the checker. At C18, R1/R2 cite formula/variable mismatch; R3 cites the comment/executable-role error caught by the checker. Therefore the result is **2 of 16 majority-Fail documents flagged**, not two of sixteen adjudicated individual errors detected.

## Reference-discordant alerts

C12 (Yield) and C27 (On-Spec) are checker Fail / majority Pass. R3 identifies the checker’s same concrete error: a Python docstring mapped to output alias `a`, and SQL cast type `FLOAT` mapped to output alias rather than `on_spec_percentage`. Source inspection supports these errors. The FP designation means discordance with the majority label; it does not establish that the alert is objectively false.

## Interpretation

The reference criteria were applied broadly: some votes concern ownership, formula meaning, data domains, output meaning, or formula provenance. Those judgments should remain reported judgments until independently adjudicated at the defect level. Positive source-role kappa does not validate all underlying rationales.

## Complete additional alert records

The following records retain the same fields as the majority-Fail cases in the JSON and CSV ledger.

### C12 — ethylene_production_yield.html

```json
{
  "case": "C12",
  "document": "ethylene_production_yield.html",
  "criterion": "source_role_accuracy",
  "R1": "PASS",
  "R2": "PASS",
  "R3": "FAIL",
  "majority": "PASS",
  "checker": "FAIL",
  "set_membership": "additional checker alert on majority-Pass document",
  "observed_rationale_topics": "docstring/executable role",
  "rule_coverage_explanation": "Checker catches docstring described as an output alias; R3 identifies the same alias error, while R1/R2 record Pass.",
  "source_file": "evidence/primary/artifact_28/dossiers/ethylene_production_yield.html",
  "source_description_pairs": [
    {
      "source_excerpt": "1 | def calculate_ethylene_yield_pct(ethylene_produced_tons: float, feedstock_input_tons: float) -> float:",
      "published_description": "Calculation expression: combines source variables used by the formal formula."
    },
    {
      "source_excerpt": "2 | \"\"\"Calculates ethylene production yield as a percentage of feedstock input.\"\"\"",
      "published_description": "Output alias: maps this expression to a in the result set."
    },
    {
      "source_excerpt": "3 | if feedstock_input_tons <= 0:",
      "published_description": "Source context: supports the KPI definition or execution boundary."
    },
    {
      "source_excerpt": "4 | return 0.0",
      "published_description": "Source context: supports the KPI definition or execution boundary."
    },
    {
      "source_excerpt": "5 | return (ethylene_produced_tons / feedstock_input_tons) * 100.0",
      "published_description": "Calculation expression: combines source variables used by the formal formula."
    }
  ],
  "checker_hits": [
    {
      "code": "\"\"\"Calculates ethylene production yield as a percentage of feedstock input.\"\"\"",
      "description": "Output alias: maps this expression to a in the result set.",
      "reason": "comment_or_docstring_assigned_executable_role"
    }
  ],
  "reviewer_rationales": {
    "R1": "SOURCE-ROLE: Roles correctly assigned. CONDITION: Zero guard (feedstock_input_tons<=0) disclosed. DISAGREEMENT: No conflict. REVIEW-AUTHORITY: Governance Validated; Trust consistent.",
    "R2": "Python yield formula and feedstock_input_tons <= 0 guard are visible and explicitly safeguarded; Validated state is consistent.",
    "R3": "Source-role: the Python docstring is incorrectly described as an output alias mapping to 'a'. Condition: feedstock_input_tons <= 0 returns 0, but Logic Safeguards omits that nonpositive-input branch. Disagreement: no separate explicit conflict is visible. Authority: Governance Status is Validated, the page says ready for governed use, and the visible business objective is populated; the main authority statements align with that state."
  },
  "exact_defect_match_assessment": "Checker error overlaps R3 rationale and directly inspected source; majority Pass does not make this an objectively false alert."
}
```

### C27 — onspec_rate.html

```json
{
  "case": "C27",
  "document": "onspec_rate.html",
  "criterion": "source_role_accuracy",
  "R1": "PASS",
  "R2": "PASS",
  "R3": "FAIL",
  "majority": "PASS",
  "checker": "FAIL",
  "set_membership": "additional checker alert on majority-Pass document",
  "observed_rationale_topics": "cast-type/output-alias role",
  "rule_coverage_explanation": "Checker catches FLOAT cast type described as output alias; R3 identifies the same discrepancy, while R1/R2 record Pass.",
  "source_file": "evidence/primary/artifact_28/dossiers/onspec_rate.html",
  "source_description_pairs": [
    {
      "source_excerpt": "1 | -- KPI: On-Spec Rate (%)",
      "published_description": "KPI marker: tells LEAP this nearby code defines or documents a KPI."
    },
    {
      "source_excerpt": "2 | -- Formula: \\mathrm{On\\text{-}Spec\\,\\%} = \\frac{\\mathrm{On\\text{-}Spec\\,Batches}}{\\mathrm{Total\\,Batches}} \\times 100",
      "published_description": "Calculation hint: documents the business expression expected inside the KPI implementation."
    },
    {
      "source_excerpt": "3 | CREATE VIEW kpi_on_spec_rate AS",
      "published_description": "Source context: supports the KPI definition or execution boundary."
    },
    {
      "source_excerpt": "4 | SELECT",
      "published_description": "Query entry point: starts the data-selection logic used to calculate the KPI."
    },
    {
      "source_excerpt": "5 | CAST(100.0 * on_spec_batches / NULLIF(total_batches, 0) AS FLOAT) AS on_spec_percentage",
      "published_description": "Output alias: maps this expression to FLOAT in the result set."
    },
    {
      "source_excerpt": "6 | FROM batch_quality_summary;",
      "published_description": "Source relation: identifies the table, view, or dataset read by the KPI."
    }
  ],
  "checker_hits": [
    {
      "code": "CAST(100.0 * on_spec_batches / NULLIF(total_batches, 0) AS FLOAT) AS on_spec_percentage",
      "description": "Output alias: maps this expression to FLOAT in the result set.",
      "reason": "cast_type_labeled_as_output_alias",
      "actual_alias": "on_spec_percentage"
    }
  ],
  "reviewer_rationales": {
    "R1": "SOURCE-ROLE: SQL view roles correctly assigned. CONDITION: NULLIF zero guard disclosed. DISAGREEMENT: No conflict. REVIEW-AUTHORITY: Governance Validated; Trust consistent.",
    "R2": "SQL expression, source table, and NULLIF denominator guard match the formal formula; Validated state is consistent.",
    "R3": "Source-role: the CAST expression is said to map the output alias to FLOAT, but FLOAT is the cast type; the actual alias is on_spec_percentage. Condition: NULLIF(total_batches,0) is accurately disclosed as the zero-denominator guard and Total Batches is the denominator. Disagreement: no explicit competing formula/source rule is visible. Authority: status says Validated/ready, while Decision/Business Context says owner confirmation is required before executive use."
  },
  "exact_defect_match_assessment": "Checker error overlaps R3 rationale and directly inspected source; majority Pass does not make this an objectively false alert."
}
```
