#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
else
  command -v pdflatex >/dev/null 2>&1 || { echo 'pdflatex missing' >&2; exit 1; }
  command -v bibtex >/dev/null 2>&1 || { echo 'bibtex missing' >&2; exit 1; }
  pdflatex -interaction=nonstopmode -halt-on-error main.tex
  bibtex main
  pdflatex -interaction=nonstopmode -halt-on-error main.tex
  pdflatex -interaction=nonstopmode -halt-on-error main.tex
fi
