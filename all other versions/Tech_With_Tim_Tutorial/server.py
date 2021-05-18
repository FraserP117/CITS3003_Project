import socket
import threading

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

# server socket:
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the server_socket to an address:
server_socket.bind(ADDR)

'''
This function will run for each client - in the client's own thread.
'''
def handle_a_client_request(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected to the server.")

    connected = True;
    while connected:
        # wait to recieve info from the client and store this in a "msg" variable:
        # msg_length = conn.recv(HEADER).decode(FORMAT) # OG Version
        msg_length = len(conn.recv(HEADER).decode(FORMAT))
        if msg_length: # if the message has SOME content:
            msg_length = int(msg_length)

            # and then the "actual" message:
            msg = conn.recv(msg_length).decode(FORMAT)

            # check if client wanted to disconnect:
            if msg == DISCONNECT_REQUEST:
                connected = False

            # print out some info:
            print(f"[{addr}] {msg}")

            # send a message from the server to the client:
            conn.send("MSG recieved".encode(FORMAT))

    # close the current conection with this client:
    conn.close()

def start_server():
    server_socket.listen()
    print(f"[LISTENING] Server is listening on: {SERVER_IP}")

    while True:
        # conn = the client's own socket object
        # addr = IP address of connecting client
        conn, addr = server_socket.accept()

        # create a thread:
        thread = threading.Thread(
            target = handle_a_client_request,
            args = (conn, addr) # give the connection and address of the client
            # to the server's client handling function
        )
        # print the number of active threads - for debug only:
        # OG print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") # subtract 1 because start_server() is also running
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()}") # subtract 1 because start_server() is also running
        # start the thread:
        thread.start()

print("[STARTING] Starting the server...")
start_server()
