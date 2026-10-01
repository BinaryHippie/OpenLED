# OpenLED 2x6 Manufacturing Panel

This directory contains the generated manufacturing panel for OpenLED.

## Panel configuration

- 2 columns x 6 rows
- 12 OpenLED boards
- Individual board size: 37 mm x 7 mm
- PCB thickness: 0.8 mm
- 5 mm breakaway tabs
- Routed slots with mouse-bite depanelization
- Mouse bites: 0.60 mm NPTH, 1.00 mm pitch, -0.40 mm KiKit offset
- 6 mouse-bite holes per tab
- 3 tooling holes, 2.0 mm
- 3 fiducial locations on both top and bottom copper
- No V-cuts

## Copper zones

Do not refill copper zones in the generated panel.

The source OpenLED PCB must be zone-filled before panelization. The generated
panel preserves the source-board copper geometry.

Refilling the generated panel can extend copper into the breakaway tabs.

Therefore:

- Disable "Refill all zones before performing DRC" when running panel DRC.
- Disable "Apply automatic fill for all zones" in Fabrication Toolkit.
- If the source PCB changes, regenerate the panel instead of modifying its zones.

## Panel generation

Run from the repository root using a KiCad Command Prompt:

    kikit panelize ^
      --source "tolerance: 15mm" ^
      --layout "grid; rows: 6; cols: 2; hspace: 2mm; vspace: 3mm; renameref: Board_{n}-{orig}" ^
      --tabs "annotation; tabfootprints: lib:Tab" ^
      --cuts "mousebites; drill: 0.6mm; spacing: 1mm; offset: -0.4mm; prolong: 0mm" ^
      --framing "frame; width: 5mm; space: 3mm; cuts: none" ^
      --tooling "3hole; hoffset: 3.85mm; voffset: 3.85mm; size: 2mm" ^
      --fiducials "3fid; hoffset: 12mm; voffset: 3.85mm; coppersize: 1mm; opening: 2mm" ^
      --post "millradius: 1mm; script: hardware/panel_post.py" ^
      hardware\OpenLED.kicad_pcb ^
      hardware\production\panel\OpenLED-panel-2x6.kicad_pcb

`hardware/panel_post.py` excludes KiKit tooling holes and fiducials from BOM
and position files. KiKit excludes mouse-bite NPTH footprints itself.

## Footprint library

The panel-local `fp-lib-table` must reference the source library using:

    ${KIPRJMOD}/../../lib.pretty

Do not replace this with an absolute machine-specific path.

## Production output

Fabrication Toolkit generates temporary output in:

    production/

This directory is ignored by Git.

Reviewed releases are stored in:

    release/rev0.1/

For PCB fabrication use:

    OpenLED-panel-2x6-rev0.1.zip

For assembly use:

    OpenLED-panel-2x6-rev0.1_bom.csv
    OpenLED-panel-2x6-rev0.1_positions.csv