"""少量正常场景自查，不代替候选人的边界测试与客户端演示。"""

import argparse
import socket

from tool_service.client import exchange


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["baseline", "text", "numbers", "store"])
    parser.add_argument("--port", type=int, default=7878)
    args = parser.parse_args()
    with socket.create_connection(("127.0.0.1", args.port), timeout=12) as connection:
        with connection.makefile("rb") as reader:

            def call(request):
                result = exchange(connection, reader, request)
                assert result["ok"], result
                return result["data"]

            assert call({"id": 1, "action": "ping"}) == "pong"
            if args.stage == "baseline":
                assert call({"id": 2, "action": "echo", "data": "你好"}) == "你好"
            elif args.stage == "text":
                assert call({"id": 2, "action": "text_stats", "text": "hi\nRM"}) == {
                    "characters": 5,
                    "lines": 2,
                }
            elif args.stage == "numbers":
                data = call({"id": 2, "action": "number_stats", "numbers": [1, 2, 3]})
                assert data == {"count": 3, "min": 1, "max": 3, "mean": 2}
            else:
                call({"id": 2, "action": "set", "key": "__self_check__", "value": "robot"})
                assert call({"id": 3, "action": "get", "key": "__self_check__"}) == {
                    "value": "robot"
                }
                call({"id": 4, "action": "delete", "key": "__self_check__"})
    print(f"PASS: {args.stage} 正常场景；仍需核对 acceptance.md")


if __name__ == "__main__":
    main()
