import socket

'''
Code to implement a simple server.
'''

'''
# OG code for a simple server:

# create an IPv4 TCP socket:
# a socket is the "end point" that recieves data - can send/recieve data
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind server_socket to a tuple: (IP, Port_Number):
# socket.getsockname() just gets the name of the IP address of the hostname: "localhost"
server_socket.bind((socket.gethostname(), 6235))

# listen on this socket for clients:
# have a queue of 5 possible clients
server_socket.listen(5)

# listen forever for connections:
while True:
    # client_socket = the client's socket object much like "server_socket"
    # client_address = the IP address of the client
    client_socket, client_address = server_socket.accept()

    # print some info after sucesful client-server connection:
    print(f"a connection from client: {client_address} has been succesfuly established!")

    # send some info to the client socket- from te server:
    # bytes takes a message and the type of bytes to send
    client_socket.send(bytes("Welcome to the server!", "utf-8"))

    # close the socket with the client:
    client_socket.close()
'''


"""
IMPORTANT NOTES:

* From the server's point of view, client's have diferent IP addresses.
* Just send back to the corresponding IP address via a TCP socket to communicate with each client.
"""

# the size of the headder:
HEADERSIZE = 10

# create an IPv4 TCP socket:
# a socket is the "end point" that recieves data - can send/recieve data
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind server_socket to a tuple: (IP, Port_Number):
# socket.getsockname() just gets the name of the IP address of the hostname: "localhost"
# the Port_Number: 6225 is the port number "for this application"
server_socket.bind((socket.gethostname(), 6225))

# listen on this socket for clients:
# have a queue of 5 possible clients
server_socket.listen(5)

# listen forever for connections:
while True:
    # client_socket = the client's socket object much like "server_socket"
    # client_address = the IP address of the client
    client_socket, client_address = server_socket.accept()

    # print some info after sucesful client-server connection:
    print(f"a connection from client: {client_address} has been succesfuly established!")

    # a fixed length header:
    msg = "Welcome to the server!"
    msg = f'{len(msg):<{HEADERSIZE}}'+ msg

    # send some info to the client socket- from te server:
    # bytes takes a message and the type of bytes to send
    client_socket.send(bytes(msg, "utf-8"))

    # close the socket with the client:
    client_socket.close()
