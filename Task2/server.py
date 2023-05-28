import socket
import threading
# Первым должен быть запущен сервер! servier и client должны быть запущены в разных терминалах / вкладках PyCharm (IDE)

'''
    Сервер
        должен служить для пересылки сообщений между клиентами
        должен иметь возможность обрабатывать несколько сообщений, без ожиданий
        может запоминать сообщения для клиентов, которых сейчас нет в чате
        и при появлении клиента отдавать недоставленные сообщения
'''

class Server():
    def __init__(self, users=2) -> None:
        self.host = socket.gethostname()
        self.port = 55000

        self.server_socket = socket.socket()
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(users)

        #self.connection, self.address = self.server_socket.accept()
        print('Starting server')

        self.user_connection_table = {}

        self.rooms = {}

        self.run()

    # def __del__(self):
    #     self.conn.close()

    def send_room_message(self, room, message):
        for user in self.rooms[room]:
            self.user_connection_table[user].send(message)
            

    '''
        table dict :
            client1 : object socket ... 1
            client2 : object socket ... 2
        
        rooms:
            'room1' : [client1, client2,  ... , ]
    '''

    def handle_client(self, room, user):
        while True:
            try:
                connection = self.user_connection_table[user]
                message = connection.recv(1024)
                self.send_room_message(room, message)
            except:
                #TODO caching

                connection.close()
                self.send_room_message(room, f'\'{user}\' disconnected from')
                self.user_connection_table.pop(user)
                self.rooms[room].remove(user)
                break



    def run(self):
        while True:
            print('Server is running')
            connection, address = self.server_socket.accept()
            print(f'connection on {address}')
            
            connection.send('User: '.encode('utf-8'))
            user = connection.recv(1024)
            connection.send('Room: '.encode('utf-8'))
            room = connection.recv(1024)

            self.user_connection_table[user] = connection
            self.rooms[room] = user

            self.send_room_message(room, f'\'{user}\' connected to the room. Welcome')

            thread = threading.Thread(target=self.handle_client, args=[room, user])
            thread.start()


    # def working_with_clients(self):
    #     while True:
    #         print(f"Ожидаем сообщение от клиента")
    #         data = self.connection.recv(1024).decode()  # получаем данные, разрешаем размер пакета до 1024 байт
    #         if not data:  # если нет данных, разрываем соединение
    #             break
    #         print(f"Сообщение от пользователя: {data}")
    #         data = input('Введите сообщение: ')
    #         self.connection.send(data.encode())  # отправляем данные клиенту
            


# def server():
#     host = socket.gethostname()  # получаем имя хоста
#     port = 55000  # устанавливаем порт соединения

#     server_socket = socket.socket()  # создаём сокет
#     server_socket.bind((host, port))  # связываем хост и порт (в сокет)
#     print(f"Связываем сокет")

#     server_socket.listen(1)  # сколько клиентов мы ожидаем
#     conn, address = server_socket.accept()  # разрешаем соединение
#     print(f"Соединение от: {address}")
#     while True:
#         print(f"Ожидаем сообщение от клиента")
#         data = conn.recv(1024).decode()  # получаем данные, разрешаем размер пакета до 1024 байт
#         if not data:  # если нет данных, разрываем соединение
#             break
#         print(f"Сообщение от пользователя: {data}")
#         data = input('Введите сообщение: ')
#         conn.send(data.encode())  # отправляем данные клиенту

#     conn.close()  # закрываем соединение


# if __name__ == '__main__':
#     server()

server = Server(users=3)