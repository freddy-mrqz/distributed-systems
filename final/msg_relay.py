#!python

import threading
import server_globals

class MsgRelay(threading.Thread):
    def __init__(self, connection, name):
        threading.Thread.__init__(self)
        self.connection = connection
        self.name = name

    def run(self):
        while True:
            msg_bytes = self.connection.recv(1024)
            if len(msg_bytes):
                pass
            else:
                self.connection.close()
                server_globals.connections.remove(self.connection)
                break

            name_msg = str(self.name) + ': '
            for cur_connection in server_globals.connections:
                if cur_connection is not self.connection:
                    cur_connection.send(name_msg.encode())
                    cur_connection.send(msg_bytes)
