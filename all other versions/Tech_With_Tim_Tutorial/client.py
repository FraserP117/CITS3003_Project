import socket

HEADER = 64 # a fixed length header of length 64 bytes.
# the first message to the server from the client is a header of length 64
# which tells the server the length of the message that is comming next.
#       - since we (the server) don't know how big a message from the client
#         will be; we will simply institute the protocol that the first message
#         to the server (from this client) must be a mesage of length 64.
#       - the 64 bytes in the header will have a number "in them" which
#         represents the length of the amount of bytes for the incomming
#         message from the client.
#       - Example:
#           * say client wants to send "hello"
#           * the first thing sent to the server is "5"; padded such that it is
#             64 bytes long.

PORT_NUMBER = 5051 # port number for some service on the server
SERVER_IP = socket.gethostbyname(socket.gethostname()) # the server's IP address
ADDR = (SERVER_IP, PORT_NUMBER) # (server's IP, port number for some service on the server)
FORMAT = 'utf-8' # encoding format for all messages
DISCONNECT_REQUEST = "!DISCONNECT" # client sends this to server to notify the
# server of its disconect

# client socket:
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server:
client_socket.connect(ADDR)

def send_message_to_server(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    # now we have to padd send_length to make it 64 bytes long
    send_length += b' ' * (HEADER - len(send_length))

    # send the "send_length" HEADER to the server:
    client_socket.send(send_length)

    # send the data to the server:
    client_socket.send(message)

    # recieve the messgae from the server - sort of an acknowlegement:
    print(client_socket.recv(2048).decode(FORMAT))

send_message_to_server("HELLO Server!!!!")
input()
send_message_to_server("Who want's to play?")
input()
send_message_to_server("I requre a service!!")
input()
send_message_to_server(DISCONNECT_REQUEST)
