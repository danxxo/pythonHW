import socket
import threading


class Client():
    def __init__(self) -> None:
        self.host = socket.gethostname()
        self.port = 55000

        self.client_socket = socket.socket()
        self.client_socket.connect((self.host, self.port))

        self.threads = []

        self.user = input('User: ')
        self.room = input('Room: ')





    def client_recieve(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message == 'User':
                    print('Client send')
                    self.client_socket.send(self.user.encode('utf-8'))
                elif message == 'Room':
                    self.client_socket.send(self.room.encode('utf-8'))
                elif message == 'close':
                    self.end()
                    return
                else:
                    print(message)
            except:
                print('error')
                self.client_socket.close()
                break

    def client_send(self):
        while True:
            input_message = input()
            if input_message == 'close':
                self.end()
                return
            message = f'\'{self.user}\': {input_message}'
            self.client_socket.send(message.encode('utf-8'))


    def end(self):
        for i in self.threads:
            i.join()

client = Client()

recieve_thread = threading.Thread(target=client.client_recieve)
recieve_thread.start()

send_thread = threading.Thread(target=client.client_send)
send_thread.start()

# send_thread.join()
# recieve_thread.join()

# recieve_thread.join()
# send_thread.join()

'''
    Клиент
        клиенты должны быть идентифицируемы (иметь id), например, могут вводить имя при входе
        должны иметь возможность писать и читать сообщения асинхронно, не дожидаясь друг друга 
        (можно испольовать потоки)
        сообщения клиентов должны быть маршрутизируемыми, то есть помимо текста, содержать информацию, 
        о том какому клиенту они предназначены (id), а адресат должен знать об отправителе
'''
