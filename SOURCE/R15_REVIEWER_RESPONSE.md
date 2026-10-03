# Response to IST R14 Production Assessment — R15

## Disposition

R15 is a production-only correction. Scientific content, tables, numerical results, independent-review data, citations, and frozen evidence are unchanged from R14.

## Listing 1 alignment repair

The remaining author-visible issue was that Listing 1 still appeared visually attached to the sentence above it and its framed box did not align as cleanly as the surrounding column material.

R15 removes the minipage wrapper and returns Listing 1 to native `listings` column flow. Spacing and alignment are derived from the document class and TeX box parameters rather than hard-coded distances:

- above/below separation: `\intextsep`;
- symmetric listing margins: `\fboxsep`;
- no `\vspace`;
- no `\hspace`;
- no minipage wrapper;
- no manual page break;
- no coordinates or pixel offsets.

The existing `\FloatBarrier` remains at the Section 4 / Section 5 semantic boundary so Section 4 tables cannot cross into the detailed-case section.

The resulting page 7 shows normal separation from the introductory sentence, a frame aligned with the left-column content, the complete unsplit code excerpt, and a normal listing caption below it.

## Visual verification of previously disputed extraction items

Direct renders of the submitted PDF are included in `EDITOR_VISUAL_VERIFICATION_R15.zip`.

- Page 4 visually shows `NULLIF(variable,0)` and `<= 0` guard semantics.
- Page 5 visually shows `<= 0` semantics in the root-cause discussion and uses `dossier` rather than the extraction corruption `decision`.
- Page 7 visually shows Listing 1 with `if feedstock_input_tons <= 0:`, Table 5 with `feedstock_input_tons <= 0`, and the full Table 6 caption.
- The Section 5.1 criterion paragraph appears once.
- Page 9 visually shows `reader-facing criterion` and `each failure mode inspectable`.
- Pages 9–10 show one continuous unnumbered author-year reference list.
- The FastAPI commit remains `33d411dbc3236275dd64d200bfe18d5d60a49b2e` in source and rendered reference output.

Layout-aware PDF extraction from R15 also contains the exact Listing 1 guard, Table 5 `<= 0` wording, and the Table 6 caption, and contains zero occurrences of `repared` or `checkere`.

## Verification

- PDF: 10 pages.
- R14→R15 rendered diff: page 7 only.
- Exact R15 source-ZIP rebuild: 0/10 changed rendered pages.
- `git diff --check`: PASS.
- Final local audit Git status: clean.
- Frozen technical supplement: 155/155 manifest PASS before and after reproduction.
- Ten documented technical reproduction commands: PASS.
- R5 technical verifier: 27/27 PASS.
- Release verifier: 26/26 PASS.
- Independent-evaluation manifest: 46/46 PASS before and after analysis reruns.

No scientific revision was introduced.
