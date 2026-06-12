# Critérios de Aceite

## Backend livros

- `POST /books` cadastra livro.
- `GET /books?title=` busca por título.
- `GET /books?author=` busca por autor.
- SQLite é usado.
- OpenAPI documenta endpoints.
- Testes unitários/integrados passam.

## Chatbot

- Usuário pergunta sobre Python.
- Backend usa LangChain.
- Modelo OpenAI configurável por env.
- Resposta vem em português.
- Exemplo de lista Python funciona.
- Testes usam mock/fake.

## Vector search

- Documentos são indexados.
- Embeddings são gerados.
- FAISS armazena vetores.
- Consulta retorna documentos relevantes.
- Processo é documentado.

## Frontend

- App abre em desktop e mobile.
- Tema claro/escuro funciona.
- Usuário cria conversa.
- Usuário envia pergunta.
- Usuário escolhe thinking mode.
- Payload inclui thinking mode.
- Resposta aparece.
- Upload de imagem/documento mostra preview.
- Áudio pode ser gravado/anexado.
- Storybook contém componentes principais.
- Vitest cobre componentes críticos.
- Playwright cobre fluxo principal.

## Qualidade

- Lint passa.
- Typecheck passa.
- Testes passam.
- Build passa.
- Sem segredos.
- Documentação atualizada.
