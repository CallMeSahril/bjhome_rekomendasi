from urllib.parse import quote

def generate_share_text(nama, cross, up):
    text = f"Hai {nama}, berikut rekomendasi produk dari pembelian Anda:\n\n"
    text += "🔵 Cross-Selling:\n"
    for i in cross:
        text += f"- {i['produk']} → {i['nama_produk']} (skor: {i['skor']})\n"
    text += "\n🔴 Up-Selling:\n"
    for i in up:
        text += f"- {i['produk']} → {i['nama_produk']} (skor: {i['skor']})\n"
    return text

def whatsapp_share_link(nama, cross, up):
    text = generate_share_text(nama, cross, up)
    return f"https://wa.me/?text={quote(text)}"
