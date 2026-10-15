"""Single-rectangle reciprocating primitive as a vector PDF.

The 2400x2400 PNG has no generator. Poses, the five-strip boustrophedon, and
the dashed other-axis line follow that raster. The media box keeps every disc,
arm, and dashed endpoint inside a positive margin.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tikzfig import FIGURES, compile_tikz


# PNG rectangle mapped into millimetres. Unit 100 is one side of the rectangle.
ORIGIN = (10.0, 12.0)
SCALE = 0.58
DISC_R_UNIT = 3.62
DISC_R = DISC_R_UNIT * SCALE
CHASSIS_HALF = (8.15 * SCALE, 4.70 * SCALE)
WIDTH_MM = 86.0
HEIGHT_MM = 78.0
MARGIN_MM = 4.0

# Travel alternates. Five strips, so the top pass ends on the right, at the disc.
_X_LEFT = 10.0
_X_RIGHT = 90.0
_STRIP_Y = (10.0, 30.0, 50.0, 70.0, 90.0)


def mm(xu: float, yu: float) -> tuple[float, float]:
    return (ORIGIN[0] + xu * SCALE, ORIGIN[1] + yu * SCALE)


def _pose(xu: float, yu: float, dxu: float, dyu: float, angle: float) -> dict:
    cx, cy = mm(xu, yu)
    dx, dy = mm(dxu, dyu)
    return {
        "chassis": (cx, cy),
        "angle": angle,
        "disc": (dx, dy),
        "arm": ((cx, cy), (dx, dy)),
    }


def scene() -> dict:
    """One rectangle, five strips, the path, five bases, and the end disc."""
    poses = [
        _pose(14.6, 10.1, 0.0, 10.1, 0.0),
        _pose(89.8, 10.2, 89.8, -4.6, 90.0),
        _pose(43.2, 30.2, 57.8, 30.2, 0.0),
        _pose(66.8, 51.6, 55.1, 42.3, math.degrees(math.atan2(42.3 - 51.6, 55.1 - 66.8))),
        _pose(10.0, 70.1, 9.9, 55.3, 90.0),
    ]
    end = mm(103.5, _STRIP_Y[-1])
    discs = [pose["disc"] for pose in poses] + [end]
    path = []
    x_left, x_right = mm(_X_LEFT, 0.0)[0], mm(_X_RIGHT, 0.0)[0]
    ys = [mm(0.0, y)[1] for y in _STRIP_Y]
    for index, y in enumerate(ys):
        going_right = index % 2 == 0
        x_start, x_end = (x_left, x_right) if going_right else (x_right, x_left)
        if index == len(ys) - 1:
            x_end = end[0]
        path.append((x_start, y, x_end, y))
        if index < len(ys) - 1:
            y_next = ys[index + 1]
            x_turn = x_right if going_right else x_left
            path.append((x_turn, y, x_turn, y_next))
    rect = (*mm(0.0, 0.0), *mm(100.0, 100.0))
    return {
        "width_mm": WIDTH_MM,
        "height_mm": HEIGHT_MM,
        "margin_mm": MARGIN_MM,
        "disc_r": DISC_R,
        "chassis_half": CHASSIS_HALF,
        "rectangle": rect,
        "strips": [
            (rect[0], mm(0.0, 20.0 * i)[1], rect[2], mm(0.0, 20.0 * (i + 1))[1])
            for i in range(5)
        ],
        "poses": poses,
        "end_disc": end,
        "discs": discs,
        "path": path,
        "dashed": (mm(15.3, 11.2), mm(116.0, 88.7)),
    }


def _num(value: float) -> str:
    return f"{value:.2f}"


def _body(spec: dict) -> str:
    x0, y0, x1, y1 = spec["rectangle"]
    lines = [
        r"\begin{tikzpicture}[x=1mm,y=1mm]",
        (
            "  \\useasboundingbox (0,0) rectangle "
            f"({_num(spec['width_mm'])}mm,{_num(spec['height_mm'])}mm);"
        ),
    ]
    for index, (sx0, sy0, sx1, sy1) in enumerate(spec["strips"]):
        style = "workband" if index % 2 else "secondary!18!white"
        lines.append(
            f"  \\fill[{style}] ({_num(sx0)},{_num(sy0)}) rectangle ({_num(sx1)},{_num(sy1)});"
        )
    lines.append(f"  \\draw[main] ({_num(x0)},{_num(y0)}) rectangle ({_num(x1)},{_num(y1)});")
    (dx0, dy0), (dx1, dy1) = spec["dashed"]
    lines.append(f"  \\draw[aux] ({_num(dx0)},{_num(dy0)}) -- ({_num(dx1)},{_num(dy1)});")
    ex, ey = spec["end_disc"]
    lines.append(f"  \\draw[disc] ({_num(ex)},{_num(ey)}) circle[radius={_num(spec['disc_r'])}];")
    hl, hw = spec["chassis_half"]
    for pose in spec["poses"]:
        cx, cy = pose["chassis"]
        lines.append(f"  \\begin{{scope}}[shift={{({_num(cx)},{_num(cy)})}}, rotate={_num(pose['angle'])}]")
        lines.append(f"    \\draw[chassis] ({_num(-hl)},{_num(-hw)}) rectangle ({_num(hl)},{_num(hw)});")
        lines.append(f"    \\draw[aux, dotted] ({_num(-hl)},{_num(-hw)}) -- ({_num(hl)},{_num(hw)});")
        lines.append(f"    \\draw[aux, dotted] ({_num(-hl)},{_num(hw)}) -- ({_num(hl)},{_num(-hw)});")
        lines.append(r"  \end{scope}")
    for dx, dy in (pose["disc"] for pose in spec["poses"]):
        lines.append(f"  \\draw[disc] ({_num(dx)},{_num(dy)}) circle[radius={_num(spec['disc_r'])}];")
    for x_a, y_a, x_b, y_b in spec["path"]:
        lines.append(f"  \\draw[flow] ({_num(x_a)},{_num(y_a)}) -- ({_num(x_b)},{_num(y_b)});")
    for (ax, ay), (bx, by) in (pose["arm"] for pose in spec["poses"]):
        lines.append(f"  \\draw[arm] ({_num(ax)},{_num(ay)}) -- ({_num(bx)},{_num(by)});")
    for cx, cy in (pose["chassis"] for pose in spec["poses"]):
        lines.append(f"  \\fill[ink] ({_num(cx)},{_num(cy)}) circle[radius=0.32];")
    lines.append(r"\end{tikzpicture}")
    return "\n".join(lines) + "\n"


def main() -> None:
    compile_tikz(_body(scene()), FIGURES / "figure_6_single_rectangle_coverage.pdf")


if __name__ == "__main__":
    main()
