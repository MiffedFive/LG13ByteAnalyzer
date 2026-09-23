# LG-HVAC-13Byte

A Saleae Logic High Level Analyzer (HLA) for decoding LG HVAC wall-controller traffic that uses a fixed 13-byte packet format.

The analyzer is intended to run on top of a UART/Async Serial analyzer in Saleae Logic 2. It converts raw bytes into readable status, capability, configuration, temperature, power, and extended-information records.

## Features

- Buffers incoming serial bytes into 13-byte packets.
- Resets the packet buffer after an inter-byte timeout of 350 ms.
- Validates the packet checksum:
  
  ```text
  checksum = (sum(bytes[0:12]) & 0xFF) ^ 0x55
  ```

- Reports invalid packets as `Bad Checksum` frames and includes the raw packet.
- Decodes the source, product type, and message type from byte 0.
- Decodes the following message types:
  - Type 0: current status, power, mode, setpoint, room temperature, fan, flags, zones, timers, and errors.
  - Type 1: unit capabilities, supported modes, fan speeds, vanes, and optional features.
  - Type 2: fan calibration, vane positions, temperature limits, and installer settings.
  - Type 3: pipe temperatures, DRED state, Wi-Fi access-point state, and request flag.
  - Type 4: filter time, accumulated power, room temperature, and setpoint mode.
  - Type 6: extended status and setting commands.
  - Type 7: raw current-power data.
  - Type 5 and other unsupported types: raw packet output.

## Requirements

- Saleae Logic 2.
- A Saleae capture containing the LG HVAC serial traffic.
- A serial analyzer configured for the protocol. The current implementation assumes 102 baud (8N1, 10 bits per byte) and one byte per roughly 98 ms.
- Python support provided by Saleae Logic for High Level Analyzers.

## Repository files

```text
LG13ByteAnalyzer/
├── extension.json          # Saleae extension metadata and entry point
├── LG13ByteAnalyzer.py     # High Level Analyzer implementation
└── README.md               # This documentation
```

## Installation in Saleae Logic 2

1. Clone or download this repository.
2. Open Saleae Logic 2.
3. Open the Extensions or Analyzers management view and choose the option to load an existing extension.
4. Select the repository directory containing `extension.json`.
5. Confirm that `LG-HVAC-13Byte` appears as an available High Level Analyzer.
6. Open a capture containing the LG HVAC traffic.

The extension metadata is defined in `extension.json`.

If Logic does not load the extension, make sure that `extension.json` and `LG13ByteAnalyzer.py` are in the same directory and that the entry-point name has not been changed.

## Using the analyzer

### 1. Capture the signal

Connect the Saleae device to the signal carrying the LG HVAC serial traffic. Use the correct electrical interface and voltage level for the controller. Do not connect a Saleae input directly to a signal whose voltage exceeds the input limits.

Capture enough traffic to include complete 13-byte packets and the idle gap between packets.

### 2. Add the serial analyzer

Add an **Async Serial** analyzer to the capture channel and configure it with the verified bus parameters:

- **Bit Rate (Baud Rate):** `102`
- **Bits per Frame:** `8 Bits`
- **Stop Bits:** `1 Stop Bit`
- **Parity Bit:** `None`
- **Significant Bit:** `LSB First`

Verify that the serial analyzer produces one data frame for each received byte (~98 ms per byte). If framing errors occur or bytes are missing, verify signal levels and adjust the baud rate within the 100–104 baud window.

### 3. Add `LG-HVAC-13Byte`

Add the `LG-HVAC-13Byte` High Level Analyzer and select the serial analyzer as its input analyzer. The HLA consumes the serial analyzer's byte frames and emits decoded frames in the analyzer results pane.

Typical results look like:

```text
[Master] Status: ON, Cool, Set: 22.0°C, Room: 24.5°C, Fan: High
[Slave] Capabilities: Kind: Wall (1 Vane), Fans: [Auto,High,Med,Low]
[Unit] Advanced: Pipe Temps: [In: 20°C, Out: 18°C, Mid: 19°C], DRED: 0, AP: OFF
ERROR: Bad Checksum! Raw: ...
```

The exact output depends on the packet contents and the tables defined in `LG13ByteAnalyzer.py`.

## Packet format

Each packet is expected to contain exactly 13 bytes:

```text
Byte 0       Header: source, product type, and message type
Bytes 1-11  Message-specific payload
Byte 12      Checksum
```

Byte 0 is interpreted as follows:

```text
bits 7-5    Source ID
bits 4-3    Product type
bits 2-0    Message type
```

Known source IDs are:

| ID | Source |
| ---: | --- |
| 1 | Slave |
| 5 | Master |
| 6 | Unit |

Known product types are:

| ID | Product |
| ---: | --- |
| 0 | Ventilation |
| 1 | AC |
| 2 | HeatExchanger |

Unknown IDs are retained in the output as `Src:<id>` or `Prod:<id>`.

## Timing and packet boundaries

The analyzer does not use a separate sync byte. It collects bytes until 13 bytes are available. If the gap between consecutive bytes is greater than 350 ms, the current buffer is discarded and a new packet begins.

This means that:

- The serial analyzer must decode every byte correctly.
- A capture should preserve the idle interval between packets.
- Dropped bytes can shift packet alignment until the timeout starts a new packet.
- A stream with a different packet length or timing will not be decoded reliably without code changes.

## Development

The implementation uses the Saleae High Level Analyzer API:

```python
from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame
```

The entry point is:

```text
LG13ByteAnalyzer.LG13ByteAnalyzer
```

To make changes:

1. Edit `LG13ByteAnalyzer.py`.
2. Reload the extension in Saleae Logic 2.
3. Run a capture containing representative packets.
4. Check both valid packets and intentionally invalid checksums.

A basic syntax check can be run with:

```bash
PYTHONPYCACHEPREFIX="$TMPDIR/pycache" python3 -m py_compile LG13ByteAnalyzer.py
```

## Limitations

- The protocol mapping is based on observed LG HVAC traffic and may not apply to every LG model or controller firmware.
- The pipe-temperature lookup table covers the byte values currently documented in the source. Unknown values are displayed as raw hexadecimal values.
- Type 7 power data is currently displayed as a raw substring rather than converted to engineering units.
- No packet transmission or control commands are generated; this project only analyzes captured traffic.
- The analyzer requires exactly 13 bytes per packet.

## Protocol reference

This extension is based on the LG HVAC protocol documentation from [JanM321/esphome-lg-controller](https://github.com/JanM321/esphome-lg-controller/blob/main/protocol.md). The packet decoding and field interpretations in this repository follow that reference and may include additional implementation-specific observations.

## Disclaimer

This is an independent reverse-engineering tool and is not affiliated with or endorsed by LG Electronics or Saleae. Use appropriate electrical safety precautions when connecting measurement equipment to HVAC control equipment.
