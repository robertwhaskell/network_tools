import socket
import sys


def start_client(message=""):
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP
        )
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall(message)
    client_socket.shutdown(socket.SHUT_WR)
    buffersize = 32
    response = ''
    done = False
    while not done:
        msg_part = client_socket.recv(buffersize)
        if buffersize > len(msg_part):
            done = True
            client_socket.close()
        response += msg_part
    return response


if __name__ == '__main__':
    print start_client(sys.argv[1])
