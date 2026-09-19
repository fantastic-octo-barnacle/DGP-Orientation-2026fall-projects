"""按行收发，限制帧长度；EOF 与完整 JSON 消息分开处理。"""

import io
import select
import socket
import time
from typing import Any, BinaryIO

from .protocol import MAX_LINE


class FrameError(ValueError):
    pass


class IncompleteFrame(ConnectionError):
    pass


def wait_for_input(connection: socket.socket, deadline: float | None = None) -> None:
    # Windows 的无限阻塞 socket 调用可能延迟处理 Ctrl-C。
    while True:
        remaining = 0.2 if deadline is None else min(0.2, deadline - time.monotonic())
        if remaining <= 0:
            raise TimeoutError("等待完整响应超时")
        if select.select([connection], [], [], remaining)[0]:
            return


def send_bytes(connection: socket.socket, payload: bytes, timeout: float | None = None) -> None:
    """按实际发送字节推进；等待期间可响应 Ctrl-C。"""
    original_timeout = connection.gettimeout()
    deadline = None if timeout is None else time.monotonic() + timeout
    connection.setblocking(False)
    try:
        pending = memoryview(payload)
        while pending:
            remaining = 0.2 if deadline is None else min(0.2, deadline - time.monotonic())
            if remaining <= 0:
                raise TimeoutError("发送请求超时")
            if not select.select([], [connection], [], remaining)[1]:
                continue
            try:
                sent = connection.send(pending)
            except BlockingIOError:
                continue
            if sent == 0:
                raise ConnectionError("连接已关闭")
            pending = pending[sent:]
    finally:
        connection.settimeout(original_timeout)


class SocketReader(io.RawIOBase):
    """定期处理退出信号，缓冲由外层 BufferedReader 管理。"""

    def __init__(self, connection: socket.socket, deadline: float | None = None) -> None:
        super().__init__()
        self.connection = connection
        self.deadline = deadline

    def readable(self) -> bool:
        return True

    def readinto(self, buffer: Any) -> int:
        if not buffer:
            return 0
        wait_for_input(self.connection, self.deadline)
        return self.connection.recv_into(buffer)


def read_frame(stream: BinaryIO) -> bytes | None:
    raw = stream.readline(MAX_LINE + 3)
    if not raw:
        return None
    if not raw.endswith(b"\n"):
        if len(raw) > MAX_LINE + 1:
            raise FrameError("oversized frame")
        raise IncompleteFrame("peer closed during a frame")
    payload = raw[:-1]
    if payload.endswith(b"\r"):
        payload = payload[:-1]
    if len(payload) > MAX_LINE:
        raise FrameError("oversized frame")
    return payload
