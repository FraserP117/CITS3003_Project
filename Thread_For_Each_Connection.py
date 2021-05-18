import threading
import socket

'''
How use threads with sockets. Method uses a thread for each socket
connection.

Use this with Basic_Client.py
'''

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def process_connection(self, connection):
        recieved_data = connection.recv(1024)
        if recieved_data:
            print(recieved_data)
            connection.sendall("Got your message!".encode())
        connection.close()

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen()

        while True:
            # the diference here is that when a new connection is accepted,
            # we create a new thread to allow for multiple client connections
            # at once:
            connection, address = sock.accept()
            threading.Thread(
                target = self.process_connection,
                args = (connection,),
                daemon = True
            ).start()


server = Server("localhost", 6969)
server.start()

if __name__ == '__main__':
    main()

'''
This works well for multiple connections.
However, the more connections; the more threads needed.
There is a creation/destruction overhead associated with threads and
so the more threads; the slower things will run.
'''
