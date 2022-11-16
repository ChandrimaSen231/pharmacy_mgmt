import sqlite3 as sql

conn = sql.connect("test.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS inventory_order;")
cursor.execute("DROP TABLE IF EXISTS items;")
conn.commit()