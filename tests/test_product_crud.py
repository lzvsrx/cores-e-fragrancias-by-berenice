
import os, tempfile, sqlite3
from pathlib import Path

def test_product_crud():
    tmp = tempfile.TemporaryDirectory()
    db = os.path.join(tmp.name, 'test.db')
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, quantity INTEGER, image_path TEXT, description TEXT, updated_at TEXT, created_at TEXT)')
    conn.commit()
    cur.execute('INSERT INTO products (name, price, quantity, created_at, updated_at) VALUES (?, ?, ?, ?, ?)', ('Prod A', 10.0, 5, 'now', 'now'))
    conn.commit()
    cur.execute('SELECT * FROM products WHERE name=?', ('Prod A',))
    row = cur.fetchone()
    assert row is not None
    assert row[1] == 'Prod A'
    conn.close()
