# CITS3002 2021 Assignment
#
# This file implements a basic server that allows a single client to play a
# single game with no other participants, and very little error checking.
#
# Any other all_clients that connect during this time will need to wait for the
# first client's game to complete.
#
# Your task will be to write a new server that adds all connected all_clients into
# a pool of players. When enough players are available (two or more), the server
# will create a game with a random sample of those players (no more than
# tiles.PLAYER_LIMIT players will be in any one game). Players will take turns
# in an order determined by the server, continuing until the game is finished
# (there are less than two players remaining). When the game is finished, if
# there are enough players available the server will start a new game with a
# new selection of all_clients.

import socket
import sys
import tiles
import threading
import queue
import time
import select
import message


class Server:

    # def __init__(self, host_address, port_number):
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.turn_Queue = queue.Queue(maxsize = 4) # the queue for the players
        self.spectator_Queue = queue.Queue(maxsize = 1) # the queue of spectators

    '''
    Need functions to:

    * handle a client that just joined
    * track the turn of the client
    * start the game
    * check which client's turn it is at any given point
    * broardcast the messages to be sent to everyone
    * swap the next player's turn
    * handle the main game loop
    '''

    '''
    Adds all connected clients into a pool of players - the queue?
    '''
    def add_player_to_queue(self):
        pass

    '''
    * When enough players are available (two or more), the server
    will create a game with a random sample of those players (no more than
    tiles.PLAYER_LIMIT players will be in any one game).

    * Players will take turns in an order determined by the server,
    continuing until the game is finished (there are less than two players remaining).

    * When the game is finished, if there are enough players available the
    server will start a new game with a new selection of clients.
    '''
    def handle_joinned_client(self):
        global all_clients
        pass

    # send a message to all clients. if the client's connection is down, then the
    # sendall() might fail. don't worry too much about that here, we will detect
    # the severed connection later (when we next attempt to read from the
    # connection), and we can handle the disconnection there.
    def send_message_to_all_clients(msg):
        global all_clients
        msgbytes = msg.pack() # pack the message once
        for client in clients:
            try:
                client.connection.sendall(msgbytes)
            except Exception as e:
                print('exception sending message: {}'.format(e))

    # remove a client from the server (because they have disconnected)
    # we need to remove them from the global client list, and also remove their
    # connection from our list of connections-to-listen-to
    def remove_client(client):
        global all_clients, listening
        listening.remove(client.connection)
        all_clients.remove(client)

    # def client_handler(self, lock, connection, address):
    # this conection is the client connection?
    def client_handler(self, connection, address):
        global idnum
        global live_idnums
        global turn_Queue # get the idnum from the queue
        global all_clients

        # with lock:
        if len(all_clients) > 1:
            idnum = turn_Queue.get()
            # global turn_Queue
            host, port = address
            name = '{}:{}'.format(host, port)
            print(f"{name} has joined")

            # idnum = len(all_clients)
            all_clients.append([idnum, connection, address])

            if not live_idnums:
                live_idnums = [idnum]
                turn_Queue.queue.clear() # empty the queue just incase
                turn_Queue.put(idnum)
            else:
                live_idnums.append(idnum)
                turn_Queue.put(idnum)


            # idnum = 0
            # live_idnums = [idnum]

            # with lock:
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

            # Don't do the following unless >= 2 all_clients
            # if num_live_id_nums > 1:
            print("Now the game can START!")

            while True:
                chunk = connection.recv(4096)
                if not chunk:
                    print('client {} disconnected'.format(address))
                    return

                buffer.extend(chunk)

                # while True:
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

            # added:
            self.task_queue.task_done()
        else:
            print("Need one more client to start!")

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


class Client():
  """This class stores one client connection, the address of the client,
  and a buffer of bytes that we have received from the client but not yet
  processed.
  """
  def __init__(self, connection, address):
    self.connection = connection
    self.client_address = address
    self.message_queues = {} # a dictionary of message queues for all in all_clients
    self.buffer = bytearray()


