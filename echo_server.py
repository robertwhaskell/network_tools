import socket

buffersize = 8


def start_server():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP
        )
    server_socket.bind(('127.0.0.1', 50001))
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
    okay_response = "HTTP/1.1 200 OK\r\n"
    headers = "Content-Type: text/plain\r\n"
    body = "you requested: {}".format(uri)
    return "{}{}{}\r\n".format(okay_response, headers, body)


def response_error(error_num, error_msg):
    error_response = "HTTP/1.1 {} ERROR\r\n".format(error_num)
    headers = "Content-Type: text/plain\r\n"
    body = "ERROR {}, {}\r\n".format(error_num, error_msg)
    return "{}{}{}".format(error_response, headers, body)


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
