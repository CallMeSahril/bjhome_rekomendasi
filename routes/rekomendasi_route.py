from flask import Blueprint, request, render_template
from models.produk_model import get_all_produk
from services.rekomendasi_service import get_rekomendasi

rekomendasi_bp = Blueprint("rekomendasi_bp", __name__)


@rekomendasi_bp.route("/rekomendasi", methods=["GET", "POST"])
def rekomendasi():
    df = get_all_produk()
    produk_list = df["nama_produk"].tolist()
    selected = None
    cross = []
    up = []

    if request.method == "POST":
        selected = request.form.get("produk")
        cross, up = get_rekomendasi(selected)

    return render_template("rekomendasi.html", produk_list=produk_list, selected=selected, cross=cross, up=up)
