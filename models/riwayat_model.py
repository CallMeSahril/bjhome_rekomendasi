# def simpan_riwayat(nama, data, jenis, db):
#     for item in data:
#         db.execute("""
#             INSERT INTO riwayat_rekomendasi (nama_pelanggan, produk_dipilih, jenis, nama_produk, skor)
#             VALUES (%s, %s, %s, %s, %s)
#         """, (nama, item["produk"], jenis, item["nama_produk"], item["skor"]))
