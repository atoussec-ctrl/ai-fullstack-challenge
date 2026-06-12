"""Flask application factory for MindSight AI."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from app.config import config_by_name
from app.extensions import cors, db
from app.utils.http import error_response


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure the Flask application.

    Args:
        config_name: One of 'development', 'testing', 'production'.
                     Falls back to the ``APP_ENV`` env-var, then 'development'.

    Returns:
        A fully configured Flask app instance.
    """
    if config_name is None:
        config_name = os.getenv("APP_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    cors.init_app(app, origins=app.config["CORS_ALLOWED_ORIGINS"].split(","))

    _register_blueprints(app)
    _register_error_handlers(app)

    @app.route("/health")
    def health():  # type: ignore[return]
        return jsonify(
            {
                "status": "ok",
                "service": "python-ai-assistant",
                "request_id": request.headers.get("X-Request-ID"),
            }
        )

    with app.app_context():
        from app import models  # noqa: F401

        database_uri = app.config["SQLALCHEMY_DATABASE_URI"]
        if str(database_uri).startswith("sqlite:///"):
            database_path = Path(str(database_uri).removeprefix("sqlite:///"))
            database_path.parent.mkdir(parents=True, exist_ok=True)
        Path(app.config["UPLOAD_DIR"]).mkdir(parents=True, exist_ok=True)
        db.create_all()
        _ensure_sqlite_schema(app)

    return app


def _register_blueprints(app: Flask) -> None:
    """Import and register all API blueprints."""
    from app.routes.attachments import attachments_bp
    from app.routes.books import books_bp
    from app.routes.chat import chat_bp
    from app.routes.health import health_bp
    from app.routes.openapi import docs_bp
    from app.routes.semantic_search import semantic_search_bp

    app.register_blueprint(health_bp, url_prefix="/api/v1")
    app.register_blueprint(books_bp, url_prefix="/api/v1")
    app.register_blueprint(chat_bp, url_prefix="/api/v1")
    app.register_blueprint(attachments_bp, url_prefix="/api/v1")
    app.register_blueprint(semantic_search_bp, url_prefix="/api/v1")
    app.register_blueprint(docs_bp)


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):  # type: ignore[no-untyped-def]
        return error_response(
            code=error.name.replace(" ", "_").upper(),
            message=error.description,
            status_code=error.code or 500,
        )

    @app.errorhandler(ValueError)
    def handle_value_error(error: ValueError):  # type: ignore[no-untyped-def]
        return error_response(
            code="VALIDATION_ERROR",
            message=str(error),
            status_code=400,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):  # type: ignore[no-untyped-def]
        if app.config.get("TESTING"):
            raise error
        return error_response(
            code="INTERNAL_SERVER_ERROR",
            message="Erro interno inesperado.",
            status_code=500,
        )


def _ensure_sqlite_schema(app: Flask) -> None:
    database_uri = str(app.config["SQLALCHEMY_DATABASE_URI"])
    if not database_uri.startswith("sqlite:///"):
        return
    with db.engine.connect() as connection:
        columns = {
            row[1]
            for row in connection.exec_driver_sql("PRAGMA table_info(books)").fetchall()
        }
        if columns and "category" not in columns:
            connection.exec_driver_sql(
                "ALTER TABLE books ADD COLUMN category VARCHAR(120) NOT NULL DEFAULT 'Programação'"
            )
            connection.commit()
        message_columns = {
            row[1]
            for row in connection.exec_driver_sql("PRAGMA table_info(chat_messages)").fetchall()
        }
        if message_columns and "trace_id" not in message_columns:
            connection.exec_driver_sql("ALTER TABLE chat_messages ADD COLUMN trace_id VARCHAR(128)")
            connection.commit()
        session_columns = {
            row[1]
            for row in connection.exec_driver_sql("PRAGMA table_info(chat_sessions)").fetchall()
        }
        if session_columns and "pinned" not in session_columns:
            connection.exec_driver_sql(
                "ALTER TABLE chat_sessions ADD COLUMN pinned BOOLEAN NOT NULL DEFAULT 0"
            )
            connection.exec_driver_sql("ALTER TABLE chat_sessions ADD COLUMN pinned_at DATETIME")
            connection.commit()
