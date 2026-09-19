import argparse
import json

from flask import Flask, request
from werkzeug.exceptions import HTTPException

from .service import Service


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 512 * 1024
    service = Service()

    @app.errorhandler(HTTPException)
    def error(exc):
        return {"message": exc.description}, exc.code

    @app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE"])
    @app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
    def dispatch(path):
        body = None
        if request.method in ("POST", "PUT"):
            try:
                body = json.loads(
                    request.get_data().decode("utf-8"),
                    parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
                )
            except (ValueError, UnicodeError):
                return {"message": "Expected UTF-8 JSON"}, 400
        status, result = service.handle(
            request.method, "/" + path, body, request.headers.get("Authorization", "")
        )
        return result, status

    return app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7878)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be 1..65535")
    # Task: bounded request reading and shutdown of in-flight requests.
    create_app().run(host=args.host, port=args.port, threaded=False, use_reloader=False)
