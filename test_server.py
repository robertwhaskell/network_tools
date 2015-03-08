from echo_client import start_client
import pytest
from echo_server import *


def test_response_okay():
    assert response_ok() == "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"


def test_repsonse_error():
    assert response_error('666', 'test') == "HTTP/1.1 666 ERROR\r\nContent-Type: text/plain\r\n\r\nERROR 666, test\r\n"


def test_repsonse_error_method():
    assert response_error('405', 'METHOD NOT ALLOWED') == "HTTP/1.1 405 ERROR\r\nContent-Type: text/plain\r\n\r\nERROR 405, METHOD NOT ALLOWED\r\n"


def test_repsonse_error_protocol():
    assert response_error('505', 'PROTOCOL NOT SUPPORTED') == "HTTP/1.1 505 ERROR\r\nContent-Type: text/plain\r\n\r\nERROR 505, PROTOCOL NOT SUPPORTED\r\n"


def test_repsonse_error_request():
    assert response_error('400', 'BAD REQUEST') == "HTTP/1.1 400 ERROR\r\nContent-Type: text/plain\r\n\r\nERROR 400, BAD REQUEST\r\n"


def test_parse_request():
    assert parse_request("GET test HTTP/1.1") == "test"


def test_parse_request_bad_method():
    with pytest.raises(HTTPMethodNotAllowed):
        parse_request("PUT test HTTP/1.1")


def test_parse_request_bad_protocol():
    with pytest.raises(HTTPProtocolNotAccepted):
        parse_request("GET test HTTP/1.2")


def test_parse_request_bad_request():
    with pytest.raises(HTTPIvalidRequest):
        parse_request("")


def test_get_response():
    assert get_response('GET test HTTP/1.1') == "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\ntest\r\n"


def test_get_response_bad_method():
    assert get_response("PUT test HTTP/1.1") == "HTTP/1.1 405 ERROR\r\nContent-Type: text/plain\r\n\r\nERROR 405, METHOD NOT ALLOWED\r\n"


def test_get_response_bad_protocol():
    assert get_response("GET test HTTP/1.2") == "HTTP/1.1 505 ERROR\r\nContent-Type: text/plain\r\n\r\nERROR 505, PROTOCOL NOT SUPPORTED\r\n"


def test_get_response_bad_request():
    assert get_response("") == "HTTP/1.1 400 ERROR\r\nContent-Type: text/plain\r\n\r\nERROR 400, BAD REQUEST\r\n"


def test_echo_response():
    assert start_client('GET test HTTP/1.1') == "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\ntest\r\n"


def test_error_response_bad_method():
    assert start_client("PUT test HTTP/1.1") == "HTTP/1.1 405 ERROR\r\nContent-Type: text/plain\r\n\r\nERROR 405, METHOD NOT ALLOWED\r\n"


def test_with_client_bad_protocol():
    assert start_client("GET test HTTP/1.2\r\nhost:www.fakesite.com") == "HTTP/1.1 505 ERROR\r\nContent-Type: text/plain\r\n\r\nERROR 505, PROTOCOL NOT SUPPORTED\r\n"


def test_with_client_bad_method():
    assert start_client("PUT test HTTP/1.1\r\nhost:www.fakesite.com") == "HTTP/1.1 405 ERROR\r\nContent-Type: text/plain\r\n\r\nERROR 405, METHOD NOT ALLOWED\r\n"


def test_with_client_bad_request():
    assert start_client("") == "HTTP/1.1 400 ERROR\r\nContent-Type: text/plain\r\n\r\nERROR 400, BAD REQUEST\r\n"


def test_resolve_uri():
    assert resolve_uri('webroot') == (
        '<h1>webroot</h1><ul><li>a_web_page.html</li><li>images</li><li>make_time.py</li><li>sample.txt</li></ul>', 
        'text/html'
        )


def test_resolve_uri_with_bad_uri():
    with pytest.raises(IOError):
        resolve_uri("this is a bad uri")


def test_read_file_data_txt():
    assert read_file_data('webroot/a_web_page.html') == """<!DOCTYPE html>
<html>
<body>

<h1>North Carolina</h1>

<p>A fine place to spend a week learning web programming!</p>

</body>
</html>

"""


def test_generate_dir_html():
    assert generate_dir_html('webroot') == '<h1>webroot</h1><ul><li>a_web_page.html</li><li>images</li><li>make_time.py</li><li>sample.txt</li></ul>'


def test_generate_dir_html_nested_dir():
    assert generate_dir_html('webroot/images') == '<h1>webroot/images</h1><ul><li>JPEG_example.jpg</li><li>sample_1.png</li><li>Sample_Scene_Balls.jpg</li></ul>'


def test_with_client_webroot_request():
    assert start_client("GET webroot HTTP/1.1") == "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>webroot</h1><ul><li>a_web_page.html</li><li>images</li><li>make_time.py</li><li>sample.txt</li></ul>\r\n"


def test_with_client_file_html_request():
    assert start_client("GET webroot/a_web_page.html HTTP/1.1") == "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html>\n<html>\n<body>\n\n<h1>North Carolina</h1>\n\n<p>A fine place to spend a week learning web programming!</p>\n\n</body>\n</html>\n\n\r\n"


def test_with_client_file_txt_request():
    assert start_client("GET webroot/sample.txt HTTP/1.1") == "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nThis is a very simple text file.\nJust to show that we can server it up.\nIt is three lines long.\r\n"


def test_with_client_file_py_request(): 
    assert start_client("GET webroot/make_time.py HTTP/1.1") == 'HTTP/1.1 200 OK\r\nContent-Type: text/x-python\r\n\r\n#!/usr/bin/env python\n\n"""\nmake_time.py\n\nsimple script that returns and HTML page with the current time\n"""\n\nimport datetime\n\ntime_str = datetime.datetime.now().isoformat()\n\nhtml = """\n<http>\n<body>\n<h2> The time is: </h2>\n<p> %s <p>\n</body>\n</http>\n"""% time_str\n\nprint html'





