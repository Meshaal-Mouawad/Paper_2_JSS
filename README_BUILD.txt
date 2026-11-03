SCP research manuscript — editable LaTeX source

Build main.tex to main.pdf from this directory:

    bash build.sh

Alternatively:

    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

The source package includes the bibliography database and generated main.bbl,
required class/style files, and editable figure sources with matching vector PDFs.
The manuscript includes figures/checker_results.tex and
figures/sql_source_role.tex directly. Standalone figure PDFs can be regenerated
from this directory using:

    pdflatex -output-directory=figures figures/checker_results_standalone.tex
    pdflatex -output-directory=figures figures/sql_source_role_standalone.tex

The source and PDF belong to the same revised manuscript. Supporting evidence,
verification reports, and author-review declarations are provided separately.
