"""MindSight AI — Application entry-point.

Usage:
    python run.py
"""

from app.env_loader import load_project_env

load_project_env()

from app import create_app  # noqa: E402

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
