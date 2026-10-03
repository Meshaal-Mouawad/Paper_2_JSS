#!/usr/bin/env bash
set -euo pipefail
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if command -v bibtex >/dev/null 2>&1; then bibtex main; else /usr/bin/bibtex.original main; fi
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
