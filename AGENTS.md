<!-- Keep this one-view brief at every project stage. Fill it from verified
     repository facts as the design develops; omit sections that do not yet
     apply instead of adding plans or placeholders.

     Keep the section order identical in every OpenDrone repo. State current
     fact only. No plans, no TODOs, no history outside Revisions. -->

# OpenLED

OpenLED is a compact arm-mounted 5 V addressable RGB LED board for OpenDrone
builds. It carries four WS2812B-V6 LEDs in one serial data chain and exposes
5 V, GND, DIN and DOUT through solder pads. It has no onboard controller,
regulator or logic-level translator.

## Architecture

LED data enters through J3 (DIN), passes through D1, D2, D3 and D4 in order,
and leaves through J6 (DOUT).

J1 and J2 provide the 5 V and GND input connections. J4 and J5 expose the same
5 V and GND rails at the opposite end of the board.

Each WS2812B-V6 regenerates DOUT for the next LED in the chain.

C1 and C2 provide 10 uF bulk capacitance near opposite ends of the power rail.
C3-C6 provide one 100 nF local decoupling capacitor per LED.

## Power

| Rail | Source | Distribution | Loads |
|---|---|---|---|
| 5 V | J1 | F.Cu 5 V plane | D1-D4, C1-C6, J4 |
| GND | J2 | B.Cu GND plane and local F.Cu GND zones | D1-D4, C1-C6, J5 |

```text
Externally regulated 5 V
├── J1 -> +5V plane -> D1-D4
│                   -> C1-C6
│                   -> J4
└── J2 -> GND plane/local zones -> D1-D4
                                -> C1-C6
                                -> J5
```

Motor current must not pass through OpenLED.

## Key parts

| Function | Ref | Part | LCSC | Note |
|---|---|---|---|---|
| Addressable RGB LED | D1-D4 | WORLDSEMI WS2812B-V6 | C52917433 | 5 V, 5050, integrated controller |
| Bulk capacitor | C1-C2 | Samsung CL10A106KO8NQNC | C962136 | 10 uF, 16 V, X5R, 0603 |
| Local decoupling | C3-C6 | Samsung CL05B104KO5NNNC | C1525 | 100 nF, one per LED, 0402 |

## Connectors and I/O

All external connections are solder pads rather than fitted connectors.

| Connector | Ref | Part | Function |
|---|---|---|---|
| 5 V input | J1 | `SolderPad_2.2x1.6mm` | 5 V supply input |
| GND input | J2 | `SolderPad_2.2x1.6mm` | Ground input |
| DIN | J3 | `SolderPad_2.2x1.6mm` | Addressable LED data input |
| 5 V output | J4 | `SolderPad_2.2x1.6mm` | 5 V pass-through |
| GND output | J5 | `SolderPad_2.2x1.6mm` | Ground pass-through |
| DOUT | J6 | `SolderPad_2.2x1.6mm` | Data output after D4 |

J1-J6 are excluded from the BOM and position files.

## Layout rules

The PCB is 37 x 7 mm, 0.8 mm thick, two-layer FR4 with 35 um copper and
1 mm corner radii.

The four LEDs are placed on 7 mm centres.

Keep each 100 nF capacitor and its ground return close to the LED it supports.

The primary 5 V distribution is an F.Cu copper zone. Ground is primarily a
B.Cu plane with local F.Cu GND zones.

The D1->D2, D2->D3 and D3->D4 links intentionally use repeated routing
geometry. D3->D4 is the reference geometry; preserve that pattern unless an
electrical or mechanical requirement justifies a change.

OpenDrone manufacturing minima used by the project include 0.09 mm electrical
clearance and track width, 0.075 mm minimum annular width, 0.35 mm minimum via
diameter and 0.20 mm minimum drill.

OpenLED deliberately routes more conservatively:

| Netclass | Clearance | Track width | Via |
|---|---:|---:|---:|
| Default | 0.20 mm | 0.20 mm | 0.60 mm / 0.30 mm drill |
| POWER | 0.20 mm | 0.50 mm | 0.60 mm / 0.30 mm drill |

The POWER netclass applies to `+5V` and `GND`. Normal vias are tented on both
sides.

Mechanical fit on each intended OpenFrame size must be verified physically
before compatibility is considered final.

The manufacturing panel is generated from the standalone board. Do not refill
zones in a generated panel; see `hardware/PANELIZATION.md`.

## Repo

| | |
|---|---|
| Maintainer | @BinaryHippie |
| Status | See the `status-*` topic on the repository |
| Designed in | KiCad 10 |
| KiCad project | `hardware/OpenLED.kicad_pro` |
| Root schematic | `hardware/OpenLED.kicad_sch` |
| Board | `hardware/OpenLED.kicad_pcb`, 2 layers, 0.8 mm FR4, 35 um copper |
| Local library | `hardware/lib.kicad_sym`, `hardware/lib.pretty/`, `hardware/lib.3dshapes/`, nickname `lib` |
| Shared library | `hardware/KiCad-Library/`, submodule of OpenDrone-hw/KiCad-Library, nickname `OpenDrone`; exact shared datasheets resolve through `OPENDRONE_LIB` |
| Design rules | `hardware/OpenLED.kicad_dru`, OpenDrone canonical rules plus board settings in the KiCad project |
| Fab config | `hardware/fabrication-toolkit-options.json` |
| Board setup | 2 layers, 0.8 mm FR4; 0.20 mm normal routing, 0.50 mm POWER routing; OpenDrone manufacturing minima apply |
| Panel workflow | `hardware/PANELIZATION.md`, with board-specific tooling in `hardware/tools/` |
| License | CERN-OHL-S-2.0 |

