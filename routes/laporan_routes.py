from flask import Blueprint, render_template
from models.produk_model import get_all_produk
from models.kategori_model import get_all_kategori
from models.riwayat_model import get_all_riwayat
from models.riwayat_model import get_statistik_top_produk


from flask import send_file
import pandas as pd
from io import BytesIO

laporan_bp = Blueprint("laporan_bp", __name__)


@laporan_bp.route("/laporan")
def laporan_menu():
    return render_template("laporan/laporan.html")


@laporan_bp.route("/laporan/produk")
def cetak_produk():
    produk = get_all_produk()
    df = pd.DataFrame(produk)  # asumsi: list of dicts
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Produk')
    output.seek(0)
    return send_file(output,
                     download_name="laporan_produk.xlsx",
                     as_attachment=True,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@laporan_bp.route("/laporan/kategori")
def cetak_kategori():
    kategori = get_all_kategori()
    df = pd.DataFrame(kategori)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Kategori')
    output.seek(0)
    return send_file(output, download_name="laporan_kategori.xlsx", as_attachment=True,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@laporan_bp.route("/laporan/riwayat")
def cetak_riwayat():
    riwayat = get_all_riwayat()
    df = pd.DataFrame(riwayat)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Riwayat')
    output.seek(0)
    return send_file(output, download_name="laporan_riwayat.xlsx", as_attachment=True,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@laporan_bp.route("/laporan/statistik")
def cetak_statistik():
    statistik = get_statistik_top_produk()
    df = pd.DataFrame(statistik)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Statistik')
    output.seek(0)
    return send_file(output, download_name="laporan_statistik.xlsx", as_attachment=True,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
