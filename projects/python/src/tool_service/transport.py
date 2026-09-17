"""按行收发，限制帧长度；EOF 与完整 JSON 消息分开处理。"""

from typing import BinaryIO

from .protocol import MAX_LINE


class FrameError(ValueError):
    pass


class IncompleteFrame(ConnectionError):
    pass


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
