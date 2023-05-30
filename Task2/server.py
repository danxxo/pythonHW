import socket
import threading
from threading import Event, Lock
import time
from pathlib import Path


# Первым должен быть запущен сервер! servier и client должны быть запущены в разных терминалах / вкладках PyCharm (IDE)

'''
    Сервер
        должен служить для пересылки сообщений между клиентами
        должен иметь возможность обрабатывать несколько сообщений, без ожиданий
        может запоминать сообщения для клиентов, которых сейчас нет в чате
        и при появлении клиента отдавать недоставленные сообщения
'''


'''
    table dict :
        client1 : object socket ... 1
        client2 : object socket ... 2
    
    rooms:
        'room1' : [client1, client2,  ... , ]
'''

class Server():
    def __init__(self, users=2) -> None:
        self.host = socket.gethostname()
        self.port = 55000

        self.server_socket = socket.socket()
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(users)

        print('Starting server')

        self.user_connection_table = {}
        self.rooms = {'1': [], '2': []}
        self.room_path = Path('./cache')
        self.mutex = Lock()

    def create_cached_files(self):
        for i in self.rooms:
            file_name = i + '.txt'
            file_path = self.room_path.joinpath(file_name)
            with open(file_path, 'w') as file:
                file.write(f'cache_room_{i}\n')

    def cache(self, room, message):
        file_path = self.room_path.joinpath(f'{room}.txt')
        with open(file_path, 'a') as file:
            file.write(message.decode('utf-8'))
            file.write('\n')

    def recieve_cache(self, room):
        file_path = self.room_path.joinpath(f'{room}.txt')
        with open(file_path, 'r') as file:
            message = file.read()
        return message.encode('utf-8')


    def send_room_message(self, room, message): 
        for user in self.rooms.get(room):
            # with self.mutex:
            #     self.cache(room, message)
            self.user_connection_table.get(user).send(message)
            
    def handle_client(self, room, user):
        while True:
            try:
                connection = self.user_connection_table.get(user)
                message = connection.recv(1024)
                self.send_room_message(room, message)
                with self.mutex:
                    self.cache(room, message)

            except:
                break
                # self.send_room_message(room, f'\'{user}\' disconnected from'.encode('utf-8'))
                # connection.close()
                # self.user_connection_table.pop(user)
                # self.rooms[room].remove(user)
                # print(self.user_connection_table)
                # print(self.rooms)
                # break

    def run(self):
        self.create_cached_files()
        while True:
            print('Server is running')
            connection, address = self.server_socket.accept()
            print(f'connection on {address}')
            
            connection.send('User'.encode('utf-8'))
            user = connection.recv(1024).decode('utf-8')
            connection.send('Room'.encode('utf-8'))
            room = connection.recv(1024).decode('utf-8')

            self.user_connection_table[user] = connection
            self.rooms[room].append(user)

            if len(self.rooms[room]) > 1:
                connection.send('--- You have unread room messages! ---'.encode('utf-8'))
                connection.send(self.recieve_cache(room))

            self.send_room_message(room, f'\'{user}\' connected to the room. Welcome'.encode('utf-8'))

            thread = threading.Thread(target=self.handle_client, args=[room, user])
            thread.start()
            # thread.join()
    

server = Server(users=3)
server.run()