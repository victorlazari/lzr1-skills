---
name: tomate-pos80
description: "Comprehensive integration skill for the Tomate POS-80 (MDK-080, MDK-081, MDK-08260) thermal receipt printer. Use when: configuring, formatting, or sending raw print commands, managing encoding/special characters, generating barcodes/QR codes, and designing receipt templates."
---

# Tomate POS-80 Thermal Receipt Printer Integration

This skill provides comprehensive, expert-level instructions and resources for integrating and printing with the **Tomate POS-80** (including models MDK-080, MDK-081, and MDK-08260) thermal receipt printer. It details the ESC/POS command specifications, character encoding configurations, printing processes, and formatting templates required to achieve professional, error-free printing in any environment.

## Scope and Triggers

- **Scope**: Configuring, formatting, and sending raw print commands, managing encoding/special characters, generating barcodes/QR codes, and designing receipt templates for Tomate POS-80 printers.
- **Triggers**: When the user requests to print receipts, configure a Tomate POS-80 printer, or generate ESC/POS commands.
- **Non-goals**: This skill does not cover network discovery of printers or integration into larger Python applications (see Cross-Skill Routes).

## Preconditions

1. **Target Identification**: Identify the connection method (USB, Network, or Serial) and target address.
2. **Environment**: Ensure the executing environment has network access to the printer IP or permissions to write to the USB device file.
3. **Inputs**: Determine the required receipt layout, encoding (WPC1252 for Portuguese), and necessary ESC/POS commands.

## Source Freshness

The ESC/POS commands and hardware specifications are stable. The reference files hardcode the verified hex/byte sequences.
- **Verified against upstream**: 2026-08-07
- **Primary Sources**: ZKTECO POS-80-Series Printer Programmer Manual, Tomate MDK-080 product specifications.

## Workflow

1. **Identify Connection**: Determine the connection method (USB, Network, or Serial) and target address.
2. **Determine Layout**: Determine the required receipt layout, encoding (WPC1252 for Portuguese), and necessary ESC/POS commands from the reference files.
3. **Construct Byte Stream**: Construct the raw byte stream using the appropriate Python codecs.
4. **Dry-Run**: Execute a dry-run to verify the byte sequence using `scripts/example.py`.
5. **Confirmation**: Request user confirmation before transmitting to the physical printer.
6. **Transmit**: Transmit the data and handle any connection errors.

## Safety

- **Read-only Discovery**: Perform dry-runs to verify byte sequences before sending to the printer.
- **Confirmation Required**: Require explicit user confirmation before sending raw bytes to a network IP or USB port.
- **Validation**: Validate that the provided IP address is reachable before attempting a socket connection.

## Validation

- **Syntax Checks**: Ensure Python scripts compile and execute successfully in dry-run mode.
- **Postcondition Verification**: Confirm the printer successfully received and printed the data without errors.

## Failure Handling

- **Connection Errors**: Catch and handle socket timeouts gracefully. Verify the IP address and network connectivity.
- **Encoding Errors**: Ensure the correct code page (e.g., WPC1252) is selected and the text is encoded with the matching Python codec (`cp1252`).

## Output Contract

- **Structure**: A detailed summary of the printing operation, including the connection method, layout used, and any errors encountered.
- **Evidence**: The raw byte sequence generated during the dry-run.
- **Next Steps**: Actionable advice for resolving any connection or encoding issues.

## Resources

- [Detailed Command Set](references/commands.md): Exhaustive reference of all ESC/POS commands.
- [Special Characters & Encoding Map](references/encoding.md): Character maps and code page tables.
- [Barcodes & QR Codes](references/barcodes.md): Command syntaxes for 1D barcodes and 2D QR codes.
- [Receipt Layout Templates](references/templates.md): Production-ready layout designs.
- [Example Script](scripts/example.py): Python script for generating and sending ESC/POS commands.

## Cross-Skill Routes

- **network-discovery**: Route when the printer IP address is unknown and needs to be discovered on the local network.
- **python-developer**: Route when the user needs to integrate the ESC/POS commands into a larger Python application or web service.

## Printer Specifications

| Specification | Detail |
| :--- | :--- |
| **Print Method** | Direct Thermal (no ink or ribbon required) |
| **Paper Width** | 80mm (79.5 ± 0.5mm) |
| **Print Width** | 72mm (576 dots per line) |
| **Print Speed** | 230 mm/s (MDK-080) / 150 mm/s (MDK-08260) |
| **Resolution** | 203 dpi |
| **Line Spacing** | Default 3.75mm (1/6 inch) |
| **Interfaces** | USB, LAN (Ethernet), RJ11 (Cash Drawer) |
| **Operating Systems** | Windows, Linux |
| **Command Set** | Standard ESC/POS Command Set |

## Connection Methods

- **USB (Raw Access)**: Write raw bytes directly to the USB device file (e.g., `/dev/usb/lp0` on Linux) or use a spooler.
- **Ethernet (TCP/IP)**: Open a raw TCP socket to the printer's IP address on **Port 9100** (default raw print port).
- **Virtual Serial (COM)**: Communicate via virtual COM ports configured by the USB driver.

## Character Encoding & Code Pages

Thermal printers use hardware code pages to print accented and special characters. For Portuguese, configuring the correct code page is critical.

1. **WPC1252 (Latin-1)**: Highly recommended for Portuguese. Select using command `ESC t 16`.
2. **PC850 (Multilingual)**: Good fallback. Select using command `ESC t 2`.
3. **PC860 (Portuguese)**: Native Portuguese hardware page. Select using command `ESC t 3`.

> **Crucial Rule**: When sending text, you **must** encode the string using the corresponding Python/Node.js codec (e.g., `cp1252`, `cp850`, or `cp860`) before converting it to raw bytes. Do not send UTF-8 strings directly!

## Basic Formatting Command Quick-Reference

| Command | Hex Bytes | Description |
| :--- | :--- | :--- |
| **LF** | `0A` | Print and line feed |
| **ESC @** | `1B 40` | Initialize printer (resets settings) |
| **ESC a n** | `1B 61 n` | Alignment: `n=0` (Left), `n=1` (Center), `n=2` (Right) |
| **ESC ! n** | `1B 21 n` | Master Print Mode (combine Font B, Bold, Double-Height, Double-Width, Underline) |
| **GS ! n** | `1D 21 n` | Select character size (independent width/height magnification 1x to 8x) |
| **GS V m n** | `1D 56 m n` | Feed and cut paper: `m=66` feeds `n` units and cuts partially |
