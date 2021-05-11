import socket

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen()

        while True:
            connection, address = sock.accept()
            recieved_data = connection.recv(1024)
            if recieved_data:
                print(recieved_data)
                connection.sendall("the server got your message!".encode())
            else:
                connection.close()
                break
            connection.close()
        sock.close()

if __name__ == '__main__':
    server = Server("localhost", 6969)
    server.start_server()
