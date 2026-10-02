# OpenLED 1x4 Manufacturing Panel

This document describes the reproducible manufacturing-panel workflow for
OpenLED.

The production panel contains four identical OpenLED boards, providing one
complete four-arm LED set for a drone.

## Panel configuration

- 1 column x 4 rows
- 4 identical OpenLED boards
- Individual board size: 37 mm x 7 mm
- PCB thickness: 0.8 mm
- Generated panel outline: approximately 53 mm x 53 mm
- 5 mm outer frame
- 3 mm spacing between boards and frame
- 5 mm breakaway tabs
- Routed slots with mouse-bite depanelization
- Mouse bites: 0.60 mm NPTH drill
- Mouse-bite pitch: 1.00 mm centre-to-centre
- Mouse-bite offset: -0.30 mm
- 6 mouse-bite holes per 5 mm tab
- 3 tooling holes, 2.0 mm diameter
- 3 fiducial locations on top and bottom copper
- No V-cuts

The tooling holes and fiducials are retained even when the prototype panels are
hand assembled. They keep the panel suitable for future automated assembly and
provide a consistent manufacturing-panel layout.

## Source of truth

The standalone board is the design source of truth:

    hardware/OpenLED.kicad_pcb

The generated panel is production output and must not be edited as the master
design.

Panel configuration is stored in:

    hardware/tools/panelize.json

KiKit post-processing is implemented in:

    hardware/tools/panel_post.py

The reproducible panel build is orchestrated by:

    hardware/tools/build_panel.py

Generated panel files are written below:

    hardware/production/panel/

The entire `hardware/production/` tree is ignored by Git because it contains
regenerable manufacturing output.

## Requirements

The panel workflow requires:

- KiCad
- Python
- KiKit

Run the build from an environment where Python and KiKit are available.

On Windows, the KiCad Command Prompt is the recommended environment unless
Python and KiKit have separately been added to the normal system PATH.

On Linux and macOS, a normal shell can be used when Python, KiCad and KiKit are
installed and available.

No absolute machine-specific paths are required.

## Generate the panel

From the repository root:

    python hardware/tools/build_panel.py

The script:

1. locates the OpenLED repository relative to its own path;
2. checks that KiKit is available;
3. creates `hardware/production/panel/` when required;
4. generates the 1x4 panel using `hardware/tools/panelize.json`;
5. applies `hardware/tools/panel_post.py`;
6. writes the panel-local footprint-library table;
7. writes panel-specific Fabrication Toolkit settings;
8. writes the fully resolved KiKit preset for inspection.

The normal generated board is:

    hardware/production/panel/OpenLED-panel-1x4.kicad_pcb

## KiKit source tolerance

The panel preset uses:

    tolerance: 15mm

This is a KiKit source-extraction tolerance, not a PCB manufacturing tolerance.

It enlarges the source extraction area so that panelization annotations and
other required board items extending outside the OpenLED Edge.Cuts are not
discarded.

The value is deliberately generous and has been verified with the current
OpenLED source board.

## Footprint libraries

The generated panel receives its own `fp-lib-table`.

Its project-local footprint library resolves through:

    ${KIPRJMOD}/../../lib.pretty

The shared OpenDrone library resolves through:

    ${KIPRJMOD}/../../KiCad-Library/footprint/OpenDrone.pretty

These are relative project paths. Do not replace them with absolute local
filesystem paths.

This allows a generated panel to be opened from a clone located anywhere on
Windows, Linux or macOS.

## Copper-zone handling

The standalone OpenLED PCB must have its copper zones filled and saved before
panel generation.

For the source board:

1. open `hardware/OpenLED.kicad_pcb`;
2. refill zones normally;
3. save the board;
4. run the normal source-board DRC.

The generated panel is different.

**DO NOT REFILL ZONES IN THE GENERATED PANEL.**

KiKit preserves the filled copper geometry from the individual source boards.
Refilling the generated panel can cause zones to extend into the sacrificial
tabs and panel structure.

Therefore:

- do not press `B` in the generated panel;
- disable `Refill all zones before performing DRC` when checking the panel;
- keep Fabrication Toolkit `AUTO FILL` disabled for the panel;
- regenerate the panel from the source board instead of manually modifying its
  copper zones.

`build_panel.py` automatically creates a panel-specific
`fabrication-toolkit-options.json` with:

    "AUTO FILL": false

The tracked source-board Fabrication Toolkit configuration remains separate and
may use normal zone refill.

## Panel post-processing

`hardware/tools/panel_post.py` marks KiKit tooling holes and fiducials as:

- excluded from BOM;
- excluded from position files;
- board-only objects.

KiKit handles the mouse-bite NPTH footprints separately.

This metadata is retained even though current prototypes are hand assembled so
the panel remains suitable for future automated assembly workflows.

## Manufacturing outputs

For the current prototype stage the boards are fabricated by JLCPCB and
assembled manually.

The PCB fabrication upload therefore uses the Gerber and drill archive from the
generated panel.

Fabrication Toolkit may also generate BOM and position files. These are retained
as useful generated outputs for verification and possible future automated
assembly, but they are not the authoritative component database.

The KiCad schematic remains authoritative for fitted components, manufacturer
part numbers and LCSC identifiers.

Do not manually maintain a second BOM as a source of truth.

## Verification

After any change affecting the board layout or panel configuration:

1. refill and save the standalone source PCB;
2. run source ERC and DRC;
3. regenerate the panel with `build_panel.py`;
4. visually inspect the generated panel;
5. run panel DRC with zone refill disabled;
6. inspect the generated Gerber and drill files;
7. verify BOM and position-file contents when generated.

A change to the panel preset requires the generated panel to be revalidated
before fabrication.

## Release status

The generated manufacturing files are prototype/in-progress outputs.

Do not create an OpenDrone `rev*` Git tag or GitHub release solely because a
prototype fabrication package has been generated.

The formal OpenDrone release process is performed after manufactured hardware
has been reviewed and the project reaches the appropriate project stage.
