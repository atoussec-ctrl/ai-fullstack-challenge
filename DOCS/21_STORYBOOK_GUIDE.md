# Storybook

## Objetivo

Criar, testar e documentar componentes isolados.

## Componentes prioritários

- Button variants.
- ChatComposer.
- MessageBubble.
- AssistantMarkdown.
- ThinkingModeSelector.
- AttachmentPreview.
- AudioRecorderButton.
- ChatSidebar.
- EmptyState.
- ThemeToggle.

## Instalação sugerida

```bash
pnpm dlx storybook@latest init
```

## Story de exemplo

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { ChatComposer } from "./ChatComposer";

const meta = {
  title: "Widgets/ChatComposer",
  component: ChatComposer,
  args: {
    disabled: false,
    onSubmit: console.log,
    onAttach: console.log,
    onRecordAudio: console.log,
  },
} satisfies Meta<typeof ChatComposer>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const Disabled: Story = {
  args: {
    disabled: true,
  },
};
```

## Estados que devem existir no Storybook

| Componente | Estados |
|---|---|
| ChatComposer | default, disabled, with attachments |
| MessageBubble | user, assistant, streaming, error |
| Sidebar | empty, many sessions, mobile |
| AttachmentPreview | image, pdf, audio, invalid |
| ThemeToggle | light, dark, system |
| EmptyState | default, with suggestions |

## MSW no Storybook

Usar MSW para simular:

- lista de sessões;
- mensagens;
- envio de mensagem;
- upload;
- erro de API.

## Benefícios

- Documentação visual.
- Testes manuais rápidos.
- Reduz regressões de UI.
- Facilita revisão por avaliadores.
