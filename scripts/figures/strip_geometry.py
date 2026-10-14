"""Principle figure for subsection 3.5.2 (revision 63, first figure).

Three panels, using symbols already defined in the methodology:
(a) disc center on the rectangle boundary, base retracted by d_p+L;
(b) ell_R, h_R, w_s, N_s, and one start corner;
(c) arm at +/- phi_w with w_s, L, and r_d.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Rectangle

from paper_style import INK, NAVY, RULE, SLATE, WORK, figures_dir, use_serif


def _dim(ax, p0, p1, text, offset=(0, 0.16), color=SLATE):
    ax.annotate(
        "",
        xy=p1,
        xytext=p0,
        arrowprops=dict(arrowstyle="<->", color=color, lw=0.9, shrinkA=0, shrinkB=0),
    )
    mid = ((p0[0] + p1[0]) / 2 + offset[0], (p0[1] + p1[1]) / 2 + offset[1])
    ax.text(mid[0], mid[1], text, ha="center", va="center", fontsize=11, color=NAVY)


def _panel_a(ax):
    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(-0.15, 3.7)
    rect = Rectangle((2.15, 0.45), 3.5, 2.35, facecolor="#F4F7FB", edgecolor=INK, lw=1.1, zorder=1)
    ax.add_patch(rect)
    # theta = pi puts the retracted base outside the left boundary.
    disc = np.array([2.15, 1.62])
    base = disc + np.array([-1.45, 0.0])
    ax.plot([base[0], disc[0]], [base[1], disc[1]], color=NAVY, lw=1.35, zorder=2)
    ax.add_patch(Rectangle((base[0] - 0.42, base[1] - 0.28), 0.84, 0.56,
                           facecolor="#E7EEF5", edgecolor=NAVY, lw=1.1, zorder=3))
    ax.add_patch(Circle(disc, 0.30, facecolor="#D6E4F0", edgecolor=WORK, lw=1.2, zorder=4))
    ax.plot(*disc, "o", color=INK, ms=3.5, zorder=5)
    ax.annotate(
        "",
        xy=(base[0] - 0.62, base[1]),
        xytext=(base[0] - 0.05, base[1]),
        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.1),
    )
    ax.text(base[0] - 0.62, base[1] + 0.16, r"$\theta$", color=NAVY, fontsize=11, ha="center")
    _dim(ax, (base[0], 2.55), (disc[0], 2.55), r"$d_p+L$", offset=(0, 0.18))
    ax.plot([base[0], base[0]], [base[1] + 0.28, 2.55], color=RULE, lw=0.6)
    ax.plot([disc[0], disc[0]], [disc[1] + 0.30, 2.55], color=RULE, lw=0.6)
    ax.text(disc[0] + 0.42, disc[1] - 0.55, "disc center", fontsize=9, color=INK, ha="left")
    ax.set_title("(a)", loc="left", fontsize=12, color=NAVY, pad=2)


def _panel_b(ax):
    ax.set_xlim(-0.55, 5.3)
    ax.set_ylim(-0.85, 3.55)
    width, height = 3.6, 2.4
    origin = (0.35, 0.25)
    strips = 3
    strip_h = height / strips
    ax.add_patch(Rectangle(origin, width, height, facecolor="#F4F7FB", edgecolor=INK, lw=1.1))
    for k in range(1, strips):
        y = origin[1] + k * strip_h
        ax.plot([origin[0], origin[0] + width], [y, y], color=WORK, lw=0.8, ls=(0, (3, 2)))
    # One start corner.
    corner = (origin[0], origin[1])
    ax.plot(*corner, "o", color=NAVY, ms=6, zorder=4)
    ax.text(corner[0] + 0.12, corner[1] + 0.12, "start", fontsize=9, color=NAVY, ha="left", va="bottom")
    _dim(ax, (origin[0], -0.15), (origin[0] + width, -0.15), r"$\ell_R$", offset=(0, -0.28))
    _dim(ax, (origin[0] + width + 0.28, origin[1]), (origin[0] + width + 0.28, origin[1] + height),
         r"$h_R$", offset=(0.32, 0))
    _dim(ax, (origin[0] - 0.22, origin[1]), (origin[0] - 0.22, origin[1] + strip_h),
         r"$w_s$", offset=(-0.28, 0))
    ax.text(origin[0] + width / 2, origin[1] + height + 0.18, r"$N_s$", ha="center", va="bottom",
            fontsize=12, color=NAVY)
    ax.set_title("(b)", loc="left", fontsize=12, color=NAVY, pad=2)


def _panel_c(ax):
    ax.set_xlim(-0.35, 2.55)
    ax.set_ylim(-1.55, 1.55)
    length = 1.15
    phi = 0.62
    radius = 0.28
    half = length * np.sin(phi) + radius
    ax.axhspan(-half, half, color="#F4F7FB", zorder=0)
    ax.plot([-0.15, 2.15], [half, half], color=INK, lw=0.8)
    ax.plot([-0.15, 2.15], [-half, -half], color=INK, lw=0.8)
    ax.plot([-0.15, 2.15], [0, 0], color=RULE, lw=0.7, ls=(0, (2, 2)))
    pivot = np.array([0.15, 0.0])
    for sign, shade in ((1, 0.55), (-1, 0.25)):
        angle = sign * phi
        tip = pivot + length * np.array([np.cos(angle), np.sin(angle)])
        ax.plot([pivot[0], tip[0]], [pivot[1], tip[1]], color=NAVY, lw=1.3, alpha=0.45 + shade, zorder=3)
        ax.add_patch(Circle(tip, radius, facecolor="#D6E4F0", edgecolor=WORK, lw=1.1,
                            alpha=0.55 + 0.4 * shade, zorder=4))
    ax.plot(*pivot, "o", color=INK, ms=4, zorder=5)
    arc = Arc(pivot, 0.85, 0.85, angle=0, theta1=-np.degrees(phi), theta2=np.degrees(phi),
              color=SLATE, lw=0.9)
    ax.add_patch(arc)
    ax.text(pivot[0] + 0.52, 0.22, r"$\phi_w$", fontsize=11, color=NAVY)
    ax.text(pivot[0] + 0.52, -0.38, r"$-\phi_w$", fontsize=11, color=NAVY)
    mid_tip = pivot + length * np.array([np.cos(phi), np.sin(phi)])
    arm = mid_tip - pivot
    perp = np.array([-arm[1], arm[0]]) / np.linalg.norm(arm)
    label_l = (pivot + mid_tip) / 2 + 0.16 * perp
    ax.text(label_l[0], label_l[1], r"$L$", fontsize=12, color=NAVY, ha="center", va="center")
    # Outer disc edge meets the strip boundary: that radial gap is r_d.
    ax.annotate(
        "",
        xy=(mid_tip[0], mid_tip[1] + radius),
        xytext=(mid_tip[0], mid_tip[1]),
        arrowprops=dict(arrowstyle="<->", color=SLATE, lw=0.8, shrinkA=0, shrinkB=0),
    )
    ax.text(mid_tip[0] + radius + 0.06, mid_tip[1] + radius / 2, r"$r_d$", fontsize=11,
            color=NAVY, ha="left", va="center")
    _dim(ax, (2.25, -half), (2.25, half), r"$w_s$", offset=(0.34, 0))
    ax.set_title("(c)", loc="left", fontsize=12, color=NAVY, pad=2)


def main() -> None:
    use_serif()
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 3.15))
    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")
    _panel_a(axes[0])
    _panel_b(axes[1])
    _panel_c(axes[2])
    fig.tight_layout(w_pad=1.4)
    out = figures_dir() / "figure_strip_geometry.png"
    fig.savefig(out, dpi=220)
    plt.close(fig)
    print(out)


if __name__ == "__main__":
    main()
