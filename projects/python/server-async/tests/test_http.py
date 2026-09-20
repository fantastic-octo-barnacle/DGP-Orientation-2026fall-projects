from collections.abc import AsyncGenerator

import pytest
from httpx2 import ASGITransport, AsyncClient

from text_service.server import create_app

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient]:
    app = create_app()
    async with (
        app.router.lifespan_context(app),
        AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client,
    ):
        yield client


async def test_http_routes(client: AsyncClient) -> None:
    assert (await client.get("/ping")).status_code == 200
    response = await client.post("/users", json={"username": "alice", "password": "password1"})
    assert response.status_code == 201
    response = await client.post("/sessions", json={"username": "alice", "password": "password1"})
    token = response.json()["data"]["token"]
    assert (
        await client.get("/texts", headers={"Authorization": f"Bearer {token}"})
    ).status_code == 200
    assert (await client.get("/texts")).status_code == 401
    assert (
        await client.post(
            "/users", content=b"not JSON", headers={"Content-Type": "application/json"}
        )
    ).status_code == 400
    assert (
        await client.post(
            "/users", content=b"x" * 524289, headers={"Content-Type": "application/json"}
        )
    ).status_code == 413


@pytest.mark.parametrize("body", [b"not JSON", b"\xff", b"NaN"])
async def test_invalid_json(client: AsyncClient, body: bytes) -> None:
    assert (await client.post("/users", content=body)).status_code == 400


async def test_body_limit_and_routing(client: AsyncClient) -> None:
    exact = b"{}" + b" " * (524288 - 2)
    assert (await client.post("/users", content=exact)).status_code == 400
    assert (await client.post("/users", content=exact + b" ")).status_code == 413
    assert (await client.get("/missing")).status_code == 404
    assert (await client.get("/echo")).status_code == 404
    assert (await client.patch("/ping")).status_code == 405
    assert (await client.get("/ping?test=1")).json() == {"data": "pong"}


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
async def test_unimplemented_routes_are_absent(client: AsyncClient, method: str, path: str) -> None:
    assert (await client.request(method, path)).status_code == 404


@pytest.mark.parametrize("path", ["/ping", "/users", "/sessions", "/sessions/current", "/texts"])
async def test_wrong_method_precedes_authentication(client: AsyncClient, path: str) -> None:
    assert (await client.patch(path)).status_code == 405
