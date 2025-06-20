
from flask import Flask
from routes.home_route import home_bp
from routes.rekomendasi_route import rekomendasi_bp
from routes.produk_route import produk_bp
from routes.kategori_routes import kategori_bp
from routes.riwayat_routes import riwayat_bp
from routes.transaksi_routes import transaksi_bp


app = Flask(__name__)
app.secret_key = "bjhome-secret-2025" 
app.register_blueprint(home_bp)
app.register_blueprint(rekomendasi_bp)
app.register_blueprint(produk_bp)
app.register_blueprint(kategori_bp)
app.register_blueprint(riwayat_bp)
app.register_blueprint(transaksi_bp)

if __name__ == "__main__":
    app.run(debug=True)
