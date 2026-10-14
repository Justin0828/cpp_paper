"""Base advance of one disc diameter during a half-swing."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tikzfig import FIGURES, compile_tikz


BODY = r"""
\begin{tikzpicture}[x=1mm,y=1mm]
  \useasboundingbox (0,0) rectangle (\paperfullwidth, 84mm);
  \begin{scope}[shift={(16,5)}, scale=1.18]
  \newcommand{\pose}[2]{%
    \begin{scope}[shift={(#1,32)}]
      \draw[arm] (0,0) -- (#2:15);
      \draw[chassis] (-3.6,-2.6) rectangle (3.6,2.6);
      \draw[disc] (#2:15) circle[radius=6];
      \fill[ink] (0,0) circle[radius=0.4];
    \end{scope}%
  }
  \pose{64}{-52}
  \pose{76}{52}

  \draw[guide] (64,36) -- (64,53);
  \draw[guide] (76,36) -- (76,53);
  \draw[dim] (64,53) -- (76,53);
  \node[sym, anchor=south] at (70,53.2) {$2r_d$};
  \draw[guide] (64,53) -- (64,59.5);
  \draw[guide] (76,53) -- (76,59.5);
  \draw[dim] (64,59.5) -- (76,59.5);
  \node[sym, anchor=south] at (70,59.7) {$T_{\mathrm{half}}$};

  \draw[flow] (46,32) -- (58,32);
  \node[sym, anchor=east] at (45.2,32) {$v_{\mathrm{work}}$};
  \node[sym, anchor=north] at (70,15.5) {$-\phi_w$};
  \node[sym, anchor=south] at (90,48) {$+\phi_w$};
  \end{scope}
\end{tikzpicture}
"""


def main() -> None:
    compile_tikz(BODY, FIGURES / "figure_speed_coupling.pdf")


if __name__ == "__main__":
    main()
