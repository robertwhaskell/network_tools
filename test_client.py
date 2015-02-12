import echo_client


def test_basic_entry():
    assert echo_client.start_client("Hello") == "Received message: Hello"


def test_long_entry():
    msg = echo_client.start_client("This message is longer than buffer")
    assert msg == "Received message: This message is longer than buffer"


def test_unicode_entry():
    msg = echo_client.start_client(unicode('Hello'))
    assert msg == "Received message: Hello"


def test_HTTP_okay():
    msg = echo_client.start_client("""
            GET /path/to/index.html HTTP/1.1\r\nHost: localhost:50001\r\n
            """)
    assert msg == """
            HTTP/1.1 200 OK\r\n
            Content-Type: text/plain\r\n
            you requested: /path/to/index.html\r\n
            """


def test_HTTP_method_error():
    msg = echo_client.start_client("""
            POST /path/to/index.html HTTP/1.1\r\nHost: localhost:50001\r\n
            """)
    assert msg == """
    "HTTP/1.1 405 ERROR\r\n
    Content-Type: text/plain\r\n
    body = "ERROR 405, POST METHOD NOT ALLOWED\r\n".
    """


def test_HTTP_version_error():
    msg = echo_client.start_client("""
            GET /path/to/index.html HTTP/1.0\r\nHost: localhost:50001\r\n
            """)
    assert msg == """
    "HTTP/1.1 505 ERROR\r\n
    Content-Type: text/plain\r\n
    body = "ERROR 505, HTTP/1.0 NOT SUPPORTED\r\n".
    """