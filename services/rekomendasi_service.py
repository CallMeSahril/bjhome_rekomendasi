from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models.produk_model import get_all_produk_with_fungsi
import pandas as pd
from db import get_connection


def get_rekomendasi(nama_produk):
    df = get_all_produk_with_fungsi()

    # Gabungkan fitur teks
    df["fitur"] = df[["kategori", "merek", "bahan", "ukuran", "warna"]].astype(
        str).agg(" ".join, axis=1)

    vectorizer = CountVectorizer()
    fitur_matrix = vectorizer.fit_transform(df["fitur"])
    similarity_matrix = cosine_similarity(fitur_matrix)

    produk_index = df.reset_index().set_index("nama_produk").to_dict()["index"]

    if nama_produk not in produk_index:
        return [], []

    idx = produk_index[nama_produk]
    ref = df.iloc[idx]
    ref_fungsi = ref["fungsi_produk"]
    ref_kategori = ref["kategori"]

    # Hitung skor kemiripan
    skor_kemiripan = list(enumerate(similarity_matrix[idx]))
    skor_kemiripan = sorted(
        skor_kemiripan, key=lambda x: x[1], reverse=True)[1:10]

    cross, up = [], []

    for i, skor in skor_kemiripan:
        if skor < 0.1:
            continue  # skip yang terlalu tidak mirip

        cmp = df.iloc[i]
        cmp_fungsi = cmp["fungsi_produk"]
        cmp_kategori = cmp["kategori"]

        # ✅ Prioritaskan filter fungsi terlebih dahulu
        if cmp_fungsi != ref_fungsi:
            continue  # beda fungsi? langsung skip (bukan cross-sell relevan)

        # 🔴 Up-Selling
        if ref_kategori == cmp_kategori and ref["ukuran"] != cmp["ukuran"]:
            up.append(
                {"nama_produk": cmp["nama_produk"], "skor": round(skor, 2)})

        # 🔵 Cross-Selling: beda kategori tapi fungsi sama
        elif cmp_kategori != ref_kategori:
            cross.append(
                {"nama_produk": cmp["nama_produk"], "skor": round(skor, 2)})

    return cross, up
def proses_transaksi_excel(file_path):
    import pandas as pd
    from db import get_connection

    print(f"🚀 Memproses file transaksi: {file_path}")
    df = pd.read_excel(file_path)
    conn = get_connection()
    cursor = conn.cursor()

    # Validasi kolom wajib
    for col in ["nama_pelanggan", "nama_produk"]:
        if col not in df.columns:
            raise KeyError(f"❌ Kolom '{col}' tidak ditemukan.")

    pelanggan = df["nama_pelanggan"].iloc[0]

    # Simpan transaksi
    cursor.execute("INSERT INTO transaksi (nama_pelanggan, tanggal) VALUES (%s, NOW())", (pelanggan,))
    transaksi_id = cursor.lastrowid
    print(f"📌 Transaksi ID baru: {transaksi_id}")

    # Hitung frekuensi pembelian
    frekuensi = df["nama_produk"].value_counts().reset_index()
    frekuensi.columns = ["nama_produk", "jumlah"]

    # Ambil semua produk + fungsi_produk
    cursor.execute("""
        SELECT p.nama_produk, p.kategori, p.merek, p.bahan, p.ukuran, p.warna, k.fungsi_produk
        FROM produk p 
        JOIN kategori k ON p.kategori = k.nama_kategori
    """)
    produk_list = [
        {
            "nama_produk": r[0],
            "kategori": r[1],
            "merek": r[2],
            "bahan": r[3],
            "ukuran": r[4],
            "warna": r[5],
            "fungsi_produk": r[6]
        }
        for r in cursor.fetchall()
    ]

    hasil = []
    hasil_display = []

    for _, row in frekuensi.iterrows():
        asal = row["nama_produk"]
        p1 = next((p for p in produk_list if p["nama_produk"] == asal), None)
        if not p1:
            print(f"⚠️ Produk '{asal}' tidak ditemukan.")
            continue

        for p2 in produk_list:
            if p2["nama_produk"] == asal or p1["fungsi_produk"] != p2["fungsi_produk"]:
                continue

            skor = sum([
                0.5 if p1["kategori"] == p2["kategori"] else 0,
                0.3 if p1["merek"] == p2["merek"] else 0,
                0.2 if p1["bahan"] == p2["bahan"] else 0
            ])

            if skor > 0:
                jenis = "up" if p1["kategori"] == p2["kategori"] else "cross"
                hasil.append((transaksi_id, asal, p2["nama_produk"], jenis, round(skor, 2)))

                # Buat dict untuk ditampilkan di HTML
                hasil_display.append({
                    "nama_produk": p2["nama_produk"],
                    "kategori": p2["kategori"],
                    "merek": p2["merek"],
                    "bahan": p2["bahan"],
                    "ukuran": p2["ukuran"],
                    "warna": p2["warna"],
                    "skor": round(skor, 2)
                })

    for row in hasil:
        try:
            cursor.execute("""
                INSERT INTO hasil_rekomendasi
                (transaksi_id, produk_asal, produk_rekomendasi, jenis, skor, tanggal)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, row)
        except Exception as e:
            print(f"❌ Gagal insert hasil rekomendasi: {e}")

    conn.commit()
    conn.close()

    print(f"✅ Proses selesai. Jumlah rekomendasi: {len(hasil)}")
    print("🔍 Rekomendasi:", hasil_display)
    return hasil_display
