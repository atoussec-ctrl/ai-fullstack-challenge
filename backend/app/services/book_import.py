"""AI-assisted book import from uploaded files.

The MVP uses deterministic extraction so tests never call external LLMs. The
service boundary is intentionally isolated so a LangChain/OpenAI extractor can
replace the heuristic extractor later.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from werkzeug.datastructures import FileStorage

from app.models import Book
from app.services.books import BookService
from app.services.observability import traceable_if_enabled


@dataclass(frozen=True)
class ExtractedBook:
    title: str
    category: str
    author: str
    publication_year: int
    summary: str


class BookMetadataExtractor:
    @traceable_if_enabled("books.extract_metadata", run_type="tool")
    def extract(self, *, filename: str, content: str) -> ExtractedBook:
        payload = parse_json_content(content) or {}
        title = value_from_payload(payload, "title", "titulo", "título") or regex_value(
            content, r"(?:t[ií]tulo|title)\s*[:\-]\s*(.+)"
        )
        title = title or heading_title(content) or Path(filename).stem.replace("_", " ")

        author = value_from_payload(payload, "author", "autor", "autora") or regex_value(
            content, r"(?:autor(?:a)?|author)\s*[:\-]\s*(.+)"
        )
        category = value_from_payload(payload, "category", "categoria") or regex_value(
            content, r"(?:categoria|category)\s*[:\-]\s*(.+)"
        )
        year_value = (
            value_from_payload(payload, "publication_year", "year", "ano")
            or regex_value(content, r"(?:ano|year|publica[cç][aã]o|publication)\D+(\d{4})")
            or first_year(content)
        )
        summary = value_from_payload(payload, "summary", "resumo") or summary_from_text(content)

        missing = []
        if not title:
            missing.append("title")
        if not author:
            missing.append("author")
        if not year_value:
            missing.append("publication_year")
        if not summary:
            missing.append("summary")
        if missing:
            raise ValueError(
                "Não foi possível extrair metadados obrigatórios do livro: "
                + ", ".join(missing)
                + ". Inclua título, autor, ano e resumo no arquivo."
            )

        return ExtractedBook(
            title=clean(title),
            category=clean(category or "Programação"),
            author=clean(author),
            publication_year=int(str(year_value)[:4]),
            summary=clean(summary),
        )


class BookImportService:
    def __init__(
        self,
        extractor: BookMetadataExtractor | None = None,
        book_service: BookService | None = None,
    ) -> None:
        self.extractor = extractor or BookMetadataExtractor()
        self.book_service = book_service or BookService()

    @traceable_if_enabled("books.import_file", run_type="chain")
    def import_file(self, file: FileStorage | None) -> tuple[Book, ExtractedBook]:
        if not file or not file.filename:
            raise ValueError("Campo file é obrigatório.")
        extension = Path(file.filename).suffix.lower()
        if extension not in {".txt", ".md", ".json", ".pdf"}:
            raise ValueError("Envie um arquivo .txt, .md, .json ou .pdf.")

        raw = file.read()
        if extension == ".pdf":
            content = extract_pdf_text(raw)
        else:
            content = raw.decode("utf-8", errors="ignore")
        if not content.strip():
            raise ValueError("Arquivo sem texto legível para extração.")

        extracted = self.extractor.extract(filename=file.filename, content=content)
        book = self.book_service.create(
            {
                "title": extracted.title,
                "category": extracted.category,
                "author": extracted.author,
                "publication_year": extracted.publication_year,
                "summary": extracted.summary,
            }
        )
        return book, extracted


def extract_pdf_text(raw: bytes) -> str:
    """Extract text from PDF bytes. Returns empty string for scanned/text-less PDFs."""
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - depends on optional package
        raise RuntimeError("Dependência pypdf não instalada para leitura de PDF.") from exc

    try:
        reader = PdfReader(BytesIO(raw))
        pages = [page.extract_text() or "" for page in reader.pages]
    except Exception:
        return ""
    return "\n".join(pages).strip()


def parse_json_content(content: str) -> dict[str, object] | None:
    try:
        payload = json.loads(content)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def value_from_payload(payload: dict[str, object], *keys: str) -> str | None:
    for key in keys:
        value = payload.get(key)
        if value is not None and str(value).strip():
            return str(value)
    return None


def regex_value(content: str, pattern: str) -> str | None:
    match = re.search(pattern, content, flags=re.IGNORECASE)
    if not match:
        return None
    return match.group(1).strip()


def heading_title(content: str) -> str | None:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.removeprefix("# ").strip()
    return None


def first_year(content: str) -> str | None:
    match = re.search(r"\b(1[5-9]\d{2}|20\d{2}|21\d{2})\b", content)
    return match.group(1) if match else None


def summary_from_text(content: str) -> str | None:
    match = re.search(
        r"(?:resumo|summary)\s*[:\-]\s*(.+?)(?:\n\s*\n|$)",
        content,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if match:
        return match.group(1).strip()
    paragraphs = [line.strip() for line in content.splitlines() if line.strip()]
    if len(paragraphs) >= 3:
        return " ".join(paragraphs[2:])[:1200]
    return None


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().strip('"')
