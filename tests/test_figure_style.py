"""The eight figure scripts use only the shared style and the saved numbers."""

from __future__ import annotations

import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "figures"))

from coverage_comparison import BASELINE, OURS, read_json  # noqa: E402
from pipeline_box4 import SVG, TITLE, visible_text  # noqa: E402
from speed_data import PANELS, read_series  # noqa: E402

STYLE_TEX = ROOT / "figures" / "style" / "paperstyle.tex"
STYLE_MPL = ROOT / "figures" / "style" / "paper.mplstyle"
FIGURES = ROOT / "english_paper" / "figures"
BUILDERS = [
    "class_quadrant.py",
    "strip_geometry.py",
    "speed_coupling.py",
    "coverage_segments.py",
    "figure6_primitive.py",
    "coverage_comparison.py",
    "figure_5a_vehicle_speed_map_simple_en.py",
    "figure_5b_vehicle_speed_parkingGraph_en.py",
    "pipeline_box4.py",
]
FULL_WIDTH_PT = 455.24411 * 72 / 72.27
SPEED_WIDTH_PT = 223.07211 * 72 / 72.27
PDFS = {
    "figure_cpp_class_quadrant.pdf": FULL_WIDTH_PT,
    "figure_strip_geometry.pdf": FULL_WIDTH_PT,
    "figure_speed_coupling.pdf": FULL_WIDTH_PT,
    "figure_coverage_segments.pdf": FULL_WIDTH_PT,
    "figure_2_coverage_comparison_en.pdf": FULL_WIDTH_PT,
    "figure_5a_vehicle_speed_map_simple_en.pdf": SPEED_WIDTH_PT,
    "figure_5b_vehicle_speed_parkingGraph_en.pdf": SPEED_WIDTH_PT,
    "pipeline_overall_improved_en.pdf": FULL_WIDTH_PT,
}


def test_style_defines_the_five_roles_and_two_strokes():
    tex = STYLE_TEX.read_text(encoding="utf-8")
    mpl = STYLE_MPL.read_text(encoding="utf-8")
    colors = dict(re.findall(r"\\definecolor\{(\w+)\}\{HTML\}\{([0-9A-Fa-f]{6})\}", tex))
    for role in ("disc", "discfill", "chassis", "path", "secondary", "emphasis"):
        assert role in colors
        assert colors[role] in mpl.replace("#", "")
    assert r"\newcommand{\lwmain}{0.8pt}" in tex
    assert r"\newcommand{\lwaux}{0.5pt}" in tex
    assert re.search(r"^lines\.linewidth:\s*0\.8\s*$", mpl, re.M)
    assert re.search(r"^grid\.linewidth:\s*0\.5\s*$", mpl, re.M)


def test_figure_scripts_do_not_define_colors_or_strokes():
    for name in BUILDERS:
        text = (ROOT / "scripts" / "figures" / name).read_text(encoding="utf-8")
        assert not re.search(r"#[0-9A-Fa-f]{6}", text), name
        assert "0.8pt" not in text and "0.5pt" not in text, name
        assert "definecolor" not in text, name


def test_speed_series_match_the_csv_files():
    for panel, path in PANELS.items():
        series = read_series(path)
        frame = pd.read_csv(path).sort_values("configured_speed_mps")
        assert len(series) == len(frame) == 6
        for row, saved in zip(series, frame.itertuples(index=False)):
            assert row["speed_mps"] == float(saved.configured_speed_mps)
            assert row["coverage_ratio"] == float(saved.full_trajectory_disc_coverage_ratio)
            assert row["duration_seconds"] == float(saved.duration_seconds)
            assert row["rho_m_per_deg"] == row["speed_mps"] / float(saved.arm_angular_velocity_deg_s)
            assert row["speed_mps"] > 0
        assert panel in {"simple", "complex"}


