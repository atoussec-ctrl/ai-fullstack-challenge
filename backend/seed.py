"""MindSight AI — database seeding entry-point.

Usage:
    python seed.py

Idempotent: running it again will not duplicate existing books.
"""

from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

from app import create_app  # noqa: E402
from app.services.seed import seed_books  # noqa: E402


def main() -> None:
    app = create_app()
    with app.app_context():
        result = seed_books()
    print(
        f"Seed concluído: {result.created} criado(s), "
        f"{result.skipped} já existente(s), {result.total} no catálogo."
    )


if __name__ == "__main__":
    main()
