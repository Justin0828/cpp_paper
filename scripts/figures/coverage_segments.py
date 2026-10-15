"""Work sweep versus full-trajectory sweep on two rectangles and one transfer.

Strip count and width follow Section 3.5: N_s strips of width w_s = h_R / N_s
tile each rectangle. Gray bands are the non-work sweeps and have width 2 r_d.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tikzfig import FIGURES, compile_tikz


# One transverse side for both rectangles. Eq. (13): w_s = h_R / N_s.
N_S = 3
W_S = 10.0
H_R = N_S * W_S
R_D = 2.0
GRAY_W = 2.0 * R_D
ELL_LEFT = 26.0
ELL_RIGHT = 18.0
GAP = 10.0
PAD = 1.5
CANVAS_H_MM = 74.0

# Panel origins. Local geometry is added to these.
_ORIGINS = ((4.0, 16.0), (86.0, 16.0))


def _rect(x: float, y: float, w: float, h: float) -> dict:
    strips = [(x, y + i * W_S, w, W_S) for i in range(N_S)]
    return {"x": x, "y": y, "w": w, "h": h, "strips": strips}


def _turns(rect: dict) -> list[tuple[float, float, float, float]]:
    """Lane-change bands outside the short ends. Width is 2 r_d."""
    bands = []
    for i in range(N_S - 1):
        y0 = rect["y"] + (i + 0.5) * W_S
        if i % 2 == 0:
            bands.append((rect["x"] + rect["w"], y0, GRAY_W, W_S))
        else:
            bands.append((rect["x"] - GRAY_W, y0, GRAY_W, W_S))
    return bands


def _transfer(left: dict, right: dict) -> tuple[float, float, float, float]:
    """One band in the gap, centered on the top strip, width 2 r_d."""
    y_mid = left["y"] + (N_S - 0.5) * W_S
    x0 = left["x"] + left["w"]
    return (x0, y_mid - GRAY_W / 2.0, right["x"] - x0, GRAY_W)


def _bbox(boxes: list[tuple[float, float, float, float]]) -> tuple[float, float, float, float]:
    x0 = min(b[0] for b in boxes)
    y0 = min(b[1] for b in boxes)
    x1 = max(b[0] + b[2] for b in boxes)
    y1 = max(b[1] + b[3] for b in boxes)
    return (x0, y0, x1, y1)


def _expand(box: tuple[float, float, float, float], pad: float) -> tuple[float, float, float, float]:
    return (box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad)


def _arrow(strip: tuple[float, float, float, float], direction: int) -> tuple[float, float, float, float]:
    x, y, w, h = strip
    y_mid = y + h / 2.0
    inset = 2.4
    if direction > 0:
        return (x + inset, y_mid, x + w - inset, y_mid)
    return (x + w - inset, y_mid, x + inset, y_mid)


def _centerline(band: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    x, y, w, h = band
    if w <= h:
        return (x + w / 2.0, y, x + w / 2.0, y + h)
    return (x, y + h / 2.0, x + w, y + h / 2.0)


def layout() -> dict:
    """Absolute millimetre geometry for both panels. Panel 0 is (a)."""
    panels = []
    for index, (ox, oy) in enumerate(_ORIGINS):
        left = _rect(ox + 8.0, oy + 6.0, ELL_LEFT, H_R)
        right = _rect(left["x"] + left["w"] + GAP, oy + 6.0, ELL_RIGHT, H_R)
        gray = _turns(left) + _turns(right) + [_transfer(left, right)]
        orange_boxes = [tuple(s) for rect in (left, right) for s in rect["strips"]]
        orange_bb = _bbox(orange_boxes)
        union_bb = _bbox(orange_boxes + gray)
        if index == 0:
            mark = _expand(orange_bb, PAD)
            mark_name = "c_work"
        else:
            mark = _expand(union_bb, PAD)
            mark_name = "c_traj"
        arrows = []
        for rect in (left, right):
            for i, strip in enumerate(rect["strips"]):
                arrows.append(_arrow(strip, 1 if i % 2 == 0 else -1))
        cx = (left["x"] + right["x"] + right["w"]) / 2.0
        panels.append(
            {
                "tag": "(a)" if index == 0 else "(b)",
                "tag_at": (cx, oy - 1.5),
                "rectangles": [left, right],
                "gray": gray,
                "arrows": arrows,
                "centerlines": [_centerline(band) for band in gray],
                "orange_bbox": orange_bb,
                "union_bbox": union_bb,
                "mark": mark,
                "mark_name": mark_name,
            }
        )
    return {"width_mm": 160.0, "height_mm": CANVAS_H_MM, "panels": panels}


def _num(value: float) -> str:
    return f"{value:.2f}"


def _rect_fill(box: tuple[float, float, float, float], style: str) -> str:
    x, y, w, h = box
    return (
        f"  \\fill[{style}] ({_num(x)},{_num(y)}) rectangle "
        f"({_num(x + w)},{_num(y + h)});"
    )


def _draw_segment(segment: tuple[float, float, float, float], style: str) -> str:
    x0, y0, x1, y1 = segment
    return f"  \\draw[{style}] ({_num(x0)},{_num(y0)}) -- ({_num(x1)},{_num(y1)});"


def _body(spec: dict) -> str:
    lines = [
        r"\begin{tikzpicture}[x=1mm,y=1mm]",
        f"  \\useasboundingbox (0,0) rectangle (\\paperfullwidth, {_num(spec['height_mm'])}mm);",
    ]
    for panel in spec["panels"]:
        lines.append(f"  \\node[tag, anchor=north] at ({_num(panel['tag_at'][0])},{_num(panel['tag_at'][1])}) {{{panel['tag']}}};")
        if panel["mark_name"] == "c_traj":
            for band in panel["gray"]:
                lines.append(_rect_fill(band, "nonworkfill"))
        for rect in panel["rectangles"]:
            for strip in rect["strips"]:
                lines.append(_rect_fill(strip, "workband"))
            lines.append(
                "  \\draw[main] "
                f"({_num(rect['x'])},{_num(rect['y'])}) rectangle "
                f"({_num(rect['x'] + rect['w'])},{_num(rect['y'] + rect['h'])});"
            )
        for arrow in panel["arrows"]:
            lines.append(_draw_segment(arrow, "flow"))
        if panel["mark_name"] == "c_traj":
            for segment in panel["centerlines"]:
                lines.append(_draw_segment(segment, "aux"))
        x0, y0, x1, y1 = panel["mark"]
        lines.append(
            f"  \\draw[guide] ({_num(x0)},{_num(y0)}) rectangle ({_num(x1)},{_num(y1)});"
        )
        label = r"$\mathcal{C}_{\mathrm{work}}$" if panel["mark_name"] == "c_work" else r"$\mathcal{C}_{\mathrm{traj}}$"
        lines.append(
            f"  \\node[sym, anchor=south] at ({_num((x0 + x1) / 2.0)},{_num(y1 + 0.8)}) {{{label}}};"
        )
    lines.append(r"\end{tikzpicture}")
    return "\n".join(lines) + "\n"


def main() -> None:
    compile_tikz(_body(layout()), FIGURES / "figure_coverage_segments.pdf")


if __name__ == "__main__":
    main()
