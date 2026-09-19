"""少量正常场景自查，不代替候选人的边界测试与客户端演示。"""

import argparse
import io
import json
import math
import socket
import time
from typing import Any

# 自查只依赖标准库和公开协议，候选人可自由调整项目内部结构。
MAX_LINE = 65_536


def exchange(
    connection: socket.socket,
    reader: io.BufferedIOBase,
    request: dict[str, Any],
    timeout: float = 12,
) -> dict[str, Any]:
    connection.sendall(
        json.dumps(request, ensure_ascii=False, allow_nan=False).encode("utf-8") + b"\n"
    )
    deadline = time.monotonic() + timeout
    original_timeout = connection.gettimeout()
    raw = b""
    try:
        while not raw.endswith(b"\n") and len(raw) < MAX_LINE + 3:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("等待完整响应超时")
            connection.settimeout(remaining)
            chunk = reader.read1(MAX_LINE + 3 - len(raw))
            if not chunk:
                break
            raw += chunk
    finally:
        connection.settimeout(original_timeout)
    if not raw.endswith(b"\n"):
        raise ValueError("未收到完整响应行")
    frame = raw[:-1].removesuffix(b"\r")
    if len(frame) > MAX_LINE:
        raise ValueError("响应超过 65536 字节")
    try:
        response = json.loads(frame.decode("utf-8"))
    except (ValueError, UnicodeError, RecursionError) as error:
        raise ValueError("响应不是有效的 UTF-8 JSON") from error
    if (
        not isinstance(response, dict)
        or type(response.get("id")) is not int
        or response["id"] != request["id"]
        or type(response.get("ok")) is not bool
    ):
        raise ValueError(f"响应格式或 id 错误: {response!r}")
    fields = {"id", "ok", "data"} if response["ok"] else {"id", "ok", "error"}
    if set(response) != fields:
        raise ValueError(f"响应字段错误: {response!r}")
    return response


def matches(actual: Any, expected: Any) -> bool:
    """普通结果逐字段检查类型和值，避免将布尔值当成整数。"""
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            matches(actual[key], value) for key, value in expected.items()
        )
    return actual == expected


def matches_numbers(actual: Any, expected: dict[str, Any]) -> bool:
    if not isinstance(actual, dict) or actual.keys() != expected.keys():
        return False
    if type(actual["count"]) is not int or actual["count"] != expected["count"]:
        return False
    for key in ("min", "max", "mean"):
        value = actual[key]
        if type(value) not in (int, float):
            return False
        try:
            if not math.isfinite(value) or not math.isclose(
                value, expected[key], rel_tol=1e-9, abs_tol=1e-12
            ):
                return False
        except OverflowError:
            return False
    return True


def check_case(
    connection: socket.socket,
    reader: io.BufferedIOBase,
    request: dict[str, Any],
    expected: Any,
) -> None:
    label = request["action"]
    details = (
        f"检查项: {label}\n"
        f"请求: {json.dumps(request, ensure_ascii=False)}\n"
        f"预期 data: {json.dumps(expected, ensure_ascii=False)}"
    )
    try:
        response = exchange(connection, reader, request)
    except (OSError, ValueError) as error:
        raise ValueError(f"{details}\n收发失败: {error}") from error
    compare = matches_numbers if label == "number_stats" else matches
    if not response["ok"] or not compare(response["data"], expected):
        raise ValueError(f"{details}\n实际响应: {json.dumps(response, ensure_ascii=False)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["baseline", "text", "numbers", "store"])
    parser.add_argument("--port", type=int, default=7878)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("端口范围为 1–65535")
    try:
        with socket.create_connection(("127.0.0.1", args.port), timeout=12) as connection:
            with connection.makefile("rb") as reader:
                check_case(connection, reader, {"id": 1, "action": "ping"}, "pong")
                if args.stage == "baseline":
                    check_case(
                        connection, reader, {"id": 2, "action": "echo", "data": "你好"}, "你好"
                    )
                elif args.stage == "text":
                    check_case(
                        connection,
                        reader,
                        {"id": 2, "action": "text_stats", "text": "hi\nRM"},
                        {"characters": 5, "lines": 2},
                    )
                elif args.stage == "numbers":
                    check_case(
                        connection,
                        reader,
                        {"id": 2, "action": "number_stats", "numbers": [1, 2, 3]},
                        {"count": 3, "min": 1, "max": 3, "mean": 2},
                    )
                else:
                    check_case(
                        connection,
                        reader,
                        {"id": 2, "action": "set", "key": "__self_check__", "value": "robot"},
                        {},
                    )
                    check_case(
                        connection,
                        reader,
                        {"id": 3, "action": "get", "key": "__self_check__"},
                        {"value": "robot"},
                    )
                    check_case(
                        connection,
                        reader,
                        {"id": 4, "action": "delete", "key": "__self_check__"},
                        {},
                    )
    except (OSError, ValueError) as error:
        parser.exit(
            1,
            f"FAIL: {args.stage}\n{error}\n"
            "请核对服务端、端口和当前阶段；若连接超时，先退出占用服务端的交互客户端。\n",
        )
    print(f"PASS: {args.stage} 正常场景；仍需核对 acceptance.md")


if __name__ == "__main__":
    main()
