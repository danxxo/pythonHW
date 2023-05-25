import socket


def client():
    host = socket.gethostname()  # получаем имя хоста
    port = 55000  # указываем порт сервера

    client_socket = socket.socket()
    client_socket.connect((host, port))  # соединяемся с сервером

    message = input("Введите сообщение: ")

    while message.strip() != 'close':
        client_socket.send(message.encode())  # отправляем сообщение
        print(f"Ожидаем сообщение от сервера")
        data = client_socket.recv(1024).decode()  # получаем данные

        print(f'Received from server: {data}')

        message = input("Введите сообщение: ")

    client_socket.close()  # закрываем соединение


if __name__ == '__main__':
    client()
