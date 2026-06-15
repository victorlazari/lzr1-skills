# Tomate POS-80 Detailed ESC/POS Command Reference

This document compiles the exhaustive command set for the Tomate POS-80 thermal printer based on the official programmer's manual [1]. Use these codes to build custom drivers, format receipts, or control peripheral hardware.

---

## 1. Print & Feed Commands

These commands control the basic movement of paper and printing of buffer data [1].

### LF (Print and Line Feed)
- **ASCII**: `LF`
- **Hex**: `0A`
- **Decimal**: `10`
- **Description**: Prints any data in the print buffer and feeds one line based on the current line spacing [1]. Resets the print position to the beginning of the line.

### CR (Print and Carriage Return)
- **ASCII**: `CR`
- **Hex**: `0D`
- **Decimal**: `13`
- **Description**: If automatic line feed is enabled, functions identically to `LF`. If disabled, it is ignored [1].

### ESC J n (Print and Feed Paper)
- **ASCII**: `ESC J n`
- **Hex**: `1B 4A n`
- **Decimal**: `27 74 n`
- **Range**: `0 ≤ n ≤ 255`
- **Description**: Prints the data in the print buffer and feeds the paper by `n` motion units (`n * vertical motion unit` inches) [1]. Does not affect current line spacing settings.

### ESC d n (Print and Feed n Lines)
- **ASCII**: `ESC d n`
- **Hex**: `1B 64 n`
- **Decimal**: `27 100 n`
- **Range**: `0 ≤ n ≤ 255`
- **Description**: Prints buffer data and feeds `n` lines [1]. Maximum feed amount is 1016mm (40 inches).

---

## 2. Printer Hardware Control

These commands control printer hardware initialization, cash drawers, and cutting [1].

### ESC @ (Initialize Printer)
- **ASCII**: `ESC @`
- **Hex**: `1B 40`
- **Decimal**: `27 64`
- **Description**: Clears print buffer data and resets the printer to its power-on default modes [1]. Receive buffer, macros, and NV graphics memory are not cleared.

### GS V m (Select Cut Mode and Cut Paper)
- **ASCII**: `GS V m`
- **Hex**: `1D 56 m`
- **Decimal**: `29 86 m`
- **Range**: `m = 1, 49`
- **Description**: Executes a partial cut of the paper (one point left uncut) [1].

### GS V m n (Feed and Cut Paper)
- **ASCII**: `GS V m n`
- **Hex**: `1D 56 m n`
- **Decimal**: `29 86 m n`
- **Range**: `m = 66`, `0 ≤ n ≤ 255`
- **Description**: Feeds paper by `n` vertical motion units and performs a partial cut [1]. When `n = 0`, it feeds to the physical cutting blade position and cuts.

### ESC p m t1 t2 (Generate Pulse / Cash Drawer Kick-out)
- **ASCII**: `ESC p m t1 t2`
- **Hex**: `1B 70 m t1 t2`
- **Decimal**: `27 112 m t1 t2`
- **Range**: `m = 0, 1, 48, 49`, `0 ≤ t1 ≤ 255`, `0 ≤ t2 ≤ 255`
- **Description**: Outputs a pulse to the cash drawer connector pin specified by `m` [1].
  - `m = 0, 48`: Drawer kick-out pin 2.
  - `m = 1, 49`: Drawer kick-out pin 5.
  - Pulse ON time is `t1 * 2 ms`. Pulse OFF time is `t2 * 2 ms`.

---

## 3. Formatting & Styling Commands

These commands manipulate text alignment, sizing, and style [1].

### ESC a n (Select Justification)
- **ASCII**: `ESC a n`
- **Hex**: `1B 61 n`
- **Decimal**: `27 97 n`
- **Range**: `0 ≤ n ≤ 2`, `48 ≤ n ≤ 50`
- **Description**: Aligns all data in a line [1]. Must be sent at the beginning of a line.
  - `n = 0, 48`: Left justification (default).
  - `n = 1, 49`: Centering.
  - `n = 2, 50`: Right justification.

