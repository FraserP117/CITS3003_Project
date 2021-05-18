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




# CWV Mine 16/04/ 2:23
# VERSION 1




'''
Program Flow/Requirements
For sake of simplicity we specify the flow of a single game below.

1. A selection of at most four players is chosen from all connected clients.
2. A random turn order for the four players is also determined.
3. Each client is notified that a new game is starting.
4. Each player is provided tiles to fill their starting hand.
5. While more than one player is alive:
    a. Notify all clients whose turn it is
    b. Wait for the current player to make a valid move
    c. Process the results of the move
        i. Notify all clients of new tile placements
        ii. Notify all clients of new token positions
        iii. Notify all clients of any eliminated players
        iv. If there are less than two players remaining, exit the loop
6. If the current player played a tile, send them a new tile
7. Switch to the next (remaining) player's turn

When a game is completed, the server should start a new game if there are enough clients available.
Otherwise it should wait for more clients to join.
'''


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
# CLEAN VERSION - SEE OG BELOW
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

        self.MAX_CLIENTS = 3 # 5
        self.MAX_PLAYERS = 2 # 4
        self.MAX_SPECTATORS = 1 # 1

        self.game_message_history = []
        self.disconnected_clients = []

        # self.board = tiles.Board()
        # live_idnums


    # remove a client from the server (because they have disconnected)
    # we need to remove them from the global client list, and also remove their
    # connection from our list of connections-to-listen-to
    def remove_client(client):
        # global self.all_connected_clients
        # global listening
        self.listening.remove(client.connection)
        self.all_connected_clients.remove(client)


    # '''
    # Returns the list of idnums for all clients participating in gameplay.
    # '''
    # def select_Players_From_Connected_Clients(self):
    #     # global idnum
    #
    #     live_id_nums = []
    #     # while (len(self.current_players) < 2):
    #     print("----------------- ONE -----------------")
    #     if (len(self.current_players) < self.MAX_PLAYERS):
    #     # while (len(self.current_players) < self.MAX_PLAYERS):
    #         player_choice = random.choice(self.all_connected_clients) # self.all_connected_clients is empty !!!!!!!!!
    #
    #         if player_choice not in self.current_players:
    #             print("----------------- FOUR -----------------")
    #             self.current_players.append(player_choice) # added
    #             print("----------------- FIVE -----------------")
    #             live_id_nums.append(player_choice.idnum)
    #             print("----------------- SIX -----------------")
    #
    #         if server.turn_Queue.qsize() < self.MAX_PLAYERS: # or server.game_started == False:
    #             print("----------------- SEVEN -----------------")
    #         # if self.turn_Queue.qsize() < 4 and self.game_started == False:
    #             self.turn_Queue.put(player_choice) # put the newely connected client on the turn
    #             print("----------------- EIGHT -----------------")
    #             all_idnums_on_the_turn_queue.append(idnum)
    #             print("----------------- NINE -----------------")
    #
    #     print("----------------- TEN -----------------")
    #     return live_id_nums


    '''
    Returns the list of idnums for all clients participating in gameplay.
    '''
    def select_Players_From_Connected_Clients(self):
        # global idnum
        live_id_nums = []
        # while (len(self.current_players) < 2):
        # print("----------------- ONE -----------------")
        # while (len(self.current_players) < self.MAX_PLAYERS):
        if (len(self.current_players) < self.MAX_PLAYERS):
            player_choice = random.choice(self.all_connected_clients) # self.all_connected_clients is empty !!!!!!!!!
            print("----------------- ONE -----------------")
            print(f"----------------- self.current_players: {self.current_players} ----------------- ")
            print(f"----------------- len(self.current_players): {len(self.current_players)} ----------------- ")
            print(f"-----------------")
            print(f"----------------- self.MAX_PLAYERS: {self.MAX_PLAYERS} ----------------- ")

            print(f"----------------- player_choice.idnum: {player_choice.idnum} ----------------- ")
            print(f"----------------- self.current_players.idnum: {[s.idnum for s in self.current_players]} ----------------- ")
            print(f"----------------- len(self.current_players): {len(self.current_players)} ----------------- ")
            print(f"----------------- self.all_connected_clients.idnum: {[c.idnum for c in self.all_connected_clients]} ----------------- ")
            print(f"----------------- self.all_connected_clients: {self.all_connected_clients} ----------------- ")
            print(f"----------------- len(self.all_connected_clients): {len(self.all_connected_clients)} ----------------- ")

            if player_choice not in self.current_players:
                # print("----------------- FOUR -----------------")
                self.current_players.append(player_choice) # added
                # print("----------------- FIVE -----------------")
                live_id_nums.append(player_choice.idnum)
                # print("----------------- SIX -----------------")

                print("----------------- TWO -----------------")
                print(f"----------------- self.current_players: {self.current_players} ----------------- ")
                print(f"----------------- len(self.current_players): {len(self.current_players)} ----------------- ")
                print(f"-----------------")
                print(f"----------------- self.MAX_PLAYERS: {self.MAX_PLAYERS} ----------------- ")

                print(f"----------------- player_choice.idnum: {player_choice.idnum} ----------------- ")
                print(f"----------------- self.current_players.idnum: {[s.idnum for s in self.current_players]} ----------------- ")
                print(f"----------------- len(self.current_players): {len(self.current_players)} ----------------- ")
                print(f"----------------- self.all_connected_clients.idnum: {[c.idnum for c in self.all_connected_clients]} ----------------- ")
                print(f"----------------- self.all_connected_clients: {self.all_connected_clients} ----------------- ")
                print(f"----------------- len(self.all_connected_clients): {len(self.all_connected_clients)} ----------------- ")

            if server.turn_Queue.qsize() < self.MAX_PLAYERS: # or server.game_started == False:
                # print("----------------- SEVEN -----------------")
            # if self.turn_Queue.qsize() < 4 and self.game_started == False:
                self.turn_Queue.put(player_choice) # put the newely connected client on the turn
                # print("----------------- EIGHT -----------------")
                all_idnums_on_the_turn_queue.append(idnum)
                # print("----------------- NINE -----------------")

        print("----------------- TEN -----------------")
        return live_id_nums


    # def select_Spectators_From_Connected_Clients(self, live_id_nums):
    #
    #     spectator_id_nums = []
    #
    #     # select the spectator clients
    #     # select the spectator clients
    #     for a_connected_client in self.all_connected_clients:
    #         if a_connected_client.idnum not in live_id_nums:
    #             self.spectators.append(a_connected_client.idnum)
    #
    #     return spectator_id_nums


    def resetState(self):
        print("reset")
        for one_client in self.all_connected_clients:
            #
            one_client.connection.send(tiles.MessageGameStart().pack())
            #currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
            #currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())
            #
        print("reset")
        #return board.reset()


    # def start_game(self):
    def start_game(self, board, live_id_nums):  # take in live_id_nums ????????????????????????????????????????????????????????????????????????
    #  start_game(self, board):  # take in live_id_nums ????????????????????????????????????????????????????????????????????????


        # live_id_nums = []
        # live_id_nums = server.select_Players_From_Connected_Clients()
        print("sending Welcome messgae to all players")
        print("Adding tiles to each player's hand")
        for i in self.current_players:
            print("----------------------------------------------- HERE 1 ??? ----------------------------------------------- ")
            # live_id_nums.append(i.idnum)
            currentConnection = i.connection
            print("----------------------------------------------- HERE 2 ??? ----------------------------------------------- ")
            currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
            print("----------------------------------------------- HERE 3 ??? ----------------------------------------------- ")
            currentConnection.send(tiles.MessageGameStart().pack())

            #step 4

            for _ in range(tiles.HAND_SIZE):
                print("----------------------------------------------- HERE 4 ??? ----------------------------------------------- ")
                # print("THREE")
                tileid = tiles.get_random_tileid()
                print("----------------------------------------------- HERE 5 ??? ----------------------------------------------- ")
                currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())

            for j in self.all_connected_clients:
                print("----------------------------------------------- HERE 6 ??? ----------------------------------------------- ")
                print("FOUR")
                print(i.name)
                j.connection.send(tiles.MessagePlayerJoined(i.name, i.idnum).pack())

        # for j in self.spectators:
        #     print("FOUR")
        #     print(i.name)
        #     j.connection.send(tiles.MessagePlayerJoined(i.name, i.idnum).pack())

        # started = 1
        self.game_started = True
        #main game loop
        buffer = bytearray()

        while len(live_id_nums) > 1: #step 5
            # print("start")
            current = self.turn_Queue.get()
            current_idnum = current.idnum
            # print(current_idnum)
            current_connection = current.connection
            current_address = current.client_address
            for i in self.all_connected_clients:
                #step 5 a
                i.connection.send(tiles.MessagePlayerTurn(current_idnum).pack())
            #step 5 b
            chunk = current_connection.recv(4096)

            if not chunk:
                print('client {} disconnected'.format(current_address))
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

                self.game_message_history.append(msg)

                if board.set_tile(msg.x, msg.y, msg.tileid, msg.rotation, msg.idnum):
                    for i in self.all_connected_clients:
                        i.connection.send(msg.pack())
                    positionupdates, eliminated = board.do_player_movement(live_id_nums)

                    for msg in positionupdates:

                        self.game_message_history.append(msg)

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
                            #return # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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


    # OG
    # # def start_game(self):
    # def start_game(self, board):  # take in live_id_nums ????????????????????????????????????????????????????????????????????????
    #     # global live_id_nums
    #     # global game_message_history
    #     # global self.all_connected_clients
    #     # global current_players
    #     # global started
    #     # global board
    #
    #     # have access to these
    #     # live_id_nums = self.select_Players_From_Connected_Clients()
    #     # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
    #
    #     # live_id_nums = self.select_Players_From_Connected_Clients()
    #     live_id_nums = []
    #     # live_id_nums = server.select_Players_From_Connected_Clients()
    #     print("sending Welcome messgae to all players")
    #     print("Adding tiles to each player's hand")
    #     for i in self.current_players:
    #         live_id_nums.append(i.idnum)
    #         currentConnection = i.connection
    #         currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
    #         currentConnection.send(tiles.MessageGameStart().pack())
    #
    #         #step 4
    #
    #         for _ in range(tiles.HAND_SIZE):
    #             # print("THREE")
    #             tileid = tiles.get_random_tileid()
    #             currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())
    #
    #         for j in self.all_connected_clients:
    #             print("FOUR")
    #             print(i.name)
    #             j.connection.send(tiles.MessagePlayerJoined(i.name, i.idnum).pack())
    #
    #     # for j in self.spectators:
    #     #     print("FOUR")
    #     #     print(i.name)
    #     #     j.connection.send(tiles.MessagePlayerJoined(i.name, i.idnum).pack())
    #
    #     # started = 1
    #     self.game_started = True
    #     #main game loop
    #     buffer = bytearray()
    #
    #     while len(live_id_nums) > 1: #step 5
    #         # print("start")
    #         current = self.turn_Queue.get()
    #         current_idnum = current.idnum
    #         # print(current_idnum)
    #         current_connection = current.connection
    #         current_address = current.client_address
    #         for i in self.all_connected_clients:
    #             #step 5 a
    #             i.connection.send(tiles.MessagePlayerTurn(current_idnum).pack())
    #         #step 5 b
    #         chunk = current_connection.recv(4096)
    #
    #         if not chunk:
    #             print('client {} disconnected'.format(current_address))
    #             return
    #
    #
    #         buffer.extend(chunk)
    #
    #         #step 5 c
    #         msg, consumed = tiles.read_message_from_bytearray(buffer)
    #         if not consumed:
    #             break
    #
    #         buffer = buffer[consumed:]
    #
    #         print('received message {}'.format(msg))
    #
    #         #step 5 c all
    #         #can probably combine
    #         if isinstance(msg, tiles.MessagePlaceTile):
    #
    #             self.game_message_history.append(msg)
    #
    #             if board.set_tile(msg.x, msg.y, msg.tileid, msg.rotation, msg.idnum):
    #                 for i in self.all_connected_clients:
    #                     i.connection.send(msg.pack())
    #                 positionupdates, eliminated = board.do_player_movement(live_id_nums)
    #
    #                 for msg in positionupdates:
    #
    #                     self.game_message_history.append(msg)
    #
    #                     for i in self.all_connected_clients:
    #                         i.connection.send(msg.pack())
    #
    #                 for e in eliminated:
    #                     live_id_nums.remove(e)
    #                     print("liveid len is"+str(len(live_id_nums)))
    #                     for i in self.all_connected_clients:
    #                         i.connection.send(tiles.MessagePlayerEliminated(e).pack())
    #                     if e == current_idnum:
    #                         print("You lose!")
    #                         break
    #                         #return # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    # #                     if current_idnum in eliminated:
    # #                         for i in self.all_connected_clients:
    # #                             i.connection.send(tiles.MessagePlayerEliminated(current_idnum).pack())
    # #                         live_id_nums.remove(current_idnum)
    # #                         #eliminated
    # #                         print("You lose!")
    # #                         return
    #
    #                 tileid = tiles.get_random_tileid()
    #                 current_connection.send(tiles.MessageAddTileToHand(tileid).pack())
    #
    #             self.turn_Queue.put(current)
    #
    #         elif isinstance(msg, tiles.MessageMoveToken):
    #             if not board.have_player_position(msg.idnum):
    #                 if board.set_player_start_position(msg.idnum, msg.x, msg.y, msg.position):
    #
    #                     positionupdates, eliminated = board.do_player_movement(live_id_nums)
    #                     for msg in positionupdates:
    #                         for i in self.all_connected_clients:
    #                             i.connection.send(msg.pack())
    #                     for e in eliminated:
    #                         live_id_nums.remove(e)
    #                         print("liveid len is"+str(len(live_id_nums)))
    #                         for i in self.all_connected_clients:
    #                             i.connection.send(tiles.MessagePlayerEliminated(e).pack())
    #                         if e == current_idnum:
    #                             print("You lose!")
    #                             break
    #                             #return
    #
    #                 self.turn_Queue.put(current)
    #
    #     print("End of start_game()")
    #     # server.restart()
    #     self.game_started == False
    #     return

    # def handle_late_spectator(self, client):
    #
    #     currentIdnum = client.idnum
    #     currentCon = client.connection
    #     currentCon.send(tiles.MessageWelcome(currentIdnum).pack())
    #     for i in current_players:
    #         currentCon.send(tiles.MessagePlayerJoined(i.name,i.idnum).pack())
    #         currentCon.send(tiles.MessagePlayerTurn(i.idnum).pack())
    #
    #     for move in self.game_message_history:
    #         currentCon.send(move.pack())
