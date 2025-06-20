from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def export_rekomendasi_pdf(nama, cross, up, path="static/laporan_rekomendasi.pdf"):
    c = canvas.Canvas(path, pagesize=A4)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 800, f"Laporan Rekomendasi Produk untuk {nama}")
    y = 770

    c.setFont("Helvetica", 12)
    c.drawString(50, y, "🔵 Cross-Selling:")
    y -= 20
    for i in cross:
        c.drawString(70, y, f"{i['produk']} → {i['nama_produk']} (skor: {i['skor']})")
        y -= 18

    y -= 10
    c.drawString(50, y, "🔴 Up-Selling:")
    y -= 20
    for i in up:
        c.drawString(70, y, f"{i['produk']} → {i['nama_produk']} (skor: {i['skor']})")
        y -= 18

    c.save()
    return path
