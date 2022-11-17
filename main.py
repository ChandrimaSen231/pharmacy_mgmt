from backend import *
from pharmacy_backend import *
from login_backend import *
import sqlite3 as sql

conn = sql.connect("test.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS login_table")
cursor.execute("DROP TABLE IF EXISTS custs")
cursor.execute("DROP TABLE IF EXISTS items")
cursor.execute("DROP TABLE IF EXISTS inventory_order")

create_table_items()
create_table_orders()
create_login_table()
create_cust_table()

def insert_items_custs(name,age,sex,address,phone):
    global cursor
    
    insert_cmd = f'''INSERT INTO custs (name,age,sex,address,phone_no) 
                VALUES('{name}','{age}','{sex}','{address}',{phone} );'''
    #print(insert_cmd)
    cursor.execute(insert_cmd)
    conn.commit()

insert_items_custs('Cust1',28,'M','123 Street',42571)
insert_items_custs('Cust2',45,'F','Building 23 Town Center',11111)
insert_items_custs('Cust3',32,'F','Plot 16 East Side',32146)
insert_items_custs('Cust4',60,'M','Richards Villa Main City',24617 )


def insert_items_item(item_name,stock_qty,amt,total_amt,desc):
    global cursor
    
    insert_cmd = f'''INSERT INTO items (item_name,stock_qty,amount,total_amount,desc) 
                VALUES('{item_name}',{stock_qty},{amt},{total_amt} ,'{desc}' );'''
    #print(insert_cmd)
    cursor.execute(insert_cmd)
    conn.commit()

insert_items_item('Med 1',10,200,2000,'Medicine 1')
insert_items_item('Med 2',12,140,1680,'Medicine 2')
insert_items_item('Med 3',15,210,3150,'Medicine 3')
insert_items_item('Med 4',20,100,2000,'Medicine 4')
insert_items_item('Med 5',10,300,3000,'Medicine 5')

def insert_items_lg(username, password,_type):
    global cursor
    
    insert_cmd = f'''INSERT INTO login_table  
                VALUES('{username}','{password}','{_type}' );'''
    #print(insert_cmd)
    cursor.execute(insert_cmd)
    conn.commit()

insert_items_lg("admin1",'123','Admin')
insert_items_lg("sales1",'234','Sales')
