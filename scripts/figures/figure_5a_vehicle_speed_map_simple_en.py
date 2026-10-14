"""Full-trajectory coverage and time on simple, from map_test1."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from speed_data import draw


def main() -> None:
    draw("simple", "figure_5a_vehicle_speed_map_simple_en.pdf")


if __name__ == "__main__":
    main()
