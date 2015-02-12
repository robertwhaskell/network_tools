import echo_client


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
            GET /fake/uri HTTP/1.1\r\nHost: localhost:50001\r\n
            """)
    okay_response = "HTTP/1.1 200 OK\r\n"
    headers = "Content-Type: text/plain\r\n"
    body = "you requested: /fake/uri"
    response = "{}{}{}\r\n".format(okay_response, headers, body)
    assert msg == response


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
            GET /path/to/index.html HTTP/1.0\r\nHost: localhost:50001\r\n
            """)
    error_response = "HTTP/1.1 505 ERROR\r\n"
    headers = "Content-Type: text/plain\r\n"
    body = "ERROR 505, HTTP/1.0 NOT SUPPORTED\r\n"
    response = "{}{}{}".format(error_response, headers, body)
    assert msg == response
