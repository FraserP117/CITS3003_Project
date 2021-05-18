# CITS3002 2021 Assignment
#
# Full Name: Charles John Owens
# Student #: 22244175
#
# This code works for the following
# Multiple connections
# A connection after the game start
# Restarting a game
# Picking randomly 4 players for a game start
# Waiting for the new game to start to reflect on the old game
#
# This code does work for the following
# For a connection to play a move when it is not its turn
# A connection to exit during a game
# Any of tier 4

import socket
import sys
import queue
import time
import select
import tiles
import threading
import message
import random


class Server:

    # A server class that has a TCP/IP socket and handles everything game related
    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.turnQueue = queue.Queue(maxsize = 4) # the queue for the players




    #The main game loop
    def startGame(self):
        global started

        #The Start variable is the time the server waits for a game to start
        start = 10
        #Create a board
        board = tiles.Board()
        #The game loop
        while True:


            #Server uses the startTimer function that gives a delay
            print("A new game is about to start!")
            now = time.time()
            server.startTimer(now,start)

            #Reset everything in the server
            #This happens after the start timer so extra games can see what happened in the previous game before starting again
            server.resetState()
            board.reset()



            #The pickPlayers function updates the global variables that deal with current players
            liveIdNums = server.pickPlayers()

            #The game should now start
            started = 1

            #The function that handles the game playing
            server.gameStart(board,liveIdNums)

            print("This game is over!")



    #The resetState function is used to wipe all information clean
    def resetState(self):
        global allClients
        global moves
        global turnOrder
        global currentPlayers

        turnOrder = []
        moves = []
        currentPlayers =[]

        for i in allClients:
            i.connection.send(tiles.MessageGameStart().pack())

        server.turnQueue.queue.clear()


    #The pickPlayers function picks either 4 connections at random to be players or if there is less then 4 connections all of them
    def pickPlayers(self):
        global allClients
        global currentPlayers
        global turnOrder

        liveIdNums = []

        #The loop for picking at random
        while (len(currentPlayers)<4):

            choice = random.choice(allClients)
            #This conditional is used if the same client is picked twice
            if choice not in currentPlayers:
                turnOrder.append(choice)
                server.turnQueue.put(choice)
                currentPlayers.append(choice)
                liveIdNums.append(choice.idnum)
                #Used if there is less then 4 connections and all those connections are currently players
                if(len(currentPlayers)==len(allClients)):
                    break

        return liveIdNums


    #This function forces the game to wait until a new game start
    def startTimer(self,now,start):

        count = 0
        future = now + start
        #Everything in this while loop just is nice UI
        while time.time() < future:
            if time.time() > future - start +count:
                print("The game will start in: "+str(start - count))
                count = count + 1





    #The function that playes the game
    def gameStart(self,board,liveIdNums):

        global allClients
        global currentPlayers
        global moves
        global listening
        global started

        #Initializes all current players sends them welcome and their cards
        #Also informs all clients about the current players
        for i in currentPlayers:
            currentConnection = i.connection
            currentConnection.send(tiles.MessageWelcome(i.idnum).pack())


            for _ in range(tiles.HAND_SIZE):
                tileid = tiles.get_random_tileid()
                currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())

            for j in allClients:
                j.connection.send(tiles.MessagePlayerJoined(i.name,i.idnum).pack())


        buffer = bytearray()

        #Loop used to handle the game
        while len(liveIdNums)>1:

            current = self.turnQueue.get()
            currentIDnum = current.idnum
            #This if statement skips a players turn if they were eliminated
            if currentIDnum not in liveIdNums:
                continue

            currentConnection = current.connection
            currentAddress = current.clientAddress

            #Sends all players the current players turn start
            for i in allClients:
                i.connection.send(tiles.MessagePlayerTurn(currentIDnum).pack())


            chunk = currentConnection.recv(4096)

            if not chunk:
              print('#client {} disconnected'.format(address))
              continue


            buffer.extend(chunk)


            msg, consumed = tiles.read_message_from_bytearray(buffer)
            if not consumed:
                break

            buffer = buffer[consumed:]

            print('received message {}'.format(msg))


            #The two if statements to tell what type of move it was
            if isinstance(msg, tiles.MessagePlaceTile):

                #Moves is an array storing the moves in order to give to spectators
                moves.append(msg)

                if board.set_tile(msg.x, msg.y, msg.tileid, msg.rotation, msg.idnum):

                    for i in allClients:
                        i.connection.send(msg.pack())

                    positionupdates, eliminated = board.do_player_movement(liveIdNums)

                    for msg in positionupdates:
                        moves.append(msg)
                        for i in allClients:
                            i.connection.send(msg.pack())

                    for e in eliminated:
                        liveIdNums.remove(e)
                        for i in allClients:
                            i.connection.send(tiles.MessagePlayerEliminated(e).pack())

                    tileid = tiles.get_random_tileid()
                    currentConnection.send(tiles.MessageAddTileToHand(tileid).pack())

                self.turnQueue.put(current)

            #This if statement if a player choices his start position
            elif isinstance(msg, tiles.MessageMoveToken):

                if not board.have_player_position(msg.idnum):

                    if board.set_player_start_position(msg.idnum, msg.x, msg.y, msg.position):

                        positionupdates, eliminated = board.do_player_movement(liveIdNums)

                        for msg in positionupdates:
                            moves.append(msg)
                            for i in allClients:
                                i.connection.send(msg.pack())

                        for e in eliminated:
                            liveIdNums.remove(e)
                            for i in allClients:
                                i.connection.send(tiles.MessagePlayerEliminated(e).pack())

                    self.turnQueue.put(current)
        started = 0
        #The game is over and thus started isn't 1
        return



    #This function is used in the primary connection loop to bring any clients that join after a game starts up to speed
    def bringUpSpeed(self, client):
        global moves
        global turnOrder

        currentIdnum = client.idnum
        currentCon = client.connection

        currentCon.send(tiles.MessageWelcome(currentIdnum).pack())

        #We only need to tell the spectators of the current players not other spectators as they shouldn't send information
        for i in turnOrder:
            currentCon.send(tiles.MessagePlayerJoined(i.name,i.idnum).pack())
            currentCon.send(tiles.MessagePlayerTurn(i.idnum).pack())
        #Play all the moves in order
        for move in moves:
            currentCon.send(move.pack())




