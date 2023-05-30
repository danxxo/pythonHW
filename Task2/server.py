import socket
import threading
from threading import Event, Lock
import time
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

        self.rooms = {'1': [], '2': []}

        self.mutex = Lock()


    # def __del__(self):
    #     self.conn.close()

    def send_room_message(self, room, message): 
        for user in self.rooms.get(room):

            self.user_connection_table.get(user).send(message)
            

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
                connection = self.user_connection_table.get(user)
                message = connection.recv(1024)
                message_decoded = message.decode('utf-8')

                # if message_decoded[message_decoded.find(':')+2:len(message_decoded)] == 'close':
                #     self.send_room_message(room, f'\'{user}\' disconnected from'.encode('utf-8'))
                #     connection.send('close'.encode('utf-8'))
                #     time.sleep(2)
                #     connection.close()
                #     self.user_connection_table.pop(user)
                #     self.rooms[room].remove(user)
                #     print(self.user_connection_table)
                #     print(self.rooms)
                #     return
                
                self.send_room_message(room, message)
                # print(threading.active_count())
            except:
                #TODO caching
                break
                self.send_room_message(room, f'\'{user}\' disconnected from'.encode('utf-8'))
                connection.close()
                self.user_connection_table.pop(user)
                self.rooms[room].remove(user)
                print(self.user_connection_table)
                print(self.rooms)
                break

    def add_user_to_room(self, user, room):
        ...

    def run(self):
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

            self.send_room_message(room, f'\'{user}\' connected to the room. Welcome'.encode('utf-8'))

            thread = threading.Thread(target=self.handle_client, args=[room, user])
            thread.start()
            thread.join()
    


server = Server(users=3)
server.run()