from pathlib import Path
import json
import os
import shutil
import subprocess
import sys


TOOLS_DIR = Path(__file__).resolve().parent
HARDWARE_DIR = TOOLS_DIR.parent
REPO_ROOT = HARDWARE_DIR.parent

SOURCE_BOARD = HARDWARE_DIR / "OpenLED.kicad_pcb"
PRESET = TOOLS_DIR / "panelize.json"

PANEL_DIR = HARDWARE_DIR / "production" / "panel"
OUTPUT_BOARD = PANEL_DIR / "OpenLED-panel-1x4.kicad_pcb"

FP_LIB_TABLE = PANEL_DIR / "fp-lib-table"
FAB_OPTIONS_FILE = PANEL_DIR / "fabrication-toolkit-options.json"
RESOLVED_PRESET = PANEL_DIR / "panelize-resolved.json"


FP_LIB_CONTENT = """(fp_lib_table
    (version 7)
    (lib (name "lib")(type "KiCad")(uri "${KIPRJMOD}/../../lib.pretty")(options "")(descr "OpenLED project-local footprints"))
    (lib (name "OpenDrone")(type "KiCad")(uri "${KIPRJMOD}/../../KiCad-Library/footprint/OpenDrone.pretty")(options "")(descr "OpenDrone shared parts catalogue"))
)
"""


FAB_OPTIONS = {
    "ARCHIVE_NAME": f"{OUTPUT_BOARD.stem}-rev0.1",
    "EXTRA_LAYERS": "",
    "ALL_ACTIVE_LAYERS": False,
    "EXTEND_EDGE_CUT": False,
    "ALTERNATIVE_EDGE_CUT": False,
    "AUTO TRANSLATE": True,
    "AUTO FILL": False,
    "EXCLUDE DNP": False,
    "OPEN BROWSER": True,
    "NO_BACKUP_OPT": False,
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def warning(message: str) -> None:
    use_color = (
        sys.stderr.isatty()
        and os.environ.get("NO_COLOR") is None
    )

    if use_color:
        red_bold = "\033[1;31m"
        reset = "\033[0m"
        print(f"{red_bold}{message}{reset}", file=sys.stderr)
    else:
        print(message, file=sys.stderr)


def main() -> None:
    kikit = shutil.which("kikit")

    if kikit is None:
        fail(
            "KiKit was not found in PATH. "
            "Run this script from an environment where the 'kikit' command works."
        )

    if not SOURCE_BOARD.is_file():
        fail(f"Source board not found: {SOURCE_BOARD}")

    if not PRESET.is_file():
        fail(f"Panel preset not found: {PRESET}")

    PANEL_DIR.mkdir(parents=True, exist_ok=True)

    if OUTPUT_BOARD.exists():
        OUTPUT_BOARD.unlink()

    print("Generating OpenLED 1x4 panel...")

    subprocess.run(
        [
            kikit,
            "panelize",
            "-p",
            str(PRESET),
            "-d",
            str(RESOLVED_PRESET),
            str(SOURCE_BOARD),
            str(OUTPUT_BOARD),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    with FP_LIB_TABLE.open("w", encoding="utf-8", newline="\n") as file:
        file.write(FP_LIB_CONTENT)

    with FAB_OPTIONS_FILE.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(FAB_OPTIONS, file, indent=2)
        file.write("\n")

    print()
    print("Panel generated successfully:")
    print(f"  {OUTPUT_BOARD}")

    print()
    print("Generated panel support files:")
    print(f"  {FP_LIB_TABLE}")
    print(f"  {FAB_OPTIONS_FILE}")
    print(f"  {RESOLVED_PRESET}")

    print()
    warning("WARNING: DO NOT REFILL ZONES IN THE GENERATED PANEL.")

    print()
    print("Fabrication Toolkit AUTO FILL is disabled for the generated panel.")
    print("The source OpenLED PCB remains the design source of truth.")


if __name__ == "__main__":
    main()
