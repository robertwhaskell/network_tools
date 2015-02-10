import pytest
import socket


@pytest.fixture()
def set_up_client_socket(request):
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP
        )
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall("Hey, can you hear me?")
    buffersize = 32
    response = ''
    done = False
    while not done:
        msg_part = client_socket.recv(buffersize)
        if buffersize > response:
            done = True
            client_socket.close()
        response += msg_part
    print response
