#! python

import threading
import os, sys

class FileRequestListener(threading.Thread):
    def __init__(self, serversocket):
        threading.Thread.__init__(self)
        self.serversocket= serversocket

    def run(self):
        while True:
            try:
                sock, addr =self.serversocket.accept()
                filename = sock.recv(2048).decode()
                print('received request for file: ' + filename)
                file_stat = os.stat(filename)
                if file_stat.st_size:
                    file = open(filename, 'rb')
                    while True:
                        file_bytes = file.read(2048)
                        if file_bytes:
                            sock.send(file_bytes)
                        else:
                            break
                    file.close()
                else:
                    pass
                sock.close() # Close the connection
            except OSError:
                pass
