# routes/riwayat_routes.py

from flask import Blueprint, render_template
from db import get_connection
import pandas as pd

riwayat_bp = Blueprint("riwayat_bp", __name__)

@riwayat_bp.route("/riwayat/")
def list_riwayat():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM hasil_rekomendasi ORDER BY tanggal DESC", conn)
    conn.close()
    return render_template("riwayat.html", data=df)