# the turn queue for the "playing" players
# turn_Queue = queue.Queue(maxsize = 4)

# spectator_Queue = queue.Queue(maxsize = 1)
# message_queues = {} # a dictionary of message queues for all in all_clients

SERVER_IP = ''
PORT_NUMBER = 30020

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = Server()
server.server_socket.bind((SERVER_IP, PORT_NUMBER))
# server.server_socket.setblocking(False)
server.server_socket.listen(5)

# -------------------------------------------------------------------------------------------------------------

print('listening on {}'.format(server.server_socket.getsockname()))
# a list of all the connections that we want to listen to:
listening = [server.server_socket]
# a list of all the all_clients currently connected to our server
all_clients = []

all_idnums_on_the_turn_queue = []
all_idnums_on_the_spec_queue = []

idnum = 0
# live_idnums = [idnum]

print("ONE")
while True:
# while listening:
    # readable, writeable, exceptional = select.select(listening, all_clients, listening)
    print("TWO")
    readable, writeable, exceptional = select.select(listening, [], listening)
    print("THREE")
    # for all the sockets:
    # for socket in readable:
    # if socket in readable:
    if server.server_socket in readable:
        print("FOUR")
        # global server.server_socket
        # handle each new connection independently
        # connection, client_address = socket.accept() # connect the new client
        connection, client_address = server.server_socket.accept() # connect the new client
        print()
        print(f"client joined with address: {client_address}")
        print()
        print("FIVE")

        # all_clients.append([idnum, connection, client_address]) # add the client to the list of connected clients
        # could just put the client object on the queue ???????????????????????????????????????????????????????????????
        # remember we need to randomly select the players from a pool of player in the final version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if server.turn_Queue.qsize() < 4:
            server.turn_Queue.put(idnum) # put the newely connected client on the turn
            all_idnums_on_the_turn_queue.append(idnum)
            idnum += 1
        # elif server.spectator_Queue.size() < 1:
        if server.turn_Queue.size() == 4:
            # make all subequent connecting clients, spectators of the game:
            server.spectator_Queue.put(idnum)
            all_idnums_on_the_spec_queue.append(idnum)
            idnum += 1
        else:
            print("Sorry! that's all we can allow on the server i'm affraid!")
        print("SIX")

        # store the info of the "just-then-conected" client:
        client = Client(connection, client_address)
        all_clients.append(client)
        listening.append(client.connection)

        print("SEVEN")
        print()
        print(f"all idnums on turn_Queue:      {all_idnums_on_the_turn_queue}")
        print(f"all idnums on spectator_Queue: {all_idnums_on_the_spec_queue}\n")
        print()
        print("EIGHT")

        # if at least 2 clients then start the game

        disconnected_clients = []

        if client.connection in exceptional:
            print("NINE")
            print('client {} exception'.format(client.address))
            disconnected_clients.append(client)

        print("NINE AND A HALF")
        # elif client.connection in readable:
        if client.connection in readable:
            print("TEN")
            print("\n\nwe got to the creation of the thread!\n\n")
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # client_handler(client.connection, client.address) # create a thread for this?????
            # lock = threading.RLock()

            thread = threading.Thread(
                target = server.client_handler,
                # args = (lock, connection, client_address),
                args = (client.connection, client.address),
                daemon = True
            )
            thread.start()

            print("ELEVEN")

            # need this ???????????????????????????
            # thread.join()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # attempt to read a chunk of bytes from this client:
            try:
                print("TWELVE")
                byte_chunk = client.connection.recv(4069)
            except Exception:
                print("THIRTEEN")
                print('client {} recv exception, removing client'.format(client.address))
                disconnected_clients.append(client)
                continue # go to next client

            # if client message does not exist:
            print("FOURTEEN")
            if not byte_chunk:
                print("FIFTEEN")
                print('client {} closed connection'.format(client.address))
                disconnected_clients.append(client)
                continue # go to next client

            print("SIXTEEN")
            # add the bytes read from the client to the client's buffer:
            client.buffer.extend(chunk)

            # read as manny - complete - messages as possible, out of this client's
            # buffer:
            print("SEVENTEEN")
            while True:
                print("EIGHTEEN")
                message, consumed = message.Message.unpack(client.buffer)
                print("NINETEEN")
                if consumed:
                    print("TWENTY")
                    client.buffer = client.buffer[consumed:]

                    printmsg = '{}: {}'.format(client.address, msg.contents)
                    print(printmsg)

                    server.send_message_to_all_clients(message.Message(printmsg))
                else:
                    print("TWENTYONE")
                    break

        print("TWENTYTWO")
        # remove any disconnected clients
        for client in disconnected_clients:
            print("TWENTYTHREE")
            server.remove_client(client)






