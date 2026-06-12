# Chatbot com IA Generativa — Python Assistant

## Objetivo

Criar um chatbot focado em programação Python.

## Prompt system

```txt
Você é um assistente sênior especializado em Python.
Responda em português.
Explique passo a passo quando necessário.
Inclua exemplos de código claros.
Quando houver risco de erro, avise.
Não invente APIs.
Priorize Flask, FastAPI, SQLAlchemy, testes, arquitetura e boas práticas.
```

## Thinking mode

O frontend envia:

```json
{
  "thinking_mode": "fast"
}
```

O backend mapeia:

| Modo | Temperatura | Instrução |
|---|---:|---|
| fast | 0.2 | Seja direto e objetivo |
| balanced | 0.3 | Explique com exemplos |
| deep | 0.2 | Analise trade-offs e detalhe |

## Exemplo de pergunta

```txt
Como criar uma lista em Python?
```

## Exemplo de resposta esperada

```txt
Em Python, uma lista é criada usando colchetes.

Exemplo:

numbers = [1, 2, 3]
names = ["Ana", "Bruno", "Carla"]

Você pode acessar elementos pelo índice:

print(names[0])  # Ana

E pode adicionar novos itens com append:

names.append("Daniel")
```

## Gateway

```python
class ChatCompletionGateway:
    def answer(self, question: str, thinking_mode: str) -> str:
        raise NotImplementedError
```

## Testabilidade

Nos testes unitários:

- não chamar OpenAI;
- usar fake gateway;
- validar prompt;
- validar tratamento de pergunta vazia;
- validar mapeamento de thinking mode.

## LangSmith

LangSmith deve ser habilitado por env:

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=replace-me
LANGSMITH_PROJECT=python-ai-assistant
```

## Segurança

- A chave OpenAI nunca deve ir para o frontend.
- Logs não devem guardar arquivos sensíveis.
- Respostas devem ser rastreáveis por request ID.
