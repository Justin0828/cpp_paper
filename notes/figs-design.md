# Figure designs

Measured inclusion widths for `english_paper` (`a4paper`, 11 pt, 25 mm margins):

- `\textwidth` = 455.24411 pt = 160.000 mm. Six full-width figures use this as the PDF media-box width.
- Speed minipage `0.49\linewidth` = 223.07211 pt = 78.401 mm. `figure_5a` and `figure_5b` use this width. Their `\includegraphics[width=\linewidth]` lines and the lines `\small (a) \texttt{simple}` and `\small (b) \texttt{complex}` stay. Those two PDFs contain no second `(a)` or `(b)`.

The manuscript is not a 3.5 in / 7 in two-column page. Media boxes follow the real inclusion width so 8–9 pt type is not scaled.

Colors and strokes are only in `figures/style/paperstyle.tex` and `figures/style/paper.mplstyle`.

| Role | Hex | Sample |
| --- | --- | --- |
| Disc stroke | `#E97132` | Arm in figure 4 and figure 6 |
| Disc fill | `#F2AA84` | Disc fill in figure 4 and figure 6 |
| Chassis fill | `#8FDFED` | Base fill in figure 4 and figure 6 |
| Path / main line | `#156082` | Paths and dimension arrows in figure 4 and figure 6 |
| Secondary | `#7F7F7F` | Dotted construction line in figure 6 |
| Emphasis | `#C23B3B` | No red sample in figure 4 or figure 6; kept distinct from the disc orange |

`#042433` is the disc-rim outline in figure 4 and is used only as type ink. `#F3F3F3` is a neutral secondary tint for free-space fills. Strokes are 0.8 pt (main) and 0.5 pt (auxiliary). Dimension lines are solid 0.5 pt with a double arrow. Dashes are only auxiliary lines. Schematic type is `newtxtext` / `newtxmath`. Data figures use Nimbus Roman, the Times-metric face, through `paper.mplstyle`. Panel tags, where a figure has panels, are `(a)`, `(b)`, `(c)`, `(d)` centered directly under the panel at 9 pt. The same placement is used for every multi-panel figure.

Same object, same color: disc and disc sweep are orange, the base is cyan, routes and structure lines are navy, non-work or construction marks are gray, collisions and the fourth capability class are red.

## figure_cpp_class_quadrant

One sentence. The four capability classes already named in Section 2.2 sit on map representation and robot-model fidelity, and BiRect is the environment--platform coupled class.

Layout. One panel, no `(a)` tag. Media box 455.24411 pt by 112 mm. Four rounded cells in a 2 by 2 grid. A navy arrow under the grid is the horizontal axis; a navy arrow on the left is the vertical axis.

Elements.

- Lower left, white fill, navy 0.8 pt edge: class “Idealized coverage”; entries BCD and STC.
- Lower right, same edge: “Map-enhanced”; Polygon CPP, Fields2Cover, Nobleo.
- Upper left, same edge: “Platform-constrained”; Mobile manipulator, SatAOI.
- Upper right, red 0.8 pt edge, “BiRect” in red: “Environment--platform coupled”.
- Horizontal axis label “Map representation”, ends “idealized” and “complex”.
- Vertical axis label “Robot model”, ends “fixed footprint” and “base--arm--disc”.
- No series, no map, no percentages.

Symbols and the body. The figure has no mathematical symbols. The two axis names are the two dimensions defined in the paragraph that begins “Existing CPP methods can be compared along two dimensions” (`english_paper/sections/introduction.tex`, before `fig:cpp-classes`). The four class names are the names in that same paragraph and in Table `tab:cpp-comparison`. Fields2Cover is drawn only in the map-enhanced cell, as the table note requires. BiRect is the proposed row of that table.

Baseline match. Flat cells, navy structure, one red accent, serif labels, no chart furniture. Figure 3 places titles under panels; this figure is a single diagram, so it has no panel tag.

Advisor B25. The sketch uses only the four existing classes. It plots no experimental map and no numeric result.

## figure_strip_geometry

One sentence. For one rectangle, the retracted entry pose puts the base outside the boundary, the rectangle is divided into \(N_s\) work strips, and the swing half-amplitude \(\phi_w\) is the angle that lets the disc cover one strip.

