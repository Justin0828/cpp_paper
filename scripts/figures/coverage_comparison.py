"""BiRect and Fields2Cover coverage on simple and complex.

BiRect's full-trajectory mask is rebuilt from the frozen config and seed.
The printed ratios are the saved metrics, and the rebuild must match them.
"""

from __future__ import annotations

import json
import math
import os
import random
import sys
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Polygon as MplPolygon
from matplotlib.path import Path as MplPath
import numpy as np

from style_loader import inches, load, stroke
from tikzfig import FIGURES

CPP = Path("/home/panyz/workspace/Tsinghua/cpp_paper/Coverage_Path_Planning")
PPC = CPP / "pathCoverage_experiment"
F2C = CPP / "Fields2Cover" / "experiments"
sys.path.insert(0, str(PPC))

from src.configuration import load_experiment_config  # noqa: E402
from src.main_pipeline import (  # noqa: E402
    build_traversal_order,
    compute_coverage_metrics,
    create_robot,
    generate_pipeline_poses,
    segment_map_into_rectangles,
)


OURS = {
    "simple": {
        "config": PPC / "experiments/fields2cover_comparison/configs/experiment_map_test1.json",
        "metrics": PPC / "experiments/fields2cover_comparison/results/map_test1/metrics.json",
    },
    "complex": {
        "config": PPC / "experiments/fields2cover_comparison/configs/experiment_parkingGraph.json",
        "metrics": PPC / "experiments/fields2cover_comparison/results/parkingGraph/metrics.json",
    },
}
BASELINE = {
    "simple": {
        "geojson": F2C / "maps/test1.geojson",
        "path": F2C / "results/robot_baseline_test1_tool1p5_cruise2_turn0p5/path.csv",
        "metrics": F2C / "results/robot_baseline_test1_tool1p5_cruise2_turn0p5/metrics.json",
    },
    "complex": {
        "geojson": F2C / "maps/parkingGraph.geojson",
        "path": F2C / "results/robot_baseline_parkingGraph_tool1p5_cruise2_turn0p5/path.csv",
        "metrics": F2C / "results/robot_baseline_parkingGraph_tool1p5_cruise2_turn0p5/metrics.json",
    },
}


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def rebuild_birect(panel: str) -> dict:
    """Return the saved full-trajectory mask. Abort if the rebuild drifts."""
    spec = OURS[panel]
    config = load_experiment_config(spec["config"])
    random.seed(config.random_seed)
    np.random.seed(config.random_seed)
    robot = create_robot(config.robot, config.work_speed_policy)
    raw_map, _segmentation, rectangles, stats = segment_map_into_rectangles(config)
    _graph, order, _start = build_traversal_order(
        rectangles,
        config,
        fixed_start_rect=stats["start_rectangle_before_connectivity"],
    )
    segments: list = []
    poses, _ = generate_pipeline_poses(
        rectangles,
        order,
        robot,
        config.sample_rate,
        motion_segments=segments,
    )
    metrics = compute_coverage_metrics(
        poses,
        raw_map,
        robot,
        config.pixel_size,
        motion_segments=segments,
        rect_list=rectangles,
        order=order,
    )
    saved = read_json(spec["metrics"])
    saved_ratio = float(saved["coverage"]["full_trajectory_disc"]["coverage_ratio"])
    saved_px = int(saved["coverage"]["full_trajectory_disc"]["covered_free_px"])
    got_ratio = float(metrics["trajectory_coverage_ratio"])
    got_px = int(metrics["trajectory_covered_free_px"])
    if got_px != saved_px or abs(got_ratio - saved_ratio) > 1e-12:
        raise SystemExit(
            f"{panel} rebuild {got_ratio} ({got_px} px) != saved {saved_ratio} ({saved_px} px)"
        )
    return {
        "panel": panel,
        "raw_map": raw_map,
        "covered": metrics["trajectory_covered_map"] & (raw_map == 255),
        "pixel_size": float(config.pixel_size),
        "coverage_ratio": saved_ratio,
        "invalid_area_m2": None,
    }


