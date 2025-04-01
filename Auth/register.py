import sqlite3
from database import database1

def customer_register(id, full_name, email, password, mb_no, address, city, pincode):
    try:
        conn = sqlite3.connect(database1)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customer (id, full_name, email, password, mb_no, address, city, pincode) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
        (id, full_name, email, password, mb_no, address, city, pincode))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding Customer: {e}")
        return False
    finally:
        conn.close()

def admin_register(email, password):
    try:
        conn = sqlite3.connect(database1)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO admin (email, password) VALUES (?, ?)", 
        (email, password))
        conn.commit()
    except Exception as e:
        print(f"Error adding Admin: {e}")
    finally:
        conn.close()

def professional_register(id, full_name, email, mb_no, password, address, city, pincode, id_proof, main_service_type, speciality, experience):
    try:
        conn = sqlite3.connect(database1)
        cursor = conn.cursor()
        id_proof_data = id_proof.read()
        cursor.execute("INSERT INTO professional (id, full_name, email, mb_no, password, address, city, pincode, id_proof, main_service_type, speciality, experience) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
        (id, full_name, email, mb_no, password, address, city, pincode, id_proof_data, main_service_type, speciality, experience))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding Professional: {e}")
        return False
    finally:
        conn.close()