Layout. Three panels in one row. Media box 455.24411 pt by 68 mm. Tags `(a)`, `(b)`, `(c)` centered under the panels.

Elements.

- `(a)` Entry pose. Free rectangle, navy 0.8 pt. Disc (orange fill, orange 0.8 pt edge) centered on the left boundary. Cyan base outside that boundary. Orange arm. Heading arrow \(\theta\) pointing out of the rectangle (the left-boundary case \(\theta=\pi\)). Solid 0.5 pt double arrow from the base center to the disc center, labeled \(d_p+L\).
- `(b)` Work strips. One rectangle, three bands separated by gray dashed 0.5 pt lines. Solid 0.5 pt double arrows: \(\ell_R\) along the strip, \(h_R\) across all strips, \(w_s\) across one strip. \(N_s\) above the rectangle. Red dot at the lower-left corner, the starting corner.
- `(c)` Swing amplitude. Cross-section of one strip. Gray dashed centerline. Arms at \(+\phi_w\) and \(-\phi_w\), length \(L\), orange. Discs of radius \(r_d\) whose outer edges meet the strip boundaries. Solid 0.5 pt angle mark \(\phi_w\). Solid 0.5 pt double arrows for \(r_d\) and \(w_s\).

Symbols and the body. All are introduced before or at the figure in `methodology.tex`.

- \(d_p\), \(L\), \(r_d\), \(\theta\): Section 3.2, the paragraph before Eq. (1), and Eq. (1).
- \(d_p+L\): Eq. (10), retracted base center.
- \(\ell_R\), \(h_R\), work strip: the paragraph that begins “The swing amplitude is the half-amplitude”, immediately before this figure.
- \(\phi_w\): the first sentence of that paragraph.
- \(N_s\), \(w_s\): Eq. (13).
- The relation drawn in `(c)`, outer edge at \(L\sin\phi_w+r_d\), is Eq. (14).

Baseline match. Disc orange, base cyan, structure navy, as in figure 4. Dimension arrows are the same double-arrow idea as figure 4, drawn solid 0.5 pt because dashes are reserved for auxiliary lines. Serif math is `newtxmath`, the body font. No paragraph inside the figure.

Advisor B63, first figure. Principle drawing for Section 3.5.2. Only symbols already defined for that subsection. Not an experimental map.

## figure_speed_coupling

One sentence. During the half-swing time \(T_{\mathrm{half}}\) the chassis at \(v_{\mathrm{work}}\) advances one disc diameter \(2r_d\), while the arm swings from \(-\phi_w\) to \(+\phi_w\).

Layout. One panel, no tag. Media box 455.24411 pt wide, drawing centered with margin on both sides. Two poses, travel to the right. The left pose is the start of the half-swing; the right pose is the end. The only length dimension is the gap between the two chassis centers.

Elements.

- Left pose, arm at \(-\phi_w\): cyan chassis, orange arm, orange disc. Right pose, arm at \(+\phi_w\), same parts. The drawn center-to-center gap equals the drawn disc diameter.
- One solid 0.5 pt double arrow, and no other length dimension, between the two chassis centers, labeled \(2r_d\).
- Time is not that arrow. Under the poses, a time axis runs from \(t=0\) at the left chassis to \(t=T_{\mathrm{half}}\) at the right chassis. \(T_{\mathrm{half}}\) appears only as a time mark.
- \(-\phi_w\) and \(+\phi_w\) are angle arcs between each arm and the travel direction, at the pivot. The labels sit on those arcs, not beside the discs.
- \(v_{\mathrm{work}}\) is a navy 0.8 pt arrow on the travel line through the chassis centers.
- No second disc-radius arrow and no arm-length arrow; those stay in the strip figure.

Symbols and the body. Section 3.5.3 and Eqs. (15)–(17). \(\phi_w\) and \(r_d\) are already defined in Section 3.5.2 and Section 3.2. \(v_{\mathrm{work}}=\min(v_{\max},2r_d/T_{\mathrm{half}})\). \(T_{\mathrm{half}}=2\phi_w/\omega_{a,\max}\) is a time; \(2r_d\) is the distance the chassis travels in that time.

