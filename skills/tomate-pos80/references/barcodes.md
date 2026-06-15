# Tomate POS-80 Barcodes & QR Codes Guide

The Tomate POS-80 supports native, high-speed printing of 1D barcodes and 2D QR codes [1]. Utilizing hardware-rendered codes is significantly faster and sharper than printing them as raster images.

---

## 1. General Barcode Configuration Commands

Before printing a barcode, configure its height, width, and text visibility using these commands [1]:

### GS h n (Select Barcode Height)
- **ASCII**: `GS h n`
- **Hex**: `1D 68 n`
- **Decimal**: `29 104 n`
- **Range**: `1 ≤ n ≤ 255`
- **Description**: Sets the vertical height of the barcode in dots [1]. Default is `n = 162`.

### GS w n (Select Barcode Width)
- **ASCII**: `GS w n`
- **Hex**: `1D 77 n`
- **Decimal**: `29 119 n`
- **Range**: `2 ≤ n ≤ 6`
- **Description**: Sets the horizontal module width of the barcode elements [1].
  - `n = 2`: 0.25mm thin element width.
  - `n = 3`: 0.375mm thin element width (default).
  - `n = 4`: 0.50mm thin element width.

### GS H n (Select Text Printing Position)
- **ASCII**: `GS H n`
- **Hex**: `1D 48 n`
- **Decimal**: `29 72 n`
- **Range**: `0 ≤ n ≤ 3`, `48 ≤ n ≤ 51`
- **Description**: Selects where the Human Readable Interpretation (HRI) characters are printed [1]:
  - `n = 0, 48`: Not printed (default).
  - `n = 1, 49`: Printed above the barcode.
  - `n = 2, 50`: Printed below the barcode.
  - `n = 3, 51`: Printed both above and below.

---

## 2. Printing 1D Barcodes (GS k)

The printer supports two syntaxes for printing 1D barcodes. Syntax ② is highly recommended as it explicitly defines the data length `n`, preventing buffer reading issues [1].

### Command Syntax ②
```
ASCII:   GS k m n d1...dn
Hex:     1D 6B m n d1...dn
Decimal: 29 107 m n d1...dn
```

- **`m`**: Selects the barcode system [1].
- **`n`**: Specifies the number of characters in the barcode data [1].
- **`d1...dn`**: The actual character bytes to be encoded [1].

| System `m` | Barcode Type | Data Length `n` | Valid Characters |
| :---: | :--- | :--- | :--- |
| **`65`** | **UPC-A** | 11 to 12 | Numbers `0-9` (ASCII 48-57) |
| **`67`** | **EAN13** | 12 to 13 | Numbers `0-9` (ASCII 48-57) |
| **`68`** | **EAN8** | 7 to 8 | Numbers `0-9` (ASCII 48-57) |
| **`69`** | **CODE39** | 1 to 255 | Numbers `0-9`, Uppercase `A-Z`, Symbols: ` `, `$`, `%`, `+`, `-`, `.`, `/` |
| **`70`** | **ITF** (Interleaved 2 of 5) | 1 to 255 (even) | Numbers `0-9` (ASCII 48-57) |
| **`71`** | **CODABAR** | 1 to 255 | Numbers `0-9`, Letters `A-D`, Symbols: `$`, `+`, `-`, `.`, `/`, `:` |
| **`72`** | **CODE93** | 1 to 255 | Full ASCII set (0-127) |
| **`73`** | **CODE128** | 2 to 255 | Full ASCII set (0-127). Must start with a subset selector (e.g., `{A`, `{B`, `{C`) |

---

## 3. Printing 2D QR Codes (ESC Z)

The Tomate POS-80 utilizes a specific, highly efficient command `ESC Z` to print QR codes natively [1].

### Command Syntax
```
ASCII:   ESC Z m n k dL dH d1...dn
Hex:     1B 5A m n k dL dH d1...dn
Decimal: 27 90 m n k dL dH d1...dn
```

### Parameters
- **`m`**: Persist byte (usually set to `0` or `1`).
- **`n`**: Error Correction Level [1]:
  - `L` (7% recovery)
  - `M` (15% recovery)
  - `Q` (25% recovery)
  - `H` (30% recovery)
- **`k`**: Enlarge multiple (size of QR code module in dots, usually `3` to `8`) [1].
- **`dL dH`**: Data length specified as two bytes (`length = dL + dH * 256`) [1].
- **`d1...dn`**: The actual string data to encode in the QR code [1].

---

## 4. Python Implementation Examples

### 1D Barcode (EAN13) Example
```python
def print_ean13_barcode(socket_conn, code: str):
    if len(code) not in [12, 13]:
        raise ValueError("EAN13 barcode must be 12 or 13 digits long")
        
    # 1. Initialize printer
    socket_conn.sendall(b'\x1b\x40')
    
    # 2. Configure height (100 dots) and width (module size 3)
    socket_conn.sendall(b'\x1d\x68\x64') # GS h 100
    socket_conn.sendall(b'\x1d\x77\x03') # GS w 3
    
    # 3. Print text below barcode
    socket_conn.sendall(b'\x1d\x48\x02') # GS H 2
    
    # 4. Center align
    socket_conn.sendall(b'\x1b\x61\x01') # ESC a 1
    
    # 5. Send print barcode command (m=67 for EAN13)
    data_bytes = code.encode('ascii')
    header = b'\x1d\x6b\x43' + bytes([len(data_bytes)])
    socket_conn.sendall(header + data_bytes + b'\x0a')
```

### 2D QR Code Example
```python
def print_qr_code(socket_conn, data: str, size=4, ec_level=b'M'):
    # 1. Initialize printer
    socket_conn.sendall(b'\x1b\x40')
    
    # 2. Center align
    socket_conn.sendall(b'\x1b\x61\x01') # ESC a 1
    
    # 3. Prepare data length
    data_bytes = data.encode('utf-8')
    length = len(data_bytes)
    dL = length & 0xFF
    dH = (length >> 8) & 0xFF
    
    # 4. Build ESC Z command
    # \x1b\x5a = ESC Z
    # \x00 = persist byte
    # ec_level = L, M, Q, or H
    # size = module size multiple
    command = b'\x1b\x5a\x00' + ec_level + bytes([size]) + bytes([dL, dH]) + data_bytes
    
    # 5. Send command and line feed
    socket_conn.sendall(command + b'\x0a')
```

---

## References
[1] ZKTECO Colombia, *POS-80-Series Printer Programmer Manual (Barcodes)*, Pages 44-46, https://zktecocolombia.com/wp-content/uploads/2025/08/Manual-de-Progamacion.pdf
