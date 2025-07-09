import sqlite3
import bcrypt
from datetime import datetime
from getpass import getpass
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        data_register TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

init_db()

def register_users(username: str, password: str) -> bool:
    try:
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users(username, password_hash) VALUES (?, ?)",
                (username,password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("Пользователь уже существует!")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

#def login_users(username: str, password: str) -> bool:
#   conn = sqlite3.connect('users.db')
#    cursor = conn.cursor()
 #   try:
   #     username = input("Введите почту:")
   #     password = getpass("Введите пароль:")

    #2    cursor.execute("SELECT")