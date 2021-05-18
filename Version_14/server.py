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
import select

# class Server:
#
#     # def __init__(self, host_address, port_number):
#     def __init__(self):
#         # self.host = host_address
#         # self.port = port_number
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.number_of_threads = 2
        # self.number_of_threads = 0 # increment the number of threads each time we connect a new client
        # self.thread_pool = [] # just a list of threads "in the pool"
        # self.task_queue = queue.Queue()


    # def init_new_client(self, connection, address):
        # global clients
        # global listening
        # global live_client_idnums
        #
        # print("starting game!")
        #
        # host, port = address
        # name = '{}:{}'.format(host, port)
        # print(f"{name} has joined")
        # # idnum = len(clients)+1
        # client_idnum = len(clients)
        # clients.append([client_idnum, connection, address])
        #
        #
        # live_client_idnums.append(client_idnum)
        # connection.send(tiles.MessageWelcome(client_idnum).pack())
        # connection.send(tiles.MessagePlayerJoined(name, client_idnum).pack())

    # def client_handler(self, lock, connection, address):
    # def client_handler(self, connection, address):
    #     # global turn_Queue
    #     host, port = address
    #     name = '{}:{}'.format(host, port)
    #     print(f"{name} has joined")
    #
    #     idnum = 0
    #     live_idnums = [idnum]
    #
    #     connection.send(tiles.MessageWelcome(idnum).pack())
    #     connection.send(tiles.MessagePlayerJoined(name, idnum).pack())
    #     connection.send(tiles.MessageGameStart().pack())
    #     # get a client from the queue:
    #     # client_socket_id = turn_Queue.get() # is this now idnum???????????????????????????????????
    #
    #     for _ in range(tiles.HAND_SIZE):
    #         tileid = tiles.get_random_tileid()
    #         connection.send(tiles.MessageAddTileToHand(tileid).pack())
    #
    #     connection.send(tiles.MessagePlayerTurn(idnum).pack())
    #     board = tiles.Board()
    #     buffer = bytearray()
    #
    #     # Don't do the following unless >= 2 clients
    #     # if num_live_id_nums > 1:
    #     print("Now the game can START!")
    #
    #     while True:
    #         chunk = connection.recv(4096)
    #         if not chunk:
    #             print('client {} disconnected'.format(address))
    #             return
    #
    #         buffer.extend(chunk)
    #
    #         while True:
    #             # with lock:
    #             # connection, msg = self.task_queue.get() # added
    #             msg, consumed = tiles.read_message_from_bytearray(buffer)
    #             if not consumed:
    #               break
    #
    #             buffer = buffer[consumed:]
    #
    #             print('received message {}'.format(msg))
    #
    #             # sent by the player to put a tile onto the board (in all turns except
    #             # their second)
    #             if isinstance(msg, tiles.MessagePlaceTile):
    #                 if board.set_tile(msg.x, msg.y, msg.tileid, msg.rotation, msg.idnum):
    #                     # notify client that placement was successful
    #                     connection.send(msg.pack())
    #
    #                     # check for token movement
    #                     positionupdates, eliminated = board.do_player_movement(live_idnums)
    #
    #                     for msg in positionupdates:
    #                         connection.send(msg.pack())
    #
    #                     if idnum in eliminated:
    #                         connection.send(tiles.MessagePlayerEliminated(idnum).pack())
    #                         return
    #
    #                     # pickup a new tile
    #                     tileid = tiles.get_random_tileid()
    #                     connection.send(tiles.MessageAddTileToHand(tileid).pack())
    #
    #                     # start next turn
    #                     connection.send(tiles.MessagePlayerTurn(idnum).pack())
    #
    #             # sent by the player in the second turn, to choose their token's
    #             # starting path
    #             elif isinstance(msg, tiles.MessageMoveToken):
    #                 if not board.have_player_position(msg.idnum):
    #                     if board.set_player_start_position(msg.idnum, msg.x, msg.y, msg.position):
    #                         # check for token movement
    #                         positionupdates, eliminated = board.do_player_movement(live_idnums)
    #
    #                         for msg in positionupdates:
    #                             connection.send(msg.pack())
    #
    #                         if idnum in eliminated:
    #                             connection.send(tiles.MessagePlayerEliminated(idnum).pack())
    #                             return
    #
    #                         # start next turn
    #                         connection.send(tiles.MessagePlayerTurn(idnum).pack())
    #
    #             # # added:
    #             # self.task_queue.task_done()
    #         # else:
    #         #     print("Need one more client to start!")


    # # create a socket
    # def socket_create(self):
    #     try:
    #         # global all_connections
    #         global SERVER_IP
    #         global PORT_NUMBER
    #         global server_socket
    #         # SERVER_IP = ''
    #         # PORT_NUMBER = 9998 # 9999
    #         server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         # server_socket.setsocketopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #         print("Created the server socket\n")
    #
    #         # all_connections.append(server_socket) # ??????????????????????????????????????????????
    #     except socket.error as msg:
    #         print("Socket creation error: " + str(msg))

    # # this is supposed to bind incomming client's IP to the server port
    # # does not currently do that; currently binds the server socket to the server port ????
    # def bind_socket(self):
    #     try:
    #         global SERVER_IP
    #         global PORT_NUMBER
    #         global server_socket
    #         server_socket.bind((SERVER_IP, PORT_NUMBER))
    #         server_socket.listen(5)
    #         print('listening on {}'.format(server_socket.getsockname()))
    #     except socket.error as msg:
    #         print("Socket binding error: " + str(msg))
    #         time.sleep(5)
    #         self.bind_socket()
    #
    # # A function to accept multiple connections and save to a list:
    # def accept_client_connection(self):
    #     global all_connections
    #     global all_addresses
    #     # while True:
    #     #     # accept a bunch of connections and whenever another client
    #     #     # connects, we will add them to the lists:
    #     try:
    #         conn, addr = server_socket.accept()
    #         # conn.setblocking(1) # specify "no timeout"
    #         # add the connection object to the list of client connections:
    #         # self.all_connections.append(conn)
    #         all_connections.append(conn)
    #         # add the address of the newwly connected client to the address list:
    #         # self.all_addresses.append(addr)
    #         all_addresses.append(addr)
    #
    #         self.number_of_threads += 1
    #         # provide connection status info:
    #         print(f"\nConnection established with: {addr[0]} on port: {addr[1]}")
    #
    #         num_live_id_nums += 1
    #     except:
    #         print("\nConnection error: could not connect client!")
    #
    # # the nexd job for a thread to do in the queue:
    # # (one handles connections, the other sends comands)
    # # def thread_task(self): # pass in connection and address for client_handler() here too # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # # def thread_task(self, thread_lock, connection, address): # pass in connection and address for client_handler() here too # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # def thread_task(self, connection, address):
    #     while True:
    #         task = self.task_queue.get()
    #         # if the first job then handle the connection:
    #         if task == 1:
    #             # self.socket_create()
    #             # self.bind_socket()
    #             self.accept_client_connection()
    #         # if the second job then deal with the commands for the remote clients:
    #         if task == 2:
    #             # with thread_lock:
    #             # self.client_handler(self.all_connections[thr], self.all_addresses[thr])
    #             self.client_handler(connection, address)
    #         self.task_queue.task_done()
    #
    # def process_connection(self, lock, connection, address):
    #     global turn_Queue
    #     recieved_data = connection.recv(1024)
    #     if recieved_data:
    #         print("Adding a client to the game")
    #         connection.send(tiles.MessageWelcome(client_idnum).pack())
    #         connection.send(tiles.MessagePlayerJoined(name, client_idnum).pack())
    #
    #         # enqueue the address of the most recently connected client into the
    #         # turn queue:
    #         client_socket_id = (connection, address)
    #         turn_Queue.put(client_socket_id)
    #
    #         # HANDLE EM:
    #         with lock:
    #             client_handler(connection, address)

    # the nexd job for a thread to do in the queue:
    # (one handles connections, the other sends comands)
    # def thread_task(self): # pass in connection and address for client_handler() here too # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # def thread_task(self, thread_lock, connection, address): # pass in connection and address for client_handler() here too # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # def thread_task(self, connection, address):
    #     while True:
    #         task = self.task_queue.get()
    #         # if the first job then handle the connection:
    #         if task == 1:
    #             # self.socket_create()
    #             # self.bind_socket()
    #             self.accept_client_connection()
    #         # if the second job then deal with the commands for the remote clients:
    #         if task == 2:
    #             # with thread_lock:
    #             # self.client_handler(self.all_connections[thr], self.all_addresses[thr])
    #             self.client_handler(connection, address)
    #         self.task_queue.task_done()

    # def process_connection(self, lock, connection, address):
    #     global turn_Queue
    #     recieved_data = connection.recv(1024)
    #     if recieved_data:
    #         print("Adding a client to the game")
    #         connection.send(tiles.MessageWelcome(client_idnum).pack())
    #         connection.send(tiles.MessagePlayerJoined(name, client_idnum).pack())
    #
    #         # enqueue the address of the most recently connected client into the
    #         # turn queue:
    #         client_socket_id = (connection, address)
    #         turn_Queue.put(client_socket_id)
    #
    #         # HANDLE EM:
    #         with lock:
    #             client_handler(connection, address)

        # incomming_client_data = server_socket.recv(2048)
        # if incomming_client_data:
        #     message_queues[thing].put(incomming_client_data)
        #     if thing not in clients:
        #         clients.remove(thing)
        #     listening.remove(thing)
        #     server_socket.close()
        #     del message_queues[thing]


