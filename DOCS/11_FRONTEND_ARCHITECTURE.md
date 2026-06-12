# Arquitetura Frontend

## Stack

```txt
Vite
React
TypeScript
Tailwind CSS
shadcn/ui
Motion / Framer Motion
TanStack Query
TanStack Router
TanStack Form
Zod
Vitest
React Testing Library
Playwright
Storybook
MSW
```

## Camadas

```txt
Presentation
  Components, Pages, Widgets
Application
  Hooks, Use Cases, Commands
Domain
  Types, Models, Validation Rules
Infrastructure
  API Client, Storage, Browser APIs
```

## Estrutura sugerida

```txt
src/
├── app/
├── pages/
├── widgets/
├── features/
├── entities/
└── shared/
```

## Exemplo de entidade

```ts
export type MessageRole = "user" | "assistant" | "system";

export type ThinkingMode = "fast" | "balanced" | "deep";

export interface ChatMessage {
  id: string;
  sessionId: string;
  role: MessageRole;
  content: string;
  thinkingMode?: ThinkingMode;
  createdAt: string;
}
```

## Exemplo de porta de API

```ts
import type { ChatMessage, ThinkingMode } from "@/entities/message/model/types";

export interface SendMessageInput {
  sessionId: string;
  content: string;
  thinkingMode: ThinkingMode;
  attachmentIds?: string[];
}

export interface ChatApi {
  sendMessage(input: SendMessageInput): Promise<{
    userMessageId: string;
    assistantMessageId: string;
    status: "processing";
  }>;

  listMessages(sessionId: string): Promise<ChatMessage[]>;
}
```

## Regra de dependência

Componentes não devem chamar `fetch` diretamente.

Correto:

```txt
Component → hook/use case → api client → Flask
```

Incorreto:

```txt
Component → fetch direto
```

## Convenções

- Nomes de componentes em PascalCase.
- Hooks começam com `use`.
- Tipos terminam com `Input`, `Output`, `DTO` ou `Model`.
- Arquivos de teste próximos ao código quando fizer sentido.
- Componentes de UI reutilizáveis em `shared/ui`.
