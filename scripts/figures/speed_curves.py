"""Redraw the two speed-study curves from the existing CSVs (revision 81).

The rho axis starts at 0. Ticks and markers stay on the measured ratios
only: there is no sample at rho=0 and no single-strip curve. Titles are
simple and complex. The CSVs are read in place and are not copied.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

from paper_style import figures_dir, use_serif


COVERAGE_COLOR = "#42678D"
DURATION_COLOR = "#B45A5A"
GRID_COLOR = "#B9B9B9"
_DATA = Path(
    "/home/panyz/workspace/Tsinghua/cpp_paper/Coverage_Path_Planning"
    "/pathCoverage_experiment/experiments/vehicle_speed_comparison/results"
)
_PLOTS = (
    (_DATA / "map_test1" / "comparison_summary.csv", "simple",
     "figure_5a_vehicle_speed_map_simple_en.png"),
    (_DATA / "parkingGraph" / "comparison_summary.csv", "complex",
     "figure_5b_vehicle_speed_parkingGraph_en.png"),
)


def _read_rows(summary_csv: Path) -> pd.DataFrame:
    rows = pd.read_csv(summary_csv)
    if rows.empty:
        raise ValueError(f"no rows in {summary_csv}")
    rows = rows.sort_values("configured_speed_mps").copy()
    rows["rho_m_per_deg"] = (
        rows["configured_speed_mps"] / rows["arm_angular_velocity_deg_s"]
    )
    rows["coverage_percent"] = 100.0 * rows["full_trajectory_disc_coverage_ratio"]
    return rows


def _style_axis(axis, *, grid: bool) -> None:
    for spine in axis.spines.values():
        spine.set_color("black")
        spine.set_linewidth(0.9)
    axis.tick_params(direction="out", length=3.2, width=0.8, color="black")
    if grid:
        axis.grid(True, axis="y", linestyle=":", linewidth=0.75, color=GRID_COLOR, zorder=0)
    else:
        axis.grid(False)


def _plot(summary_csv: Path, title: str, output: Path) -> None:
    rows = _read_rows(summary_csv)
    speeds = rows["configured_speed_mps"].to_numpy()
    durations = rows["duration_seconds"].to_numpy()
    coverage = rows["coverage_percent"].to_numpy()
    rho = rows["rho_m_per_deg"].to_numpy()
    if len(rho) != len(rows) or (rho <= 0).any():
        raise SystemExit(f"unexpected rho values in {summary_csv}")

    fig, coverage_axis = plt.subplots(figsize=(7.1, 4.4))
    duration_axis = coverage_axis.twinx()
    coverage_axis.plot(
        rho, coverage, color=COVERAGE_COLOR, marker="o", markersize=5.8,
        markeredgecolor="black", markeredgewidth=0.45, linewidth=1.45,
        label="Full-trajectory coverage",
    )
    duration_axis.plot(
        rho, durations, color=DURATION_COLOR, marker="s", markersize=5.2,
        markeredgecolor="black", markeredgewidth=0.45, linewidth=1.45,
        label="Total duration",
    )
    reference = rows.loc[rows["configured_speed_mps"].sub(1.0).abs().idxmin()]
    coverage_axis.annotate(
        "1.0 m/s",
        (reference["rho_m_per_deg"], reference["coverage_percent"]),
        xytext=(6, 7), textcoords="offset points", fontsize=8, color="black",
    )
    coverage_axis.set_xlabel(
        r"Vehicle speed $v$ (m/s)   |   Speed-to-arm-rate ratio $\rho$ (m/deg)",
        labelpad=28,
    )
    coverage_axis.set_ylabel("Full-trajectory coverage (%)", color=COVERAGE_COLOR)
    duration_axis.set_ylabel("Total duration (s)", color=DURATION_COLOR)
    coverage_axis.tick_params(axis="y", colors=COVERAGE_COLOR)
    duration_axis.tick_params(axis="y", colors=DURATION_COLOR)
    coverage_axis.set_xticks(rho)
    coverage_axis.set_xticklabels([])
    bottom = coverage_axis.get_xaxis_transform()
    for speed, ratio in zip(speeds, rho):
        coverage_axis.annotate(
            f"{speed:g}", xy=(ratio, 0), xycoords=bottom, xytext=(-4, -8),
            textcoords="offset points", ha="right", va="top", fontsize=9.5,
            color="black", clip_on=False,
        )
        coverage_axis.annotate(
            f"{ratio:.5f}", xy=(ratio, 0), xycoords=bottom, xytext=(4, -8),
            textcoords="offset points", ha="left", va="top", fontsize=9.5,
            color="black", clip_on=False,
        )
    coverage_axis.set_ylim(max(0.0, coverage.min() - 2.0), min(100.0, coverage.max() + 1.5))
    right = coverage_axis.get_xlim()[1]
    coverage_axis.set_xlim(left=0, right=right)
    if coverage_axis.get_xlim()[0] != 0:
        raise SystemExit("rho axis does not start at 0")
    if 0 in set(coverage_axis.get_xticks()):
        raise SystemExit("a tick was placed at rho=0")
    duration_axis.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
    _style_axis(coverage_axis, grid=True)
    _style_axis(duration_axis, grid=False)
    coverage_axis.set_title(title, pad=10)
    lines = coverage_axis.get_lines() + duration_axis.get_lines()
    coverage_axis.legend(
        lines, [line.get_label() for line in lines], loc="upper right",
        bbox_to_anchor=(0.985, 0.985), ncol=2, handlelength=2.1, columnspacing=1.25,
    )
    fig.subplots_adjust(left=0.105, right=0.875, bottom=0.205, top=0.90)
    with plt.rc_context({"savefig.bbox": None}):
        fig.savefig(output, dpi=600)
    plt.close(fig)
    print(output)


def main() -> None:
    use_serif()
    plt.rcParams.update({
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.labelweight": "bold",
        "axes.linewidth": 0.9,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "legend.fontsize": 9.5,
        "legend.frameon": False,
    })
    out_dir = figures_dir()
    for csv_path, title, name in _PLOTS:
        _plot(csv_path, title, out_dir / name)


if __name__ == "__main__":
    main()
