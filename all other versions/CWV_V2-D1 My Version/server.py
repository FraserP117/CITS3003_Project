# CITS3002 2021 Assignment
#
# This file implements a basic server that allows a single client to play a
# single game with no other participants, and very little error checking.
#
# Any other self.all_connected_clients that connect during this time will need to wait for the
# first client's game to complete.
#
# Your task will be to write a new server that adds all connected self.all_connected_clients into
# a pool of players. When enough players are available (two or more), the server
# will create a game with a random sample of those players (no more than
# tiles.PLAYER_LIMIT players will be in any one game). Players will take turns
# in an order determined by the server, continuing until the game is finished
# (there are less than two players remaining). When the game is finished, if
# there are enough players available the server will start a new game with a
# new selection of self.all_connected_clients.

# CWV Mine 15/04/21 12:18 pm
# MOST CURRENT !

import socket
import sys
import tiles
import threading
import queue
import time
import select
import message
import random

# global idnum
# maybe

'''
* When enough players are available (two or more), the server
will create a game with a random sample of those players (no more than
tiles.PLAYER_LIMIT players will be in any one game).

* Players will take turns in an order determined by the server,
continuing until the game is finished (there are less than two players remaining).

* When the game is finished, if there are enough players available the
server will start a new game with a new selection of clients.
'''

class Client():
    """This class stores one client connection, the address of the client,
    and a buffer of bytes that we have received from the client but not yet
    processed.
    """
    def __init__(self, idnum, connection, address):
        self.idnum = idnum
        self.connection = connection
        self.client_address = address
        self.name = '{}:{}'.format(SERVER_IP, address)
        self.message_queues = {} # a dictionary of message queues for all in self.all_connected_clients
        self.buffer = bytearray()

