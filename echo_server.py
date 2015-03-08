import socket
import os
import mimetypes

BUFFERSIZE = 8


class HTTPMethodNotAllowed(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class HTTPProtocolNotAccepted(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class HTTPIvalidRequest(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


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
                msg_part = conn.recv(BUFFERSIZE)
                message = "{}{}".format(message, msg_part)
                if len(msg_part) < BUFFERSIZE:
                    done = True

            conn.sendall(get_response(message))
            conn.close()

    except:
        server_socket.close()
        print "\nclosed server socket"
    finally:
        raise


def response_ok():
    okay_response = "HTTP/1.1 200 OK\r\n"
    headers = "Content-Type: text/plain\r\n\r\n"
    return "{}{}".format(okay_response, headers)


def response_error(error_num, error_msg):
    error_response = "HTTP/1.1 {} ERROR\r\n".format(error_num)
    headers = "Content-Type: text/plain\r\n\r\n"
    body = "ERROR {}, {}\r\n".format(error_num, error_msg)
    return "{}{}{}".format(error_response, headers, body)


def parse_request(request):
    try:
        req_list = request.splitlines()[0].split(' ')
    except IndexError:
        raise HTTPIvalidRequest('invalid request')
    if len(req_list) != 3:
        raise HTTPIvalidRequest('request needs exactly 3 parts: GET, uri, protocol')
    if req_list[0] != 'GET':
        raise HTTPMethodNotAllowed('not a GET request')
    if req_list[2] != 'HTTP/1.1':
        raise HTTPProtocolNotAccepted('protocol not supported')
    return req_list[1]


def get_response(message):
    try:
        uri = parse_request(message)
        response = "{}{}\r\n".format(response_ok(), uri)
    except HTTPMethodNotAllowed:
        response = response_error('405', 'METHOD NOT ALLOWED')
    except HTTPProtocolNotAccepted:
        response = response_error('505', 'PROTOCOL NOT SUPPORTED')
    except HTTPIvalidRequest:
        response = response_error('400', 'BAD REQUEST')
    return response


def resolve_uri(uri):
    if os.path.isdir(uri):
        return (generate_dir_html(uri), 'text/html')
    return (read_file_data(uri), mimetypes.guess_type(uri)[0])


def read_file_data(uri):
    read_data = ""
    with open(uri, 'r') as f:
        read_data = f.read()
    return read_data


def generate_dir_html(uri):
    dirname = "<h1>{}</h1>".format(uri)
    items_in_dir = "<ul>"
    for item in os.listdir(uri):
        items_in_dir = "{}<li>{}</li>".format(items_in_dir, item)
    items_in_dir = "{}</ul>".format(items_in_dir)
    return "{}{}".format(dirname, items_in_dir)

if __name__ == '__main__':
    print start_server()
