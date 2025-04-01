import sqlite3
from database import database1

def service_intilization(id, status, service_info, customer_info):
    try:
        service_init_id = id
        customer_status = status
        conn = sqlite3.connect(database1)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO service_inti_or_close (service_init_id, customer_id, customer_name, customer_mobile, customer_address, customer_city, customer_pincode, service_id, service_main, service_sub_type, customer_status, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
        (service_init_id, customer_info[0][0], customer_info[0][1], customer_info[0][2], customer_info[0][3], customer_info[0][4], customer_info[0][5], service_info[0][0], service_info[0][1], service_info[0][2], customer_status, service_info[0][3] ) ) 
        conn.commit()
        return True
    except Exception as e:
        print(f'Processing a booking service ')
    finally:
        conn.close()

def get_service_status(id):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT  service_init_id, service_main, service_sub_type, customer_status, accepted_prof_name, accepted_prof_number, price FROM service_inti_or_close WHERE customer_status = 'init' AND customer_id = ?", (id,)) # retrive customer info customer_id, name, mobile, address, city, pincode, 
    result = cursor.fetchall()
    conn.close()
    return result

