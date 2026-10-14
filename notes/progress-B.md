# Class B progress

- [x] 25. Quadrant of the four classes already named in the introduction. Map representation increases to the right; robot-model fidelity increases upward. Idealized holds BCD and STC; map-enhanced holds Polygon CPP, Fields2Cover, and Nobleo; platform-constrained holds the mobile manipulator and SatAOI; environment–platform coupled is marked not yet unified and BiRect. Fields2Cover and SatAOI each appear once. No experimental map, and Table 1 is unchanged.

  ```bash
  python scripts/figures/class_quadrant.py
  ```

  Output: `english_paper/figures/figure_cpp_class_quadrant.png`, included after the four class-name definitions in `english_paper/sections/introduction.tex`. No caption.

- [x] 38. Stage 4 header “Global Routing” is now “global route planning”. The other module boxes are unchanged.

  ```bash
  python scripts/figures/relabel_workflow.py
  ```

  Output: `english_paper/figures/pipeline_overall_improved_en.png`. Source text: `assets/svg_sources/pipeline_overall_improved_en.svg`.

- [x] 48. Figure 4 subplot titles now sit under each panel. The main title stays on top, and the LaTeX caption is untouched.

  ```bash
  python scripts/figures/move_raster_titles.py
  ```

  Output: `english_paper/figures/figure_3_geometric_to_binary_raster.png`. Baselines in `assets/svg_sources/transfer.svg` are `y="118"` and `y="232"`.

- [x] 49. The lower-right black cluster in Figure 4(d) agrees with the two rectangles in the horizontal arm of the left-hand geometry. The check is in `notes/codebase-map.md` under “Figure 4(d) black cluster”. Those cells were not redrawn, and no caption was added.
- [ ] 63. Principle figures for 3.5.2 and 3.5.3.
- [ ] 67. Section 3.7 schematic.
- [ ] 70. In-figure map names.
- [ ] 81. Speed curves.
