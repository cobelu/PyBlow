# PyBlow

Generate 3D STL models of blown acrylic bubbles for manufacturing and design.

PyBlow models the shape of a heated acrylic sheet that has been blown with air into a bubble. The tool generates accurate STL files suitable for 3D printing, CAD, or manufacturing reference.

## Installation

```bash
python3 -m venv .venv
source ./.venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

### Interactive Mode

Run the script and answer the prompts:

```bash
python3 main.py
```

### Command Line Mode

Specify all parameters directly:

```bash
python3 main.py --length 96 --width 48 --height 12 --resolution 50 --output bubble.stl
```

### Parameters

- `--length`: Sheet length in inches (default: 96" for 8 feet)
- `--width`: Sheet width in inches (default: 48" for 4 feet)
- `--height`: Maximum bubble height at center in inches (default: 12")
- `--resolution`: Mesh resolution, points per side (default: 50)
- `--output`: Output STL filename (default: bubble.stl)

### Examples

Standard 4'x8' sheet with 12" bubble:
```bash
python3 main.py --length 96 --width 48 --height 12 --resolution 50 --output standard.stl
```

Smaller sheet with shallow bubble:
```bash
python3 main.py --length 48 --width 24 --height 6 --resolution 40 --output small.stl
```

High-resolution mesh:
```bash
python3 main.py --length 96 --width 48 --height 12 --resolution 100 --output high_res.stl
```

## How It Works

PyBlow uses an ellipsoidal cap model to simulate the physics of a blown acrylic sheet:

- The base represents the clamped edges of the sheet (z=0)
- Height follows the formula: `z = h × √(1 - (x/a)² - (y/b)²)`
- Creates a structured triangular mesh (not point cloud reconstruction)
- Exports directly to STL format

## Development

Format code with black:
```bash
python3 -m black main.py
```

Lint with ruff:
```bash
python3 -m ruff check main.py
```
