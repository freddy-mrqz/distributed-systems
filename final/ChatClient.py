#! python

import socket
import sys
import getopt
import server_globals


def usage( script_name ):
    print('Usage: py ' + script_name + ' -l <client listening port number> ' +
          '-p <connect server port>')


def displayMenu():
    '''display menu options for client'''
    print('Enter an option(\'m\', \'f\', \'x\'):\n' +
          '  (M)essage (send)\n' +
          '  (F)ile (request)\n' +
          ' e(X)it')
    response = sys.stdin.readline().rstrip()
    return response


def createlisteningSocket(port):
    listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listensocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listensocket.bind(('', int(port)))
    listensocket.listen(1)
    return listensocket

def sendMessage(sock):
    '''send message to connected clients'''
    print('Enter your message: ')
    msg = sys.stdin.readline()
    if not msg:
        return None
    try:
        sock.send(msg.encode())
    except:
        return None
    return 1

def send_name(sock):
    '''sends and stores client name to server'''
    print('Waiting for request from server...')
    msg_bytes = sock.recv(1024)
    print(msg_bytes.decode())
    name = sys.stdin.readline().rstrip()
    print('Sending name to server...')
    sock.send(name.encode())
    print('Sending port ' + str(l_port) + ' to server...')
    sock.send(l_port.encode())

def requestFile(sock):
    print('Who owns the file?')
    owner = sys.stdin.readline().rstrip()
    sock.send(owner.encode())
    port = sock.recv(1024)
    print(str(owner) + ' lives in port ' + str(port))
    print('Which file do you want?')
    filename = sys.stdin.readline().rstrip()
    if not filename:
        return None
    RetrieveFile(owner, port, filename).start()
    return 1

if __name__ == "__main__":
    if len(sys.argv) != 5:
        usage(sys.argv[0])
        sys.exit()

    optlist, args = getopt.getopt(sys.argv[1:], 'l:p:')
    l_port = None
    c_port = None

    for opt, arg in optlist:
        if opt == '-l':
            l_port = arg
        if opt == '-p':
            c_port = arg

    if not l_port or not c_port:
        usage(sys.argv[0])
        sys.exit()

    # creates socket and connects to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', int(c_port)))
    send_name(sock)

    l_sock = createlisteningSocket(l_port)
    from file_request_listener import FileRequestListener
    FileRequestListener(l_sock).start()

    from recv_messages import RecvMessages
    RecvMessages(sock).start()

    from retrieve_file import RetrieveFile

    while True:
        option = displayMenu()
        if option == 'm':
            sock.send(option.encode())
            if not sendMessage(sock):
                break
        elif option == 'f':
            sock.send(option.encode())
            if not requestFile(sock):
                break
        elif option == 'x':
            break
        else:
            print('invalid choice')
    try:
        sock.shutdown(socket.SHUT_WR)
        sock.close()
    except:
        pass
