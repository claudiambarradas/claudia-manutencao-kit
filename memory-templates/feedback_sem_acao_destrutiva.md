---
name: Nunca executar acao destrutiva sem confirmacao explicita
description: Antes de rm/drop/reset/kill/delete em producao ou infra, sempre pedir "ok" explicito
type: feedback
---

Nunca executar acoes destrutivas sem confirmacao explicita do usuario, mesmo que o contexto sugira que e seguro.

**Why:** Acoes destrutivas em infra (`rm -rf`, `DROP TABLE`, `git reset --hard`, `crontab -r`, `systemctl stop`, restore em cima de prod) sao dificeis ou impossiveis de reverter. O custo de perguntar "posso?" e zero, o custo de errar e caro demais.

**How to apply:** Sempre que for propor uma acao destrutiva, mostre o comando exato, explique o efeito em uma linha, e pergunte "pode executar?". Espere "sim", "pode", "ok", ou equivalente antes de rodar. Um "ok" passado em outro contexto nao autoriza a acao atual.
