import datetime
import sqlite3
import json
import data.config

# пример базы данных (его не объзательно использовать)
class Database:
    def __init__(self, path_to_db = data.config.path_to_database):
        self.path_to_db = path_to_db
        self.create_table_of_rooms()
        self.create_table_of_users()


    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()

        connection = self.connection
        # connection.set_trace_callback(logger)
        cursor = connection.cursor()
        # cursor.execute(sql, parameters)
        data = None

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()

        return data

    def create_table_of_rooms(self):
        sql = """
        create table `rooms` (
          `room_floor` INT8 not null,
          `room_number` INT8 not null,
          `occupied` BOOLEAN null,
          `room_resident` varchar(255) not null,
          `room_id` INTEGER PRIMARY KEY not null
    )"""
        self.execute(sql, commit=True)

    def create_table_of_users(self):
        sql = """
        create table `users` (
          `user_id` INTEGER PRIMARY KEY not null,
          `first_name` VARCHAR(255) not null,
          `last_name` VARCHAR(255) not null,
          `login` VARCHAR(255) not null,
          `password` VARCHAR(255) not null,
          `login_status` VARCHAR(255) not null
    )"""
        self.execute(sql, commit=True)

    def user_login(self, login, password):
        sql = "SELECT * FROM users WHERE login = ? and password = ?"
        result = self.execute(sql, (login, password), fetchone=True)

        if result is not None:
            sql_update = "UPDATE users SET login_status='active' WHERE user_id=?"
            self.execute(sql_update, (result.user_id,), commit=True)
            return json.dumps({
                'server_answer': f"Вы успешно вошли в аккаунт",
                'answer_status': 'ok'
            })
        else:
            return json.dumps({
                'server_answer': f"Пользователя с такими данными не существует",
                'answer_status': 'ok'
            })

    def user_register(self, login, password, first_name, last_name):
        sql = "SELECT * FROM users WHERE login=?"
        result = self.execute(sql, (login,), fetchone=True)

        if result is not None:
            return json.dumps({
                'server_answer': f"Пользователь с таким именем уже зарегистрирован",
                'answer_status': 'ok'
            })
        else:
            sql_insert = "INSERT INTO users (login, password, first_name, last_name, login_status) VALUES (?, ?, ?, ?, ?)"
            self.execute(sql_insert, (login, password, first_name, last_name, 'active'), commit=True)
            print("Вы успешно зарегистрировались")
            return json.dumps({
                'server_answer': f"Вы успешно зарегистрировались",
                'answer_status': 'ok'
            })

    def login_status(self, login):
        sql = "SELECT login_status FROM users WHERE login=?"
        result = self.execute(sql, (login,), fetchone=True)
        if result is not None:
            status = result[0]
            return status
        else:
            return None

    def get_rooms_list(self):
        sql = "SELECT * FROM rooms"
        result = self.execute(sql, fetchall=True)

        rooms = []

        for item in result:
            rooms.append({
                'room_floor':item[0],
                'room_number':item[1],
                'occupied': bool(item[2]),
                'room_resident':item[3]
            })

            return json.dumps({
                'server_answer':'Список комнат',
                'rooms': rooms
            })


if __name__ == '__main__':
    db = Database()
    db.user_register("zxc", "123", "Gleb", "Kim")

