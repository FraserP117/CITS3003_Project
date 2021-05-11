import socket

class Client:

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server_host, self.server_port))

        sock.sendall("Connecting to yer server!".encode())
        response = sock.recv(1024)
        print(response)
        sock.close()

if __name__ == '__main__':
    client = Client("localhost", 6969)
    client.connect()
