import sqlite3
import bcrypt
from datetime import datetime
from getpass import getpass
from contextlib import closing
def init_db():
    conn = sqlite3.connect('db_manager_password.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        data_register TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services(
            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name_service TEXT NOT NULL,
            login_service TEXT NOT NULL,
            password_service TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
    conn.commit()
    conn.close()

init_db()

def register_users(email: str, username: str, password: str) -> bool:
    try:
        with closing(sqlite3.connect('db_manager_password.db')) as conn:
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            cursor = conn.cursor()

            cursor.execute("INSERT INTO users(email, username, password_hash) VALUES (?, ?, ?)",
                    (email, username, password_hash.decode('utf-8')))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        print("Пользователь уже существует!")
        return False

def get_user_id(username: str) -> int:
    with closing(sqlite3.connect('db_manager_password.db')) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        return cursor.fetchone()[0]
def services_users(user_id: int, name_service: str, login_service: str, password_service: str) -> bool:
    try:

        with closing(sqlite3.connect('db_manager_password.db')) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
            if not cursor.fetchone():
                print(f"Ошибка: Пользователь с ID {user_id} не найден")
                return False
            password_hash = bcrypt.hashpw(password_service.encode("utf-8"), bcrypt.gensalt())
            cursor.execute("INSERT INTO services(user_id, name_service, login_service, password_service) VALUES (?, ?, ?, ?)",
                (user_id, name_service,login_service,password_hash.decode("utf-8")))
            conn.commit()
            return True
    except sqlite3.IntegrityError as e:
        print(f"Ошибка уникальности: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
        return False
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return False


