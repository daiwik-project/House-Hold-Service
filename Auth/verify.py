
import sqlite3
from database import database1


def professionals_block_status(email):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT block FROM professional WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return False  
    return result[0] == 0 

def recheck_email(email):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professional WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return True
    else:
        return False

def professional_approv_check(email):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT verified FROM professional WHERE email =?",(email,))
    result = cursor.fetchone()
    conn.close()
    return result[0] == 1 

def customer_block_status(email):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT block FROM customer WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return True  
    return result[0]== 0 