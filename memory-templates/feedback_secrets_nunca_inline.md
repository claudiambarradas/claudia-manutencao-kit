---
name: Nunca imprimir ou comitar valores de secrets/tokens
description: Tokens e senhas nunca aparecem no output do terminal nem em commits — exporte via env, nao mostre valores
type: feedback
---

Valores de tokens, senhas, chaves de API e secrets nunca devem aparecer no output do terminal, em logs, em mensagens, em commits git, nem em arquivos de memoria.

**Why:** Terminal logga no historico. Historico vaza (screenshot, compartilhamento de tela, backup do shell, sincronizacao de dotfiles). Commit em repo publico expoe pra sempre, mesmo que deletado depois (permanece no historico git). Um token vazado = um ataque em potencial.

**How to apply:** Sempre ler secrets via `$VAR_AMBIENTE` sem ecoar. Nunca usar `echo $TOKEN` nem `set -x` perto de secrets. Ao reportar auditoria de token, dizer "valido" ou "expirado", nunca os primeiros/ultimos caracteres. Se um secret for detectado em repo commitado, pare tudo: revogar imediatamente, nao apenas remover do proximo commit.
