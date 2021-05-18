# CITS3002 2021 Assignment
#
# This file implements a basic server that allows a single client to play a
# single game with no other participants, and very little error checking.
#
# Any other clients that connect during this time will need to wait for the
# first client's game to complete.
#
# Your task will be to write a new server that adds all connected clients into
# a pool of players. When enough players are available (two or more), the server
# will create a game with a random sample of those players (no more than
# tiles.PLAYER_LIMIT players will be in any one game). Players will take turns
# in an order determined by the server, continuing until the game is finished
# (there are less than two players remaining). When the game is finished, if
# there are enough players available the server will start a new game with a
# new selection of clients.

import socket
import sys
import tiles
import threading
import queue
import time

SERVER_IP = ''
PORT_NUMBER = 30020
# SERVER_ADDR = (SERVER_IP, PORT_NUMBER)

# # create a TCP/IP socket
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# # bind to the server address
# server_socket.bind(SERVER_ADDR)

# make 2 lists:
# any time we set up a connection we get: a connection object and address info
# all_connections = [] # a list of client "connection objects"
# all_addresses = []   # a list of all client "addresses"
#
# # we need to identify each thread by it's task/job:
# # the first thread "1" will handle connections - allow clients to connect.
# # the second thread "2" will send a client commands over the network
# THREAD_JOB_NUMBER = [1, 2]

# # create a task queue:
# queue = Queue()


all_connections = [] # a list of client "connection objects"        # Dom's "master"
all_addresses = []   # a list of all client "addresses"             # Dom's "master_address"
THREAD_JOB_NUMBER = [1, 2]


