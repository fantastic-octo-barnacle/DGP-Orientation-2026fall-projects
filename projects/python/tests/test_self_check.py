import io
import json
import runpy
import shutil
import socket
import subprocess
import sys
import threading
from pathlib import Path

import pytest


@pytest.mark.parametrize("business_error", [False, True])
def test_self_check_reports_expected_and_actual(business_error, tmp_path):
    script = Path(__file__).resolve().parents[1] / "self-check/check.py"
    shutil.copyfile(script, tmp_path / "check.py")
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
                "-I",
                "-S",
                "-X",
                "utf8",
                "check.py",
                "baseline",
                "--port",
                str(listener.getsockname()[1]),
            ],
            cwd=tmp_path,
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


@pytest.mark.parametrize(
    "data, accepted",
    [
        ({"count": 3, "min": 1.0, "max": 3, "mean": 2.0000000001}, True),
        ({"count": 3, "min": 1, "max": 3, "mean": 2.01}, False),
        ({"count": 3, "min": True, "max": 3, "mean": 2}, False),
        ({"count": 3.0, "min": 1, "max": 3, "mean": 2}, False),
        ({"count": 3, "min": 1, "max": 3, "mean": float("nan")}, False),
        ({"count": 3, "min": 1, "max": 3, "mean": float("inf")}, False),
        ({"count": 3, "min": 1, "max": 3, "mean": 10**400}, False),
        ({"count": 3, "min": 1, "max": 3}, False),
        ({"count": 3, "min": 1, "max": 3, "mean": 2, "extra": 0}, False),
    ],
)
def test_number_self_check_uses_protocol_types_and_tolerance(data, accepted):
    script = Path(__file__).resolve().parents[1] / "self-check/check.py"
    check_case = runpy.run_path(str(script))["check_case"]
    request = {"id": 2, "action": "number_stats", "numbers": [1, 2, 3]}
    expected = {"count": 3, "min": 1, "max": 3, "mean": 2}
    frame = json.dumps({"id": 2, "ok": True, "data": data}).encode() + b"\n"
    client, peer = socket.socketpair()
    with client, peer:
        if accepted:
            check_case(client, io.BytesIO(frame), request, expected)
        else:
            with pytest.raises(ValueError, match="实际响应"):
                check_case(client, io.BytesIO(frame), request, expected)
