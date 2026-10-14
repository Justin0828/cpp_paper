"""Entry pose, work strips, and swing amplitude for one rectangle."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tikzfig import FIGURES, compile_tikz


BODY = r"""
\begin{tikzpicture}[x=1mm,y=1mm]
  \useasboundingbox (0,0) rectangle (\paperfullwidth, 68mm);
  \node[tag, anchor=north] at (26,8) {(a)};
  \node[tag, anchor=north] at (82,8) {(b)};
  \node[tag, anchor=north] at (136,8) {(c)};

  % (a) retracted entry on the left boundary, heading outward.
  \draw[region] (20,22) rectangle (48,50);
  \draw[arm] (11.2,36) -- (20,36);
  \draw[chassis] (3.4,32.8) rectangle (11.2,39.2);
  \draw[disc] (20,36) circle[radius=4.0];
  \fill[ink] (20,36) circle[radius=0.45];
  \fill[ink] (7.3,36) circle[radius=0.4];
  \draw[guide] (7.3,39.2) -- (7.3,55);
  \draw[guide] (20,40) -- (20,55);
  \draw[dim] (7.3,55) -- (20,55);
  \node[sym, anchor=south] at (13.6,55.3) {$d_p+L$};
  \draw[flow] (7.3,29.6) -- (2.2,29.6);
  \node[sym, anchor=north] at (4.6,29.2) {$\theta$};

  % (b) strips along the long side.
  \draw[region] (64,24) rectangle (100,50);
  \draw[aux] (64,32.667) -- (100,32.667);
  \draw[aux] (64,41.333) -- (100,41.333);
  \fill[emphasis] (64,24) circle[radius=0.75];
  \draw[guide] (64,24) -- (64,17.5);
  \draw[guide] (100,24) -- (100,17.5);
  \draw[dim] (64,17.5) -- (100,17.5);
  \node[sym, anchor=north] at (82,17.1) {$\ell_R$};
  \draw[guide] (100,24) -- (106,24);
  \draw[guide] (100,50) -- (106,50);
  \draw[dim] (106,24) -- (106,50);
  \node[sym, anchor=west] at (106.4,37) {$h_R$};
  \draw[guide] (64,24) -- (58.5,24);
  \draw[guide] (64,32.667) -- (58.5,32.667);
  \draw[dim] (58.5,24) -- (58.5,32.667);
  \node[sym, anchor=east] at (58.1,28.3) {$w_s$};
  \node[sym, anchor=south] at (82,50.3) {$N_s$};

  % (c) half-amplitude that brings the disc edge to the strip boundary.
  \begin{scope}[shift={(122,39)}]
    \draw[main] (-4,12.43) -- (20,12.43);
    \draw[main] (-4,-12.43) -- (20,-12.43);
    \draw[aux] (-4,0) -- (20,0);
    \draw[arm] (0,0) -- (36:14);
    \draw[arm] (0,0) -- (-36:14);
    \draw[disc] (36:14) circle[radius=4.2];
    \draw[disc] (-36:14) circle[radius=4.2];
    \fill[ink] (0,0) circle[radius=0.45];
    \draw[guide] (0,0) ++(36:6.5) arc[start angle=36, end angle=-36, radius=6.5];
    \node[sym, anchor=west] at (7.2,2.3) {$\phi_w$};
    \node[sym, anchor=west] at (7.2,-3.6) {$-\phi_w$};
    \node[sym, anchor=south] at (34:8.6) {$L$};
    \draw[guide] (36:14) -- ++(0:4.2);
    \node[sym, anchor=west] at ($(36:14)+(0:5.0)$) {$r_d$};
    \draw[guide] (20,12.43) -- (24.5,12.43);
    \draw[guide] (20,-12.43) -- (24.5,-12.43);
    \draw[dim] (24.5,-12.43) -- (24.5,12.43);
    \node[sym, anchor=west] at (25,0) {$w_s$};
  \end{scope}
\end{tikzpicture}
"""


def main() -> None:
    compile_tikz(BODY, FIGURES / "figure_strip_geometry.pdf")


if __name__ == "__main__":
    main()