def test_coverage_labels_match_the_metrics_files():
    for panel, spec in OURS.items():
        saved = read_json(spec["metrics"])
        ratio = float(saved["coverage"]["full_trajectory_disc"]["coverage_ratio"])
        assert f"{ratio * 100:.2f}" in {"94.11", "95.73"}
        assert panel in {"simple", "complex"}
    for panel, spec in BASELINE.items():
        saved = read_json(spec["metrics"])
        ratio = float(saved["coverage_ratio"])
        outside = float(saved["path_validation"]["swept_area_outside_field_m2"])
        assert f"{ratio * 100:.2f}" in {"78.40", "92.84"}
        assert f"{outside:.2f}" in {"4.51", "20.00"}
        assert panel in {"simple", "complex"}


def test_pipeline_title_and_shared_weight():
    svg = SVG.read_text(encoding="utf-8")
    assert TITLE in visible_text(svg[svg.find('x="857.5" y="452"') - 80 : svg.find('x="857.5" y="452"') + 400])
    assert "font-weight: 700" in svg
    assert svg.count('class="title-small"') >= 4
    assert "Liberation" not in svg
    assert "base64" not in svg


def _fold_pdf_text(raw: str) -> str:
    """Turn mathematical italic from pdftotext into ASCII, then restore subscripts."""
    pieces = []
    for ch in raw:
        code = ord(ch)
        if 0x1D434 <= code <= 0x1D44D:
            pieces.append(chr(ord("A") + code - 0x1D434))
        elif 0x1D44E <= code <= 0x1D467:
            pieces.append(chr(ord("a") + code - 0x1D44E))
        elif code in (0x1D719, 0x1D711, 0x03D5, 0x03C6):
            pieces.append("phi")
        elif code == 0x2212:
            pieces.append("-")
        else:
            pieces.append(ch)
    text = re.sub(r"\s+", "", "".join(pieces))
    text = text.replace("phiw", "phi_w").replace("2rd", "2r_d")
    text = text.replace("vwork", "v_work").replace("Thalf", "T_half")
    return text


def _near(rgb, target, tol):
    return all(abs(int(channel) - want) <= tol for channel, want in zip(rgb, target))


def _px(mm, dpi):
    return mm * dpi / 25.4


def _sample(image, x_mm, y_mm, height_mm, dpi):
    pixel_x = int(round(_px(x_mm, dpi)))
    pixel_y = int(round(_px(height_mm - y_mm, dpi)))
    pixel_x = min(max(pixel_x, 0), image.width - 1)
    pixel_y = min(max(pixel_y, 0), image.height - 1)
    return image.getpixel((pixel_x, pixel_y))[:3], pixel_x, pixel_y


def _window_has(image, x_mm, y_mm, height_mm, dpi, target, tol, radius=2):
    cx = int(round(_px(x_mm, dpi)))
    cy = int(round(_px(height_mm - y_mm, dpi)))
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            px = min(max(cx + dx, 0), image.width - 1)
            py = min(max(cy + dy, 0), image.height - 1)
            if _near(image.getpixel((px, py))[:3], target, tol):
                return True
    return False


def _render(pdf: Path, dpi: int) -> Image.Image:
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.check_call(
            ["pdftocairo", "-png", "-r", str(dpi), "-singlefile", str(pdf), f"{tmp}/fig"],
        )
        image = Image.open(f"{tmp}/fig.png").convert("RGB")
        image.load()
        return image


