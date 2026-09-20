import argparse
import json
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from time import perf_counter
from typing import Annotated, Any

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import RequestResponseEndpoint

from .service import ROUTES, Service, route_error

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Press Ctrl+C to exit. All in-memory data is lost on exit.")
    logger.info("Routes:")
    for method, path in ROUTES:
        logger.info("  %s %s", method, path)
    yield


async def read_body(request: Request) -> Any:
    if request.method not in ("POST", "PUT"):
        return None
    raw = bytearray()
    async for chunk in request.stream():
        raw.extend(chunk)
        if len(raw) > 512 * 1024:
            raise HTTPException(413, "Request body too large")
    try:
        return json.loads(
            raw.decode("utf-8"),
            parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
        )
    except (ValueError, UnicodeError) as exc:
        raise HTTPException(400, "Expected UTF-8 JSON") from exc


def create_app() -> FastAPI:
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None, lifespan=lifespan)
    service = Service()

    @app.middleware("http")
    async def log_request(request: Request, call_next: RequestResponseEndpoint) -> Response:
        started = perf_counter()
        status = 500
        try:
            if error := route_error(request.method, request.url.path):
                response = JSONResponse(
                    {"message": "Not found" if error == 404 else "Method not allowed"},
                    status_code=error,
                )
            else:
                response = await call_next(request)
            status = response.status_code
            return response
        finally:
            logger.info(
                "%s %s -> %d %.1fms",
                request.method,
                json.dumps(request.url.path, ensure_ascii=False),
                status,
                (perf_counter() - started) * 1000,
            )

    @app.api_route(
        "/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
    )
    def dispatch(request: Request, body: Annotated[Any, Depends(read_body)]) -> JSONResponse:
        # FastAPI runs this synchronous handler in a thread pool.
        status, result = service.handle(
            request.method, request.url.path, body, request.headers.get("Authorization", "")
        )
        return JSONResponse(result, status_code=status)

    return app


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7878)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be 1..65535")
    uvicorn.run(create_app(), host=args.host, port=args.port, workers=1, access_log=False)
