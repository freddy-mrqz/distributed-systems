#! python

import socket
import sys

def usage( script_name ):
    print( 'Usage: py ' + script_name + ' <port number>')

def send_name(sock):
    print('Wating for request from server...')
    msg_bytes = sock.recv(1024)
    print(msg_bytes.decode())
    name = sys.stdin.readline().rstrip()
    print('Sending name to server...')
    sock.send(name.encode())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage(sys.argv[0])
        sys.exit()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', int(sys.argv[1])))
    send_name(sock)

    from recv_messages import RecvMessages
    RecvMessages(sock).start()

    while True:
        message= sys.stdin.readline()
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
