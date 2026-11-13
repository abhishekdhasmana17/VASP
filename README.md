# VASP Python Toolkit
### Python Utilities for VASP Post-Processing, Analysis, and Visualization

Welcome to the **VASP Python Toolkit**!

This repository is an evolving collection of Python scripts developed to simplify and automate common tasks associated with the Vienna Ab initio Simulation Package (VASP).

The primary goal of this project is to make VASP post-processing, data extraction, analysis, and visualization more efficient, reproducible, and accessible to researchers working in computational materials science, computational chemistry, and first-principles simulations.

I will continuously upload new Python scripts covering different aspects of VASP calculations, from extracting useful information from output files to generating publication-quality plots and visualizing atomic structures.

## Objectives

VASP calculations generate a substantial amount of computational data across files such as `OUTCAR`, `OSZICAR`, `CONTCAR`, `PROCAR`, `DOSCAR`, `EIGENVAL`, and `vasprun.xml`.

Extracting, organizing, interpreting, and visualizing this information can involve repetitive manual operations.

This repository aims to address these challenges through lightweight and practical Python tools that help researchers:

- Automate repetitive post-processing tasks.
- Extract relevant physical and chemical properties from VASP output files.
- Analyze electronic and structural properties.
- Visualize atomic configurations and structural evolution.
- Organize and process computational data.
- Generate figures and datasets for scientific publications.
- Improve the efficiency and reproducibility of computational workflows.

## Repository Contents

The repository will grow continuously as new scripts and utilities are developed.

Scripts will be organized into categories based on their primary applications.

| Category | Examples of planned utilities |
|---|---|
| Structural analysis | Structural comparison, bond distances, bond angles, coordination environments |
| Electronic structure | DOS, PDOS, band structures, Fermi-level analysis |
| Charge analysis | Bader charge extraction and charge-transfer analysis |
| Vibrational analysis | Phonon and vibrational-frequency data processing |
| Energy analysis | Total energy extraction, energy comparisons, adsorption energies |
| Surface and adsorption analysis | Adsorption configurations, binding energies, surface structures |
| Visualization | Atomic structure visualization, trajectory animations, plotting |
| Output-file processing | OUTCAR, OSZICAR, DOSCAR, PROCAR and vasprun.xml processing |
| Workflow automation | File organization, input generation, calculation monitoring and batch processing |
| Data analysis | Data extraction, comparison, statistical analysis and plotting |

*The categories above represent the intended scope of the repository; scripts will be added as they become available.*

## Available Scripts

### 1. VASP OUTCAR Trajectory GIF Generator

**Script:** `allgif.py`

A Python utility for combining one or more sequential VASP `OUTCAR` files and generating continuous GIF animations of atomic structural evolution.

**Features:**
- Supports single and multiple OUTCAR files.
- Automatically detects duplicate configurations at consecutive file boundaries.
- Checks atomic composition and ordering.
- Generates animations along X, Y, and Z viewing directions.
- Automatically cleans previous PNG frames in the selected viewing directory.
- Supports customizable GIF duration and output filenames.

**Example:**

```bash
python allgif.py ../../OUTCAR ../OUTCAR ./OUTCAR
```

See the script-specific documentation and usage examples for more details.

## Installation

Most scripts will use commonly available scientific Python libraries.

Typical dependencies include:

- Python
- NumPy
- Matplotlib
- ASE (Atomic Simulation Environment)
- SciPy
- Pandas
- Pillow
- ImageIO

Install the dependencies required by an individual script using its corresponding instructions.

Where appropriate, a `requirements.txt` file will be provided.

## General Usage

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Navigate to the repository:

```bash
cd YOUR_REPOSITORY
```

Run an individual script:

```bash
python script_name.py
```

Each script will include its own usage instructions, required dependencies, input-file requirements, and execution examples.

## Intended Users

This repository is intended for:

- Researchers using VASP for density functional theory calculations.
- PhD students and graduate researchers in computational materials science.
- Computational chemists and physicists.
- Researchers investigating heterogeneous catalysis, surface chemistry, adsorption, and electronic structures.
- Anyone interested in automating repetitive VASP post-processing tasks using Python.

## Contributions and Suggestions

This is a continuously developing project.

Suggestions for new scripts, improvements, bug reports, and contributions are welcome.

If you have a repetitive VASP post-processing task that could be automated, feel free to open an issue or submit a feature request.

## Development Philosophy

The focus of this repository is on practical, readable, and reusable scripts that address real challenges encountered during VASP calculations.

Whenever possible, scripts will include:

- Clear input and output specifications.
- Simple command-line execution.
- Comments explaining important operations.
- Error handling and input validation.
- Reproducible processing workflows.
- Examples demonstrating practical applications.

## Disclaimer

These scripts are provided as research utilities and are intended to assist with computational workflows.

Users are responsible for checking the validity of extracted data, computational settings, and scientific interpretations before using the results in research publications.

The scripts do not replace the need for appropriate convergence testing, physical validation, or careful interpretation of DFT results.

## License

This repository is distributed under the MIT License unless otherwise specified for an individual component.

---

**A growing collection of Python tools to make VASP post-processing, analysis, and visualization easier.**

*More scripts and utilities will be added over time.*
