# 合并报告

`rev/merged` 从 `main`（`3590a4a`，add advisor revision plan）拉出。先 `--no-ff` 合并 `rev/A`（`e2b9e96`，提交 `5023819`），再 `--no-ff` 合并 `rev/B`（`c44c621`，提交 `92121bb`）。没有推送，也没有并进 `main`。

两个分支改的都是英文稿 `english_paper/`。仓库根目录的 `main.tex` 和 `sections/` 相对 `main` 没有差异。下面的页码都是英文 PDF `english_paper/build/main.pdf`（29 页）。根目录中文 PDF `build/main.pdf` 是 31 页，latexmk 退出码为 0，内容仍是合并前的中文稿。

## 各分支改了多少项

分类以 `revisions.md` 为准。C 类为 0。

`rev/A` 改了 73 项：1、2、3、4、5、6、7、8、9、10、11、12、13、14、15、16、17、18、19、20、21、22、23、24、26、27、28、29、30、31、32、33、34、35、36、37、39、40、41、42、43、44、45、46、47、50、51、52、53、54、55、56、57、58、59、60、61、62、64、65、66、68、69、71、72、73、74、75、76、77、78、79、80。

`rev/B` 改了 8 项：25、38、48、49、63、67、70、81。

## 冲突

Git 冲突两处，都在英文稿。两处都按 `revisions.md` 合并，没有拿不准的句子，没有插入 `\todo{合并待确认}`。

### 1. `english_paper/sections/introduction.tex`

位置：第 2.2 节，四类能力定义之后、第一类段落之前。英文 PDF 第 5 页，Figure 3。

双方改动：

- A（条目 18–21、19）：四类定义按本文用词写完后，直接进入第一类，并写明 BCD/STC 不能表示 base 与 disc 的相对位置和臂角。第四类需求段放在三类介绍之后。
- B（条目 25）：在四类定义后插入 `figure_cpp_class_quadrant.png`，没有图注，并紧接着写了一段 “Swing-arm troweling CPP requires both capabilities of the fourth class…”。B 这边的第一类段落仍是旧写法（point robot / disc robot / fixed-width tool）。

取舍：留下 A 的第一类段落和后文第四类结论。留下 B 的象限图，补上一句图注 “Four capability classes arranged by map representation and robot model.”，并让后文第四类那句指向 Fig. cpp-classes。删掉 B 那段与 A 重复的第四类开头。图是 2×2：横轴 regular map 到 complex map，纵轴 point or fixed footprint 到 base–arm–disc；四格为 Idealized、Map-enhanced、Platform-constrained、Environment–platform coupled。图注和像素一致。

### 2. `english_paper/sections/methodology.tex`

位置：3.5.2 “Starting Corner, Strip Width, and Swing Amplitude” 开头。英文 PDF 第 16 页，Figure 8。

双方改动：

- A（条目 64、65）：开头定义 swing amplitude \(\phi_w\) 和 work strip，并保持 \(\ell_R\) 是一条条带的行驶长度、\(h_R\) 是条带共同跨越的横向宽度。
- B（条目 63）：同一位置只插入 `figure_strip_geometry.png`，没有图注。B 的正文从 \(\ell_R\)、\(h_R\) 写起，没有 \(\phi_w\) 和 work strip 的定义。

取舍：留下 A 的定义，接上 B 的图，并补图注 “Entry pose, work strips, and swing amplitude \(\phi_w\) for one rectangle.”。图有三块：(a) 入口位姿 \(d_p+L\) 与 disc center，(b) 矩形上的 \(\ell_R\)、\(h_R\)、\(w_s\)、\(N_s\) 和 start，(c) \(\phi_w\)、\(-\phi_w\)、\(L\)、\(r_d\)、\(w_s\)。图注和像素一致。没有保留 B 那份缺定义的短段。

## 不是 Git 冲突、但合并时补上的对齐

