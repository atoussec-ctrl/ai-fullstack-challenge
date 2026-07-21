"""TDD: HashingEmbeddingModel must stay deterministic across processes.

Python's builtin hash() for str is randomized per-process via PYTHONHASHSEED,
so `hash(token) % dimensions` would produce different buckets on every run —
breaking the "deterministic" contract HashingEmbeddingModel promises. These
tests pin the bucket formula to sha256, which is stable regardless of seed.
"""

from __future__ import annotations

from hashlib import sha256

from app.services.semantic_search import HashingEmbeddingModel, stable_token_bucket


def test_stable_token_bucket_matches_sha256_formula():
    dimensions = 64
    token = "python"

    expected = int(sha256(token.encode()).hexdigest(), 16) % dimensions

    assert stable_token_bucket(token, dimensions) == expected


def test_stable_token_bucket_stays_within_dimensions_bounds():
    dimensions = 8

    for token in ["a", "lists", "flask", "sqlalchemy", "listas"]:
        bucket = stable_token_bucket(token, dimensions)
        assert 0 <= bucket < dimensions


def test_stable_token_bucket_is_stable_across_repeated_calls():
    assert stable_token_bucket("dicionario", 64) == stable_token_bucket("dicionario", 64)


def test_embed_is_deterministic_across_fresh_instances():
    model_a = HashingEmbeddingModel(dimensions=32)
    model_b = HashingEmbeddingModel(dimensions=32)

    assert model_a.embed("Listas em Python") == model_b.embed("Listas em Python")
