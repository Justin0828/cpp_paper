"""Compile one TikZ figure. Colors and stroke widths stay in paperstyle.tex."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STYLE = ROOT / "figures" / "style" / "paperstyle.tex"
FIGURES = ROOT / "english_paper" / "figures"


def compile_tikz(body: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    work = dest.parent / f".build-{dest.stem}"
    if work.exists():
        for old in work.iterdir():
            old.unlink()
    else:
        work.mkdir(parents=True)
    tex = work / "fig.tex"
    tex.write_text(
        "\n".join(
            [
                r"\documentclass[tikz,border=0pt]{standalone}",
                r"\usepackage{newtxtext,newtxmath}",
                r"\usepackage{amsmath}",
                r"\usetikzlibrary{arrows.meta,calc}",
                r"\input{" + str(STYLE) + "}",
                r"\begin{document}",
                body,
                r"\end{document}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "fig.tex"],
        cwd=work,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    dest.write_bytes((work / "fig.pdf").read_bytes())
    print(dest)
