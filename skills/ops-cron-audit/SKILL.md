---
name: ops-cron-audit
description: Use when the user wants to audit all scheduled jobs on their machines — Mac (crontab + launchd) and VPS (crontab + /etc/cron.d + systemd timers). Lists every job, explains what each one does in plain Portuguese, flags orphans (job without known purpose), broken schedules, duplicates, and timezone surprises.
---

# ops-cron-audit

## Quando usar

- "Que crons eu tenho rodando?"
- Suspeita de cron orfa/duplicada comendo recurso.
- Apos migracao de VPS — conferir se tudo foi transportado.
- Checagem trimestral de higiene.

## Pre-requisito

`infra-snapshot.md` — pra comparar o que **deveria** existir com o que **existe de fato**.

## Passo a passo

### 1. Colete tudo

**Mac local:**
```bash
# Crontab do usuario
echo "=== crontab do usuario ==="
crontab -l 2>/dev/null

# LaunchAgents do usuario
echo "=== LaunchAgents (usuario) ==="
ls -1 ~/Library/LaunchAgents/*.plist 2>/dev/null

# LaunchAgents globais
echo "=== LaunchAgents (sistema) ==="
ls -1 /Library/LaunchAgents/*.plist 2>/dev/null

# LaunchDaemons
echo "=== LaunchDaemons ==="
ls -1 /Library/LaunchDaemons/*.plist 2>/dev/null
```

**VPS:**
```bash
ssh <user>@<host> bash -c '
  echo "=== crontab root ==="
  sudo -n crontab -l 2>/dev/null || crontab -l 2>/dev/null
  echo "=== /etc/cron.d ==="
  ls -1 /etc/cron.d/ 2>/dev/null
  for f in /etc/cron.d/*; do echo "--- $f ---"; cat "$f"; done 2>/dev/null
  echo "=== cron.hourly/daily/weekly/monthly ==="
  ls -1 /etc/cron.hourly /etc/cron.daily /etc/cron.weekly /etc/cron.monthly 2>/dev/null
  echo "=== systemd timers ==="
  systemctl list-timers --all --no-pager 2>/dev/null | head -30
'
```

### 2. Decodifique os schedules

Para cada linha de cron, traduza `* * * * *` em portugues:
- `0 9 * * *` -> "todo dia as 09:00"
- `*/15 * * * *` -> "a cada 15 minutos"
- `0 3 * * 0` -> "domingo as 03:00"
- `0 */2 * * *` -> "a cada 2 horas, em ponto"

**Cuidado com timezone:** cron usa o TZ do sistema. Pergunte ou cheque `timedatectl` (Linux) / `date` (Mac). Se a VPS estiver em UTC mas o usuario pensa em BRT, "9h" pode virar "6h local". Sempre avise.

### 3. Classifique cada job

Compare com a secao "Agentes" do `infra-snapshot.md`:

- ✅ **Conhecida:** bate com agente listado no snapshot.
- ❓ **Orfa:** existe no sistema mas nao esta no snapshot. Pode ser legit esquecido OU lixo.
- ⚠️ **Duplicada:** dois jobs rodando a mesma coisa (ex: 2 crons chamando o mesmo script em horarios proximos).
- ❌ **Quebrada:** sintaxe invalida, binario nao existe, caminho errado.

### 4. Investigue orfas (com o usuario)

Para cada ❓, pergunte: "Voce reconhece esse cron? `<linha>` — ultima execucao: `<quando>`, script: `<caminho>`."

Ofereca opcoes:
- Adicionar no snapshot (era legit, so nao tinha sido registrada)
- Remover (era lixo de teste antigo)
- Investigar (nao sabe o que e)

**Nao delete nada automaticamente.** Nunca.

### 5. Relate

```
Auditoria de crons — <data>

VPS (srv.cliente.com)
  ✅ 5 crons conhecidos (batem com snapshot)
  ❓ 1 orfa: "* * * * * /root/old-test.sh" — ultima exec: 2025-01-03 (ha 1 ano)
  ⚠️ 1 duplicada: backup.sh roda as 02:00 (cron.d) E as 02:15 (crontab root)
  ❌ 1 quebrada: "0 6 * * * /usr/bin/node /scripts/daily.js" — /scripts/daily.js nao existe

Mac local
  ✅ 2 LaunchAgents conhecidos
  ❓ 1 orfa: com.claudia.teste.plist

Timezone: VPS em UTC (BRT = UTC-3). "9h na VPS" = "6h no seu relogio".

Acoes sugeridas (confirmar cada uma):
  1. Remover cron orfa old-test.sh?
  2. Consolidar duplicacao do backup?
  3. Investigar cron quebrada do daily.js — o script existe em outro caminho?
```

### 6. Nao delete sem confirmacao

Mesmo que seja obvio, sempre pergunte.

## Regras

- Um `rm` ou `crontab -r` so com "ok, pode remover X" explicito.
- Backup do crontab atual antes de editar: `crontab -l > ~/crontab-backup-$(date +%F).txt`.
- Ao editar `/etc/cron.d/` via SSH, sempre via editor temporario — nao use `echo >>`.