class Server:

    def __init__(self, host_address, port_number):
        self.host = host_address
        self.port = port_number
        self.number_of_threads = 2
        # self.thread_pool = [] # just a list of threads "in the pool"
        self.task_queue = queue.Queue()
        # make 2 lists:
        # any time we set up a connection we get: a connection object and address info



        # self.all_connections = [] # a list of client "connection objects"        # Dom's "master"
        # self.all_addresses = []   # a list of all client "addresses"             # Dom's "master_address"
        #
        # # we need to identify each thread by it's task/job:
        # # the first thread "1" will handle connections - allow clients to connect.
        # # the second thread "2" will send a client commands over the network
        # self.THREAD_JOB_NUMBER = [1, 2]

        # SERVER_IP = ''
        # PORT_NUMBER = 9998 # 9999
        #
        # conn, addr = server_socket.accept()
        # # conn.setblocking(1) # specify "no timeout"
        # # add the connection object to the list of client connections:
        # self.all_connections.append(conn)
        # # add the address of the newwly connected client to the address list:
        # self.all_addresses.append(addr)
        # # provide connection status info:
        # print(f"\nConnection established with: {addr[0]} on port: {addr[1]}")

    def client_handler(self, connection, address):
        print(f"[NEW CONNECTION] {address} connected to the server.")

        host, port = address
        name = '{}:{}'.format(host, port)

        idnum = 0
        live_idnums = [idnum]

        connection.send(tiles.MessageWelcome(idnum).pack())
        connection.send(tiles.MessagePlayerJoined(name, idnum).pack())
        connection.send(tiles.MessageGameStart().pack())

        for _ in range(tiles.HAND_SIZE):
            tileid = tiles.get_random_tileid()
            connection.send(tiles.MessageAddTileToHand(tileid).pack())

        connection.send(tiles.MessagePlayerTurn(idnum).pack())

        board = tiles.Board()

        buffer = bytearray()

        while True:
            # with lock:
            # connection, msg = self.task_queue.get() # added

            chunk = connection.recv(4096)
            if not chunk:
                print('client {} disconnected'.format(address))
                return

            buffer.extend(chunk)

            while True:
                msg, consumed = tiles.read_message_from_bytearray(buffer)
                if not consumed:
                    break

                buffer = buffer[consumed:]

                print('received message {}'.format(msg))

                # sent by the player to put a tile onto the board (in all turns except
                # their second)
                if isinstance(msg, tiles.MessagePlaceTile):
                    if board.set_tile(msg.x, msg.y, msg.tileid, msg.rotation, msg.idnum):
                        # notify client that placement was successful
                        connection.send(msg.pack())

                        # check for token movement
                        positionupdates, eliminated = board.do_player_movement(live_idnums)

                        for msg in positionupdates:
                            connection.send(msg.pack())

                        if idnum in eliminated:
                            connection.send(tiles.MessagePlayerEliminated(idnum).pack())
                            return

                        # pickup a new tile
                        tileid = tiles.get_random_tileid()
                        connection.send(tiles.MessageAddTileToHand(tileid).pack())

                        # start next turn
                        connection.send(tiles.MessagePlayerTurn(idnum).pack())

                # sent by the player in the second turn, to choose their token's
                # starting path
                elif isinstance(msg, tiles.MessageMoveToken):
                    if not board.have_player_position(msg.idnum):
                        if board.set_player_start_position(msg.idnum, msg.x, msg.y, msg.position):
                            # check for token movement
                            positionupdates, eliminated = board.do_player_movement(live_idnums)

                            for msg in positionupdates:
                                connection.send(msg.pack())

                            if idnum in eliminated:
                                connection.send(tiles.MessagePlayerEliminated(idnum).pack())
                                return

                            # start next turn
                            connection.send(tiles.MessagePlayerTurn(idnum).pack())
                # # added:
                # self.task_queue.task_done()

    # create a socket
    def socket_create(self):
        try:
            global all_connections

            global SERVER_IP
            global PORT_NUMBER
            global server_socket
            # SERVER_IP = ''
            # PORT_NUMBER = 9998 # 9999
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            all_connections.append(server_socket) # ??????????????????????????????????????????????
        except socket.error as msg:
            print("Socket creation error: " + str(msg))

    def bind_socket(self):
        try:
            global SERVER_IP
            global PORT_NUMBER
            global server_socket
            server_socket.bind((SERVER_IP, PORT_NUMBER))
            server_socket.listen(5)
        except socket.error as msg:
            print("Socket binding error: " + str(msg))
            time.sleep(5)
            self.bind_socket()

    # A function to accept multiple connections and save to a list:
    def accept_client_connection(self):
        global all_connections
        global all_addresses
        # while True:
        #     # accept a bunch of connections and whenever another client
        #     # connects, we will add them to the lists:
        try:
            conn, addr = server_socket.accept()
            # conn.setblocking(1) # specify "no timeout"
            # add the connection object to the list of client connections:
            # self.all_connections.append(conn)
            all_connections.append(conn)
            # add the address of the newwly connected client to the address list:
            # self.all_addresses.append(addr)
            all_addresses.append(addr)
            # provide connection status info:
            print(f"\nConnection established with: {addr[0]} on port: {addr[1]}")
        except:
            print("\nConnection error: could not connect client!")

    # the nexd job for a thread to do in the queue:
    # (one handles connections, the other sends comands)
    # def thread_task(self): # pass in connection and address for client_handler() here too # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def thread_task(self, connection, address): # pass in connection and address for client_handler() here too # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        while True:
            task = self.task_queue.get()
            # if the first job then handle the connection:
            if task == 1:
                self.socket_create()
                self.bind_socket()
                self.accept_client_connection()
            # if the second job then deal with the commands for the remote clients:
            if task == 2:
                # self.client_handler(self.all_connections[thr], self.all_addresses[thr])
                self.client_handler(connection, address)
            self.task_queue.task_done()

    # THE THREADDING:
    # creating the "worker" theads - only need 2:
    def create_worker_threads(self):
        # self.accept_client_connection()
        global all_connections
        global all_addresses

        # try:
        #     conn, addr = server_socket.accept()
        #     # conn.setblocking(1) # specify "no timeout"
        #     # add the connection object to the list of client connections:
        #     # self.all_connections.append(conn)
        #     all_connections.append(conn)
        #     # add the address of the newwly connected client to the address list:
        #     # self.all_addresses.append(addr)
        #     all_addresses.append(addr)
        #     # provide connection status info:
        #     print(f"\nConnection established with: {addr[0]} on port: {addr[1]}")
        # except:
        #     print("\nConnection error: could not connect client!")

        for i in range(self.number_of_threads-1):
            print(f"i: {i}")
            print(f"all_connections: {all_connections}")
            print("AYEEEEEEEEEEEEE!")

            connectionz = all_connections[i-1]
            print(f"connectionz: {connectionz}")
            # print(f"conn: {conn}")
            addrz = all_addresses[i-1]
            thread = threading.Thread(
                target = self.thread_task,
                # args = (self.all_connections[thr], self.all_addresses[thr]),
                args = (connectionz, addrz),
                daemon = True
            )
            thread.start()

    # each list element is a new job:
    def create_thread_tasks(self):
        # for thread_job in self.THREAD_JOB_NUMBER:
        for thread_job in THREAD_JOB_NUMBER:
            self.task_queue.put(thread_job)
        self.task_queue.join()

server = Server(SERVER_IP, PORT_NUMBER)
print("[STARTING] Starting the server...")

server.socket_create()
server.bind_socket()
server.accept_client_connection()

server.create_worker_threads()
server.create_thread_tasks()