class Server:

    # def __init__(self, host_address, port_number):
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def client_handler(self, lock, connection, address):
    # def client_handler(self, connection, address):
        # global turn_Queue
        host, port = address
        name = '{}:{}'.format(host, port)
        print(f"{name} has joined")

        idnum = 0
        live_idnums = [idnum]

        with lock:
            connection.send(tiles.MessageWelcome(idnum).pack())
            connection.send(tiles.MessagePlayerJoined(name, idnum).pack())
            connection.send(tiles.MessageGameStart().pack())

            # get a client from the queue:
            # client_socket_id = turn_Queue.get() # is this now idnum???????????????????????????????????

            for _ in range(tiles.HAND_SIZE):
                tileid = tiles.get_random_tileid()
                connection.send(tiles.MessageAddTileToHand(tileid).pack())

            connection.send(tiles.MessagePlayerTurn(idnum).pack())
            board = tiles.Board()
            buffer = bytearray()

            # Don't do the following unless >= 2 clients
            # if num_live_id_nums > 1:
            print("Now the game can START!")

            while True:
                chunk = connection.recv(4096)
                if not chunk:
                    print('client {} disconnected'.format(address))
                    return

                buffer.extend(chunk)

                while True:
                    # with lock:
                    # connection, msg = self.task_queue.get() # added
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
                # else:
                #     print("Need one more client to start!")

    def process_connection(self, lock, connection, address):
        global turn_Queue
        recieved_data = connection.recv(1024)
        if recieved_data:
            print("Adding a client to the game")
            connection.send(tiles.MessageWelcome(client_idnum).pack())
            connection.send(tiles.MessagePlayerJoined(name, client_idnum).pack())

            # enqueue the address of the most recently connected client into the
            # turn queue:
            client_socket_id = (connection, address)
            turn_Queue.put(client_socket_id)

            # HANDLE EM:
            with lock:
                client_handler(connection, address)


