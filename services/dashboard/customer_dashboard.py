import sqlite3
from database import database1

def customer_dashboard_functions(customer_id):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT full_name FROM customer WHERE id = ?", (customer_id,))
    result = cursor.fetchone() 
    conn.close()
    if result:
        return result[0]
    return None

def get_service_info():
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name_or_type FROM service")
    result = cursor.fetchall()
    conn.close()
    return result
    
def get_sub_service(name_or_type):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name_or_type, sub_type, description, base_price FROM service WHERE name_or_type = ?", (name_or_type,))
    result = cursor.fetchall()
    conn.close()
    return result

def close_my_service(id, status):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE service_inti_or_close
    SET customer_status = ?
    WHERE service_init_id = ?
    ''', (status, id))
    conn.commit()
    conn.close()
    return True

def service_close(id):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT service_init_id,  service_main, service_sub_type, customer_status, price FROM  service_inti_or_close WHERE customer_status = 'close' AND customer_id = ?", (id,))
    result = cursor.fetchall()
    conn.close()
    return result

def customer_info(id):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT full_name, email, mb_no, address, city, pincode FROM customer WHERE id = ?",(id,))
    result = cursor.fetchall()
    conn.close()
    return result