from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def load_sql_file(path):
    conn = get_connection()
    cur = conn.cursor()
    with open(path, 'r') as f:
        cur.execute(f.read())
    conn.commit()
    cur.close()
    conn.close()
    print(f"{path} loaded.")

def search(pattern):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()
    print("Search results:", rows)
    cur.close()
    conn.close()

def paginate(limit, offset):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    print(f"Page (limit={limit}, offset={offset}):", rows)
    cur.close()
    conn.close()

def upsert(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    print(f"Upserted: {name} - {phone}")
    cur.close()
    conn.close()

def bulk_insert(names, phones):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL bulk_insert_contacts(%s, %s, %s)", (names, phones, None))
    conn.commit()
    print("Bulk insert done.")
    cur.close()
    conn.close()

def delete(value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()
    print(f"Deleted: {value}")
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_table()
    load_sql_file("functions.sql")
    load_sql_file("procedures.sql")

    upsert("Alice", "+7 701 123 4567")
    upsert("Bob", "+7 702 987 6543")
    upsert("Alice", "+7 701 111 1111")

    search("Alice")
    paginate(2, 0)

    bulk_insert(["Charlie", "Dave"], ["+7 703 000 0000", "abc_bad_phone"])

    delete("Bob")
    search("")