"""The eight figure scripts use only the shared style and the saved numbers."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

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
