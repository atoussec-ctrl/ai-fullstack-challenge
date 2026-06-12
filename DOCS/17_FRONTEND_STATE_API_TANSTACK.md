# TanStack — Estado, Rotas, Formulários e API

## Decisão

Usar TanStack em três áreas:

| Ferramenta | Uso |
|---|---|
| TanStack Query | Estado assíncrono e comunicação com Flask |
| TanStack Router | Rotas type-safe |
| TanStack Form | Formulários e validação |
| Zod | Validação runtime |

## Estado local vs server state

### Estado local

Exemplos:

- sidebar aberta/fechada;
- tema;
- texto temporário do composer;
- arquivos pendentes;
- gravação de áudio.

Pode ficar em React state/context.

### Server state

Exemplos:

- sessões de chat;
- mensagens;
- attachments enviados;
- livros;
- resultados de busca semântica.

Deve ficar em TanStack Query.

## API client

```ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:5000/api/v1";

export async function apiRequest<TResponse>(
  path: string,
  init?: RequestInit,
): Promise<TResponse> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json() as Promise<TResponse>;
}
```

## Query hook

```tsx
import { useQuery } from "@tanstack/react-query";
import { apiRequest } from "@/shared/api/client";
import type { ChatMessage } from "@/entities/message/model/types";

export function useMessages(sessionId: string) {
  return useQuery({
    queryKey: ["messages", sessionId],
    queryFn: () => apiRequest<ChatMessage[]>(`/chat/sessions/${sessionId}/messages`),
    enabled: Boolean(sessionId),
  });
}
```

## Mutation hook

```tsx
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiRequest } from "@/shared/api/client";

interface SendMessageInput {
  sessionId: string;
  content: string;
  thinkingMode: "fast" | "balanced" | "deep";
}

export function useSendMessage() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (input: SendMessageInput) =>
      apiRequest("/chat/messages", {
        method: "POST",
        body: JSON.stringify({
          session_id: input.sessionId,
          content: input.content,
          thinking_mode: input.thinkingMode,
        }),
      }),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["messages", variables.sessionId],
      });
    },
  });
}
```

## Upload com FormData

```ts
export async function uploadAttachment(file: File, sessionId: string) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("session_id", sessionId);

  const response = await fetch(`${API_BASE_URL}/attachments`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Falha ao enviar arquivo.");
  }

  return response.json();
}
```

## Streaming

Para streaming, usar `fetch` com `ReadableStream` ou SSE.

Recomendação MVP:

- REST para criar mensagem;
- SSE para receber tokens;
- fallback para polling se SSE falhar.
