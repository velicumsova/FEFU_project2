import json
import socket

class Client:
    def __init__(self, ip='127.0.0.1', port=12345):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))

    def send_message_to_server(self, message):
        self.client.send(message.encode('utf-8'))
        response = self.client.recv(1024).decode("utf-8")

        return response

    def close_connection(self):
        self.client.close()


if __name__ == '__main__':
    client = Client()
    while True:
        res = client.send_message_to_server(input('Введите сообщение:'))
        print(res)