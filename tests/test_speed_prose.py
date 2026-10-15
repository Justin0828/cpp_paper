"""The speed paragraph and the map-label sentence follow the saved runs."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "figures"))

from work_speed import both_panels  # noqa: E402

EXPERIMENTS = ROOT / "english_paper" / "sections" / "experiments.tex"
METHODOLOGY = ROOT / "english_paper" / "sections" / "methodology.tex"


def _fmt(value: float) -> str:
    return f"{value:.1f}"


def test_truncation_statement_uses_the_saved_runs() -> None:
    panels = both_panels()
    prose = EXPERIMENTS.read_text(encoding="utf-8")
    speed = prose[prose.find("Effect of Base--Arm Velocity Coupling") :]
    statement = speed[
        speed.find("The six commanded speeds") : speed.find("Table~\\ref{tab:speed-study} shows")
    ]
    assert statement, "speed paragraph is missing before the coverage conclusion"
    # The saved runs bypass Eq. (17). The paragraph must say so, and must not
    # report that the equation left every tier untruncated.
    assert "truncated" not in statement
    assert "none of the six" not in statement
    bypass_at = statement.find("do not apply")
    recorded_at = statement.find("recorded work speed is the command")
    conclusion_at = statement.find("leaves more coverage missing")
    assert 0 <= bypass_at < recorded_at < conclusion_at
    assert r"v_{\mathrm{safe}}" in statement
    for name, info in panels.items():
        assert info["policy"] == "commanded"
        assert info["applies_v_safe"] == (info["policy"] == "coverage_safe")
        assert info["recorded_equals_command"] is True
        assert "\\texttt{" + name + "}" in statement
        assert _fmt(info["v_work_min_mps"]) in statement
        assert _fmt(info["v_work_max_mps"]) in statement
        for command, recorded in zip(info["commands_mps"], info["recorded_mps"]):
            assert _fmt(command) in statement
            assert abs(recorded - command) <= 1e-6
    caption = prose[
        prose.find("\\caption{Effect of base--arm") : prose.find("\\label{fig:speed-study}")
    ]
    sample = next(iter(panels.values()))
    assert f"{sample['r_d_m']:.2f}" in caption
    assert f"{sample['arm_length_m']:.2f}" in caption
    assert f"{sample['omega_deg_s']:.0f}" in caption
    for info in panels.values():
        assert info["r_d_m"] == sample["r_d_m"]
        assert info["arm_length_m"] == sample["arm_length_m"]
        assert info["omega_deg_s"] == sample["omega_deg_s"]


def test_map_labels_are_pixel_labels() -> None:
    text = METHODOLOGY.read_text(encoding="utf-8")
    sentence = text[text.find("The labels $0$ and $255$") : text.find("With physical pixel size")]
    assert "8-bit pixel labels" in sentence
    assert "not physical" in sentence
    assert "not grayscale values" not in text
    assert r"M\in\{0,255\}" in text
    assert "s_p" in sentence or "s_p" in text[text.find("With physical pixel size") : text.find("With physical pixel size") + 80]


if __name__ == "__main__":
    test_truncation_statement_uses_the_saved_runs()
    test_map_labels_are_pixel_labels()
    print("ok test_speed_prose")
