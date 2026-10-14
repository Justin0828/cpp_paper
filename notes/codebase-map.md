# Coverage codebase map

Read-only survey of `/home/panyz/workspace/Tsinghua/cpp_paper/Coverage_Path_Planning` and of the figures `english_paper/` actually includes. This note does not change any `.tex`. The Coverage tree is not part of the `rev/B` worktree.

Host used for the survey: Linux, `/home/panyz/miniconda3/bin/python` (3.13). The checked-in `pathCoverage_experiment/.venv` is a macOS arm64 virtualenv and does not run here (see Bugs).

## Fields2Cover

What it does. Upstream Fields2Cover 2.1.0 (C++17), a coverage planner for agricultural vehicles: headlands, swaths, route order, and Dubins connections on non-convex fields with obstacles. This checkout adds a paper experiment layer under `Fields2Cover/experiments/` that plans a fixed-width implement over the same two maps as the proposed method and records coverage, path length, time, and a base-collision check.

Entry.

- Library: `Fields2Cover/CMakeLists.txt` (`BUILD_PYTHON` uses SWIG).
- Paper runs: `Fields2Cover/experiments/run_experiment.py`.
- Metric-only refresh of an existing path: `experiments/backfill_full_trajectory_coverage.py`.
- Robot profile check: `python3 experiments/robot_config.py robot_baseline` from `Fields2Cover/`.

Dependencies. CMake ≥ 3.12, TinyXML2, Threads, GDAL ≥ 3.0, Eigen3, optional Gnuplot (plots), SWIG ≥ 4 and Python (bindings). Experiment scripts import the built module `fields2cover` plus the local helpers `path_validation.py`, `robot_config.py`, and `trajectory_coverage.py`.

Inputs.

- `experiments/maps/*.geojson` (metric polygons; interior rings are obstacles). The comparison uses `test1.geojson` and `parkingGraph.geojson`.
- `experiments/configs/robots.json`, `experiments/configs/planners.json`.

Outputs, per run name under `experiments/results/<run-name>/`.

- `metrics.json` (full-path fixed-tool coverage, swath-only coverage, lengths, times, path validation).
- `path.csv` (serialized states), `route.png`, `path.png`.

The runs that feed the paper figure are:

- `experiments/results/robot_baseline_test1_tool1p5_cruise2_turn0p5/`
- `experiments/results/robot_baseline_parkingGraph_tool1p5_cruise2_turn0p5/`

Command shape (does not redraw a cited figure by itself):

```bash
cd /home/panyz/workspace/Tsinghua/cpp_paper/Coverage_Path_Planning/Fields2Cover
python3 experiments/run_experiment.py \
  --robot robot_baseline \
  --map test1.geojson \
  --run-name robot_baseline_test1
```

## pathCoverage_experiment

What it does. The proposed swing-arm planner and the frozen experiment runner: binary-map rectangle segmentation, connectivity completion, traversal order, local base–arm coverage, and disc-sweep metrics.

Entry. `src/main_pipeline.py`.

```bash
cd /home/panyz/workspace/Tsinghua/cpp_paper/Coverage_Path_Planning/pathCoverage_experiment
python -m src.main_pipeline --config experiments/fields2cover_comparison/configs/experiment_map_test1.json
```

Dependencies. `requirements.txt`: numpy ≥ 1.24, pillow ≥ 10, matplotlib ≥ 3.7, pandas ≥ 3, seaborn ≥ 0.13, imageio, imageio-ffmpeg. Python ≥ 3.10. Algorithm code lives in `algorithms/` (`build_graph.py`, `rectangle_coverage.py`, `segmentation.py`, `segmentation_methods/`, `connectivity_methods/`). Config loading is `src/configuration.py`. Plots and the coverage video are `src/visualization.py`.

Inputs. One experiment JSON. Paths inside it are relative to the repository root. Shared robot baseline: `experiments/configs/robot_config_default.json`. Maps are PNG occupancy images (white 255 free, black 0 obstacle) with `pixel_size` in metres.

Outputs of one pipeline run: `metrics.json`, `segmentation.png`, `traversal_order.png`, `coverage.mp4`, `coverage_final.png`, `config_snapshot.json`.

Four experiment drivers, each with its own `configs/`, `maps/`, and `results/`:

