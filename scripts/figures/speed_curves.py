"""Rebuild both speed-study panels. Colors stay in the style files."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from figure_5a_vehicle_speed_map_simple_en import main as draw_simple
from figure_5b_vehicle_speed_parkingGraph_en import main as draw_complex


def main() -> None:
    draw_simple()
    draw_complex()


if __name__ == "__main__":
    main()
