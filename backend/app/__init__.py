from pathlib import Path

from flask import Flask, send_from_directory

from .api import api
from .db import ensure_db


def create_app() -> Flask:
    app = Flask(__name__)
    ensure_db()
    app.register_blueprint(api)

    frontend_dir = Path(__file__).resolve().parents[2] / "frontend"

    @app.get("/")
    def index():
        return send_from_directory(frontend_dir, "index.html")

    @app.get("/app.js")
    def app_js():
        return send_from_directory(frontend_dir, "app.js")

    @app.get("/styles.css")
    def styles_css():
        return send_from_directory(frontend_dir, "styles.css")

    return app
