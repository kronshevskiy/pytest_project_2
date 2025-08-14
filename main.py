import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="test_user",
        database="test_db",
    )

def create_table(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                birthday DATE,
                gender VARCHAR(10),
                preference TEXT
            )
        """)
        conn.commit()
    finally:
        cursor.close()

def add_user(conn, name, birthday, gender, preference):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT 1 FROM users WHERE name = %s AND birthday = %s LIMIT 1",
            (name, birthday)
        )
        exists = cursor.fetchone()
        if exists:
            print("User with this name and birthday already exists. Skipping insert.")
            return

        cursor.execute(
            "INSERT INTO users (name, birthday, gender, preference) VALUES (%s, %s, %s, %s)",
            (name, birthday, gender, preference)
        )
        conn.commit()
        print(f"User '{name}' added.")
    finally:
        cursor.close()

def delete_user(conn, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        print(f"User with ID {user_id} deleted.")
    finally:
        cursor.close()

def view_users(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
    finally:
        cursor.close()

    print(f"{'ID':<3} {'Name':<25} {'Birthday':<12} {'Gender':<8} {'Preference'}")
    print("-" * 60)
    for user_id, name, birthday, gender, preference in rows:
        print(f"{user_id:<3} {name:<25} {birthday} {gender:<8} {preference}")
    print()

def main():
    conn = connect_db()
    create_table(conn)
    try:
        while True:
            print("1: Add user\n2: Delete user\n3: View users\n4: Exit")
            choice = input("Choose: ").strip()
            if choice == '1':
                name = input("Name: ").strip()
                birthday = input("Birthday (YYYY-MM-DD): ").strip()
                gender = input("Gender: ").strip()
                preference = input("Preference: ").strip()
                if name and birthday and gender:
                    add_user(conn, name, birthday, gender, preference)
                else:
                    print("Name, Birthday and Gender are required.")
            elif choice == '2':
                try:
                    user_id = int(input("User ID to delete: ").strip())
                    delete_user(conn, user_id)
                except ValueError:
                    print("Invalid ID.")
            elif choice == '3':
                view_users(conn)
            elif choice == '4':
                break
            else:
                print("Invalid choice")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
