# Estrutura Recomendada do Monorepo

```txt
python-ai-assistant/
├── apps/
│   ├── backend-flask/
│   │   ├── src/
│   │   │   ├── app.py
│   │   │   ├── blueprints/
│   │   │   ├── schemas/
│   │   │   └── config.py
│   │   └── tests/
│   ├── backend-fastapi/
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── routers/
│   │   │   └── schemas/
│   │   └── tests/
│   └── frontend/
│       ├── src/
│       │   ├── app/
│       │   ├── pages/
│       │   ├── widgets/
│       │   ├── features/
│       │   ├── entities/
│       │   └── shared/
│       ├── e2e/
│       ├── stories/
│       └── public/
├── packages/
│   ├── backend-domain/
│   ├── backend-application/
│   ├── backend-infrastructure/
│   └── ai/
├── docs/
├── scripts/
├── .github/
│   └── workflows/
├── docker-compose.yml
├── Makefile
└── README.md
```

## Estrutura frontend detalhada

```txt
apps/frontend/src/
├── app/
│   ├── providers/
│   │   ├── AppProviders.tsx
│   │   ├── QueryProvider.tsx
│   │   ├── ThemeProvider.tsx
│   │   └── RouterProvider.tsx
│   ├── router/
│   │   ├── routes.tsx
│   │   └── routeTree.gen.ts
│   └── styles/
│       └── globals.css
├── pages/
│   ├── ChatPage/
│   └── SettingsPage/
├── widgets/
│   ├── AppShell/
│   ├── ChatSidebar/
│   ├── ChatHeader/
│   ├── MessageList/
│   └── ChatComposer/
├── features/
│   ├── send-message/
│   ├── upload-attachment/
│   ├── record-audio/
│   ├── select-thinking-mode/
│   ├── switch-theme/
│   └── manage-session/
├── entities/
│   ├── message/
│   │   ├── model/
│   │   ├── api/
│   │   └── ui/
│   ├── session/
│   ├── attachment/
│   └── assistant/
├── shared/
│   ├── api/
│   ├── config/
│   ├── lib/
│   ├── ui/
│   └── test/
└── main.tsx
```

## Princípios

- `shared` não depende de `features`.
- `entities` não depende de `widgets`.
- `features` implementam ações do usuário.
- `widgets` compõem blocos grandes de UI.
- `pages` conectam rota, layout e widgets.
- `app` contém providers e bootstrap.

## Benefícios

- Facilita testes.
- Evita acoplamento.
- Permite evolução incremental.
- Mantém a UI organizada mesmo com chat, upload e streaming.
