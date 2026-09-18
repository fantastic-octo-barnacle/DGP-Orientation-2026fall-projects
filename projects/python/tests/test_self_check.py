import json
import socket
import subprocess
import sys
import threading
from pathlib import Path

import pytest


@pytest.mark.parametrize("business_error", [False, True])
def test_self_check_reports_expected_and_actual(business_error):
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        listener.settimeout(5)

        def server():
            connection, _ = listener.accept()
            with connection, connection.makefile("rb") as reader:
                connection.settimeout(5)
                for _ in range(2):
                    request = json.loads(reader.readline())
                    response = {"id": request["id"], "ok": True, "data": "pong"}
                    if request["action"] == "echo":
                        if business_error:
                            response = {
                                "id": request["id"],
                                "ok": False,
                                "error": {"code": "unknown_action", "message": "not implemented"},
                            }
                        else:
                            response["data"] = "wrong-result"
                    connection.sendall(json.dumps(response).encode() + b"\n")

        worker = threading.Thread(target=server, daemon=True)
        worker.start()
        result = subprocess.run(
            [
                sys.executable,
                "-X",
                "utf8",
                "self-check/check.py",
                "baseline",
                "--port",
                str(listener.getsockname()[1]),
            ],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=8,
        )
        worker.join(2)
        assert not worker.is_alive()
    assert result.returncode == 1
    assert "检查项: echo" in result.stderr
    assert "预期 data:" in result.stderr
    assert "实际响应:" in result.stderr
    assert ("unknown_action" if business_error else "wrong-result") in result.stderr
    assert "Traceback" not in result.stderr