# start = -1
class Server:

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening = [self.server_socket]
        self.game_started = False # game has not started by default
        self.turn_Queue = queue.Queue(maxsize = 4) # the queue for the players
        self.all_connected_clients = []
        self.current_players = []
        self.spectators = [] # the queue of spectators
        # self.board = tiles.Board()

    # # send a message to all clients. if the client's connection is down, then the
    # # sendall() might fail. don't worry too much about that here, we will detect
    # # the severed connection later (when we next attempt to read from the
    # # connection), and we can handle the disconnection there.
    # def send_message_to_all_connected_clients(self, msg):
    #     # global self.all_connected_clients
    #     msgbytes = msg.pack() # pack the message once
    #     for client in clients:
    #         try:
    #             client.connection.sendall(msgbytes)
    #         except Exception as e:
    #             print('exception sending message: {}'.format(e))

    # remove a client from the server (because they have disconnected)
    # we need to remove them from the global client list, and also remove their
    # connection from our list of connections-to-listen-to
    def remove_client(client):
        # global self.all_connected_clients
        # global listening
        self.listening.remove(client.connection)
        self.all_connected_clients.remove(client)

    '''
    Returns the list of idnums for all clients participating in gameplay.
    '''
    def select_Players_From_Connected_Clients(self):
        print("inside: select_Players_From_Connected_Clients")
        # global self.all_connected_clients
        # global self.current_players

        live_id_nums = []
        # self.current_players = []#just in case theres anything left in there

        # while (len(self.current_players)<4):
        while (len(self.current_players) <= tiles.IDNUM_LIMIT):
            player_choice = random.choice(self.all_connected_clients)
            if player_choice not in self.current_players:
                self.current_players.append(player_choice)
                live_id_nums.append(player_choice.idnum)
                # if(len(self.current_players)==len(self.all_connected_clients)):
                if(len(self.current_players) == tiles.PLAYER_LIMIT): # it's getting stuck in here! need 4 players!
                    break
        return live_id_nums

    # # this conection is the client connection?
    # def startTimer(self,now):
    #     # global started
    #     start = 5
    #     count = 0
    #     future = now + start
    #     #print("here")
    #     while time.time() < future:
    #         if time.time() > future - start + count:
    #             print("The game will start in: "+str(start - count))
    #             count = count + 1
    #     print("here")
    #     # started = 1
    #     self.game_started = True
    #     server.start_game()

    def threaded_start_game(self): # this goes in the thread
        # global live_id_nums
        start = 5
        print("maybe")

        while True:
            print("HELLO ??????????")
            board = tiles.Board()
            print("The GaMe Is ABoUT tO StARt!!!!!!!!!")
            #new players
            live_id_nums = self.select_Players_From_Connected_Clients()
            print("DID WE GET HERE ??????????")
            # self.game_started == True
            self.start_game(board)
            print("IS THE GAME STARTING ??????????")

    # def start_game(self):
    def start_game(self,board):
        # global self.all_connected_clients
        # global current_players
        # global started
        # global board

        # live_id_nums = self.select_Players_From_Connected_Clients()
        live_id_nums = []

        print("ONE")

        for i in self.current_players:
            print("TWO")
            # live_id_nums.append(i.idnum)
            live_id_nums.append(i.idnum)
            currentConnection = i.connection
            currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
            print("ONE")

            #step 4

            for _ in range(tiles.HAND_SIZE):
                print("THREE")
                tileid = tiles.get_random_tileid()
                currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())

            for j in self.all_connected_clients:
                print("FOUR")
                print(i.name)
                j.connection.send(tiles.MessagePlayerJoined(i.name,i.idnum).pack())

        # started = 1
        self.game_started = True
        #main game loop
        buffer = bytearray()
        print("A MEMEMEMEMEMEME")
        for i in live_id_nums:
            print(i)

        while len(live_id_nums)>1: #step 5
            print("start")
            current = self.turn_Queue.get()
            current_idnum = current.idnum
            print(current_idnum)
            current_connection = current.connection
            current_address = current.client_address
            for i in self.all_connected_clients:
                #step 5 a
                i.connection.send(tiles.MessagePlayerTurn(current_idnum).pack())
            #step 5 b
            chunk = current_connection.recv(4096)

            if not chunk:
                print('client {} disconnected'.format(address))
                return


            buffer.extend(chunk)

            #step 5 c
            msg, consumed = tiles.read_message_from_bytearray(buffer)
            if not consumed:
                break

            buffer = buffer[consumed:]

            print('received message {}'.format(msg))

            #step 5 c all
            #can probably combine
            if isinstance(msg, tiles.MessagePlaceTile):
                if board.set_tile(msg.x, msg.y, msg.tileid, msg.rotation, msg.idnum):
                    for i in self.all_connected_clients:
                        i.connection.send(msg.pack())
                    positionupdates, eliminated = board.do_player_movement(live_id_nums)

                    for msg in positionupdates:
                        for i in self.all_connected_clients:
                            i.connection.send(msg.pack())

                    for e in eliminated:
                        live_id_nums.remove(e)
                        print("liveid len is"+str(len(live_id_nums)))
                        for i in self.all_connected_clients:
                            i.connection.send(tiles.MessagePlayerEliminated(e).pack())
                        if e == current_idnum:
                            print("You lose!")
                            break
                            #return

#                     if current_idnum in eliminated:
#                         for i in self.all_connected_clients:
#                             i.connection.send(tiles.MessagePlayerEliminated(current_idnum).pack())
#                         live_id_nums.remove(current_idnum)
#                         #eliminated
#                         print("You lose!")
#                         return

                    tileid = tiles.get_random_tileid()
                    current_connection.send(tiles.MessageAddTileToHand(tileid).pack())

                self.turn_Queue.put(current)

            elif isinstance(msg, tiles.MessageMoveToken):
                if not board.have_player_position(msg.idnum):
                    if board.set_player_start_position(msg.idnum, msg.x, msg.y, msg.position):

                        positionupdates, eliminated = board.do_player_movement(live_id_nums)
                        for msg in positionupdates:
                            for i in self.all_connected_clients:
                                i.connection.send(msg.pack())
                        for e in eliminated:
                            live_id_nums.remove(e)
                            print("liveid len is"+str(len(live_id_nums)))
                            for i in self.all_connected_clients:
                                i.connection.send(tiles.MessagePlayerEliminated(e).pack())
                            if e == current_idnum:
                                print("You lose!")
                                break
                                #return

                    self.turn_Queue.put(current)

        print("End of start_game()")
        # server.restart()
        self.game_started == False
        return

    def restart(self):
        print("The game is over starting a new game in:")
        now = time.time()
        start = 5
        count = 0
        future = now + start
        while time.time() < future:
            if time.time() > future - start +count:
                print(start - count)
                count = count + 1

        # while (len(self.current_players)<4):
        while (len(self.current_players) <= 4):
            choice = random.choice(self.all_connected_clients)
            if choice not in self.current_players:
                self.current_players.append(choice)

                # why do we have this ??????????????????????????????????????????????????????????????????????
                # if(len(current_players)==len(self.all_connected_clients)):
                #     break

               #and not (len(self.all_connected_clients)==len(current_players)):
        #all_players_ids = [self.all_connected_clients]
        for i in self.all_connected_clients:
            print(i.idnum)


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
# listening = [server.server_socket]
# a list of all the self.all_connected_clients currently connected to our server
# self.all_connected_clients = []
# current_players = []
now = -1
all_idnums_on_the_turn_queue = []
all_idnums_on_the_spec_queue = []

