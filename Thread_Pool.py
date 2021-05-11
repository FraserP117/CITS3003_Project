import threading
import socket
import queue

'''
How use threads with sockets. Method uses a thread pool.

Use this with Basic_Client.py
'''

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.number_of_threads = 4
        self.thread_pool = [] # just a list of threads "in the pool"
        self.task_queue = queue.Queue()

    '''
    This is essentially a task that we want a thread to exec.
    '''
    def worker(self):
        while True:
            connection, msg = self.task_queue.get()
            recieved_data = connection.recv(1024)
            if recieved_data:
                print(recieved_data)
                connection.sendall(msg.encode())
            self.task_queue.task_done()

    def start(self):
        for i in range(self.number_of_threads):
            thread = threading.Thread(
                target = self.worker,
                daemon = True
            )
            thread.start()
            self.thread_pool.append(thread)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen()

        j = 0
        while True:
            connection, address = sock.accept()
            if j % 2 == 0:
                self.task_queue.put(
                    (connection, "I don't want to talk, please leave")
                )
            else:
                self.task_queue.put(
                    (connection, "STAAP bothering me!")
                )
            j += 1

server = Server("localhost", 6969)
server.start()

if __name__ == '__main__':
    main()
