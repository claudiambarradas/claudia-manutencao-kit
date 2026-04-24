---
name: ops-health-check
description: Use when the user asks "está tudo rodando?", "tá tudo de pé?", "como tá a infra?", or wants a fast status report of their operational stack. Reads infra-snapshot.md to know WHAT to check, then runs parallel probes on Mac + VPS (crons, agents, disk, services, recent logs) and returns a concise green/yellow/red report.
---

# ops-health-check

## Quando usar

- "Ta tudo rodando?" / "Como ta a infra?" / "Health check"
- Manha cedo, antes de comecar o dia
- Depois de uma mudanca grande (deploy, migracao)

## Pre-requisito

Precisa do `infra-snapshot.md` na memoria. Se nao existir, pare e peca pra rodar `ops-infra-scan` primeiro.

## Passo a passo

### 1. Leia o snapshot

```bash
cat ~/.claude/projects/<projeto>/memory/infra-snapshot.md
```

Identifique: VPS (tem/nao tem), agentes, crons esperados, servicos externos.

### 2. Rode probes em paralelo

Use uma so chamada Bash com multiplas verificacoes em paralelo (ampersand + wait), ou multiplas chamadas Bash no mesmo turno.

**Mac local:**
```bash
# Crons ativos
crontab -l 2>/dev/null | grep -cv "^#" || echo "0"

# LaunchAgents carregados
launchctl list | grep -vE "^(PID|-)" | wc -l

# Disco
df -h / | tail -1
```

**VPS (se houver):**
```bash
ssh <user>@<host> bash -c '
  echo "=== UPTIME ==="; uptime
  echo "=== DISCO ==="; df -h / | tail -1
  echo "=== MEMORIA ==="; free -h | head -2
  echo "=== SERVICOS CAIDOS ==="; systemctl list-units --type=service --state=failed --no-pager 2>/dev/null | head -10
  echo "=== DOCKER ==="; docker ps --format "table {{.Names}}\t{{.Status}}" 2>/dev/null || echo "sem docker"
  echo "=== CRONS RECENTES (ultimas 24h) ==="; grep CRON /var/log/syslog 2>/dev/null | tail -5 || journalctl -u cron --since "24 hours ago" --no-pager 2>/dev/null | tail -5
'
```

**Agentes especificos (do snapshot):**
Para cada agente listado, cheque o sinal de vida que faca sentido. Exemplos:
- Bot Telegram: testa se o webhook responde (`curl -s <webhook>/health` se houver endpoint)
- Agente com cron: confere ultimo arquivo de log ou registro no banco
- Webhook: `curl -sI <url>` pra ver se 200

### 3. Classifique cada item

- 🟢 **Verde:** rodando, dentro do esperado
- 🟡 **Amarelo:** rodando, mas algo suspeito (disco >80%, sem log ha >24h quando esperado diario)
- 🔴 **Vermelho:** caido, sem resposta, erro

### 4. Relatorio final

Curto. Exemplo:

```
Health check — <data>

VPS (srv.cliente.com)
  🟢 Uptime 12d, disco 34%, memoria OK
  🟢 Docker: 3 containers up
  🔴 cron "backup-diario" nao rodou nas ultimas 24h

Mac local
  🟢 3 LaunchAgents ativos
  🟡 Disco 82% — considere limpeza

Agentes
  🟢 agente-relatorio: ultimo log 07:15 hoje
  🔴 bot-whatsapp: webhook retornou 502

Acoes sugeridas:
  1. Investigar cron "backup-diario" (ver ops-backup-verify)
  2. Diagnosticar bot-whatsapp (ver ops-agent-triage)
```

### 5. Ofereca proximo passo

Se tem vermelho, ofereca rodar `ops-agent-triage` ou `ops-workflow-debug` pro item. Se tem amarelo de disco, ofereca investigar.

## Regras

- **Nao execute acoes corretivas** — so diagnostica. Fix e decisao do usuario.
- **Nao rode nada destrutivo** nem reinicie servicos sem pedir confirmacao.
- Se SSH falhar, reporte como vermelho e siga. Nao trave.
