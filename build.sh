#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
if command -v latexmk >/dev/null 2>&1; then
    exec latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
fi
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if command -v bibtex >/dev/null 2>&1; then bibtex main; else /usr/bin/bibtex.original main; fi
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
