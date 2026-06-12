# Design System Frontend

## Base

- Tailwind CSS.
- shadcn/ui.
- CSS variables.
- Tema claro e escuro.
- Tokens semânticos.

## Tokens

```css
:root {
  --background: 0 0% 100%;
  --foreground: 240 10% 3.9%;
  --sidebar: 0 0% 98%;
  --composer: 0 0% 100%;
  --border: 240 5.9% 90%;
  --muted: 240 4.8% 95.9%;
  --primary: 240 5.9% 10%;
  --radius: 1rem;
}

.dark {
  --background: 240 10% 3.9%;
  --foreground: 0 0% 98%;
  --sidebar: 240 10% 5%;
  --composer: 240 5% 12%;
  --border: 240 3.7% 15.9%;
  --muted: 240 3.7% 15.9%;
  --primary: 0 0% 98%;
}
```

## Componentes shadcn/ui sugeridos

| Componente | Uso |
|---|---|
| Button | Ações do composer, sidebar, copiar código |
| Textarea | Input do chat |
| ScrollArea | Lista de mensagens e sidebar |
| Sheet | Sidebar mobile |
| Dialog | Preview de arquivo |
| DropdownMenu | Menu de ações |
| Select | Thinking mode |
| Tooltip | Ações por ícone |
| Avatar | Identidade do usuário/assistente |
| Badge | Status de upload/thinking |
| Progress | Upload |
| Skeleton | Loading |
| Toast/Sonner | Feedback |

## Componentes próprios

```txt
ChatComposer
MessageBubble
AssistantMarkdown
CodeBlock
AttachmentPreview
AudioRecorderButton
ThinkingModeSelector
ConversationList
ThemeToggle
```

## Acessibilidade visual

- Contraste adequado no dark mode.
- Foco visível.
- Tamanho mínimo de hit target: 44px.
- Estados hover/focus/disabled.
- Labels para botões de ícone.
