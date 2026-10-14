"""Set pipeline box 4's title and re-export the included PDF."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import cairosvg

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tikzfig import FIGURES, ROOT


SVG = ROOT / "assets" / "svg_sources" / "pipeline_overall_improved_en.svg"
TITLE = "4. Global Route Planning & Rectangle Coverage"
CANONICAL = (
    '<text class="title-small" x="857.5" y="452" style="font-size:18px">'
    '<tspan x="857.5" y="452">4. Global Route Planning &amp;</tspan>'
    '<tspan x="857.5" y="477"> Rectangle Coverage</tspan></text>'
)
BOX4 = re.compile(
    r'<text class="title-small" x="857\.5" y="452".*?</text>'
    r'(?:\s*<text class="title-small" x="857\.5" y="477".*?</text>)?',
    re.S,
)


def visible_text(fragment: str) -> str:
    plain = re.sub(r"<[^>]+>", "", fragment)
    plain = plain.replace("&amp;", "&")
    return re.sub(r"\s+", " ", plain).strip()


def rewrite(svg: str) -> str:
    match = BOX4.search(svg)
    if match is None:
        raise SystemExit("box 4 title element was not found")
    updated = BOX4.sub(CANONICAL, svg, count=1)
    if visible_text(CANONICAL) != TITLE:
        raise SystemExit("canonical title text does not match the required string")
    if updated.count('class="title-small"') < 4:
        raise SystemExit("title-small class is no longer shared by the four boxes")
    weight = re.search(r"\.title-small\s*\{[^}]*font-weight:\s*(\d+)", updated)
    weights = re.findall(r"\.title(?:-small)?\s*\{[^}]*font-weight:\s*(\d+)", updated)
    if weight is None or len(set(weights)) != 1:
        raise SystemExit(f"box title weights diverged: {weights}")
    return updated


def _lower_subscripts(text: str) -> str:
    """cairosvg ignores baseline-shift, so subscripts are lowered with dy."""

    def replace(match: re.Match[str]) -> str:
        size = int(match.group(1) or "11")
        drop = max(3, round(size * 0.32))
        body = match.group(2)
        follow = match.group(3)
        lowered = f'<tspan dy="{drop}" font-size="{size}">{body}</tspan>'
        if follow:
            lowered += f'<tspan dy="-{drop}">{follow}</tspan>'
        return lowered

    return re.sub(
        r'<tspan baseline-shift="sub"(?: font-size="(\d+)")?>(.*?)</tspan>([^<]*)',
        replace,
        text,
    )


def export_source(svg_path: Path) -> str:
    """Render with installed faces. The SVG source keeps Arial and Cambria Math.

    A tspan with font-style italic gets a zero advance in cairosvg, so the
    italic face is embedded as its own family and used with font-style normal.
    """
    import base64

    italic = base64.b64encode(
        Path("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf").read_bytes()
    ).decode("ascii")
    text = svg_path.read_text(encoding="utf-8")
    text = text.replace("Arial,", "Liberation Sans,")
    face = (
        "@font-face { font-family: 'PaperMath'; "
        f"src: url('data:font/ttf;base64,{italic}'); "
        "font-style: normal; font-weight: 400; }\n      "
    )
    text = text.replace("<style>", "<style>\n      " + face, 1)
    text = text.replace(
        "font-family: 'Cambria Math', Cambria, serif;",
        "font-family: 'PaperMath', serif;",
    )
    text = text.replace("font-style: italic;", "font-style: normal;")
    text = re.sub(r"<tspan class=\"math\">(.*?)</tspan>", r"\1", text)
    text = text.replace(
        "(R\u1d62,R\u2c7c)",
        '(R<tspan dy="3" font-size="9">i</tspan><tspan dy="-3">,R</tspan>'
        '<tspan dy="3" font-size="9">j</tspan><tspan dy="-3">)</tspan>',
    )
    text = _lower_subscripts(text)
    return _start_anchor_formula(text)


def _start_anchor_formula(text: str) -> str:
    """Middle anchor plus a tspan mis-measures the line, so the formula is placed from the left."""
    from PIL import ImageFont

    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
        15,
    )
    visible = "Tcover(R), Ttransit(R\u1d62,R\u1d63)"
    x = 502.5 - font.getlength(visible) / 2.0
    old = '<text class="formula" x="502.5" y="671">'
    new = f'<text class="formula" x="{x:.2f}" y="671" style="text-anchor: start">'
    if old not in text:
        raise SystemExit("formula element was not found for anchor correction")
    return text.replace(old, new, 1)


def export_pdf(svg_text: str, dest: Path) -> None:
    work = dest.parent / f".build-{dest.stem}"
    work.mkdir(parents=True, exist_ok=True)
    styled = work / "styled.svg"
    styled.write_text(svg_text, encoding="utf-8")
    native = work / "native.pdf"
    cairosvg.svg2pdf(url=str(styled), write_to=str(native))
    tex = work / "wrap.tex"
    tex.write_text(
        "\n".join(
            [
                r"\documentclass[border=0pt]{standalone}",
                r"\usepackage{graphicx}",
                r"\begin{document}",
                r"\includegraphics[width=455.24411pt]{native.pdf}",
                r"\end{document}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "wrap.tex"],
        cwd=work,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    dest.write_bytes((work / "wrap.pdf").read_bytes())


def main() -> None:
    original = SVG.read_text(encoding="utf-8")
    updated = rewrite(original)
    if updated != original:
        SVG.write_text(updated, encoding="utf-8")
    styled = export_source(SVG)
    png = FIGURES / "pipeline_overall_improved_en.png"
    cairosvg.svg2png(
        bytestring=styled.encode("utf-8"),
        write_to=str(png),
        output_width=1400,
        output_height=760,
    )
    pdf = FIGURES / "pipeline_overall_improved_en.pdf"
    export_pdf(styled, pdf)
    print(pdf)
    print("DATA pipeline title=" + visible_text(CANONICAL))


if __name__ == "__main__":
    main()
