import sqlite3
from database import database1

def customer_login(email, password):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM customer WHERE email = ?", (email,))

    result = cursor.fetchone()
    conn.close()
    if result and result[1] == password:
        return True, result[0]
    return False, None

def admin_login_function(email, password):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM admin WHERE email = ?",(email,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] == password:
        return True, email
    return False, email

def professional_login(email, password):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM professional WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    if result and result[1] == password:
        return True, result[0]
    return False, None
        