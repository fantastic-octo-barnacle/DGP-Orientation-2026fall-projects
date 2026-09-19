import runpy
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from tool_service.client import exchange
from tool_service.transport import send_bytes


@pytest.mark.parametrize("use_self_check", [False, True])
def test_response_deadline_is_not_reset_by_fragments(use_self_check):
    client, peer = socket.socketpair()
    stop = threading.Event()

    def reply():
        try:
            peer.recv(4096)
            for part in [b'{"id":1,', b'"ok":true,', b'"data":', b'"pong"}', b"\n"]:
                if stop.wait(0.1):
                    return
                peer.sendall(part)
        except OSError:
            pass

    with client, peer:
        client.settimeout(2)
        peer.settimeout(2)
        worker = threading.Thread(target=reply, daemon=True)
        worker.start()
        try:
            with pytest.raises(TimeoutError):
                if use_self_check:
                    checker = runpy.run_path(
                        str(Path(__file__).resolve().parents[1] / "self-check/check.py")
                    )
                    with client.makefile("rb") as reader:
                        checker["exchange"](
                            client, reader, {"id": 1, "action": "ping"}, timeout=0.25
                        )
                else:
                    exchange(client, {"id": 1, "action": "ping"}, timeout=0.25)
        finally:
            stop.set()
            worker.join(2)
        assert not worker.is_alive()


def test_partial_sends_preserve_data():
    sender, receiver = socket.socketpair()
    payload = b"abcdefgh" * 65536
    received = bytearray()
    errors = []

    def read():
        try:
            time.sleep(0.3)
            while len(received) < len(payload):
                chunk = receiver.recv(8192)
                if not chunk:
                    break
                received.extend(chunk)
        except OSError as error:
            errors.append(error)

    with sender, receiver:
        sender.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024)
        sender.settimeout(2)
        receiver.settimeout(3)
        worker = threading.Thread(target=read, daemon=True)
        worker.start()
        send_bytes(sender, payload, timeout=3)
        worker.join(4)
        assert not worker.is_alive()
        assert not errors
        assert received == payload
        assert sender.gettimeout() == 2


@pytest.mark.parametrize(
    "entry", ["tool_service.client", "tool_service.server", "self-check/check.py"]
)
@pytest.mark.parametrize("port", ["-1", "70000"])
def test_invalid_port_is_an_argument_error(entry, port):
    command = [sys.executable, "-X", "utf8"]
    command += [entry, "baseline"] if entry.endswith(".py") else ["-m", entry]
    result = subprocess.run(
        command + ["--port", port], capture_output=True, text=True, encoding="utf-8", timeout=3
    )
    assert result.returncode == 2
    assert "端口范围" in result.stderr
    assert "Traceback" not in result.stderr


def test_occupied_port_reports_startup_error():
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        result = subprocess.run(
            [
                sys.executable,
                "-X",
                "utf8",
                "-m",
                "tool_service.server",
                "--port",
                str(listener.getsockname()[1]),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=3,
        )
    assert result.returncode == 1
    assert "服务端启动或运行失败" in result.stderr
    assert "Traceback" not in result.stderr