def test_speed_coupling_and_coverage_segments_semantics():
    subprocess.check_call([sys.executable, "scripts/figures/speed_coupling.py"], cwd=ROOT)
    speed_src = (ROOT / "scripts" / "figures" / "speed_coupling.py").read_text(encoding="utf-8")
    assert not re.search(r"#[0-9A-Fa-f]{6}", speed_src)
    assert "0.8pt" not in speed_src and "0.5pt" not in speed_src
    assert "definecolor" not in speed_src

    assert speed_src.count(r"\draw[dim]") == 1
    dim_at = speed_src.find(r"\draw[dim]")
    dim_label = speed_src[dim_at : speed_src.find("\n", speed_src.find("$2r_d$", dim_at)) + 1]
    assert "$2r_d$" in dim_label
    assert "T_" not in dim_label
    assert r"arc[start angle=0, end angle=-50" in speed_src
    assert r"arc[start angle=0, end angle=50" in speed_src
    assert r"$-\phi_w$" in speed_src and r"$+\phi_w$" in speed_src
    assert r"$t=0$" in speed_src and r"$t=T_{\mathrm{half}}$" in speed_src
    speed_txt = _fold_pdf_text(
        subprocess.check_output(
            ["pdftotext", "-layout", str(FIGURES / "figure_speed_coupling.pdf"), "-"],
            text=True,
        )
    )
    for token in ("2r_d", "T_half", "v_work", "phi_w", "t=0", "t=T_half"):
        assert token in speed_txt, (token, speed_txt)


def _box_area(box):
    return (box[2] - box[0]) * (box[3] - box[1])


def _contains_box(outer, inner, slack=0.05):
    return (
        outer[0] <= inner[0] + slack
        and outer[1] <= inner[1] + slack
        and outer[2] >= inner[2] - slack
        and outer[3] >= inner[3] - slack
    )


def _overlaps_interior(band, rect):
    x, y, w, h = band
    return (
        x < rect["x"] + rect["w"] - 1e-6
        and x + w > rect["x"] + 1e-6
        and y < rect["y"] + rect["h"] - 1e-6
        and y + h > rect["y"] + 1e-6
    )


def _gray_bbox(bands):
    return (
        min(b[0] for b in bands),
        min(b[1] for b in bands),
        max(b[0] + b[2] for b in bands),
        max(b[1] + b[3] for b in bands),
    )


def _at_turn_or_transfer(band, rects):
    x, _y, w, _h = band
    left, right = rects
    for rect in rects:
        if abs((x + w) - rect["x"]) < 1e-6 and x + w <= rect["x"] + 1e-6:
            return True
        if abs(x - (rect["x"] + rect["w"])) < 1e-6:
            return True
    gap0 = left["x"] + left["w"]
    gap1 = right["x"]
    return x >= gap0 - 1e-6 and x + w <= gap1 + 1e-6


def _boxes_overlap(a, b, eps=1e-6):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return (
        ax < bx + bw - eps
        and ax + aw > bx + eps
        and ay < by + bh - eps
        and ay + ah > by + eps
    )


def _arrow_on_strip(arrows, strip):
    x, y, w, h = strip
    mid = y + h / 2.0
    found = [
        arrow
        for arrow in arrows
        if abs(arrow[1] - mid) < 1e-6
        and abs(arrow[3] - mid) < 1e-6
        and min(arrow[0], arrow[2]) >= x - 1e-6
        and max(arrow[0], arrow[2]) <= x + w + 1e-6
    ]
    assert len(found) == 1, (strip, found)
    return found[0]


def _goes_right(arrow):
    return arrow[2] > arrow[0]


def _start_x(rect, arrow):
    return rect["x"] if _goes_right(arrow) else rect["x"] + rect["w"]


def _end_x(rect, arrow):
    return rect["x"] + rect["w"] if _goes_right(arrow) else rect["x"]


def _y_hits(band, strip):
    _x, y, _w, h = band
    _sx, sy, _sw, sh = strip
    return y < sy + sh - 1e-6 and y + h > sy + 1e-6


def _band_on_end(band, rect, end_x):
    x, _y, w, _h = band
    if abs(end_x - (rect["x"] + rect["w"])) < 1e-6:
        return abs(x - end_x) < 1e-6
    if abs(end_x - rect["x"]) < 1e-6:
        return abs((x + w) - end_x) < 1e-6
    return False


