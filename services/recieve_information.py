import sqlite3
from database import database1

def retrive_service_info(id):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name_or_type, sub_type, base_price FROM service WHERE id = ?", (id,))
    result = cursor.fetchall()
    conn.close()
    return result

def retrive_customer_info(id):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, mb_no, address, city, pincode FROM customer WHERE id = ?", (id,)) 
    result = cursor.fetchall()
    conn.close()
    return result


def main_service_name():
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name_or_type FROM service")
    result = cursor.fetchall()
    conn.close()
    return result

def sub_service_name(name_or_type):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT name_or_type, sub_type FROM service WHERE name_or_type = ?", (name_or_type,))
    result = cursor.fetchall()
    conn.close()
    return result
