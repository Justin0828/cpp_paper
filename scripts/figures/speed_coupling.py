"""Principle figure for subsection 3.5.3 (revision 63, second figure).

While the arm swings from -phi_w to +phi_w, the base advances one disc
diameter. The labels are v_work and T_half. No new sweep of r_d or L.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

from paper_style import INK, NAVY, RULE, SLATE, WORK, figures_dir, use_serif


def _pose(ax, origin, sign, length, phi, radius, alpha):
    pivot = np.array(origin)
    tip = pivot + length * np.array([np.cos(sign * phi), np.sin(sign * phi)])
    ax.add_patch(Rectangle((pivot[0] - 0.16, pivot[1] - 0.22), 0.46, 0.44,
                           facecolor="#E7EEF5", edgecolor=NAVY, lw=1.0, alpha=alpha, zorder=3))
    ax.plot([pivot[0], tip[0]], [pivot[1], tip[1]], color=NAVY, lw=1.4, alpha=alpha, zorder=4)
    ax.add_patch(Circle(tip, radius, facecolor="#D6E4F0", edgecolor=WORK, lw=1.1, alpha=alpha, zorder=5))
    ax.plot(*pivot, "o", color=INK, ms=3.5, alpha=alpha, zorder=6)
    return tip


def main() -> None:
    use_serif()
    fig, ax = plt.subplots(figsize=(7.2, 3.35))
    length = 1.15
    phi = 0.62
    radius = 0.34
    # Disc centers share the forward offset L cos(phi), so a base shift of
    # one diameter 2 r_d makes the two discs meet.
    advance = 2 * radius
    start = np.array([0.55, 0.0])
    end = start + np.array([advance, 0.0])
    ax.set_xlim(-0.45, 3.55)
    ax.set_ylim(-1.55, 2.15)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.plot([-0.2, 3.35], [0, 0], color=RULE, lw=0.7, ls=(0, (2, 2)), zorder=0)
    tip0 = _pose(ax, start, -1, length, phi, radius, 0.45)
    tip1 = _pose(ax, end, +1, length, phi, radius, 1.0)
    # Base travel of one disc diameter, drawn above the bases so it misses both discs.
    y_dim = 1.05
    ax.annotate(
        "",
        xy=(end[0], y_dim),
        xytext=(start[0], y_dim),
        arrowprops=dict(arrowstyle="<->", color=SLATE, lw=0.9),
    )
    ax.plot([start[0], start[0]], [0.22, y_dim], color=RULE, lw=0.6)
    ax.plot([end[0], end[0]], [0.22, y_dim], color=RULE, lw=0.6)
    ax.text((start[0] + end[0]) / 2, y_dim + 0.10, r"$2r_d$", ha="center", va="bottom",
            fontsize=12, color=NAVY)
    ax.annotate(
        "",
        xy=(end[0], 0.50),
        xytext=(start[0], 0.50),
        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.3),
    )
    ax.text(start[0] - 0.22, 0.50, r"$v_{\mathrm{work}}$",
            ha="right", va="center", fontsize=12, color=NAVY)
    y_time = max(tip0[1], tip1[1]) + radius + 0.38
    ax.annotate(
        "",
        xy=(tip1[0], y_time),
        xytext=(tip0[0], y_time),
        arrowprops=dict(arrowstyle="<->", color=SLATE, lw=0.9),
    )
    ax.text((tip0[0] + tip1[0]) / 2, y_time + 0.08, r"$T_{\mathrm{half}}$", ha="center", va="bottom",
            fontsize=12, color=NAVY)
    ax.text(tip0[0] + 0.08, tip0[1] - radius - 0.08, r"$-\phi_w$", fontsize=11, color=NAVY,
            ha="center", va="top")
    ax.text(tip1[0] + radius + 0.08, tip1[1], r"$+\phi_w$", fontsize=11, color=NAVY,
            ha="left", va="center")
    out = figures_dir() / "figure_speed_coupling.png"
    fig.savefig(out, dpi=220)
    plt.close(fig)
    print(out)


if __name__ == "__main__":
    main()
