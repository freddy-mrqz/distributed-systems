#! python



import threading
import os, sys

class RecvMessages(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client_socket= client_socket

    def run(self):
        while True:
            try:
                msg_bytes= self.client_socket.recv(2048)
            except:
                sys.exit()
            if len(msg_bytes):
                print(msg_bytes.decode(), end='')
            else:
                print('[other side closed socket, shutting down...]')
                self.client_socket.close()
                os._exit(0)
