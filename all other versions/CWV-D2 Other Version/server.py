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

# CWV Other 15/04/21 12:20 pm

import socket
import sys
import tiles
import threading
import queue
import time
import select
import message
import random

# need this ? fairly sure it does nothing
# start = -1
class Server:

    # def __init__(self, host_address, port_number):
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.turn_Queue = queue.Queue(maxsize = 4) # the queue for the players
        self.spectators = [] # the queue of spectators
        self.game_started = False # game has not started by default

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


    #the main game loop
    def startGame(self):
        start = 5
        print("maybe")

        while True:
            board = tiles.Board()
            print("Game is about to start!")
            now = time.time()
            server.startTimer(now,start)

            print("up to startgame")
            print("we got here")
            #new players
            live_id_nums = server.pickPlayers()

            server.gameStart(board)
            print("the game finished plsss")
            #rese
            start = 10
            #board.reset()
            #board = server.resetState(board)

            #

    def resetState(self,board):
        print("reset")
        global all_clients
        for i in all_clients:
            print(i.idnum)
        print("reset")
        return board.reset()

    def pickPlayers(self):
        global all_clients
        global current_players
        live_id_nums = []
        current_players =[]#just in case theres anything left in there
        while (len(current_players)<4):
            choice = random.choice(all_clients)
            if choice not in current_players:
                current_players.append(choice)
                live_id_nums.append(choice.idnum)
                if(len(current_players)==len(all_clients)):
                    break

        #
        return live_id_nums
        #

    # this conection is the client connection?
    def startTimer(self,now,start):
        global started
        count = 0

    def gameStart(self,board):
        global all_clients
        global current_players
        global started
        global started
        live_id_nums = []
        for i in current_players:
            live_id_nums.append(i.idnum)
            currentConnection = i.connection
            currentConnection.send(tiles.MessageWelcome(i.idnum).pack())

            #step 4

            for _ in range(tiles.HAND_SIZE):
                tileid = tiles.get_random_tileid()
                currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())

            for j in all_clients:
                print(i.name)
                j.connection.send(tiles.MessagePlayerJoined(i.name,i.idnum).pack())
        started = 1
        #main game loop
        buffer = bytearray()

        while len(live_id_nums)>1: #step 5
            print("start")
            current = self.turn_Queue.get()
            current_idnum = current.idnum
            print(current_idnum)
            current_connection = current.connection
            current_address = current.client_address
            print("here")
            for i in all_clients:
                #step 5 a
                i.connection.send(tiles.MessagePlayerTurn(current_idnum).pack())
            print("here1")

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
                    for i in all_clients:
                        i.connection.send(msg.pack())
                start_game    positionupdates, eliminated = board.do_player_movement(live_id_nums)

                    for msg in positionupdates:
                        for i in all_clients:
                            i.connection.send(msg.pack())
                    print("gothere")
                    for e in eliminated:
                        live_id_nums.remove(e)
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


        future = now + start
        #print("here")
        while time.time() < future:
            if time.time() > future - start +count:
                print("The game will start in: "+str(start - count))
                count = count + 1
        print("here")
        started = 1


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
        global current_players
        current_players = []
        #some form of check all  "all_clients" are still connected
        global all_clients

        while (len(current_players)<4):
            choice = random.choice(all_clients)
            if choice not in current_players:
                current_players.append(choice)
                if(len(current_players)==len(all_clients)):
                    break
               #and not (len(all_clients)==len(current_players)):
        #all_players_ids = [all_clients]
        for i in all_clients:
            print(i.idnum)
        print("here")
        print("pie")

class Client():
  """This class stores one client connection, the address of the client,
  and a buffer of bytes that we have received from the client but not yet
  processed.
  """
  def __init__(self,idnum, connection, address):
    self.idnum = idnum
    self.connection = connection
    self.client_address = address
    host, port = client_address
    self.name = '{}:{}'.format(host, port)
    self.message_queues = {} # a dictionary of message queues for all in all_clients
    self.buffer = bytearray()


# the turn queue for the "playing" players
# turn_Queue = queue.Queue(maxsize = 4)


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
current_players = []
now = -1
all_idnums_on_the_turn_queue = []
all_idnums_on_the_spec_queue = []
started = -1
idnum = 0
live_idnums = {}

# live_idnums = [idnum]
print("ONE")
while True:

    readable, writeable, exceptional = select.select(listening, [], listening)

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

        # store the info of the "just-then-conected" client:
        host, port = client_address
        name = '{}:{}'.format(host, port)
        client = Client(idnum, connection, client_address)
        all_clients.append(client)
        if(started == -1 and len(all_clients)>1):
                # print("started has been changed")
                print("starting the game now")

                started == 0
                thread = threading.Thread(
                    #target = server.cew,#server.client_handler,
                    target = server.startGame,
                    #args = (started, ),
                    #args = (now, ),#client.connection, client.client_address),
                    daemon = True
                )
                thread.start()

        listening.append(client.connection)

        if server.turn_Queue.qsize() < 4 and started != 1:
            server.turn_Queue.put(client) # put the newely connected client on the turn
            current_players.append(client)
            live_idnums.update({idnum:client})


        elif server.turn_Queue.qsize() == 4 or started ==1:
            # make all subequent connecting clients, spectators of the game:
            server.spectators.append(idnum)
        else:
            print("Sorry! that's all we can allow on the server i'm affraid!")
        print("SIX")


        idnum += 1
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
        #print(client.connection)
        print("NINE AND A HALF")

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
        print("ELEVEN")

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
        print("SEVENTEEN")
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
#                     server.send_message_to_all_clients(message.Message(printmsg))
#                 else:
#                     print("TWENTYONE")
#                     break

        print("TWENTYTWO")
        # remove any disconnected clients
#         for client in disconnected_clients:
#             print("TWENTYTHREE")
#             server.remove_client(client)
