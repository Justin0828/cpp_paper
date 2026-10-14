"""Rename in-figure map titles on the coverage comparison (revision 70).

Only the first line of each panel changes. The coverage line, the masks,
and the legend stay. map_simple becomes simple and parkingGraph becomes
complex. scan map names are not in this figure.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from paper_style import figures_dir


# Inclusive boxes around the first title line only. The coverage line begins
# at y=37 on the top row and y=629 on the bottom row.
_TITLES = (
    ((240, 9, 539, 33), (389.5, 28), "(a) simple, proposed"),
    ((968, 9, 1323, 35), (1140.5, 28), "(b) simple, Fields2Cover"),
    ((78, 600, 397, 625), (237.5, 620), "(c) complex, proposed"),
    ((807, 600, 1171, 626), (989.0, 620), "(d) complex, Fields2Cover"),
)
_FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
_SIZE = 24
_BG = (254, 254, 254)


def _already(image: Image.Image, font: ImageFont.FreeTypeFont) -> bool:
    """True when the new titles are present and the old names are gone."""
    # A second run whitens these same boxes and redraws the same glyphs.
    probe = image.copy()
    _paint(probe, font)
    return np.array_equal(np.asarray(probe), np.asarray(image))


def _paint(image: Image.Image, font: ImageFont.FreeTypeFont) -> None:
    draw = ImageDraw.Draw(image)
    for (x0, y0, x1, y1), (cx, baseline), text in _TITLES:
        draw.rectangle((x0, y0, x1, y1), fill=_BG)
        draw.text((cx, baseline), text, font=font, fill=(0, 0, 0), anchor="ms")


def main() -> None:
    path = figures_dir() / "figure_2_coverage_comparison_en.png"
    image = Image.open(path).convert("RGB")
    before = np.asarray(image)
    font = ImageFont.truetype(_FONT, _SIZE)
    if _already(image, font):
        print(f"titles already renamed: {path}")
        return
    # Coverage lines sit directly under the titles and must not move.
    coverage = (
        before[37:56, 180:700].copy(),
        before[37:56, 900:1330].copy(),
        before[629:650, 40:700].copy(),
        before[629:656, 760:1336].copy(),
    )
    outside = before.copy()
    _paint(image, font)
    after = np.asarray(image)
    for box, _, _ in _TITLES:
        x0, y0, x1, y1 = box
        outside[y0 : y1 + 1, x0 : x1 + 1] = after[y0 : y1 + 1, x0 : x1 + 1]
    if not np.array_equal(outside, after):
        raise SystemExit("pixels outside the title boxes changed")
    kept = (
        after[37:56, 180:700],
        after[37:56, 900:1330],
        after[629:650, 40:700],
        after[629:656, 760:1336],
    )
    for index, (old, new) in enumerate(zip(coverage, kept)):
        if not np.array_equal(old, new):
            raise SystemExit(f"coverage line {index} changed")
    image.save(path)
    print(path)


if __name__ == "__main__":
    main()
