import socket

buffersize = 8


def start_server():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP
        )
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)
    try:
        while True:
            conn, addr = server_socket.accept()
            done = False
            message = ""
            while not done:
                msg_part = conn.recv(buffersize)
                message = "{}{}".format(message, msg_part)
                if len(msg_part) < buffersize:
                    done = True
            conn.sendall("Received message: {0}".format(message))
            conn.close()
    except:
        server_socket.close()
        print "\nclosed server socket"
    finally:
        raise

if __name__ == '__main__':
    print start_server()
