# Observabilidade, Logs e Tracing

## Frontend

Registrar eventos técnicos sem dados sensíveis:

- app loaded;
- message sent;
- upload started;
- upload failed;
- stream started;
- stream finished;
- theme changed;
- audio permission denied.

## Backend

Usar logs estruturados:

```json
{
  "level": "INFO",
  "request_id": "req_123",
  "event": "chat.message.created",
  "session_id": "session_123"
}
```

## LangSmith

Usar para:

- tracing de chamadas LLM;
- inspeção de prompts;
- latência;
- avaliação de respostas;
- debug de chains.

## Métricas úteis

| Métrica | Motivo |
|---|---|
| Latência do chat | UX |
| Tempo de primeiro token | Streaming |
| Erros por endpoint | Estabilidade |
| Tamanho médio de upload | Custo |
| Tokens por resposta | Custo IA |
| Taxa de retry | Qualidade API |

## Request ID

Todo request deve ter um ID.

Frontend pode receber:

```txt
x-request-id: req_123
```

Backend deve propagar para logs.

## Erros no frontend

Mostrar mensagens amigáveis:

```txt
Não foi possível enviar sua mensagem. Tente novamente.
```

Mas logar tecnicamente:

```txt
POST /chat/messages failed with 500
```
