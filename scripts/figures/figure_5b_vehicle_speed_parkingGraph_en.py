"""Full-trajectory coverage and time on complex, from parkingGraph."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from speed_data import draw


def main() -> None:
    draw("complex", "figure_5b_vehicle_speed_parkingGraph_en.pdf")


if __name__ == "__main__":
    main()
