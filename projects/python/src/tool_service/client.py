"""同步文字客户端。连接参考服务端时使用相同消息格式。"""

import argparse
import io
import json
import socket
import time
from typing import Any

from .protocol import encode, parse_response
from .transport import SocketReader, read_frame, send_bytes


def build_request(choice: str, request_id: int, data: str = "") -> dict[str, Any]:
    if choice == "1":
        return {"id": request_id, "action": "ping"}
    if choice == "2":
        return {"id": request_id, "action": "echo", "data": data}
    raise ValueError("未知菜单选项")


def exchange(
    connection: socket.socket, request: dict[str, Any], timeout: float = 12
) -> dict[str, Any]:
    send_bytes(connection, encode(request), timeout)
    # 协议逐请求收发，当前响应结束后才发送下一条请求。
    deadline = time.monotonic() + timeout
    with io.BufferedReader(SocketReader(connection, deadline)) as reader:
        frame = read_frame(reader)
    if frame is None:
        raise ConnectionError("服务端关闭了连接")
    return parse_response(frame, request["id"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=7878)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("端口范围为 1–65535")
    try:
        with socket.create_connection(("127.0.0.1", args.port), timeout=12) as connection:
            request_id = 1
            while True:
                print("1: ping  2: echo  q: 退出")
                choice = input("> ").strip()
                if choice == "q":
                    return
                if choice not in {"1", "2"}:
                    print("请选择 1、2 或 q")
                    continue
                data = input("内容: ") if choice == "2" else ""
                response = exchange(connection, build_request(choice, request_id, data))
                print(json.dumps(response, ensure_ascii=False))
                request_id += 1
    except (OSError, ValueError, ConnectionError) as error:
        parser.exit(1, f"请求失败: {error}\n")
    except (EOFError, KeyboardInterrupt):
        print("\n客户端已退出。")


if __name__ == "__main__":
    main()
