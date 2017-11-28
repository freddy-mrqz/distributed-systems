 #freddy marquez-chairez
 #! python

 #messenger

def connectToServer(port, server):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if server:
        sock.connect((server, int(port)))
    else:
        sock.connect(('localhost', int(port)))
    return sock

def listenForConnection(port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('', int(port)))
    serversocket.listen(5)
    sock, addr = serversocket.accept()
    return sock

def usage( script_name ):
    print( 'Usage: py ' + script_name + '[-l]'+ ' <port number>' + '[<server address>]' )

#store command line argument
if __name__ == "__main__":
    import sys
    import socket
    import getopt

    argc= len( sys.argv )
    if argc < 2 or argc > 4:
        usage(sys.argv[0])
        sys.exit()

    optlist, non_option_args = getopt.getopt(sys.argv[1:], 'l')
    act_as_server= False

    for opt, arg in optlist:
        if opt == '-l':
            act_as_server= True

    host_args_len= len(non_option_args)

    port=non_option_args[0]

    server=None

    if host_args_len == 2:
        server=non_option_args[1]
    if act_as_server == True and server:
        oops(server);
        sys.exit()
    # if act_as_server == True:
    #     print('listening on port ' + port)
    # elif server == None:
    #     print('connecting to localhost on port ' + port)
    # else:
    #     print('connecting to ' + server + ' on port ' + port)

    if act_as_server:
        sock = listenForConnection(port)
    else:
        sock= connectToServer(port, server)

    from recv_messages import RecvMessages
    RecvMessages(sock).start()

    while True:

        sys.stdout.flush()
        message= sys.stdin.readline().rstrip()
        if not message:
            break

        try:
            sock.send(message.encode())
        except:
            sys.exit()

    try:
        sock.shutdown(socket.SHUT_WR)
        sock.close()
    except:
        pass
