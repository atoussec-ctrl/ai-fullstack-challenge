# Playwright — Especificações E2E

## Objetivo

Validar fluxos críticos em navegador real.

## Fluxos mínimos

### E2E-001 — Abrir aplicação

```txt
Dado que o usuário acessa /
Então deve ver o composer
E deve ver sugestões de perguntas sobre Python
```

### E2E-002 — Enviar mensagem

```txt
Dado que o usuário está na tela inicial
Quando digita "Como criar uma lista em Python?"
E clica em enviar
Então a mensagem deve aparecer na conversa
E uma resposta do assistente deve aparecer
```

### E2E-003 — Trocar tema

```txt
Dado que o usuário está no app
Quando troca para tema escuro
Então a classe dark deve estar ativa
E a preferência deve persistir após reload
```

### E2E-004 — Selecionar thinking profundo

```txt
Dado que o usuário seleciona "Profundo"
Quando envia uma mensagem
Então o request deve conter thinking_mode = "deep"
```

### E2E-005 — Anexar imagem

```txt
Dado que o usuário está no composer
Quando anexa uma imagem
Então deve ver preview
E deve conseguir remover antes do envio
```

### E2E-006 — Mobile

```txt
Dado viewport mobile
Então a sidebar deve estar oculta
E deve existir botão de menu
E o composer deve permanecer fixo no rodapé
```

## Exemplo Playwright

```ts
import { expect, test } from "@playwright/test";

test("usuário envia pergunta sobre lista em Python", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel("Mensagem para o assistente Python").fill("Como criar uma lista em Python?");
  await page.getByLabel("Enviar mensagem").click();

  await expect(page.getByText("Como criar uma lista em Python?")).toBeVisible();
  await expect(page.getByLabel("Resposta do assistente")).toBeVisible();
});
```

## Boas práticas

- Usar `getByRole` e `getByLabel`.
- Não depender de classes CSS.
- Mockar backend no CI quando necessário.
- Manter E2E pequeno e focado.
- Capturar trace em falha.
