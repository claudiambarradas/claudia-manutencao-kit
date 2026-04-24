---
name: ops-agent-triage
description: Use when the user reports a specific agent/bot is broken, silent, stopped, or misbehaving (e.g. "o bot X parou", "agente Y nao ta respondendo", "nao recebi o relatorio de hoje"). Runs a guided diagnostic walking through the likely failure points in order — cron fired? process alive? webhook reachable? API token valid? quota exceeded? Stops at the first smoking gun.
---

# ops-agent-triage

## Quando usar

- Usuario diz: "o agente X parou", "nao recebi o relatorio", "o bot ta mudo", "tava funcionando ontem".
- Um vermelho apareceu no `ops-health-check` pra um agente especifico.

## Pre-requisito

`infra-snapshot.md` deve existir. Se nao, rode `ops-infra-scan` primeiro.

## Passo a passo

### 1. Identifique o agente

Pergunte ou deduza pelo nome. Abra o snapshot e pegue:
- Onde roda (Mac / VPS / cloud)
- Como e disparado (cron / webhook / manual)
- Dependencias (APIs externas, bancos, tokens)
- Caminho do log

Se o agente nao esta no snapshot, pergunte e adicione antes de prosseguir.

### 2. Checklist de diagnostico (na ordem)

Rode ate achar a primeira coisa quebrada. Nao pule etapas.

**A. O disparador disparou?**
- Cron: `grep <nome-do-job> /var/log/syslog` na VPS (ou `journalctl -u cron`). Ultima execucao?
- LaunchAgent (Mac): `launchctl list | grep <label>`. Ultima linha mostra exit status.
- Webhook: bate `curl -sI <url>` e ve se responde. Se for webhook que e chamado externamente, veja o log de quem chama.

**B. O processo rodou?**
- Se cron: cheque log do agente. Se o log nao tem entrada do horario esperado, o processo nao rodou (ou nao logou).
- Se daemon: `systemctl status <service>` ou `ps aux | grep <processo>`.

**C. O processo completou sem erro?**
- Ultimas linhas do log: tem stack trace? timeout? "connection refused"?
- Exit code (se disponivel via launchctl/systemctl)

**D. Dependencias externas estao vivas?**
- API externa que o agente chama: teste manualmente com `curl` usando as credenciais.
- Token valido? Use `ops-token-expiry-watch` se desconfiar.
- Quota estourada? Muitos erros 429 ou 403 no log.

**E. Dados de entrada existem?**
- Se o agente espera uma tabela/fila/arquivo, ele existe? Tem dados? Tem dados novos desde a ultima execucao boa?

### 3. Relate o achado

Ao achar a primeira quebra, pare e relate:

```
Agente: <nome>
Ultima execucao saudavel: <quando>
Primeira quebra: <etapa>
Evidencia: <linha do log ou saida do comando>

Causa provavel: <hipotese>
Proximo passo sugerido: <acao especifica>
```

### 4. Ofereca correcao — sem executar

Sempre proponha. Nunca aplique sem "ok" explicito. Especialmente:
- Restart de servico
- Re-publicar workflow
- Rotacao de token
- Limpeza de fila/tabela

### 5. Se for webhook/workflow

Se a pista apontar pra webhook ou automacao tipo n8n/Make/OpenClaw, transfira pra `ops-workflow-debug` — ela e especializada.

## Regras

- Um diagnostico por vez. Nao investigue 3 agentes em paralelo — foca.
- Se o cron nao disparou, PARE de investigar o codigo do agente. A causa ta antes.
- Se re-rodar manualmente pra testar, avise o usuario primeiro e execute o comando identico ao do cron (nao simplifique — o bug pode estar na diferenca).
