# Especificação UI/UX — Chat Moderno

## Referência visual

As imagens anexadas mostram uma aplicação de chat com:

- sidebar lateral no desktop;
- lista de conversas recentes;
- área central de mensagens;
- composer fixo na parte inferior;
- suporte a tema claro e escuro;
- layout responsivo para tablet e mobile;
- menu compacto em telas menores;
- botões de ação próximos ao input;
- visual limpo, com bastante espaço em branco no tema claro;
- contraste alto no tema escuro.

## Importante

A aplicação deve ser semelhante em experiência, mas não deve copiar marca, nome, logo ou identidade visual de terceiros.

## Layout desktop

```txt
┌──────────────────────────────────────────────────────────────┐
│ Sidebar        │ Header                                      │
│                ├─────────────────────────────────────────────┤
│ Novo chat      │                                             │
│ Buscar         │              MessageList                    │
│ Conversas      │                                             │
│                │                                             │
│                ├─────────────────────────────────────────────┤
│ User footer    │ ChatComposer                                │
└──────────────────────────────────────────────────────────────┘
```

## Layout mobile

```txt
┌──────────────────────┐
│ ☰           ⋯        │
├──────────────────────┤
│                      │
│     MessageList      │
│                      │
├──────────────────────┤
│ + input mic send     │
└──────────────────────┘
```

## Componentes visuais

| Componente | Descrição |
|---|---|
| AppShell | Estrutura geral |
| ChatSidebar | Histórico e navegação |
| ChatHeader | Título, thinking mode e ações |
| MessageList | Lista virtualizada de mensagens |
| MessageBubble | Mensagem do usuário ou assistente |
| AssistantMessage | Render com markdown e código |
| ChatComposer | Input, anexos, áudio e envio |
| AttachmentTray | Pré-visualização de arquivos |
| ThinkingModeSelect | Rápido, equilibrado, profundo |
| ThemeToggle | Claro/escuro/sistema |
| MobileNav | Menu compacto |
| EmptyState | Tela inicial com sugestões |

## Estados da conversa

| Estado | UI |
|---|---|
| empty | Sugestões de perguntas sobre Python |
| typing | Cursor/loader no assistente |
| streaming | Tokens surgindo progressivamente |
| uploading | Barra de progresso |
| recording | Indicador vermelho/pulsante |
| error | Card com retry |
| offline | Banner de conexão |

## Animações

Usar Motion/Framer Motion para:

- entrada de mensagens;
- abertura da sidebar mobile;
- exibição do attachment tray;
- troca de tema suave;
- feedback de gravação de áudio;
- skeleton loading.

## Regras de UX

- O input deve permanecer visível no fundo.
- `Enter` envia mensagem.
- `Shift + Enter` quebra linha.
- `Esc` fecha menus e previews.
- Upload deve mostrar tipo, nome e tamanho.
- Áudio deve permitir cancelar antes de enviar.
- Mensagens com código devem ter botão copiar.
- A resposta do assistente deve priorizar Python.
