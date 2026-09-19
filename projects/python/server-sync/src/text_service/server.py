import argparse
import json
from typing import Annotated, Any

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .service import Service


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
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
    service = Service()

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
    # Task: bounded request reading and shutdown of in-flight requests.
    uvicorn.run(create_app(), host=args.host, port=args.port, workers=1)
