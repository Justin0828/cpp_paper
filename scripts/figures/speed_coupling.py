"""During T_half the chassis advances one disc diameter and the arm swings."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tikzfig import FIGURES, compile_tikz


BODY = r"""
\begin{tikzpicture}[x=1mm,y=1mm]
  \useasboundingbox (0,0) rectangle (\paperfullwidth, 92mm);
  % Chassis centers are one drawn disc diameter apart.
  \begin{scope}[shift={(70,52)}]
    \newcommand{\pose}[2]{%
      \begin{scope}[shift={(#1,0)}]
        \draw[arm] (3.6,0) -- ++(#2:22);
        \draw[chassis] (-3.6,-3.2) rectangle (3.6,3.2);
        \draw[disc] ($(3.6,0)+(#2:22)$) circle[radius=11];
        \fill[ink] (0,0) circle[radius=0.45];
        \fill[ink] (3.6,0) circle[radius=0.35];
      \end{scope}%
    }
    \pose{0}{-50}
    \pose{22}{50}

    % Only length dimension: center to center.
    \draw[guide] (0,3.2) -- (0,24);
    \draw[guide] (22,3.2) -- (22,24);
    \draw[dim] (0,24) -- (22,24);
    \node[sym, anchor=south] at (11,24.3) {$2r_d$};

    % Angle between each arm and the travel direction, inside the wedge.
    \draw[guide] (3.6,0) ++(0:7) arc[start angle=0, end angle=-50, radius=7];
    \node[sym, anchor=south] at ($(3.6,0)+(-25:11)$) {$-\phi_w$};
    \draw[guide] (25.6,0) ++(0:7) arc[start angle=0, end angle=50, radius=7];
    \node[sym, anchor=north] at ($(25.6,0)+(25:11)$) {$+\phi_w$};

    % Work speed on the travel line through the chassis centers.
    \draw[flow] (-28,0) -- (-4.4,0);
    \node[sym, anchor=south] at (-16,0.9) {$v_{\mathrm{work}}$};

    % Time axis. Not a length dimension.
    \draw[flow] (0,-38) -- (22,-38);
    \node[sym, anchor=north east] at (-0.8,-38.8) {$t=0$};
    \node[sym, anchor=north west] at (22.8,-38.8) {$t=T_{\mathrm{half}}$};
  \end{scope}
\end{tikzpicture}
"""


def main() -> None:
    compile_tikz(BODY, FIGURES / "figure_speed_coupling.pdf")


if __name__ == "__main__":
    main()
