import csv
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

def insert_from_csv(filepath):
    conn = get_connection()
    cur = conn.cursor()
    with open(filepath, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook(name, phone) VALUES (%s, %s)",
                (row['name'], row['phone'])
            )
    conn.commit()
    cur.close()
    conn.close()

def insert_from_console():
    name = input("Name: ")
    phone = input("Phone: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phonebook(name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def search_by_name(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM phonebook WHERE name ILIKE %s",
        (f"%{name}%",)
    )
    rows = cur.fetchall()
    print(rows)
    cur.close()
    conn.close()

def search_by_phone(phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM phonebook WHERE phone ILIKE %s",
        (f"%{phone}%",)
    )
    rows = cur.fetchall()
    print(rows)
    cur.close()
    conn.close()

def update_phone(name, new_phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE name = %s",
        (new_phone, name)
    )
    conn.commit()
    cur.close()
    conn.close()

def update_name(phone, new_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE phonebook SET name = %s WHERE phone = %s",
        (new_name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_contact(value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM phonebook WHERE name = %s OR phone = %s",
        (value, value)
    )
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    create_table()
    insert_from_csv("contacts.csv")
    insert_from_console()

    get_all()
    search_by_name("Ali")
    search_by_phone("7700")

    update_phone("Alice", "+77000000000")
    update_name("+77029876543", "Bobby")

    delete_contact("Charlie")

    get_all()