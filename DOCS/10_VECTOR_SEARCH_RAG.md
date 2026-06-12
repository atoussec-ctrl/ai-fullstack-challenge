# Busca Semântica, Embeddings e RAG

## Objetivo

Implementar a questão de vector stores e preparar evolução para RAG.

## MVP

- Conjunto local de documentos.
- Chunking simples.
- Embeddings.
- FAISS.
- Busca top-k.
- Exibição dos documentos mais relevantes.

## Fluxo

```txt
Documento
  ↓
Chunking
  ↓
Embedding
  ↓
FAISS index
  ↓
Consulta
  ↓
Embedding da consulta
  ↓
Similaridade
  ↓
Top-k documentos
```

## Documentos iniciais

- Artigo sobre listas em Python.
- Artigo sobre dicionários em Python.
- Artigo sobre Flask.
- Artigo sobre FastAPI.
- Artigo sobre pytest.
- Artigo sobre SQLAlchemy.

## Contrato de busca

### POST /semantic-search

Request:

```json
{
  "query": "Como guardar vários itens em Python?",
  "k": 3
}
```

Response:

```json
{
  "results": [
    {
      "document_id": "doc_lists",
      "title": "Listas em Python",
      "score": 0.89,
      "excerpt": "Listas em Python armazenam múltiplos valores..."
    }
  ]
}
```

## Evolução para RAG

1. Buscar top-k documentos.
2. Montar contexto.
3. Enviar contexto ao LLM.
4. Responder citando fontes internas.
5. Evitar alucinação quando contexto não for suficiente.

## FAISS vs Milvus

| Critério | FAISS | Milvus |
|---|---|---|
| Setup local | Simples | Mais complexo |
| Prova/MVP | Excelente | Exagerado |
| Produção escalável | Limitado | Melhor |
| Multiusuário | Manual | Melhor |
| Filtros avançados | Manual | Melhor |

## Decisão

Usar FAISS no MVP e documentar Milvus como evolução.
