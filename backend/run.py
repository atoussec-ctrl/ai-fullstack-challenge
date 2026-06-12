"""MindSight AI — Application entry-point.

Usage:
    python run.py
"""

from dotenv import load_dotenv

# Load .env from project root (one level up)
load_dotenv(dotenv_path="../.env")

from app import create_app  # noqa: E402

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