# -------------------------------------------------------------------------------

    # def accept_socket_connection(self):
    #     connection, client_address = server_socket.accept()
    #     # add the connection object to the list of client connections:
    #     all_connections.append(connection)
    #     # add the address of the newwly connected client to the address list:
    #     all_addresses.append(client_address)
    #     # provide connection status info:
    #     print(f"\nConnection established with: {client_address[0]} on port: {client_address[1]}")
    #
    #
    # # the nexd job for a thread to do in the queue:
    # # (one handles connections, the other sends comands)
    # def thread_job():
    #     while True:
    #         task = self.task_queue.get() # added
    #         if task == 1:
    #         # if the first job then handle the connection:
    #             socket_create()
    #             bind_socket()
    #             accept_connection()
    #         # if the second job then deal with the commands for the remote clients:
    #         if task == 2:
    #             client_handler()
    #         queue.task_done()
    #
    # '''
    # A function to start the server.
    # Implements a thread pool to support multiple concurrent clients
    # on a single server
    #
    # Currently creates a new thread for each socket connection - see "Thread_For_Each_Connection.py"
    # '''
    # def start_server(self):
    #     # for i in range(self.number_of_threads):
    #     #     # create a thread:
    #     #     thread = threading.Thread(
    #     #           target = self.client_handler,
    #     #           args = (connection, client_address),
    #     #           daemon = True
    #     #     )
    #     #     thread.start()
    #     #     # add the thread to the thread pool:
    #     #     self.thread_pool.append(thread)
    #
    #     # create a TCP/IP socket
    #     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     # bind to the server address: SERVER_ADDR = (SERVER_IP, PORT_NUMBER)
    #     server_socket.bind((self.host, self.port))
    #     # listen on the socket:
    #     server_socket.listen(5)
    #     print('listening on {}'.format(server_socket.getsockname()))
    #
    #     while True:
    #       # connection = the client's own socket object
    #       # client_address = IP address of connecting client
    #       # connection, client_address = server_socket.accept()
    #       # # add the connection object to the list of client connections:
    #       # all_connections.append(connection)
    #       # # add the address of the newwly connected client to the address list:
    #       # all_addresses.append(client_address)
    #       # # provide connection status info:
    #       # print(f"\nConnection established with: {client_address[0]} on port: {client_address[1]}")
    #       self.accept_socket_connection()
    #
    #       # create the "worker" threads:
    #       for i in range(self.number_of_threads):
    #           # create a thread:
    #           thread = threading.Thread(
    #                 target = self.client_handler,
    #                 args = (connection, client_address),
    #                 daemon = True
    #           )
    #           thread.start()
    #           # add the thread to the thread pool:
    #           self.thread_pool.append(thread)
    #
    #       for thread in self.thread_pool:
    #           thread.join()
    #
    #       print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    #
    #       # put a thread on the queue:
    #       for task in THREAD_JOB_NUMBER:
    #           self.task_queue.put(task)
    #       self.task_queue.join()
    #
    #       # self.task_queue.put(
    #       #     (connection, "IS THIS WORKING????")
    #       # )
    #
    #       '''
    #
    #       HOW DOES THE TASK QUEUE WORK????
    #
    #       '''

    # -------------------------------------------------------------------------------------------------

    # print('listening on {}'.format(sock.getsockname()))

    # server_socket.listen(5)

    # while True:
    #   # handle each new connection independently
    #   connection, client_address = server_socket.accept()
    #   print('received connection from {}'.format(client_address))
    #   client_handler(connection, client_address)






    #     # server_socket.listen(5)
    #     # print('listening on {}'.format(sock.getsockname()))
    #
    #     # create a TCP/IP socket
    #     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #
    #     # bind to the server address: SERVER_ADDR = (SERVER_IP, PORT_NUMBER)
    #     server_socket.bind((self.host, self.port))
    #
    #     # listen on the socket:
    #     server_socket.listen(5)
    #     print('listening on {}'.format(server_socket.getsockname()))
    #
    #     while True:
    #       # connection = the client's own socket object
    #       # client_address = IP address of connecting client
    #       connection, client_address = server_socket.accept()
    #
    #       # create a thread:
    #       thread = threading.Thread(
    #             target = self.client_handler,
    #             args = (connection, client_address),
    #             daemon = True
    #       )
    #       thread.start()
    #       print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    #       print('received connection from {}'.format(client_address))
    #
    # # print('listening on {}'.format(sock.getsockname()))
    #
    # # server_socket.listen(5)
    #
    # # while True:
    # #   # handle each new connection independently
    # #   connection, client_address = server_socket.accept()
    # #   print('received connection from {}'.format(client_address))
    # #   client_handler(connection, client_address)

# server = Server(SERVER_IP, PORT_NUMBER)
# print("[STARTING] Starting the server...")
# server.start_server()
