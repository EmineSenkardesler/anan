"""
Visualize heart edge coordinates from a CSV text file produced by animate_love.py.

Usage:
  python view_heart_from_txt.py
  python view_heart_from_txt.py --input heart_edge_coordinates.txt --style both --message "I love you"

File format expected (CSV):
  x,y
  <x0>,<y0>
  <x1>,<y1>
  ...
"""

from __future__ import annotations

import argparse
from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt


def read_coordinates_from_txt(file_path: str) -> Tuple[np.ndarray, np.ndarray]:
    """Read x,y coordinates from a CSV .txt file with a one-line header."""
    try:
        data = np.loadtxt(file_path, delimiter=",", skiprows=1)
    except OSError as error:
        raise SystemExit(f"Could not read file '{file_path}': {error}")

    if data.ndim == 1:
        # Single row case
        if data.size != 2:
            raise SystemExit("Invalid data format: expected two columns x,y")
        data = data.reshape(1, 2)

    if data.shape[1] != 2:
        raise SystemExit("Invalid data format: expected two columns x,y")

    x = data[:, 0]
    y = data[:, 1]
    return x, y


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Visualize saved heart edge coordinates from a text file.")
    parser.add_argument(
        "--input",
        type=str,
        default="heart_edge_coordinates.txt",
        help='Path to the coordinates text file (default: "heart_edge_coordinates.txt")',
    )
    parser.add_argument(
        "--style",
        type=str,
        choices=["line", "points", "both"],
        default="line",
        help="How to display the heart: line, points, or both (default: line)",
    )
    parser.add_argument(
        "--message",
        type=str,
        default="I love my husband",
        help="Optional message to display on the figure (default: 'I love my husband')",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    x, y = read_coordinates_from_txt(args.input)

    figure, axes = plt.subplots(figsize=(6.5, 6.5))
    axes.set_aspect("equal", adjustable="box")
    axes.axis("off")

    # Compute bounds with a margin
    margin = 3.0
    xmin, xmax = float(np.min(x)) - margin, float(np.max(x)) + margin
    ymin, ymax = float(np.min(y)) - margin, float(np.max(y)) + margin
    axes.set_xlim(xmin, xmax)
    axes.set_ylim(ymin, ymax)

    # Draw according to chosen style
    if args.style in ("line", "both"):
        axes.plot(x, y, color="crimson", linewidth=2.5)
    if args.style in ("points", "both"):
        axes.scatter(x, y, color="crimson", s=10, alpha=0.9)

    # Add optional message centered a bit above the horizontal middle
    axes.text(
        (xmin + xmax) / 2.0,
        ymin + 0.18 * (ymax - ymin),
        args.message,
        ha="center",
        va="center",
        fontsize=18,
        color="darkred",
        fontweight="bold",
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()


