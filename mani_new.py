from login_backend import create_login_table
import sqlite3 as sql

conn = sql.connect("test.db")
cursor = conn.cursor()

create_login_table()

def insert_items(username, password,_type):
    global cursor
    
    insert_cmd = f'''INSERT INTO login_table  
                VALUES('{username}','{password}','{_type}' );'''
    #print(insert_cmd)
    cursor.execute(insert_cmd)
    conn.commit()

insert_items("admin1",'123','Admin')
insert_items("sales1",'234','Sales')