| Driver | Command | What it writes |
| --- | --- | --- |
| Fields2Cover comparison | `python -m src.main_pipeline --config experiments/fields2cover_comparison/configs/experiment_<map>.json` | `experiments/fields2cover_comparison/results/<map>/` |
| Scan-order ablation | `python experiments/segmentation_order_comparison/run_comparison.py` | `results/<map>/<strategy>/` and `comparison_summary.json` |
| Connectivity ablation | `python experiments/connectivity_repair_ablation/run_ablation.py` | paired with/without bridge repair |
| Vehicle speed | `python experiments/vehicle_speed_comparison/run_comparison.py` | per-speed metrics plus `comparison_summary.csv` and the speed curves |

`run_comparison.py` for vehicle speed calls `plot_results.plot_comparison` on the CSV it just wrote. Replotting from an existing CSV does not rerun the planner:

```bash
cd /home/panyz/workspace/Tsinghua/cpp_paper/Coverage_Path_Planning/pathCoverage_experiment
python -c "
from pathlib import Path
from experiments.vehicle_speed_comparison.plot_results import plot_comparison
root = Path('experiments/vehicle_speed_comparison/results')
plot_comparison(root/'map_test1'/'comparison_summary.csv', root/'map_test1')
plot_comparison(root/'parkingGraph'/'comparison_summary.csv', root/'parkingGraph')
"
```

That command is the one that produces the cited speed PNGs. See the figure table.

## polygon_coverage_planning

What it does. ETH Zurich polygon coverage (Bähnemann et al.): Boustrophedon or trapezoidal cells on a polygon with holes, sweep candidates, and a GTSP plus visibility-graph transfer. It is the related-work method named Polygon CPP. It does not generate any file that `english_paper/` includes.

Entry.

- ROS: `roslaunch polygon_coverage_ros coverage_planner.launch`, then `scripts/run_coverage_service_client.py`.
- Headless Docker wrapper: `docker/run_headless_experiment.sh` (sources ROS Noetic and a catkin workspace, writes `experiment_results/<timestamp>/`).

Dependencies. Ubuntu ROS Noetic, mono, CGAL (GPL pieces), the Gutin–Karapetyan GTSP solver. Packages: `polygon_coverage_msgs`, `polygon_coverage_geometry`, `polygon_coverage_solvers`, `polygon_coverage_planners`, `polygon_coverage_ros`, `polygon_coverage_benchmark`, `rviz_polygon_tool`.

Inputs. A polygon with holes via the ROS service, the launch parameter, or RViz. The headless script takes start and goal coordinates.

Outputs. A `geometry_msgs/PoseArray` on `/waypoint_list`, plus whatever the client writes under `experiment_results/`. Those results are not copied into the paper figures.

## Top-level figure and SVG generators

Python dependencies for the `figures/` scripts are the tree-level `requirements.txt`: numpy, pandas, matplotlib, seaborn, scipy, jupyter, ipykernel, openpyxl. Each script sets `MPLBACKEND` to Agg and writes next to itself under `figures/`.

| Script or source | Command | Output | Cited by English tex? |
| --- | --- | --- | --- |
| `figures/generate_figure_1.py` | `python figures/generate_figure_1.py` | `figures/figure_1{a–e}_*_binary_cn.{png,svg,pdf}` from the five segmentation maps | No. Binary-map posters, Chinese labels. |
| `figures/generate_figure_2.py` | `python figures/generate_figure_2.py` | `figures/figure_2_coverage_comparison_cn.{png,pdf}` | The Chinese PNG matches `paper-B/figures/`. The English cited PNG is a separate file; see the table. |
| `figures/generate_figure_3.py` | `python figures/generate_figure_3.py` | `figures/figure_3_segmentation_order_cn.{png,svg,pdf}` | Chinese only. The English cited pair is the saved SVG plus its 220 dpi PNG. |
| `figures/generate_exact_to_raster_conversion.py` | `python figures/generate_exact_to_raster_conversion.py` | `figures/exact_to_raster_conversion_scenarios_cn.{png,svg,pdf}` | No. Different layout (six stacked rows, Chinese titles, decomposition rectangles). The cited raster is `transfer.svg`. |
| `figures/generate_troweling_robot_layout_taxonomy.py` | `python figures/generate_troweling_robot_layout_taxonomy.py` | `figures/troweling_disc_vehicle_layout_taxonomy_cn.{png,svg,pdf}` | No. A schematic taxonomy, not the photo-based disc figure. |
| `figures/create_improved_coverage_ppt.py` | expects a macOS pptx path | `figures/ppt_outputs/coveragePath_improved.pptx` and a preview PNG | No. |
| `compose_robot_figure.mjs` | `node compose_robot_figure.mjs` | overwrites `robot_disk_relationships.svg` from three SVGs in `/Users/justin/Desktop` | The cited figure is the later hand-edited SVG, not this script’s captions. |
| `pipeline_overall_improved_en.svg` | hand-written SVG, viewBox `0 0 1400 760`, page size 140 mm × 76 mm | `pipeline_overall_improved_en.png` is 1400×760 | Yes. Workflow figure. |
| `pipeline_overall_improved.svg` | Chinese counterpart of the workflow | not the English include | No. |
| `robot_disk_relationships.svg` (Coverage tree) | older captions: “Disk separated / centered / overlapping” | not the cited PNG | The cited file matches `paper-B/assets/svg_sources/robot_disk_relationships.svg`. |
| `rect_coverage_recolored.svg` (1660×1416) | artwork related to rectangle coverage | not size-matched to the cited PNG | No direct include. |
| `figures/swing_arm_troweling_robot_photo_shobserver.jpg` | photograph | copied byte-for-byte to the cited photo | Yes, as the photo figure. |

