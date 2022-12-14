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


def execute_sql(sql):
    global cursor
    cursor.execute(sql)
    return cursor.fetchall()


def close():
    conn.commit()
    conn.close()


def data_dict_fmt(raw_data, fieldnames):
    data = {key: [] for key in fieldnames}
    data["raw_data"] = raw_data
    for row in raw_data:
        for index, attr in enumerate(row):
            data[fieldnames[index]].append(attr[0])
    return data


def get_field_names(table):
    field_names = []
    for field_data in table[fields]:
        if len(field_data) > 1:
            field_names.append(field_data[0])
    return field_names


def create_table(table):
    global cursor
    schema_text = ""
    for column_def in table[fields]:
        if isinstance(column_def, str):
            schema_text = schema_text + column_def + ", "
        elif len(column_def) > 1:
            schema_text = schema_text + " ".join(column_def) + ", "
        else:
            pass

    create_cmd = f"CREATE TABLE IF NOT EXISTS {table[name]}({schema_text[:-2]})"
    cursor.execute(create_cmd)

def create_cust_table():
    create_table(customers)

def select_statement(table_name, cols="*", condition="*"):
    global cursor
    if condition == "*":
        sel_cmd = f"SELECT {cols} FROM {table_name}"
    else:
        sel_cmd = f"SELECT {cols} FROM {table_name} WHERE {condition}"
    cursor.execute(sel_cmd)
    data = cursor.fetchall()
    return data


def insert_from_dict(table, data_dict):
    global cursor
    attributes = str(tuple(data_dict.keys()))
    values = str(tuple(data_dict.values()))
    ins_cmd = "INSERT INTO {0}{1} VALUES {2}".format(table[name], attributes, values)
    print(ins_cmd)
    cursor.execute(ins_cmd)



meds = {
    name: "meds",
    fields: [
        ("id", INT, PRIMARY_KEY, "AUTOINCREMENT"),
        ("name", VARCHAR),
        ("manufacturer", VARCHAR),
        ("stock_quantity", INT),
        ("mrp", FLOAT),
        ("gst_percent", INT),
    ],
}

customers = {
    name: "custs",
    fields: [
        ("cust_id", INT, PRIMARY_KEY, "AUTOINCREMENT"),
        ("name", VARCHAR),
        ("age", INT),
        ("sex", VARCHAR),
        ("address", VARCHAR),
        ("phone_no", INT),
    ],
}

orders = {
    name: "cust_orders",
    fields: [
        (
            "order_id",
            INT,
            "NOT NULL",
            "UNIQUE",
        ),
        ("cust_id", INT),
        ("med_id", INT),
        ("qty", INT),
        ("txn_date", VARCHAR),
        ("PRIMARY KEY (order_id, cust_id, med_id)"),
        (
            FOREIGN_KEY("med_id", meds[name], "id"),
            "ON DELETE CASCADE ON UPDATE NO ACTION",
        ),
        (
            FOREIGN_KEY("cust_id", customers[name], "cust_id"),
            "ON DELETE CASCADE ON UPDATE NO ACTION",
        ),
    ],
}

emp = {
    name: "employees",
    fields: [
        ("emp_id", VARCHAR, PRIMARY_KEY),
        ('dept', VARCHAR),
        ("password", VARCHAR),
    ],
}





def register_new_customer(data):
    insert_from_dict(customers[name], data)


def add_new_medicines(data):
    insert_from_dict(meds[name], data)


def get_med_quantity(med_id):
    med_qty = select_statement(meds[name], "stock_quantity", f"id = {med_id}")
    med_qty = int(med_qty)
    return med_qty


def search_by_field(table, search_attr, value):
    data_list = list(
        execute_sql(f"SELECT * FROM {table[name]} WHERE {search_attr} LIKE '{value}%'")
    )
    print(data_list)
    return data_list





def search_med_by_name():
    med_list = execute_sql(f"SELECT item_name FROM items")
    return med_list

def check_med_availability(med_name,qty):
    global cursor
    select_cmd = f"SELECT stock_qty FROM items WHERE item_name='{med_name}';"
    cursor.execute(select_cmd)
    row = cursor.fetchone()
    if row[0] >= qty:
        return True
    else:
        return False

def search_cust_by_name(cust_name):
    global cursor
    cust_list = execute_sql(f"SELECT * FROM {customers[name]} WHERE name LIKE {cust_name}%")
    return cust_list

def search_cust_by_phone_no(phone_no):
    global cursor
    select_cmd = f"SELECT * FROM {customers[name]} WHERE phone_no={phone_no}"
    cursor.execute(select_cmd)
    row = cursor.fetchone()
    return row

