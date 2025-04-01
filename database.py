import sqlite3

database1 = "./database/household_services.db"

def setup_database():
    try:
            conn = sqlite3.connect(database1)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admin (
                    email TEXT PRIMARY KEY NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customer (
                    id TEXT PRIMARY KEY NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    mb_no TEXT NOT NULL,
                    address TEXT NOT NULL,
                    city TEXT NOT NULL,
                    pincode TEXT NOT NULL,
                    block INTEGER NOT NULL DEFAULT 0
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS professional (
                    id TEXT PRIMARY KEY NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    mb_no TEXT NOT NULL,
                    password TEXT NOT NULL,
                    address TEXT NOT NULL,
                    city TEXT NOT NULL,
                    pincode TEXT NOT NULL,
                    id_proof BLOB NOT NULL,
                    main_service_type TEXT NOT NULL,
                    speciality TEXT NOT NULL,
                    experience INTEGER NOT NULL,
                    rating INTEGER,
                    block INTEGER NOT NULL DEFAULT 0,
                    verified INTERGER NOT NULL DEFAULT 0
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS service (
                    id TEXT PRIMARY KEY NOT NULL,
                    name_or_type TEXT NOT NULL,
                    sub_type TXT NOT NULL,
                    description TEXT,
                    base_price INTEGER NOT NULL
                )
            """)  

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS service_inti_or_close (
                    service_init_id TEXT PRIMARY KEY NOT NULL,
                    customer_id TEXT NOT NULL,
                    customer_name TEXT NOT NULL,
                    customer_mobile TEXT NOT NULL ,
                    customer_address TEXT  NOT NULL,
                    customer_city TEXT NOT NULL,
                    customer_pincode TEXT NOT NULL,
                    service_id TEXT NOT NULL,
                    service_main TEXT NOT NULL,
                    service_sub_type TEXT NOT NULL,
                    customer_status TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    accepted_prof_id TEXT DEFAULT NULL,
                    accepted_prof_name TEXT DEFAULT NULL,
                    accepted_prof_number TEXT DEFAULT NULL,
                    reject_prof_id TEXT,
                    professional_status TEXT,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
                )
            """)
            conn.commit()

    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        conn.close()

def intidb():
    return setup_database()
