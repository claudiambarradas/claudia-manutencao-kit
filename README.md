# Kit de Manutenção IA

Skills e templates pro Claude Code virar seu **assistente de manutenção de infra**: VPS, agentes, workflows, crons, backups, tokens.

Não é sobre marketing, conteúdo ou vendas. É sobre **manter tudo rodando** — com um bot que sabe onde olhar, o que checar, e o que te avisar.

## O que tem aqui

- **`skills/ops-infra-scan/`** — primeira skill a rodar. Varre seu Mac, pergunta da sua VPS (SSH), escaneia ela também, e monta um mapa da sua infra (`infra-snapshot.md`) que todas as outras skills consultam.
- **`skills/ops-health-check/`** — "tá tudo de pé?" Varre crons, agentes, serviços, últimos logs. Relatório de status em 30s.
- **`skills/ops-agent-triage/`** — "o agente X parou" — diagnóstico guiado: cron rodou? webhook respondeu? token vivo? quota estourou?
- **`skills/ops-workflow-debug/`** — webhook ou workflow quebrado (n8n, OpenClaw, Make, Zapier, o que for). Isola onde parou.
- **`skills/ops-backup-verify/`** — checa se o último backup rodou, se tem tamanho razoável, se tá íntegro.
- **`skills/ops-cron-audit/`** — lista todas as crons (Mac + VPS), explica cada uma em português, sinaliza órfãs/quebradas.
- **`skills/ops-token-expiry-watch/`** — varre tokens de APIs (Meta, Google, etc.) e avisa quais vão expirar.
- **`memory-templates/`** — feedbacks e referências prontos pro Claude saber as regras da sua operação.
- **`claude-md-template/CLAUDE.md`** — template de CLAUDE.md focado em ops (stack, VPS, agentes, serviços).

## Instalação

```bash
git clone https://github.com/claudiambarradas/claudia-manutencao-kit.git
cd claudia-manutencao-kit
./install.sh
```

O `install.sh` copia:
- Skills → `~/.claude/skills/`
- Templates de memória → `~/.claude/projects/.../memory/templates/`
- CLAUDE.md (só se você não tiver um) → `~/CLAUDE.md`

Depois, abre o Claude Code e diz:

> Roda a skill `ops-infra-scan` pra mapear minha infra.

Ele te entrevista, escaneia o que precisa escanear, e monta o snapshot. A partir daí, qualquer uma das outras skills já funciona.

## Filosofia

Cada skill é **abstrata de stack**. Não importa se você usa n8n, Make, OpenClaw, launchd, systemd, cron, Supabase, Railway, Hetzner, o que for — a skill pergunta ou descobre, e adapta.

O que personaliza é o **`infra-snapshot.md`** que o `ops-infra-scan` cria na sua memória. É ali que fica "ah, a VPS dela é a X, os agentes dela são Y, os backups rodam toda terça". Todas as outras skills leem esse arquivo antes de agir.

## Requisitos

- Claude Code instalado
- (Opcional) Acesso SSH à sua VPS, se você tiver uma
- (Opcional) `gh` CLI, se você quiser que o Claude abra issues/PRs no GitHub automaticamente

## Feito por

[@belezadeempresa](https://instagram.com/belezadeempresa) — se te ajudou, me marca.
