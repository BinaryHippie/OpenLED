# OpenLED

OpenLED is a low-profile addressable RGB LED board intended for mounting on
OpenDrone frame arms. Each board carries four individually addressable
WS2812B-V6 LEDs and connects using solder pads for 5 V, ground and LED data.
An output set provides 5 V, ground and DOUT for optional daisy chaining.

The current design is a fixed 37 x 7 mm rigid PCB. It does not carry motor
current and does not include an onboard controller; LED data and 5 V power are
provided by the flight controller or another compatible source.

## Why

Arm-mounted LEDs can provide orientation, status indication and visual effects
without requiring a separate bulky lighting module.

OpenLED keeps the board simple: four addressable LEDs, direct solder-pad
connections and no additional controller. The design is intended to remain
lightweight, low profile, repairable and easy to integrate with OpenDrone
hardware.

The first revision is being developed as a reusable arm LED board. Mechanical
fit on the intended OpenFrame sizes must be verified physically before frame
compatibility is treated as final.

## Specifications

| | |
|---|---|
| Supply voltage | 5 V |
| LEDs | 4x WS2812B-V6 |
| LED type | Individually addressable RGB |
| Data interface | DIN / DOUT |
| Input connections | 5 V, GND, DIN solder pads |
| Output connections | 5 V, GND, DOUT solder pads |
| Bulk capacitance | 2x 10 uF |
| PCB size | 37 x 7 mm |
| PCB thickness | 0.8 mm |
| Copper layers | 2 |
| Copper weight | 35 um |
| Board material | FR4 |

## Constraints

- The board is powered from a regulated 5 V source.
- Motor current must not be routed through the OpenLED PCB.
- The board has no onboard MCU or LED protocol controller.
- LED data enters at DIN and propagates through D1-D4 to DOUT.
- Connections use solder pads rather than board-mounted connectors to minimise
  height and weight.
- The PCB is 37 x 7 mm with 1 mm corner radii.
- The design uses a front-layer 5 V plane and a back-layer GND plane.
- The board is intended for arm mounting and should remain compatible with
  heat-shrink or another lightweight strain-relief method.
- Mechanical compatibility with each intended OpenFrame size must be physically
  verified before release.
- Components should retain exact Manufacturer, MPN and LCSC fields where
  applicable.
- The project is authored in KiCad 10.

## Prior art

- Commercial FPV arm LED strips demonstrate the usefulness of compact,
  arm-mounted addressable lighting.
- SpeedyBee arm LED products were reviewed as a reference for compact layout,
  power distribution and end-of-board bulk capacitance.
- OpenDrone flight-controller designs provide the intended integration context
  for 5 V power and LED-strip data.

## Design questions

- Confirm physical fit and mounting method on each intended OpenFrame size.
- Confirm the preferred wire routing and strain-relief method on an assembled
  arm.
- Validate LED visibility and spacing when installed under the intended
  protective covering.
- Confirm the production PCB finish and final assembly process after prototype
  testing.

## In the line

OpenLED is intended as an optional lighting accessory for OpenDrone builds.

It is designed to accept a 5 V supply and an addressable LED data signal from a
compatible flight controller, while retaining DOUT for optional chaining.

What pairs with what, and what is available:
[opendrone.be](https://opendrone.be).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Hardware licensed under
[CERN-OHL-S-2.0](https://ohwr.org/cern_ohl_s_v2.txt), see [LICENSE](LICENSE).