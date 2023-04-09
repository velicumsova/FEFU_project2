import datetime
import sqlite3

import data.config

# пример базы данных (его не объзательно использовать)
class DatabasePrototype:
    def __init__(self, path_to_db=data.config.path_to_database):
        self.path_to_db = path_to_db
        self.create_table_of_user()

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()

        connection = self.connection
        # connection.set_trace_callback(logger)
        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        data = None

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()

        return data

    def create_table_of_user(self):
        sql = """
        CREATE TABLE IF NOT EXISTS All_Users (
        telegram_id int NOT NULL,
        telegram_username varchar,
        registration_date varchar,
        user_status varchar,

        PRIMARY KEY (telegram_id)
        );
        """
        self.execute(sql, commit=True)

    def add_user(self, telegram_id, telegram_username):
        print(telegram_id)
        print(telegram_username)
        registration_date = datetime.datetime.now().strftime('%H:%M:%S %d.%m.%y')
        user_status = 'OK'
        is_new_user = 1

        result = self.select_one_user(telegram_id=telegram_id)
        if result is not None:
            print(f'Пользователь {telegram_id} - уже существует! Его нельзя зарегистрировать!')
            return f'Пользователь {telegram_id} - уже существует! Его нельзя зарегистрировать!'

        sql = "INSERT INTO All_Users(telegram_id, telegram_username, registration_date, user_status)" \
              " VALUES(?, ?, ?, ?)"
        parameters = (telegram_id, telegram_username, registration_date, user_status)
        self.execute(sql, parameters=parameters, commit=True)
        print(f'Пользователь {telegram_id} - успешно добавлен!')
        return f'Пользователь {telegram_id} - успешно добавлен!'

    def select_all_users(self):
        sql = 'SELECT * FROM All_Users'
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        # используется для создания sql команды с нужными параметрами для команды ниже
        sql += ' AND '.join([
            f"{item} = ?" for item in parameters.keys()
        ])
        return sql, tuple(parameters.values())

    def select_one_user(self, **kwargs):
        sql = 'SELECT * FROM All_Users WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)
        # пример использования команды select_user(id=131, name='JoJo')

    def select_many_users(self, **kwargs):
        sql = 'SELECT * FROM All_Users WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)
        # пример использования команды select_user(id=131, name='JoJo')

    def update_any_info_about_line(self, user_id, thing_to_change, new_data):
        result = self.select_one_user(telegram_id=user_id)
        if not result:
            print('Пользователя не существует, проверьте правильность id')
            return 'Пользователя не существует, проверьте правильность id'

        sql = f"UPDATE All_Users SET {thing_to_change}=? WHERE telegram_id=?"
        self.execute(sql, parameters=(new_data, user_id), commit=True)


if __name__ == '__main__':
    pass


