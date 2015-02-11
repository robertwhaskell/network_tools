import echo_client


def test_basic_entry():
    assert echo_client.start_client("Hello") == "Received message: Hello"


def test_long_entry():
    msg = echo_client.start_client("This message is longer than buffer")
    assert msg == "Received message: This message is longer than buffer"


def test_unicode_entry():
    msg = echo_client.start_client(unicode('Hello'))
    assert msg == "Received message: Hello"
