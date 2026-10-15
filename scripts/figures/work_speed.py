"""Which commanded speeds Eq. (17) actually truncated in the saved runs.

Eq. (16) sets v_safe = 2 r_d / T_half and Eq. (17) sets v_work = min(v_max, v_safe).
The speed experiment stores the executed work speed, not a per-strip v_safe.
A commanded tier is truncated when that executed speed is below the command.
"""

from __future__ import annotations

import json
from pathlib import Path

DATA_ROOT = Path(
    "/home/panyz/workspace/Tsinghua/cpp_paper/Coverage_Path_Planning"
    "/pathCoverage_experiment/experiments/vehicle_speed_comparison/results"
)
PANELS = {
    "simple": DATA_ROOT / "map_test1",
    "complex": DATA_ROOT / "parkingGraph",
}
COMMANDED = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0)
_SPEED_TOL = 1e-6


def _directory(speed: float) -> str:
    text = f"{speed:.1f}"
    whole, frac = text.split(".")
    return f"speed_{whole}p{frac}"


def _load(panel: str, speed: float) -> dict:
    path = PANELS[panel] / _directory(speed) / "metrics.json"
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def truncation(panel: str) -> dict:
    """Return the truncated commands and the executed work-speed range.

    ``truncated`` lists commands for which the saved trajectory's maximum
    work speed is below v_max, the observable form of Eq. (17). The range is
    the minimum and maximum average work speed actually recorded.
    """
    rows = []
    radii = set()
    lengths = set()
    rates = set()
    for speed in COMMANDED:
        report = _load(panel, speed)
        trajectory = report["trajectory"]
        geometry = report["coverage"]["geometry"]
        commanded = float(trajectory["configured_speed_limit_mps"])
        if abs(commanded - speed) > _SPEED_TOL:
            raise ValueError(f"{panel} {speed}: metrics command is {commanded}")
        actual_max = float(trajectory["actual_max_work_speed_mps"])
        actual_avg = float(trajectory["actual_average_work_speed_mps"])
        # Eq. (17) binds only when the executed speed falls below v_max.
        limited = actual_max < commanded - _SPEED_TOL
        if bool(trajectory["work_speed_limited"]) != limited:
            raise ValueError(f"{panel} {speed}: work_speed_limited disagrees with Eq. (17)")
        rows.append(
            {
                "command_mps": commanded,
                "actual_average_mps": actual_avg,
                "actual_max_mps": actual_max,
                "truncated": limited,
                "policy": trajectory["work_speed_policy"],
            }
        )
        radii.add(float(geometry["disc_radius_m"]))
        lengths.add(float(geometry["arm_length_m"]))
        rates.add(float(trajectory["arm_angular_velocity_limit_deg_s"]))
    if len(radii) != 1 or len(lengths) != 1 or len(rates) != 1:
        raise ValueError(f"{panel}: r_d, L, or arm rate is not fixed across the six runs")
    averages = [row["actual_average_mps"] for row in rows]
    return {
        "panel": panel,
        "policy": rows[0]["policy"],
        "truncated_mps": [row["command_mps"] for row in rows if row["truncated"]],
        "v_work_min_mps": min(averages),
        "v_work_max_mps": max(averages),
        "r_d_m": radii.pop(),
        "arm_length_m": lengths.pop(),
        "omega_deg_s": rates.pop(),
        "rows": rows,
    }


def both_panels() -> dict[str, dict]:
    return {name: truncation(name) for name in PANELS}