def load_geojson(path: Path) -> tuple[np.ndarray, list[np.ndarray]]:
    rings = read_json(path)["features"][0]["geometry"]["coordinates"]
    outer = np.array([[point[0], point[1]] for point in rings[0]], dtype=float)
    holes = [
        np.array([[point[0], point[1]] for point in ring], dtype=float)
        for ring in rings[1:]
    ]
    return outer, holes


def load_path(path: Path) -> np.ndarray:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            parts = line.split()
            if len(parts) >= 2:
                rows.append([float(parts[0]), float(parts[1])])
    return np.asarray(rows, dtype=float)


def field_mask(outer: np.ndarray, holes: list[np.ndarray], xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
    points = np.column_stack([xs.ravel(), ys.ravel()])
    inside = MplPath(outer[:, :2]).contains_points(points)
    for hole in holes:
        inside &= ~MplPath(hole[:, :2]).contains_points(points)
    return inside.reshape(xs.shape)


def simplify(points: np.ndarray, tolerance: float) -> np.ndarray:
    if len(points) <= 2:
        return points
    keep = np.zeros(len(points), dtype=bool)
    keep[0] = True
    keep[-1] = True
    stack = [(0, len(points) - 1)]
    limit = tolerance * tolerance
    while stack:
        start_i, end_i = stack.pop()
        if end_i <= start_i + 1:
            continue
        start = points[start_i]
        end = points[end_i]
        segment = end - start
        length_sq = float(np.dot(segment, segment))
        middle = points[start_i + 1 : end_i]
        if length_sq <= 1e-12:
            dist_sq = np.sum((middle - start) ** 2, axis=1)
        else:
            scale = np.clip(((middle - start) @ segment) / length_sq, 0.0, 1.0)
            projection = start + scale[:, None] * segment
            dist_sq = np.sum((middle - projection) ** 2, axis=1)
        local = int(np.argmax(dist_sq))
        if dist_sq[local] > limit:
            split = start_i + 1 + local
            keep[split] = True
            stack.append((start_i, split))
            stack.append((split, end_i))
    return points[keep]


def outside_runs(points: np.ndarray, outer: np.ndarray, holes: list[np.ndarray]) -> tuple[list, list]:
    inside = MplPath(outer[:, :2]).contains_points(points)
    for hole in holes:
        inside &= ~MplPath(hole[:, :2]).contains_points(points)
    inside_runs: list[np.ndarray] = []
    outside_runs_list: list[np.ndarray] = []
    current: list[np.ndarray] = []
    current_inside = bool(inside[0])
    current.append(points[0])
    for point, flag in zip(points[1:], inside[1:]):
        flag = bool(flag)
        if flag == current_inside:
            current.append(point)
            continue
        current.append(point)
        run = np.asarray(current)
        (inside_runs if current_inside else outside_runs_list).append(run)
        current = [point]
        current_inside = flag
    if len(current) >= 2:
        run = np.asarray(current)
        (inside_runs if current_inside else outside_runs_list).append(run)
    return inside_runs, outside_runs_list


def sweep_mask(outer, holes, path: np.ndarray, radius: float, resolution: float):
    xmax = float(np.max(outer[:, 0]))
    ymax = float(np.max(outer[:, 1]))
    xs = np.arange(resolution / 2.0, xmax, resolution)
    ys = np.arange(resolution / 2.0, ymax, resolution)
    grid_x, grid_y = np.meshgrid(xs, ys)
    free = field_mask(outer, holes, grid_x, grid_y)
    covered = np.zeros(grid_x.shape, dtype=bool)
    radius_sq = radius * radius
    simple = simplify(path, 0.08)
    cell = float(xs[1] - xs[0]) if len(xs) > 1 else resolution
    for start, end in zip(simple[:-1], simple[1:]):
        xmin = min(start[0], end[0]) - radius
        xmax_seg = max(start[0], end[0]) + radius
        ymin = min(start[1], end[1]) - radius
        ymax_seg = max(start[1], end[1]) + radius
        ix0 = max(0, int(math.floor(xmin / cell)))
        ix1 = min(grid_x.shape[1], int(math.ceil(xmax_seg / cell)) + 1)
        iy0 = max(0, int(math.floor(ymin / cell)))
        iy1 = min(grid_x.shape[0], int(math.ceil(ymax_seg / cell)) + 1)
        if ix0 >= ix1 or iy0 >= iy1:
            continue
        sub_x = grid_x[iy0:iy1, ix0:ix1]
        sub_y = grid_y[iy0:iy1, ix0:ix1]
        vx, vy = end - start
        length_sq = float(vx * vx + vy * vy)
        if length_sq <= 1e-12:
            dist_sq = (sub_x - start[0]) ** 2 + (sub_y - start[1]) ** 2
        else:
            scale = ((sub_x - start[0]) * vx + (sub_y - start[1]) * vy) / length_sq
            scale = np.clip(scale, 0.0, 1.0)
            dist_sq = (sub_x - (start[0] + scale * vx)) ** 2 + (sub_y - (start[1] + scale * vy)) ** 2
        covered[iy0:iy1, ix0:ix1] |= dist_sq <= radius_sq
    return free, covered & free, (0.0, xmax, 0.0, ymax)


def load_fields2cover(panel: str) -> dict:
    spec = BASELINE[panel]
    metrics = read_json(spec["metrics"])
    outer, holes = load_geojson(spec["geojson"])
    path = load_path(spec["path"])
    radius = float(metrics["robot"]["coverage_width_m"]) / 2.0
    free, covered, extent = sweep_mask(outer, holes, path, radius, 0.15)
    return {
        "panel": panel,
        "outer": outer,
        "holes": holes,
        "path": path,
        "free": free,
        "covered": covered,
        "extent": extent,
        "coverage_ratio": float(metrics["coverage_ratio"]),
        "invalid_area_m2": float(metrics["path_validation"]["swept_area_outside_field_m2"]),
    }


def _rgb(hex_color: str) -> np.ndarray:
    return np.array(plt.matplotlib.colors.to_rgb(hex_color))


def paint_birect(data: dict, colors: dict[str, str]) -> tuple[np.ndarray, tuple]:
    raw = data["raw_map"]
    free = raw == 255
    image = np.empty((*raw.shape, 4), dtype=float)
    image[..., :3] = _rgb(colors["secondaryfill"])
    image[..., 3] = 1.0
    image[data["covered"], :3] = _rgb(colors["discfill"])
    image[~free, :3] = _rgb(colors["ink"])
    pixel = data["pixel_size"]
    extent = (0.0, raw.shape[1] * pixel, 0.0, raw.shape[0] * pixel)
    return image, extent


def paint_sweep(free: np.ndarray, covered: np.ndarray, colors: dict[str, str]) -> np.ndarray:
    image = np.zeros((*free.shape, 4), dtype=float)
    image[free, :3] = _rgb(colors["secondaryfill"])
    image[free, 3] = 1.0
    image[covered, :3] = _rgb(colors["discfill"])
    image[covered, 3] = 1.0
    return image


def style_map(ax, colors: dict[str, str], aux: float) -> None:
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.tick_params(length=2.2, width=aux)
    for spine in ax.spines.values():
        spine.set_color(colors["ink"])
        spine.set_linewidth(aux)


def draw_birect(ax, data: dict, colors: dict[str, str], aux: float) -> None:
    image, extent = paint_birect(data, colors)
    ax.imshow(image, extent=extent, origin="lower", interpolation="nearest", zorder=1)
    style_map(ax, colors, aux)


def draw_fields(ax, data: dict, colors: dict[str, str], main: float, aux: float) -> None:
    ax.add_patch(
        MplPolygon(
            data["outer"][:, :2],
            closed=True,
            facecolor=colors["secondaryfill"],
            edgecolor=colors["path"],
            linewidth=main,
            zorder=0,
        )
    )
    image = paint_sweep(data["free"], data["covered"], colors)
    ax.imshow(image, extent=data["extent"], origin="lower", interpolation="nearest", zorder=1)
    for hole in data["holes"]:
        ax.add_patch(
            MplPolygon(
                hole[:, :2],
                closed=True,
                facecolor=colors["ink"],
                edgecolor=colors["ink"],
                linewidth=aux,
                zorder=3,
            )
        )
    inside, outside = outside_runs(data["path"], data["outer"], data["holes"])
    for run in inside:
        ax.plot(run[:, 0], run[:, 1], color=colors["path"], linewidth=main, solid_capstyle="butt", zorder=4)
    for run in outside:
        ax.plot(run[:, 0], run[:, 1], color=colors["emphasis"], linewidth=main, solid_capstyle="butt", zorder=5)
    style_map(ax, colors, aux)
    ax.set_xlim(data["extent"][0], data["extent"][1])
    ax.set_ylim(data["extent"][2], data["extent"][3])


def caption_lines(data: dict, name: str, method: str, tag: str) -> tuple[str, str]:
    title = f"({tag}) {name}, {method}"
    ratio = f"{data['coverage_ratio'] * 100:.2f}%"
    if data["invalid_area_m2"] is None:
        return title, ratio
    area = f"{data['invalid_area_m2']:.2f}"
    return title, f"{ratio}, {area} m$^2$ outside"


def main() -> None:
    colors = load()
    main_stroke = stroke("main")
    aux = stroke("aux")
    panels = {
        ("simple", "BiRect"): rebuild_birect("simple"),
        ("complex", "BiRect"): rebuild_birect("complex"),
        ("simple", "Fields2Cover"): load_fields2cover("simple"),
        ("complex", "Fields2Cover"): load_fields2cover("complex"),
    }
    for (name, method), data in panels.items():
        invalid = data["invalid_area_m2"]
        print(
            "DATA coverage"
            f" map={name}"
            f" method={method}"
            f" coverage_ratio={data['coverage_ratio']:.12g}"
            f" invalid_m2={'' if invalid is None else f'{invalid:.12g}'}"
        )

    width = inches(colors, "__full_in")
    fig, axes = plt.subplots(2, 2, figsize=(width, 7.05))
    order = [
        (axes[0, 0], "simple", "BiRect", "a"),
        (axes[0, 1], "simple", "Fields2Cover", "b"),
        (axes[1, 0], "complex", "BiRect", "c"),
        (axes[1, 1], "complex", "Fields2Cover", "d"),
    ]
    for ax, name, method, tag in order:
        data = panels[(name, method)]
        if method == "BiRect":
            draw_birect(ax, data, colors, aux)
        else:
            draw_fields(ax, data, colors, main_stroke, aux)
        title, detail = caption_lines(data, name, method, tag)
        ax.set_title("")
        ax._panel_tag = (title, detail)  # noqa: SLF001

    fig.subplots_adjust(left=0.08, right=0.985, bottom=0.09, top=0.90, wspace=0.32, hspace=0.72)
    for ax, *_rest in order:
        title, detail = ax._panel_tag
        box = ax.get_position()
        fig.text(
            box.x0 + box.width / 2,
            box.y0 - 0.058,
            title + "\n" + detail,
            ha="center",
            va="top",
            fontsize=8,
            linespacing=1.2,
            color=colors["ink"],
        )
    fig.legend(
        handles=[
            Patch(facecolor=colors["secondaryfill"], edgecolor=colors["ink"], linewidth=aux, label="Uncovered"),
            Patch(facecolor=colors["discfill"], edgecolor="none", label="Sweep"),
            Patch(facecolor=colors["ink"], edgecolor="none", label="Obstacle"),
            Line2D([0], [0], color=colors["path"], linewidth=main_stroke, label="Centerline"),
            Line2D([0], [0], color=colors["emphasis"], linewidth=main_stroke, label="Invalid"),
        ],
        loc="upper center",
        ncol=5,
        bbox_to_anchor=(0.5, 0.988),
        handlelength=1.4,
        columnspacing=1.0,
    )
    dest = FIGURES / "figure_2_coverage_comparison_en.pdf"
    fig.savefig(dest)
    plt.close(fig)
    print(dest)


if __name__ == "__main__":
    main()
