"""Shared type and color setup for the class-B figure scripts."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager


NAVY = "#173B5E"
SLATE = "#415A77"
INK = "#1D2939"
RULE = "#B7C4D1"
WORK = "#42678D"
WORK_WASH = "#D6E2EE"
NONWORK = "#6B7280"
NONWORK_WASH = "#E6E4E1"
PAPER = "#FFFFFF"

_FONT_DIR = Path("/usr/share/fonts/opentype/urw-base35")


def use_serif() -> None:
    """Use Nimbus Roman, the Times-metric face installed on this host."""
    for path in sorted(_FONT_DIR.glob("NimbusRoman-*.otf")):
        font_manager.fontManager.addfont(str(path))
    plt.rcParams.update(
        {
            "font.family": "Nimbus Roman",
            "font.size": 11,
            "axes.unicode_minus": False,
            "mathtext.fontset": "custom",
            "mathtext.rm": "Nimbus Roman",
            "mathtext.it": "Nimbus Roman:italic",
            "mathtext.bf": "Nimbus Roman:bold",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.facecolor": "white",
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.04,
        }
    )


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def figures_dir() -> Path:
    path = repo_root() / "english_paper" / "figures"
    path.mkdir(parents=True, exist_ok=True)
    return path
