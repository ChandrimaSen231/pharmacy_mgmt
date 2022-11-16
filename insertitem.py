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



def insert_items(item_name,stock_qty,amt,total_amt,desc):
    global cursor
    
    insert_cmd = f'''INSERT INTO items (item_name,stock_qty,amount,total_amount,desc) 
                VALUES('{item_name}',{stock_qty},{amt},{total_amt} ,'{desc}' );'''
    #print(insert_cmd)
    cursor.execute(insert_cmd)
    conn.commit()

insert_items('Med 1',10,200,2000,'Medicine 1')
insert_items('Med 2',12,140,1680,'Medicine 2')
insert_items('Med 3',15,210,3150,'Medicine 3')
insert_items('Med 4',20,100,2000,'Medicine 4')
insert_items('Med 5',10,300,3000,'Medicine 5')