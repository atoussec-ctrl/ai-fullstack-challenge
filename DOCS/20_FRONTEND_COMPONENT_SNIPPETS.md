# Snippets de Componentes Frontend

## ChatComposer

```tsx
import { Send, Plus, Mic } from "lucide-react";
import { useState } from "react";

interface ChatComposerProps {
  disabled?: boolean;
  onSubmit: (content: string) => void;
  onAttach: (files: FileList) => void;
  onRecordAudio: () => void;
}

export function ChatComposer({
  disabled = false,
  onSubmit,
  onAttach,
  onRecordAudio,
}: ChatComposerProps) {
  const [content, setContent] = useState("");

  function handleSubmit() {
    const trimmed = content.trim();

    if (!trimmed || disabled) {
      return;
    }

    onSubmit(trimmed);
    setContent("");
  }

  return (
    <form
      className="mx-auto flex w-full max-w-3xl items-end gap-2 rounded-3xl border bg-background p-2 shadow-sm"
      onSubmit={(event) => {
        event.preventDefault();
        handleSubmit();
      }}
    >
      <label className="inline-flex h-10 w-10 cursor-pointer items-center justify-center rounded-full hover:bg-muted">
        <Plus aria-hidden="true" />
        <span className="sr-only">Anexar arquivo</span>
        <input
          className="hidden"
          type="file"
          multiple
          onChange={(event) => {
            if (event.target.files) {
              onAttach(event.target.files);
            }
          }}
        />
      </label>

      <textarea
        aria-label="Mensagem para o assistente Python"
        className="min-h-10 flex-1 resize-none bg-transparent px-2 py-2 outline-none"
        placeholder="Pergunte algo sobre Python"
        value={content}
        onChange={(event) => setContent(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            handleSubmit();
          }
        }}
      />

      <button
        type="button"
        aria-label="Gravar áudio"
        className="h-10 w-10 rounded-full hover:bg-muted"
        onClick={onRecordAudio}
      >
        <Mic aria-hidden="true" />
      </button>

      <button
        type="submit"
        aria-label="Enviar mensagem"
        disabled={disabled || !content.trim()}
        className="h-10 w-10 rounded-full bg-primary text-primary-foreground disabled:opacity-50"
      >
        <Send aria-hidden="true" />
      </button>
    </form>
  );
}
```

## ThinkingModeSelector

```tsx
import type { ThinkingMode } from "@/entities/message/model/types";

interface ThinkingModeSelectorProps {
  value: ThinkingMode;
  onChange: (value: ThinkingMode) => void;
}

const options: Array<{ value: ThinkingMode; label: string; description: string }> = [
  { value: "fast", label: "Rápido", description: "Resposta objetiva" },
  { value: "balanced", label: "Equilibrado", description: "Resposta com exemplo" },
  { value: "deep", label: "Profundo", description: "Análise detalhada" },
];

export function ThinkingModeSelector({ value, onChange }: ThinkingModeSelectorProps) {
  return (
    <label className="flex items-center gap-2 text-sm">
      <span className="text-muted-foreground">Thinking</span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value as ThinkingMode)}
        className="rounded-md border bg-background px-2 py-1"
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}
```

## MessageBubble

```tsx
import type { ChatMessage } from "@/entities/message/model/types";

interface MessageBubbleProps {
  message: ChatMessage;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <article
      className={isUser ? "ml-auto max-w-2xl rounded-2xl bg-muted p-4" : "mr-auto max-w-3xl p-4"}
      aria-label={isUser ? "Mensagem do usuário" : "Resposta do assistente"}
    >
      <p className="whitespace-pre-wrap leading-7">{message.content}</p>
    </article>
  );
}
```
