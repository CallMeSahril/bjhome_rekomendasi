from flask import Blueprint, render_template, request, redirect, flash, send_file
import pandas as pd
import os
from werkzeug.utils import secure_filename
from services.rekomendasi_service import proses_transaksi_excel
import io
transaksi_bp = Blueprint("transaksi_bp", __name__)
UPLOAD_FOLDER = "uploads"


@transaksi_bp.route("/transaksi/upload", methods=["GET", "POST"])
def upload_transaksi():
    if request.method == "POST":
        try:
            file = request.files['file']
            print("📥 File diterima:", file.filename)

            if file and file.filename.endswith('.xlsx'):
                filename = secure_filename(file.filename)
                print("🧼 Nama file aman:", filename)

                # Buat folder jika belum ada
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(path)
                print("💾 File disimpan di:", path)

                # Proses file Excel
                print("🚀 Memproses file transaksi...")
                rekomendasi = proses_transaksi_excel(path)
                print("✅ Proses selesai. Jumlah rekomendasi:", len(rekomendasi))
                print("🔍 Rekomendasi:", rekomendasi)
                flash("Data transaksi berhasil diproses dan rekomendasi disimpan.")
                return render_template("upload_transaksi.html", rekomendasi=rekomendasi)

            else:
                print("⚠️ Format file salah atau tidak ada file")
                flash("Format file harus .xlsx!")
                return render_template("upload_transaksi.html")

        except Exception as e:
            print("❌ ERROR saat upload/proses:", str(e))
            flash(f"Terjadi kesalahan: {str(e)}")
            return render_template("upload_transaksi.html")

    # GET method
    print("📄 Halaman upload transaksi dibuka (GET)")
    return render_template("upload_transaksi.html")


@transaksi_bp.route("/transaksi/template")
def download_template():

    df = pd.DataFrame([
    {
        "nama_pelanggan": "Budi Santoso",
        "nama_produk": "Cat Avitex Interior 10L",
        "kategori": "Cat",
        "merek": "Avitex",
        "bahan": "Akrilik",
        "ukuran": "10L",
        "warna": "Putih",
        "tanggal_transaksi": "2025-06-20",
        "jumlah": 2
    },
    {
        "nama_pelanggan": "Budi Santoso",
        "nama_produk": "Semen Tiga Roda 40Kg",
        "kategori": "Semen",
        "merek": "Tiga Roda",
        "bahan": "Semen",
        "ukuran": "40Kg",
        "warna": "Abu",
        "tanggal_transaksi": "2025-06-20",
        "jumlah": 5
    },
   
  
    ])


    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Template")

    output.seek(0)
    return send_file(
        output,
        download_name="template_transaksi.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
