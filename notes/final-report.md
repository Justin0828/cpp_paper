# 终版 PDF

两份 PDF 都含 `rev/figs`（`bf9d98b`）的八张矢量图。没有推送。`main` 仍是 `3590a4a933d97dd775314b2dfb62d4a9d5b996db`。`cpp_paper` 工作区仍在该提交上。`rev/figs` 没有在本工作区检出。

## 终版论文

- 路径：`english_paper/final/paper_final.pdf`
- 页数：28（`pdfinfo`；A4）
- 加入该文件的提交：`0955e4bc554843b727427eec4304952dc12ca5e8`（`rev/merged`）
- 来源：在 `rev/merged` 上对 `english_paper/main.tex` 用 `latexmk -pdf`（pdflatex）完整编译两次，退出码都是 0，两次都是 28 页。日志里没有 undefined references，也没有未定义的引用。
- 正文标题是 “BiRect: Bidirectional Rectangular Coverage Path Planning for a Swing-Arm Concrete Troweling Robot”。`pdftotext` 里标题在版心处断成两行。抽出的文字没有 U+FFFD，也没有 `??`。
- 页码从 1 到 28，连续，无缺号。
- 八张重绘图是矢量 PDF，按设计版心宽度嵌入，图内字号是导出时的字号：
  - 第 5 页 `figure_cpp_class_quadrant.pdf`
  - 第 9 页 `pipeline_overall_improved_en.pdf`
  - 第 15 页 `figure_strip_geometry.pdf`
  - 第 16 页 `figure_speed_coupling.pdf`
  - 第 19 页 `figure_coverage_segments.pdf`
  - 第 22 页 `figure_2_coverage_comparison_en.pdf`
  - 第 26 页 `figure_5a_vehicle_speed_map_simple_en.pdf` 与 `figure_5b_vehicle_speed_parkingGraph_en.pdf`
- `rev/figs` 没有改成矢量的图仍是原来的光栅文件：第 2 页照片 JPG，第 4 页盘与基座 PNG，第 10 页几何栅格 PNG，第 14 页单矩形 PNG，第 24 页分割顺序 PNG。

## 批阅版

- 路径：`english_paper/final/paper_diff_for_advisor.pdf`
- 同一份编译结果也写在 `english_paper/diff.pdf`
- 页数：32（`pdfinfo`；A4）
- 加入该文件的提交：`ac63d9514c9ed25276401507c0a4911eee5c592f`（`rev/merged-diff`）
- 来源：在 `rev/merged-diff` 上对 `english_paper/diff.tex` 用 `latexmk -xelatex` 编译两次，退出码都是 0，两次都是 32 页。日志里没有 undefined references，也没有未定义的引用。`pdffonts` 有 `NotoSansCJKjp` 和 `NotoSansCJKsc`（Noto Sans CJK）。抽出的中文是原文，包括 `修订对照说明`、`图例`、`新增`，以及边注 `[2]`、`[11]`。
- 第 1 页是图例（`\thispagestyle{empty}`），没有印页码。第 2–32 页的页码是 2 到 32，连续，无缺号。
- 图例页、latexdiff 红删蓝增、以及 `76b418f` 里的全部 `\marginpar` 正文都还在。
- 新增图标“新增”，用的是最新矢量 PDF，并与终版同一幅图：第 7 页象限图，第 19 页条带几何，第 20 页速度耦合，第 22 页覆盖分段。
- 修改的图左红框旧、右蓝框新。左侧是 `old_figs/` 里与 `3590a4a` 逐字节相同的 PNG，右侧是矢量 PDF：第 12 页流程图，第 25 页覆盖对比，第 29 页速度曲线。旧图仍是原先的 `map_simple` / `parkingGraph` 或旧流程框，新图与终版一致，没有放反。
- `figure_3_geometric_to_binary_raster` 没有矢量 PDF，第 13 页左右都仍是 PNG。
- 边注抽查了第 2–4、7、10–13、19–20、24–27、29–30 页。边注之间不重叠。扫描策略段那一行原先压住边注 `[76]`，已在 `map_test1` / `simple` 前断行；断行后 `[76]` 与正文之间有空隙。`[70]`、`[75]`、`[77]`、`[79]`、`[80]` 也不压正文。

## 遗留问题

- 两份编译日志都有 hyperref / xdvipdfmx 的 `equation.3.1` 目标名重复警告。正文公式编号仍按顺序印出。这是合并前就有的锚点问题，这次没有改公式。
- 批阅版第 1 页按原 `diff.tex` 不印页码。后面的页码没有缺号。
- `diff.tex` 里仍有若干 latexdiff 造成的 overfull 行。已查看的边注不与正文或其他边注重叠。第 25 页表 2 的 Map 列里，删除的 `map_test1` / `parkingGraph` 和新增的 `simple` / `complex` 挤在同一格，没有伸进边注。
- `pdftotext` / `pdftoppm` 对部分图内字体报 “Mismatch between font type and embedded font file”。抽出的正文没有替换字符，也没有 `??`。
- 照片和 `rev/figs` 仍引用为 PNG/JPG 的图没有另做矢量版。

## 覆盖条带与单矩形原语

`rev/figs` 重画了两张图，随后重编了两份 PDF。没有推送。`main` 仍是 `3590a4a933d97dd775314b2dfb62d4a9d5b996db`。上文里 “第 14 页单矩形 PNG” 指的是上一版；这一版 Figure 6 已改为下面的矢量 PDF。

