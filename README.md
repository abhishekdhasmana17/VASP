# VASP OUTCAR Trajectory GIF Generator

A Python utility for visualizing atomic structural evolution recorded in VASP `OUTCAR` files. `allgif.py` reads one or more OUTCAR files, combines their ionic configurations in the supplied chronological order, and creates an animated GIF from the resulting trajectory.

## Features

- Reads a single OUTCAR or combines multiple sequential OUTCAR files.
- Removes an identical configuration at the boundary between consecutive files.
- Checks atom count and chemical-symbol ordering across all configurations.
- Creates separate frame directories and GIFs for X, Y, and Z viewing directions.
- Cleans old PNG frames in the selected view directory before rendering.
- Normalizes rendered frames to consistent pixel dimensions.
- Allows custom GIF filename and frame duration.
- Uses Matplotlib's non-interactive `Agg` backend for remote Linux/HPC environments.

## Repository contents

```text
vasp-outcar-trajectory-gif/
├── allgif.py
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

## Requirements and installation

Python 3.8 or newer is recommended. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Or install them directly:

```bash
python -m pip install ase numpy matplotlib pillow imageio
```

On a shared HPC system, install into an appropriate virtual environment or user environment if system-wide installation is unavailable.

## Basic usage

Run the script from the directory containing the script, or provide its path. Supply OUTCAR paths in chronological order.

### 1. Single-step / single-OUTCAR calculation

For a calculation whose trajectory is contained in one OUTCAR:

```bash
python allgif.py ./OUTCAR
```

This uses the default Z view and creates:

```text
z_frames/
outcar_z.gif
```

### 2. Two-step calculation

Example directory structure:

```text
Calculation/
├── Step_1/
│   └── OUTCAR
└── Step_2/
    └── OUTCAR
```

Run from `Step_2`:

```bash
python allgif.py ../Step_1/OUTCAR ./OUTCAR
```

The two trajectories are concatenated in the order supplied.

### 3. Three-step calculation

Example directory structure:

```text
Calculation/
├── Step_1/
│   └── OUTCAR
├── Step_2/
│   └── OUTCAR
└── Step_3/
    └── OUTCAR
```

Run from `Step_3`:

```bash
python allgif.py ../../Step_1/OUTCAR ../Step_2/OUTCAR ./OUTCAR
```

### 4. More than three OUTCAR files

Add as many paths as required, keeping them in chronological order:

```bash
python allgif.py ../../../Step_1/OUTCAR ../../Step_2/OUTCAR ../Step_3/OUTCAR ./OUTCAR
```

## Viewing directions and output organization

The default viewing direction is Z. The script uses a separate frame directory and default GIF name for each view.

| Command | Frame directory | Default GIF |
|---|---|---|
| `python allgif.py ./OUTCAR --view x` | `x_frames/` | `outcar_x.gif` |
| `python allgif.py ./OUTCAR --view y` | `y_frames/` | `outcar_y.gif` |
| `python allgif.py ./OUTCAR --view z` | `z_frames/` | `outcar_z.gif` |
| `python allgif.py ./OUTCAR` | `z_frames/` | `outcar_z.gif` |

For the same multi-file trajectory, generate all three views with:

```bash
python allgif.py ../../Step_1/OUTCAR ../Step_2/OUTCAR ./OUTCAR --view x
python allgif.py ../../Step_1/OUTCAR ../Step_2/OUTCAR ./OUTCAR --view y
python allgif.py ../../Step_1/OUTCAR ../Step_2/OUTCAR ./OUTCAR --view z
```

Changing the view changes the rendered camera orientation; it does not modify atomic coordinates.

## Animation speed

`--duration` sets the display duration of each GIF frame in seconds. It changes playback speed, not the physical time interval between ionic steps.

```bash
# Fast playback
python allgif.py ./OUTCAR --duration 0.2

# Moderate playback
python allgif.py ./OUTCAR --duration 0.5

# Slow playback for inspection
python allgif.py ./OUTCAR --duration 1.0
```

The default is `0.5` seconds per frame.

## Custom output filename

Use `--output` to override the default GIF filename:

```bash
python allgif.py ./OUTCAR --view x --output relaxation_x.gif
```

The frame directory remains `x_frames/`; only the GIF filename changes.

## Combined command examples

```bash
# Three OUTCAR files, X view, fast playback
python allgif.py ../../Step_1/OUTCAR ../Step_2/OUTCAR ./OUTCAR --view x --duration 0.3

# Two OUTCAR files, Y view, slow playback
python allgif.py ../Step_1/OUTCAR ./OUTCAR --view y --duration 1.0

# Three OUTCAR files, Z view, custom GIF name
python allgif.py ../../Step_1/OUTCAR ../Step_2/OUTCAR ./OUTCAR --view z --output final_relaxation.gif

# Show command-line help
python allgif.py --help
```

## Command-line reference

| Argument | Required? | Description | Default |
|---|---:|---|---|
| `outcars` | Yes | One or more OUTCAR paths, in chronological order | None |
| `--view {x,y,z}` | No | Viewing direction | `z` |
| `--output OUTPUT` | No | Custom output GIF filename | `outcar_<view>.gif` |
| `--duration SECONDS` | No | Duration per frame in seconds; must be positive | `0.5` |
| `-h`, `--help` | No | Display help | — |

## Frame cleanup behavior

Before rendering, the script removes existing `.png` files directly inside the selected view directory:

- `--view x` cleans PNG files in `x_frames/`.
- `--view y` cleans PNG files in `y_frames/`.
- `--view z`, or no `--view` argument, cleans PNG files in `z_frames/`.

Other view directories, non-PNG files, and subdirectories are preserved. The script does not delete an existing GIF before writing the new GIF.

## Scientific and technical considerations

1. **Chronological ordering:** The script does not infer calculation order. Supply the earliest OUTCAR first and the latest OUTCAR last.
2. **Structural compatibility:** All configurations must have the same atom count and chemical-symbol ordering. This is a consistency check, not a complete validation of the physical continuity of the calculations.
3. **Boundary duplicate removal:** Only the first configuration of a file is compared with the final configuration already collected from the preceding file. A frame is removed only if atom ordering, positions, and cell match within the specified numerical tolerance.
4. **No interpolation:** The script concatenates configurations recorded in OUTCAR files. It does not reconstruct missing ionic steps or interpolate between structures.
5. **Trajectory interpretation:** For geometry optimization, the animation shows the sequence of ionic relaxation configurations. It should not be described as molecular dynamics unless the underlying VASP calculation was an MD calculation.
6. **Rendering cost:** High-resolution rendering (2100 × 1800 pixels, 300 DPI) can require substantial CPU time and storage for long trajectories.

## Troubleshooting

**`ModuleNotFoundError`**

Install the missing package in the Python environment used to execute the script:

```bash
python -m pip install -r requirements.txt
```

**No OUTCAR file found**

Check the relative paths and current working directory. For example:

```bash
pwd
ls -l ../OUTCAR
```

**Atomic composition or ordering mismatch**

Confirm that the OUTCAR files belong to the same system and use the same POSCAR/POTCAR atom ordering. Do not concatenate trajectories with different atom counts or atom orderings.

**GIF frames have inconsistent dimensions**

The script normalizes every rendered image to the same target pixel dimensions before GIF assembly.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE).

## Contributions

Bug reports, suggestions, and pull requests are welcome.

---

A lightweight visualization utility for researchers using VASP, ASE, and atomistic simulations.
