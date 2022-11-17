import sqlite3 as sql
import datetime
import random as rn
import backend

conn = sql.connect("test.db")
cursor = conn.cursor()

create_login = '''CREATE TABLE IF NOT EXISTS login_table (
                        username VARCHAR(50) PRIMARY KEY,
                        password VARCHAR(50),
                        type VARCHAR(50)
                    );'''

def create_login_table():
    backend.create_table(create_login)

def delete_login_table():
    global cursor
    delete_cmd = "DROP TABLE IF EXISTS login_table;"
    cursor.execute(delete_cmd)
    conn.commit()

def verify_data(username,password,_type):
    global cursor
    fetch_cmd = f"SELECT * FROM login_table WHERE username = '{username}' AND password = '{password}' AND type ='{_type}';"
    cursor.execute(fetch_cmd)
    if cursor.fetchone():
        return True
    else:
        return False