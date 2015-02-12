import echo_client
import os

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


def test_HTTP_has_root():
    msg = echo_client.start_client("""
            GET webroot HTTP/1.0\r\nHost: localhost:50001\r\n
            """)
    okay_response = "HTTP/1.1 200 OK\r\n"
    headers = "Content-Type: text/html\r\n"
    body = """
    <h1>webroot</h1>
    <ul>
        <li>images</li>
        <li>a_web_page.html</li>
        <li>sample.txt</li>
    </ul>
        """
    response = "{}{}{}\r\n".format(okay_response, headers, body)
    assert msg == response


def test_HTTP_returns_webpage():
    msg = echo_client.start_client("""
            GET webroot/a_web_page.html HTTP/1.0\r\nHost: localhost:50001\r\n
            """)
    okay_response = "HTTP/1.1 200 OK\r\n"
    headers = "Content-Type: text/html\r\n"
    body = os.path('webroot/a_web_page')
    response = "{}{}{}\r\n".format(okay_response, headers, body)
    assert msg == response


def test_HTTP_returns_dynamic_error():
    error_response = "HTTP/1.1 400 ERROR\r\n"
    headers = "Content-Type: text/plain\r\n"
    body = "ERROR 400, BAD REQUEST\r\n"
    response = "{}{}{}".format(error_response, headers, body)

    request_list = ["""
            POST webroot HTTP/1.0\r\nHost: localhost:50001\r\n
            """, """
            GET webroot/non-thing HTTP/1.0\r\nHost: localhost:50001\r\n
            """, """
            GET webroot HTTP/500.0\r\nHost: localhost:50001\r\n
            """]
    for req in request_list:
        assert echo_client(req) != response
