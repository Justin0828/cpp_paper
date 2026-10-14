"""Move Figure 4 subplot titles from above each panel to below it.

The panel artwork stays. Old title ink is cleared, including the light
antialiasing, and the same six strings are drawn under the panels. A few
descender pixels that sat on a grid stroke are restored to that stroke.
The SVG baselines move with the titles. Running again redraws the same labels.
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
SVG = ROOT / "assets" / "svg_sources" / "transfer.svg"
PNG = ROOT / "english_paper" / "figures" / "figure_3_geometric_to_binary_raster.png"
FONT = Path("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf")

TEXT = np.array([31, 41, 55], dtype=np.int16)
STROKE = np.array([75, 85, 99], dtype=np.int16)
# Pixel shift matching the SVG baseline move 34.5 -> 118 and 148.5 -> 232.
SHIFT = 378
SCALE_X = 2400 / 530

# (svg_x, source baseline y, text, fit width or None)
TITLES = (
    (88, 156, "(a) Axis-Aligned Rectangle", None),
    (265, 156, "(b) Curved Boundary", None),
    (442, 156, "(c) L-Shaped Region", None),
    (88, 672, "(d) L-Shaped Region with Multiple Obstacles", 667),
    (265, 672, "(e) Region with an Internal Obstacle", None),
    (442, 672, "(f) Irregular Multi-Obstacle Region", None),
)
WINDOWS = ((128, 167), (644, 684))


def _update_svg() -> None:
    text = SVG.read_text(encoding="utf-8")
    if 'y="34.5"' in text or 'y="148.5"' in text:
        text = text.replace('y="34.5"', 'y="118"').replace('y="148.5"', 'y="232"')
    if text.count('y="118"') != 3 or text.count('y="232"') != 3:
        raise SystemExit("SVG title baselines did not land on the six subplot titles")
    SVG.write_text(text, encoding="utf-8")


def _dilate(mask: np.ndarray, radius: int) -> np.ndarray:
    out = mask.copy()
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if max(abs(dy), abs(dx)) > radius:
                continue
            shifted = np.zeros_like(mask)
            y0 = max(0, dy)
            y1 = mask.shape[0] + min(0, dy)
            x0 = max(0, dx)
            x1 = mask.shape[1] + min(0, dx)
            shifted[y0:y1, x0:x1] = mask[y0 - dy:y1 - dy, x0 - dx:x1 - dx]
            out |= shifted
    return out


def _clear_old_titles(array: np.ndarray) -> np.ndarray:
    """Return the raster with subplot-title ink removed and panels unchanged."""
    original = array.copy()
    distance = np.linalg.norm(original.astype(np.int16) - TEXT, axis=2)
    exact = np.all(original == STROKE, axis=2)
    title = np.zeros(array.shape[:2], dtype=bool)
    # Windows cover the six subplot titles, including descenders, and not the
    # figure title or the legend.
    for y0, y1 in ((128, 172), (643, 692)):
        title[y0:y1] = distance[y0:y1] < 58
    title = _dilate(title, 2)
    # A pixel next to the grid stroke is panel ink unless it is the title core.
    near_stroke = _dilate(exact, 1)
    title &= ~near_stroke | (distance < 36)
    array[title & ~near_stroke] = 255
    array[title & near_stroke] = STROKE
    # Anything that was not title ink is copied back, so grid edges stay put.
    array[~title] = original[~title]
    # The grid's antialiased top is a uniform color. Put those pixels back even
    # when a descender was drawn over them, then fill any remaining text-colored
    # hole from the neighboring grid pixel.
    edge_colors = (
        (165, 169, 178),
        (107, 114, 128),
        (96, 105, 118),
        (104, 112, 125),
        (99, 107, 119),
        (78, 87, 101),
        (85, 95, 108),
    )
    grid = np.all(original == STROKE, axis=2)
    for color in edge_colors:
        match = np.all(original == color, axis=2)
        array[match] = color
        grid |= match
    white_now = np.all(array == 255, axis=2)
    was_text = distance < 36
    holes = white_now & was_text & _dilate(grid, 1)
    array[holes] = STROKE
    _fill_notches(array)
    return original


def _fill_notches(array: np.ndarray) -> None:
    """Close descender gaps that sit inside the dark top edge of a raster."""
    height, width = array.shape[:2]
    for _ in range(6):
        filled = 0
        for y in list(range(157, 166)) + list(range(673, 686)):
            for x in range(1, width - 1):
                if array[y, x].max() > 250 and array[y + 1, x].max() < 150:
                    if array[y, x - 1].max() < 150 or array[y, x + 1].max() < 150 or array[y - 1, x].max() < 150:
                        donors = []
                        for dy, dx in ((1, 0), (0, -1), (0, 1), (-1, 0)):
                            sample = array[y + dy, x + dx]
                            if sample.max() < 150:
                                donors.append(sample)
                        if donors:
                            array[y, x] = donors[0]
                            filled += 1
        if filled == 0:
            break


def _draw_titles(image: Image.Image) -> None:
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(FONT), 36)
    fill = (31, 41, 55)
    for svg_x, baseline, text, fit in TITLES:
        cx = svg_x * SCALE_X
        used = font
        if fit is not None:
            width = font.getbbox(text)[2] - font.getbbox(text)[0]
            size = max(8, int(round(36 * fit / width)))
            used = ImageFont.truetype(str(FONT), size)
        draw.text((cx, baseline + SHIFT), text, font=used, fill=fill, anchor="ms")


def main() -> None:
    _update_svg()
    image = Image.open(PNG).convert("RGB")
    if image.size != (2400, 1268):
        raise SystemExit(f"unexpected raster size {image.size}")
    array = np.array(image)
    distance = np.linalg.norm(array.astype(np.int16) - TEXT, axis=2)
    source = int((distance[128:172] < 36).sum() + (distance[643:692] < 36).sum())
    dest = int((distance[500:560] < 36).sum() + (distance[1000:1070] < 36).sum())
    if source < 200 and dest > 2000:
        print("titles already sit below the panels")
        print(PNG)
        return
    _clear_old_titles(array)
    cleaned = Image.fromarray(array, mode="RGB")
    _draw_titles(cleaned)
    cleaned.save(PNG)
    print(PNG)


if __name__ == "__main__":
    main()
