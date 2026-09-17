import io
import socket
import threading

import pytest

from tool_service.client import build_request, exchange
from tool_service.protocol import encode, handle
from tool_service.server import serve_connection
from tool_service.transport import FrameError, read_frame


def test_protocol_and_text():
    assert handle(encode({"id": 1, "action": "ping"}))["data"] == "pong"
    assert handle(encode({"id": 2, "action": "echo", "data": "你好"}))["data"] == "你好"
    response = handle(encode({"id": 3, "action": "text_stats", "text": "hi\nRM"}))
    assert response["data"] == {"characters": 5, "lines": 2}
    assert handle(encode({"id": 4, "action": "text_stats", "text": ""}))["data"]["lines"] == 0


def test_existing_error_contract():
    assert handle(b"{")["error"]["code"] == "invalid_json"
    assert handle(encode({"id": True, "action": "ping"}))["error"]["code"] == "invalid_request"
    assert handle(encode({"id": 1, "action": "missing"}))["error"]["code"] == "unknown_action"
    assert handle(encode({"id": 1, "action": "ping", "x": 1}))["error"]["code"] == "invalid_request"


def test_frame_boundaries():
    assert read_frame(io.BytesIO(b"{}\r\n")) == b"{}"
    assert read_frame(io.BytesIO(b"")) is None
    with pytest.raises(FrameError):
        read_frame(io.BytesIO(b"x" * 65537 + b"\n"))


def test_real_connection_multiple_requests():
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()

        def server():
            connection, _ = listener.accept()
            with connection:
                serve_connection(connection)

        worker = threading.Thread(target=server, daemon=True)
        worker.start()
        with socket.create_connection(listener.getsockname(), timeout=2) as client:
            with client.makefile("rb") as reader:
                assert exchange(client, reader, build_request("1", 1))["data"] == "pong"
                client.sendall(b"{\n")
                assert b"invalid_json" in reader.readline()
                assert exchange(client, reader, build_request("2", 2, "again"))["data"] == "again"
        worker.join(2)
        assert not worker.is_alive()
