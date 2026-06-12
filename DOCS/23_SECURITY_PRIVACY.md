# Segurança e Privacidade

## Segredos

- Nunca enviar `OPENAI_API_KEY` ao frontend.
- Nunca versionar `.env`.
- Usar `.env.example`.
- Usar secret scanning no CI.

## Uploads

### Frontend

- Validar extensão.
- Validar tamanho.
- Mostrar erro legível.
- Não executar arquivos.
- Revogar Object URLs.

### Backend

- Revalidar MIME.
- Limitar tamanho.
- Sanitizar nome.
- Salvar com ID interno.
- Não confiar no filename original.
- Não expor path local.
- Verificar PDF/imagem antes de processar.

## IA

- Não enviar dados sensíveis sem aviso.
- Não logar conteúdo completo de arquivos por padrão.
- Permitir apagar conversa futuramente.
- Registrar `request_id`, não segredo.

## CORS

No desenvolvimento:

```txt
http://localhost:5173 → http://localhost:5000
```

Em produção:

- permitir apenas domínios oficiais;
- não usar `*` com credenciais.

## Headers

Recomendações futuras:

- Content-Security-Policy.
- X-Content-Type-Options.
- Referrer-Policy.
- Permissions-Policy para microfone.

## Acessos do browser

Microfone deve solicitar permissão apenas quando usuário clicar em gravar.

## LGPD

Para produção:

- política de retenção de dados;
- opção de exclusão;
- aviso sobre envio de arquivos;
- minimização de dados.
