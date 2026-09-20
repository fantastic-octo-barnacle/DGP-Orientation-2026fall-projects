import pytest
from fastapi.testclient import TestClient

from text_service.server import create_app


def test_http_routes() -> None:
    with TestClient(create_app()) as client:
        assert client.get("/ping").status_code == 200
        response = client.post("/users", json={"username": "alice", "password": "password1"})
        assert response.status_code == 201
        response = client.post("/sessions", json={"username": "alice", "password": "password1"})
        token = response.json()["data"]["token"]
        assert client.get("/texts", headers={"Authorization": f"Bearer {token}"}).status_code == 200
        assert client.get("/texts").status_code == 401
        assert (
            client.post(
                "/users", content=b"not JSON", headers={"Content-Type": "application/json"}
            ).status_code
            == 400
        )
        assert (
            client.post(
                "/users", content=b"x" * 524289, headers={"Content-Type": "application/json"}
            ).status_code
            == 413
        )


@pytest.mark.parametrize("body", [b"not JSON", b"\xff", b"NaN"])
def test_invalid_json(body: bytes) -> None:
    with TestClient(create_app()) as client:
        assert client.post("/users", content=body).status_code == 400


def test_body_limit_and_routing() -> None:
    with TestClient(create_app()) as client:
        exact = b"{}" + b" " * (524288 - 2)
        assert client.post("/users", content=exact).status_code == 400
        assert client.post("/users", content=exact + b" ").status_code == 413
        assert client.get("/missing").status_code == 404
        assert client.get("/echo").status_code == 404
        assert client.patch("/ping").status_code == 405
        assert client.get("/ping?test=1").json() == {"data": "pong"}


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("POST", "/echo"),
        ("DELETE", "/users/me"),
        ("PUT", "/texts/note"),
        ("GET", "/texts/note"),
        ("DELETE", "/texts/note"),
    ],
)
def test_unimplemented_routes_are_absent(method: str, path: str) -> None:
    with TestClient(create_app()) as client:
        assert client.request(method, path).status_code == 404


@pytest.mark.parametrize("path", ["/ping", "/users", "/sessions", "/sessions/current", "/texts"])
def test_wrong_method_precedes_authentication(path: str) -> None:
    with TestClient(create_app()) as client:
        assert client.patch(path).status_code == 405