### ESC ! n (Select Print Mode - Master Command)
- **ASCII**: `ESC ! n`
- **Hex**: `1B 21 n`
- **Decimal**: `27 33 n`
- **Range**: `0 ≤ n ≤ 255`
- **Description**: Combines multiple formatting options into a single byte `n` using bitwise flags [1]:
  - **Bit 0**: Font selection (`0` = Font A 12x24, `1` = Font B 9x17).
  - **Bit 3**: Emphasized/Bold (`1` = ON).
  - **Bit 4**: Double-Height (`1` = ON).
  - **Bit 5**: Double-Width (`1` = ON).
  - **Bit 7**: Underline (`1` = ON).

### GS ! n (Select Character Size)
- **ASCII**: `GS ! n`
- **Hex**: `1D 21 n`
- **Decimal**: `29 33 n`
- **Range**: `0 ≤ n ≤ 255`
- **Description**: Selects independent character height (bits 0-2, 1x to 8x) and character width (bits 4-7, 1x to 8x) [1].

### ESC E n (Turn Emphasized Mode On/Off)
- **ASCII**: `ESC E n`
- **Hex**: `1B 45 n`
- **Decimal**: `27 69 n`
- **Description**: Turns bold printing on/off [1]. Only the least significant bit (LSB) of `n` is used (`0` = Off, `1` = On).

### ESC - n (Turn Underline Mode On/Off)
- **ASCII**: `ESC - n`
- **Hex**: `1B 2D n`
- **Decimal**: `27 45 n`
- **Range**: `0 ≤ n ≤ 2`, `48 ≤ n ≤ 50`
- **Description**: Turns underline mode on or off [1].
  - `n = 0, 48`: Turns off underline mode.
  - `n = 1, 49`: Turns on 1-dot thick underline.
  - `n = 2, 50`: Turns on 2-dot thick underline.

### GS B n (Turn White/Black Reverse Printing On/Off)
- **ASCII**: `GS B n`
- **Hex**: `1D 42 n`
- **Decimal**: `29 66 n`
- **Description**: Inverts character colors (white text on black background) [1]. LSB of `n` determines state (`0` = Off, `1` = On).

### ESC { n (Turn Upside-Down Printing On/Off)
- **ASCII**: `ESC { n`
- **Hex**: `1B 7B n`
- **Decimal**: `27 123 n`
- **Description**: Rotates text 180 degrees [1]. Must be sent at the beginning of a line. LSB of `n` determines state (`0` = Off, `1` = On).

---

## 4. Spacing & Margin Control

These commands control the printable margins and line spacing of the paper [1].

### ESC 2 (Select Default Line Spacing)
- **ASCII**: `ESC 2`
- **Hex**: `1B 32`
- **Decimal**: `27 50`
- **Description**: Resets line spacing to the default `1/6-inch` (approximately 4.23mm) [1].

### ESC 3 n (Set Line Spacing)
- **ASCII**: `ESC 3 n`
- **Hex**: `1B 33 n`
- **Decimal**: `27 51 n`
- **Range**: `0 ≤ n ≤ 255`
- **Description**: Sets the line spacing to `n * vertical motion unit` inches [1].

### GS L nL nH (Set Left Margin)
- **ASCII**: `GS L nL nH`
- **Hex**: `1D 4C nL nH`
- **Decimal**: `29 76 nL nH`
- **Description**: Sets the left margin to `(nL + nH * 256) * horizontal motion unit` inches [1]. Must be sent at the beginning of a line.

### GS W nL nH (Set Printing Area Width)
- **ASCII**: `GS W nL nH`
- **Hex**: `1D 57 nL nH`
- **Decimal**: `29 87 nL nH`
- **Description**: Sets the total printable area width to `(nL + nH * 256) * horizontal motion unit` inches [1]. Default is `nL=0, nH=2` (72mm width).

---

## References
[1] ZKTECO Colombia, *POS-80-Series Printer Programmer Manual*, https://zktecocolombia.com/wp-content/uploads/2025/08/Manual-de-Progamacion.pdf
