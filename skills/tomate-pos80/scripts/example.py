#!/usr/bin/env python3
"""
Tomate POS-80 Thermal Printer Integration Example.
This script demonstrates how to construct and send raw ESC/POS commands
including custom formatting, Portuguese accents, barcodes, and QR codes
to a Tomate POS-80 printer over a network (TCP/IP Port 9100).
"""

import sys
import socket

# Mock Socket class for local dry-run testing
class MockSocket:
    def sendall(self, data):
        # Simply prints the raw bytes in hex/ascii representation
        print(f"[RAW BYTES SENT]: {data}")
    def close(self):
        print("[SOCKET CLOSED]")

def generate_sample_receipt():
    """
    Generates a full raw ESC/POS receipt byte-stream with WPC1252 (Latin-1) encoding
    for correct Portuguese accents, custom alignments, bold styling, a native barcode,
    and a native QR code.
    """
    b = []
    
    # --- STEP 1: INITIALIZE & SELECT CODE PAGE ---
    b.append(b'\x1b\x40')      # ESC @ (Initialize printer)
    b.append(b'\x1b\x74\x10')  # ESC t 16 (Select WPC1252 / Windows Latin-1)
    
    # --- STEP 2: HEADER (Centered, Bold, Double-Height) ---
    b.append(b'\x1b\x61\x01')  # ESC a 1 (Center Alignment)
    b.append(b'\x1b\x21\x18')  # ESC ! 24 (Bold + Double-Height)
    b.append("SUPERMERCADO TOMATE\n".encode('cp1252'))
    
    # Reset Formatting
    b.append(b'\x1b\x21\x00')  # ESC ! 0 (Normal size, reset)
    b.append("Av. Brasil, 1500 - São Paulo, SP\n".encode('cp1252'))
    b.append("CNPJ: 11.222.333/0001-44\n".encode('cp1252'))
    b.append("------------------------------------------------\n".encode('cp1252'))
    
    # --- STEP 3: TRANSACTION DETAILS (Left Aligned) ---
    b.append(b'\x1b\x61\x00')  # ESC a 0 (Left Alignment)
    b.append("Data: 31/05/2026 15:45:10   PDV: 02\n".encode('cp1252'))
    b.append("================================================\n".encode('cp1252'))
    
    # Table Header (48 columns)
    # Qtd (5 cols) + Item (31 cols) + Valor (12 cols) = 48 cols
    b.append(f"{'Qtd':<5}{'Item':<31}{'Valor (R$)':>12}\n".encode('cp1252'))
    b.append("------------------------------------------------\n".encode('cp1252'))
    
    # Items
    items = [
        (2, "Café Premium Moído 500g", 18.90),
        (1, "Pão de Forma Integral", 8.50),
        (3, "Sabonete Líquido Hidratante", 6.20),
        (1, "Água Mineral Sem Gás 1.5L", 3.00)
    ]
    
    subtotal = 0.0
    for qty, name, price in items:
        item_total = qty * price
        subtotal += item_total
        price_str = f"{item_total:.2f}".replace('.', ',')
        # Truncate item name if too long to fit in 31 characters
        if len(name) > 29:
            name = name[:27] + ".."
        line = f"{qty:<5}{name:<31}{price_str:>12}\n"
        b.append(line.encode('cp1252'))
        
    b.append("------------------------------------------------\n".encode('cp1252'))
    
    # --- STEP 4: TOTALS ---
    sub_str = f"{subtotal:.2f}".replace('.', ',')
    discount = 5.00
    disc_str = f"{discount:.2f}".replace('.', ',')
    total = subtotal - discount
    tot_str = f"{total:.2f}".replace('.', ',')
    
    b.append(f"{'Subtotal:':<30}{'R$ ' + sub_str:>18}\n".encode('cp1252'))
    b.append(f"{'Desconto Especial:':<30}{'R$ ' + disc_str:>18}\n".encode('cp1252'))
    
    # Total in Bold + Double-Width
    b.append(b'\x1b\x21\x28')  # ESC ! 40 (Bold + Double-Width)
    b.append(f"{'TOTAL:':<15}{'R$ ' + tot_str:>9}\n".encode('cp1252'))
    b.append(b'\x1b\x21\x00')  # Reset to normal
    
    b.append("================================================\n".encode('cp1252'))
    b.append(f"{'Forma de Pagamento:':<30}{'Cartão de Crédito':>18}\n".encode('cp1252'))
    b.append("------------------------------------------------\n".encode('cp1252'))
    
    # --- STEP 5: BARCODE & QR CODE (Centered) ---
    b.append(b'\x1b\x61\x01')  # ESC a 1 (Center Alignment)
    b.append("Acesse a NFC-e pelo QR Code abaixo:\n\n".encode('cp1252'))
    
    # Native QR Code (ESC Z)
    qr_data = "https://www.sefaz.sp.gov.br/nfce?id=123456789"
    qr_bytes = qr_data.encode('utf-8')
    length = len(qr_bytes)
    dL = length & 0xFF
    dH = (length >> 8) & 0xFF
    # ESC Z \x00 M(EC Level) \x04(Size 4)
    b.append(b'\x1b\x5a\x00\x4d\x04' + bytes([dL, dH]) + qr_bytes + b'\n\n')
    
    # Native Barcode (EAN13)
    b.append("Código do Cliente:\n".encode('cp1252'))
    b.append(b'\x1d\x68\x50')  # GS h 80 (Height 80 dots)
    b.append(b'\x1d\x77\x03')  # GS w 3 (Width module 3)
    b.append(b'\x1d\x48\x02')  # GS H 2 (HRI text below barcode)
    # GS k 67 12 d1...d12 (EAN13 print barcode)
    barcode_data = "789123456789"
    b.append(b'\x1d\x6b\x43\x0c' + barcode_data.encode('ascii') + b'\n')
    
    # --- STEP 6: FEED & CUT ---
    b.append(b'\x1b\x64\x04')  # ESC d 4 (Feed 4 lines)
    b.append(b'\x1d\x56\x42\x00') # GS V 66 0 (Feed to cut line and partial cut)
    
    return b''.join(b)

def print_receipt(ip=None, port=9100, dry_run=False):
    """
    Connects to the printer and transmits the generated receipt byte-stream.
    """
    receipt_bytes = generate_sample_receipt()
    
    if dry_run or not ip:
        print("--- RUNNING DRY-RUN MODE (OUTPUTTING BYTES TO CONSOLE) ---")
        conn = MockSocket()
        conn.sendall(receipt_bytes)
        conn.close()
        return
        
    print(f"Connecting to Tomate POS-80 at {ip}:{port}...")
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.settimeout(5.0)
        conn.connect((ip, port))
        print("Connected! Sending print data...")
        conn.sendall(receipt_bytes)
        print("Data sent successfully!")
    except Exception as e:
        print(f"Error communicating with printer: {e}", file=sys.stderr)
    finally:
        conn.close()

if __name__ == "__main__":
    # If IP is provided as argument, attempt real print; otherwise run console dry-run
    printer_ip = sys.argv[1] if len(sys.argv) > 1 else None
    print_receipt(ip=printer_ip, dry_run=(printer_ip is None))
