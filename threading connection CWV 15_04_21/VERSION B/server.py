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


'''
Traceback (most recent call last):
  File "server.py", line 675, in <module>
    live_id_nums = server.select_Players_From_Connected_Clients() # WE GET STUCK HERE
  File "server.py", line 166, in select_Players_From_Connected_Clients
    player_choice = random.choice(self.all_connected_clients) # self.all_connected_clients is empty !!!!!!!!!
  File "/usr/lib/python3.8/random.py", line 290, in choice
    raise IndexError('Cannot choose from an empty sequence') from None
IndexError: Cannot choose from an empty sequence


'''

# Full Name: Fraser Paterson
# Student Number: 22258324


import socket
import sys
import tiles
import threading
import queue
import time
import select
import message
import random

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
        self.message_queues = {}
        self.buffer = bytearray()

class Server:

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening = [self.server_socket]
        self.game_started = False # game has not started by default
        self.turn_Queue = queue.Queue(maxsize = 4) # the turn queue for the players
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


    def select_Spectators_From_Connected_Clients(self, live_id_nums):

        spectator_id_nums = []

        # select the spectator clients
        # select the spectator clients
        for a_connected_client in self.all_connected_clients:
            if a_connected_client.idnum not in live_id_nums:
                self.spectators.append(a_connected_client.idnum)

        return spectator_id_nums


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
    # def start_game(self, board, live_id_nums):  # take in live_id_nums ????????????????????????????????????????????????????????????????????????
    def start_game(self, board):  # take in live_id_nums ????????????????????????????????????????????????????????????????????????


        live_id_nums = []
        # live_id_nums = server.select_Players_From_Connected_Clients()
        print("sending Welcome messgae to all players")
        print("Adding tiles to each player's hand")
        for i in self.current_players:
            print("----------------------------------------------- HERE 1 ??? ----------------------------------------------- ")
            live_id_nums.append(i.idnum)
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

    def handle_late_spectator(self, client):

        currentIdnum = client.idnum
        currentCon = client.connection
        currentCon.send(tiles.MessageWelcome(currentIdnum).pack())
        for i in current_players:
            currentCon.send(tiles.MessagePlayerJoined(i.name,i.idnum).pack())
            currentCon.send(tiles.MessagePlayerTurn(i.idnum).pack())

        for move in self.game_message_history:
            currentCon.send(move.pack())
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
    server.start_game(board) # game starts now
    # server.reset_clients()
    # server.start_game(board, live_id_nums) # game starts now