#         for j in all_clients:
#             print("idnum is "+str(j.idnum))
#             currentCon.send(tiles.MessagePlayerJoined(j.name,j.idnum).pack())#dont need to send back
#         print("current plyares")
#
#
#         for k in current_players:#this has to be backwards for order lmao idk why
#         #for k in reversed(current_players):#this has to be backwards for order lmao idk why
#             print(k.client_address)
#             currentCon.send(tiles.MessagePlayerTurn(k.idnum).pack())
            #currentCon.connection.send(tiles.MessagePlayerJoined(i.name,i.idnum).pack())
#         print("current plyares")
#         board = tiles.Board()
#         #currentCon.connection.send(

#         print(len(moves))




#         tempQueue = queue.Queue()
#         while
#         tempQueue = self.movesQueue
#         current = tempQueue.get()
#         print("nigod")
#         print(self.movesQueue.qsize())
#         print(tempQueue.qsize())
#         print(currentIdnum)
#         print("nigor")




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

        while (len(self.current_players)<4):
        # while (len(self.current_players) <= 4):
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

    # def handle_client_connection(self, socket):
    def handle_client_connection(self, readable, writeable, exceptional):
    # def handle_client_connection(self, lock, readable, writeable, exceptional):
        # with lock:
        global idnum
        # if self.turn_Queue.qsize() < self.MAX_PLAYERS and self.game_started == False:
        if len(self.all_connected_clients) < self.MAX_CLIENTS:
            print("ADDING CLIENT")
            connection, client_address = self.server_socket.accept() # connect the new client
            host, port = client_address
            name = '{}:{}'.format(host, port)
            client = Client(idnum, connection, client_address)
            self.all_connected_clients.append(client)
            self.listening.append(client.connection)
            print(f"----------------------------- self.all_connected_clients: {self.all_connected_clients} ----------------------------- ")
        else:
            print("Sorry! that's all the clients' we can connect i'm affraid!")

        if idnum <= tiles.IDNUM_LIMIT:
            idnum += 1
        else:
            print("OH NO!")

        print()
        print(f"Client joined with address: {client_address}")
        print(f"all the currently connected clients: {[c.idnum for c in self.all_connected_clients]}")
        print()

        if client.connection in exceptional:
            print('client {} exception'.format(client.address))
            self.disconnected_clients.append(client)


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
all_idnums_on_the_turn_queue = []
all_idnums_on_the_spec_queue = []

idnum = 0
# game_message_history = []

live_idnums = {}
# live_idnums = []
# board = tiles.Board()

while True:
    print("------------------------ DOING SELECT.SELECT ------------------------")
    readable, writeable, exceptional = select.select(server.listening, [], server.listening)

    # lock = threading.RLock()

    # continuiously connect clients to the server - until we reach the client limit:
    print("------------------------ CREATING A 'handle_client_connection()' THREAD ------------------------")

    # if (len(server.all_connected_clients) < server.MAX_CLIENTS + 1):
    if (len(server.all_connected_clients) < server.MAX_CLIENTS):
        thread = threading.Thread(
            #target = server.cew,#server.client_handler,
            target = server.handle_client_connection,
            args = (readable, writeable, exceptional),
            # args = (lock, readable, writeable, exceptional),
            daemon = True
        )
        thread.start()
    else:
        print("Sorry, that's all the clients the server can support!")


    print("------------------------ ALL CONNECTED CLIENTS ------------------------")
    print(server.all_connected_clients)

    # select the players from the current pool of connected clients
    print("------------------------ CREATE THE LIST OF LIVE_ID_NUMS ------------------------")
    live_id_nums = server.select_Players_From_Connected_Clients() # WE GET STUCK HERE

    # start the game with the current players and spectators:
    print("------------------------ CREATE THE BOARD OBJECT ------------------------")
    board = tiles.Board()
    print("------------------------ START THE GAME ------------------------")
    # server.start_game(board) # game starts now
    # server.reset_clients()
    server.start_game(board, live_id_nums) # game starts now







