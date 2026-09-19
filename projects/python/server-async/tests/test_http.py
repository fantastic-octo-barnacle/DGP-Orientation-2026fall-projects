from starlette.testclient import TestClient

from text_service.server import create_app


def test_http_routes():
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
