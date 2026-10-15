"""Recorded work speed of the saved vehicle-speed runs.

Eq. (16) is v_safe = 2 r_d / T_half and Eq. (17) is v_work = min(v_max, v_safe).
The result directory stores the work-speed policy and the executed work speed.
It does not store per-strip arm spans, so v_safe is not recomputed here.
Under the commanded policy the controller sets the work speed to the command
and does not apply the v_safe cap.
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


def _load_json(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _near(left: float, right: float) -> bool:
    return abs(left - right) <= _SPEED_TOL


def _recorded_mps(trajectory: dict, command: float) -> float:
    duration = float(trajectory["work_duration_seconds"])
    if duration <= 0:
        raise ValueError("work duration is not positive")
    from_path = float(trajectory["work_distance_m"]) / duration
    average = float(trajectory["actual_average_work_speed_mps"])
    maximum = float(trajectory["actual_max_work_speed_mps"])
    if not (
        _near(from_path, command)
        and _near(average, command)
        and _near(maximum, command)
    ):
        raise ValueError(
            "recorded work speed is not the command "
            f"{command}: distance/duration={from_path}, "
            f"average={average}, max={maximum}"
        )
    return from_path


def recorded_runs(panel: str) -> dict:
    """Return the saved policy and the executed work-speed range.

    ``applies_v_safe`` is true only for the coverage_safe policy. These
    artifacts have no per-strip arm span, so a coverage_safe run cannot be
    turned into an Eq. (16) cap here. The commanded policy does not apply
    that cap; the recorded speed is then the command.
    """
    rows = []
    radii = set()
    lengths = set()
    rates = set()
    for speed in COMMANDED:
        directory = PANELS[panel] / _directory(speed)
        report = _load_json(directory / "metrics.json")
        snapshot = _load_json(directory / "config_snapshot.json")
        trajectory = report["trajectory"]
        geometry = report["coverage"]["geometry"]
        command = float(trajectory["configured_speed_limit_mps"])
        if abs(command - speed) > _SPEED_TOL:
            raise ValueError(f"{panel} {speed}: metrics command is {command}")
        if abs(float(snapshot["robot"]["speed_limit"]) - command) > _SPEED_TOL:
            raise ValueError(f"{panel} {speed}: snapshot speed differs from the metrics")
        policy = trajectory["work_speed_policy"]
        if snapshot["work_speed_policy"] != policy:
            raise ValueError(f"{panel} {speed}: snapshot policy differs from the metrics")
        recorded = _recorded_mps(trajectory, command)
        rows.append(
            {
                "command_mps": command,
                "recorded_mps": recorded,
                "policy": policy,
            }
        )
        radii.add(float(geometry["disc_radius_m"]))
        lengths.add(float(geometry["arm_length_m"]))
        rates.add(float(trajectory["arm_angular_velocity_limit_deg_s"]))
    policies = {row["policy"] for row in rows}
    if policies != {"commanded"} and policies != {"coverage_safe"}:
        raise ValueError(f"{panel}: mixed work-speed policies {sorted(policies)}")
    if len(radii) != 1 or len(lengths) != 1 or len(rates) != 1:
        raise ValueError(f"{panel}: r_d, L, or arm rate is not fixed across the six runs")
    policy = rows[0]["policy"]
    applies_v_safe = policy == "coverage_safe"
    if applies_v_safe:
        raise ValueError(
            f"{panel}: coverage_safe runs need stored arm spans to evaluate "
            "Eq. (16); the saved results do not include them"
        )
    recorded = [row["recorded_mps"] for row in rows]
    return {
        "panel": panel,
        "policy": policy,
        "applies_v_safe": applies_v_safe,
        "recorded_equals_command": all(
            _near(row["recorded_mps"], row["command_mps"]) for row in rows
        ),
        "commands_mps": [row["command_mps"] for row in rows],
        "recorded_mps": recorded,
        "v_work_min_mps": min(recorded),
        "v_work_max_mps": max(recorded),
        "r_d_m": radii.pop(),
        "arm_length_m": lengths.pop(),
        "omega_deg_s": rates.pop(),
        "rows": rows,
    }


def both_panels() -> dict[str, dict]:
    return {name: recorded_runs(name) for name in PANELS}
