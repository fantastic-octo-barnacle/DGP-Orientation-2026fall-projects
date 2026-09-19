"""消息格式与基线动作。网络读写与业务处理分开。"""

import json
import math
from typing import Any

MAX_LINE = 65_536
MAX_ID = 9_007_199_254_740_991


def failure(request_id: int | None, code: str, message: str) -> dict[str, Any]:
    return {"id": request_id, "ok": False, "error": {"code": code, "message": message}}


def encode(message: dict[str, Any]) -> bytes:
    payload = json.dumps(message, ensure_ascii=False, allow_nan=False).encode("utf-8")
    if len(payload) > MAX_LINE:
        raise ValueError("message exceeds 65536 bytes")
    return payload + b"\n"


def handle(raw: bytes) -> dict[str, Any]:
    try:
        request = json.loads(raw.decode("utf-8"), parse_constant=reject_constant)
        validate_json_values(request)
    except (ValueError, UnicodeError, RecursionError):
        return failure(None, "invalid_json", "expected UTF-8 JSON")
    if not isinstance(request, dict):
        return failure(None, "invalid_request", "expected an object")
    request_id = request.get("id")
    if type(request_id) is not int or not 0 <= request_id <= MAX_ID:
        return failure(None, "invalid_request", "id must be a nonnegative safe integer")
    action = request.get("action")
    if not isinstance(action, str):
        return failure(request_id, "invalid_request", "action must be a string")
    fields = {
        "ping": {"id", "action"},
        "echo": {"id", "action", "data"},
        "text_stats": {"id", "action", "text"},
    }
    if action not in fields:
        return failure(request_id, "unknown_action", "action is not supported")
    if set(request) != fields[action]:
        return failure(request_id, "invalid_request", "missing or extra fields")
    if action == "ping":
        data: Any = "pong"
    elif action == "echo":
        if not isinstance(request["data"], str):
            return failure(request_id, "invalid_request", "data must be a string")
        data = request["data"]
    else:
        text = request["text"]
        if not isinstance(text, str):
            return failure(request_id, "invalid_request", "text must be a string")
        data = {"characters": len(text), "lines": 0 if text == "" else text.count("\n") + 1}
    return {"id": request_id, "ok": True, "data": data}


def reject_constant(value: str) -> None:
    raise ValueError(f"non-JSON number: {value}")


def validate_json_values(value: Any) -> None:
    if isinstance(value, str):
        value.encode("utf-8")
    elif isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite JSON number")
    elif isinstance(value, list):
        for item in value:
            validate_json_values(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            validate_json_values(key)
            validate_json_values(item)


def parse_response(frame: bytes, request_id: int) -> dict[str, Any]:
    """解析并校验与请求对应的响应。"""
    try:
        response = json.loads(frame.decode("utf-8"), parse_constant=reject_constant)
        validate_json_values(response)
    except (ValueError, UnicodeError, RecursionError) as error:
        raise ValueError("响应必须是有效的 UTF-8 JSON") from error
    if not isinstance(response, dict):
        raise ValueError("响应必须是对象")
    response_id = response.get("id")
    if type(response_id) is not int or not 0 <= response_id <= MAX_ID or response_id != request_id:
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
