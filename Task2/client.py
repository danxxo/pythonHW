import socket
import threading
import time


class Client:
    def __init__(self) -> None:
        self.host = socket.gethostname()
        self.port = 55000

        self.client_socket = socket.socket()
        self.client_socket.connect((self.host, self.port))

        print('To end the connection, type: close')

        self.user = input("User: ")
        self.room = input("Room: ")

        self.mutex = threading.Lock()

    def client_recieve(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                if message == 'close':
                    print('clent recieving will be closed')
                    self.client_socket.close()
                    break
                elif message == "User":
                    self.client_socket.send(self.user.encode("utf-8"))
                elif message == "Room":
                    self.client_socket.send(self.room.encode("utf-8"))
                else:
                    print(message)
            except:
                print("error")
                break

    def client_send(self):
        while True:
            input_msg = input()
            if input_msg == 'close':
                self.client_socket.send(input_msg.encode("utf-8"))
                break
            else:
                message = f"'{self.user}': {input_msg}"
                self.client_socket.send(message.encode("utf-8"))


client = Client()

send_thread = threading.Thread(target=client.client_send)
send_thread.start()

recieve_thread = threading.Thread(target=client.client_recieve)
recieve_thread.start()
