
import os, sqlite3, tempfile
from pathlib import Path

def test_db_and_insert():
    from sqlite3 import connect
    tmp = tempfile.TemporaryDirectory()
    db = os.path.join(tmp.name, 'test.db')
    conn = connect(db)
    cur = conn.cursor()
    cur.execute('CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, quantity INTEGER, created_at TEXT, updated_at TEXT)')
    conn.commit()
    cur.execute("INSERT INTO products (name, price, quantity, created_at, updated_at) VALUES (?, ?, ?, ?, ?)", ('Test', 10.0, 5, 'now','now'))
    conn.commit()
    cur.execute("SELECT COUNT(1) FROM products")
    assert cur.fetchone()[0] == 1
    conn.close()
