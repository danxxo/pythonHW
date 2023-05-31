from threading import Event, Lock, Thread, active_count
from pathlib import Path
import socket
import time


class Server:
    def __init__(self, delete_cache_after_end=True) -> None:
        self.host = socket.gethostname()
        self.port = 55000

        self.server_socket = socket.socket()

        while True:
            try:
                self.server_socket.bind((self.host, self.port))
                break
            except OSError as er:
                print(f'Server error {er}. Retrying in 5 sec..(approx 15 secs..)')
                time.sleep(5)

        self.server_socket.listen()

        self.delete_cache_after_end = delete_cache_after_end

        print("Starting server")

        self.user_connection_table = {}
        self.rooms = {}
        self.room_path = Path("./cache")

        if not Path.exists(self.room_path):
            Path.mkdir(self.room_path)

        self.mutex = Lock()

    def create_one_cached_file(self, room):
        file_name = room + ".txt"
        file_path = self.room_path.joinpath(file_name)
        with open(file_path, 'w') as file:
            file.write(f"cache_room_{room}\n")

    def create_cached_files(self):
        for i in self.rooms:
            self.create_one_cached_file(i)

    def cache(self, room, message):
        file_path = self.room_path.joinpath(f"{room}.txt")
        with open(file_path, "a") as file:
            file.write(message.decode("utf-8"))
            file.write("\n")

    def recieve_cache(self, room):
        file_path = self.room_path.joinpath(f"{room}.txt")
        with open(file_path, "r") as file:
            message = file.read()
        message = message.replace(f'cache_room_{room}\n', '')
        return message[:-1].encode("utf-8")
    
    def delete_cache(self):
        file_iter = Path.iterdir(self.room_path)
        for x in list(file_iter):
            Path(x).unlink(missing_ok=True)

    def create_room(self, room):
        self.rooms.update({f'{room}': []})
        self.create_one_cached_file(room)

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
                decoded_msg = message.decode('utf-8')
                if decoded_msg == 'close':
                    connection.send('close'.encode('utf-8'))
                    connection.close()
                    self.user_connection_table.pop(user)
                    self.rooms[room].remove(user)
                    break
                self.send_room_message(room, message)
                with self.mutex:
                    self.cache(room, message)

            except:
                break


    def run(self):
        self.create_cached_files()
        while True:
            try:
        
                print("Server is running")
                connection, address = self.server_socket.accept()
                print(f"connection on {address}")

                connection.send("User".encode("utf-8"))
                user = connection.recv(1024).decode("utf-8")
                connection.send("Room".encode("utf-8"))
                room = connection.recv(1024).decode("utf-8")

                if room not in self.rooms:
                    print('new room: ', room)
                    self.create_room(room)

                self.user_connection_table[user] = connection
                self.rooms[room].append(user)

                # if len(self.rooms[room]) > 1:
                #     connection.send(
                #         "--- You have unread room messages! ---".encode("utf-8")
                #     )
                connection.send(self.recieve_cache(room))

                self.send_room_message(
                    room, f"'{user}' connected to the room. Welcome".encode("utf-8")
                )

                thread = Thread(target=self.handle_client, args=[room, user])
                thread.start()
                # thread.join()
            except KeyboardInterrupt:
                print('server is closed')
                self.server_socket.close()
                if self.delete_cache_after_end:
                    self.delete_cache() # There we clean the 
                    print('Cache was deleted')
                break


server = Server(delete_cache_after_end=True)
server.run()
