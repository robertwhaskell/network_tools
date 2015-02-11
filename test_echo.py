import pytest
import echo_client
import echo_server


def test_client_basic():
    assert echo_client.start_client("Hello") == "Received message: Hello"


def test_server_keyboard():
    assert echo_server.start_server() == "closed server socket"
