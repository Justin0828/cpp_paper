"""Work sweep versus full-trajectory sweep on one shared path."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tikzfig import FIGURES, compile_tikz


BODY = r"""
\begin{tikzpicture}[x=1mm,y=1mm]
  \useasboundingbox (0,0) rectangle (\paperfullwidth, 96mm);
  \node[tag, anchor=north] at (40,11) {(a)};
  \node[tag, anchor=north] at (116,11) {(b)};

  \fill[workband] (46,89) rectangle (52,93.2);
  \node[anchor=west] at (53.2,91.1) {work sweep};
  \fill[secondary, fill opacity=0.40] (88,89) rectangle (94,93.2);
  \node[anchor=west] at (95.2,91.1) {non-work sweep};

  \newcommand{\workbands}{%
    \fill[workband] (10,21.8) rectangle (30,26.2);
    \fill[workband] (10,31.8) rectangle (30,36.2);
    \fill[workband] (10,41.8) rectangle (30,46.2);
    \fill[workband] (52,23.8) rectangle (70,28.2);
    \fill[workband] (52,35.8) rectangle (70,40.2);
  }
  \newcommand{\routepaths}{%
    \draw[flow] (11,24) -- (29,24);
    \draw[flow] (29,34) -- (11,34);
    \draw[flow] (11,44) -- (29,44);
    \draw[flow] (53,26) -- (69,26);
    \draw[flow] (69,38) -- (53,38);
    \draw[aux] (30,24) .. controls (35.2,24) and (35.2,34) .. (30,34);
    \draw[aux] (10,34) .. controls (4.8,34) and (4.8,44) .. (10,44);
    \draw[aux] (70,26) .. controls (75.2,26) and (75.2,38) .. (70,38);
    \draw[aux] (30,44) .. controls (40,58) and (48,52) .. (52,26);
  }
  % Disc-diameter band along the lane changes and the transfer. Same width as the orange strips.
  \newcommand{\nonworkband}{%
    \fill[secondary, fill opacity=0.40]
      (30.00,26.20) -- (30.39,26.25) -- (30.66,26.37) -- (30.92,26.58) -- (31.18,26.91)
      -- (31.42,27.39) -- (31.59,27.99) -- (31.69,28.65) -- (31.69,29.35) -- (31.59,30.01)
      -- (31.42,30.61) -- (31.18,31.09) -- (30.92,31.42) -- (30.66,31.63) -- (30.39,31.75)
      -- (30.00,31.80) -- (30.00,36.20) -- (31.56,35.99) -- (32.94,35.40) -- (34.07,34.50)
      -- (34.92,33.41) -- (35.52,32.21) -- (35.89,30.95) -- (36.08,29.65) -- (36.08,28.35)
      -- (35.89,27.05) -- (35.52,25.79) -- (34.92,24.59) -- (34.07,23.50) -- (32.94,22.60)
      -- (31.56,22.01) -- (30.00,21.80) -- cycle;
    \fill[secondary, fill opacity=0.40]
      (10.00,31.80) -- (8.44,32.01) -- (7.06,32.60) -- (5.93,33.50) -- (5.08,34.59)
      -- (4.48,35.79) -- (4.11,37.05) -- (3.92,38.35) -- (3.92,39.65) -- (4.11,40.95)
      -- (4.48,42.21) -- (5.08,43.41) -- (5.93,44.50) -- (7.06,45.40) -- (8.44,45.99)
      -- (10.00,46.20) -- (10.00,41.80) -- (9.61,41.75) -- (9.34,41.63) -- (9.08,41.42)
      -- (8.82,41.09) -- (8.58,40.61) -- (8.41,40.01) -- (8.31,39.35) -- (8.31,38.65)
      -- (8.41,37.99) -- (8.58,37.39) -- (8.82,36.91) -- (9.08,36.58) -- (9.34,36.37)
      -- (9.61,36.25) -- (10.00,36.20) -- cycle;
    \fill[secondary, fill opacity=0.40]
      (70.00,28.20) -- (70.28,28.24) -- (70.51,28.36) -- (70.79,28.64) -- (71.10,29.12)
      -- (71.37,29.79) -- (71.58,30.61) -- (71.69,31.53) -- (71.69,32.47) -- (71.58,33.39)
      -- (71.37,34.21) -- (71.10,34.88) -- (70.79,35.36) -- (70.51,35.64) -- (70.28,35.76)
      -- (70.00,35.80) -- (70.00,40.20) -- (71.66,39.94) -- (73.10,39.20) -- (74.20,38.14)
      -- (75.00,36.91) -- (75.56,35.57) -- (75.91,34.17) -- (76.08,32.73) -- (76.08,31.27)
      -- (75.91,29.83) -- (75.56,28.43) -- (75.00,27.09) -- (74.20,25.86) -- (73.10,24.80)
      -- (71.66,24.06) -- (70.00,23.80) -- cycle;
    \fill[secondary, fill opacity=0.40]
      (28.21,45.28) -- (30.30,47.97) -- (32.40,50.15) -- (34.53,51.84) -- (36.76,52.99)
      -- (39.09,53.53) -- (41.44,53.34) -- (43.63,52.41) -- (45.55,50.89) -- (47.22,48.85)
      -- (48.70,46.33) -- (50.03,43.33) -- (51.24,39.85) -- (52.33,35.85) -- (53.31,31.35)
      -- (54.17,26.33) -- (49.83,25.67) -- (48.99,30.51) -- (48.05,34.81) -- (47.03,38.55)
      -- (45.94,41.73) -- (44.78,44.34) -- (43.60,46.35) -- (42.43,47.78) -- (41.35,48.65)
      -- (40.38,49.06) -- (39.43,49.14) -- (38.32,48.88) -- (36.95,48.16) -- (35.38,46.91)
      -- (33.64,45.10) -- (31.79,42.72) -- cycle;
  }

  \begin{scope}[shift={(2,16)}]
    \draw[region] (6,18) rectangle (36,52);
    \draw[region] (48,20) rectangle (74,48);
    \workbands
    \routepaths
    \node[sym, anchor=south] (cw) at (18,55.5) {$\mathcal{C}_{\mathrm{work}}$};
    \draw[guide] (cw.south) -- (18,46.2);
  \end{scope}
  \begin{scope}[shift={(78,16)}]
    \draw[region] (6,18) rectangle (36,52);
    \draw[region] (48,20) rectangle (74,48);
    \nonworkband
    \workbands
    \routepaths
    \node[sym, anchor=south] (ct) at (40,61) {$\mathcal{C}_{\mathrm{traj}}$};
    \draw[guide] (ct.south) -- (40,52.2);
  \end{scope}
\end{tikzpicture}
"""


def main() -> None:
    compile_tikz(BODY, FIGURES / "figure_coverage_segments.pdf")


if __name__ == "__main__":
    main()
