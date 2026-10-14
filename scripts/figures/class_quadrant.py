"""Four CPP classes on map representation and robot-model fidelity."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tikzfig import FIGURES, compile_tikz


BODY = r"""
\begin{tikzpicture}[x=1mm,y=1mm]
  \useasboundingbox (0,0) rectangle (\paperfullwidth, 112mm);

  \draw[cell] (46,26) rectangle (98,62);
  \draw[cell] (104,26) rectangle (156,62);
  \draw[cell] (46,68) rectangle (98,104);
  \draw[cellon] (104,68) rectangle (156,104);

  \node[align=center, font=\fontsize{9}{10.8}\selectfont] at (72,50) {Idealized coverage};
  \node[align=center] at (72,38) {BCD\\[1.5pt]STC};

  \node[align=center, font=\fontsize{9}{10.8}\selectfont] at (130,51) {Map-enhanced};
  \node[align=center] at (130,37) {Polygon CPP\\[1pt]Fields2Cover\\[1pt]Nobleo};

  \node[align=center, font=\fontsize{9}{10.8}\selectfont] at (72,93) {Platform-constrained};
  \node[align=center] at (72,79) {Mobile manipulator\\[1.5pt]SatAOI};

  \node[align=center, font=\fontsize{9}{10.8}\selectfont] at (130,92)
    {Environment--platform\\coupled};
  \node[align=center, text=emphasis] at (130,76) {BiRect};

  \draw[flow] (46,16) -- (156,16);
  \node[anchor=north west] at (46,15.2) {idealized};
  \node[anchor=north east] at (156,15.2) {complex};
  \node[anchor=north, font=\fontsize{9}{10.8}\selectfont] at (101,8.2) {Map representation};

  \draw[flow] (38,26) -- (38,104);
  \node[anchor=east, align=right] at (36,32) {fixed\\footprint};
  \node[anchor=east] at (36,98) {base--arm--disc};
  \node[anchor=center, rotate=90, font=\fontsize{9}{10.8}\selectfont] at (8,65) {Robot model};
\end{tikzpicture}
"""


def main() -> None:
    compile_tikz(BODY, FIGURES / "figure_cpp_class_quadrant.pdf")


if __name__ == "__main__":
    main()
