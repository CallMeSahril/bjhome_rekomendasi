import mysql.connector
from config import DB_CONFIG
import pandas as pd

def get_all_kategori():
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT * FROM kategori", conn)
    conn.close()
    return df

def get_kategori_by_id(id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kategori WHERE id = %s", (id,))
    result = cursor.fetchone()
    conn.close()
    return result

def insert_kategori(nama_kategori, fungsi_produk):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO kategori (nama_kategori, fungsi_produk) VALUES (%s, %s)", (nama_kategori, fungsi_produk))
    conn.commit()
    conn.close()

def update_kategori(id, nama_kategori, fungsi_produk):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("UPDATE kategori SET nama_kategori = %s, fungsi_produk = %s WHERE id = %s", (nama_kategori, fungsi_produk, id))
    conn.commit()
    conn.close()

def delete_kategori(id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM kategori WHERE id = %s", (id,))
    conn.commit()
    conn.close()