def _assert_lane_changes_follow_the_path(panel, gray_w):
    """Each gray band is the path's turn or the one transfer, and they do not overlap."""
    left, right = panel["rectangles"]
    transfers = [
        band
        for band in panel["gray"]
        if abs(band[0] - (left["x"] + left["w"])) < 1e-6 and abs((band[0] + band[2]) - right["x"]) < 1e-6
    ]
    assert len(transfers) == 1, transfers
    transfer = transfers[0]
    assert abs(transfer[3] - gray_w) < 1e-9
    turns = [band for band in panel["gray"] if band != transfer]
    assert len(turns) == 2 * (len(left["strips"]) - 1)
    for band in turns:
        assert not _boxes_overlap(band, transfer), (band, transfer)
    for index, band in enumerate(turns):
        for other in turns[index + 1 :]:
            assert not _boxes_overlap(band, other), (band, other)

    def strip_at(rect, y_mid):
        hits = [
            index
            for index, strip in enumerate(rect["strips"])
            if abs((strip[1] + strip[3] / 2.0) - y_mid) < 1e-6
        ]
        assert len(hits) == 1
        return hits[0]

    y_mid = transfer[1] + transfer[3] / 2.0
    src = strip_at(left, y_mid)
    dst = strip_at(right, y_mid)
    src_arrow = _arrow_on_strip(panel["arrows"], left["strips"][src])
    dst_arrow = _arrow_on_strip(panel["arrows"], right["strips"][dst])
    assert abs(transfer[0] - _end_x(left, src_arrow)) < 1e-6
    assert abs((transfer[0] + transfer[2]) - _start_x(right, dst_arrow)) < 1e-6

    def unseen_neighbor(rect, index, seen, *, at_start):
        anchor = _arrow_on_strip(panel["arrows"], rect["strips"][index])
        x_value = _start_x(rect, anchor) if at_start else _end_x(rect, anchor)
        hits = []
        for other in (index - 1, index + 1):
            if other < 0 or other >= len(rect["strips"]) or other in seen:
                continue
            arrow = _arrow_on_strip(panel["arrows"], rect["strips"][other])
            other_x = _end_x(rect, arrow) if at_start else _start_x(rect, arrow)
            if abs(other_x - x_value) < 1e-6:
                hits.append(other)
        assert len(hits) <= 1, (panel["tag"], index, hits)
        return hits[0] if hits else None

    def hop_band(rect, leave, enter):
        shared = _end_x(rect, _arrow_on_strip(panel["arrows"], rect["strips"][leave]))
        assert abs(shared - _start_x(rect, _arrow_on_strip(panel["arrows"], rect["strips"][enter]))) < 1e-6
        matched = [
            band
            for band in turns
            if _band_on_end(band, rect, shared)
            and _y_hits(band, rect["strips"][leave])
            and _y_hits(band, rect["strips"][enter])
        ]
        assert len(matched) == 1, (panel["tag"], leave, enter, shared, matched)
        assert abs(min(matched[0][2], matched[0][3]) - gray_w) < 1e-9
        return matched[0]

    used = []
    cursor = src
    seen = {cursor}
    while True:
        prev = unseen_neighbor(left, cursor, seen, at_start=True)
        if prev is None:
            break
        used.append(hop_band(left, prev, cursor))
        seen.add(prev)
        cursor = prev
    assert seen == set(range(len(left["strips"])))

    cursor = dst
    seen = {cursor}
    while True:
        nxt = unseen_neighbor(right, cursor, seen, at_start=False)
        if nxt is None:
            break
        used.append(hop_band(right, cursor, nxt))
        seen.add(nxt)
        cursor = nxt
    assert seen == set(range(len(right["strips"])))
    assert len(used) == len(turns)
    assert {tuple(band) for band in used} == {tuple(band) for band in turns}


