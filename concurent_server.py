from echo_server import parse_request
from gevent.monkey import patch_all
from gevent.server import StreamServer


def echo(socket, address):
    buffsize = 8
    try:
        message = ""
        while True:
            data = socket.recv(buffsize)
            if data:
                message += data
            else:
                print message
                socket.sendall(parse_request(message))
                socket.close()
                break
    except:
        socket.close()
        raise


if __name__ == '__main__':
    patch_all()
    server = StreamServer(('127.0.0.1', 50001), echo)
    server.serve_forever()
