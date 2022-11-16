from pharmacy_backend import create_cust_table
import sqlite3 as sql

conn = sql.connect("test.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS custs")
create_cust_table()

def insert_items(name,age,sex,address,phone):
    global cursor
    
    insert_cmd = f'''INSERT INTO custs (name,age,sex,address,phone_no) 
                VALUES('{name}','{age}','{sex}','{address}',{phone} );'''
    #print(insert_cmd)
    cursor.execute(insert_cmd)
    conn.commit()

insert_items('Cust1',28,'M','123 Street',42571)
insert_items('Cust2',45,'F','Building 23 Town Center',11111)
insert_items('Cust3',32,'F','Plot 16 East Side',32146)
insert_items('Cust4',60,'M','Richards Villa Main City',24617 )