#
# while True:
#
#     readable, writeable, exceptional = select.select(server.listening, [], server.listening)
#
#     if server.server_socket in readable:
#
#
#         thread = threading.Thread(
#             #target = server.cew,#server.client_handler,
#             target = server.handle_client_connection,
#             args = (readable, writeable, exceptional),
#             daemon = True
#         )
#         thread.start()
#
#     # NOW WE PLAY THE GAME!!!
#     # write the functions to implement the game logic
#     if(server.game_started == False and len(server.all_connected_clients) > 1):
#         print("At least 2 clients connected")
#         # start the game
#         print("THE GAME IS STARTING!!!!")
#
#         # while True:
#         print("making the board")
#         board = tiles.Board()
#         # new players
#
#         live_id_nums = server.select_Players_From_Connected_Clients()
#
#         # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
#         # self.game_started == True
#         print("calling the start_game method")
#         server.start_game(board) # game starts now
#         print("calling reset")
#         # board.reset()
#         # print("calling resetState")
#         # server.resetState() # do this
#
#         # # or this:
#         # print("reset")
#         # for one_client in server.all_connected_clients:
#         #     #
#         #     one_client.connection.send(tiles.MessageGameStart().pack())
#         #     #currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
#         #     #currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())
#         #     #
#         # print("reset")
#
#
#
#
#
#
#
#         # while len(server.all_connected_clients) >= 1:
#         # # while True:
#         #     print("making the board")
#         #     board = tiles.Board()
#         #     # new players
#         #
#         #     live_id_nums = server.select_Players_From_Connected_Clients()
#         #
#         #     # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
#         #     # self.game_started == True
#         #     print("calling the start_game method")
#         #     server.start_game(board) # game starts now
#         #     print("calling reset")
#         #     # board.reset()
#         #     # print("calling resetState")
#         #     # server.resetState() # do this
#         #
#         #     # # or this:
#         #     # print("reset")
#         #     # for one_client in server.all_connected_clients:
#         #     #     #
#         #     #     one_client.connection.send(tiles.MessageGameStart().pack())
#         #     #     #currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
#         #     #     #currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())
#         #     #     #
#         #     # print("reset")









# SECOND VERSION - SEE OG BELOW
# while True:
#
#     readable, writeable, exceptional = select.select(server.listening, [], server.listening)
#
#     if server.server_socket in readable:
#
#
#         thread = threading.Thread(
#             #target = server.cew,#server.client_handler,
#             target = server.handle_client_connection,
#             args = (readable, writeable, exceptional),
#             daemon = True
#         )
#         thread.start()
#
#     # NOW WE PLAY THE GAME!!!
#     # write the functions to implement the game logic
#     if(server.game_started == False and len(server.all_connected_clients) > 1):
#         print("At least 2 clients connected")
#         # start the game
#         print("THE GAME IS STARTING!!!!")
#
#         # while True:
#         print("making the board")
#         board = tiles.Board()
#         # new players
#
#         live_id_nums = server.select_Players_From_Connected_Clients()
#
#         # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
#         # self.game_started == True
#         print("calling the start_game method")
#         server.start_game(board) # game starts now
#         print("calling reset")
#         # board.reset()
#         # print("calling resetState")
#         # server.resetState() # do this
#
#         # # or this:
#         # print("reset")
#         # for one_client in server.all_connected_clients:
#         #     #
#         #     one_client.connection.send(tiles.MessageGameStart().pack())
#         #     #currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
#         #     #currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())
#         #     #
#         # print("reset")
#
#
#
#
#
#
#
#         # while len(server.all_connected_clients) >= 1:
#         # # while True:
#         #     print("making the board")
#         #     board = tiles.Board()
#         #     # new players
#         #
#         #     live_id_nums = server.select_Players_From_Connected_Clients()
#         #
#         #     # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
#         #     # self.game_started == True
#         #     print("calling the start_game method")
#         #     server.start_game(board) # game starts now
#         #     print("calling reset")
#         #     # board.reset()
#         #     # print("calling resetState")
#         #     # server.resetState() # do this
#         #
#         #     # # or this:
#         #     # print("reset")
#         #     # for one_client in server.all_connected_clients:
#         #     #     #
#         #     #     one_client.connection.send(tiles.MessageGameStart().pack())
#         #     #     #currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
#         #     #     #currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())
#         #     #     #
#         #     # print("reset")




































# OG VERSION
# while True:
#
#     readable, writeable, exceptional = select.select(server.listening, [], server.listening)
#
#     # global server
#     # global self.all_connected_clients
#     # global idnum
#     # global listening # added
#     # global started
#
#     if server.server_socket in readable:
#
#
#         thread = threading.Thread(
#             #target = server.cew,#server.client_handler,
#             target = server.handle_client_connection,
#             daemon = True
#         )
#         thread.start()
#
#         # server.listening.append(client.connection)
#
#         # # if server.turn_Queue.qsize() < 4 or server.game_started == False:
#         # if server.turn_Queue.qsize() < 4 and server.game_started == False:
#         #     server.turn_Queue.put(client) # put the newely connected client on the turn
#         #     all_idnums_on_the_turn_queue.append(idnum)
#         #     server.current_players.append(client)
#         #     live_idnums.update({idnum:client})
#         #
#         # # elif server.turn_Queue.qsize() == 4 or server.game_started == True:
#         # elif server.turn_Queue.qsize() == 4 and server.game_started == True:
#         #     server.send_history_to_spectator(client)
#         #     # make all subequent connecting clients, spectators of the game:
#         #     server.spectators.append(idnum)
#         #     all_idnums_on_the_spec_queue.append(idnum)
#         # else:
#         #     print("Sorry! that's all we can allow on the server i'm affraid!")
#         #
#         # if idnum <= tiles.IDNUM_LIMIT:
#         #     idnum += 1
#         # else:
#         #     print("OH NO!")
#         #
#         # print()
#         # print(f"Client joined at: {client_address}")
#         # print(f"all the currently connected clients: {[c.idnum for c in server.all_connected_clients]}")
#         # print(f"the turn_Queue.qsize(): {server.turn_Queue.qsize()}")
#         # print(f"all idnums on turn_Queue:      {all_idnums_on_the_turn_queue}")
#         # print(f"all idnums on spectator_Queue: {all_idnums_on_the_spec_queue}\n")
#         # print()
#         #
#         #
#         # disconnected_clients = []
#         #
#         # if client.connection in exceptional:
#         #     print('client {} exception'.format(client.address))
#         #     disconnected_clients.append(client)
#
#         # else:
#         #     print("Sorry! that's all we can allow on the server i'm affraid!")
#
#
#     # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     # NOW WE PLAY THE GAME!!!
#     # write the functions to implement the game logic
#
#
#         if(server.game_started == False and len(server.all_connected_clients) > 1):
#             # start the game
#                 print("starting the game now")
#                 #
#                 # thread = threading.Thread(
#                 #     #target = server.cew,#server.client_handler,
#                 #     target = server.threaded_start_game,
#                 #     daemon = True
#                 # )
#                 # thread.start()
#                 # server.star
#                 while True:
#                     board = tiles.Board()
#                     #new players
#                     live_id_nums = self.select_Players_From_Connected_Clients()
#                     # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
#                     # self.game_started == True
#                     self.start_game(board) # game starts now
#                     board.reset()
#                     server.resetState()


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

