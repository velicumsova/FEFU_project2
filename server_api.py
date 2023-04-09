import json
# обработавыет запросы, полученные сервером от клиента, и возвращает ответ на них, который сервер отправит клиенту
# + вносит соответсвующие изменения в базы данных и т.д


class ClientSession:
    def __init__(self):
        self.client_username = None
        self.client_password = None
        self.is_admin = False

    def message_handle(self, command: str):
        # сервер принемает команды в формате json  и отвечает на них тоже json
        # пример команды(запроса от пользователя):
        # '{"command_name": "login", "args": {"login": "123", "password": "123"}}'
        # Другими слова сервер получает json словарь формата
        '''{
            'command_name': 'Имя команды от клиента',
            'args': Словарь с дополнитальными данными от пользователя (клиента)
        }'''

        try:
            command = json.loads(command)
            if not ('command_name' in command):
                return json.dumps({
                    'server_answer': 'no command_name in command',
                    'answer_status': 'problem'  # статус problem - только в случае неверного формата команды
                })
        except Exception as er:
            return json.dumps({
                'server_answer': 'invalid json',
                'answer_status': 'problem' # статус problem - только в случае неверного формата команды
            })

        # ниже представлен список доступных команд. Их всех нужно реализовать. В каждой каманде:
        # command - пример(формат) команды от пользователь + что должна сделать команда + формат ответа

        # команды для всех пользователей
        if command['command_name'] == 'login':
            command = {
                'command_name': 'login',
                'args': {
                    'login': '123',
                    'password': '123',
                }
            }
            # Команда должна проверять зарегистрирован ли пользователь с указанными данными.
            # Если да, то меняет статус пользователя

            return json.dumps({
                'server_answer': 'Вы успешно вошли в аккаунт/Пользователя с такими данными не существует',
                'login_status': True,
                'answer_status': 'ok'
            })
        elif command['command_name'] == 'register':
            command = {
                'command_name': 'register',
                'args': {
                    'login': '123',
                    'password': '123',
                }
            }
            # Команда должна регистрировать пользователя с указанными данными.
            # Если такого пользователя нет, то регистрировать его

            return json.dumps({
                'server_answer': 'Вы успешно зарегистрировались/Пользователя с таким именем уже существует',
                'register_success_status': True,
                'answer_status': 'ok'
            })
        elif command['command_name'] == 'login_status':
            command = {
                'command_name': 'login_status',
            }
            # Команда должна проверять текущий статус пользователя

            return json.dumps({
                'server_answer': '',
                'register_status': True,
                'is_admin': True,
                'answer_status': 'ok'
            })
        # команды для пользователей, которые вошли в аккаунт (мы уже знаем их логины, поэтому пользователя не нужно их передавать)
        elif command['command_name'] == 'get_rooms_list':
            command = {
                'command_name': 'get_rooms_list',
            }
            # получаем список всех комнат

            return json.dumps({
                'server_answer': 'Список комнат',
                'rooms': [
                    {
                        'room_number': 1, # уникален для каждой комнаты
                        'room_floor': 2,
                        'occupied': False, # True - комна занята False - комната свободна
                        'room_resident': '', # ник человека проживающего в комнате (эти данные получает только админ),
                        'reserve_list': ['Gor', 'Nom'] # Список
                    },
                    {
                        'room_number': 4,
                        'room_floor': 54,
                        'occupied': True,  # True - комна занята False - комната свободна
                        'room_resident': 'John',  # ник человека проживающего в комнате (эти данные получает только админ)
                    }
                ],
                'answer_status': 'ok'
            })
        elif command['command_name'] == 'reserve_room':
            command = {
                'command_name': 'reserve_room',
                'args': {
                    'room_number': 1
                }
            }
            # резервирование свободной комнаты, можно зарезервировать только 1 не занятую комнату
            # создаёт уведомление для пользователя

            # если админ подтверждает резервирование, то пользователь засиляется в комнату

            return json.dumps({
                'server_answer': 'Комната успешно зарезервирована/Комната уже занята',
                'reserve_status': 'ok',
                'answer_status': 'ok'
            })
        elif command['command_name'] == 'get_notifications':
            command = {
                'command_name': 'get_notifications',
            }
            # Некоторые действия создают уведомления
            # получаем все уведомление
            # типы уведомлений:
            # 1) Комната успешно зарезервирована
            # 2) Админ не подтвердил вашу резервацую
            # 3) Вы заселены (Админ подтвердил вашу резервацую)
            # 4) Вы выселены

            return json.dumps({
                'server_answer': 'Есть новые уведомления',
                'notifications': [
                    {
                        'notification_time': '21:43 09.03.2002',
                        'notification_title': 'Заголовок',
                        'notification_text': 'Текст уведомления',
                        'notification_read_status': True, # True - прочитано False - не прочитано
                    }
                ],
                'answer_status': 'ok'
            })
        # команды для админов
        elif command['command_name'] == 'get_all_users':
            command = {
                'command_name': 'get_all_users',
            }
            # все зарегестрированные пользователи

            return json.dumps({
                'server_answer': '',
                'users': [
                    {
                        'login': 'Jonh',
                        'password': '1234',
                        'is_admin': False,
                        'room_number': 5, # если нет комнаты то -1
                        'reserve_room_number': -1 # номер зарезервированной комнаты (-1 если нет)
                    },
                    {
                        'login': 'Jonh2',
                        'password': '12343',
                        'is_admin': True,
                        'room_number': -1,  # если нет комнаты то -1
                        'reserve_room_number': -1
                    }
                ],
                'answer_status': 'ok'
            })
        elif command['command_name'] == 'change_user_residence_status':
            command = {
                'command_name': 'change_user_residence_status',
                'args': {
                    'change_type': 'confirm_reserve/cansel_reserve/kick_from_room',
                    'username': 'John', # мы и так знаем где John живёт или где хочет
                    'reason': 'причина от админа, нужна для уведомления пользователю. '
                              'Например: Комитет по заселению одобрил вашу кандидатуру!'
                }
            }

            # меняем статус проживание пользователя подтверждаем/отклоняем его бронь или выселяем пользователя
            # создаёт уведомление для пользователя

            return json.dumps({
                'server_answer': 'Вы успешно заселили пользователя',
                'command_status': True, # команда успешно выполнена
                'command_error': '', # возможные ошибки, например нет пользователя. Тогда command_status==False
                'answer_status': 'ok'
            })

        return json.dumps({
            'server_answer': 'unknown command',
            'answer_status': 'problem'
        })


