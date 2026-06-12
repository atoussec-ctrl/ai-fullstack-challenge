# Funcionalidades Frontend

## Chat textual

### Fluxo

```txt
Usuário digita pergunta
  ↓
Seleciona thinking mode
  ↓
Clica em enviar ou pressiona Enter
  ↓
Mensagem aparece como pending
  ↓
Frontend chama Flask
  ↓
Resposta inicia streaming
  ↓
Mensagem final é persistida
```

## Sugestões iniciais

Exemplos:

- Como criar uma lista em Python?
- Explique decorators em Python.
- Como criar uma API com Flask?
- Como testar endpoints com pytest?
- Como usar SQLAlchemy com SQLite?

## Thinking mode

| Modo | Label | Descrição |
|---|---|---|
| fast | Rápido | Respostas curtas |
| balanced | Equilibrado | Respostas com exemplo |
| deep | Profundo | Análise detalhada |

## Upload de documentos

Tipos aceitos no MVP:

- `.txt`
- `.md`
- `.py`
- `.json`
- `.pdf`

## Upload de imagens

Tipos aceitos:

- `image/png`
- `image/jpeg`
- `image/webp`

Uso esperado:

- print de erro;
- diagrama;
- screenshot de código;
- tela de terminal.

## Áudio

O usuário pode:

- gravar áudio no navegador;
- cancelar gravação;
- enviar áudio;
- anexar áudio à mensagem.

O backend decide se transcreve ou processa diretamente.

## Histórico

- Criar nova conversa.
- Renomear conversa.
- Buscar conversas.
- Remover conversa.
- Fixar conversa futuramente.

## Configurações

- Tema: claro, escuro, sistema.
- Thinking padrão.
- Tamanho de fonte.
- Preferência por respostas curtas ou detalhadas.