## Cited English figures

`english_paper/main.tex` sets `\graphicspath{{figures/}}`. Every `\includegraphics` below is under `english_paper/figures/`. Hashes were compared to the Coverage tree and to `paper-B/figures/` (the Chinese draft’s copies).

| Tex file | What the paper calls it | Script, data, command | Output path |
| --- | --- | --- | --- |
| `figure_1_swing_arm_troweling_robot_photo.jpg` | On-site swing-arm robot (`introduction.tex`) | No script. Byte-identical to `Coverage_Path_Planning/figures/swing_arm_troweling_robot_photo_shobserver.jpg`. | `english_paper/figures/figure_1_swing_arm_troweling_robot_photo.jpg` |
| `figure_2_disc_vehicle_relationships.png` | Three disc–base arrangements (`introduction.tex`) | Source SVG: `paper-B/assets/svg_sources/robot_disk_relationships.svg` (viewBox 1400×500, page 140 mm × 50 mm). Captions: “(a) Underbody or center-mounted disk”, “(b) Front-mounted disk”, “(c) Swing-arm-mounted disk”. PNG is 3307×1181, which is that page size at 600 dpi (`140/25.4*600`). No checked-in command; the SVG is the source. `compose_robot_figure.mjs` is an older assembler and is not this file. | `english_paper/figures/figure_2_disc_vehicle_relationships.png` |
| `pipeline_overall_improved_en.png` | Workflow (`methodology.tex`, advisor Figure 3) | Source SVG: `paper-B/assets/svg_sources/pipeline_overall_improved_en.svg`, identical to `Coverage_Path_Planning/pipeline_overall_improved_en.svg`. PNG is 1400×760, one pixel per viewBox unit, and is byte-identical to the Coverage-tree PNG. Stage 4 header text is `4. Global Routing &` / `Rectangle Coverage`. | `english_paper/figures/pipeline_overall_improved_en.png` |
| `figure_3_geometric_to_binary_raster.png` | Exact geometry to binary raster (`methodology.tex`, advisor Figure 4) | Source SVG: `paper-B/assets/svg_sources/transfer.svg` (530×280). Same panel titles as the PNG, including “(d) L-Shaped Region with Multiple Obstacles”. PNG is 2400×1268. `generate_exact_to_raster_conversion.py` draws a different Chinese figure and is not this file. | `english_paper/figures/figure_3_geometric_to_binary_raster.png` |
| `figure_4_body_arm_disc_model.png` | Base–arm–disc geometry (`methodology.tex`, advisor Figure 5) | No generator script in the Coverage tree. Raster only, 2400×1400, labels \(r_d\), \(L\), \(\phi\), \(d_p\), \(\theta\), \(l_c\), \(w_c\), “disk”, “robot base”, “Heading”. `robot_main.svg` is a different aspect ratio and is not this raster. | `english_paper/figures/figure_4_body_arm_disc_model.png` |
| `figure_6_single_rectangle_coverage.png` | Single-rectangle primitive (`methodology.tex`, advisor Figure 6) | No generator script. Raster only, 2400×2400. `rect_coverage_recolored.svg` is related artwork at 1660×1416 and is not this file. | `english_paper/figures/figure_6_single_rectangle_coverage.png` |
| `figure_2_coverage_comparison_en.png` | Proposed vs Fields2Cover (`experiments.tex`) | `figures/generate_figure_2.py`. Proposed panels recompute the sweep from `pathCoverage_experiment` configs `experiments/fields2cover_comparison/configs/experiment_{map_test1,parkingGraph}.json` and print the ratio stored in `results/<map>/metrics.json`. Fields2Cover panels read `Fields2Cover/experiments/maps/{test1,parkingGraph}.geojson`, `results/robot_baseline_*_tool1p5_cruise2_turn0p5/path.csv`, and the matching `metrics.json`. The script as it stands writes Chinese labels to `figures/figure_2_coverage_comparison_cn.png` (byte-identical to `paper-B/figures/figure_2_coverage_comparison_cn.png`). The cited English PNG (1337×1176) has the same four-panel geometry with English titles `(a) map_simple, proposed`, `(b) map_simple, Fields2Cover`, `(c) parkingGraph, proposed`, `(d) parkingGraph, Fields2Cover` and an English legend. No separate English script is in the tree. | `english_paper/figures/figure_2_coverage_comparison_en.png` |
| `figure_3_segmentation_order_en.png` | Scan strategies on `scan_mixed_weave` (`experiments.tex`) | Data images: `pathCoverage_experiment/experiments/segmentation_order_comparison/maps/scan_mixed_weave.png` and `results/scan_mixed_weave/{row_only,col_only,row_then_col}/segmentation.png`. `figures/generate_figure_3.py` composites them. The current script writes Chinese titles to `figure_3_segmentation_order_cn.*`. The cited English figure is the matplotlib SVG `paper-B/assets/svg_sources/figure_3_segmentation_order_en.svg` (viewBox 924.0768 pt × 217.427 pt, byte-identical to the Coverage-tree SVG) and its PNG. PNG size 2823×664 equals that viewBox at 220 dpi, the dpi in `generate_figure_3.py`. English strings: “(a) Original Map” through “(d) Row-Then-Column Scan”, plus the overlap and trajectory-coverage notes. | `english_paper/figures/figure_3_segmentation_order_en.png` |
| `figure_5a_vehicle_speed_map_simple_en.png` | Speed study, simple map (`experiments.tex`, advisor Figure 7a) | `pathCoverage_experiment/experiments/vehicle_speed_comparison/plot_results.py` function `plot_comparison`. Data: `results/map_test1/comparison_summary.csv` only (`configured_speed_mps`, `arm_angular_velocity_deg_s`, `full_trajectory_disc_coverage_ratio`, `duration_seconds`). The directory name `map_test1` is relabeled `map_simple` in the plot title. Figure size 7.1×4.4 in at 600 dpi gives 4260×2640. The PNG is byte-identical to `results/map_test1/speed_ratio_curve.png` and to `Coverage_Path_Planning/figures/figure_5a_vehicle_speed_map_simple_en.png`. The PDF twin is `assets/pdf_sources/figure_5a_vehicle_speed_map_simple_en.pdf`, byte-identical to `speed_ratio_curve.pdf`. Replot command is the `plot_comparison` snippet above. `run_comparison.py` also calls it, but that reruns the planner. | `english_paper/figures/figure_5a_vehicle_speed_map_simple_en.png` |
| `figure_5b_vehicle_speed_parkingGraph_en.png` | Speed study, parking map (`experiments.tex`, advisor Figure 7b) | Same script and function. Data: `results/parkingGraph/comparison_summary.csv`. Title stays `parkingGraph` (`display_names` only renames `map_test1`). PNG byte-identical to `results/parkingGraph/speed_ratio_curve.png`. | `english_paper/figures/figure_5b_vehicle_speed_parkingGraph_en.png` |

