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

SERVER_IP = ''
PORT_NUMBER = 30020
SERVER_ADDR = (SERVER_IP, PORT_NUMBER)

# # create a TCP/IP socket
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# # bind to the server address
# server_socket.bind(SERVER_ADDR)


class Server:

    def __init__(self, host_address, port_number):
        self.host = host_address
        self.port = port_number
        # self.number_of_threads = 4
        # self.thread_pool = [] # just a list of threads "in the pool"
        # self.task_queue = queue.Queue()

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

    '''
    A function to start the server.
    Implements a thread pool to support multiple concurrent clients
    on a single server
    '''
    def start_server(self):
        # server_socket.listen(5)
        # print('listening on {}'.format(sock.getsockname()))

        # create a TCP/IP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind to the server address: SERVER_ADDR = (SERVER_IP, PORT_NUMBER)
        server_socket.bind((self.host, self.port))

        # listen on the socket:
        server_socket.listen(5)
        print('listening on {}'.format(server_socket.getsockname()))

        while True:
          # connection = the client's own socket object
          # client_address = IP address of connecting client
          connection, client_address = server_socket.accept()

          # create a thread:
          thread = threading.Thread(
                target = self.client_handler,
                args = (connection, client_address) # ,
                # daemon = True
          )
          thread.start()
          print(f"[ACTIVE CONNECTIONS] {threading.activeCount()}")
          print('received connection from {}'.format(client_address))

    # print('listening on {}'.format(sock.getsockname()))

    # server_socket.listen(5)

    # while True:
    #   # handle each new connection independently
    #   connection, client_address = server_socket.accept()
    #   print('received connection from {}'.format(client_address))
    #   client_handler(connection, client_address)

server = Server(SERVER_IP, PORT_NUMBER)
print("[STARTING] Starting the server...")
server.start_server()
