# English LaTeX paper

This directory contains the standalone English version of the paper. The text
is written in standard LaTeX, with section sources in `sections/`, figures in
`figures/`, and bibliography data in `refs.bib`.

Compile from this directory with:

```bash
latexmk -pdf -outdir=build main.tex
```

The rendered paper is written to `build/main.pdf`.
