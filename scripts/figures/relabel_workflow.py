"""Replace the stage-4 header “Global Routing” with “global route planning”.

Only that header line is repainted. The module boxes and every other label
stay on the existing raster. The SVG text is updated to the same words.
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
SVG = ROOT / "assets" / "svg_sources" / "pipeline_overall_improved_en.svg"
PNG = ROOT / "english_paper" / "figures" / "pipeline_overall_improved_en.png"
FONT = Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf")

OLD = "4. Global Routing &amp;"
NEW = "4. global route planning &amp;"
# Header band of stage 4, first line only. Measured on the 1400×760 raster:
# white glyphs sit in y=437..451; the second line starts at y=463.
BAND = (730, 432, 990, 458)  # x0, y0, x1, y1
CENTER = (857.5, 446)


def _update_svg() -> None:
    text = SVG.read_text(encoding="utf-8")
    if NEW in text and OLD not in text:
        return
    if OLD not in text:
        raise SystemExit(f"workflow SVG is missing both {OLD!r} and {NEW!r}")
    text = text.replace(
        f'<text class="title-small" x="857.5" y="452" style="font-size:20px">{OLD}</text>',
        f'<text class="title-small" x="857.5" y="452" style="font-size:18px">{NEW}</text>',
        1,
    )
    if NEW not in text:
        raise SystemExit("SVG replacement did not land")
    SVG.write_text(text, encoding="utf-8")


def _relabel_png() -> None:
    image = Image.open(PNG).convert("RGB")
    before = np.array(image)
    x0, y0, x1, y1 = BAND
    fill = tuple(int(v) for v in before[430, 720])
    if fill != (23, 59, 94):
        raise SystemExit(f"unexpected header color {fill}")
    draw = ImageDraw.Draw(image)
    draw.rectangle(BAND, fill=fill)
    font = ImageFont.truetype(str(FONT), 18)
    draw.text(CENTER, "4. global route planning &", font=font, fill=(255, 255, 255), anchor="mm")
    after = np.array(image)
    outside = np.ones(before.shape[:2], dtype=bool)
    outside[y0:y1, x0:x1] = False
    changed = np.any(before != after, axis=2) & outside
    if int(changed.sum()):
        raise SystemExit(f"pixels outside the header band changed: {int(changed.sum())}")
    image.save(PNG)
    print(PNG)


def main() -> None:
    _update_svg()
    _relabel_png()


if __name__ == "__main__":
    main()
