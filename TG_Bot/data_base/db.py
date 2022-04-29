import sqlite3

# класс по управлению БД
class Database_users:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    # поверка пользователя в БД
    def user_exists(self, user_id, table='users'):
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM "{table}" WHERE "user_id" = ?', (user_id,)).fetchmany(1)
            return bool(len(result))

    # Добавить пользователя в БД
    def add_user(self, user_id, table='users'):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO '{table}' ('user_id') VALUES (?) ", (user_id,))

    # Изменить статус пользователя в БД
    def set_active(self, user_id, active=1, table='users'):
        with self.connection:
            return self.cursor.execute(f"""UPDATE '{table}' SET 'active' =  ? WHERE 'user_id' = ?""",(active, user_id,))

    # Получить статус пользователя в БД
    def get_users(self, table='users'):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM '{table}' ").fetchall()
