"""Speed-study curves from the saved comparison_summary.csv files."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
import pandas as pd

from style_loader import inches, load, stroke
from tikzfig import FIGURES


DATA_ROOT = Path(
    "/home/panyz/workspace/Tsinghua/cpp_paper/Coverage_Path_Planning"
    "/pathCoverage_experiment/experiments/vehicle_speed_comparison/results"
)
PANELS = {
    "simple": DATA_ROOT / "map_test1" / "comparison_summary.csv",
    "complex": DATA_ROOT / "parkingGraph" / "comparison_summary.csv",
}


def read_series(csv_path: Path) -> list[dict[str, float]]:
    frame = pd.read_csv(csv_path)
    if frame.empty:
        raise ValueError(f"no rows in {csv_path}")
    frame = frame.sort_values("configured_speed_mps")
    series = []
    for row in frame.itertuples(index=False):
        speed = float(row.configured_speed_mps)
        omega = float(row.arm_angular_velocity_deg_s)
        ratio = float(row.full_trajectory_disc_coverage_ratio)
        duration = float(row.duration_seconds)
        if omega == 0 or speed <= 0 or ratio < 0 or duration < 0:
            raise ValueError(f"unexpected row in {csv_path}: speed={speed}")
        series.append(
            {
                "speed_mps": speed,
                "arm_deg_s": omega,
                "rho_m_per_deg": speed / omega,
                "coverage_ratio": ratio,
                "coverage_percent": 100.0 * ratio,
                "duration_seconds": duration,
            }
        )
    return series


def plot_series(series: list[dict[str, float]], dest: Path) -> None:
    colors = load()
    width = inches(colors, "__speed_in")
    main = stroke("main")
    aux = stroke("aux")
    speeds = [row["speed_mps"] for row in series]
    coverage = [row["coverage_percent"] for row in series]
    duration = [row["duration_seconds"] for row in series]
    if min(speeds) <= 0:
        raise ValueError("a non-positive speed would put a marker at the origin")

    fig, coverage_axis = plt.subplots(figsize=(width, 2.55))
    duration_axis = coverage_axis.twinx()
    coverage_axis.plot(
        speeds,
        coverage,
        color=colors["path"],
        linewidth=main,
        marker="o",
        markersize=4.2,
        markerfacecolor=colors["path"],
        markeredgecolor=colors["ink"],
        markeredgewidth=aux,
        label="Coverage",
        zorder=3,
    )
    duration_axis.plot(
        speeds,
        duration,
        color=colors["emphasis"],
        linewidth=main,
        marker="s",
        markersize=3.6,
        markerfacecolor=colors["emphasis"],
        markeredgecolor=colors["ink"],
        markeredgewidth=aux,
        label="Time",
        zorder=3,
    )
    coverage_axis.set_xlim(0, max(speeds) * 1.08)
    coverage_axis.set_xticks([0.0, *speeds])
    coverage_axis.set_xlabel("Base speed $v$ (m/s)\n$\\rho = v/\\omega_a$")
    coverage_axis.set_ylabel("Coverage (%)")
    duration_axis.set_ylabel("Time (s)")
    low = min(coverage)
    coverage_axis.set_ylim(low - 3.0, 100.0)
    duration_axis.set_ylim(min(duration) * 0.9, max(duration) * 1.06)
    coverage_axis.grid(True, axis="y")
    duration_axis.grid(False)
    for spine in duration_axis.spines.values():
        spine.set_linewidth(aux)
        spine.set_color(colors["ink"])
    if coverage_axis.get_xlim()[0] != 0:
        raise SystemExit("speed axis does not start at 0")
    ticks = [float(tick) for tick in coverage_axis.get_xticks()]
    if not any(abs(tick) < 1e-9 for tick in ticks):
        raise SystemExit("speed axis has no tick at 0")
    for line in coverage_axis.get_lines() + duration_axis.get_lines():
        if any(abs(float(value)) < 1e-9 for value in line.get_xdata()):
            raise SystemExit("a data point was plotted at speed 0")
    if len(coverage_axis.get_lines()) != 1 or len(duration_axis.get_lines()) != 1:
        raise SystemExit("expected one coverage curve and one time curve")
    lines = coverage_axis.get_lines() + duration_axis.get_lines()
    coverage_axis.legend(
        lines,
        [line.get_label() for line in lines],
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=2,
        handlelength=1.8,
        columnspacing=1.1,
        borderaxespad=0.0,
    )
    fig.subplots_adjust(left=0.20, right=0.80, bottom=0.20, top=0.82)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest)
    x0 = coverage_axis.get_xlim()[0]
    plt.close(fig)
    print(dest)
    for row in series:
        print(
            "DATA speed"
            f" file={dest.name}"
            f" v={row['speed_mps']:.12g}"
            f" rho={row['rho_m_per_deg']:.12g}"
            f" coverage_ratio={row['coverage_ratio']:.12g}"
            f" duration_s={row['duration_seconds']:.12g}"
            f" xlim0={x0:.12g}"
            f" ticks={','.join(f'{tick:.12g}' for tick in ticks)}"
        )


def draw(panel: str, filename: str) -> None:
    series = read_series(PANELS[panel])
    plot_series(series, FIGURES / filename)
