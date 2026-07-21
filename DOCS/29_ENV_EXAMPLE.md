# Variaveis de ambiente

As variaveis ficam em `.env` na raiz do projeto. O backend carrega esse arquivo via `backend/app/env_loader.py`.

## Aplicacao

| Variavel | Exemplo | Uso |
| --- | --- | --- |
| `APP_ENV` | `development`, `testing`, `production` | Seleciona config Flask. |
| `LOG_LEVEL` | `INFO` | Existe no template, mas ainda nao e aplicado globalmente. |
| `FLASK_DEBUG` | `false` | Liga o debug server apenas quando explicitamente `true` em `backend/run.py`. |
| `SECRET_KEY` | valor forte | Chave de assinatura Flask. Obrigatoria em producao. |

Recomendacao: em producao, falhar startup se `SECRET_KEY` estiver vazio, placeholder ou default.

## Banco de dados

| Variavel | Exemplo | Uso |
| --- | --- | --- |
| `DATABASE_URL` | `sqlite:///./storage/app.db` | URI SQLAlchemy. |

Tradeoff atual: SQLite simplifica setup local, mas nao resolve concorrencia, migracoes e operacao multiusuario como Postgres.

## Gateway de chat

| Variavel | Exemplo | Uso |
| --- | --- | --- |
| `CHAT_GATEWAY` | `local`, `openai`, `huggingface`, `auto` | Seleciona gateway. |
| `OPENAI_API_KEY` | chave real | Usada quando gateway OpenAI estiver ativo. |
| `OPENAI_MODEL` | `gpt-4.1-mini` | Modelo OpenAI default. |
| `HUGGINGFACE_API_KEY` | chave real | Usada pelo router Hugging Face. |
| `HF_CHAT_MODEL` | `deepseek-ai/DeepSeek-V4-Flash` | Modelo HF default. |
| `HF_BASE_URL` | `https://router.huggingface.co/v1` | Endpoint OpenAI-compatible. |
| `CHAT_MAX_OUTPUT_TOKENS` | `4096` | Limite de tokens de saida. |

O modo `local` e o melhor default para desenvolvimento e CI, pois nao depende de rede nem de custo externo.

## LangSmith

| Variavel | Exemplo | Uso |
| --- | --- | --- |
| `LANGSMITH_TRACING` | `false` | Habilita tracing. |
| `LANGSMITH_API_KEY` | chave real | Autenticacao LangSmith. |
| `LANGSMITH_PROJECT` | `mindsight-ai` | Projeto de traces. |

O codigo degrada para no-op quando tracing esta desabilitado ou pacote/chave falha.

## Embeddings e busca

| Variavel | Exemplo | Uso |
| --- | --- | --- |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Modelo planejado para embeddings reais. |
| `VECTOR_STORE` | `faiss` | Vector store planejado. |
| `FAISS_INDEX_PATH` | `./storage/faiss.index` | Caminho do indice. |

Estado atual: a busca semantica usa hashing local demonstrativo, nao FAISS real.

## Uploads

| Variavel | Exemplo | Uso |
| --- | --- | --- |
| `UPLOAD_DIR` | `./storage/uploads` | Pasta de arquivos. |
| `MAX_UPLOAD_SIZE_MB` | `10` | Limite por arquivo. |

Recomendacoes para producao:

- Validar tipo real do arquivo, nao apenas extensao/MIME informado.
- Manter testes garantindo remocao fisica quando sessoes/anexos forem deletados.
- Aplicar limites de paginas/tempo para PDFs.
- Considerar armazenamento externo, como S3, quando houver escala.

## CORS e frontend

| Variavel | Exemplo | Uso |
| --- | --- | --- |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3002` | Origens aceitas pelo Flask-CORS. |
| `VITE_API_BASE_URL` | `http://localhost:5000/api/v1` | Base URL usada pelo frontend. |
| `VITE_API_PROXY_TARGET` | `http://localhost:5000` | Proxy do Vite em desenvolvimento. |
| `VITE_APP_NAME` | `MindSight AI` | Nome exibido na UI. |
| `VITE_DEFAULT_THINKING_MODE` | `balanced` | Modo inicial do chat. |
