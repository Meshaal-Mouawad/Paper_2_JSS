# R11 condition-criterion sensitivity audit

The R10 review identified a criterion ambiguity in condition disclosure. This audit recomputes the released condition checker on the same ten checker-eligible cases under the two disclosure criteria actually observed in the independent reviewer data.

- **Source visibility (R1/R2):** TP=2, FP=3, FN=0, TN=5, precision=0.40, recall=1.00.
- **Reader-facing publication (R3):** TP=5, FP=0, FN=0, TN=5, precision=1.00, recall=1.00.

R1 and R2 provide identical labels on all ten checker-eligible condition cases. R3 provides an explicit label on all ten. The calculation changes no reviewer label and no checker output. It isolates the effect of the disclosure definition on the reported condition-rule precision.
