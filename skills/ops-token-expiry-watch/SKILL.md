---
name: ops-token-expiry-watch
description: Use when the user wants to audit API tokens and credentials for upcoming expiration — Meta Ads access tokens, Google OAuth refresh tokens, Telegram bot tokens, webhook secrets, SSL certificates, SSH keys. Tests each token by making a cheap authenticated call, reports expiry dates when the API exposes them, and flags anything expired or expiring soon.
---

# ops-token-expiry-watch

## Quando usar

- Checagem mensal de rotina.
- Depois que um agente caiu com erro de autenticacao.
- Antes de viajar / entrar em periodo critico (lancamento).

## Pre-requisito

`infra-snapshot.md` com a secao "Servicos externos e tokens" preenchida — nome do token, onde vive, onde renova. **NAO deve conter o valor do token.**

O valor do token fica em:
- `.env` do projeto
- Vault proprio (ex: `~/.claudia-vault/`)
- Secret manager (1Password, Bitwarden, provedor cloud)

## Passo a passo

### 1. Liste os tokens do snapshot

Pegue a lista de servicos externos. Para cada um, descubra:
- Onde esta o valor (qual `.env` ou cofre)
- Como testa (qual endpoint cheap de healthcheck)
- Como descobre expiracao (alguns exposem, outros nao)

### 2. Teste cada token

**Meta Ads / Facebook Graph:**
```bash
curl -s "https://graph.facebook.com/v19.0/me?access_token=$META_TOKEN" | head -c 200
# Expiracao:
curl -s "https://graph.facebook.com/debug_token?input_token=$META_TOKEN&access_token=$META_TOKEN" | jq '.data.expires_at'
```

**Google OAuth (refresh token):**
```bash
curl -s -X POST https://oauth2.googleapis.com/token \
  -d "client_id=$ID&client_secret=$SECRET&refresh_token=$REFRESH&grant_type=refresh_token" \
  | jq '.access_token' | head -c 50
# Se retornar access_token, o refresh token ainda funciona.
```

**Telegram Bot:**
```bash
curl -s "https://api.telegram.org/bot$TG_TOKEN/getMe" | jq '.ok'
# true = vivo, false = revogado
```

**Z-API / API generica com auth header:**
```bash
curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOKEN" <endpoint-health>
# 200 = vivo, 401/403 = problema
```

**SSL/TLS certificado de dominio:**
```bash
echo | openssl s_client -servername <dominio> -connect <dominio>:443 2>/dev/null | openssl x509 -noout -dates
```

**SSH key:**
```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 <user>@<host> "echo ok" && echo "OK" || echo "FALHOU"
```

### 3. Classifique

- 🟢 **OK:** token responde, sem expiracao conhecida ou >60 dias pra expirar.
- 🟡 **Atencao:** expira em 7-60 dias.
- 🔴 **Urgente:** expira em <7 dias, ja expirado, ou retornou erro de auth.

### 4. Relate

```
Auditoria de tokens — <data>

🟢 Telegram bot (Bianca): vivo, sem expiracao
🟢 Supabase service key: vivo
🟡 Meta Ads access token: vence em 2026-05-14 (20 dias) — renovar no Business Manager
🟡 SSL cert belezadeempresa.com.br: vence em 2026-06-02 (38 dias) — Let's Encrypt auto-renova?
🔴 Google OAuth (Drive): refresh_token invalido — reautorizar em console.cloud.google.com

Acao prioritaria:
  1. Reautorizar Google OAuth agora — agente-X depende disso.
  2. Agendar lembrete pra renovar Meta Ads em 2026-05-07 (7 dias antes).
```

### 5. Ofereca agendar lembretes

Para tokens com expiracao conhecida, ofereca criar cron/schedule/lembrete X dias antes. Ex: "Quer que eu te avise dia 07/05 pra renovar o token Meta?"

## Regras

- **Nunca mostre o valor do token no output.** Nem nos primeiros/ultimos caracteres. Loga isso no terminal = loga em historico = vaza.
- **Nunca mande token em URL de GET publico** se puder evitar (usa header, nao query string).
- Se descobrir que um token JA vazou (cometado em repo, mandado em canal publico), pare e diga: "Esse token precisa ser revogado agora." Nao continue com outras checagens.
