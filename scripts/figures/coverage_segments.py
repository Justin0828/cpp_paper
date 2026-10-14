"""Work sweep on two rectangles, plus one transfer in the full trajectory."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tikzfig import FIGURES, compile_tikz


BODY = r"""
\begin{tikzpicture}[x=1mm,y=1mm]
  \useasboundingbox (0,0) rectangle (\paperfullwidth, 74mm);
  \node[tag, anchor=north] at (40,8) {(a)};
  \node[tag, anchor=north] at (120,8) {(b)};

  \newcommand{\scene}[1]{%
    \begin{scope}[shift={(#1,0)}]
      \draw[region] (6,20) rectangle (34,52);
      \draw[region] (46,22) rectangle (74,50);
      \fill[workband] (8,24.2) rectangle (32,28.6);
      \fill[workband] (8,33.2) rectangle (32,37.6);
      \fill[workband] (8,42.2) rectangle (32,46.6);
      \fill[workband] (48,27.2) rectangle (72,31.6);
      \fill[workband] (48,39.2) rectangle (72,43.6);
      \draw[flow] (8,26.4) -- (32,26.4);
      \draw[flow] (32,35.4) -- (8,35.4);
      \draw[flow] (8,44.4) -- (32,44.4);
      \draw[flow] (48,29.4) -- (72,29.4);
      \draw[flow] (72,41.4) -- (48,41.4);
      \draw[aux] (34,44.4) .. controls (39,56) and (41,56) .. (46,41.4);
    \end{scope}%
  }
  \scene{0}
  \node[sym, anchor=south] at (40,58) {$\mathcal{C}_{\mathrm{work}}$};

  \scene{80}
  \foreach \pt in {(116.7,49.9), (118.4,52.2), (120.0,52.7), (121.6,51.5), (123.3,48.4)} {
    \draw[draw=secondary, fill=nonworkfill, line width=\lwaux] \pt circle[radius=1.8];
  }
  \draw[aux] (114,44.4) .. controls (119,56) and (121,56) .. (126,41.4);
  \node[sym, anchor=south] at (120,60) {$\mathcal{C}_{\mathrm{traj}}$};
\end{tikzpicture}
"""


def main() -> None:
    compile_tikz(BODY, FIGURES / "figure_coverage_segments.pdf")


if __name__ == "__main__":
    main()
