from flask import Blueprint, request, redirect, render_template
from models import kategori_model

kategori_bp = Blueprint("kategori_bp", __name__)

@kategori_bp.route("/kategori")
def list_kategori():
    data = kategori_model.get_all_kategori()
    return render_template("kategori/index.html", data=data)

@kategori_bp.route("/kategori/tambah", methods=["GET", "POST"])
def tambah_kategori():
    if request.method == "POST":
        nama = request.form["nama_kategori"]
        fungsi = request.form["fungsi_produk"]
        kategori_model.insert_kategori(nama, fungsi)
        return redirect("/kategori")
    return render_template("kategori/form.html", kategori={})

@kategori_bp.route("/kategori/edit/<int:id>", methods=["GET", "POST"])
def edit_kategori(id):
    kategori = kategori_model.get_kategori_by_id(id)
    if request.method == "POST":
        nama = request.form["nama_kategori"]
        fungsi = request.form["fungsi_produk"]
        kategori_model.update_kategori(id, nama, fungsi)
        return redirect("/kategori")
    return render_template("kategori/form.html", kategori=kategori)

@kategori_bp.route("/kategori/hapus/<int:id>", methods=["POST"])
def hapus_kategori(id):
    kategori_model.delete_kategori(id)
    return redirect("/kategori")
