#! python

import sys
import socket
import server_globals


def usage( script_name ):
    print('Usage: py ' + script_name + ' <port number>')


def get_name(sock):
    print('Requesting name from client...')
    request= 'What is your name?'
    sock.send(request.encode())
    name_bytes = sock.recv(1024)
    name = name_bytes.decode()
    port_bytes = sock.recv(1024)
    port = port_bytes.decode()
    server_globals.ports[name] = port
    print(str(server_globals.ports[name]) + ' belongs to ' + str(name))
    for i in server_globals.ports:
        print(i, server_globals.ports[i])
    return name


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
        name = get_name(sock)
        option_bytes = sock.recv(1024)
        if option_bytes == 'm':
            MsgRelay(sock, name).start()
        elif option_bytes == 'f':
            name_bytes = sock.recv(1024)
            supplier_name = name_bytes.decode()
            port = server_globals.ports[supplier_name]
            sock.send(port.encode())
        else:
            pass
