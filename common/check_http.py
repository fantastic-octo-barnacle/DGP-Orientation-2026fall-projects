"""Black-box HTTP checks; standard library only, independent of candidate code."""

import argparse
import json
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError
from urllib.request import ProxyHandler, Request, build_opener


def request(url, method, path, body=None, token="", expected=200):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode()
    req = Request(url.rstrip("/") + path, data, headers, method=method)
    try:
        response = build_opener(ProxyHandler({})).open(req, timeout=15)
    except HTTPError as exc:
        response = exc
    with response:
        raw = response.read()
        assert response.status == expected, (
            f"{method} {path}: expected {expected}, got {response.status}: {raw[:200]!r}"
        )
        if expected >= 400:
            return None
        result = json.loads(raw)
        assert isinstance(result, dict) and set(result) == {"data"}, result
        return result["data"]


def account(url):
    body = {"username": "check_" + uuid.uuid4().hex[:16], "password": "password1"}
    assert request(url, "POST", "/users", body, expected=201) == {
        "username": body["username"]
    }
    login = request(url, "POST", "/sessions", body)
    assert isinstance(login["token"], str) and login["token"]
    return body, login


def baseline(url):
    assert request(url, "GET", "/ping") == "pong"
    body, login = account(url)
    old = login["token"]
    request(url, "POST", "/users", body, expected=409)
    request(url, "POST", "/sessions", {**body, "password": "incorrect"}, expected=401)
    new = request(url, "POST", "/sessions", body)["token"]
    assert old != new
    request(url, "GET", "/texts", token=old, expected=401)
    request(url, "GET", "/texts", expected=401)
    assert request(url, "GET", "/texts", token=new) == []
    assert request(url, "DELETE", "/sessions/current", token=new) is None
    request(url, "GET", "/texts", token=new, expected=401)
    request(
        url, "POST", "/users", {"username": True, "password": "password1"}, expected=400
    )


def business(url):
    body, login = account(url)
    token = login["token"]
    _, other = account(url)
    text = "你好\nHTTP"
    assert request(url, "POST", "/echo", {"text": text}) == text
    start = time.monotonic()
    assert request(url, "POST", "/delay", {"milliseconds": 200}) == {
        "milliseconds": 200
    }
    assert time.monotonic() - start >= 0.18, "delay returned too early"
    for value in [True, 1.5, -1, 10001]:
        request(url, "POST", "/delay", {"milliseconds": value}, expected=400)
    for name in ["z", "a"]:
        assert request(url, "PUT", f"/texts/{name}", {"text": text}, token) is None
    assert request(url, "GET", "/texts", token=token) == ["a", "z"]
    assert request(url, "GET", "/texts/a", token=token) == text
    request(url, "GET", "/texts/a", token=other["token"], expected=404)
    request(url, "PUT", "/texts/a", {"text": "other"}, other["token"])
    for value in ["", "x" * 65536, "界" * 21845]:
        request(url, "PUT", "/texts/a", {"text": value}, token)
        assert request(url, "GET", "/texts/a", token=token) == value
    request(url, "PUT", "/texts/a", {"text": "界" * 21846}, token, expected=413)
    request(url, "PUT", "/texts/invalid.name", {"text": "x"}, token, expected=400)
    request(url, "DELETE", "/texts/z", token=token)
    request(url, "DELETE", "/texts/z", token=token, expected=404)
    request(url, "DELETE", "/users/me", token=token)
    request(url, "GET", "/texts", token=token, expected=401)
    request(url, "POST", "/users", body, expected=201)
    renewed = request(url, "POST", "/sessions", body)["token"]
    assert request(url, "GET", "/texts", token=renewed) == []
    request(url, "GET", "/texts", token=token, expected=401)
    assert request(url, "GET", "/texts/a", token=other["token"]) == "other"


def expiry(url, ttl):
    body, login = account(url)
    assert type(login.get("expires_in")) is int and login["expires_in"] == ttl
    token = login["token"]
    started = time.monotonic()
    assert request(url, "GET", "/texts", token=token) == []
    time.sleep(ttl / 2)
    assert request(url, "GET", "/texts", token=token) == []
    time.sleep(max(0, started + ttl + 0.2 - time.monotonic()))
    request(url, "GET", "/texts", token=token, expected=401)
    new = request(url, "POST", "/sessions", body)["token"]
    assert new != token
    assert request(url, "GET", "/texts", token=new) == []
    request(url, "GET", "/texts", token=token, expected=401)


def concurrency(url):
    with ThreadPoolExecutor(max_workers=2) as pool:
        slow = pool.submit(request, url, "POST", "/delay", {"milliseconds": 1500})
        time.sleep(0.2)
        start = time.monotonic()
        assert request(url, "GET", "/ping") == "pong"
        assert time.monotonic() - start < 0.8, "ping blocked by delay"
        assert slow.result(timeout=5) == {"milliseconds": 1500}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "stage", choices=["baseline", "business", "expiry", "concurrency"]
    )
    parser.add_argument("--url", default="http://127.0.0.1:7878")
    parser.add_argument("--ttl", type=int, default=2)
    args = parser.parse_args()
    if args.ttl <= 0:
        parser.error("ttl must be positive")
    try:
        if args.stage == "expiry":
            expiry(args.url, args.ttl)
        else:
            globals()[args.stage](args.url)
    except (AssertionError, OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"FAIL: {args.stage}: {exc}\n")
    print(f"PASS: {args.stage}")


if __name__ == "__main__":
    main()
