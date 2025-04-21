# logic.py

import subprocess
import tempfile
import os

from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces


def convert_svg_to_paths(input_svg_path: str) -> str:
    """
    Converts all SVG elements to paths using Inkscape CLI.
    Returns path to cleaned SVG with only <path> tags.
    """
    # Create a temp file for cleaned output
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".svg")
    tmp.close()
    cleaned_svg_path = tmp.name

    # Construct the new Inkscape CLI command (v1.0+ syntax)
    cmd = [
        "inkscape",
        input_svg_path,
        "--export-type=svg",
        "--export-plain-svg",
        f"--export-filename={cleaned_svg_path}",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(
            f"Inkscape failed with code {result.returncode}:\n"
            f"{result.stderr or result.stdout}"
        )

    # Confirm file was created and is not empty
    if not os.path.exists(cleaned_svg_path) or os.stat(cleaned_svg_path).st_size == 0:
        raise RuntimeError("Inkscape did not generate a valid cleaned SVG file.")

    return cleaned_svg_path


def convert_svg_to_gcode(
    svg_path: str, movement_speed: float, cutting_speed: float, pass_depth: float
) -> str:
    """
    Full pipeline:
      1) Run Inkscape to flatten & convert all shapes to <path>.
      2) Parse the cleaned SVG into curves.
      3) Compile curves into G‑code.
      4) Clean up temporary SVG.

    Returns the G‑code as a single string.
    """
    # 1) flatten shapes → paths
    cleaned_svg = convert_svg_to_paths(svg_path)

    try:
        # 2) parse into geometric curves
        curves = parse_file(cleaned_svg)

        # 3) compile to G‑code
        compiler = Compiler(
            interfaces.Gcode,
            movement_speed=movement_speed,
            cutting_speed=cutting_speed,
            pass_depth=pass_depth,
        )
        compiler.append_curves(curves)
        gcode = compiler.compile()

    finally:
        # 4) cleanup
        try:
            os.remove(cleaned_svg)
        except OSError:
            pass

    return gcode
