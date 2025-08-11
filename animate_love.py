"""
Animate a heart with a moving ball, display a loving message, and save
the heart edge coordinates to a text file for later sharing.

Behavior:
- Prints "hellpworks" to the console.
- Shows an animation: a red heart outline with a small ball moving along its edge.
- Displays the text "I love my husband" centered on the heart.
- Saves the heart boundary coordinates to `heart_edge_coordinates.txt` (CSV format).

Usage:
  python animate_love.py

Optional:dasdsd
  python animate_love.py --points 1200 --output heart_edge_coordinates.txt
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle


@dataclass(frozen=True)
class HeartData:
    x: np.ndarray
    y: np.ndarray


def generate_heart_coordinates(num_points: int) -> HeartData:
    """Generate parametric heart curve coordinates.

    Uses the classic parametric heart ("sin^3" heart):
      x(t) = 16 sin^3(t)
      y(t) = 13 cos(t) - 5 cos(2t) - 2 cos(3t) - cos(4t)

    Args:
        num_points: Number of samples along the curve (higher -> smoother).

    Returns:
        HeartData with arrays x, y (closed curve included as last point equals first).
    """
    # Use endpoint=False to avoid duplicating start point for animation loop.
    theta = np.linspace(0.0, 2.0 * np.pi, num_points, endpoint=False)
    x = 16.0 * np.sin(theta) ** 3
    y = (
        13.0 * np.cos(theta)
        - 5.0 * np.cos(2.0 * theta)
        - 2.0 * np.cos(3.0 * theta)
        - np.cos(4.0 * theta)
    )

    return HeartData(x=x, y=y)


def save_coordinates_to_txt(file_path: str, x: np.ndarray, y: np.ndarray) -> None:
    """Save coordinates to a CSV-formatted .txt file with header.

    The file format is:
        x,y\n
        <x0>,<y0>\n
        <x1>,<y1>\n
        ...

    Args:
        file_path: Destination file path (e.g., "heart_edge_coordinates.txt").
        x: X-coordinates array.
        y: Y-coordinates array.
    """
    # For a closed boundary, append the first point to the end
    x_closed = np.concatenate([x, x[:1]])
    y_closed = np.concatenate([y, y[:1]])
    data = np.column_stack((x_closed, y_closed))
    # Save without a leading comment marker so the header is plain text
    np.savetxt(
        file_path,
        data,
        delimiter=",",
        header="x,y",
        comments="",
        fmt="%.6f",
    )


def create_animation(x: np.ndarray, y: np.ndarray, title_text: str = "I love my husband") -> None:
    """Create and display the heart animation with a moving ball and title text."""
    figure, axes = plt.subplots(figsize=(6.5, 6.5))
    axes.set_aspect("equal", adjustable="box")
    axes.axis("off")

    # Determine nice limits with margin
    margin = 3.0
    xmin, xmax = float(np.min(x)) - margin, float(np.max(x)) + margin
    ymin, ymax = float(np.min(y)) - margin, float(np.max(y)) + margin
    axes.set_xlim(xmin, xmax)
    axes.set_ylim(ymin, ymax)

    # Plot the heart outline
    axes.plot(x, y, color="crimson", linewidth=2.5)

    # Add the loving message roughly near the center
    axes.text(
        0.0,
        ymin + 0.18 * (ymax - ymin),  # place a bit above bottom for aesthetics
        title_text,
        ha="center",
        va="center",
        fontsize=18,
        color="darkred",
        fontweight="bold",
    )

    # Ball settings
    max_range = max(xmax - xmin, ymax - ymin)
    ball_radius = 0.03 * max_range
    ball = Circle((x[0], y[0]), radius=ball_radius, color="goldenrod", ec="black", lw=0.8, zorder=5)
    axes.add_patch(ball)

    # Animation update logic
    total_frames = len(x)

    def init() -> Tuple[Circle]:
        ball.center = (x[0], y[0])
        return (ball,)

    def update(frame_index: int) -> Tuple[Circle]:
        idx = frame_index % total_frames
        ball.center = (x[idx], y[idx])
        return (ball,)

    animation.FuncAnimation(
        figure,
        update,
        init_func=init,
        frames=total_frames,
        interval=20,  # milliseconds between frames (~50 FPS)
        blit=True,
        repeat=True,
    )

    plt.tight_layout()
    plt.show()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Animate a heart and save its edge coordinates to a text file.")
    parser.add_argument(
        "--points",
        type=int,
        default=1000,
        help="Number of points along the heart boundary (default: 1000)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="heart_edge_coordinates.txt",
        help='Output text file to save coordinates (default: "heart_edge_coordinates.txt")',
    )
    return parser.parse_args()


def main() -> None:
    print("hellpworks")
    arguments = parse_args()

    heart = generate_heart_coordinates(num_points=arguments.points)
    save_coordinates_to_txt(arguments.output, heart.x, heart.y)

    create_animation(heart.x, heart.y, title_text="I love my husband")


if __name__ == "__main__":
    main()