idnum = 0

live_idnums = {}
# live_idnums = []
# board = tiles.Board()

while True:

    readable, writeable, exceptional = select.select(server.listening, [], server.listening)

    # global server
    # global self.all_connected_clients
    # global idnum
    # global listening # added
    # global started

    if server.server_socket in readable:
        # if len(server.all_connected_clients) < 2:
        #     print("Nice! you won't be able to start a game untill at least one other player joins.")
        # if len(server.all_connected_clients) <= 5:

        connection, client_address = server.server_socket.accept() # connect the new client
        # socket
        # store the info of the "just-then-conected" client:
        host, port = client_address
        name = '{}:{}'.format(host, port)
        client = Client(idnum, connection, client_address)
        server.all_connected_clients.append(client)

        # # if (server.game_started == -1 and len(server.all_connected_clients) > 1):
        # if (server.game_started == False and len(server.all_connected_clients) > 1):
        #     server.game_started = True

        if(server.game_started == False and len(server.all_connected_clients) > 1):
                # print("started has been changed")
                print("starting the game now")

                # server.game_started == True
                thread = threading.Thread(
                    #target = server.cew,#server.client_handler,
                    target = server.threaded_start_game,
                    daemon = True
                )
                thread.start()

        server.listening.append(client.connection)

        # the second player is being put onto the spectator queue instead of the player queue - need to fix this!
        # if server.turn_Queue.qsize() < 4 or server.game_started == False:
        if server.turn_Queue.qsize() < 4 and server.game_started == False:
            server.turn_Queue.put(client) # put the newely connected client on the turn
            all_idnums_on_the_turn_queue.append(idnum)
            server.current_players.append(client)
            live_idnums.update({idnum:client})

        # elif server.turn_Queue.qsize() == 4 or server.game_started == True:
        elif server.turn_Queue.qsize() == 4 and server.game_started == True:
            # make all subequent connecting clients, spectators of the game:
            server.spectators.append(idnum)
            all_idnums_on_the_spec_queue.append(idnum)
        else:
            print("Sorry! that's all we can allow on the server i'm affraid!")

        if idnum <= tiles.IDNUM_LIMIT:
            idnum += 1
        else:
            print("OH NO!")

        print()
        print(f"Client joined at: {client_address}")
        print(f"all the currently connected clients: {[c.idnum for c in server.all_connected_clients]}")
        print(f"the turn_Queue.qsize(): {server.turn_Queue.qsize()}")
        print(f"all idnums on turn_Queue:      {all_idnums_on_the_turn_queue}")
        print(f"all idnums on spectator_Queue: {all_idnums_on_the_spec_queue}\n")
        print()

        # if at least 2 clients then start the game

        disconnected_clients = []

        if client.connection in exceptional:
            print('client {} exception'.format(client.address))
            disconnected_clients.append(client)

        # else:
        #     print("Sorry! that's all we can allow on the server i'm affraid!")


    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # NOW WE PLAY THE GAME!!!
    # write the functions to implement the game logic

    '''
    3. track the turn of the client
    4. start the game
    5. check which client's turn it is at any given point
    6. broardcast the messages to be sent to everyone
    7. swap the next player's turn
    8. handle the main game loop
    '''



'''
listening:
a list of all the connections that we want to listen to:

self.all_connected_clients = []:
a list of all the self.all_connected_clients currently connected to our server
self.all_connected_clients = []

current_players = []:
a list of all the current players in the game - those players which "participate" in gameplay

now = -1
A time value for now

all_idnums_on_the_turn_queue = []
all_idnums_on_the_spec_queue = []
Lists to show what is on each respective queue

idnum = 0
the "identification number" of a certain client

live_idnums = {}
a dictionary contaiing the idnum for a certain client where the
idnum is of those clients in current_players

board = tiles.Board()
the board object for the game
'''

