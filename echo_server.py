import socket
import os
import mimetypes

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
            response = parse_request(message)
            try:
                conn.sendall(response)
            except TypeError:
                conn.sendall(response_error('400', 'BAD REQUEST'))
            conn.close()
    except:
        server_socket.close()
        print "\nclosed server socket"
    finally:
        raise


def response_ok(uri, body_and_type):
    okay_response = "HTTP/1.1 200 OK\r\n"
    headers = "Content-Type: {}\r\n".format(body_and_type[1])
    body = "{}".format(body_and_type[0])
    return "{}{}{}\r\n".format(okay_response, headers, body)


def response_error(error_num, error_msg):
    error_response = "HTTP/1.1 {} ERROR\r\n".format(error_num)
    headers = "Content-Type: text/plain\r\n"
    body = "ERROR {}, {}\r\n".format(error_num, error_msg)
    return "{}{}{}".format(error_response, headers, body)


def parse_request(request):
    request_list = request.split()
    error_check = check_for_errors(request_list)
    if error_check == "Good to go!":
        body_and_type = resolve_uri(request_list[1])
        return response_ok(request_list[1], body_and_type)
    return error_check


def check_for_errors(request):
    if len(request) < 5:
        return response_error('400', 'BAD REQUEST')
    if request[0] != 'GET':
        return response_error('405', '{} METHOD NOT ALLOWED'.format(request[0]))
    if not os.path.exists(request[1]):
        return response_error('404', 'NOT FOUND')
    if request[2] != 'HTTP/1.1':
        return response_error('505', '{} NOT SUPPORTED'.format(request[2]))
    return "Good to go!"


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
