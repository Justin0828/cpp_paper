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

## 边注去掉“按导师意见”

改 `diff.tex` 在重编批阅版之前。`english_paper/diff.tex` 的 81 条边注都删去了开头的“按导师意见”，以及紧跟其后的冒号、逗号或空格。这次没有一条边注在这四个字后面带冒号、逗号或空格，所以只去掉这四个字。编号和后面的说明没有改。`[61]` 现在是“删去 Figure 6 图注的后半句。”，`[67]` 现在是“用两个矩形和一次转移新画覆盖率原理图，未用实验地图。”图例里的“对应导师意见”不是边注，没有改。

重编用 `latexmk -xelatex` 对 `english_paper/diff.tex` 跑了两次，退出码都是 0，都是 32 页。`english_paper/final/paper_diff_for_advisor.pdf` 与 `english_paper/diff.pdf` 字节相同，提交是 `361abf2adaf2921175d7a7ff7c6ae9660306a510`。抽出的文字里没有“按导师意见”。`main` 仍是 `3590a4a933d97dd775314b2dfb62d4a9d5b996db`。没有推送。

## 掉头弧落在橙色作业区上

上一节的灰带画在矩形外面。这一节把掉头扫过的区域收到矩形内部，叠在橙色上。Figure 6 没有再改。没有推送。`main` 仍是 `3590a4a933d97dd775314b2dfb62d4a9d5b996db`。

- 图：`english_paper/figures/figure_coverage_segments.pdf`。每个矩形内部整块是作业区，橙色铺满，条带首尾相接，没有空隙。掉头在路径离开的一端，沿掉头弧叠一层宽 \(2r_d\) 的半透明灰，中心线内收 \(r_d\)，描边不越出矩形边界。橙色仍从灰下透出。两个矩形之间的转移带仍是纯灰，宽 \(2r_d\)。(a) 只有橙色，\(\mathcal C_{\mathrm{work}}\) 包住全部橙色；(b) 的 \(\mathcal C_{\mathrm{traj}}\) 包住橙色与转移灰带的并集。图注仍是一句。
- `rev/figs`：`b35863b52e6b9e7888a50e9b76ab70c589b13f2b`。
- `rev/merged`：合并 `c1606468cf00dad288517f0bc6301f9aed5a757a`，终版 PDF 在 `eb0bf9d891252c12de85560828acae3cd39a3aef`。路径 `english_paper/final/paper_final.pdf`。`latexmk -pdf` 两次退出码都是 0，都是 28 页。Figure 7 仍在第 14 页，圆盘和虚线没有被裁切。Figure 10 在第 19 页，橙色铺满，掉头弧在矩形内，只有转移带是纯灰。
- `rev/merged-diff`：合并 `889a862de8beb6f2d77f72047ee490947474c457`，批阅版 PDF 在 `7fcdae45822ee273c535b630f420d12d4209c7bd`。`english_paper/diff.tex` 的图路径和边注没有改，包括 `[60]`、`[61]`、`[67]`。旧图仍只来自 `old_figs/`。`latexmk -xelatex` 两次退出码都是 0，都是 32 页。`english_paper/final/paper_diff_for_advisor.pdf` 与 `english_paper/diff.pdf` 字节相同。Figure 7 在第 18 页，没有被裁切，删去的长图注仍是红字。Figure 10 在第 22 页蓝框内，标“新增”，掉头弧在橙色之上，转移带是纯灰。
- hyperref 的 `equation.3.1` 目标名重复，以及 `pdftotext` 的字体类型不匹配，仍是原有警告。这次没有改公式。

## P0：栅格、条带数和速度

按 2026-10-15 审阅的五条 P0 改了英文版。Figure 5(d) 已重画。没有推送。`main` 仍是 `3590a4a933d97dd775314b2dfb62d4a9d5b996db`。

- 意见 49。右下角黑格与左侧 L 形及臂上矩形的保守栅格不符。网格以内角对齐，与圆盘或矩形相交的格子标为不可用。已重画 panel (d)，并用 1–4 标出圆盘、竖干方块、臂上矩形和臂下矩形。自由格从 145 减到 122。panel (c) 没有改。
- 意见 63。Figure 8(b) 的 \(N_s\) 从水平顶边移到沿 \(h_R\) 排开的条带组旁，写成 \(N_s\) strips。顶边只留矩形边界。\(w_s\) 仍标一条带高度，\(h_R\) 仍标横向总高。
- 意见 81。Figure 13 横轴补上 0 刻度。0 是原点，曲线仍只有 0.5 到 3.0 m/s 六档。横轴是基座速度 \(v\)，轴上写出 \(\rho=v/\omega_a\)。图注的固定参数与实验记录和正文一致：\(r_d=0.75\) m，\(L=1.20\) m，\(\omega_a=90^\circ\)/s。
- 意见 72/78/81。六档指令速度是 0.5、1.0、1.5、2.0、2.5、3.0 m/s。式 (17) 为 \(v_{\mathrm{work}}=\min(v_{\max},v_{\mathrm{safe}})\)。保存的 12 次运行用 commanded 策略，`work_speed_limited` 为假，记录的作业速度等于指令速度。simple 和 complex 上六档都没有被截断，实际作业速度都是 0.5 到 3.0 m/s。这句话写在“速度越快漏覆盖越多”之前。没有另编 \(\phi_w\)。
- 意见 51。地图一句现为：0 和 255 是 8-bit 像素标签，不是物理尺寸或连续的几何量。\(M\in\{0,255\}\) 和像素物理尺寸 \(s_p\) 仍在。

边注：`[49]` 改为重画说明。另外四条只写这一轮的改动，开头没有“按导师意见”。原先的 `[51]`、`[63]`、`[81]` 和其他边注还在。图例那句还在。

- `rev/figs`：`6e2e23f4022d1f690137cf2a1481a5d426f4cb12`。
- `rev/merged`：合并 `0bcb1fb07da1798eb17e19ab910098dc9eb2404a`，正文 `4f5721536e171e392012f2dab1e4cc9c7fea73fd`，终版 PDF `f0d45c92d70e6258daefe0d31a2c1fa0dbd7ae82`。路径 `english_paper/final/paper_final.pdf`。对 `english_paper/main.tex` 用 `latexmk -pdf` 编译两次，退出码都是 0，都是 28 页。Figure 5(d) 在第 10 页，障碍 1–4 标在几何和黑格上。Figure 8(b) 在第 15 页，\(N_s\) strips 在条带组旁。地图标签句在第 11 页。速度段在第 25 页。Figure 13 在第 26 页，横轴有 0，图注有上述三个固定参数。
- `rev/merged-diff`：正文与图先合并为 `7e272324c588e45a4029bd0b0e9d64affe1d350e`，终版 PDF 再合并为 `30a3b913c99e6d91aa3836e4fd5070900967b8ad`，批阅版 PDF 在 `b54b4c50be5d8425e2ff39adf175c24083ff60a0`。对 `english_paper/diff.tex` 用 `latexmk -xelatex` 编译两次，退出码都是 0，这一轮是 31 页。参考文献仍收到 [22]。`english_paper/final/paper_diff_for_advisor.pdf` 与 `english_paper/diff.pdf` 字节相同。旧图仍只来自 `old_figs/`。Figure 5(d) 在第 13 页，左红右蓝。Figure 8 在第 19 页。地图标签在第 14 页。速度段在第 28 页。Figure 13 在第 29 页。
- hyperref 的 `equation.3.1` 目标名重复，以及 `pdftotext` 的字体类型不匹配，仍是原有警告。这次没有改公式编号，也没有改表 2–4 的数字。
