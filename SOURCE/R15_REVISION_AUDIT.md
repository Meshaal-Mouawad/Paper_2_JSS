# R15 Production-Layout Audit

## Scope

R15 addresses only Listing 1 spacing/alignment and provides direct visual evidence for the production items that external text extraction has represented inconsistently. Scientific content is unchanged.

## Source change

R14 used a `\columnwidth` minipage around the listing and `\medskipamount`. R15 removes that wrapper and uses native `listings` flow.

The listing now uses:

- `aboveskip=\intextsep`
- `belowskip=\intextsep`
- `xleftmargin=\fboxsep`
- `xrightmargin=\fboxsep`
- `breaklines=true`
- `breakatwhitespace=true`

Source scan confirms zero `\vspace`, zero `\hspace`, and zero listing minipage wrappers.

## Visual result

On rendered page 7, Listing 1 is separated from the preceding prose by the same class-defined in-text separation used for in-flow objects. Its frame is inset symmetrically using the TeX frame-box separation parameter, and its content remains inside the left column. The listing and caption are fully visible and do not overlap the right column.

## Production text checks

R15 PDF/layout extraction confirms:

- `if feedstock_input_tons <= 0:` present;
- Table 5 `<= 0 branch counted as` present;
- Table 6 full caption present;
- `repared`: 0;
- `checkere`: 0.

Source confirms:

- `NULLIF(variable,0)`;
- `<= 0` semantics;
- `dossier` wording;
- `reader-facing criterion`;
- `each retained claim and each failure mode inspectable`;
- FastAPI commit `33d411dbc3236275dd64d200bfe18d5d60a49b2e`.

## Regression and evidence gates

- R14→R15 visual diff: 1/10 pages changed, page 7 only.
- Exact source-ZIP rebuild: 0/10 changed pages.
- PDF remains 10 pages and 4,898 TeXcount words.
- Frozen technical supplement: 155/155 manifest PASS.
- Technical reproduction: 10/10 PASS.
- R5 verifier: 27/27 PASS.
- Release verifier: 26/26 PASS.
- Independent-evaluation manifest: 46/46 PASS.
- Independent analysis scripts rerun successfully.
- `git diff --check`: PASS.
- Audit Git working tree: clean.

## Disposition

Production alignment gate closed. No scientific content changed.
