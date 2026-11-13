import os
import argparse
import numpy as np
import matplotlib

# Headless plotting for remote Linux/HPC environments
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import imageio.v2 as imageio

from PIL import Image, ImageOps
from ase.io import read
from ase.visualize.plot import plot_atoms


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

FRAME_SIZE = (2100, 1800)
DPI = 300

VIEW_ROTATIONS = {
    "x": "0x,90y,0z",
    "y": "90x,0y,0z",
    "z": "0x,0y,0z"
}


# ---------------------------------------------------------
# Compare two atomic configurations
# ---------------------------------------------------------

def structures_match(atoms1, atoms2, tolerance=1e-5):
    """Return True if atom order, positions, and cell match."""
    if len(atoms1) != len(atoms2):
        return False

    if atoms1.get_chemical_symbols() != atoms2.get_chemical_symbols():
        return False

    if not np.allclose(
        atoms1.positions, atoms2.positions,
        atol=tolerance, rtol=0
    ):
        return False

    if not np.allclose(
        atoms1.cell, atoms2.cell,
        atol=tolerance, rtol=0
    ):
        return False

    return True


# ---------------------------------------------------------
# Read and combine one or more OUTCAR files
# ---------------------------------------------------------

def combine_outcars(outcar_files):
    """Read OUTCAR files in supplied order and concatenate configurations."""
    all_images = []
    reference_symbols = None

    for file_number, outcar in enumerate(outcar_files, start=1):
        if not os.path.isfile(outcar):
            raise FileNotFoundError(f"OUTCAR file not found: {outcar}")

        print(
            f"\nReading OUTCAR {file_number}/{len(outcar_files)}: "
            f"{outcar}"
        )

        images = read(outcar, index=":", format="vasp-out")

        if len(images) == 0:
            raise ValueError(f"No ionic configurations found in {outcar}")

        print(f"  Configurations found: {len(images)}")

        # Check atom count and chemical-symbol ordering in every frame.
        for atoms in images:
            symbols = atoms.get_chemical_symbols()

            if reference_symbols is None:
                reference_symbols = symbols
            elif symbols != reference_symbols:
                raise ValueError(
                    "Atomic composition or ordering mismatch "
                    f"in {outcar}"
                )

        # Remove only an identical boundary frame between adjacent files.
        if all_images and structures_match(all_images[-1], images[0]):
            print(
                "  Duplicate boundary configuration detected; "
                "removing the first frame of this OUTCAR."
            )
            images = images[1:]

        all_images.extend(images)
        print(f"  Total configurations collected: {len(all_images)}")

    print("\n----------------------------------------")
    print(f"Total ionic configurations: {len(all_images)}")
    print("----------------------------------------\n")

    return all_images


# ---------------------------------------------------------
# Clean selected frame directory
# ---------------------------------------------------------

def clean_frame_directory(frame_dir):
    """
    Remove PNG files directly inside the selected view directory.
    Preserve subdirectories and all non-PNG files.
    """
    if os.path.isdir(frame_dir):
        print(f"\nCleaning existing frame directory: {frame_dir}")

        removed = 0
        for filename in os.listdir(frame_dir):
            file_path = os.path.join(frame_dir, filename)

            if (
                os.path.isfile(file_path)
                and filename.lower().endswith(".png")
            ):
                os.remove(file_path)
                removed += 1

        print(f"Removed {removed} old PNG frame(s).")
    else:
        os.makedirs(frame_dir, exist_ok=True)
        print(f"\nCreated frame directory: {frame_dir}")


# ---------------------------------------------------------
# Generate GIF frames
# ---------------------------------------------------------

def generate_frames(images, rotation, frame_dir):
    os.makedirs(frame_dir, exist_ok=True)

    gif_frames = []
    total_frames = len(images)

    for i, atoms in enumerate(images):
        fig, ax = plt.subplots(figsize=(7, 6))

        try:
            plot_atoms(
                atoms,
                ax,
                rotation=rotation,
                show_unit_cell=2
            )
            ax.set_axis_off()

            frame_path = os.path.join(
                frame_dir,
                f"frame_{i:05d}.png"
            )

            fig.savefig(
                frame_path,
                dpi=DPI,
                bbox_inches=None,
                facecolor="white"
            )
        finally:
            plt.close(fig)

        # Normalize every frame to identical pixel dimensions.
        with Image.open(frame_path) as source:
            img = source.convert("RGB")
            img = ImageOps.pad(
                img,
                FRAME_SIZE,
                method=Image.LANCZOS,
                color="white"
            )
            gif_frames.append(np.array(img))

        if (i + 1) % 10 == 0 or (i + 1) == total_frames:
            percentage = 100.0 * (i + 1) / total_frames
            print(
                f"Rendering: {i + 1}/{total_frames} "
                f"({percentage:.1f}%)"
            )

    return gif_frames


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Combine one or more sequential VASP OUTCAR files "
            "and generate an animated GIF."
        )
    )

    parser.add_argument(
        "outcars",
        nargs="+",
        help="One or more OUTCAR files in chronological order"
    )

    parser.add_argument(
        "--view",
        choices=["x", "y", "z"],
        default="z",
        help="Viewing direction (default: z)"
    )

    parser.add_argument(
        "--output",
        default=None,
        help=(
            "Custom GIF filename. By default, the name is "
            "outcar_x.gif, outcar_y.gif, or outcar_z.gif."
        )
    )

    parser.add_argument(
        "--duration",
        type=float,
        default=0.5,
        help="Duration of each GIF frame in seconds (default: 0.5)"
    )

    args = parser.parse_args()

    if args.duration <= 0:
        parser.error("--duration must be greater than zero.")

    view = args.view
    frame_dir = f"{view}_frames"
    output_gif = args.output or f"outcar_{view}.gif"
    rotation = VIEW_ROTATIONS[view]

    print("\n========================================")
    print("       VASP OUTCAR GIF GENERATOR")
    print("========================================")
    print(f"Number of OUTCAR files: {len(args.outcars)}")
    print(f"Viewing direction: {view.upper()}")
    print(f"Frame directory: {frame_dir}")
    print(f"Output GIF: {output_gif}")

    # 1. Read and combine the trajectory.
    images = combine_outcars(args.outcars)

    if not images:
        raise ValueError(
            "No configurations available for GIF generation."
        )

    # 2. Clean only the selected view's PNG frames.
    clean_frame_directory(frame_dir)

    # 3. Render the combined trajectory.
    print("\nGenerating image frames...\n")
    gif_frames = generate_frames(images, rotation, frame_dir)

    # 4. Assemble the GIF.
    print("\nCreating GIF...\n")
    imageio.mimsave(
        output_gif,
        gif_frames,
        duration=args.duration,
        loop=0
    )

    print("\n----------------------------------------")
    print("GIF generation completed successfully.")
    print(f"Frame directory: {os.path.abspath(frame_dir)}")
    print(f"Output GIF: {os.path.abspath(output_gif)}")
    print(f"Total frames: {len(gif_frames)}")
    print("----------------------------------------")


if __name__ == "__main__":
    main()
