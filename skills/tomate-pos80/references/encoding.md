# Tomate POS-80 Character Encoding & Special Characters Map

Accented characters and special symbols can print incorrectly on thermal receipt printers if the correct code page is not selected and the string is not encoded with the matching codec [1] [2]. This document provides a complete guide to selecting and using the correct code pages on the Tomate POS-80.

---

## 1. Character Code Table Selection Command

The `ESC t n` command is used to switch between different hardware code pages built into the printer's ROM [3].

```
ASCII:   ESC t n
Hex:     1B 74 n
Decimal: 27 116 n
```

The parameter `n` selects the active code page [3]. The table below lists the relevant pages supported by the Tomate POS-80:

| Parameter `n` | Code Page Name | Target Language / Region | Python Codec |
| :--- | :--- | :--- | :--- |
| **`0`** | **PC437** | Standard US & Western Europe (Default) | `cp437` |
| **`2`** | **PC850** | Multilingual (Latin-1) | `cp850` |
| **`3`** | **PC860** | Portuguese | `cp860` |
| **`16`** | **WPC1252** | Windows Latin-1 (Highly Recommended) | `cp1252` |
| **`19`** | **PC858** | Multilingual with Euro Symbol | `cp858` |

---

## 2. Recommended Configuration for Portuguese (Brazil)

Since Tomate is a brand primarily distributed in Brazil, Portuguese character encoding is the most common integration requirement [4]. 

### The Problem
If you send standard UTF-8 strings like `"R$ 15,00 - Café com Pão"` directly to the printer, it will print as `"R$ 15,00 - CafÃ© com P\u00e3o"` or show random graphical characters.

### The Solution
To print Portuguese accents (`á`, `é`, `í`, `ó`, `ú`, `â`, `ê`, `ô`, `ã`, `õ`, `ç`) correctly, you must:
1. Initialize the printer using `ESC @` (`1B 40`) [3].
2. Select the **WPC1252** code page using `ESC t 16` (`1B 74 10`) [3].
3. Encode your text string using the `cp1252` codec before sending the raw bytes to the printer.

---

## 3. Portuguese Character Map (WPC1252 / CP1252)

When using `WPC1252` (`ESC t 16`), characters map directly to the standard Windows-1252 character set. Below are the hex values for Portuguese characters:

| Character | Hex Value (WPC1252) | Character | Hex Value (WPC1252) |
| :---: | :---: | :---: | :---: |
| **`á`** | `E1` | **`Á`** | `C1` |
| **`é`** | `E9` | **`É`** | `C9` |
| **`í`** | `ED` | **`Í`** | `CD` |
| **`ó`** | `F3` | **`Ó`** | `D3` |
| **`ú`** | `FA` | **`Ú`** | `DA` |
| **`â`** | `E2` | **`Â`** | `C2` |
| **`ê`** | `EA` | **`Ê`** | `CA` |
| **`ô`** | `F4` | **`Ô`** | `D4` |
| **`ã`** | `E3` | **`Ã`** | `C3` |
| **`õ`** | `F5` | **`Õ`** | `D5` |
| **`ç`** | `E7` | **`Ç`** | `C7` |
| **`º`** | `BA` | **`ª`** | `AA` |

---

## 4. Alternative: PC860 (Portuguese Hardware Page)

If WPC1252 is not available or supported by a specific legacy software driver, you can use the native **PC860** Portuguese hardware page by sending `ESC t 3` [3]. Below is the character translation map for PC860:

| Character | Hex Value (PC860) | Character | Hex Value (PC860) |
| :---: | :---: | :---: | :---: |
| **`á`** | `A0` | **`Á`** | `C1` (spelled out or custom mapped) |
| **`é`** | `82` | **`É`** | `90` |
| **`í`** | `A1` | **`Í`** | `D6` |
| **`ó`** | `A2` | **`Ó`** | `E3` |
| **`ú`** | `A3` | **`Ú`** | `E2` |
| **`â`** | `83` | **`Â`** | `C2` |
| **`ê`** | `88` | **`Ê`** | `D2` |
| **`ô`** | `93` | **`Ô`** | `E5` |
| **`ã`** | `C6` | **`Ã`** | `C7` |
| **`õ`** | `C4` | **`Õ`** | `C5` |
| **`ç`** | `87` | **`Ç`** | `80` |

---

## 5. Python Implementation Code

Always wrap your text outputs in an encoding function to guarantee correct transmission:

```python
def print_portuguese_line(socket_connection, text: str):
    # 1. Initialize printer
    socket_connection.sendall(b'\x1b\x40')
    
    # 2. Select WPC1252 code page
    socket_connection.sendall(b'\x1b\x74\x10')
    
    # 3. Encode string to cp1252 bytes and append Line Feed
    raw_bytes = text.encode('cp1252', errors='replace') + b'\x0a'
    
    # 4. Send to printer
    socket_connection.sendall(raw_bytes)
```

---

## References
[1] StackOverflow, *Selecting character code table in ESC/POS command*, https://stackoverflow.com/questions/52390499/selecting-character-code-table-in-esc-pos-command  
[2] B4X Forum, *Portuguese characters in a ESC POS BT printer*, https://www.b4x.com/android/forum/threads/portuguese-characters-in-a-esc-pos-bt-printer.69646/  
[3] ZKTECO Colombia, *POS-80-Series Printer Programmer Manual (ESC t)*, Page 28, https://zktecocolombia.com/wp-content/uploads/2025/08/Manual-de-Progamacion.pdf  
[4] Tomate Official Website, *Impressora Térmica de Recibos 80mm MDK-080*, https://tomate.tv/products/perifericos/impressoras/impressora-termica-de-recibos-80mm-mdk-080