# client_handler
all_connections = [] # a list of client "connection objects"
all_addresses = []   # a list of all client "addresses"
THREAD_JOB_NUMBER = [1, 2]
live_client_idnums = []
num_live_id_nums = 1
turn_Queue = queue.Queue(maxsize = 4) # turns for the player
message_queues = {} # a dictionary of message queues for all clients

SERVER_IP = ''
PORT_NUMBER = 30020

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = Server()
server.server_socket.bind((SERVER_IP, PORT_NUMBER))
server.server_socket.listen(5)

# -------------------------------------------------------------------------------------------------------------

print('listening on {}'.format(server.server_socket.getsockname()))

# a list of all the clients currently connected to our server
clients = []
# a list of all the connections that we want to listen to:
# - first sock, which will tell us about new incoming client connections
# - later we will also add the client connections, so that we can read their
#   messages
listening = [server.server_socket]

# while True:
while listening:
    readable, writeable, exceptional = select.select(listening, clients, listening)
    # for all the sockets:
    for thing in readable:
        # if we find the server socket:
        if thing is server.server_socket:
            # global server.server_socket
            # handle each new connection independently
            connection, client_address = server.server_socket.accept()

            print('received connection from {}'.format(client_address))
            # client_handler(connection, client_address)

            lock = threading.RLock()

            # what to make as the thread ?????????????????????????????????????????????
            # thread = threading.Thread(
            #     target = server.process_connection,
            #     args = (lock, connection, client_address),
            #     daemon = True
            # )

            thread = threading.Thread(
                target = server.client_handler,
                args = (lock, connection, client_address),
                # args = (connection, client_address),
                daemon = True
            )
            thread.start()

            # need this ???????????????????????????
            thread.join()

            connection.setblocking(0) # do not block
            listening.append(connection)
            message_queues[connection] = queue.Queue()
        else:
            incomming_client_data = server.server_socket.recv(2048)
            if incomming_client_data:
                message_queues[thing].put(incomming_client_data)
                if thing not in clients:
                    clients.remove(thing)
                listening.remove(thing)
                server.server_socket.close()
                del message_queues[thing]

    for thing in writeable:
        try:
            next_message = message_queues[thing].get_nowait() # .get(False)
            # Queue.get(block=True, timeout=None)
            # Remove and return an item from the queue. If optional args block is true and timeout is None (the default),
            # block if necessary until an item is available. If timeout is a positive number, it blocks at most timeout
            # seconds and raises the Empty exception if no item was available within that time. Otherwise (block is false),
            # return an item if one is immediately available, else raise the Empty exception (timeout is ignored in that case).
            # Prior to 3.0 on POSIX systems, and for all versions on Windows, if block is true and timeout is None, this
            # operation goes into an uninterruptible wait on an underlying lock. This means that no exceptions can occur,
            # and in particular a SIGINT will not trigger a KeyboardInterrupt.
        except Queue.Empty:
            clients.remove(thing)
        else:
            thing.send(next_message)

    for thing in exceptional:
        listening.remove(thing)
        if thing in clients:
            clients.remove(thing)
        server.server_socket.close()
        del message_queues[thing]