#Class to store all information needed about a client
class Client():
  def __init__(self,idnum, connection, address):
    self.idnum = idnum
    self.connection = connection
    self.clientAddress = address
    host, port = clientAddress
    self.name = '{}:{}'.format(host, port)
    self.buffer = bytearray()








# listen on all network interfaces
SERVER_IP = ''
PORT_NUMBER = 30020

#Creates the server and gets it to listen
server = Server()
server.serverSocket.bind((SERVER_IP, PORT_NUMBER))
server.serverSocket.listen(10)

print('listening from server {}'.format(server.serverSocket.getsockname()))

#An array of connections we are listening to
listening = [server.serverSocket]

#Global variables that are used throughout the games

#An array of every client currently connected
allClients = []

#An array of clients currently deemed players
currentPlayers = []

#A boolean that shows whether the game has started
started = 0

#A count to give each client a unique number
idnum = 0

#An array to store the moves that have been played in order to bring spectators up to speed
moves = []

#An array to store the order that players play there moves
turnOrder = []

#The loop that handles the game
while True:

    readable, writeable, exceptional = select.select(listening, [], listening)

    if server.serverSocket in readable:
        connection, clientAddress = server.serverSocket.accept() # connect the new client
        print(f"client joined with address: {clientAddress}")

        client = Client(idnum, connection, clientAddress)
        allClients.append(client)

        #If two clients join start the game thread
        if(len(allClients)==2):
                thread = threading.Thread(
                    target = server.startGame,
                    daemon = True
                )
                thread.start()


        listening.append(client.connection)

        #If the game has started the new client is a spectator
        if started == 1:
            server.bringUpSpeed(client)

        idnum += 1

        disconnectedClients = []

    if client.connection in exceptional:
        print('client {} exception'.format(client.address))
        disconnectedClients.append(client)
    