Baseline match. Disc orange, chassis cyan, path navy, as in figure 4. One travel arrow, as in figure 6. Serif math from `newtx`. Strokes only from `paperstyle.tex`.

Advisor B63, second figure. Principle drawing for Section 3.5.3. No new symbol beyond that subsection.

## figure_coverage_segments

One sentence. \(\mathcal C_{\mathrm{work}}\) is only the disc sweep on work strips; \(\mathcal C_{\mathrm{traj}}\) is that sweep plus the disc sweep on the non-work path (lane change and the transfer).

Layout. Two panels. Media box 455.24411 pt wide. Tags `(a)` and `(b)` centered under the panels. One legend above both panels, not inside either scene: orange swatch “work sweep”, gray swatch “non-work sweep”. The two panels use the same rectangles, the same work-strip centerlines, and the same dashed non-work path. Only the sweep bands differ.

Elements.

- Two free rectangles, navy 0.8 pt, light gray fill. Work strips are orange bands of one disc diameter, with a navy 0.8 pt centerline and a direction arrow.
- Non-work path, in both panels: dashed 0.5 pt lane changes between strips, and one dashed transfer from the left rectangle to the right. Dashed because the path is auxiliary.
- `(a)`: orange work bands only. The dashed lane change and the transfer have no sweep band. \(\mathcal C_{\mathrm{work}}\) is a leader callout whose line ends on an orange band.
- `(b)`: the same orange bands, plus one continuous gray semi-transparent band along the whole non-work path. The band width equals the disc diameter, the same width as the orange bands. It is a filled band, not a row of discs. \(\mathcal C_{\mathrm{traj}}\) is a leader callout whose line ends on that gray band.
- No map, no third ratio, no sentence. No separate icon for deploy, retract, or an in-place turn; those non-work phases are the same gray sweep as the lane change and the transfer.

Symbols and the body. \(\mathcal C_{\mathrm{work}}\) and \(\mathcal C_{\mathrm{traj}}\) are Eq. (25) in Section 3.7. The paragraph above the figure says entry, lane change, rotation, deploy or retract, transit, and handoff are non-work, and that \(\mathcal C_{\mathrm{traj}}\) adds those sweeps to the work sweep.

Baseline match. Disc orange and path navy follow figure 4 and figure 6. Gray is the secondary role, drawn translucent. Panel tags sit under the panels, as in figure 3. Strokes and colors only from `paperstyle.tex`.

Advisor B67. Two rectangles and one transfer, plus the lane change that the work/non-work paragraph already names. Not an experimental map.

## figure_2_coverage_comparison_en

One sentence. On `simple` and on `complex`, BiRect’s full-trajectory disc sweep stays in the free space, while the Fields2Cover centerline leaves the field.

Layout. Two by two. Media box 455.24411 pt wide; height set with the panels (about 6.4 in). Tags under the panels:

- `(a)` `simple`, BiRect
- `(b)` `simple`, Fields2Cover
- `(c)` `complex`, BiRect
- `(d)` `complex`, Fields2Cover

Each tag line also carries the saved ratio, and the Fields2Cover lines carry the saved outside area. Equal aspect, axes in metres. One legend under the grid: uncovered free space, full-trajectory sweep, obstacle, centerline, invalid. The legend does not cover the maps.

Elements.

- Free space: secondary tint. Obstacle: ink. Full-trajectory sweep: disc fill. Centerline: path navy at the main stroke on the Fields2Cover panels, with the portion outside the field in emphasis red.
- BiRect panels show the full-trajectory disc mask. The stored `coverage_final.png` is the work-only mask (its blue count equals `work_disc.covered_free_px`, not the full-trajectory count). The full-trajectory mask is not stored. The script rebuilds it from the frozen config and seed, the reproduction path in `notes/codebase-map.md`, and aborts if the rebuilt pixel count or ratio differs from `metrics.json`. It writes no result file.
- Fields2Cover panels read the GeoJSON field, `path.csv`, and `metrics.json`. The raster is a half-width buffer of the saved path, drawn as a picture of that path. The printed ratio and outside area are the saved metric values, not a new measurement.
- In-figure names are `simple` and `complex`. File names stay `map_test1` and `parkingGraph`.