def test_coverage_segments_tiles_and_marks():
    from coverage_segments import (  # noqa: E402
        GRAY_W,
        H_R,
        N_S,
        R_D,
        W_S,
        _body,
        layout,
    )

    assert abs(N_S * W_S - H_R) < 1e-9
    assert abs(GRAY_W - 2 * R_D) < 1e-9
    assert GRAY_W < W_S
    spec = layout()
    panels = spec["panels"]
    assert [panel["tag"] for panel in panels] == ["(a)", "(b)"]
    assert panels[0]["mark_name"] == "c_work"
    assert panels[1]["mark_name"] == "c_traj"
    orange = (244, 185, 154)
    gray = (214, 214, 214)
    navy = (21, 96, 130)

    for panel in panels:
        assert len(panel["rectangles"]) == 2
        for rect in panel["rectangles"]:
            strips = rect["strips"]
            assert len(strips) == N_S
            assert abs(rect["h"] - H_R) < 1e-9
            assert abs(strips[0][1] - rect["y"]) < 1e-9
            for left_strip, right_strip in zip(strips, strips[1:]):
                assert abs(left_strip[0] - rect["x"]) < 1e-9
                assert abs(left_strip[2] - rect["w"]) < 1e-9
                assert abs(left_strip[3] - W_S) < 1e-9
                assert abs((left_strip[1] + left_strip[3]) - right_strip[1]) < 1e-9
            assert abs((strips[-1][1] + strips[-1][3]) - (rect["y"] + rect["h"])) < 1e-9
        for band in panel["gray"]:
            assert abs(min(band[2], band[3]) - GRAY_W) < 1e-9
            assert _at_turn_or_transfer(band, panel["rectangles"])
            for rect in panel["rectangles"]:
                assert not _overlaps_interior(band, rect)
        _assert_lane_changes_follow_the_path(panel, GRAY_W)
        assert _contains_box(panel["mark"], panel["orange_bbox"])
        assert panel["mark"][3] + 5.0 < spec["height_mm"]
        assert panel["tag_at"][1] > 3.0

    work = panels[0]
    one = work["rectangles"][0]["strips"][0]
    one_box = (one[0], one[1], one[0] + one[2], one[1] + one[3])
    assert _box_area(work["mark"]) > _box_area(one_box) * (N_S + 1)
    full = panels[1]
    gray_box = _gray_bbox(full["gray"])
    assert _contains_box(full["mark"], full["union_bbox"])
    assert _contains_box(full["union_bbox"], gray_box)
    assert (full["union_bbox"][3] - full["union_bbox"][1]) > (gray_box[3] - gray_box[1]) + 1.0
    assert _box_area(full["mark"]) > _box_area(gray_box)

    cover_src = (ROOT / "scripts" / "figures" / "coverage_segments.py").read_text(encoding="utf-8")
    assert not re.search(r"#[0-9A-Fa-f]{6}", cover_src)
    assert "0.8pt" not in cover_src and "0.5pt" not in cover_src
    assert "definecolor" not in cover_src
    assert "circle" not in cover_src
    body = _body(spec)
    assert body.count("nonworkfill") == len(full["gray"])
    assert body.count("workband") == 2 * len(work["rectangles"]) * N_S
    assert r"\mathcal{C}_{\mathrm{work}}" in body and r"\mathcal{C}_{\mathrm{traj}}" in body

    subprocess.check_call([sys.executable, "scripts/figures/coverage_segments.py"], cwd=ROOT)
    cover_raw = subprocess.check_output(
        ["pdftotext", "-layout", str(FIGURES / "figure_coverage_segments.pdf"), "-"],
        text=True,
    )
    assert "(a)" in cover_raw and "(b)" in cover_raw
    compact = re.sub(r"\s+", "", cover_raw).replace("Cwork", "C_work").replace("Ctraj", "C_traj")
    assert "C_work" in compact and "C_traj" in compact

    dpi = 144
    image = _render(FIGURES / "figure_coverage_segments.pdf", dpi)
    assert abs(image.width - _px(spec["width_mm"], dpi)) < 3

    def mid_edge(box, which):
        x0, y0, x1, y1 = box
        if which == "s":
            return ((x0 + x1) / 2.0, y0)
        if which == "n":
            return ((x0 + x1) / 2.0, y1)
        if which == "w":
            return (x0, (y0 + y1) / 2.0)
        return (x1, (y0 + y1) / 2.0)

    for panel in panels:
        for rect in panel["rectangles"]:
            for strip in rect["strips"]:
                x, y, w, h = strip
                for frac in (0.25, 0.5, 0.75):
                    rgb, _, _ = _sample(image, x + frac * w, y + 0.35 * h, spec["height_mm"], dpi)
                    assert _near(rgb, orange, 8), (panel["tag"], rgb, strip)
            for index in range(len(rect["strips"]) - 1):
                boundary = rect["strips"][index][1] + rect["strips"][index][3]
                x_mid = rect["x"] + 0.5 * rect["w"]
                for sign in (-1, 1):
                    rgb, _, _ = _sample(image, x_mid, boundary + sign * 0.35, spec["height_mm"], dpi)
                    assert _near(rgb, orange, 8), (panel["tag"], "seam", rgb)
        for which in ("s", "n", "w", "e"):
            px, py = mid_edge(panel["mark"], which)
            assert _window_has(image, px, py, spec["height_mm"], dpi, navy, 40, radius=3), (
                panel["tag"],
                which,
            )

    def fill_point(band):
        x, y, w, h = band
        if w <= h:
            return (x + 0.28 * w, y + 0.55 * h)
        return (x + 0.55 * w, y + 0.28 * h)

    for band in work["gray"]:
        px, py = fill_point(band)
        rgb, _, _ = _sample(image, px, py, spec["height_mm"], dpi)
        assert not _near(rgb, gray, 12), rgb
        assert not _near(rgb, orange, 12), rgb
    for band in full["gray"]:
        px, py = fill_point(band)
        rgb, _, _ = _sample(image, px, py, spec["height_mm"], dpi)
        assert _near(rgb, gray, 8), (rgb, band)


