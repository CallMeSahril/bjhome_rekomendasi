from flask import Blueprint, render_template
from db import get_connection

home_bp = Blueprint("home_bp", __name__)


@home_bp.route("/")
def login():
    return render_template("login.html")


@home_bp.route("/dashboard")
def dashboard():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM produk")
    total_produk = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM kategori")
    total_kategori = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM transaksi")
    total_transaksi = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM hasil_rekomendasi")
    total_rekomendasi = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM hasil_rekomendasi WHERE jenis = 'up'")
    total_up = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM hasil_rekomendasi WHERE jenis = 'cross'")
    total_cross = cur.fetchone()[0]

    cur.execute("""
        SELECT produk_rekomendasi, COUNT(*) AS jumlah
        FROM hasil_rekomendasi
        WHERE jenis = 'up'
        GROUP BY produk_rekomendasi
        ORDER BY jumlah DESC
        LIMIT 5
    """)
    top_upselling = cur.fetchall()

    cur.execute("""
        SELECT produk_rekomendasi, COUNT(*) AS jumlah
        FROM hasil_rekomendasi
        WHERE jenis = 'cross'
        GROUP BY produk_rekomendasi
        ORDER BY jumlah DESC
        LIMIT 5
    """)
    top_crosselling = cur.fetchall()

    conn.close()

    return render_template("dashboard.html",
                           total_produk=total_produk,
                           total_kategori=total_kategori,
                           total_transaksi=total_transaksi,
                           total_rekomendasi=total_rekomendasi,
                           total_up=total_up,
                           total_cross=total_cross,
                           top_upselling=top_upselling,
                           top_crosselling=top_crosselling)
