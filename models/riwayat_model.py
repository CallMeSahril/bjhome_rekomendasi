import pandas as pd
from db import get_connection


def get_all_riwayat():
    conn = get_connection()
    query = """
        SELECT id, transaksi_id, produk_asal, produk_rekomendasi, jenis, skor, tanggal
        FROM hasil_rekomendasi
        ORDER BY tanggal DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def get_statistik_top_produk(limit=10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            produk_rekomendasi AS nama_produk,
            COUNT(*) AS total,
            jenis AS tipe
        FROM hasil_rekomendasi
        GROUP BY produk_rekomendasi, jenis
        ORDER BY total DESC
        LIMIT %s
    """
    cursor.execute(query, (limit,))
    result = cursor.fetchall()
    conn.close()
    return result
