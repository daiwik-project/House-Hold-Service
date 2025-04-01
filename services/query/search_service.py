import sqlite3
from database import database1

def customer_search(customer_id, search_param, customer_query):
    if search_param == 'date':
        conn = sqlite3.connect(database1)
        cursor = conn.cursor()
        cursor.execute("""SELECT service_init_id, customer_pincode, service_main, service_sub_type, customer_status, price, accepted_prof_name, accepted_prof_number, date FROM service_inti_or_close WHERE customer_id = ? AND DATE(date) = ? GROUP BY service_sub_type""", (customer_id, customer_query,))
        result = cursor.fetchall()
        conn.close()
        return result


    if search_param == 'professional_number':
        conn = sqlite3.connect(database1)
        cursor = conn.cursor()
        cursor.execute("""SELECT service_init_id, customer_pincode, service_main, service_sub_type, customer_status, price, accepted_prof_name, accepted_prof_number, date FROM service_inti_or_close WHERE customer_id = ? AND accepted_prof_number = ? GROUP BY DATE(date)""", (customer_id, customer_query,))
        result = cursor.fetchall() 
        conn.close()
        return result
    
    if search_param == 'service_type':
        conn = sqlite3.connect(database1)
        cursor = conn.cursor()
        cursor.execute("""SELECT service_init_id, customer_pincode, service_main, service_sub_type, customer_status, price, accepted_prof_name, accepted_prof_number, date FROM service_inti_or_close WHERE customer_id = ? AND service_sub_type  = ? GROUP BY DATE(date)""", (customer_id, customer_query,))
        result = cursor.fetchall() 
        conn.close()
        return result

    if search_param == 'pincode':
        conn = sqlite3.connect(database1)
        cursor = conn.cursor()
        cursor.execute("""SELECT service_init_id, customer_pincode, service_main, service_sub_type, customer_status, price, accepted_prof_name, accepted_prof_number, date FROM service_inti_or_close WHERE customer_id = ? AND customer_pincode = ? GROUP BY DATE(date)""", (customer_id, customer_query,))
        result = cursor.fetchall() 
        conn.close()
        return result
    
def prof_search(professional_id, search_param, professional_query):
    if search_param == 'date':
        conn = sqlite3.connect(database1)
        cursor = conn.cursor()
        cursor.execute("""SELECT service_init_id, customer_name, customer_mobile, customer_address, customer_city, customer_pincode, customer_status, price, professional_status FROM service_inti_or_close WHERE accepted_prof_id = ? AND DATE(date) = ? GROUP BY DATE(date)""", (professional_id, professional_query,))
        result = cursor.fetchall() 
        conn.close()
        return result
    
    if search_param == 'customer_number':
        conn = sqlite3.connect(database1)
        cursor = conn.cursor()
        cursor.execute("""SELECT service_init_id, customer_name, customer_mobile, customer_address, customer_city, customer_pincode, customer_status, price, professional_status FROM service_inti_or_close WHERE accepted_prof_id = ? AND customer_mobile = ? GROUP BY DATE(date)""", (professional_id, professional_query,))
        result = cursor.fetchall() 
        conn.close()
        return result
    
    
    if search_param == 'customer_address':
        conn = sqlite3.connect(database1)
        cursor = conn.cursor()
        cursor.execute("""SELECT service_init_id, customer_name, customer_mobile, customer_address, customer_city, customer_pincode, customer_status, price, professional_status FROM service_inti_or_close WHERE accepted_prof_id = ? AND customer_address = ? GROUP BY DATE(date)""", (professional_id, professional_query,))
        result = cursor.fetchall() 
        conn.close()
        return result
    
    if search_param == 'pincode':
        conn = sqlite3.connect(database1)
        cursor = conn.cursor()
        cursor.execute("""SELECT service_init_id, customer_name, customer_mobile, customer_address, customer_city, customer_pincode, customer_status, price, professional_status FROM service_inti_or_close WHERE accepted_prof_id = ? AND customer_address = ? GROUP BY DATE(date)""", (professional_id, professional_query,))
        result = cursor.fetchall()
        conn.close()
        return result


def admin_search(admin_param, admin_query):
    conn = sqlite3.connect(database1)
    cursor = conn.cursor()
    sql_query = f"SELECT {admin_query} FROM {admin_param}"
    cursor.execute(sql_query)
    result = cursor.fetchall()
    if admin_query == '*':
        column_names = [description[0] for description in cursor.description]
    else:
        column_names = admin_query.split(', ')
    conn.close()
    return result, column_names

    
