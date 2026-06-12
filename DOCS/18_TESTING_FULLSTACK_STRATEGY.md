# Estratégia de Testes Fullstack

## Pirâmide de testes

```txt
             E2E Playwright
        Integração API/UI com MSW
    Componentes com React Testing Library
Unitários de domínio, hooks, utils e use cases
```

## Frontend

### Unitários

Ferramentas:

- Vitest.
- Testing Library para componentes simples.

Cobrir:

- formatadores;
- validação de arquivos;
- reducer/estado local;
- hooks puros;
- mapeamento de thinking mode.

### Componentes

Cobrir:

- ChatComposer;
- ThinkingModeSelector;
- AttachmentPreview;
- ThemeToggle;
- MessageBubble;
- Sidebar.

### Integração

Ferramentas:

- MSW;
- TanStack Query Provider;
- Router Provider.

Cobrir:

- envio de mensagem com mock da API;
- upload com retorno mockado;
- listagem de sessões;
- erro de API e retry.

### E2E

Ferramenta:

- Playwright.

Cobrir fluxos críticos:

- abrir app;
- trocar tema;
- criar conversa;
- enviar pergunta;
- ver resposta;
- anexar imagem;
- gravar áudio ou simular permissão;
- navegar no mobile.

## Backend

### Unitários

- Entidades.
- Casos de uso.
- Validações.
- Prompt builder.
- Thinking mode mapper.

### Integração

- Flask test client.
- SQLite temporário.
- Repositórios.
- Uploads.
- Endpoints de livros.

### IA

- Usar mocks/fakes para OpenAI.
- Não chamar API externa no CI.
- Testar contrato do gateway.

## Coverage recomendado

| Área | Meta |
|---|---:|
| Domain/backend | 90% |
| Application/backend | 85% |
| Frontend hooks/utils | 85% |
| Componentes críticos | 80% |
| E2E | Fluxos críticos, não percentual |

## Comandos

```bash
# frontend
pnpm test
pnpm test:coverage
pnpm test:e2e
pnpm storybook

# backend
pytest
pytest --cov=packages --cov=apps
ruff check .
mypy .
```

## Anti-patterns

- Testar detalhes internos de componente.
- Mockar tudo e não testar integração.
- Chamar OpenAI no CI.
- Testar apenas snapshots.
- E2E para todos os casos pequenos.
