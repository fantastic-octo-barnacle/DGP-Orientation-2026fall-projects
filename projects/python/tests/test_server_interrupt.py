import json
import queue
import socket
import subprocess
import sys
import threading
import time
from contextlib import ExitStack

import pytest


@pytest.mark.parametrize(
    "state", ["listening", "idle_connection", "partial_frame", "blocked_write"]
)
def test_pending_interrupt_stops_server(state):
    # 在线程中设置待处理的 SIGINT，模拟 Windows 阻塞 I/O 期间收到 Ctrl-C。
    program = """
import _thread
import sys
import threading
import socket
from tool_service import server

original = server.serve_connection
def serve(connection):
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024)
    original(connection)
server.serve_connection = serve

def interrupt():
    if sys.stdin.buffer.read(1):
        _thread.interrupt_main()

threading.Thread(target=interrupt, daemon=True).start()
sys.argv = ['rm-server', '--port', '0']
server.main()
"""
    process = subprocess.Popen(
        [sys.executable, "-X", "utf8", "-u", "-c", program],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    assert process.stdout is not None
    startup: queue.Queue[str] = queue.Queue()
    output = process.stdout
    threading.Thread(target=lambda: startup.put(output.readline()), daemon=True).start()
    try:
        line = startup.get(timeout=5)
        assert line.startswith("LISTENING "), line
        port = int(line.strip().rsplit(":", 1)[1])
        with ExitStack() as stack:
            if state != "listening":
                client = stack.enter_context(socket.socket())
                client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024)
                client.settimeout(2)
                client.connect(("127.0.0.1", port))
                reader = stack.enter_context(client.makefile("rb"))
                client.sendall(b'{"id":1,"action":"ping"}\n')
                assert json.loads(reader.readline())["data"] == "pong"
                if state == "partial_frame":
                    client.sendall(b'{"id":2,')
                if state == "blocked_write":
                    request = (
                        json.dumps({"id": 2, "action": "echo", "data": "x" * 60000}).encode()
                        + b"\n"
                    )

                    def flood():
                        try:
                            client.sendall(request * 20)
                        except OSError:
                            pass

                    sender = threading.Thread(target=flood, daemon=True)
                    sender.start()
                    time.sleep(0.3)
            stdout, stderr = process.communicate(input="x", timeout=3)
            assert process.returncode == 0, stderr
            assert "服务端已停止" in stdout
    finally:
        if process.poll() is None:
            process.kill()
            process.communicate(timeout=3)
