"""少量正常场景自查，不代替候选人的边界测试与客户端演示。"""

import argparse
import json
import socket
from typing import Any, BinaryIO

from tool_service.client import exchange


def check_case(
    connection: socket.socket,
    reader: BinaryIO,
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
    if not response["ok"] or response["data"] != expected:
        raise ValueError(f"{details}\n实际响应: {json.dumps(response, ensure_ascii=False)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["baseline", "text", "numbers", "store"])
    parser.add_argument("--port", type=int, default=7878)
    args = parser.parse_args()
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
