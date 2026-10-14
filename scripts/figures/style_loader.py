"""Load paper.mplstyle and the named colors from paperstyle.tex."""

from __future__ import annotations

import re
from pathlib import Path

from matplotlib import font_manager
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
MPLSTYLE = ROOT / "figures" / "style" / "paper.mplstyle"
TEXSTYLE = ROOT / "figures" / "style" / "paperstyle.tex"
FONT_DIR = Path("/usr/share/fonts/opentype/urw-base35")


def load() -> dict[str, str]:
    for path in sorted(FONT_DIR.glob("NimbusRoman-*.otf")):
        font_manager.fontManager.addfont(str(path))
    plt.style.use(MPLSTYLE)
    text = TEXSTYLE.read_text(encoding="utf-8")
    colors = {
        name: "#" + hex_digits
        for name, hex_digits in re.findall(
            r"\\definecolor\{(\w+)\}\{HTML\}\{([0-9A-Fa-f]{6})\}",
            text,
        )
    }
    sheet = MPLSTYLE.read_text(encoding="utf-8")
    colors["__full_in"] = re.search(r"inclusion\.full_in:\s*([0-9.]+)", sheet).group(1)
    colors["__speed_in"] = re.search(r"inclusion\.speed_in:\s*([0-9.]+)", sheet).group(1)
    return colors


def inches(colors: dict[str, str], key: str) -> float:
    return float(colors[key])


def stroke(which: str) -> float:
    """Return the styled stroke in points. which is 'main' or 'aux'."""
    if which == "main":
        return float(plt.rcParams["lines.linewidth"])
    if which == "aux":
        return float(plt.rcParams["grid.linewidth"])
    raise KeyError(which)
