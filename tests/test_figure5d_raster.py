"""Panel (d) of the geometric-to-raster figure matches its own obstacles.

The 15 by 16 raster is the L in ``transfer.svg``, with the inner corner pinned
to a grid line. A cell is unavailable when it is not entirely inside the L or
when its rectangle meets the disc or a rectangular obstacle, including a
boundary touch.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SVG_PATH = ROOT / "assets" / "svg_sources" / "transfer.svg"
PNG_PATHS = (
    ROOT / "english_paper" / "figures" / "figure_3_geometric_to_binary_raster.png",
    ROOT / "figures" / "figure_3_geometric_to_binary_raster.png",
)
SVG_W, SVG_H = 530.0, 280.0
N_COLS, N_ROWS = 15, 16
CELL = 4
FRAME_ORIGIN = (100, 153)
FRAME_DARK = (75, 85, 99)
LABEL_DARK = (31, 41, 55)
# Lower-right window checked against the two arm rectangles. Occupied means
# the cell meets obstacle 3, obstacle 4, or both.
LOWER_RIGHT_OCCUPIED = {
    (10, 10), (11, 10),
    (10, 11), (11, 11),
    (10, 12), (11, 12), (12, 12), (13, 12), (14, 12),
    (11, 13), (12, 13), (13, 13), (14, 13),
    (11, 14), (12, 14), (13, 14), (14, 14),
    (11, 15), (12, 15), (13, 15), (14, 15),
}


def _paths(svg: str) -> list[re.Match[str]]:
    return list(re.finditer(r"<path\b[^>]*/>", svg))


def _attr(tag: str, name: str) -> str:
    match = re.search(rf'\b{name}="([^"]*)"', tag)
    if match is None:
        raise AssertionError(f"missing {name} in {tag[:80]}")
    return match.group(1)


def _cell_origin(path_d: str) -> tuple[int, int] | None:
    match = re.fullmatch(r"M(\d+) (\d+)H(\d+)V(\d+)H(\d+)V(\d+)Z", path_d)
    if match is None:
        return None
    x1, y1, x0, y2, x1b, y0b = (int(part) for part in match.groups())
    if (x1, y2, x1b, y0b) != (x0 + CELL, y1 + CELL, x1, y1):
        return None
    return x0, y1


def _panel_cells(svg: str, x0: int, y0: int) -> set[tuple[int, int]]:
    """Free-cell column/row indices whose top-left sits on this raster."""
    found: set[tuple[int, int]] = set()
    x_max = x0 + CELL * (N_COLS - 1)
    y_max = y0 + CELL * (N_ROWS - 1)
    for match in _paths(svg):
        tag = match.group(0)
        if "fill=" not in tag or _attr(tag, "fill") != "white":
            continue
        origin = _cell_origin(_attr(tag, "d"))
        if origin is None:
            continue
        left, top = origin
        if not (x0 <= left <= x_max and y0 <= top <= y_max):
            continue
        if (left - x0) % CELL or (top - y0) % CELL:
            raise AssertionError(f"cell off the 4-unit grid: {origin}")
        found.add(((left - x0) // CELL, (top - y0) // CELL))
    return found


def _rect_from_path(path_d: str) -> tuple[float, float, float, float]:
    """Axis-aligned rectangle as (xmin, xmax, ymin, ymax)."""
    numbers = [float(part) for part in re.findall(r"-?\d+(?:\.\d+)?", path_d)]
    xs = numbers[0::2]
    ys = numbers[1::2]
    return min(xs), max(xs), min(ys), max(ys)


def _l_polygon(path_d: str) -> tuple[float, float, float, float, float, float]:
    """Stem-right x, arm-top y, and the L bounding box, from the path order.

    The drawn command is M left top H stem_right V arm_top H right V bottom H left.
    """
    match = re.fullmatch(
        r"M(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)H(-?\d+(?:\.\d+)?)V(-?\d+(?:\.\d+)?)"
        r"H(-?\d+(?:\.\d+)?)V(-?\d+(?:\.\d+)?)H(-?\d+(?:\.\d+)?)V(-?\d+(?:\.\d+)?)Z",
        path_d,
    )
    if match is None:
        raise AssertionError(f"unexpected L path {path_d}")
    left, top, stem_right, arm_top, right, bottom, left2, top2 = (
        float(part) for part in match.groups()
    )
    if (left, top) != (left2, top2):
        raise AssertionError("L path does not close on its start")
    return stem_right, arm_top, left, right, top, bottom


def _disc(path_d: str) -> tuple[float, float, float]:
    """Center and radius of a circle written as four cubic lobes."""
    numbers = [float(part) for part in re.findall(r"-?\d+(?:\.\d+)?", path_d)]
    xs = numbers[0::2]
    ys = numbers[1::2]
    cx = (min(xs) + max(xs)) / 2.0
    cy = (min(ys) + max(ys)) / 2.0
    radius = (max(xs) - min(xs)) / 2.0
    if abs((max(ys) - min(ys)) / 2.0 - radius) > 1e-6:
        raise AssertionError("disc path is not circular")
    return cx, cy, radius


def _geometry(svg: str) -> dict:
    """Read panel (d) and the obstacle-free panel that shares its scale."""
    l_paths = []
    dark = []
    for match in _paths(svg):
        tag = match.group(0)
        path_d = _attr(tag, "d")
        fill = _attr(tag, "fill") if "fill=" in tag else ""
        if fill == "#F0F4F8" and path_d.startswith("M"):
            try:
                _l_polygon(path_d)
            except AssertionError:
                continue
            l_paths.append(path_d)
        elif fill == "#4B5563" and path_d.startswith("M"):
            dark.append(path_d)
    if len(l_paths) != 2:
        raise AssertionError(f"expected two L polygons, found {len(l_paths)}")
    # Panel (d) is the L translated toward the origin.
    panel_d = min(l_paths, key=lambda item: _l_polygon(item)[2])
    panel_c = max(l_paths, key=lambda item: _l_polygon(item)[2])
    stem_right, arm_top, left, right, top, bottom = _l_polygon(panel_d)
    c_stem, c_arm, c_left, c_right, c_top, c_bottom = _l_polygon(panel_c)
    if (stem_right - left, arm_top - top, right - left, bottom - top) != (
        c_stem - c_left, c_arm - c_top, c_right - c_left, c_bottom - c_top,
    ):
        raise AssertionError("the two L polygons are not the same shape")
    discs = []
    rects = []
    for path_d in dark:
        if "C" in path_d:
            cx, cy, radius = _disc(path_d)
            if left <= cx <= right and top <= cy <= bottom:
                discs.append((cx, cy, radius))
        else:
            box = _rect_from_path(path_d)
            cx = (box[0] + box[1]) / 2.0
            cy = (box[2] + box[3]) / 2.0
            if left <= cx <= right and top <= cy <= bottom and (box[1] - box[0]) < 40:
                rects.append(box)
    if len(discs) != 1 or len(rects) != 3:
        raise AssertionError(f"obstacles in panel (d): {len(discs)} discs, {len(rects)} rects")
    return {
        "left": left,
        "top": top,
        "stem_right": stem_right,
        "arm_top": arm_top,
        "right": right,
        "bottom": bottom,
        "disc": discs[0],
        "rects": tuple(sorted(rects)),
        "translation": (left - c_left, top - c_top),
        "panel_c_origin_geom": (c_left, c_top),
    }


def _stem_cell_counts(svg: str, geom: dict) -> tuple[int, int]:
    """Columns and rows of the obstacle-free raster that cover the stem only."""
    dx, dy = geom["translation"]
    # Panel (c) cells sit at the panel (d) raster origin minus this translation.
    origin_x = FRAME_ORIGIN[0] - dx
    origin_y = FRAME_ORIGIN[1] - dy
    free = _panel_cells(svg, int(origin_x), int(origin_y))
    if len(free) < 100:
        raise AssertionError("panel (c) raster was not found at the shared translation")
    stem_rows = [row for row in range(N_ROWS) if any((col, row) not in free for col in range(N_COLS))]
    if not stem_rows:
        raise AssertionError("panel (c) has no partial rows")
    n_stem_rows = max(stem_rows) + 1
    occupied_cols = {
        col
        for row in range(n_stem_rows)
        for col in range(N_COLS)
        if (col, row) not in free
    }
    n_stem_cols = min(occupied_cols)
    return n_stem_cols, n_stem_rows


def _scale_and_origin(geom: dict, n_stem_cols: int, n_stem_rows: int) -> tuple[float, float, float, float]:
    """Pin the L inner corner to the grid line after the stem cells."""
    sx = (geom["stem_right"] - geom["left"]) / n_stem_cols
    sy = (geom["arm_top"] - geom["top"]) / n_stem_rows
    return sx, sy, geom["left"], geom["top"]


def _cell_box(i: int, j: int, sx: float, sy: float, ox: float, oy: float) -> tuple[float, float, float, float]:
    return ox + sx * i, ox + sx * (i + 1), oy + sy * j, oy + sy * (j + 1)


def _inside_l(box: tuple[float, float, float, float], geom: dict) -> bool:
    x0, x1, y0, y1 = box
    if x0 < geom["left"] - 1e-9 or y0 < geom["top"] - 1e-9:
        return False
    if x1 > geom["right"] + 1e-9 or y1 > geom["bottom"] + 1e-9:
        return False
    # The missing corner is the open notch to the right of the stem and above the arm.
    notch_x0 = max(x0, geom["stem_right"])
    notch_x1 = min(x1, geom["right"])
    notch_y0 = max(y0, geom["top"])
    notch_y1 = min(y1, geom["arm_top"])
    return not (notch_x1 > notch_x0 + 1e-9 and notch_y1 > notch_y0 + 1e-9)


def _hits_disc(box: tuple[float, float, float, float], disc: tuple[float, float, float]) -> bool:
    x0, x1, y0, y1 = box
    cx, cy, radius = disc
    dx = 0.0 if x0 <= cx <= x1 else min(abs(cx - x0), abs(cx - x1))
    dy = 0.0 if y0 <= cy <= y1 else min(abs(cy - y0), abs(cy - y1))
    return dx * dx + dy * dy <= radius * radius + 1e-9


def _hits_rect(box: tuple[float, float, float, float], rect: tuple[float, float, float, float]) -> bool:
    x0, x1, y0, y1 = box
    a, b, c, d = rect
    return x0 <= b + 1e-9 and x1 >= a - 1e-9 and y0 <= d + 1e-9 and y1 >= c - 1e-9


def _obstacle_rects(geom: dict) -> tuple[tuple[float, float, float, float], ...]:
    """Stem square first, then the upper arm rectangle, then the lower one."""
    stem = [rect for rect in geom["rects"] if rect[1] <= geom["stem_right"] + 1e-9]
    arms = [rect for rect in geom["rects"] if rect not in stem]
    if len(stem) != 1 or len(arms) != 2:
        raise AssertionError(f"expected one stem square and two arm rectangles, got {geom['rects']}")
    arms.sort(key=lambda rect: rect[2])
    return stem[0], arms[0], arms[1]


def occupancy(svg: str) -> tuple[dict[tuple[int, int], tuple[int, ...]], tuple[float, float, float, float]]:
    """Map each panel-(d) cell to the obstacles that make it unavailable.

    ``0`` means the cell is not entirely inside the L. ``1`` is the disc,
    ``2`` the stem square, ``3`` the upper arm rectangle, and ``4`` the lower one.
    """
    geom = _geometry(svg)
    n_cols, n_rows = _stem_cell_counts(svg, geom)
    sx, sy, ox, oy = _scale_and_origin(geom, n_cols, n_rows)
    result = {}
    for j in range(N_ROWS):
        for i in range(N_COLS):
            box = _cell_box(i, j, sx, sy, ox, oy)
            ids: list[int] = []
            if not _inside_l(box, geom):
                ids.append(0)
            if _hits_disc(box, geom["disc"]):
                ids.append(1)
            for index, rect in enumerate(_obstacle_rects(geom), start=2):
                if _hits_rect(box, rect):
                    ids.append(index)
            result[(i, j)] = tuple(ids)
    return result, (sx, sy, ox, oy)


def free_cells(svg: str) -> set[tuple[int, int]]:
    cells, _scale = occupancy(svg)
    return {key for key, ids in cells.items() if ids == ()}


def _png_center(image: np.ndarray, i: int, j: int) -> tuple[int, int, int]:
    scale_x = image.shape[1] / SVG_W
    scale_y = image.shape[0] / SVG_H
    x = (FRAME_ORIGIN[0] + CELL * i + CELL / 2.0) * scale_x
    y = (FRAME_ORIGIN[1] + CELL * j + CELL / 2.0) * scale_y
    pixel = image[int(round(y)), int(round(x)), :3]
    return int(pixel[0]), int(pixel[1]), int(pixel[2])


def _near(pixel: tuple[int, int, int], color: tuple[int, int, int], tol: int = 8) -> bool:
    return all(abs(channel - target) <= tol for channel, target in zip(pixel, color))


def test_figure5d_raster_matches_conservative_geometry() -> None:
    svg = SVG_PATH.read_text(encoding="utf-8")
    predicted, scale = occupancy(svg)
    assert scale[0] == (38 - 15) / 7
    assert scale[1] == (183 - 157) / 8
    assert scale[2:] == (15.0, 157.0)
    free = {key for key, ids in predicted.items() if ids == ()}
    drawn = _panel_cells(svg, *FRAME_ORIGIN)
    assert drawn == free
    lower = {
        (i, j)
        for j in range(9, N_ROWS)
        for i in range(8, N_COLS)
        if predicted[(i, j)] != ()
    }
    assert lower == LOWER_RIGHT_OCCUPIED
    # The old staircase marked (9, 10) black and left (14, 15) white.
    assert predicted[(9, 10)] == ()
    assert 4 in predicted[(14, 15)]
    assert predicted[(11, 12)] == (3, 4)
    labels = re.findall(r"<text\b([^>]*)>([^<]*)</text>", svg)
    placed = []
    for attrs, body in labels:
        if body.strip() not in {"1", "2", "3", "4"}:
            continue
        x = float(_attr(f"<t {attrs}>", "x"))
        y = float(_attr(f"<t {attrs}>", "y"))
        placed.append((body.strip(), x, y))
    for digit in ("1", "2", "3", "4"):
        assert sum(item[0] == digit for item in placed) >= 2, placed
    for path in PNG_PATHS:
        image = np.asarray(Image.open(path))
        assert image.shape[1] == 2400 and image.shape[0] == 1268
        for (i, j), ids in predicted.items():
            pixel = _png_center(image, i, j)
            if ids == ():
                assert pixel == (255, 255, 255), ((i, j), pixel, path.name)
            else:
                assert _near(pixel, FRAME_DARK), ((i, j), pixel, path.name)
        # Glyphs sit on the obstacle clusters, so a black cell near each
        # right-hand label center is no longer a flat frame color.
        for digit, _x, _y in placed:
            if float(_x) < FRAME_ORIGIN[0]:
                continue
            window = image[
                int(float(_y) * image.shape[0] / SVG_H) - 6 : int(float(_y) * image.shape[0] / SVG_H) + 7,
                int(float(_x) * image.shape[1] / SVG_W) - 6 : int(float(_x) * image.shape[1] / SVG_W) + 7,
                :3,
            ]
            assert (window == 255).all(axis=2).any(), (digit, path.name)


if __name__ == "__main__":
    test_figure5d_raster_matches_conservative_geometry()
    print("ok test_figure5d_raster_matches_conservative_geometry")