# VERSION 2:
# print('listening on {}'.format(server.server_socket.getsockname()))
# # a list of all the connections that we want to listen to:
# listening = [server.server_socket]
# # a list of all the all_clients currently connected to our server
# all_clients = []
#
# all_idnums_on_the_turn_queue = []
# all_idnums_on_the_spec_queue = []
#
# idnum = 0
# # live_idnums = [idnum]
#
# # print("ONE")
# while True:
# # while listening:
#     # readable, writeable, exceptional = select.select(listening, all_clients, listening)
#     # print("TWO")
#     readable, writeable, exceptional = select.select(listening, [], listening)
#     # print("THREE")
#     # for all the sockets:
#     # for socket in readable:
#     # if socket in readable:
#     # if server.server_socket in readable:
#     for server.server_socket in readable:
#         # print("FOUR")
#         # global server.server_socket
#         # handle each new connection independently
#         # connection, client_address = socket.accept() # connect the new client
#         connection, client_address = server.server_socket.accept() # connect the new client
#         print()
#         print(f"client joined with address: {client_address}")
#         # print("FIVE")
#
#         # all_clients.append([idnum, connection, client_address]) # add the client to the list of connected clients
#         if server.turn_Queue.qsize() < 4:
#             server.turn_Queue.put(idnum) # put the newely connected client on the turn
#             all_idnums_on_the_turn_queue.append(idnum)
#             idnum += 1
#         elif server.spectator_Queue.size() < 1:
#             # make all subequent connecting clients, spectators of the game:
#             server.spectator_Queue.put(idnum)
#             all_idnums_on_the_spec_queue.append(idnum)
#             idnum += 1
#         else:
#             print("Sorry! that's all we can allow on the server i'm affraid!")
#         # print("SIX")
#
#         # store the info of the "just-then-conected" client:
#         client = Client(connection, client_address)
#         all_clients.append(client)
#         listening.append(client.connection)
#         # print("SEVEN")
#
#         print(f"all idnums on turn_Queue:      {all_idnums_on_the_turn_queue}")
#         print(f"all idnums on spectator_Queue: {all_idnums_on_the_spec_queue}\n")
#         # print("\n\n")
#         # print("EIGHT")
#
#         # if at least 2 clients then start the game
#
#     disconnected_clients = []
#
#     for client in all_clients:
#         if client.connection in exceptional:
#           print('client {} exception'.format(client.address))
#           disconnected_clients.append(client)
#
#         elif client.connection in readable:
#             print("\n\nwe got to the creation of the thread!\n\n")
#             # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#             # client_handler(client.connection, client.address) # create a thread for this?????
#             # lock = threading.RLock()
#
#             thread = threading.Thread(
#                 target = server.client_handler,
#                 # args = (lock, connection, client_address),
#                 args = (client.connection, client.address),
#                 daemon = True
#             )
#             thread.start()
#
#             # need this ???????????????????????????
#             # thread.join()
#             # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#             # attempt to read a chunk of bytes from this client:
#             try:
#                 byte_chunk = client.connection.recv(4069)
#             except Exception:
#                 print('client {} recv exception, removing client'.format(client.address))
#                 disconnected_clients.append(client)
#                 continue # go to next client
#
#             # if client message does not exist:
#             if not byte_chunk:
#                 print('client {} closed connection'.format(client.address))
#                 disconnected_clients.append(client)
#                 continue # go to next client
#
#             # add the bytes read from the client to the client's buffer:
#             client.buffer.extend(chunk)
#
#             # read as manny - complete - messages as possible, out of this client's
#             # buffer:
#             while True:
#                 message, consumed = message.Message.unpack(client.buffer)
#                 if consumed:
#                     client.buffer = client.buffer[consumed:]
#
#                     printmsg = '{}: {}'.format(client.address, msg.contents)
#                     print(printmsg)
#
#                     server.send_message_to_all_clients(message.Message(printmsg))
#                 else:
#                     break
#
#     # remove any disconnected clients
#     for client in disconnected_clients:
#         server.remove_client(client)























