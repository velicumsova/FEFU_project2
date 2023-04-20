import socket
import threading
from server_api import ClientSession


# принимает запросы от клиента и отвечает на них на server_api
class Server:
    def __init__(self, ip='127.0.0.1', port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen(5)
        print(f'[+] Сервер запущен.')

    def start_working(self):
        print(f'[+] Ожидается подключение.')
        while True:
            client_socket, addr = self.server.accept()
            print(f'[+] Новое подключение к серверу. {addr}')
            thread = threading.Thread(target=self.client_handler, args=(client_socket, addr))
            thread.start()

    @staticmethod
    def client_handler(client_socket, addr):
        client_session = ClientSession()
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8') # сообщение от клиента
                if not data:
                    break
                # print(data)
                server_answer = client_session.message_handle(data)
                client_socket.send(f"{server_answer}".encode('utf-8'))

            except Exception as e:
                print(f"[ERROR] {e}")
                break

        print(f"[+] {addr} отлючился от сервера.")
        client_socket.close()


if __name__ == "__main__":
    server = Server()
    server.start_working()