- 条目 63 的第二张图、条目 67 的图：B 插入了 `figure_speed_coupling.png` 和 `figure_coverage_segments.png`，没有图注（`notes/DONE-B` 写明正文和图注未改）。按这两条“新画原理图”的要求各补了一句。第 17 页 Figure 9：半个摆程内 base 前进一个盘径，相邻扫掠相接。第 20 页 Figure 10：作业覆盖只计工作条带上的盘扫掠，全程覆盖再加上转移和调整段的扫掠。两句都与图内标注一致。
- 条目 70：B 把图内 `map_simple` / `parkingGraph` 改成 simple / complex，A 故意没改正文（条目 76 注明第 70 条是 B 类）。合并后图是新名字、句子仍是旧名字，对不上。英文正文、三张表、图注和结论里的 `map_test1`、`parkingGraph` 改成 `simple`、`complex`。数据文件名和实验数字没动。速度图文件名仍是 `figure_5b_vehicle_speed_parkingGraph_en.png`。三张方向图名 `scan_comb_corridors`、`scan_mixed_weave`、`scan_offset_rooms` 没动。英文 PDF 正文里已经没有这两个旧名字。中文 `sections/` 没人改过，仍写 `map_test1` 和 `parkingGraph`。
- 条目 49：B 核对过栅格图 (d) 的黑格与左侧几何相符，没有新画栅格，也没有改图注。图注保持 A 的一句（条目 50）。见第 10 页 Figure 5(d)。

## `\todo`

没有。英文稿和根目录稿的 `*.tex` 里都没有 `\todo`，也没有 `\todo{合并待确认}`。因此没有给 `\todo` 加定义。

## 修过的 bug

没有。

## 请重点看的页码

英文 PDF（`english_paper/build/main.pdf`，29 页）：

| 页 | 看什么 |
| --- | --- |
| 5 | 冲突 1。Figure 3 四类象限，图注一句。后面紧接 A 的第一类段落。 |
| 9 | 条目 38。Figure 4 流程第 4 框是 “global route planning”，不再是 Global Routing。图注是 “Workflow of BiRect.” |
| 10 | 条目 48、49。Figure 5 各子图标题在子图下方。请再看一眼 (d) 右下角黑格是否与左侧方块一致。 |
| 16 | 冲突 2。Figure 8 入口位姿、工作条带和 \(\phi_w\)。定义在图的前面。 |
| 17 | 条目 63。Figure 9 半摆程前进一个盘径。 |
| 20 | 条目 67。Figure 10 作业覆盖与全程覆盖。 |
| 23 | 条目 70。Figure 11 与表 2 用 simple / complex。图内标题、覆盖率 94.1% / 78.4% / 95.7% / 92.8% 与表中 94.11、78.40、95.73、92.84 对应。 |
| 27 | 条目 70、81。Figure 13 标题是 simple、complex。横轴从 \(\rho=0\) 起，第一个刻度仍是测得的 0.5 m/s（\(\rho=0.00556\)），0 上没有刻度，也没有补出来的单条带曲线。结论段同样使用 simple / complex。 |

根目录中文 PDF 没有这些新图。若要看中文稿里的旧地图名，打开 `build/main.pdf` 的实验节即可；那一部分这次没有改。

## 并入 rev/figs

`rev/merged` 从 `4616dcd` 快进到 `rev/figs`（`bf9d98b`）。中间只有两笔提交：`f05f697`（Redraw eight English figures to one journal style）和 `bf9d98b`（Fix the speed-coupling and coverage-segment diagrams）。没有冲突，图和脚本都是 `rev/figs` 这一侧。没有推送，也没有改 `main`。

八张重绘图换成矢量 PDF，正文 `\includegraphics` 已指向这些 PDF：

- `figure_cpp_class_quadrant.pdf`
- `figure_strip_geometry.pdf`
- `figure_speed_coupling.pdf`
- `figure_coverage_segments.pdf`
- `figure_2_coverage_comparison_en.pdf`
- `figure_5a_vehicle_speed_map_simple_en.pdf`
- `figure_5b_vehicle_speed_parkingGraph_en.pdf`
- `pipeline_overall_improved_en.pdf`

照片和 `rev/figs` 仍引用的 PNG/JPG 没有改成矢量：`figure_1_swing_arm_troweling_robot_photo.jpg`、`figure_2_disc_vehicle_relationships.png`、`figure_3_geometric_to_binary_raster.png`、`figure_3_segmentation_order_en.png`、`figure_4_body_arm_disc_model.png`、`figure_6_single_rectangle_coverage.png`。