# VERSION 1:

# idnum = 0
# # while True:
# while listening:
#     # readable, writeable, exceptional = select.select(listening, all_clients, listening)
#     # readable, writeable, exceptional = select.select(listening, all_clients, listening)
#     readable, writeable, exceptional = select.select(listening, [], listening)
#     # for all the sockets:
#     for thing in readable:
#         # if we find the server socket:
#         if thing is server.server_socket:
#             # global server.server_socket
#             # handle each new connection independently
#             connection, client_address = thing.accept() # connect the new client
#             # all_clients.append([idnum, connection, client_address]) # add the client to the list of connected clients
#             turn_Queue.put(idnum) # put the newely connected client on the turn
#             idnum += 1
#
#             # print('received connection from {}'.format(client_address))
#             # client_handler(connection, client_address)
#
#             lock = threading.RLock()
#
#             # what to make as the thread ?????????????????????????????????????????????
#             # thread = threading.Thread(
#             #     target = server.process_connection,
#             #     args = (lock, connection, client_address),
#             #     daemon = True
#             # )
#
#             thread = threading.Thread(
#                 target = server.client_handler,
#                 # args = (lock, connection, client_address),
#                 args = (connection, client_address),
#                 daemon = True
#             )
#             thread.start()
#
#             # need this ???????????????????????????
#             thread.join()
#
#             connection.setblocking(0) # do not block
#             listening.append(connection)
#             message_queues[connection] = queue.Queue()
#         else:
#             incomming_client_data = server.server_socket.recv(2048)
#             if incomming_client_data:
#                 message_queues[thing].put(incomming_client_data)
#                 if thing not in all_clients:
#                     all_clients.remove(thing)
#                 listening.remove(thing)
#                 server.server_socket.close()
#                 del message_queues[thing]
#
#     for thing in writeable:
#         try:
#             next_message = message_queues[thing].get_nowait() # .get(False)
#             # Queue.get(block=True, timeout=None)
#             # Remove and return an item from the queue. If optional args block is true and timeout is None (the default),
#             # block if necessary until an item is available. If timeout is a positive number, it blocks at most timeout
#             # seconds and raises the Empty exception if no item was available within that time. Otherwise (block is false),
#             # return an item if one is immediately available, else raise the Empty exception (timeout is ignored in that case).
#             # Prior to 3.0 on POSIX systems, and for all versions on Windows, if block is true and timeout is None, this
#             # operation goes into an uninterruptible wait on an underlying lock. This means that no exceptions can occur,
#             # and in particular a SIGINT will not trigger a KeyboardInterrupt.
#         except Queue.Empty:
#             all_clients.remove(thing)
#         else:
#             thing.send(next_message)
#
#     for thing in exceptional:
#         listening.remove(thing)
#         if thing in all_clients:
#             all_clients.remove(thing)
#         server.server_socket.close()
#         del message_queues[thing]
