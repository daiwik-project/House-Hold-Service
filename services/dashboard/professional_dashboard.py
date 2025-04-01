import sqlite3
from database import database1

def professional_dashboard_functions(id):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT full_name FROM professional WHERE id = ?", (id,))

    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def find_service_for_me(name, id):  
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()

    
    cursor.execute("""
    SELECT service_init_id, 
    customer_name, 
    customer_mobile, 
    customer_address, 
    customer_city, 
    customer_pincode, 
    price,
    reject_prof_id
    FROM service_inti_or_close 
    WHERE customer_status = 'init' 
    AND accepted_prof_id IS NULL 
    AND service_sub_type = ?
    """, (name,)) 

    result = cursor.fetchall()  
    conn.close()

    filtered_results = [] 
    for i in result:
        if i[7] is None:
            filtered_results.append(i)  
            continue 

        ids = i[7].split(',')
        if id in ids:
            continue  
        filtered_results.append(i)  
    # print(f'{filtered_results} result hai bhai')
    return filtered_results 





def my_service_type(id):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT speciality FROM professional WHERE id = ?", (id,))
    result = cursor.fetchone() 
    print(f'{result} yeh my_service_type')
    conn.close()
    return result

def prof_number(id):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT mb_no FROM professional WHERE id = ?", (id,))
    result = cursor.fetchone()
    conn.close()
    return result

def accept(sid, p_name, p_id, p_status, p_no):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE service_inti_or_close
    SET accepted_prof_id = ?,
    accepted_prof_name = ?,
    accepted_prof_number = ?,
    professional_status = ?
    WHERE service_init_id = ?
    ''', (p_id, p_name, p_no, p_status, sid))

    conn.commit()
    conn.close()
    return True

def my_services(id):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("SELECT service_init_id, customer_name, customer_mobile, customer_address, customer_city, price, customer_status FROM service_inti_or_close WHERE accepted_prof_id = ?", (id,))
    result = cursor.fetchall()
    conn.close()
    return result

def prof_profile(tid):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    cursor.execute("""SELECT full_name,
     email,
     mb_no,
     address, 
     city, 
     pincode, 
     experience FROM professional WHERE id = ?""", (tid,))
    result = cursor.fetchall()  
    conn.close()  
    if result is None:
        print(f"No professional found with id: {tid}")
        return None 
    return result


def rejected_service(sid, id):
    conn = sqlite3.connect(database1)  
    cursor = conn.cursor()
    cursor.execute("SELECT reject_prof_id FROM service_inti_or_close WHERE service_init_id = ?", (sid,))
    current_list = cursor.fetchone()
    if current_list and current_list[0]:
        new_info = current_list[0] + ',' + id
    else:
        new_info = id
    cursor.execute("UPDATE service_inti_or_close SET reject_prof_id = ? WHERE service_init_id = ?", (new_info, sid))
    conn.commit()
    conn.close()
