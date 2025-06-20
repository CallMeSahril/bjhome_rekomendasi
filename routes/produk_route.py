from flask import Blueprint, render_template, request, redirect, url_for
from models.produk_model import get_all_produk, get_produk_by_id, insert_produk, update_produk, delete_produk

produk_bp = Blueprint("produk_bp", __name__)


@produk_bp.route("/produk")
def list_produk():
    data = get_all_produk()
    return render_template("produk_list.html", data=data)


@produk_bp.route("/produk/add", methods=["GET", "POST"])
def tambah_produk():
    if request.method == "POST":
        insert_produk(request.form)
        return redirect(url_for("produk_bp.list_produk"))
    return render_template("produk_form.html", title="Tambah Produk", produk={})


@produk_bp.route("/produk/edit/<int:id>", methods=["GET", "POST"])
def edit_produk(id):
    produk = get_produk_by_id(id)
    if request.method == "POST":
        update_produk(id, request.form)
        return redirect(url_for("produk_bp.list_produk"))
    return render_template("produk_form.html", title="Edit Produk", produk=produk)


@produk_bp.route("/produk/delete/<int:id>", methods=["POST"])
def hapus_produk(id):
    delete_produk(id)
    return redirect(url_for("produk_bp.list_produk"))
