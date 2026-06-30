---
name: tomate-pos80
description: "Comprehensive integration skill for the Tomate POS-80 (MDK-080, MDK-081, MDK-08260) thermal receipt printer. Use when: configuring, formatting, or sending raw print commands, managing encoding/special characters, generating barcodes/QR codes, and designing receipt templates."
---

# Tomate POS-80 Thermal Receipt Printer Integration

This skill provides comprehensive, expert-level instructions and resources for integrating and printing with the **Tomate POS-80** (including models MDK-080, MDK-081, and MDK-08260) thermal receipt printer. It details the ESC/POS command specifications, character encoding configurations, printing processes, and formatting templates required to achieve professional, error-free printing in any environment.

## Printer Specifications

The Tomate POS-80 is a high-speed, direct thermal receipt printer widely used in points of sale (POS), restaurants, and commercial automation [1].

| Specification | Detail |
| :--- | :--- |
| **Print Method** | Direct Thermal (no ink or ribbon required) [1] [2] |
| **Paper Width** | 80mm (79.5 ± 0.5mm) [1] [2] |
| **Print Width** | 72mm (576 dots per line) [1] [2] |
| **Resolution** | 203 DPI (8 dots/mm) [1] [2] |
| **Print Speed** | 230 mm/s (MDK-080) / 150 mm/s (MDK-08260) [1] [2] |
| **Line Spacing** | Default 3.75mm (1/6 inch) [1] |
| **Interfaces** | USB, LAN (Ethernet), RJ11 (Cash Drawer) [1] |
| **Operating Systems** | Windows, Linux [1] |
| **Command Set** | Standard ESC/POS Command Set [1] |

---

## Printing Processes & Workflows

To print successfully on the Tomate POS-80, follow this structured workflow:

```
[Determine Connection] ---> [Initialize Printer] ---> [Set Code Page] ---> [Send Format & Text] ---> [Feed & Cut]
```

### 1. Connection Methods
- **USB (Raw Access)**: Write raw bytes directly to the USB device file (e.g., `/dev/usb/lp0` on Linux) or use a spooler.
- **Ethernet (TCP/IP)**: Open a raw TCP socket to the printer's IP address on **Port 9100** (default raw print port).
- **Virtual Serial (COM)**: Communicate via virtual COM ports configured by the USB driver.

### 2. Character Encoding & Code Pages
Thermal printers use hardware code pages to print accented and special characters. For Portuguese (the primary language for Tomate devices in Brazil), configuring the correct code page is critical to avoid corrupted characters (like `` or random symbols) [11] [12].

1. **WPC1252 (Latin-1)**: Highly recommended for Portuguese. Select using command `ESC t 16` [9] [10].
2. **PC850 (Multilingual)**: Good fallback. Select using command `ESC t 2` [9].
3. **PC860 (Portuguese)**: Native Portuguese hardware page. Select using command `ESC t 3` [9] [13].

> **Crucial Rule**: When sending text, you **must** encode the string using the corresponding Python/Node.js codec (e.g., `cp1252`, `cp850`, or `cp860`) before converting it to raw bytes. Do not send UTF-8 strings directly!

### 3. Basic Formatting Command Quick-Reference
These are the most common ESC/POS control characters used for receipt layouts [3] [8]:

| Command | Hex Bytes | Description |
| :--- | :--- | :--- |
| **LF** | `0A` | Print and line feed [3] |
| **ESC @** | `1B 40` | Initialize printer (resets settings) [8] |
| **ESC a n** | `1B 61 n` | Alignment: `n=0` (Left), `n=1` (Center), `n=2` (Right) [8] |
| **ESC ! n** | `1B 21 n` | Master Print Mode (combine Font B, Bold, Double-Height, Double-Width, Underline) [4] |
| **GS ! n** | `1D 21 n` | Select character size (independent width/height magnification 1x to 8x) [7] |
| **GS V m n** | `1D 56 m n` | Feed and cut paper: `m=66` feeds `n` units and cuts partially [8] |

---

## Advanced Capabilities

For detailed implementations of advanced printer features, consult the child reference files bundled with this skill:

1. **Detailed Command Set**: See [references/commands.md](references/api_reference.md) for an exhaustive reference of all ESC/POS commands, hex codes, parameters, and behaviors supported by the POS-80.
2. **Special Characters & Encoding Map**: See [references/encoding.md](references/encoding.md) for character maps, code page tables, and explicit translation guidelines for Portuguese accents and special symbols.
3. **Barcodes & QR Codes**: See [references/barcodes.md](references/barcodes.md) for command syntaxes, sizing parameters, and error-correction levels for printing 1D barcodes and 2D QR codes natively.
4. **Receipt Layout Templates**: See [references/templates.md](references/templates.md) for production-ready, beautiful layout designs (retail receipts, restaurant orders, delivery tickets) optimized for 80mm paper width.

---

## Python Implementation Example

The recommended way to print programmatically is using Python's raw socket or file access. Below is a comprehensive helper class for raw ESC/POS printing on the Tomate POS-80:

```python
import socket

class TomatePOS80:
    def __init__(self, ip=None, port=9100, usb_path=None):
        self.ip = ip
        self.port = port
        self.usb_path = usb_path
        self.socket = None
        self.encoding = 'cp1252'  # Recommended for Portuguese (WPC1252)

    def connect(self):
        if self.ip:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.port))
        elif self.usb_path:
            self.file = open(self.usb_path, 'wb')

    def send_raw(self, data: bytes):
        if self.socket:
            self.socket.sendall(data)
        elif self.file:
            self.file.write(data)
            self.file.flush()

    def init_printer(self):
        self.send_raw(b'\x1b\x40')  # ESC @

    def set_code_page(self, page_id=16):
        # 16 = WPC1252 (Latin-1), 2 = PC850, 3 = PC860 (Portuguese)
        self.send_raw(b'\x1b\x74' + bytes([page_id]))
        if page_id == 16:
            self.encoding = 'cp1252'
        elif page_id == 2:
            self.encoding = 'cp850'
        elif page_id == 3:
            self.encoding = 'cp860'

    def write_line(self, text: str, align=0, bold=False, double_height=False, double_width=False):
        # Set alignment: 0=Left, 1=Center, 2=Right
        self.send_raw(b'\x1b\x61' + bytes([align]))
        
        # Set formatting using Master Print Mode (ESC !)
        mask = 0x00
        if bold: mask |= 0x08
        if double_height: mask |= 0x10
        if double_width: mask |= 0x20
        self.send_raw(b'\x1b\x21' + bytes([mask]))
        
        # Encode and send text
        encoded_text = text.encode(self.encoding, errors='replace')
        self.send_raw(encoded_text + b'\x0a')

    def feed_and_cut(self, lines=4):
        # Feed lines
        self.send_raw(b'\x1b\x64' + bytes([lines]))
        # Feed and cut partially (GS V 66 0)
        self.send_raw(b'\x1d\x56\x42\x00')

    def close(self):
        if self.socket:
            self.socket.close()
        elif self.file:
            self.file.close()
```

---

## References

[1] Tomate Official Website, *Impressora Térmica de Recibos 80mm MDK-080 Specifications*, https://tomate.tv/products/perifericos/impressoras/impressora-termica-de-recibos-80mm-mdk-080  
[2] Loja Tomate, *Impressora Térmica 80mm Tomate MDK-08260*, https://www.lojatomate.com.br/impressora-termica-80mm-240v-25a-tomate-mdk-08260  
[3] ZKTECO Colombia, *POS-80-Series Printer Programmer Manual (Control Commands)*, Page 2, https://zktecocolombia.com/wp-content/uploads/2025/08/Manual-de-Progamacion.pdf  
[4] ZKTECO Colombia, *POS-80-Series Printer Programmer Manual (ESC ! Print Mode)*, Page 8, https://zktecocolombia.com/wp-content/uploads/2025/08/Manual-de-Progamacion.pdf  
[5] ZKTECO Colombia, *POS-80-Series Printer Programmer Manual (ESC * Bit Image)*, Page 13, https://zktecocolombia.com/wp-content/uploads/2025/08/Manual-de-Progamacion.pdf  
[6] ZKTECO Colombia, *POS-80-Series Printer Programmer Manual (ESC t Code Table)*, Page 28, https://zktecocolombia.com/wp-content/uploads/2025/08/Manual-de-Progamacion.pdf  
[7] ZKTECO Colombia, *POS-80-Series Printer Programmer Manual (GS ! Char Size)*, Page 34, https://zktecocolombia.com/wp-content/uploads/2025/08/Manual-de-Progamacion.pdf  
[8] ZKTECO Colombia, *POS-80-Series Printer Programmer Manual (GS V Cut Paper)*, Page 41, https://zktecocolombia.com/wp-content/uploads/2025/08/Manual-de-Progamacion.pdf  
[9] Diginet, *80mm Thermal Printer Supported Code Pages*, https://www.diginet.gr/fileadmin/media/files/Ektypotes_Apodeikseon/ASSO/ASSO_SUPPORTED_CODEPAGES.pdf  
[10] Diebold Nixdorf, *P1200 Standard POS Printer Programming Manual (WPC1252 Latin-1)*, https://www.dieboldnixdorf.com/-/media/diebold/files/retail/peripherals-en/printers/p1200-prog-manual.pdf  
[11] StackOverflow, *Selecting character code table in ESC/POS command*, https://stackoverflow.com/questions/52390499/selecting-character-code-table-in-esc-pos-command  
[12] B4X Forum, *Portuguese characters in a ESC POS BT printer*, https://www.b4x.com/android/forum/threads/portuguese-characters-in-a-esc-pos-bt-printer.69646/  
[13] Ascii-Codes, *Code page 860 (Portuguese language) table reference*, https://www.ascii-codes.com/cp860.html  

---

## Adversarial Verification Panel

For each significant ESC/POS integration finding produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong ESC/POS integration findings from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Commands Agent, Encoding Agent, Barcodes Agent, Templates Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the Encoding Agent recommends using WPC1252 (ESC t 16) for all text, while the Templates Agent includes a layout that relies on PC860 box-drawing characters only available via ESC t 3)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified receipt integration blueprint so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