'''
Need functions to:

1. handle a client that just joined
3. track the turn of the client
4. start the game
5. check which client's turn it is at any given point
6. broardcast the messages to be sent to everyone
7. swap the next player's turn
8. handle the main game loop
'''








    # if self.server_socket in readable:
    #     if len(self.all_connected_clients) == 1:
    #         print("Nice! Now you just have to wait for one more player to join for the game to start!!!!!")
    #
    #     connection, client_address = self.server_socket.accept() # connect the new client
    #
    #     # store the info of the "just-then-conected" client:
    #     host, port = client_address
    #     name = '{}:{}'.format(host, port)
    #     client = Client(idnum, connection, client_address)
    #     self.all_connected_clients.append(client)
    #
    #     # if (server.game_started == -1 and len(self.all_connected_clients) > 1):
    #     if (server.game_started == False and len(self.all_connected_clients) > 1):
    #         server.game_started = True
    #
    #     listening.append(client.connection)
    #
    #     # the second player is being put onto the spectator queue instead of the player queue - need to fix this!
    #     if self.turn_Queue.qsize() < 4 or server.game_started == False:
    #         self.turn_Queue.put(client) # put the newely connected client on the turn
    #         all_idnums_on_the_turn_queue.append(idnum)
    #         current_players.append(client)
    #         live_idnums.update({idnum:client})
    #
    #     elif self.turn_Queue.qsize() == 4 or server.game_started == True:
    #         # make all subequent connecting clients, spectators of the game:
    #         self.spectators.append(idnum)
    #         all_idnums_on_the_spec_queue.append(idnum)
    #     else:
    #         print("Sorry! that's all we can allow on the server i'm affraid!")
    #
    #     # if self.turn_Queue.qsize() < 4 and server.game_started == False:
    #     #     self.turn_Queue.put(client) # put the newely connected client on the turn
    #     #     all_idnums_on_the_turn_queue.append(idnum)
    #     #     current_players.append(client)
    #     #     live_idnums.update({idnum:client})
    #     #
    #     # elif self.turn_Queue.qsize() == 4 or server.game_started == True:
    #     #     # make all subequent connecting clients, spectators of the game:
    #     #     self.spectators.append(idnum)
    #     #     all_idnums_on_the_spec_queue.append(idnum)
    #     # else:
    #     #     print("Sorry! that's all we can allow on the server i'm affraid!")
    #
    #     # print("SIX")
    #     idnum += 1
    #
    #     print()
    #     print(f"Client joined at: {client_address}")
    #     print(f"the turn_Queue.qsize(): {self.turn_Queue.qsize()}")
    #     print(f"all idnums on turn_Queue:      {all_idnums_on_the_turn_queue}")
    #     print(f"all idnums on spectator_Queue: {all_idnums_on_the_spec_queue}\n")
    #     print()
    #
    #     # if at least 2 clients then start the game
    #
    #     disconnected_clients = []
    #
    #     if client.connection in exceptional:
    #         print('client {} exception'.format(client.address))
    #         disconnected_clients.append(client)


















