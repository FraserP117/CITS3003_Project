import socket

'''
Code to implement a simple client.
'''

# the size of the headder:
HEADERSIZE = 10

# create an IPv4 TCP socket:
# a socket is the "end point" that recieves data - can send/recieve data
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# rather than "binding" to a particulat socket - as in the server - we really want to
# the servers socket is represented as a tuple: (IP, Port_Number):
# socket.getsockname() just gets the name of the IP address of the hostname: "localhost"
# "connect" to a server's socket:
# the port is the server's port
client_socket.connect((socket.gethostname(), 6225))

# we will accept the message sent from the server:
# here recv(K) means to "recieve" K cunks of data from the socket.
while True:
    full_msg = ''
    new_msg = True # a flag
    while True:
        msg = client_socket.recv(16) # server_socket ??
        if new_msg:
            print(f"new message length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE].decode("utf-8"))
            new_msg = False # it's not new anymore!

        full_msg += msg.decode("utf-8")

        if len(full_msg) - HEADERSIZE == msglen:
            print("recieved full message!")
            print(full_msg[HEADERSIZE:])
            new_msg = True # now we start again
            full_msg = ''  # now we start again

    # print out the message:
    print(full_msg)
