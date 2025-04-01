import sqlite3
from database import database1

def get_all_services_details():
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name_or_type, sub_type, description, base_price FROM service ORDER BY name_or_type")
    result = cursor.fetchall() 
    conn.close()
    if result:
        return result
    return None


def pdf_data_return(aid):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT id_proof FROM professional WHERE id == ?", (aid,))
    result = cursor.fetchall()
    conn.close()
    return result


def list_all_props():
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("""SELECT id, full_name, email, mb_no, address, city, pincode, main_service_type, speciality, experience, block, verified FROM professional """)
    result = cursor.fetchall()
    conn.close()
    if result:
        return result
    return None


def add_service(id, name_or_type, sub_type, description, base_price):
    try:
        conn = sqlite3.connect(database1)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO service (id, name_or_type, sub_type, description, base_price) VALUES (?, ?, ?, ?, ?)", 
                       (id, name_or_type, sub_type, description, base_price))
        conn.commit()
        print("Service added successfully")
    except Exception as e:
        print(f"Error adding service: {e}")
    finally:
        conn.close()

def professional_approv(email):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("UPDATE professional SET verified = 1 WHERE email = ?", (email,))
    conn.commit()
    conn.close()
    return True


def list_all_service_status():
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute(" SELECT * FROM service_inti_or_close")
    result = cursor.fetchall()
    conn.close()
    # print(result)
    return result