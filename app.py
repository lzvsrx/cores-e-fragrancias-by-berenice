
import os, sqlite3, json, io
import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd
import qrcode

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")
UPLOADS = os.path.join(os.path.dirname(__file__), "uploads")

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def ensure_db(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products';")
    if not cur.fetchone():
        # initialize minimal schema for demo if missing
        cur.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, quantity INTEGER, image_path TEXT, description TEXT, updated_at TEXT, created_at TEXT)')
        conn.commit()

def generate_qr_image(data_str):
    qr = qrcode.QRCode(box_size=6, border=1)
    qr.add_data(data_str)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def product_card(r, col):
    with col:
        st.markdown(f"**{r['name']}**")
        if r['image_path'] and os.path.exists(r['image_path']):
            st.image(r['image_path'], use_column_width=True)
        else:
            st.write('Sem imagem')
        st.caption(f"R$ {float(r.get('price',0)):.2f} • Qt: {int(r.get('quantity',0))}")
        if st.button("Ver detalhes", key=f"view_{r['id']}"):
            with st.expander(f"Detalhes — {r['name']}", expanded=True):
                if r['image_path'] and os.path.exists(r['image_path']):
                    st.image(r['image_path'], width=400)
                st.markdown(r.get('description',''))
                st.write(f"Quantidade: {r.get('quantity',0)}")
                qr = generate_qr_image(json.dumps({'id': r['id'], 'name': r['name']}))
                buf = io.BytesIO()
                qr.save(buf, format='PNG')
                st.image(buf)

def main():
    st.set_page_config(page_title="Cores e Fragrâncias — Desktop", layout='wide')
    st.markdown("# Cores e Fragrâncias — Catálogo Refinado")
    conn = get_conn()
    ensure_db(conn)
    df = pd.read_sql_query("SELECT * FROM products ORDER BY updated_at DESC;", conn)
    if df.empty:
        st.info("Nenhum produto cadastrado")
        return
    # responsive grid (3 columns)
    cols = st.columns(3)
    for idx, row in df.iterrows():
        product_card(row, cols[idx % 3])

if __name__ == '__main__':
    main()
