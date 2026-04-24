---
name: ops-infra-scan
description: Use when the user wants to map their operational infrastructure for the first time, or refresh the map after adding/removing services. Interviews the user about their stack, scans their local Mac and (if they have one) their VPS, and generates an infra-snapshot.md file in memory that all other ops-* skills consult. Run this BEFORE any other ops-* skill — they depend on the snapshot existing.
---

# ops-infra-scan

## Quando usar

- Primeira vez que o usuario instala o kit.
- Quando ele adiciona/remove servico, agente, VPS, ou muda stack.
- Quando outra skill `ops-*` reclama que `infra-snapshot.md` nao existe.

## Objetivo

Gerar (ou atualizar) o arquivo `~/.claude/projects/<projeto>/memory/infra-snapshot.md` — um mapa vivo da infra do usuario. Esse arquivo vira a fonte de verdade que `ops-health-check`, `ops-agent-triage`, `ops-cron-audit`, etc. consultam.

## Passo a passo

### 1. Descubra onde salvar a memoria

O diretorio de memoria fica em `~/.claude/projects/` com um subdir especifico do projeto atual. Rode:

```bash
ls -1 ~/.claude/projects/ 2>/dev/null
```

Se houver varios, pergunte ao usuario qual e o projeto ativo (geralmente o que corresponde ao diretorio atual). Se nao existir, crie `~/.claude/projects/default/memory/`.

### 2. Entrevista basica (faca uma pergunta por vez)

Nao mande um paredao. Uma pergunta, espera resposta, proxima pergunta.

1. "Voce tem VPS? Se sim, me passa IP, usuario SSH e provedor."
2. "Que tipo de agentes ou bots voce tem? (ex: agente de relatorio diario, bot de atendimento no WhatsApp, scraper, etc.)"
3. "Voce usa n8n, Make, Zapier, OpenClaw, ou scripts proprios pra orquestrar?"
4. "Banco de dados? (Supabase, Postgres proprio, MySQL, nenhum)"
5. "Backup — o que voce protege, pra onde vai, com que frequencia?"
6. "Quais APIs externas sao criticas? (Meta, Google, Telegram, Z-API, OpenAI, outras)"

### 3. Escaneie o Mac local

```bash
# Sistema
uname -a
sw_vers

# Crons do usuario
crontab -l 2>/dev/null || echo "sem crontab"

# LaunchAgents (jeito nativo do Mac)
ls ~/Library/LaunchAgents/ 2>/dev/null
ls /Library/LaunchAgents/ 2>/dev/null
ls /Library/LaunchDaemons/ 2>/dev/null

# Processos node/python/bots rodando
ps aux | grep -iE "node|python|bun|deno" | grep -v grep | head -20

# Arquivos CLAUDE.md
find ~ -maxdepth 3 -name "CLAUDE.md" 2>/dev/null
```

### 4. Escaneie a VPS (se o usuario tiver)

Peca pra testar SSH primeiro:

```bash
ssh -o ConnectTimeout=5 <user>@<host> "echo ok"
```

Se funcionar, rode em sequencia:

```bash
ssh <user>@<host> bash -s <<'REMOTE'
echo "=== SISTEMA ==="
uname -a
lsb_release -d 2>/dev/null || cat /etc/os-release | head -3

echo "=== CRONS (root + user atual) ==="
crontab -l 2>/dev/null
sudo -n crontab -l 2>/dev/null || true
ls /etc/cron.d/ 2>/dev/null

echo "=== SERVICOS SYSTEMD USER ==="
systemctl --user list-units --type=service --state=running 2>/dev/null | head -20

echo "=== SERVICOS SYSTEMD SYSTEM (ativos) ==="
systemctl list-units --type=service --state=running 2>/dev/null | head -30

echo "=== PROCESSOS LONGOS (node/python/docker) ==="
ps aux | grep -iE "node|python|docker|n8n|openclaw" | grep -v grep | head -20

echo "=== DOCKER CONTAINERS ==="
docker ps 2>/dev/null || echo "sem docker"

echo "=== DISCO ==="
df -h / | tail -1

echo "=== UPTIME ==="
uptime
REMOTE
```

### 5. Monte o snapshot

Crie o arquivo `infra-snapshot.md` no diretorio de memoria. Estrutura:

```markdown
---
name: Infra Snapshot
description: Mapa vivo da infraestrutura operacional do usuario — stack, VPS, agentes, crons, servicos, backups
type: reference
---

# Infra Snapshot

**Ultima atualizacao:** <YYYY-MM-DD>

## Maquinas

### Mac local
- Hostname: ...
- OS: ...
- LaunchAgents ativos: ...
- Crons locais: ...

### VPS
- Provedor: ...
- IP / host: ...
- SSH: `ssh <user>@<host>`
- OS: ...
- Docker: [sim/nao, quais containers]
- Crons: ...
- Servicos systemd relevantes: ...

## Agentes / bots

Para cada agente, registre:
- Nome:
- Funcao:
- Onde roda: [Mac | VPS | cloud]
- Disparo: [cron | webhook | manual]
- Log: [caminho ou dashboard]
- Dependencias externas: [APIs, bancos]

## Workflows / automacoes

- Plataforma (n8n, Make, OpenClaw, script):
- Nome do fluxo:
- O que faz:
- Webhook URL (se aplicavel):

## Bancos / armazenamento

- ...

## Servicos externos e tokens

- Servico, pra que usa, onde recarrega token, quando vence (se souber)

## Backups

- O que: ...
- Onde: ...
- Frequencia: ...
- Comando de verificacao: ...

## Observacoes soltas

- [qualquer peculiaridade que o usuario mencionou — ex: "o webhook da Bianca precisa ser republicado apos editar"]
```

### 6. Atualize o MEMORY.md index

Adicione uma linha em `MEMORY.md`:

```
- [infra-snapshot.md](infra-snapshot.md) — mapa vivo da infra (VPS, agentes, crons, servicos)
```

### 7. Confirme com o usuario

Mostre o caminho do arquivo gerado e pergunte se quer ajustar algo antes de salvar como referencia definitiva.

## Erros comuns

- **SSH falha:** pergunte se a chave certa esta no ssh-agent (`ssh-add -l`). Nao force.
- **Usuario nao tem VPS:** tudo bem, pule a secao. O snapshot vira so-local.
- **Varios projetos em `~/.claude/projects/`:** pergunte qual. Nao adivinhe.
