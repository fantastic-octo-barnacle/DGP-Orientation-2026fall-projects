"""同步文字客户端。连接参考服务端时使用相同消息格式。"""

import argparse
import json
import socket
from typing import Any

from .protocol import MAX_ID, encode, reject_constant, validate_json_values
from .transport import read_frame


def build_request(choice: str, request_id: int, data: str = "") -> dict[str, Any]:
    if choice == "1":
        return {"id": request_id, "action": "ping"}
    if choice == "2":
        return {"id": request_id, "action": "echo", "data": data}
    raise ValueError("未知菜单选项")


def exchange(connection: socket.socket, reader: Any, request: dict[str, Any]) -> dict[str, Any]:
    connection.sendall(encode(request))
    frame = read_frame(reader)
    if frame is None:
        raise ConnectionError("服务端关闭了连接")
    try:
        response = json.loads(frame.decode("utf-8"), parse_constant=reject_constant)
        validate_json_values(response)
    except (ValueError, UnicodeError, RecursionError) as error:
        raise ValueError("响应必须是有效的 UTF-8 JSON") from error
    if not isinstance(response, dict):
        raise ValueError("响应必须是对象")
    response_id = response.get("id")
    if (
        type(response_id) is not int
        or not 0 <= response_id <= MAX_ID
        or response_id != request["id"]
    ):
        raise ValueError("响应 id 必须是与请求一致的整数")
    if type(response.get("ok")) is not bool:
        raise ValueError("响应 ok 必须是布尔值")
    if response["ok"]:
        if set(response) != {"id", "ok", "data"}:
            raise ValueError("成功响应必须恰有 id、ok 和 data 字段")
    else:
        error = response.get("error")
        if (
            set(response) != {"id", "ok", "error"}
            or not isinstance(error, dict)
            or set(error) != {"code", "message"}
            or not isinstance(error["code"], str)
            or not isinstance(error["message"], str)
        ):
            raise ValueError("错误响应必须包含 id、ok 和具有字符串 code/message 的 error")
    return response


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=7878)
    args = parser.parse_args()
    try:
        with socket.create_connection(("127.0.0.1", args.port), timeout=12) as connection:
            with connection.makefile("rb") as reader:
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
                    response = exchange(connection, reader, build_request(choice, request_id, data))
                    print(json.dumps(response, ensure_ascii=False))
                    request_id += 1
    except (OSError, ValueError, ConnectionError) as error:
        parser.exit(1, f"请求失败: {error}\n")
    except (EOFError, KeyboardInterrupt):
        print("\n客户端已退出。")


if __name__ == "__main__":
    main()
