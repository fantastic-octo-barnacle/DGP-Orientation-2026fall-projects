import argparse
import asyncio
import json

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .service import Service


def create_app() -> FastAPI:
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
    service = Service()

    @app.api_route(
        "/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
    )
    async def dispatch(request: Request):
        body = None
        if request.method in ("POST", "PUT"):
            raw = bytearray()
            async for chunk in request.stream():
                raw.extend(chunk)
                if len(raw) > 512 * 1024:
                    return JSONResponse({"message": "Request body too large"}, status_code=413)
            try:
                body = json.loads(
                    raw.decode("utf-8"),
                    parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
                )
            except (ValueError, UnicodeError):
                return JSONResponse({"message": "Expected UTF-8 JSON"}, status_code=400)
        # Password hashing is blocking: keep it off the event loop.
        status, result = await asyncio.to_thread(
            service.handle,
            request.method,
            request.url.path,
            body,
            request.headers.get("Authorization", ""),
        )
        return JSONResponse(result, status_code=status)

    return app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7878)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be 1..65535")
    # Task: request deadline and bounded shutdown, including active business operations.
    uvicorn.run(create_app(), host=args.host, port=args.port, workers=1)
