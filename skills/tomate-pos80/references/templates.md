# Tomate POS-80 Receipt Layout Templates

Designing beautiful, well-aligned receipts is crucial for a professional point-of-sale experience. On an 80mm paper width printer with a 72mm printable area, the default font A (12x24 dots) provides exactly **48 characters per line** [1]. This document contains standard templates optimized for this 48-column layout.

---

## 1. 48-Column Grid Layout Strategy

To design clean receipts, treat your line buffer as a 48-column grid. Standard structural elements should be spaced as follows:

- **Full-width Separator Line**: `------------------------------------------------` (48 hyphens)
- **Double Separator Line**: `================================================` (48 equals signs)
- **Three-Column Table (Qty, Item, Price)**:
  - Column 1 (Qty): Left-aligned, 5 characters (`%-5s`)
  - Column 2 (Item): Left-aligned, 31 characters (`%-31s`)
  - Column 3 (Price): Right-aligned, 12 characters (`%12s`)
  - Format string: `%-5s%-31s%12s` (Total: 48 characters)
- **Two-Column Table (Label, Value)**:
  - Column 1 (Label): Left-aligned, 30 characters (`%-30s`)
  - Column 2 (Value): Right-aligned, 18 characters (`%18s`)
  - Format string: `%-30s%18s` (Total: 48 characters)

---

## 2. Standard Retail Receipt Template

Below is a Python generator that outputs raw ESC/POS bytes for a beautiful, standard retail receipt containing Portuguese text and accents [2] [3]:

```python
def generate_retail_receipt(items, subtotal, discount, total, payment_method):
    # Initialize list of bytes
    b = []
    
    # 1. Initialize & Select Code Page WPC1252
    b.append(b'\x1b\x40')      # ESC @ (Initialize)
    b.append(b'\x1b\x74\x10')  # ESC t 16 (WPC1252)
    
    # 2. Header (Centered, Bold, Double-Height)
    b.append(b'\x1b\x61\x01')  # Center
    b.append(b'\x1b\x21\x18')  # Bold + Double-Height
    b.append("LOJAS TOMATE LTDA\n".encode('cp1252'))
    
    # Subheader (Normal size)
    b.append(b'\x1b\x21\x00')  # Reset format
    b.append("Av. Paulista, 1000 - São Paulo, SP\n".encode('cp1252'))
    b.append("CNPJ: 12.345.678/0001-90\n".encode('cp1252'))
    b.append("------------------------------------------------\n".encode('cp1252'))
    
    # 3. Transaction Meta (Left-aligned)
    b.append(b'\x1b\x61\x00')  # Left
    b.append("Cupom Fiscal Eletrônico - NFC-e\n".encode('cp1252'))
    b.append("Data: 31/05/2026 14:30:15   Série: 001\n".encode('cp1252'))
    b.append("================================================\n".encode('cp1252'))
    
    # Table Header
    b.append(f"{'Qtd':<5}{'Item':<31}{'Valor (R$)':>12}\n".encode('cp1252'))
    b.append("------------------------------------------------\n".encode('cp1252'))
    
    # 4. Items List
    for qty, name, price in items:
        # Format price as string
        price_str = f"{price:.2f}".replace('.', ',')
        # If item name is too long, truncate it to 29 chars and add '..'
        if len(name) > 29:
            name = name[:27] + ".."
        line = f"{qty:<5}{name:<31}{price_str:>12}\n"
        b.append(line.encode('cp1252'))
        
    b.append("------------------------------------------------\n".encode('cp1252'))
    
    # 5. Totals Section
    sub_str = f"{subtotal:.2f}".replace('.', ',')
    disc_str = f"{discount:.2f}".replace('.', ',')
    tot_str = f"{total:.2f}".replace('.', ',')
    
    b.append(f"{'Subtotal:':<30}{'R$ ' + sub_str:>18}\n".encode('cp1252'))
    b.append(f"{'Desconto:':<30}{'R$ ' + disc_str:>18}\n".encode('cp1252'))
    
    # Total (Bold + Double-Width)
    b.append(b'\x1b\x21\x28')  # Bold + Double-Width
    b.append(f"{'TOTAL:':<15}{'R$ ' + tot_str:>9}\n".encode('cp1252'))
    b.append(b'\x1b\x21\x00')  # Reset
    
    b.append("------------------------------------------------\n".encode('cp1252'))
    b.append(f"{'Forma de Pagamento:':<30}{payment_method:>18}\n".encode('cp1252'))
    b.append("================================================\n".encode('cp1252'))
    
    # 6. Footer & QR Code Placeholder
    b.append(b'\x1b\x61\x01')  # Center
    b.append("Obrigado pela preferência!\n".encode('cp1252'))
    b.append("Consulte sua NFC-e pelo QR Code abaixo:\n\n".encode('cp1252'))
    
    # Native QR Code command (ESC Z)
    # Encodes a dummy URL for the NFC-e invoice portal
    qr_data = "https://www.fazenda.sp.gov.br/nfce/qrcode?p=123456"
    qr_bytes = qr_data.encode('utf-8')
    length = len(qr_bytes)
    dL = length & 0xFF
    dH = (length >> 8) & 0xFF
    # \x1b\x5a\x00\x4d\x04 = ESC Z \x00 M(Error Correction) \x04(Size 4)
    b.append(b'\x1b\x5a\x00\x4d\x04' + bytes([dL, dH]) + qr_bytes + b'\n')
    
    # 7. Feed and Cut (GS V 66 0)
    b.append(b'\x1b\x64\x04')  # Feed 4 lines
    b.append(b'\x1d\x56\x42\x00') # Cut partially
    
    return b''.join(b)
```

