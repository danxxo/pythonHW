import socket
import threading
import time


class Client:
    def __init__(self) -> None:
        self.host = socket.gethostname()
        self.port = 55000
        self.client_socket = socket.socket()

        while True:
            try:
                self.client_socket.connect((self.host, self.port))
                break
            except ConnectionRefusedError as ex:
                print(f"Client exc: {ex}. Wait for server in 5 sec...")
                time.sleep(5)

        print("To end the connection, type: close")

        self.user = input("User: ")
        self.room = input("Room: ")
        self.mutex = threading.Lock()

    def client_recieve(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                match message:
                    case "close":
                        self.client_socket.close()
                        break
                    case "User":
                        self.client_socket.send(self.user.encode("utf-8"))
                    case "Room":
                        self.client_socket.send(self.room.encode("utf-8"))
                    case "InvalidUserName":
                        new_user_name = input("Invalid User Name. Type new: ")
                        self.user = new_user_name
                        self.client_socket.send(new_user_name.encode("utf-8"))
                    case _:
                        print(message)
            except:
                print("error")
                break

    def client_send(self):
        while True:
            try:
                input_msg = input()
                if input_msg == "close":
                    self.client_socket.send(input_msg.encode("utf-8"))
                    break
                else:
                    message = f"'{self.user}': {input_msg}"
                    self.client_socket.send(message.encode("utf-8"))
            except:
                break


client = Client()

send_thread = threading.Thread(target=client.client_send)
send_thread.start()

recieve_thread = threading.Thread(target=client.client_recieve)
recieve_thread.start()