The project text variable `OPENDRONE_LIB` resolves to
`${KIPRJMOD}/KiCad-Library`.

A repository holds design files only. Sourcing (suppliers, prices, quotes,
RFQs, contacts) is handled by Incutec and never lives in OpenDrone repositories.

## Parts and datasheets

- **Per-repository part index:** `hardware/OpenLED.kicad_sch` is authoritative
  for what this board fits. Export the netlist when a script-readable index is
  needed; do not maintain a second hand-written BOM.
- **Proven shared parts:** inspect
  `hardware/KiCad-Library/PARTS-USED.md` before creating or importing a new
  manufactured part.
- **Exact shared datasheets:**
  `hardware/KiCad-Library/datasheet/manifest.json` maps shared symbols to
  committed datasheets and hashes.
- **Local-only parts:** inspect `hardware/lib.kicad_sym`,
  `hardware/lib.pretty/` and `hardware/lib.3dshapes/`. Current OpenLED-specific
  parts remain local unless the exact part is promoted to the shared catalogue.
- Orderable parts retain exact `Manufacturer`, `MPN` and `LCSC` fields where
  applicable.

## Environment

```sh
# schematic and standalone-board checks
kicad-cli sch erc hardware/OpenLED.kicad_sch
kicad-cli pcb drc --schematic-parity --refill-zones hardware/OpenLED.kicad_pcb

# netlist for scripted analysis
kicad-cli sch export netlist --format kicadsexpr -o OpenLED.net hardware/OpenLED.kicad_sch

# reproducible manufacturing panel
python hardware/tools/build_panel.py
```

On Windows, the KiCad Command Prompt is the recommended environment for the
panel build unless Python and KiKit are separately available in `PATH`.

On macOS `kicad-cli` is at
`/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`, and `pcbnew` imports
only under KiCad's bundled Python.

Reusable OpenDrone tooling for renders, STEP export and release preparation is
external to this repository. The OpenDrone release standard is documented in
`OpenDrone-hw/.github/RELEASES.md`. Board-specific scripts live in
`hardware/tools/`.

## Rules

Identical in every OpenDrone board repo. Do not edit here; edit the template.

- **Never text-edit** `.kicad_sch`, `.kicad_pcb` or `.kicad_dru`. Use KiCad, or
  kicad-skip / the pcbnew API for scripted changes. `.kicad_pro` is JSON and may
  be edited directly for metadata.
- **Metadata yes, connections no.** An agent may write BOM and documentation
  fields (MPN, Manufacturer, LCSC, Cost, Datasheet, text variables). An agent
  may not change nets, wiring, routing, placement, footprint assignment, or any
  value that changes the circuit.
- **Close KiCad before any write to a KiCad file.** KiCad caches library tables
  at process start and overwrites files on save.
- **Reuse before you draw.** Check the `OpenDrone` library and its
  `PARTS-USED.md` first. If the part is there we have already sourced,
  footprinted and shipped it, and its symbol links to the exact committed
  datasheet: place it from `OpenDrone`. Draw a new part into `lib` only when
  the catalogue has nothing that fits, imported with `easyeda2kicad` from its
  LCSC number. Pulling a newer catalogue is a deliberate, reviewed commit:
  `git submodule update --remote hardware/KiCad-Library`, then DRC.
- **One person holds a board layout at a time.** KiCad files do not merge. Say
  on Discord that you are taking it. See [CONTRIBUTING.md](CONTRIBUTING.md).
- **Run ERC and DRC before every pull request.** Existing approved findings may
  remain; a new type or increased count must be reviewed before merge.
  Commands are in Environment above.

## Revisions

| Rev | Date | Change |
|---|---|---|
| 0.1 | 2026-09-27 | Initial OpenLED prototype design and OpenDrone repository migration |

## By task

- Check the design with the ERC and DRC commands in `Environment`.
- Check the OpenDrone shared library before adding a manufactured part.
- Add project-specific footprints and symbols only to the local `lib`.
- Keep exact Manufacturer, MPN and LCSC metadata with orderable components.
- Preserve the repeated D1->D2, D2->D3 and D3->D4 routing pattern.
- Keep one 100 nF local decoupling capacitor at each LED.
- Generate the manufacturing panel with `hardware/tools/build_panel.py`.
- Follow `hardware/PANELIZATION.md` for panel DRC and no-refill requirements.
- Generate fabrication data only from a checked design revision.
- Re-run ERC, DRC and manufacturing-output inspection after electrical,
  layout or panelization changes.
