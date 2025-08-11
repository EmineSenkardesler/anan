## Love Heart Animation and Viewer

This project includes two simple Python scripts:

- `animate_love.py`: Prints `hellpworks`, displays a heart outline with a small ball moving along its edge, shows the message “I love my husband”, and saves the heart boundary coordinates to `heart_edge_coordinates.txt`.
- `view_heart_from_txt.py`: Reads `heart_edge_coordinates.txt` and visualizes the heart outline.

### Setup (macOS / zsh)

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Run the animation and save coordinates

```sh
python animate_love.py --points 1200 --output heart_edge_coordinates.txt
```

The window will open with the animation. Close the window to end the program. The coordinates are saved as CSV text to `heart_edge_coordinates.txt`.

### View the saved heart outline

```sh
python view_heart_from_txt.py --input heart_edge_coordinates.txt --style line
```

Options for the viewer:

- `--style`: `line`, `points`, or `both` (default: `line`)
- `--message`: Custom text to display on the figure