- 图：`english_paper/figures/figure_coverage_segments.pdf`。作业带按 \(N_s\) 与 \(w_s=h_R/N_s\) 首尾相接，铺满两个矩形。非工作段是宽 \(2r_d\)、比作业带窄的灰带，只画在矩形两端掉头处和两矩形之间。(a) 只有橙色，\(\mathcal C_{\mathrm{work}}\) 的外轮廓包住全部橙色；(b) 是橙色与灰色的并集，\(\mathcal C_{\mathrm{traj}}\) 的外轮廓包住这个并集。图注仍是一句。
- 图：`english_paper/figures/figure_6_single_rectangle_coverage.pdf`。内容仍是单个矩形内的往复路径。右上圆盘、摆臂和虚线都在版心内，四周留有空白。嵌入宽度仍是 `0.5\linewidth`。删掉的长图注没有加回。
- `rev/figs`：`ba806fb88fbbc96a9c0b74d15db7ece100d2913f`。
- `rev/merged`：`c0f4c5fac1bda42b86dcf1eb72537c6b1f118e11`（合并提交 `62f2e46`）。路径 `english_paper/final/paper_final.pdf`。在 `rev/merged` 上对 `english_paper/main.tex` 用 `latexmk -pdf` 编译两次，退出码都是 0，两次都是 28 页。Figure 7 在第 14 页，圆盘和虚线没有被裁切，图注仍是 “Single-rectangle coverage primitive.”。Figure 10 在第 19 页，作业带铺满矩形，灰带更窄且只在掉头和转移处，图注仍是一句。
- `rev/merged-diff`：先合并为 `b7221a0d233fe606f3b62be01ab1b808c4b18040`，批阅版 PDF 在 `cc0e3eb4fb9ea832eacd97c33fda41b0e94cc9c6`。`english_paper/diff.tex` 里可见的 Figure 6 改为上述 PDF，宽度 `0.5\linewidth`；被注释掉的旧 PNG 行没有改。覆盖图仍在 FIGNEW 里，标“新增”，路径是 `figures/figure_coverage_segments.pdf`。边注正文与 `76b418f` 相同，包括 `[60]`、`[61]`、`[67]`。可见的旧图仍只来自 `old_figs/`。在 `rev/merged-diff` 上对 `english_paper/diff.tex` 用 `latexmk -xelatex` 编译两次，退出码都是 0，两次都是 32 页。`english_paper/final/paper_diff_for_advisor.pdf` 与 `english_paper/diff.pdf` 字节相同。Figure 7 在第 18 页，圆盘和虚线没有被裁切，删去的长图注仍是红字。Figure 10 在第 22 页蓝框内，标“新增”，作业带、灰带和两条外轮廓都完整。
- hyperref 的 `equation.3.1` 目标名重复，以及 `pdftotext` 的字体类型不匹配，仍是合并前就有的警告。这次没有改公式。

## 进入矩形的掉头端

上一节的灰带画在矩形两端，但右矩形用了和左矩形相同的端点。转移在顶带上从左矩形右端进入右矩形左端，右矩形最上一条灰带却也在这个入口，和转移重叠，并没有接在顶带出去的右端。这一节把进入矩形的掉头端翻到路径离开的那一侧。Figure 6 没有再改。没有推送。`main` 仍是 `3590a4a933d97dd775314b2dfb62d4a9d5b996db`。

- 图：`english_paper/figures/figure_coverage_segments.pdf`。两个矩形的箭头仍是底带向右、中带向左、顶带向右。左矩形自下而上，下灰带在右端、上灰带在左端。右矩形由转移进入后自上而下，上灰带在顶带出去的右端，下灰带在左端。灰带宽仍是 \(2r_d\)，比作业带窄，不进入矩形内部，也不与转移重叠。(a) 仍只有橙色，\(\mathcal C_{\mathrm{work}}\) 包住全部橙色；(b) 的 \(\mathcal C_{\mathrm{traj}}\) 包住橙色与灰色的并集。图注仍是一句。
- `rev/figs`：`07a9b2e1ef9368f9d6a8b0aa6146504b5e8f4317`。
- `rev/merged`：合并 `803b4af9fd1299afa906d9ceb97736d4a171be93`，终版 PDF 在 `958ea8adafd25aa61bd5bb62f97bcff3e7c9ae0b`。路径 `english_paper/final/paper_final.pdf`。`latexmk -pdf` 两次退出码都是 0，都是 28 页。Figure 7 仍在第 14 页，圆盘和虚线没有被裁切。Figure 10 在第 19 页，进入矩形的灰带在路径离开的一端，不盖住转移。
- `rev/merged-diff`：合并 `50538d32bb4a38801eb3b84c37e3c4caa243f420`，批阅版 PDF 在 `feeb0881cdb7857ee58860ddc0cfa44f7ce3934f`。`english_paper/diff.tex` 的图路径和边注没有改，包括 `[60]`、`[61]`、`[67]`。旧图仍只来自 `old_figs/`。`latexmk -xelatex` 两次退出码都是 0，都是 32 页。`english_paper/final/paper_diff_for_advisor.pdf` 与 `english_paper/diff.pdf` 字节相同。Figure 7 在第 18 页，没有被裁切。Figure 10 在第 22 页蓝框内，标“新增”，灰带与转移不相重叠。
- hyperref 的 `equation.3.1` 目标名重复，以及 `pdftotext` 的字体类型不匹配，仍是原有警告。这次没有改公式。
