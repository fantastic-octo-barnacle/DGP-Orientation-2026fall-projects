"""单线程同步服务端：一条连接可发送多条请求。"""

import argparse
import io
import socket

from .protocol import encode, failure, handle
from .transport import (
    FrameError,
    IncompleteFrame,
    SocketReader,
    read_frame,
    send_bytes,
    wait_for_input,
)


def serve_connection(connection: socket.socket) -> None:
    with io.BufferedReader(SocketReader(connection)) as reader:
        while True:
            try:
                frame = read_frame(reader)
            except FrameError:
                send_bytes(
                    connection, encode(failure(None, "line_too_long", "invalid frame boundary"))
                )
                return
            except IncompleteFrame:
                return
            if frame is None:
                return
            response = handle(frame)
            try:
                payload = encode(response)
            except ValueError:
                payload = encode(
                    failure(response["id"], "response_too_large", "response exceeds limit")
                )
            send_bytes(connection, payload)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=7878)
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("端口范围为 0–65535；0 表示自动分配端口")
    try:
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", args.port))
            listener.listen()
            print(f"LISTENING 127.0.0.1:{listener.getsockname()[1]}", flush=True)
            while True:
                wait_for_input(listener)
                connection, _ = listener.accept()
                with connection:
                    try:
                        serve_connection(connection)
                    except OSError as error:
                        print(f"连接结束: {error}", flush=True)
    except OSError as error:
        parser.exit(1, f"服务端启动或运行失败: {error}\n")
    except KeyboardInterrupt:
        print("\n服务端已停止。")


if __name__ == "__main__":
    main()