---

## 3. Food Delivery / Restaurant Order Template

Restaurant orders require larger text for item quantities and modifiers to prevent preparation mistakes in noisy kitchen environments [1].

```python
def generate_kitchen_ticket(order_id, table, items):
    b = []
    
    # Initialize & Select Code Page WPC1252
    b.append(b'\x1b\x40')
    b.append(b'\x1b\x74\x10')
    
    # Header (Centered, Bold, Double-Height, Double-Width)
    b.append(b'\x1b\x61\x01')  # Center
    b.append(b'\x1b\x21\x38')  # Bold + Double-Height + Double-Width
    b.append(f"PEDIDO #{order_id}\n".encode('cp1252'))
    
    # Table Info
    b.append(b'\x1b\x21\x30')  # Double-Height + Double-Width
    b.append(f"MESA: {table}\n".encode('cp1252'))
    b.append(b'\x1b\x21\x00')  # Reset
    b.append("------------------------------------------------\n".encode('cp1252'))
    
    # Time
    b.append(b'\x1b\x61\x00')  # Left
    b.append("Hora do Pedido: 31/05/2026 21:15:00\n".encode('cp1252'))
    b.append("================================================\n".encode('cp1252'))
    
    # Items
    for qty, item_name, modifiers in items:
        # Quantity & Name (Bold + Double-Height)
        b.append(b'\x1b\x21\x18')  # Bold + Double-Height
        b.append(f"{qty}x {item_name}\n".encode('cp1252'))
        
        # Modifiers (Normal size, indented, italicized/underlined if needed)
        if modifiers:
            b.append(b'\x1b\x21\x00')  # Reset to normal
            for mod in modifiers:
                b.append(f"  * OBS: {mod}\n".encode('cp1252'))
        
        b.append(b'\x1b\x21\x00')  # Reset
        b.append("------------------------------------------------\n".encode('cp1252'))
        
    # Feed & Cut
    b.append(b'\x1b\x64\x04')
    b.append(b'\x1d\x56\x42\x00')
    
    return b''.join(b)
```

---

## References
[1] ZKTECO Colombia, *POS-80-Series Printer Programmer Manual (Formatting)*, Page 34, https://zktecocolombia.com/wp-content/uploads/2025/08/Manual-de-Progamacion.pdf  
[2] Tomate Official Website, *Impressora Térmica de Recibos 80mm MDK-080*, https://tomate.tv/products/perifericos/impressoras/impressora-termica-de-recibos-80mm-mdk-080  
[3] Loja Tomate, *Impressora Térmica 80mm Tomate MDK-08260*, https://www.lojatomate.com.br/impressora-termica-80mm-240v-25a-tomate-mdk-08260