Numbers printed from the files, then shown at the table’s two-decimal rounding:

- BiRect `simple`: `coverage.full_trajectory_disc.coverage_ratio` 0.9410801963993454, label 94.11%.
- Fields2Cover `simple`: `coverage_ratio` 0.7839828689793511, label 78.40%; `path_validation.swept_area_outside_field_m2` 4.513435771890705, label 4.51 m².
- BiRect `complex`: 0.9572659524918491, label 95.73%.
- Fields2Cover `complex`: 0.92835265474812, label 92.84%; outside area 20.002713623842464, label 20.00 m².

Symbols and the body. The panel words `simple`, `complex`, BiRect, and Fields2Cover are the names in Section 4.1 and Table `tab:baseline-comparison`. No new symbol. The ratios are the table’s coverage ratios.

Baseline match. Disc-colored sweep, navy path, red for the failure, serif 8 pt labels. The map is a data figure, so it uses matplotlib and `paper.mplstyle` rather than TikZ.

Advisor B70. The picture says `simple` and `complex`. CSV, JSON, and GeoJSON names are unchanged, and no experimental number is edited.

## figure_5a_vehicle_speed_map_simple_en and figure_5b_vehicle_speed_parkingGraph_en

One sentence. As base speed rises, full-trajectory coverage and execution time both fall; the horizontal axis starts at 0 and the markers are only the six measured speeds.

Layout. One axes pair per PDF. No panel tag inside the PDF. Media box 223.07211 pt wide and 2.55 in tall. `figure_5a` reads `map_test1/comparison_summary.csv` and is the `simple` panel. `figure_5b` reads `parkingGraph/comparison_summary.csv` and is the `complex` panel. The tex under the figures already says so.

Elements.

- Horizontal axis: configured base speed \(v\) in m/s, limit starting at 0. Ticks only at the six saved speeds 0.5, 1.0, 1.5, 2.0, 2.5, 3.0. No marker at 0.
- Left axis, navy 0.8 pt, circle markers: `full_trajectory_disc_coverage_ratio` times 100.
- Right axis, red 0.8 pt, square markers: `duration_seconds`.
- Dotted gray 0.5 pt horizontal grid, auxiliary.
- Legend above the axes, one row: “Coverage”, “Time”. It does not cover the curves.
- No work-strip series and no single-strip series. `work_disc_coverage_ratio` is not plotted.
- No in-figure map title, so the tex label is not repeated.

Symbols and the body. \(v\) is the base speed in the speed-study section. \(\rho=v/\omega_a\) is defined in that section; the script prints \(\rho\) beside each point and does not add a \(\rho=0\) sample. The plotted coverage and duration are the columns behind Table `tab:speed-study`.

Baseline match. Navy and red are the path and emphasis roles. Serif 8 pt type. The two curves are the whole figure; there is no schematic mixed in.

Advisor B81 and B70. The curves are redrawn from `comparison_summary.csv`. The speed axis starts at 0. No new run, no added sample, no single-strip curve. The directory names stay in the file names; the words `simple` and `complex` stay in the tex under the figures.

## pipeline_overall_improved_en

Source: `assets/svg_sources/pipeline_overall_improved_en.svg`. The file exists, so the title is edited there and the included image is re-exported. The PNG is not painted on.

Box 4’s visible title becomes exactly `4. Global Route Planning & Rectangle Coverage`. It is split after the ampersand so it fits the box, in one `<text class="title-small">` with a `<tspan>`. `title-small` is `font-weight: 700`, the same class as boxes 1, 2, and 3. The inline size is 18 px, the size already used by the other two-line title (box 3). No other box text, module, or color in the SVG changes.

The paper includes the re-exported PDF at `\includegraphics[width=\linewidth]`. The PDF media box is `\textwidth`, so that line does not scale the artwork a second time. The SVG’s own `width="140mm"` attribute stays; the scale to the text width happens once at export.

Advisor B38. The old “Global Routing” wording becomes this global-route-planning title. The four module boxes stay.

## Self-check log

Previews were rendered with `pdftocairo` at the inclusion width and read back. Defects below are ones the preview showed; each line is the fix that removed it.