# OG VERSION
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
#
# class Client():
#     """This class stores one client connection, the address of the client,
#     and a buffer of bytes that we have received from the client but not yet
#     processed.
#     """
#     def __init__(self, idnum, connection, address):
#         self.idnum = idnum
#         self.connection = connection
#         self.client_address = address
#         self.name = '{}:{}'.format(SERVER_IP, address)
#         self.message_queues = {} # a dictionary of message queues for all in self.all_connected_clients
#         self.buffer = bytearray()
#
# # start = -1
# class Server:
#
#     def __init__(self):
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.listening = [self.server_socket]
#         self.game_started = False # game has not started by default
#         self.turn_Queue = queue.Queue(maxsize = 4) # the queue for the players
#         self.all_connected_clients = []
#
#         self.current_players = []
#         self.spectators = [] # the queue of spectators
#
#         # self.live_id_nums = []
#         # self.spectator_id_nums = []
#
#         self.MAX_CLIENTS = 5
#         self.MAX_PLAYERS = 4
#         self.MAX_SPECTATORS = 1
#
#         self.game_message_history = []
#         self.disconnected_clients = []
#
#         # self.board = tiles.Board()
#         # live_idnums
#
#
#     # remove a client from the server (because they have disconnected)
#     # we need to remove them from the global client list, and also remove their
#     # connection from our list of connections-to-listen-to
#     def remove_client(client):
#         # global self.all_connected_clients
#         # global listening
#         self.listening.remove(client.connection)
#         self.all_connected_clients.remove(client)
#
#
#     '''
#     Returns the list of idnums for all clients participating in gameplay.
#     '''
#     def select_Players_From_Connected_Clients(self):
#         # global idnum
#
#         live_id_nums = []
#
#         # while (len(self.current_players) < 2):
#         while (len(self.current_players) < self.MAX_PLAYERS):
#
#             player_choice = random.choice(self.all_connected_clients)
#
#             if player_choice not in self.current_players:
#                 self.current_players.append(player_choice)
#                 live_id_nums.append(player_choice.idnum)
#
#             if server.turn_Queue.qsize() < self.MAX_PLAYERS: # or server.game_started == False:
#             # if self.turn_Queue.qsize() < 4 and self.game_started == False:
#                 self.turn_Queue.put(player_choice) # put the newely connected client on the turn
#                 all_idnums_on_the_turn_queue.append(idnum)
#                 # live_idnums.update({idnum:client})
#
#                 # if(len(self.current_players)==len(self.all_connected_clients)):
#                 # # if(len(self.current_players) == tiles.PLAYER_LIMIT): # it's getting stuck in here! need 4 players!
#                 # # if(len(self.current_players) == len(self.current_players)):
#                 #     break
#
#         return live_id_nums
#
# # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#         # elif self.turn_Queue.qsize() == 4 or self.game_started == True:
#         # elif self.turn_Queue.qsize() == self.MAX_PLAYERS and self.game_started == True:
#         #     self.send_history_to_spectator(client)
#         #     # make all subequent connecting clients, spectators of the game:
#         #     self.spectators.append(idnum)
#         #     all_idnums_on_the_spec_queue.append(idnum)
#
#     def select_Spectators_From_Connected_Clients(self, live_id_nums):
#
#         spectator_id_nums = []
#
#         # select the spectator clients
#         # select the spectator clients
#         for a_connected_client in self.all_connected_clients:
#             if a_connected_client.idnum not in live_id_nums:
#                 self.spectators.append(a_connected_client.idnum)
#
#         return spectator_id_nums
#
#
#
#
#
#
#         # # while (len(self.current_players) < 2):
#         # if (len(self.current_players) < self.MAX_PLAYERS):
#         # # while (len(self.current_players) < tiles.IDNUM_LIMIT):
#         #     player_choice = random.choice(self.all_connected_clients)
#         #     if player_choice not in self.current_players:
#         #         self.current_players.append(player_choice)
#         #         live_id_nums.append(player_choice.idnum)
#         #         # if(len(self.current_players)==len(self.all_connected_clients)):
#         #         # if(len(self.current_players) == tiles.PLAYER_LIMIT): # it's getting stuck in here! need 4 players!
#         #         # if(len(self.current_players) == len(self.current_players)):
#         #             # break
#         # else:
#         #     print("\nOHH that's all the players that we can support i'm affraid...\n")
#         #
#         # return live_id_nums # do stuff depending on whether or not this is empty
#
#
#
#
#     # OG VERSION
#     # '''
#     # Returns the list of idnums for all clients participating in gameplay.
#     # '''
#     # def select_Players_From_Connected_Clients(self):
#     #     # print("inside: select_Players_From_Connected_Clients")
#     #     # global self.all_connected_clients
#     #     # global self.current_players
#     #
#     #     live_id_nums = []
#     #
#     #     # print("made live_id_nums in select_...")
#     #     # self.current_players = []#just in case theres anything left in there
#     #
#     #     # while (len(self.current_players) < 2):
#     #     while (len(self.current_players) < self.MAX_PLAYERS):
#     #     # while (len(self.current_players) < tiles.IDNUM_LIMIT):
#     #         player_choice = random.choice(self.all_connected_clients)
#     #         if player_choice not in self.current_players:
#     #             self.current_players.append(player_choice)
#     #             live_id_nums.append(player_choice.idnum)
#     #             if(len(self.current_players)==len(self.all_connected_clients)):
#     #             # if(len(self.current_players) == tiles.PLAYER_LIMIT): # it's getting stuck in here! need 4 players!
#     #             # if(len(self.current_players) == len(self.current_players)):
#     #                 break
#     #
#     #     return live_id_nums
#     #
#     #     # # while (len(self.current_players) < 2):
#     #     # if (len(self.current_players) < self.MAX_PLAYERS):
#     #     # # while (len(self.current_players) < tiles.IDNUM_LIMIT):
#     #     #     player_choice = random.choice(self.all_connected_clients)
#     #     #     if player_choice not in self.current_players:
#     #     #         self.current_players.append(player_choice)
#     #     #         live_id_nums.append(player_choice.idnum)
#     #     #         # if(len(self.current_players)==len(self.all_connected_clients)):
#     #     #         # if(len(self.current_players) == tiles.PLAYER_LIMIT): # it's getting stuck in here! need 4 players!
#     #     #         # if(len(self.current_players) == len(self.current_players)):
#     #     #             # break
#     #     # else:
#     #     #     print("\nOHH that's all the players that we can support i'm affraid...\n")
#     #     #
#     #     # return live_id_nums # do stuff depending on whether or not this is empty
#
#
#     def resetState(self):
#         print("reset")
#         for one_client in self.all_connected_clients:
#             #
#             one_client.connection.send(tiles.MessageGameStart().pack())
#             #currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
#             #currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())
#             #
#         print("reset")
#         #return board.reset()
#
#
#
#     # '''
#     # Returns the list of idnums for all clients participating in gameplay.
#     # '''
#     # def select_Players_From_Connected_Clients(self):
#     #     # print("inside: select_Players_From_Connected_Clients")
#     #     # global self.all_connected_clients
#     #     # global self.current_players
#     #
#     #     # print("made live_id_nums in select_...")
#     #     # self.current_players = []#just in case theres anything left in there
#     #
#     #     # while (len(self.current_players) < 2):
#     #     while (len(self.current_players) < self.MAX_PLAYERS):
#     #     # while (len(self.current_players) < tiles.IDNUM_LIMIT):
#     #         player_choice = random.choice(self.all_connected_clients)
#     #         if player_choice not in self.current_players:
#     #             self.current_players.append(player_choice)
#     #             self.live_id_nums.append(player_choice.idnum)
#     #             if(len(self.current_players)==len(self.all_connected_clients)):
#     #             # if(len(self.current_players) == tiles.PLAYER_LIMIT): # it's getting stuck in here! need 4 players!
#     #             # if(len(self.current_players) == len(self.current_players)):
#     #                 break
#
#
#     # '''
#     # Returns the list of idnums for all spectating clients.
#     #
#     # Can only be called after self.select_Players_From_Connected_Clients()
#     # '''
#     # def select_Spectators_From_Connected_Clients(self, live_id_nums):
#     #     # spectator_id_nums = []
#     #
#     #     # while (len(self.current_players) < 2):
#     #     while (len(self.spectators) < self.MAX_SPECTATORS):
#     #         for C in self.all_connected_clients:
#     #             if C not in live_id_nums:
#     #                 self.spectator_id_nums.append(C.idnum)
#     #
#     #     return spectator_id_nums
#
#     '''
#     def threaded_start_game(self): # this goes in the thread
#         while True:
#             board = tiles.Board()
#             #new players
#             live_id_nums = self.select_Players_From_Connected_Clients()
#             # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
#             # self.game_started == True
#             self.start_game(board)
#             board.reset()
#             server.resetState()
#     '''
#
#
#     # def start_game(self):
#     # def start_game(self, board):  # take in live_id_nums ????????????????????????????????????????????????????????????????????????
#     def start_game(self, board, live_id_nums):
#         # global live_id_nums
#         # global game_message_history
#         # global self.all_connected_clients
#         # global current_players
#         # global started
#         # global board
#
#         # have access to these
#         # live_id_nums = self.select_Players_From_Connected_Clients()
#         # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
#
#         # live_id_nums = self.select_Players_From_Connected_Clients()
#         # live_id_nums = []
#         # live_id_nums = server.select_Players_From_Connected_Clients()
#         print("sending Welcome messgae to all players")
#         print("Adding tiles to each player's hand")
#         for i in self.current_players:
#             # live_id_nums.append(i.idnum)
#             currentConnection = i.connection
#             currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
#             currentConnection.send(tiles.MessageGameStart().pack())
#
#             #step 4
#
#             for _ in range(tiles.HAND_SIZE):
#                 # print("THREE")
#                 tileid = tiles.get_random_tileid()
#                 currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())
#
#             for j in self.all_connected_clients:
#                 print("FOUR")
#                 print(i.name)
#                 j.connection.send(tiles.MessagePlayerJoined(i.name, i.idnum).pack())
#
#         # for j in self.spectators:
#         #     print("FOUR")
#         #     print(i.name)
#         #     j.connection.send(tiles.MessagePlayerJoined(i.name, i.idnum).pack())
#
#         # started = 1
#         self.game_started = True
#         #main game loop
#         buffer = bytearray()
#
#         while len(live_id_nums) > 1: #step 5
#             # print("start")
#             current = self.turn_Queue.get()
#             current_idnum = current.idnum
#             # print(current_idnum)
#             current_connection = current.connection
#             current_address = current.client_address
#             for i in self.all_connected_clients:
#                 #step 5 a
#                 i.connection.send(tiles.MessagePlayerTurn(current_idnum).pack())
#             #step 5 b
#             chunk = current_connection.recv(4096)
#
#             if not chunk:
#                 print('client {} disconnected'.format(current_address))
#                 return
#
#
#             buffer.extend(chunk)
#
#             #step 5 c
#             msg, consumed = tiles.read_message_from_bytearray(buffer)
#             if not consumed:
#                 break
#
#             buffer = buffer[consumed:]
#
#             print('received message {}'.format(msg))
#
#             #step 5 c all
#             #can probably combine
#             if isinstance(msg, tiles.MessagePlaceTile):
#
#                 self.game_message_history.append(msg)
#
#                 if board.set_tile(msg.x, msg.y, msg.tileid, msg.rotation, msg.idnum):
#                     for i in self.all_connected_clients:
#                         i.connection.send(msg.pack())
#                     positionupdates, eliminated = board.do_player_movement(live_id_nums)
#
#                     for msg in positionupdates:
#
#                         self.game_message_history.append(msg)
#
#                         for i in self.all_connected_clients:
#                             i.connection.send(msg.pack())
#
#                     for e in eliminated:
#                         live_id_nums.remove(e)
#                         print("liveid len is"+str(len(live_id_nums)))
#                         for i in self.all_connected_clients:
#                             i.connection.send(tiles.MessagePlayerEliminated(e).pack())
#                         if e == current_idnum:
#                             print("You lose!")
#                             break
#                             #return # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#     #                     if current_idnum in eliminated:
#     #                         for i in self.all_connected_clients:
#     #                             i.connection.send(tiles.MessagePlayerEliminated(current_idnum).pack())
#     #                         live_id_nums.remove(current_idnum)
#     #                         #eliminated
#     #                         print("You lose!")
#     #                         return
#
#                     tileid = tiles.get_random_tileid()
#                     current_connection.send(tiles.MessageAddTileToHand(tileid).pack())
#
#                 self.turn_Queue.put(current)
#
#             elif isinstance(msg, tiles.MessageMoveToken):
#                 if not board.have_player_position(msg.idnum):
#                     if board.set_player_start_position(msg.idnum, msg.x, msg.y, msg.position):
#
#                         positionupdates, eliminated = board.do_player_movement(live_id_nums)
#                         for msg in positionupdates:
#                             for i in self.all_connected_clients:
#                                 i.connection.send(msg.pack())
#                         for e in eliminated:
#                             live_id_nums.remove(e)
#                             print("liveid len is"+str(len(live_id_nums)))
#                             for i in self.all_connected_clients:
#                                 i.connection.send(tiles.MessagePlayerEliminated(e).pack())
#                             if e == current_idnum:
#                                 print("You lose!")
#                                 break
#                                 #return
#
#                     self.turn_Queue.put(current)
#
#         print("End of start_game()")
#         # server.restart()
#         self.game_started == False
#         return
#
#     def reset_clients(self):
#         for c in self.all_clients:
#             c.connection.send(tiles.MessageGameStart().pack())
#
#
#
#
#     # THIS VERSION ALSO WORKS - OG VERSION BELOW THIS ONE
#     # # def start_game(self):
#     # def start_game(self, board):
#     #     # global live_id_nums
#     #     # global game_message_history
#     #     # global self.all_connected_clients
#     #     # global current_players
#     #     # global started
#     #     # global board
#     #
#     #     # have access to these
#     #     # live_id_nums = self.select_Players_From_Connected_Clients()
#     #     # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
#     #
#     #     # live_id_nums = self.select_Players_From_Connected_Clients()
#     #     live_id_nums = []
#     #     # live_id_nums = server.select_Players_From_Connected_Clients()
#     #     print("sending Welcome messgae to all players")
#     #     print("Adding tiles to each player's hand")
#     #     for i in self.current_players:
#     #         live_id_nums.append(i.idnum)
#     #         currentConnection = i.connection
#     #         currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
#     #         currentConnection.send(tiles.MessageGameStart().pack())
#     #
#     #         #step 4
#     #
#     #         for _ in range(tiles.HAND_SIZE):
#     #             # print("THREE")
#     #             tileid = tiles.get_random_tileid()
#     #             currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())
#     #
#     #         for j in self.all_connected_clients:
#     #             print("FOUR")
#     #             print(i.name)
#     #             j.connection.send(tiles.MessagePlayerJoined(i.name, i.idnum).pack())
#     #
#     #     # for j in self.spectators:
#     #     #     print("FOUR")
#     #     #     print(i.name)
#     #     #     j.connection.send(tiles.MessagePlayerJoined(i.name, i.idnum).pack())
#     #
#     #     # started = 1
#     #     self.game_started = True
#     #     #main game loop
#     #     buffer = bytearray()
#     #
#     #     while len(live_id_nums)>1: #step 5
#     #         # print("start")
#     #         current = self.turn_Queue.get()
#     #         current_idnum = current.idnum
#     #         # print(current_idnum)
#     #         current_connection = current.connection
#     #         current_address = current.client_address
#     #         for i in self.all_connected_clients:
#     #             #step 5 a
#     #             i.connection.send(tiles.MessagePlayerTurn(current_idnum).pack())
#     #         #step 5 b
#     #         chunk = current_connection.recv(4096)
#     #
#     #         if not chunk:
#     #             print('client {} disconnected'.format(current_address))
#     #             return
#     #
#     #
#     #         buffer.extend(chunk)
#     #
#     #         #step 5 c
#     #         msg, consumed = tiles.read_message_from_bytearray(buffer)
#     #         if not consumed:
#     #             break
#     #
#     #         buffer = buffer[consumed:]
#     #
#     #         print('received message {}'.format(msg))
#     #
#     #         #step 5 c all
#     #         #can probably combine
#     #         if isinstance(msg, tiles.MessagePlaceTile):
#     #
#     #             self.game_message_history.append(msg)
#     #
#     #             if board.set_tile(msg.x, msg.y, msg.tileid, msg.rotation, msg.idnum):
#     #                 for i in self.all_connected_clients:
#     #                     i.connection.send(msg.pack())
#     #                 positionupdates, eliminated = board.do_player_movement(live_id_nums)
#     #
#     #                 for msg in positionupdates:
#     #
#     #                     self.game_message_history.append(msg)
#     #
#     #                     for i in self.all_connected_clients:
#     #                         i.connection.send(msg.pack())
#     #
#     #                 for e in eliminated:
#     #                     live_id_nums.remove(e)
#     #                     print("liveid len is"+str(len(live_id_nums)))
#     #                     for i in self.all_connected_clients:
#     #                         i.connection.send(tiles.MessagePlayerEliminated(e).pack())
#     #                     if e == current_idnum:
#     #                         print("You lose!")
#     #                         break
#     #                         #return # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     #
#     # #                     if current_idnum in eliminated:
#     # #                         for i in self.all_connected_clients:
#     # #                             i.connection.send(tiles.MessagePlayerEliminated(current_idnum).pack())
#     # #                         live_id_nums.remove(current_idnum)
#     # #                         #eliminated
#     # #                         print("You lose!")
#     # #                         return
#     #
#     #                 tileid = tiles.get_random_tileid()
#     #                 current_connection.send(tiles.MessageAddTileToHand(tileid).pack())
#     #
#     #             self.turn_Queue.put(current)
#     #
#     #         elif isinstance(msg, tiles.MessageMoveToken):
#     #             if not board.have_player_position(msg.idnum):
#     #                 if board.set_player_start_position(msg.idnum, msg.x, msg.y, msg.position):
#     #
#     #                     positionupdates, eliminated = board.do_player_movement(live_id_nums)
#     #                     for msg in positionupdates:
#     #                         for i in self.all_connected_clients:
#     #                             i.connection.send(msg.pack())
#     #                     for e in eliminated:
#     #                         live_id_nums.remove(e)
#     #                         print("liveid len is"+str(len(live_id_nums)))
#     #                         for i in self.all_connected_clients:
#     #                             i.connection.send(tiles.MessagePlayerEliminated(e).pack())
#     #                         if e == current_idnum:
#     #                             print("You lose!")
#     #                             break
#     #                             #return
#     #
#     #                 self.turn_Queue.put(current)
#     #
#     #     print("End of start_game()")
#     #     # server.restart()
#     #     self.game_started == False
#     #     return
#
#
#
#
#
# # THIS ONE WORKS:
# #     # def start_game(self):
# #     def start_game(self,board):
# #         # global live_id_nums
# #         # global game_message_history
# #         # global self.all_connected_clients
# #         # global current_players
# #         # global started
# #         # global board
# #
# #         # have access to these
# #         # live_id_nums = self.select_Players_From_Connected_Clients()
# #         # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
# #
# #         # live_id_nums = self.select_Players_From_Connected_Clients()
# #         live_id_nums = []
# #         for i in self.current_players:
# #             live_id_nums.append(i.idnum)
# #             currentConnection = i.connection
# #             currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
# #             currentConnection.send(tiles.MessageGameStart().pack())
# #
# #             #step 4
# #
# #             for _ in range(tiles.HAND_SIZE):
# #                 print("THREE")
# #                 tileid = tiles.get_random_tileid()
# #                 currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())
# #
# #             for j in self.all_connected_clients:
# #                 print("FOUR")
# #                 print(i.name)
# #                 j.connection.send(tiles.MessagePlayerJoined(i.name, i.idnum).pack())
# #
# #         # for j in self.spectators:
# #         #     print("FOUR")
# #         #     print(i.name)
# #         #     j.connection.send(tiles.MessagePlayerJoined(i.name, i.idnum).pack())
# #
# #         # started = 1
# #         self.game_started = True
# #         #main game loop
# #         buffer = bytearray()
# #
# #         while len(live_id_nums)>1: #step 5
# #             print("start")
# #             current = self.turn_Queue.get()
# #             current_idnum = current.idnum
# #             print(current_idnum)
# #             current_connection = current.connection
# #             current_address = current.client_address
# #             for i in self.all_connected_clients:
# #                 #step 5 a
# #                 i.connection.send(tiles.MessagePlayerTurn(current_idnum).pack())
# #             #step 5 b
# #             chunk = current_connection.recv(4096)
# #
# #             if not chunk:
# #                 print('client {} disconnected'.format(current_address))
# #                 return
# #
# #
# #             buffer.extend(chunk)
# #
# #             #step 5 c
# #             msg, consumed = tiles.read_message_from_bytearray(buffer)
# #             if not consumed:
# #                 break
# #
# #             buffer = buffer[consumed:]
# #
# #             print('received message {}'.format(msg))
# #
# #             #step 5 c all
# #             #can probably combine
# #             if isinstance(msg, tiles.MessagePlaceTile):
# #
# #                 self.game_message_history.append(msg)
# #
# #                 if board.set_tile(msg.x, msg.y, msg.tileid, msg.rotation, msg.idnum):
# #                     for i in self.all_connected_clients:
# #                         i.connection.send(msg.pack())
# #                     positionupdates, eliminated = board.do_player_movement(live_id_nums)
# #
# #                     for msg in positionupdates:
# #
# #                         self.game_message_history.append(msg)
# #
# #                         for i in self.all_connected_clients:
# #                             i.connection.send(msg.pack())
# #
# #                     for e in eliminated:
# #                         live_id_nums.remove(e)
# #                         print("liveid len is"+str(len(live_id_nums)))
# #                         for i in self.all_connected_clients:
# #                             i.connection.send(tiles.MessagePlayerEliminated(e).pack())
# #                         if e == current_idnum:
# #                             print("You lose!")
# #                             break
# #                             #return # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# #
# # #                     if current_idnum in eliminated:
# # #                         for i in self.all_connected_clients:
# # #                             i.connection.send(tiles.MessagePlayerEliminated(current_idnum).pack())
# # #                         live_id_nums.remove(current_idnum)
# # #                         #eliminated
# # #                         print("You lose!")
# # #                         return
# #
# #                     tileid = tiles.get_random_tileid()
# #                     current_connection.send(tiles.MessageAddTileToHand(tileid).pack())
# #
# #                 self.turn_Queue.put(current)
# #
# #             elif isinstance(msg, tiles.MessageMoveToken):
# #                 if not board.have_player_position(msg.idnum):
# #                     if board.set_player_start_position(msg.idnum, msg.x, msg.y, msg.position):
# #
# #                         positionupdates, eliminated = board.do_player_movement(live_id_nums)
# #                         for msg in positionupdates:
# #                             for i in self.all_connected_clients:
# #                                 i.connection.send(msg.pack())
# #                         for e in eliminated:
# #                             live_id_nums.remove(e)
# #                             print("liveid len is"+str(len(live_id_nums)))
# #                             for i in self.all_connected_clients:
# #                                 i.connection.send(tiles.MessagePlayerEliminated(e).pack())
# #                             if e == current_idnum:
# #                                 print("You lose!")
# #                                 break
# #                                 #return
# #
# #                     self.turn_Queue.put(current)
# #
# #         print("End of start_game()")
# #         # server.restart()
# #         self.game_started == False
# #         return
#
#     # if spetators:
#     #     for i in zip(self.current_players, self.spectators):
#     #         pass
#     # else:
#     #     pass
#
#
#     '''
#     # def start_game(self):
#     def start_game(self,board):
#         for a_client in self.all_connected_clients: # just do this ????????????????????????????????????????????
#             if a_client.idnum in live_id_nums:
#                 # do the code as given
#                 pass
#             else:
#                 # do the code for the spectator
#                 pass
#     '''
# # THE OG !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# #     def start_game(self):
# #
# #         # global self.all_connected_clients
# #         # global current_players
# #         # global started
# #         # global board
# #
# #         # have access to these
# #         # live_id_nums = self.select_Players_From_Connected_Clients()
# #         # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
# #
# #         # live_id_nums = self.select_Players_From_Connected_Clients()
# #         live_id_nums = []
# #         # for i in self.current_players:
# #         for i in self.all_connected_clients:
# #             live_id_nums.append(i.idnum)
# #             currentConnection = i.connection
# #             currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
# #
# #             #step 4
# #
# #             for _ in range(tiles.HAND_SIZE):
# #                 print("THREE")
# #                 tileid = tiles.get_random_tileid()
# #                 currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())
# #
# #             for j in self.all_connected_clients:
# #                 print("FOUR")
# #                 print(i.name)
# #                 j.connection.send(tiles.MessagePlayerJoined(i.name, i.idnum).pack())
# #
# #         # for j in self.spectators:
# #         #     print("FOUR")
# #         #     print(i.name)
# #         #     j.connection.send(tiles.MessagePlayerJoined(i.name, i.idnum).pack())
# #
# #         # started = 1
# #         self.game_started = True
# #         #main game loop
# #         buffer = bytearray()
# #
# #         while len(live_id_nums)>1: #step 5
# #             print("start")
# #             current = self.turn_Queue.get()
# #             current_idnum = current.idnum
# #             print(current_idnum)
# #             current_connection = current.connection
# #             current_address = current.client_address
# #             for i in self.all_connected_clients:
# #                 #step 5 a
# #                 i.connection.send(tiles.MessagePlayerTurn(current_idnum).pack())
# #             #step 5 b
# #             chunk = current_connection.recv(4096)
# #
# #             if not chunk:
# #                 print('client {} disconnected'.format(current_address))
# #                 return
# #
# #
# #             buffer.extend(chunk)
# #
# #             #step 5 c
# #             msg, consumed = tiles.read_message_from_bytearray(buffer)
# #             if not consumed:
# #                 break
# #
# #             buffer = buffer[consumed:]
# #
# #             print('received message {}'.format(msg))
# #
# #             #step 5 c all
# #             #can probably combine
# #             if isinstance(msg, tiles.MessagePlaceTile):
# #
# #                 game_message_history.append(msg)
# #
# #                 if board.set_tile(msg.x, msg.y, msg.tileid, msg.rotation, msg.idnum):
# #                     for i in self.all_connected_clients:
# #                         i.connection.send(msg.pack())
# #                     positionupdates, eliminated = board.do_player_movement(live_id_nums)
# #
# #                     for msg in positionupdates:
# #
# #                         game_message_history.append(msg)
# #
# #                         for i in self.all_connected_clients:
# #                             i.connection.send(msg.pack())
# #
# #                     for e in eliminated:
# #                         live_id_nums.remove(e)
# #                         print("liveid len is"+str(len(live_id_nums)))
# #                         for i in self.all_connected_clients:
# #                             i.connection.send(tiles.MessagePlayerEliminated(e).pack())
# #                         if e == current_idnum:
# #                             print("You lose!")
# #                             break
# #                             #return # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# #
# # #                     if current_idnum in eliminated:
# # #                         for i in self.all_connected_clients:
# # #                             i.connection.send(tiles.MessagePlayerEliminated(current_idnum).pack())
# # #                         live_id_nums.remove(current_idnum)
# # #                         #eliminated
# # #                         print("You lose!")
# # #                         return
# #
# #                     tileid = tiles.get_random_tileid()
# #                     current_connection.send(tiles.MessageAddTileToHand(tileid).pack())
# #
# #                 self.turn_Queue.put(current)
# #
# #             elif isinstance(msg, tiles.MessageMoveToken):
# #                 if not board.have_player_position(msg.idnum):
# #                     if board.set_player_start_position(msg.idnum, msg.x, msg.y, msg.position):
# #
# #                         positionupdates, eliminated = board.do_player_movement(live_id_nums)
# #                         for msg in positionupdates:
# #                             for i in self.all_connected_clients:
# #                                 i.connection.send(msg.pack())
# #                         for e in eliminated:
# #                             live_id_nums.remove(e)
# #                             print("liveid len is"+str(len(live_id_nums)))
# #                             for i in self.all_connected_clients:
# #                                 i.connection.send(tiles.MessagePlayerEliminated(e).pack())
# #                             if e == current_idnum:
# #                                 print("You lose!")
# #                                 break
# #                                 #return
# #
# #                     self.turn_Queue.put(current)
# #
# #         print("End of start_game()")
# #         # server.restart()
# #         self.game_started == False
# #         return
#
#
#
#     def restart(self):
#         print("The game is over starting a new game in:")
#         now = time.time()
#         start = 5
#         count = 0
#         future = now + start
#         while time.time() < future:
#             if time.time() > future - start +count:
#                 print(start - count)
#                 count = count + 1
#
#         while (len(self.current_players)<4):
#         # while (len(self.current_players) <= 4):
#             choice = random.choice(self.all_connected_clients)
#             if choice not in self.current_players:
#                 self.current_players.append(choice)
#
#                 # why do we have this ??????????????????????????????????????????????????????????????????????
#                 # if(len(current_players)==len(self.all_connected_clients)):
#                 #     break
#
#                #and not (len(self.all_connected_clients)==len(current_players)):
#         #all_players_ids = [self.all_connected_clients]
#         for i in self.all_connected_clients:
#             print(i.idnum)
#
#     # OG VERSION
#     # # def handle_client_connection(self, socket):
#     # def handle_client_connection(self, readable, writeable, exceptional):
#     #     global idnum
#     #     connection, client_address = self.server_socket.accept() # connect the new client
#     #     host, port = client_address
#     #     name = '{}:{}'.format(host, port)
#     #     client = Client(idnum, connection, client_address)
#     #     self.all_connected_clients.append(client)
#     #     self.listening.append(client.connection)
#     #
#     #     # if server.turn_Queue.qsize() < 4 or server.game_started == False:
#     #     if self.turn_Queue.qsize() < 4 and self.game_started == False:
#     #         self.turn_Queue.put(client) # put the newely connected client on the turn
#     #         all_idnums_on_the_turn_queue.append(idnum)
#     #         self.current_players.append(client)
#     #         live_idnums.update({idnum:client})
#     #
#     #     # elif self.turn_Queue.qsize() == 4 or self.game_started == True:
#     #     elif self.turn_Queue.qsize() == 4 and self.game_started == True:
#     #         self.send_history_to_spectator(client)
#     #         # make all subequent connecting clients, spectators of the game:
#     #         self.spectators.append(idnum)
#     #         all_idnums_on_the_spec_queue.append(idnum)
#     #     else:
#     #         print("Sorry! that's all we can allow on the self i'm affraid!")
#     #
#     #     if idnum <= tiles.IDNUM_LIMIT:
#     #         idnum += 1
#     #     else:
#     #         print("OH NO!")
#     #
#     #     print()
#     #     print(f"Client joined at: {client_address}")
#     #     print(f"all the currently connected clients: {[c.idnum for c in self.all_connected_clients]}")
#     #     print(f"the turn_Queue.qsize(): {self.turn_Queue.qsize()}")
#     #     print(f"all idnums on turn_Queue:      {all_idnums_on_the_turn_queue}")
#     #     print(f"all idnums on spectator_Queue: {all_idnums_on_the_spec_queue}\n")
#     #     print()
#     #
#     #     # disconnected_clients = []
#     #
#     #     if client.connection in exceptional:
#     #         print('client {} exception'.format(client.address))
#     #         self.disconnected_clients.append(client)
#
#
#     # SECOND VERSION - OG
#     # # def handle_client_connection(self, socket):
#     # def handle_client_connection(self, readable, writeable, exceptional):
#     #     global idnum
#     #     # connection, client_address = self.server_socket.accept() # connect the new client
#     #     # host, port = client_address
#     #     # name = '{}:{}'.format(host, port)
#     #     # client = Client(idnum, connection, client_address)
#     #     # self.all_connected_clients.append(client)
#     #     # self.listening.append(client.connection)
#     #
#     #     # if self.turn_Queue.qsize() < self.MAX_PLAYERS and self.game_started == False:
#     #     if len(self.all_connected_clients) < self.MAX_CLIENTS:
#     #         connection, client_address = self.server_socket.accept() # connect the new client
#     #         host, port = client_address
#     #         name = '{}:{}'.format(host, port)
#     #         client = Client(idnum, connection, client_address)
#     #         self.all_connected_clients.append(client)
#     #         self.listening.append(client.connection)
#     #
#     #
#     #         # connect a client as a player:
#     #         self.turn_Queue.put(client) # put the newely connected client on the turn
#     #         self.current_players.append(client)
#     #
#     #         all_idnums_on_the_turn_queue.append(idnum)
#     #         live_idnums.update({idnum:client}) # we just update it here - we don't select the players here (initially) ???
#     #
#     #     # elif self.turn_Queue.qsize() == self.MAX_PLAYERS and self.game_started == True:
#     #     elif len(self.current_players) == self.MAX_PLAYERS and self.game_started == True:
#     #         # connect a client as a spectator:
#     #         # select the spectator clients
#     #         for a_connected_client in self.all_connected_clients:
#     #             if a_connected_client.idnum not in live_id_nums:
#     #                 self.spectators.append(a_connected_client.idnum)
#     #                 all_idnums_on_the_spec_queue.append(idnum)
#     #
#     #         self.send_history_to_spectator(client)
#     #         # make all subequent connecting clients, spectators of the game:
#     #         # self.spectators.append(idnum)
#     #         # all_idnums_on_the_spec_queue.append(idnum)
#     #
#     #     # # if self.turn_Queue.qsize() < self.MAX_PLAYERS and self.game_started == False:
#     #     # if len(self.current_players) < self.MAX_PLAYERS and self.game_started == False:
#     #     #     # connect a client as a player:
#     #     #     self.turn_Queue.put(client) # put the newely connected client on the turn
#     #     #     self.current_players.append(client)
#     #     #
#     #     #     all_idnums_on_the_turn_queue.append(idnum)
#     #     #     live_idnums.update({idnum:client}) # we just update it here - we don't select the players here (initially) ???
#     #     #
#     #     # # elif self.turn_Queue.qsize() == self.MAX_PLAYERS and self.game_started == True:
#     #     # elif len(self.current_players) == self.MAX_PLAYERS and self.game_started == True:
#     #     #     # connect a client as a spectator:
#     #     #     # select the spectator clients
#     #     #     for a_connected_client in self.all_connected_clients:
#     #     #         if a_connected_client.idnum not in live_id_nums:
#     #     #             self.spectators.append(a_connected_client.idnum)
#     #     #             all_idnums_on_the_spec_queue.append(idnum)
#     #     #
#     #     #     self.send_history_to_spectator(client)
#     #
#     #     else:
#     #         print("Sorry! that's all the clients' we can connect i'm affraid!")
#     #
#     #     if idnum <= tiles.IDNUM_LIMIT:
#     #         idnum += 1
#     #     else:
#     #         print("OH NO!")
#     #
#     #     print()
#     #     print(f"Client joined with address: {client_address}")
#     #     print(f"all the currently connected clients: {[c.idnum for c in self.all_connected_clients]}")
#     #     # print(f"the turn_Queue.qsize(): {self.turn_Queue.qsize()}")
#     #     # print(f"all idnums on turn_Queue:      {all_idnums_on_the_turn_queue}")
#     #     # print(f"all idnums on spectator_Queue: {all_idnums_on_the_spec_queue}\n")
#     #     print()
#     #
#     #     # disconnected_clients = []
#     #
#     #     if client.connection in exceptional:
#     #         print('client {} exception'.format(client.address))
#     #         self.disconnected_clients.append(client)
#
#
#     # SECOND VERSION - CLEANED UP
#     # def handle_client_connection(self, socket):
#     def handle_client_connection(self, readable, writeable, exceptional):
#         global idnum
#         # if self.turn_Queue.qsize() < self.MAX_PLAYERS and self.game_started == False:
#         if len(self.all_connected_clients) < self.MAX_CLIENTS:# server.start_game(board) # game starts now
#             connection, client_address = self.server_socket.accept() # connect the new client
#             host, port = client_address
#             name = '{}:{}'.format(host, port)
#             client = Client(idnum, connection, client_address)
#             self.all_connected_clients.append(client)
#             self.listening.append(client.connection)
#         else:
#             print("Sorry! that's all the clients' we can connect i'm affraid!")
#
#         if idnum <= tiles.IDNUM_LIMIT:
#             idnum += 1
#         else:
#             print("OH NO!")
#
#         print()
#         print(f"Client joined with address: {client_address}")
#         print(f"all the currently connected clients: {[c.idnum for c in self.all_connected_clients]}")
#         print()
#
#         if client.connection in exceptional:
#             print('client {} exception'.format(client.address))
#             self.disconnected_clients.append(client)
#
#
#     '''
#     Send the entire game history # fallback !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     '''
#     # def send_history_to_spectator(self, client):
#     #     currentIdnum = client.idnum
#     #     currentCon = client.connection
#     #
#     #     currentCon.send(tiles.MessageWelcome(currentIdnum).pack())
#     #     for i in self.current_players:
#     #         currentCon.send(tiles.MessagePlayerJoined(i.name,i.idnum).pack())
#     #         currentCon.send(tiles.MessagePlayerTurn(i.idnum).pack())
#     #
#     #     for move in self.game_message_history:
#     #         currentCon.send(move.pack())
#     #
#     #     # board = tiles.Board()
#     #     #currentCon.connection.send(
#     #     print(len(self.game_message_history))
#     #     for move in self.game_message_history:
#     #         currentCon.send(move.pack())
#
#
# SERVER_IP = ''
# PORT_NUMBER = 30020
#
# # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server = Server()
# server.server_socket.bind((SERVER_IP, PORT_NUMBER))
# # server.server_socket.setblocking(False)
# server.server_socket.listen(5)
#
# # -------------------------------------------------------------------------------------------------------------
#
# print('listening on {}'.format(server.server_socket.getsockname()))
# # a list of all the connections that we want to listen to:
# # listening = [server.server_socket]
# # a list of all the self.all_connected_clients currently connected to our server
# # self.all_connected_clients = []
# # current_players = []
# now = -1
# all_idnums_on_the_turn_queue = []
# all_idnums_on_the_spec_queue = []
#
# idnum = 0
# # game_message_history = []
#
# live_idnums = {}
# # live_idnums = []
# # board = tiles.Board()
#
#
# while True:
#     readable, writeable, exceptional = select.select(server.listening, [], server.listening)
#
#     # continuiously connect clients to the server - until we reach the client limit:
#     # if (len(server.all_connected_clients) < server.MAX_CLIENTS + 1):
#     if (len(server.all_connected_clients) < server.MAX_CLIENTS):
#         thread = threading.Thread(
#             #target = server.cew,#server.client_handler,
#             target = server.handle_client_connection,
#             args = (readable, writeable, exceptional),
#             daemon = True
#         )
#         thread.start()
#     else:
#         print("Sorry, that's all the clients the server can support!")
#
#     # select the players from the current pool of connected clients
#     live_id_nums = server.select_Players_From_Connected_Clients()
#     # spectator_id_nums = server.select_Spectators_From_Connected_Clients(live_id_nums)
#
#     # start the game with the current players and spectators:
#     board = tiles.Board()
#     # server.start_game(board) # game starts now
#     server.start_game(board, live_id_nums) # game starts now
#     server.reset_clients()
#
#
#
#
# #
# # while True:
# #
# #     readable, writeable, exceptional = select.select(server.listening, [], server.listening)
# #
# #     if server.server_socket in readable:
# #
# #
# #         thread = threading.Thread(
# #             #target = server.cew,#server.client_handler,
# #             target = server.handle_client_connection,
# #             args = (readable, writeable, exceptional),
# #             daemon = True
# #         )
# #         thread.start()
# #
# #     # NOW WE PLAY THE GAME!!!
# #     # write the functions to implement the game logic
# #     if(server.game_started == False and len(server.all_connected_clients) > 1):
# #         print("At least 2 clients connected")
# #         # start the game
# #         print("THE GAME IS STARTING!!!!")
# #
# #         # while True:
# #         print("making the board")
# #         board = tiles.Board()
# #         # new players
# #
# #         live_id_nums = server.select_Players_From_Connected_Clients()
# #
# #         # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
# #         # self.game_started == True
# #         print("calling the start_game method")
# #         server.start_game(board) # game starts now
# #         print("calling reset")
# #         # board.reset()
# #         # print("calling resetState")
# #         # server.resetState() # do this
# #
# #         # # or this:
# #         # print("reset")
# #         # for one_client in server.all_connected_clients:
# #         #     #
# #         #     one_client.connection.send(tiles.MessageGameStart().pack())
# #         #     #currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
# #         #     #currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())
# #         #     #
# #         # print("reset")
# #
# #
# #
# #
# #
# #
# #
# #         # while len(server.all_connected_clients) >= 1:
# #         # # while True:
# #         #     print("making the board")
# #         #     board = tiles.Board()
# #         #     # new players
# #         #
# #         #     live_id_nums = server.select_Players_From_Connected_Clients()
# #         #
# #         #     # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
# #         #     # self.game_started == True
# #         #     print("calling the start_game method")
# #         #     server.start_game(board) # game starts now
# #         #     print("calling reset")
# #         #     # board.reset()
# #         #     # print("calling resetState")
# #         #     # server.resetState() # do this
# #         #
# #         #     # # or this:
# #         #     # print("reset")
# #         #     # for one_client in server.all_connected_clients:
# #         #     #     #
# #         #     #     one_client.connection.send(tiles.MessageGameStart().pack())
# #         #     #     #currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
# #         #     #     #currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())
# #         #     #     #
# #         #     # print("reset")
#
#
#
#
#
#
#
#
#
# # SECOND VERSION - SEE OG BELOW
# # while True:
# #
# #     readable, writeable, exceptional = select.select(server.listening, [], server.listening)
# #
# #     if server.server_socket in readable:
# #
# #
# #         thread = threading.Thread(
# #             #target = server.cew,#server.client_handler,
# #             target = server.handle_client_connection,
# #             args = (readable, writeable, exceptional),
# #             daemon = True
# #         )
# #         thread.start()
# #
# #     # NOW WE PLAY THE GAME!!!
# #     # write the functions to implement the game logic
# #     if(server.game_started == False and len(server.all_connected_clients) > 1):
# #         print("At least 2 clients connected")
# #         # start the game
# #         print("THE GAME IS STARTING!!!!")
# #
# #         # while True:
# #         print("making the board")
# #         board = tiles.Board()
# #         # new players
# #
# #         live_id_nums = server.select_Players_From_Connected_Clients()
# #
# #         # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
# #         # self.game_started == True
# #         print("calling the start_game method")
# #         server.start_game(board) # game starts now
# #         print("calling reset")
# #         # board.reset()
# #         # print("calling resetState")
# #         # server.resetState() # do this
# #
# #         # # or this:
# #         # print("reset")
# #         # for one_client in server.all_connected_clients:
# #         #     #
# #         #     one_client.connection.send(tiles.MessageGameStart().pack())
# #         #     #currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
# #         #     #currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())
# #         #     #
# #         # print("reset")
# #
# #
# #
# #
# #
# #
# #
# #         # while len(server.all_connected_clients) >= 1:
# #         # # while True:
# #         #     print("making the board")
# #         #     board = tiles.Board()
# #         #     # new players
# #         #
# #         #     live_id_nums = server.select_Players_From_Connected_Clients()
# #         #
# #         #     # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
# #         #     # self.game_started == True
# #         #     print("calling the start_game method")
# #         #     server.start_game(board) # game starts now
# #         #     print("calling reset")
# #         #     # board.reset()
# #         #     # print("calling resetState")
# #         #     # server.resetState() # do this
# #         #
# #         #     # # or this:
# #         #     # print("reset")
# #         #     # for one_client in server.all_connected_clients:
# #         #     #     #
# #         #     #     one_client.connection.send(tiles.MessageGameStart().pack())
# #         #     #     #currentConnection.send(tiles.MessageWelcome(i.idnum).pack())
# #         #     #     #currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())
# #         #     #     #
# #         #     # print("reset")
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # OG VERSION
# # while True:
# #
# #     readable, writeable, exceptional = select.select(server.listening, [], server.listening)
# #
# #     # global server
# #     # global self.all_connected_clients
# #     # global idnum
# #     # global listening # added
# #     # global started
# #
# #     if server.server_socket in readable:
# #
# #
# #         thread = threading.Thread(
# #             #target = server.cew,#server.client_handler,
# #             target = server.handle_client_connection,
# #             daemon = True
# #         )
# #         thread.start()
# #
# #         # server.listening.append(client.connection)
# #
# #         # # if server.turn_Queue.qsize() < 4 or server.game_started == False:
# #         # if server.turn_Queue.qsize() < 4 and server.game_started == False:
# #         #     server.turn_Queue.put(client) # put the newely connected client on the turn
# #         #     all_idnums_on_the_turn_queue.append(idnum)
# #         #     server.current_players.append(client)
# #         #     live_idnums.update({idnum:client})
# #         #
# #         # # elif server.turn_Queue.qsize() == 4 or server.game_started == True:
# #         # elif server.turn_Queue.qsize() == 4 and server.game_started == True:
# #         #     server.send_history_to_spectator(client)
# #         #     # make all subequent connecting clients, spectators of the game:
# #         #     server.spectators.append(idnum)
# #         #     all_idnums_on_the_spec_queue.append(idnum)
# #         # else:
# #         #     print("Sorry! that's all we can allow on the server i'm affraid!")
# #         #
# #         # if idnum <= tiles.IDNUM_LIMIT:
# #         #     idnum += 1
# #         # else:
# #         #     print("OH NO!")
# #         #
# #         # print()
# #         # print(f"Client joined at: {client_address}")
# #         # print(f"all the currently connected clients: {[c.idnum for c in server.all_connected_clients]}")
# #         # print(f"the turn_Queue.qsize(): {server.turn_Queue.qsize()}")
# #         # print(f"all idnums on turn_Queue:      {all_idnums_on_the_turn_queue}")
# #         # print(f"all idnums on spectator_Queue: {all_idnums_on_the_spec_queue}\n")
# #         # print()
# #         #
# #         #
# #         # disconnected_clients = []
# #         #
# #         # if client.connection in exceptional:
# #         #     print('client {} exception'.format(client.address))
# #         #     disconnected_clients.append(client)
# #
# #         # else:
# #         #     print("Sorry! that's all we can allow on the server i'm affraid!")
# #
# #
# #     # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# #     # NOW WE PLAY THE GAME!!!
# #     # write the functions to implement the game logic
# #
# #
# #         if(server.game_started == False and len(server.all_connected_clients) > 1):
# #             # start the game
# #                 print("starting the game now")
# #                 #
# #                 # thread = threading.Thread(
# #                 #     #target = server.cew,#server.client_handler,
# #                 #     target = server.threaded_start_game,
# #                 #     daemon = True
# #                 # )
# #                 # thread.start()
# #                 # server.star
# #                 while True:
# #                     board = tiles.Board()
# #                     #new players
# #                     live_id_nums = self.select_Players_From_Connected_Clients()
# #                     # spectator_id_nums = self.select_Spectators_From_Connected_Clients()
# #                     # self.game_started == True
# #                     self.start_game(board) # game starts now
# #                     board.reset()
# #                     server.resetState()
#
#
#     '''
#     3. track the turn of the client
#     4. start the game
#     5. check which client's turn it is at any given point
#     6. broardcast the messages to be sent to everyone
#     7. swap the next player's turn
#     8. handle the main game loop
#     '''
#
#
#
# '''
# listening:
# a list of all the connections that we want to listen to:
#
# self.all_connected_clients = []:
# a list of all the self.all_connected_clients currently connected to our server
# self.all_connected_clients = []
#
# current_players = []:
# a list of all the current players in the game - those players which "participate" in gameplay
#
# now = -1
# A time value for now
#
# all_idnums_on_the_turn_queue = []
# all_idnums_on_the_spec_queue = []
# Lists to show what is on each respective queue
#
# idnum = 0
# the "identification number" of a certain client
#
# live_idnums = {}
# a dictionary contaiing the idnum for a certain client where the
# idnum is of those clients in current_players
#
# board = tiles.Board()
# the board object for the game
# '''
#
# '''
# Need functions to:
#
# 1. handle a client that just joined
# 3. track the turn of the client
# 4. start the game
# 5. check which client's turn it is at any given point
# 6. broardcast the messages to be sent to everyone
# 7. swap the next player's turn
# 8. handle the main game loop
# '''
