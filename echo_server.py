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


def response_ok(uri):

    pass


def response_error(error_num, error_msg):
    pass


def parse_request(request):
    request_list = request.split()
    if check_for_errors(request_list) == "Good to go!":
        response_ok(request_list[1])


def check_for_errors(request):
    if request[0] != 'GET':
        response_error('405', '{} METHOD NOT ALLOWED'.format(request[0]))
        return
    if request[2] != 'HTTP/1.1':
        response_error('505', '{} NOT SUPPORTED'.format(request[2]))
        return
    return "Good to go!"
    # if errors exist, call response_error.
    # otherwise, return true


if __name__ == '__main__':
    print start_server()