def _chassis_sample(pose, half):
    cx, cy = pose["chassis"]
    angle = math.radians(pose["angle"])
    local_x = 0.22 * half[0]
    local_y = 0.62 * half[1]
    return (
        cx + local_x * math.cos(angle) - local_y * math.sin(angle),
        cy + local_x * math.sin(angle) + local_y * math.cos(angle),
    )


def test_figure6_primitive_is_uncropped():
    from figure6_primitive import (  # noqa: E402
        CHASSIS_HALF,
        DISC_R,
        HEIGHT_MM,
        MARGIN_MM,
        WIDTH_MM,
        scene,
    )

    spec = scene()
    assert spec["width_mm"] == WIDTH_MM
    assert spec["height_mm"] == HEIGHT_MM
    assert len(spec["strips"]) == 5
    assert len(spec["poses"]) == 5
    assert len(spec["discs"]) == 6
    horizontal = [segment for segment in spec["path"] if abs(segment[1] - segment[3]) < 1e-6]
    assert any(segment[2] > segment[0] for segment in horizontal)
    assert any(segment[2] < segment[0] for segment in horizontal)
    x0, y0, x1, y1 = spec["rectangle"]
    assert x1 - x0 > 40 and y1 - y0 > 40
    radius = spec["disc_r"]
    assert abs(radius - DISC_R) < 1e-9
    for x, y in spec["discs"]:
        assert x - radius >= MARGIN_MM
        assert y - radius >= MARGIN_MM
        assert x + radius <= WIDTH_MM - MARGIN_MM
        assert y + radius <= HEIGHT_MM - MARGIN_MM
    end_x, end_y = spec["end_disc"]
    assert end_x == max(x for x, _y in spec["discs"])
    assert WIDTH_MM - (end_x + radius) >= MARGIN_MM
    assert end_y + radius <= HEIGHT_MM - MARGIN_MM
    for point in spec["dashed"]:
        assert MARGIN_MM < point[0] < WIDTH_MM - MARGIN_MM
        assert MARGIN_MM < point[1] < HEIGHT_MM - MARGIN_MM
    for pose in spec["poses"]:
        for point in pose["arm"]:
            assert MARGIN_MM < point[0] < WIDTH_MM - MARGIN_MM
            assert MARGIN_MM < point[1] < HEIGHT_MM - MARGIN_MM
    src = (ROOT / "scripts" / "figures" / "figure6_primitive.py").read_text(encoding="utf-8")
    assert not re.search(r"#[0-9A-Fa-f]{6}", src)
    assert "0.8pt" not in src and "0.5pt" not in src
    assert "definecolor" not in src
    assert r"\mathcal{C}_{\mathrm{work}}" not in src
    include = (ROOT / "english_paper" / "sections" / "methodology.tex").read_text(encoding="utf-8")
    assert r"\includegraphics[width=0.5\linewidth]{figure_6_single_rectangle_coverage.pdf}" in include
    assert "figure_6_single_rectangle_coverage.png" not in include

    subprocess.check_call([sys.executable, "scripts/figures/figure6_primitive.py"], cwd=ROOT)
    dpi = 288
    image = _render(FIGURES / "figure_6_single_rectangle_coverage.pdf", dpi)
    margin_px = _px(MARGIN_MM, dpi)
    assert image.getpixel((1, 1))[0] > 250
    assert image.getpixel((image.width - 2, 2))[0] > 250
    assert image.getpixel((2, image.height - 2))[0] > 250
    disc_fill = (242, 170, 132)
    disc_edge = (233, 113, 50)
    chassis = (143, 223, 237)
    path = (21, 96, 130)
    secondary = (127, 127, 127)
    for x, y in spec["discs"]:
        for step in range(8):
            angle = math.radians(22.5 + 45.0 * step)
            sx = x + 0.55 * radius * math.cos(angle)
            sy = y + 0.55 * radius * math.sin(angle)
            rgb, px, py = _sample(image, sx, sy, HEIGHT_MM, dpi)
            assert _near(rgb, disc_fill, 12), (x, y, step, rgb)
            assert margin_px < px < image.width - margin_px
            assert margin_px < py < image.height - margin_px
            ox = x + 1.45 * radius * math.cos(angle)
            oy = y + 1.45 * radius * math.sin(angle)
            outside, _, _ = _sample(image, ox, oy, HEIGHT_MM, dpi)
            assert not _near(outside, disc_fill, 18), (x, y, step, outside)
        edge_x = x + radius
        assert _px(edge_x, dpi) < image.width - margin_px
    for pose in spec["poses"]:
        sx, sy = _chassis_sample(pose, CHASSIS_HALF)
        rgb, _, _ = _sample(image, sx, sy, HEIGHT_MM, dpi)
        assert _near(rgb, chassis, 12), (pose["chassis"], rgb)
        ax = (pose["arm"][0][0] + pose["arm"][1][0]) / 2.0
        ay = (pose["arm"][0][1] + pose["arm"][1][1]) / 2.0
        assert _window_has(image, ax, ay, HEIGHT_MM, dpi, disc_edge, 35, radius=3), (ax, ay)
    path_mid = spec["path"][0]
    mx = (path_mid[0] + path_mid[2]) / 2.0
    my = path_mid[1]
    assert _window_has(image, mx, my, HEIGHT_MM, dpi, path, 40, radius=3)
    for point in spec["dashed"]:
        assert _window_has(image, point[0], point[1], HEIGHT_MM, dpi, secondary, 35, radius=18), point
    # The dashed stroke and every disc stay off the raster edge.
    pixels = np.asarray(image)
    ink = np.any(pixels < 250, axis=2)
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    assert rows[0] > 2 and cols[0] > 2
    assert rows[-1] < image.height - 3 and cols[-1] < image.width - 3


def test_pdf_media_boxes_match_the_inclusion_width():
    for name, expected in PDFS.items():
        info = subprocess.check_output(["pdfinfo", str(FIGURES / name)], text=True)
        width = float(re.search(r"Page size:\s+([0-9.]+) x", info).group(1))
        assert abs(width - expected) < 1.0, (name, width, expected)


def _run() -> None:
    failures = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
            except Exception as exc:
                failures += 1
                print(f"FAIL {name}: {exc}")
            else:
                print(f"ok {name}")
    if failures:
        raise SystemExit(failures)


if __name__ == "__main__":
    _run()