# while True:
#
#     readable, writeable, exceptional = select.select(listening, [], listening)
#
#     # if server.game_started == True:
#     # print("time")
#     # now = time.time()
#
#     # thread = threading.Thread(
#     #         target = server.startTimer,
#     #         args = (now, ),
#     #         #args = (now, ),#client.connection, client.client_address),
#     #         daemon = True
#     # )
#     # thread.start()
#
#     ''' job 1 '''
#     thread = threading.Thread(
#             target = server.handle_new_connection,
#             args = (readable, ),
#             daemon = True
#     )
#     thread.start()
#
#     # else:
#         # # if (server.game_started == -1 and len(self.all_connected_clients) > 1):
#         # if not (server.game_started == True and len(self.all_connected_clients) == 2):
#         #     server.game_started = 0
#         # server.handle_new_connection(readable)
#
#     # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     # NOW WE PLAY THE GAME!!!
#     '''
#     3. track the turn of the client
#     4. start the game
#     5. check which client's turn it is at any given point
#     6. broardcast the messages to be sent to everyone
#     7. swap the next player's turn
#     8. handle the main game loop
#     '''



    # # --------------------------------------------------------------------------------
    # # for all the sockets:
    # # for socket in readable:
    # # if socket in readable:
    # if server.server_socket in readable:
    #     print("FOUR")
    #     # global server.server_socket
    #     # handle each new connection independently
    #     # connection, client_address = socket.accept() # connect the new client
    #     connection, client_address = server.server_socket.accept() # connect the new client
    #     print()
    #     print(f"client joined with address: {client_address}")
    #     print()
    #     print("FIVE")
    #
    #     # self.all_connected_clients.append([idnum, connection, client_address]) # add the client to the list of connected clients
    #     # could just put the client object on the queue ???????????????????????????????????????????????????????????????
    #     # remember we need to randomly select the players from a pool of player in the final version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #     # store the info of the "just-then-conected" client:
    #     host, port = client_address
    #     name = '{}:{}'.format(host, port)
    #     client = Client(idnum, connection, client_address)
    #     self.all_connected_clients.append(client)
    #     listening.append(client.connection)
    #
    #     if server.turn_Queue.qsize() < 4 and started != 1:
    #         server.turn_Queue.put(client) # put the newely connected client on the turn
    #         all_idnums_on_the_turn_queue.append(idnum)
    #         current_players.append(client)
    #         live_idnums.update({idnum:client})
    #     elif server.turn_Queue.qsize() == 4 or started ==1:
    #         # make all subequent connecting clients, spectators of the game:
    #         server.spectators.append(idnum)
    #         all_idnums_on_the_spec_queue.append(idnum)
    #     else:
    #         print("Sorry! that's all we can allow on the server i'm affraid!")
    #     print("SIX")
    #
    #
    #     idnum += 1
    #     print("SEVEN")
    #     print()
    #     print(f"all idnums on turn_Queue:      {all_idnums_on_the_turn_queue}")
    #     print(f"all idnums on spectator_Queue: {all_idnums_on_the_spec_queue}\n")
    #     print()
    #     print("EIGHT")
    #
    #     # if at least 2 clients then start the game
    #
    #     disconnected_clients = []
    #
    #     if client.connection in exceptional:
    #         print("NINE")
    #         print('client {} exception'.format(client.address))
    #         disconnected_clients.append(client)
    #     #print(client.connection)
    #     print("NINE AND A HALF")

        #for i in listening:
        #    print(i)
        # elif client.connection in readable:
        #here
#         if client.connection in listening:
#             print("TEN")
#             print("\n\nwe got to the creation of the thread!\n\n")
#
#             #print(start)
#             #print(now)
#             print("we")
#             thread = threading.Thread(
#                 #target = server.cew,#server.client_handler,
#                 target = server.client_handler,
#                 args = (client.connection, client.client_address,now),
#                 #args = (now, ),#client.connection, client.client_address),
#                 daemon = True
#             )
#             thread.start()
        #here
        # print("ELEVEN")

            # need this ???????????????????????????
            # thread.join()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # attempt to read a chunk of bytes from this client:
#             try:
#                 print("TWELVE")
#                 byte_chunk = client.connection.recv(4069)
#             except Exception:
#                 print("THIRTEEN")
#                 print('client {} recv exception, removing client'.format(client.address))
#                 disconnected_clients.append(client)
#                 continue # go to next client

            # if client message does not exist:
#             print("FOURTEEN")
#             if not byte_chunk:
#                 print("FIFTEEN")
#                 print('client {} closed connection'.format(client.address))
#                 disconnected_clients.append(client)
#                 continue # go to next client
#
#             print("SIXTEEN")
            # add the bytes read from the client to the client's buffer:
            #client.buffer.extend(chunk)

            # read as manny - complete - messages as possible, out of this client's
            # buffer:
        # print("SEVENTEEN")
#             while True:
#                 print("EIGHTEEN")
#                 message, consumed = message.Message.unpack(client.buffer)
#                 print("NINETEEN")
#                 if consumed:
#                     print("TWENTY")
#                     client.buffer = client.buffer[consumed:]
#
#                     printmsg = '{}: {}'.format(client.address, msg.contents)
#                     print(printmsg)
#
#                     server.send_message_to_self.all_connected_clients(message.Message(printmsg))
#                 else:
#                     print("TWENTYONE")
#                     break

        # print("TWENTYTWO")
        # remove any disconnected clients
#         for client in disconnected_clients:
#             print("TWENTYTHREE")
#             server.remove_client(client)
