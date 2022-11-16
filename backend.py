import sqlite3 as sql
import datetime
import random as rn

conn = sql.connect("test.db")
cursor = conn.cursor()

# Constants:
name = "name"
fields = "fields"

VARCHAR = "VARCHAR(50)"
INT = "INTEGER"
FLOAT = "FLOAT"
DATE = "DATE"

PRIMARY_KEY = "PRIMARY KEY"
FOREIGN_KEY = lambda key_field, foreign_table, foreign_key: "FOREIGN KEY ({0}) REFERENCES {1}({2})".format(
    key_field, foreign_table, foreign_key
)

create_invt_order_table = '''CREATE TABLE IF NOT EXISTS inventory_order (
                        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        order_name VARCHAR(50),
                        order_date DATE,
                        item_id INTEGER,
                        quantity INTEGER,
                        order_amount INTEGER,
                        status VARCHAR(50),
                        FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
                        );
                    '''
# add column order amount
create_item_table = '''CREATE TABLE IF NOT EXISTS items (
                    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name VARCHAR(50),
                    stock_qty INTEGER,
                    amount INTEGER,
                    total_amount INTEGER,
                    desc VARCHAR(50)
                    );
                '''
# add column amount and total amount

orders = {
    name: "inventory_order",
    fields: [
        ("order_id", INT, PRIMARY_KEY,'AUTOINCREMENT'),
        ("order_name", VARCHAR),
        ('order_date', DATE),
        ('item_id', INT),
        ("quantity", INT),
        
        ("status", VARCHAR),
        ("FOREIGN_KEY","'('item_id') REFERENCES ('item_id')'"," ON DELETE CASCADE")
    ],
}

items = {
    name: "items",
    fields: [
        ("item_id", INT, PRIMARY_KEY),
        ("item_name", VARCHAR),
        ("stock_qty", INT),
        ("desc", VARCHAR),
    ],
}

def create_table(create_cmd):
    global cursor 
    print(create_cmd)
    cursor.execute(create_cmd)

def create_table_orders():
    create_table(create_invt_order_table)

def create_table_items():
    create_table(create_item_table)

def get_table(table):
    global cursor
    fetch_cmd = f"SELECT * FROM {table};"
    cursor.execute(fetch_cmd)
    rows = cursor.fetchall()
    return rows

def place_order(item_id, item_name,qty):
    global cursor
    select_cmd = f"SELECT amount FROM items WHERE item_id={item_id};"
    cursor.execute(select_cmd)
    val = cursor.fetchone()[0]
    amt = val * qty
    insert_cmd = f'''INSERT INTO inventory_order (order_name,order_date,item_id,quantity,order_amount,status) 
                    VALUES('{item_name}', '{datetime.date.today()}', 
                    {item_id},{qty},{amt} ,'Pending' );'''
    #print(insert_cmd)
    cursor.execute(insert_cmd)
    conn.commit()

def change_order_status(order_id,item_id):
    global cursor
    update_cmd = f"UPDATE inventory_order SET status='Received' WHERE order_id={order_id};"
    select_cmd = f"SELECT stock_qty,amount FROM items WHERE item_id={item_id};"
    # write select cmd for fetching qty of order placed from invt orders
    # and add it with stock_qty and update it in items table
    select2_cmd = f"SELECT quantity FROM inventory_order WHERE order_id={order_id};"
    #print(select_cmd)
    cursor.execute(select_cmd)
    tup = cursor.fetchone()
    val1 = tup[0]
    print(val1)
    amt = tup[1]
    print(amt)
    cursor.execute(select2_cmd)
    val2 = cursor.fetchone()[0]
    updated_qty = val1 + val2
    updated_amt = updated_qty * amt
    update2_cmd = f"UPDATE items SET stock_qty={updated_qty} , total_amount= {updated_amt} WHERE item_id={item_id};"
    #print(update_cmd)
    cursor.execute(update_cmd)
    cursor.execute(update2_cmd)
    conn.commit()

def addItemtoDB(item_id,item_name,qty,amt,item_desc):
    global cursor
    total_amt = amt*qty
    insert_cmd = f"INSERT INTO items VALUES({item_id},'{item_name}',{qty},{amt},{total_amt} ,'{item_desc}' );"
    cursor.execute(insert_cmd)
    conn.commit()

def deleteItemfromDB(item_id):
    global cursor
    cursor.execute("PRAGMA foreign_keys=ON")
    delete_cmd = f"DELETE FROM items WHERE item_id={item_id};"
    cursor.execute(delete_cmd)
    conn.commit()

def search_item(item_name):
    global cursor
    search_cmd = f"SELECT * FROM items WHERE item_name LIKE '{item_name}%'"
    cursor.execute(search_cmd)
    rows = cursor.fetchall()
    return rows


if __name__ == '__main__':
    pass