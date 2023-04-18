import datetime
import sqlite3
import json
import data.config

# пример базы данных (его не объзательно использовать)
class Database:
    def __init__(self, path_to_db = data.config.path_to_database):
        self.path_to_db = path_to_db
        self.create_table_of_user()

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def create_table_of_user(self):
        sql = """
        create table `users` (
          `user_id` AUTOINCREMENT not null,
          `first_name` VARCHAR(255) not null,
          `last_name` VARCHAR(255) not null,
          `login` VARCHAR(255) not null,
          `password` VARCHAR(255) not null,
          `login_status` VARCHAR(255) not null,

          primary key (`user_id`)
    )"""
        self.execute(sql, commit=True)

    def user_login(self, login, password):
        sql = "SELECT * FROM users WHERE login = ? and password = ?"
        result = self.execute(sql, (login, password), fetchone=True)

        if result is not None:
            sql_update = "UPDATE users SET login_status='active' WHERE user_id=?"
            self.execute(sql_update, (result.user_id,), commit=True)
            print(f"Вы успешно вошли в аккаунт")
        else:
            print(f"Пользователя с такими данными не существует")

    def user_register(self, login, password, first_name, last_name):
        sql = "SELECT * FROM users WHERE login=?"
        result = self.execute(sql, (login,), fetchone=True)

        if result is not None:
            print("Пользователь с таким именем уже зарегистрирован")
        else:
            sql_insert = "INSERT INTO users (login, password, first_name, last_name, login_status) VALUES (?, ?, ?, ?, ?)"
            self.execute(sql_insert, (login, password, first_name, last_name, 'active'), commit=True)
            print("Вы успешно зарегистрировались")

    def login_status(self, login):
        sql = "SELECT login_status FROM users WHERE login=?"
        result = self.execute(sql, (login,), fetchone=True)
        if result is not None:
            status = result[0]
            return status
        else:
            return None

    def get_rooms_list(self):


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
        create table `users` (
          `user_id` AUTOINCREMENT not null,
          `first_name` VARCHAR(255) not null,
          `last_name` VARCHAR(255) not null,
          `login` VARCHAR(255) not null,
          `password` VARCHAR(255) not null,
          `login_status` VARCHAR(255) not null,
          
          primary key (`user_id`)
    )"""
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
        # пример использования команды select_user(id=131, name='x')

    def update_any_info_about_line(self, user_id, thing_to_change, new_data):
        result = self.select_one_user(telegram_id=user_id)
        if not result:
            print('Пользователя не существует, проверьте правильность id')
            return 'Пользователя не существует, проверьте правильность id'

        sql = f"UPDATE All_Users SET {thing_to_change}=? WHERE telegram_id=?"
        self.execute(sql, parameters=(new_data, user_id), commit=True)


if __name__ == '__main__':
    pass