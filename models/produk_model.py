import pandas as pd
from db import get_connection


def get_all_produk():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM produk", conn)
    conn.close()
    return df


def get_all_produk_with_fungsi():
    conn = get_connection()
    query = """
        SELECT p.*, k.fungsi_produk 
        FROM produk p
        JOIN kategori k ON p.kategori = k.nama_kategori
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def get_produk_by_id(produk_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produk WHERE id=%s", (produk_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data


def insert_produk(data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO produk (nama_produk, kategori, merek, bahan, ukuran, warna)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        data['nama_produk'], data['kategori'], data['merek'],
        data['bahan'], data['ukuran'], data['warna']
    ))
    conn.commit()
    cursor.close()
    conn.close()


def update_produk(produk_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE produk
        SET nama_produk=%s, kategori=%s, merek=%s, bahan=%s, ukuran=%s, warna=%s
        WHERE id=%s
    """
    cursor.execute(sql, (
        data['nama_produk'], data['kategori'], data['merek'],
        data['bahan'], data['ukuran'], data['warna'], produk_id
    ))
    conn.commit()
    cursor.close()
    conn.close()


def delete_produk(produk_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produk WHERE id=%s", (produk_id,))
    conn.commit()
    cursor.close()
    conn.close()
