import sqlite3


class Database:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return result

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id) VALUES (?) ", (user_id,))

    def set_active(self, user_id, active):
        with self.connection:
            return self.cursor.execute("UPDATE users SET active = ? WHERE user_id = ? ", (active, user_id,))

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, active FROM users ").fetchall()

    def set_admin(self, user_id, admin):
        with self.connection:
            return self.cursor.execute("UPDATE users SET admin = ? WHERE user_id = ?", (admin, user_id,))

    def get_user_flags(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT admin, active FROM users WHERE user_id = ?", (user_id,)).fetchone()

    def create_table_users(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users
        (
            id      INTEGER
                PRIMARY KEY autoincrement,
            user_id INTEGER NOT NULL UNIQUE,
            active  INTEGER DEFAULT 1,
            admin   INTEGER DEFAULT 0
        );""")