- Strip panel (c): the \(r_d\) arrow was drawn inside the disc and crossed the strip boundary. The radius is now the horizontal radius, with the label outside the disc and clear of \(w_s\).
- Coverage segments, panel (b): the gray discs sat above the transfer curve. They are centered on the Bézier, and the dashed transfer is drawn again on top of them.
- Speed coupling: the two poses sat in a small patch of a wide canvas. The geometry is scaled by 1.18 inside the same 9 pt labels, and the media box is 84 mm tall so \(T_{\mathrm{half}}\) is not clipped.
- Coverage comparison: the panel tags collided with the axis numbers, and the bottom legend collided with panel (c). The legend is above the panels. Each tag sits in the gap under its axis. The labels read `(a) simple, BiRect` / `94.11%`, `(b) simple, Fields2Cover` / `78.40%, 4.51 m² outside`, `(c) complex, BiRect` / `95.73%`, `(d) complex, Fields2Cover` / `92.84%, 20.00 m² outside`.
- Pipeline export: cairosvg gives a `tspan` with `font-style: italic` a zero advance, ignores `baseline-shift`, and this machine has neither Arial nor Cambria Math. The render copy embeds Liberation Serif Italic, lowers subscripts with `dy`, and flattens math `tspan`s. The SVG source keeps `Arial`, `Cambria Math`, and the title string. Box 4 reads `4. Global Route Planning & Rectangle Coverage` on two lines in `title-small` (`font-weight: 700`), the same class as boxes 1–3. One line does not fit the box at that size.

## Self-check, speed coupling and coverage segments

Opened the inclusion-width renders `figure_speed_coupling.png` and `figure_coverage_segments.png`.

- Speed coupling. An earlier draw put \(T_{\mathrm{half}}\) on a second length dimension above \(2r_d\), and put \(\pm\phi_w\) on the discs. The length dimension is now only \(2r_d\) between the chassis centers. Time is the axis \(t=0\) to \(t=T_{\mathrm{half}}\) under the poses. The angle labels were first outside the wedges and then on the arms; they now sit in the wedge between each arm and the travel direction, on the arcs, clear of the discs, the chassis, and \(v_{\mathrm{work}}\). \(t=0\) and \(t=T_{\mathrm{half}}\) are placed outward from the arrow ends so they do not meet. The ink is centered in the 160 mm width (left and right margins agree within a few millimetres).
- Coverage segments. The non-work sweep was a row of gray discs, and the two \(\mathcal C\) labels floated. Panel (b) now uses one continuous gray band, the same width as the orange work bands, along the dashed lane changes and the transfer. Panel (a) keeps that dashed path with no band. \(\mathcal C_{\mathrm{work}}\) has a leader onto an orange band; \(\mathcal C_{\mathrm{traj}}\) has a leader onto the gray transfer band. The first layout clipped the right-hand lane-change band; both panels were shifted left, and the opened PNG keeps margin on both sides. The legend sits above both panels and does not cover them. The two scenes match except for the sweep bands.

## Revision: coverage strips and the single-rectangle primitive

Figure 6 and `figure_coverage_segments` stay separate. Figure 6 (`fig:rectangle-primitive`) is only the reciprocating path inside one rectangle. `figure_coverage_segments` (`fig:coverage-segments`) is only the distinction between \(\mathcal C_{\mathrm{work}}\) and \(\mathcal C_{\mathrm{traj}}\). They are not merged, and Figure 6 is not redrawn as a second copy of the two-rectangle diagram.

### figure_coverage_segments

The caption stays the one sentence already in `methodology.tex`: “Work coverage counts disc sweeps on work strips; full-trajectory coverage also counts sweeps during transfer and adjustment.”

Section 3.5, Eq. (13), fixes the strip geometry. For a transverse side \(h_R\), \(N_s=\lceil h_R/w_{\max}\rceil\) and \(w_s=h_R/N_s\). The drawing uses one \(h_R\) for both rectangles: \(N_s=3\), \(w_s=10\,\mathrm{mm}\), \(h_R=N_s w_s=30\,\mathrm{mm}\). Each rectangle is filled by \(N_s\) strips of height \(w_s\). Adjacent strips share an edge. Their union is the whole rectangle. There is no interior gap and no unused band of free space inside the rectangle. The two rectangles may differ in \(\ell_R\) (drawn 26 mm and 18 mm). Travel along a strip alternates direction. That is the work path, not a second figure.

