"""Schematic for subsection 3.7 (revision 67).

Two adjacent rectangles and one transfer. Work-strip swings are effective
work. Lane changes, an in-place turn, arm deploy/retract, and the handoff
are non-work. C_work is the work-segment disc sweep; C_traj adds the
non-work disc sweep. Not an experimental map, and no third coverage ratio.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from paper_style import INK, NAVY, NONWORK, NONWORK_WASH, WORK, WORK_WASH, figures_dir, use_serif


def _swing(x0, x1, y, waves=4):
    xs = np.linspace(x0, x1, 240)
    ys = y + 0.16 * np.sin(waves * 2 * np.pi * (xs - x0) / (x1 - x0))
    return xs, ys


def _lane(x, y0, y1):
    ys = np.linspace(y0, y1, 80)
    xs = x + 0.18 * np.sin(np.pi * (ys - y0) / (y1 - y0))
    return xs, ys


def _draw_scene(ax, sweeps):
    left = (0.35, 0.55, 3.15, 2.55)
    right = (4.55, 0.55, 3.15, 2.55)
    for box in (left, right):
        ax.add_patch(Rectangle((box[0], box[1]), box[2], box[3],
                               facecolor="#F7F8FA", edgecolor=INK, lw=1.05, zorder=1))
    work = []
    nonwork = []
    # Deploy / retract outside the first rectangle.
    nonwork.append((np.array([0.05, 0.55, 0.35]), np.array([1.15, 0.85, 0.85])))
    # In-place turn just inside the entry.
    turn = np.linspace(-np.pi / 2, np.pi / 2, 40)
    nonwork.append((0.7 + 0.22 * np.cos(turn), 1.05 + 0.22 * np.sin(turn)))
    # Three work strips and two lane changes in the left rectangle.
    lanes_y = (1.05, 1.85, 2.55)
    for index, y in enumerate(lanes_y):
        xs, ys = _swing(0.7, 3.15, y, waves=3.5)
        if index % 2 == 1:
            xs = xs[::-1]
            ys = ys[::-1]
        work.append((xs, ys))
    nonwork.append(_lane(3.15, 1.05, 1.85))
    nonwork.append(_lane(0.7, 1.85, 2.55))
    # Handoff between the rectangles.
    t = np.linspace(0, 1, 80)
    nonwork.append((
        3.5 + t * 1.15,
        2.55 + 0.35 * np.sin(np.pi * t),
    ))
    # Two work strips and one lane change in the right rectangle.
    work.append(_swing(4.9, 7.35, 1.15, waves=3.5))
    xs, ys = _swing(4.9, 7.35, 2.05, waves=3.5)
    work.append((xs[::-1], ys[::-1]))
    nonwork.append(_lane(7.35, 1.15, 2.05))

    def paint(path, color, wash, width):
        xs, ys = path
        if sweeps:
            ax.plot(xs, ys, color=wash, lw=width, solid_capstyle="round", zorder=2)
        ax.plot(xs, ys, color=color, lw=1.35, solid_capstyle="round", zorder=3)

    for path in nonwork:
        paint(path, NONWORK, NONWORK_WASH, 10)
    for path in work:
        paint(path, WORK, WORK_WASH, 11)


def main() -> None:
    use_serif()
    fig, axes = plt.subplots(2, 1, figsize=(7.4, 5.6))
    for ax, sweeps, tag in (
        (axes[0], False, "(a)"),
        (axes[1], True, "(b)"),
    ):
        ax.set_xlim(-0.15, 8.05)
        ax.set_ylim(-0.55, 3.55)
        ax.set_aspect("equal")
        ax.axis("off")
        _draw_scene(ax, sweeps)
        ax.text(0.0, 3.42, tag, fontsize=12, color=NAVY, fontweight="bold", ha="left", va="top")
    axes[0].text(
        4.05, -0.48,
        "work-strip swing: effective work\n"
        "lane change, in-place turn, deploy/retract, handoff: non-work",
        ha="center", va="bottom", fontsize=8.5, color=INK,
    )
    axes[1].text(1.9, 3.22, r"$\mathcal{C}_{\mathrm{work}}$", fontsize=12, color=WORK, ha="center")
    axes[1].text(
        4.05, -0.42,
        r"$\mathcal{C}_{\mathrm{traj}}$ adds the non-work disc sweep",
        ha="center", va="bottom", fontsize=9, color=INK,
    )
    fig.tight_layout(h_pad=0.4)
    out = figures_dir() / "figure_coverage_segments.png"
    fig.savefig(out, dpi=220)
    plt.close(fig)
    print(out)


if __name__ == "__main__":
    main()