Class-B items and the files they touch:

- 25. New quadrant sketch. No existing script. Not an experimental map. Insert after the four class names in `introduction.tex`.
- 38. Workflow SVG text `4. Global Routing &` becomes `global route planning`. Same module boxes. Output remains `pipeline_overall_improved_en.png`.
- 48 and 49. `transfer.svg` / `figure_3_geometric_to_binary_raster.png`. Move in-image titles under each panel. Check the lower-right black cells of panel (d) against the left-hand geometry.
- 63. Two new principle figures at the start of subsections 3.5.2 and 3.5.3. Symbols already in `methodology.tex`: \(d_p\), \(L\), \(\ell_R\), \(h_R\), \(w_s\), \(N_s\), \(\phi_w\), \(r_d\), \(v_{\mathrm{work}}\), \(T_{\mathrm{half}}\).
- 67. One new schematic in subsection 3.7, after the work versus non-work paragraph and before the coverage-ratio formulas. Symbols \(\mathcal C_{\mathrm{work}}\) and \(\mathcal C_{\mathrm{traj}}\) already in that subsection.
- 70. In-image names `map_simple` and `parkingGraph` on the coverage comparison and the two speed plots. `scan_comb_corridors`, `scan_mixed_weave`, and `scan_offset_rooms` stay. CSV and JSON filenames stay.
- 81. Redraw the two speed plots from `comparison_summary.csv` (the same numbers as Table `tab:speed-study`). \(\rho\) axis starts at 0. No sample is added at \(\rho=0\). No strip-coverage series.

