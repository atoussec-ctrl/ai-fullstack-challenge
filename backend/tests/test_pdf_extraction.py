"""TDD para MS-105: extração real de texto de PDF no import e em anexos."""

from __future__ import annotations

from io import BytesIO

import pytest

pypdf = pytest.importorskip("pypdf")


def _make_pdf(text: str) -> bytes:
    from pypdf import PdfWriter

    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buffer = BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


# PDF mínimo válido com um objeto de texto "Título: ..." legível por extratores.
def _handcrafted_pdf(lines: list[str]) -> bytes:
    text_ops = "BT /F1 12 Tf 72 720 Td 14 TL\n"
    for line in lines:
        escaped = line.replace("(", r"\(").replace(")", r"\)")
        text_ops += f"({escaped}) Tj T*\n"
    text_ops += "ET"
    stream = text_ops.encode("latin-1")
    objects = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objects.append(
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>"
    )
    objects.append(
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream"
    )
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    pdf = b"%PDF-1.4\n"
    offsets = []
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf += f"{index} 0 obj\n".encode() + obj + b"\nendobj\n"
    xref_pos = len(pdf)
    pdf += f"xref\n0 {len(objects) + 1}\n".encode()
    pdf += b"0000000000 65535 f \n"
    for offset in offsets:
        pdf += f"{offset:010d} 00000 n \n".encode()
    pdf += (
        b"trailer\n<< /Size "
        + str(len(objects) + 1).encode()
        + b" /Root 1 0 R >>\nstartxref\n"
        + str(xref_pos).encode()
        + b"\n%%EOF"
    )
    return pdf


def test_extract_pdf_text_reads_content():
    from app.services.book_import import extract_pdf_text

    pdf_bytes = _handcrafted_pdf(["Titulo: Clean Code", "Autor: Robert Martin"])
    text = extract_pdf_text(pdf_bytes)

    assert "Clean Code" in text
    assert "Robert Martin" in text


def test_import_pdf_book(client):
    pdf_bytes = _handcrafted_pdf(
        [
            "Titulo: Arquitetura Limpa",
            "Autor: Robert C. Martin",
            "Categoria: Engenharia de Software",
            "Ano: 2017",
            "Resumo: Principios de componentes, camadas e fronteiras.",
        ]
    )

    response = client.post(
        "/api/v1/books/import",
        data={"file": (BytesIO(pdf_bytes), "arquitetura.pdf")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 201, response.get_json()
    book = response.get_json()["book"]
    assert book["title"] == "Arquitetura Limpa"
    assert book["author"] == "Robert C. Martin"
    assert book["publication_year"] == 2017


def test_import_pdf_without_text_raises(client):
    empty_pdf = _make_pdf("")

    response = client.post(
        "/api/v1/books/import",
        data={"file": (BytesIO(empty_pdf), "vazio.pdf")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"