def filter_custs(name_cond, age_cond, sex_cond):
    rel_ops = "<>="
    if name_cond == "" or not name_cond[0] in rel_ops:
        name_cond_str = ""
        n = False
    else:
        name_cond_str = "Name {}".format(name_cond)
    if age_cond == "" or not age_cond[0] in rel_ops:
        age_cond_str = ""
        a = False
    else:
        age_cond_str = "Age {}".format(age_cond)

    if sex_cond == "" or not sex_cond[0] in rel_ops:
        sex_cond_str = ""
        s = False
    else:
        sex_cond_str = "Sex {}".format(sex_cond)

    if not (n and a and s):
        cmd = "SELECT * FROM custs"
    else:
        cmd = (
            f"SELECT * FROM custs WHERE {name_cond_str} {age_cond_str} {sex_cond_str};"
        )


def create_new_order(cust_id, medicine_data, txn_date):
    if execute_sql(f"SELECT * FROM {orders[name]}") == []:
        order_id = 0000
    else:
        order_id = f"(SELECT MAX(order_id)+1 FROM {orders[name]})"
    for data_item in medicine_data:
        med_id, qty = data_item
        execute_sql(
            f"INSERT INTO {orders[name]} VALUES ({order_id}, {cust_id}, {med_id}, {qty}, {txn_date})"
        )


def show_past_orders(cust_id):
    order_list = execute_sql(
        f"SELECT DISTINCT order_id FROM {orders[name]} WHERE cust_id={cust_id}"
    )
    return order_list


def show_order_details(order_id):
    medicine_details = execute_sql(
        f"SELECT {meds[name]}.name, {orders[name]}.qty FROM {meds[name]},{orders[name]} WHERE {meds[name]}.id={orders[name]}.med_id AND {orders[name]}.order_id={order_id}"
    )
    return list(medicine_details)

def login_emp(emp_id, password):
    stored_password = execute_sql(f'SELECT password FROM {emp[name]} WHERE emp_id={emp_id}')
    if password == str(stored_password):
        return True
    else:
        return False
def get_med_quantity(med_name):
    med_qty = execute_sql(f'SELECT stock_quantity FROM {meds[name]} WHERE name = {med_name}')
    med_qty = int(med_qty)
    return med_qty

def get_amount(med_list):
    global cursor
    med_list.sort(key=lambda x: x[0])
    
    med_name = ""
    for med in med_list:
        med_name = med_name + "'"+med[0] + "',"
    med_name = med_name[:-1]
    select_cmd = f"SELECT amount FROM items WHERE item_name in ({med_name});"
    cursor.execute(select_cmd)
    amt = [c[0] for c in cursor.fetchall()]
    
    total_amt = 0
    for a,m in zip(amt,med_list):
        total_amt = total_amt +a*m[1]
    return total_amt,amt

def purchase_med(med_list):
    global cursor
    med_list.sort(key=lambda x: x[0])
    med_name = ""
    for med in med_list:
        med_name = med_name + "'"+med[0] + "',"
    med_name = med_name[:-1]
    select_cmd = f"SELECT stock_qty FROM items WHERE item_name in ({med_name});"
    cursor.execute(select_cmd)
    total_qty = [c[0] for c in cursor.fetchall()]
    rem_qty = []
    for t_qty,med in zip(total_qty,med_list):
        rem_qty.append(t_qty-med[1])
    for qty,med in zip(rem_qty,med_list):
        update_cmd = f"UPDATE items SET stock_qty = {qty} WHERE item_name = '{med[0]}';"
        cursor.execute(update_cmd)
    conn.commit()

def get_reciept(name,age,sex,date,med_list):
    receipt = """
    ABC PHARMACY

    NAME:{0} AGE:{1} SEX:{2}                   DATE:{3}
    


    MEDICINE\tQTY\tMRP\tGST\tAMOUNT\n""".format(name,age,sex,date)
    total_amt,amt = get_amount(med_list)
    f = open(f"{name}_{date}.txt",'w')
    f.write(receipt)
    for a,med in zip(amt,med_list):
        f.write(f"\t{med[0]}\t{med[1]}\t{a*med[1]}\t18%\t{round(a*1.18,2)}\n")
    f.write(f"\tNET AMOUNT: {round(total_amt*1.18,2)}")
    f.close()

execute_sql("PRAGMA foreign_keys=on")
#create_table(customers)
#create_table(meds)
#create_table(orders)
#create_table(emp)

if __name__ == "__main__":
    conn.close()