## Reproduction

One cited figure was regenerated before any class-B edit. The figure is `english_paper/figures/figure_5a_vehicle_speed_map_simple_en.png` (advisor Figure 7a, English PDF page 26).

Command, from `pathCoverage_experiment`, using the Linux interpreter because the checked-in venv is macOS-only:

```bash
python -c "
from pathlib import Path
from experiments.vehicle_speed_comparison.plot_results import plot_comparison
root = Path('experiments/vehicle_speed_comparison/results')
plot_comparison(root/'map_test1'/'comparison_summary.csv', root/'map_test1')
"
```

The run for the comparison wrote to a scratch directory so the cited PNG was not overwritten. Data file: `experiments/vehicle_speed_comparison/results/map_test1/comparison_summary.csv`. Both images are 4260×2640. They are not byte-identical: matplotlib warns that Times New Roman is missing and falls back to DejaVu Sans. The pixel difference is the glyph outlines (title `map_simple`, legend, tick labels, axis title, and the `1.0 m/s` tag). The curves, markers, grid, axis limits, and panel layout match. `pdfimages` on `english_paper/output/pdf/cpp_paper_english.pdf` page 26 extracts a 4260×2640 RGB image that is pixel-identical to the cited PNG (0 changed pixels). The reproduction is accepted as font drift, not a content mismatch.

## Figure 4(d) black cluster

Checked before any redraw. Source geometry is in `assets/svg_sources/transfer.svg`. The L region is the path `M15 157 H38 V183 H68 V213 H15 V157 Z`. Obstacles inside it are a disc centered at (26, 169) with radius 5.5, and three rectangles `(22,195)-(32,204)`, `(48,191)-(54,197)`, and `(54,199)-(62,207)`. The right-hand raster is an 15×16 block of 4 px cells whose white cells start at SVG (100, 153). A rigid map from those cells onto the L (best fit about 223 of 240 cells, origin near (15, 157), cell size about 3.4) paints the lower-right black cluster as the conservative footprint of the two rectangles in the horizontal arm. The cells that disagree are edge cells drawn white where a strict all-samples-inside test would paint them black. The circled black cluster itself agrees with the left-hand obstacles, so the raster is not altered. No caption is edited on this branch.

## Bugs

No defect was found that, once corrected, would change a number in the experiment JSON, CSV, or GeoJSON, or that silently disagrees with a cited figure’s geometry.

1. Phenomenon: `pathCoverage_experiment/.venv/bin/python` is a Mach-O arm64 executable (`file` reports Mach-O; `pyvenv.cfg` says `home = /opt/miniconda3` and the venv was created on macOS). Executing it on this Linux host fails. Location: `pathCoverage_experiment/.venv`. Fix: create a new virtualenv with the Linux interpreter and install `pathCoverage_experiment/requirements.txt`. That does not change existing figures or numeric results. The venv is outside `rev/B`, so the fix is not a commit on this branch. Replots use `/home/panyz/miniconda3/bin/python` with matplotlib, pandas, numpy, and pillow installed for the user.

2. Phenomenon: `compose_robot_figure.mjs` reads `/Users/justin/Desktop/robot{1,2,3}.svg` and writes captions that are not the cited figure’s captions. `figures/create_improved_coverage_ppt.py` reads a pptx under `/Users/justin/Documents/...` that is not in this tree. Location: those two files. Fix: retarget them at the SVGs already in the tree only if someone needs to regenerate the slide or the old three-panel assembly. Leaving them unchanged does not change any cited figure or any experimental number. They are outside `rev/B` and are not patched here.

3. Phenomenon: `figures/generate_figure_2.py` and `figures/generate_figure_3.py` write Chinese `*_cn` files. Running them as they stand does not regenerate `figure_2_coverage_comparison_en.png` or `figure_3_segmentation_order_en.png`. Location: the `output_*` paths and the Chinese title strings in those scripts. Fix, if a later edit must round-trip the English files: point the savers at the English names and use the English strings already stored in `assets/svg_sources/figure_3_segmentation_order_en.svg` and in the cited coverage PNG. Not applied in this survey. The cited English files are left as they are.