Non-work segments are gray bands of width \(2r_d\). The drawn radius is \(r_d=2\,\mathrm{mm}\), so the band is \(4\,\mathrm{mm}\) wide, strictly narrower than \(w_s\). Those bands sit only at the turnaround ends (the lane change between strip \(i\) and strip \(i+1\), outside the short ends of each rectangle) and in the single gap that is the transfer from the left rectangle to the right. They do not enter the strip interiors. They belong to \(\mathcal C_{\mathrm{traj}}\).

Panel `(a)` draws only the orange work region (`workband`). The \(\mathcal C_{\mathrm{work}}\) mark is an outer contour around both rectangles, so it spans every strip, not a leader onto one band. Panel `(b)` draws the same orange region plus the gray bands (`nonworkfill`). The \(\mathcal C_{\mathrm{traj}}\) mark is an outer contour around the union of orange and gray. That contour is larger than the gray region alone. Tags `(a)` and `(b)` stay under the panels. The media box stays `\paperfullwidth`. Strokes and colors come only from `paperstyle.tex` (`workband`, `nonworkfill`, `guide`, `flow`, `main`, `aux`).

The previous drawing of this figure left gaps between thin orange bands and gave the gray band the same width as those bands, with a leader from each \(\mathcal C\) symbol onto one band. That geometry is what this redraw replaces. The section above this one records that earlier drawing and is left as it stood.

### Figure 6

`english_paper/figures/figure_6_single_rectangle_coverage.png` is a 2400×2400 raster with no generator script. The upper-right disc and the dashed line run off that canvas. `rect_coverage_recolored.svg` is not this figure. The included file becomes a TikZ PDF of the same primitive: one rectangle, five abutting strips, the boustrophedon through the chassis centers, the swing-arm poses (disc, arm, and base, including the rotated pose), and the dashed other-axis line. The upper-right disc, the other discs, every arm, and both ends of the dashed line lie inside the media box with margin. Nothing is added that would make this a two-rectangle transfer diagram.

Colors are the `paperstyle.tex` roles: disc `#E97132`, disc fill `#F2AA84`, chassis `#8FDFED`, path `#156082`, secondary `#7F7F7F`. Alternate strips use `workband` and a secondary tint so the five passes stay visible; the PNG’s lavender is not one of those roles. The English include stays `\includegraphics[width=0.5\linewidth]`. The caption stays “Single-rectangle coverage primitive.” The root PNG and the Chinese draft are unchanged.

## Revision: lane-change ends follow the transfer

Figure 6 is unchanged. This note only corrects where `figure_coverage_segments` puts the lane-change bands. The strip count, the abutting orange tiles, the band width \(2r_d\), the one transfer, and the two outer contours stay as in the section above.

Both rectangles keep the same strip arrows. The bottom strip and the top strip travel to the right. The middle strip travels to the left. The transfer is centered on the top-strip centerline. It starts at the right end of the left rectangle, where that top strip’s arrow arrives, and it ends at the left end of the right rectangle, where that top strip’s arrow departs.

A gray lane-change band is the turnaround of this one path. It sits outside the shared end of strips \(i\) and \(i+1\): the end where the path leaves one strip and enters the next. Its width is still \(2r_d\), and it does not enter either rectangle. On the left rectangle the path climbs from the bottom strip to the top strip and then leaves through the transfer, so the lower band is on the right end and the upper band is on the left end. The transfer enters the right rectangle, so that rectangle is traversed downward. Its upper band is on the outgoing right end of the top strip, joining that end to the middle strip, and its lower band is on the left end. Those two bands are not a copy of the left rectangle’s ends. In particular the upper band is not on the entry side, and it does not overlap the transfer. No lane-change band overlaps another or the transfer.

Panel `(a)` still draws no gray fill. \(\mathcal C_{\mathrm{work}}\) still outlines every orange strip. Panel `(b)` draws the orange tiles plus these gray bands, and \(\mathcal C_{\mathrm{traj}}\) still outlines that union. The caption stays the same one sentence.
