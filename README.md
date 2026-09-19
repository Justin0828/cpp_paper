# cpp_paper

这是从 Coverage_Path_Planning 项目迁移出的中文 LaTeX 论文草稿。

## 编译

在本目录运行：

```bash
latexmk -xelatex -shell-escape -outdir=build main.tex
```

输出文件为 `build/main.pdf`。正文已按逻辑拆分为 `sections/intro.tex`、`method.tex`、`experiments.tex` 和 `conclusion.tex`，由 `main.tex` 统一组装；图片位于 `figures/`，参考文献位于 `refs.bib`。`sections/*.md` 和 `sections/abstract.md` 是修订用 Markdown 稿；核对后将章节内容同步到同名 `.tex` 文件，并将摘要同步到 `main.tex`。章节 `.tex` 文件继续使用 Markdown 语法，以保留原稿的中文、公式、图表和表格；LaTeX 的 `markdown` 宏包负责排版。`-shell-escape` 仅用于调用 TeX Live 自带的 Markdown 转换器。

## 目录说明

- `sections/`：当前论文正文源文件。
- `figures/`：当前编译使用的位图图件。
- `assets/svg_sources/`：未直接参与编译、但可用于后续修改图件的 SVG 源素材。
- `build/`：LaTeX 编译输出；以其中的 `main.pdf` 为当前论文版本。
- `archive/legacy/`：不参与编译的历史单文件草稿与旧 PDF，仅供追溯。
