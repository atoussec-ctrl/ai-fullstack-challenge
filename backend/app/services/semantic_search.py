"""Deterministic semantic search service used by the MVP."""

from __future__ import annotations

import re
from dataclasses import dataclass
from math import sqrt

from app.services.observability import traceable_if_enabled


@dataclass(frozen=True)
class SearchDocument:
    document_id: str
    title: str
    content: str


DEFAULT_DOCUMENTS = [
    SearchDocument(
        "doc_lists",
        "Listas em Python",
        "Listas em Python armazenam múltiplos valores em ordem usando colchetes.",
    ),
    SearchDocument(
        "doc_dicts",
        "Dicionários em Python",
        "Dicionários guardam pares de chave e valor para busca rápida por chave.",
    ),
    SearchDocument(
        "doc_flask",
        "Flask",
        "Flask é um microframework Python para criar APIs HTTP simples e testáveis.",
    ),
    SearchDocument(
        "doc_fastapi",
        "FastAPI",
        "FastAPI cria APIs modernas com tipagem, validação e documentação OpenAPI.",
    ),
    SearchDocument(
        "doc_pytest",
        "pytest",
        "pytest executa testes unitários e de integração com fixtures simples.",
    ),
    SearchDocument(
        "doc_sqlalchemy",
        "SQLAlchemy",
        "SQLAlchemy mapeia modelos Python para tabelas relacionais como SQLite.",
    ),
]


class HashingEmbeddingModel:
    """Small local embedding model that keeps tests deterministic."""

    def __init__(self, dimensions: int = 64) -> None:
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in tokenize(text):
            vector[hash(token) % self.dimensions] += 1.0
        norm = sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]


def tokenize(text: str) -> list[str]:
    return re.findall(r"[\wÀ-ÿ]+", text.lower())


def cosine_similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


class SemanticSearchService:
    def __init__(
        self,
        documents: list[SearchDocument] | None = None,
        embeddings: HashingEmbeddingModel | None = None,
    ) -> None:
        self.documents = documents or DEFAULT_DOCUMENTS
        self.embeddings = embeddings or HashingEmbeddingModel()
        self.document_vectors = {
            document.document_id: self.embeddings.embed(f"{document.title} {document.content}")
            for document in self.documents
        }

    @traceable_if_enabled("semantic_search.search", run_type="retriever")
    def search(self, query: str, k: int = 3) -> list[dict[str, object]]:
        if not query.strip():
            raise ValueError("Campo query é obrigatório.")
        if k < 1 or k > 10:
            raise ValueError("Campo k deve estar entre 1 e 10.")

        query_vector = self.embeddings.embed(query)
        ranked = sorted(
            (
                (
                    cosine_similarity(query_vector, self.document_vectors[document.document_id]),
                    document,
                )
                for document in self.documents
            ),
            key=lambda item: item[0],
            reverse=True,
        )
        return [
            {
                "document_id": document.document_id,
                "title": document.title,
                "score": round(score, 4),
                "excerpt": document.content[:180],
            }
            for score, document in ranked[:k]
        ]
