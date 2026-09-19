import json

import pytest

from tool_service.protocol import parse_response


def read_response(raw):
    return parse_response(raw, 1)


@pytest.mark.parametrize(
    "response",
    [
        {"id": True, "ok": True, "data": "pong"},
        {"id": 1.0, "ok": True, "data": "pong"},
        {"id": None, "ok": True, "data": "pong"},
        {"id": 2, "ok": True, "data": "pong"},
        {"id": 1, "ok": "yes", "data": "pong"},
        {"id": 1, "ok": 1, "data": "pong"},
        {"id": 1, "ok": True},
        {"id": 1, "ok": True, "data": "pong", "extra": 1},
        {"id": 1, "ok": False},
        {"id": 1, "ok": False, "error": "failed"},
        {"id": 1, "ok": False, "error": {"code": 1, "message": "failed"}},
        {"id": 1, "ok": False, "error": {"code": "invalid_request"}},
        {"id": 1, "ok": False, "error": {"code": "x", "message": "x", "extra": 1}},
        [],
    ],
)
def test_rejects_malformed_response(response):
    with pytest.raises(ValueError):
        read_response(json.dumps(response).encode())


@pytest.mark.parametrize(
    "raw",
    [
        b"{",
        b"\xff",
        b'{"id":1,"ok":true,"data":NaN}',
        b'{"id":1,"ok":true,"data":1e999}',
        b'{"id":1,"ok":true,"data":"\\ud800"}',
    ],
)
def test_rejects_invalid_json_values(raw):
    with pytest.raises(ValueError):
        read_response(raw)


@pytest.mark.parametrize(
    "response",
    [
        {"id": 1, "ok": True, "data": "pong"},
        {"id": 1, "ok": False, "error": {"code": "invalid_request", "message": "bad"}},
    ],
)
def test_accepts_success_and_business_error(response):
    assert read_response(json.dumps(response).encode()) == response
