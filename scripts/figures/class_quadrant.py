"""Quadrant sketch of the four existing CPP classes (revision 25).

Axes follow the advisor note: map representation increases to the right,
robot-model fidelity increases upward. Each method is drawn in the single
class Table 1 already assigns. No experimental map is used.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from matplotlib.patches import FancyBboxPatch
import matplotlib.pyplot as plt

from paper_style import INK, NAVY, RULE, SLATE, figures_dir, use_serif


def _cell(ax, x, y, w, h, face, title, lines, emphasize=False):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.012,rounding_size=0.08",
        facecolor=face,
        edgecolor=NAVY if emphasize else RULE,
        linewidth=1.8 if emphasize else 1.0,
        mutation_aspect=0.6,
        zorder=2,
    )
    ax.add_patch(patch)
    title_lines = title.count("\n") + 1
    ax.text(
        x + w / 2,
        y + h - 0.28,
        title,
        ha="center",
        va="top",
        fontsize=12,
        color=NAVY,
        fontweight="bold",
        linespacing=1.15,
        zorder=3,
    )
    ax.text(
        x + w / 2,
        y + (h - 0.55 * title_lines) / 2,
        "\n".join(lines),
        ha="center",
        va="center",
        fontsize=11,
        color=INK,
        linespacing=1.45,
        zorder=3,
    )


def main() -> None:
    use_serif()
    fig, ax = plt.subplots(figsize=(7.6, 6.15))
    ax.set_xlim(-0.55, 10.55)
    ax.set_ylim(-1.15, 10.35)
    ax.set_aspect("equal")
    ax.axis("off")

    # Lower row: fixed footprint. Upper row: high-fidelity robot model.
    # Left column: regular map. Right column: complex map.
    _cell(
        ax, 0.35, 0.55, 4.35, 3.85,
        "#F4F6F8",
        "Idealized",
        ["BCD", "STC"],
    )
    _cell(
        ax, 5.15, 0.55, 4.35, 3.85,
        "#E7F2F2",
        "Map-enhanced",
        ["Polygon CPP", "Fields2Cover", "Nobleo"],
    )
    _cell(
        ax, 0.35, 4.85, 4.35, 3.85,
        "#FFF6ED",
        "Platform-constrained",
        ["Mobile manipulator", "SatAOI"],
    )
    _cell(
        ax, 5.15, 4.85, 4.35, 3.85,
        "#E7F6EA",
        "Environment–platform\ncoupled",
        ["not yet unified", "BiRect"],
        emphasize=True,
    )

    # Horizontal axis: map representation.
    ax.annotate(
        "",
        xy=(9.55, -0.35),
        xytext=(0.35, -0.35),
        arrowprops=dict(arrowstyle="-|>", color=SLATE, lw=1.3),
    )
    ax.text(0.35, -0.72, "regular map", ha="left", va="top", fontsize=10, color=SLATE)
    ax.text(9.55, -0.72, "complex map", ha="right", va="top", fontsize=10, color=SLATE)
    ax.text(
        4.95, -1.05,
        "Map representation",
        ha="center", va="top", fontsize=12, color=NAVY, fontweight="bold",
    )

    # Vertical axis: robot model.
    ax.annotate(
        "",
        xy=(-0.28, 8.85),
        xytext=(-0.28, 0.45),
        arrowprops=dict(arrowstyle="-|>", color=SLATE, lw=1.3),
    )
    ax.text(
        -0.42, 0.55,
        "point or\nfixed footprint",
        ha="right", va="bottom", fontsize=10, color=SLATE,
    )
    ax.text(
        -0.42, 8.75,
        "base–arm–disc",
        ha="right", va="top", fontsize=10, color=SLATE,
    )
    ax.text(
        -0.48, 4.7,
        "Robot model",
        ha="center", va="center", fontsize=12, color=NAVY, fontweight="bold",
        rotation=90,
    )

    out = figures_dir() / "figure_cpp_class_quadrant.png"
    fig.savefig(out, dpi=220)
    plt.close(fig)
    print(out)


if __name__ == "__main__":
    main()
