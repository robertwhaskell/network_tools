import echo_client


def read_file_data(uri):
    with open(uri, 'r') as f:
        read_data = f.read()
    return read_data


def test_HTTP_bad_response_error():
    msg = echo_client.start_client("""
            Hello!
            """)
    error_response = "HTTP/1.1 400 ERROR\r\n"
    headers = "Content-Type: text/plain\r\n"
    body = "ERROR 400, BAD REQUEST\r\n"
    response = "{}{}{}".format(error_response, headers, body)
    assert msg == response


def test_HTTP_okay():
    msg = echo_client.start_client("""
            GET webroot HTTP/1.1\r\nHost: localhost:50001\r\n
            """)
    okay_response = "HTTP/1.1 200 OK\r\n"
    assert okay_response in msg


def test_HTTP_method_error():
    msg = echo_client.start_client("""
            POST /path/to/index.html HTTP/1.1\r\nHost: localhost:50001\r\n
            """)
    error_response = "HTTP/1.1 405 ERROR\r\n"
    headers = "Content-Type: text/plain\r\n"
    body = "ERROR 405, POST METHOD NOT ALLOWED\r\n"
    response = "{}{}{}".format(error_response, headers, body)
    assert msg == response


def test_HTTP_version_error():
    msg = echo_client.start_client("""
            GET webroot HTTP/1.0\r\nHost: localhost:50001\r\n
            """)
    error_response = "HTTP/1.1 505 ERROR\r\n"
    headers = "Content-Type: text/plain\r\n"
    body = "ERROR 505, HTTP/1.0 NOT SUPPORTED\r\n"
    response = "{}{}{}".format(error_response, headers, body)
    assert msg == response


def test_HTTP_has_root():
    msg = echo_client.start_client("""
            GET webroot HTTP/1.1\r\nHost: localhost:50001\r\n
            """)
    okay_response = "HTTP/1.1 200 OK\r\n"
    headers = "Content-Type: text/html\r\n"
    body = "<h1>webroot</h1><ul><li>a_web_page.html</li><li>images</li><li>make_time.py</li><li>sample.txt</li></ul>"
    response = "{}{}{}\r\n".format(okay_response, headers, body)
    assert msg == response


def test_HTTP_returns_webpage():
    msg = echo_client.start_client("""
            GET webroot/a_web_page.html HTTP/1.1\r\nHost: localhost:50001\r\n
            """)
    okay_response = "HTTP/1.1 200 OK\r\n"
    headers = "Content-Type: text/html\r\n"

    body = read_file_data('webroot/a_web_page.html')
    response = "{}{}{}\r\n".format(okay_response, headers, body)
    assert msg == response
