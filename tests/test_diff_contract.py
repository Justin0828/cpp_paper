"""The advisor diff keeps the latexdiff notes and points new figures at vector PDFs."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ROOT / "english_paper" / "sections"
FIGURES = ROOT / "english_paper" / "figures"
DIFF = ROOT / "english_paper" / "diff.tex"
OLD_DIFF = "76b418f:english_paper/diff.tex"

VECTOR_PDFS = (
    "figure_cpp_class_quadrant.pdf",
    "figure_strip_geometry.pdf",
    "figure_speed_coupling.pdf",
    "figure_coverage_segments.pdf",
    "figure_2_coverage_comparison_en.pdf",
    "figure_5a_vehicle_speed_map_simple_en.pdf",
    "figure_5b_vehicle_speed_parkingGraph_en.pdf",
    "pipeline_overall_improved_en.pdf",
)
LEGEND = (
    "图例：红色删除线表示被删除的原文；蓝色文字表示新增内容；"
    "边注用中文说明修改理由，对应导师意见中的一条以及具体改法。"
)
RASTER_PAIR = "figure_3_geometric_to_binary_raster.png"


def _brace_body(text: str, start: int) -> str:
    depth = 0
    for index in range(start, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1 : index]
    raise AssertionError("unbalanced brace")


def _marginpar_bodies(text: str) -> list[str]:
    bodies = []
    for match in re.finditer(r"\\marginpar\{", text):
        bodies.append(_brace_body(text, match.end() - 1))
    return bodies


def _blocks(text: str, kind: str) -> list[tuple[str, str]]:
    pattern = re.compile(
        rf"% ==={kind} ([^\n=]+)===\n(.*?)% ==={kind} END \1",
        re.S,
    )
    return [(name, body) for name, body in pattern.findall(text)]


def _includes(body: str) -> list[str]:
    return re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", body)


def test_sections_include_the_eight_vector_pdfs_not_the_pngs():
    sources = "\n".join(path.read_text(encoding="utf-8") for path in sorted(SECTIONS.glob("*.tex")))
    included = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", sources)
    for name in VECTOR_PDFS:
        assert name in included, name
        assert (FIGURES / name).is_file(), name
        png = name.replace(".pdf", ".png")
        assert png not in included, png


def test_figpairs_put_old_png_on_the_left_and_vector_pdf_on_the_right():
    text = DIFF.read_text(encoding="utf-8")
    pairs = _blocks(text, "FIGPAIR")
    assert pairs, "diff.tex has no FIGPAIR blocks"
    raster_pairs = []
    vector_pairs = []
    for name, body in pairs:
        stem = name[:-4] if name.endswith(".png") else name
        includes = _includes(body)
        red_at = body.find(r"\fcolorbox{red}")
        blue_at = body.find(r"\fcolorbox{blue}")
        assert red_at != -1 and blue_at != -1 and red_at < blue_at, name
        pdf = FIGURES / f"{stem}.pdf"
        if pdf.is_file():
            vector_pairs.append(stem)
            assert includes == [
                f"old_figs/{stem}.png",
                f"figures/{stem}.pdf",
            ], (name, includes)
        else:
            raster_pairs.append(stem)
            assert includes == [
                f"old_figs/{stem}.png",
                f"figures/{stem}.png",
            ], (name, includes)
    assert raster_pairs == [RASTER_PAIR[:-4]]
    assert {f"{stem}.pdf" for stem in vector_pairs} == set(VECTOR_PDFS) - {
        "figure_cpp_class_quadrant.pdf",
        "figure_strip_geometry.pdf",
        "figure_speed_coupling.pdf",
        "figure_coverage_segments.pdf",
    }


def test_fignew_blocks_use_the_vector_pdf_and_mark_them_new():
    text = DIFF.read_text(encoding="utf-8")
    blocks = _blocks(text, "FIGNEW")
    assert blocks, "diff.tex has no FIGNEW blocks"
    seen = []
    for name, body in blocks:
        stem = name[:-4] if name.endswith(".png") else name
        includes = _includes(body)
        assert includes == [f"figures/{stem}.pdf"], (name, includes)
        assert (FIGURES / f"{stem}.pdf").is_file(), stem
        assert "新增" in body, name
        seen.append(f"{stem}.pdf")
    assert set(seen) == {
        "figure_cpp_class_quadrant.pdf",
        "figure_strip_geometry.pdf",
        "figure_speed_coupling.pdf",
        "figure_coverage_segments.pdf",
    }


def test_legend_and_margin_notes_from_the_advisor_diff_remain():
    text = DIFF.read_text(encoding="utf-8")
    assert "修订对照说明" in text
    assert LEGEND in text
    assert "本次修订共 81 处，其中 A 类 73 处，B 类 8 处" in text
    previous = subprocess.check_output(["git", "show", OLD_DIFF], text=True)
    old_notes = _marginpar_bodies(previous)
    new_notes = _marginpar_bodies(text)
    assert old_notes, "76b418f diff.tex has no margin notes"
    assert new_notes == old_notes
