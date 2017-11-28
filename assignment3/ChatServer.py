#! python

import sys
import socket
import server_globals

def usage( script_name ):
    print( 'Usage: py ' + script_name + ' <port number>')

if __name__ == "__main__":

    from msg_relay import MsgRelay
    if len(sys.argv) != 2:
        usage(sys.argv[0])
        sys.exit()

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('localhost', int(sys.argv[1])))
    serversocket.listen(5)
    print('Waiting for connections on port ' + sys.argv[1] + '...')

    while True:
        sock, addr = serversocket.accept()
        server_globals.connections.append(sock)
        MsgRelay(sock).start()
