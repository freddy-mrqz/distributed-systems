#! python

import threading
import os, sys, socket

class RetrieveFile(threading.Thread):
    def __init__(self, owner, port, filename):
        threading.Thread.__init__(self)
        self.owner = owner
        self.port = port
        self.filename = filename

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', int(self.port)))

        try:
            sock.send(self.filename.encode())
        except:
            sys.exit()

        file = open(self.filename, 'wb')
        while True:
            try:
                file_bytes = sock.recv(2048)
            except:
                break
            if len(file_bytes):
                file.write(file_bytes)
            else:
                sock.close()
                break
        file.close()
