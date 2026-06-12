# Tema, Responsividade e Acessibilidade

## Tema

Suportar:

- claro;
- escuro;
- sistema.

Persistência:

```txt
localStorage.theme = "light" | "dark" | "system"
```

## ThemeProvider

```tsx
import { createContext, useContext, useEffect, useMemo, useState } from "react";

type Theme = "light" | "dark" | "system";

interface ThemeContextValue {
  theme: Theme;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<Theme>(() => {
    return (localStorage.getItem("theme") as Theme | null) ?? "system";
  });

  useEffect(() => {
    const root = document.documentElement;
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const shouldUseDark = theme === "dark" || (theme === "system" && prefersDark);

    root.classList.toggle("dark", shouldUseDark);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const value = useMemo(() => ({ theme, setTheme: setThemeState }), [theme]);

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const context = useContext(ThemeContext);

  if (!context) {
    throw new Error("useTheme deve ser usado dentro de ThemeProvider");
  }

  return context;
}
```

## Responsividade

### Breakpoints sugeridos

| Breakpoint | Layout |
|---|---|
| `< 640px` | Mobile, sidebar em Sheet |
| `640px - 1024px` | Tablet, sidebar colapsável |
| `> 1024px` | Desktop com sidebar fixa |

## Acessibilidade

### Requisitos

- Navegação por teclado.
- `aria-label` em botões de ícone.
- `aria-live` na resposta em streaming.
- Foco retorna ao input após envio.
- Upload acessível por botão e drag-and-drop.
- Erros anunciados por `role="alert"`.
- Campo de mensagem com label acessível.

## Exemplo

```tsx
<button type="button" aria-label="Enviar mensagem">
  <SendIcon aria-hidden="true" />
</button>
```

## Critérios de aceite

- Usuário consegue enviar mensagem sem mouse.
- Leitor de tela identifica o composer.
- Tema escuro não quebra contraste.
- Mobile não tem overflow horizontal.
