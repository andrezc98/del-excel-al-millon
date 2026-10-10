"""Render a fictional Peruvian receipt for the Textract demo. Every name and number is invented."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LINES = [
    "BODEGA DOÑA ROSA",
    "Av. Túpac Amaru 210, Rímac, Lima",
    "RUC 10000000001 (ficticio)",
    "",
    "BOLETA DE VENTA ELECTRÓNICA",
    "B001-000742",
    "Fecha: 18/09/2026   Hora: 19:42",
    "--------------------------------",
    "CANT DESCRIPCIÓN          IMPORTE",
    " 2   Pan francés x6         3.00",
    " 1   Leche evaporada        4.20",
    " 1   Arroz 1 kg             4.50",
    " 3   Huevos x6              9.90",
    " 1   Gaseosa 1.5 L          6.50",
    "--------------------------------",
    "OP. GRAVADA              S/ 23.81",
    "IGV 18%                  S/  4.29",
    "TOTAL                    S/ 28.10",
    "",
    "Pago: Efectivo",
    "¡Gracias por su compra!",
]

font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 26)
w, lh, pad = 620, 38, 40
img = Image.new("RGB", (w, pad * 2 + lh * len(LINES)), "white")
d = ImageDraw.Draw(img)
for i, line in enumerate(LINES):
    x = (w - d.textlength(line, font=font)) / 2 if i < 7 or i > 18 else pad
    d.text((x, pad + i * lh), line, fill="black", font=font)
out = Path(__file__).resolve().parents[1] / "demo/muestras/facturas/boleta-bodega.png"
img.save(out)
print(out)
