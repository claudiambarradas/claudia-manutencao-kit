---
name: ops-workflow-debug
description: Use when a workflow or webhook pipeline is broken — n8n, Make, Zapier, OpenClaw, GitHub Actions, cron-triggered scripts, or any multi-step automation. Symptoms include "the webhook is silent", "step X is not firing", "data is not arriving in Y", "workflow was edited and stopped working". Walks the pipeline end-to-end to isolate the broken hop.
---

# ops-workflow-debug

## Quando usar

- Webhook nao chega no destino.
- Workflow foi editado e parou de funcionar (caso classico: n8n nao republicado).
- Dado entra mas nao sai do outro lado.
- Integracao entre 2 servicos silenciou.

## Pre-requisito

`infra-snapshot.md` com o workflow listado. Se nao estiver, adicione antes.

## Passo a passo

### 1. Desenhe o pipeline

Peca ao usuario (ou deduza do snapshot) a sequencia:

```
[Trigger] -> [Passo 1] -> [Passo 2] -> [Destino final]
```

Exemplo:
```
[Hotmart webhook] -> [OpenClaw workflow "new-buyer"] -> [Supabase insert] -> [Telegram notif]
```

### 2. Descubra onde o dado morre

Comece pelo **final** e volte. Mais rapido.

Para cada hop, pergunte: "o dado chegou aqui?"

- **Destino final:** checa se o registro esperado existe (query no banco, mensagem no canal, arquivo no bucket).
- **Penultimo passo:** tem log dele processando? ou so silencio?
- Continue voltando ate achar o primeiro passo que **recebeu** dado e o primeiro que **nao recebeu**. A quebra ta entre eles.

### 3. Causas mais comuns por tipo de plataforma

**n8n / OpenClaw:**
- Workflow foi editado mas nao republicado. Faca: abra, "Activate" toggle, salve.
- Node de HTTP com URL errada ou metodo trocado.
- Credenciais expiradas no node.
- Filtro/condicional silencioso descartando o dado.

**Webhook direto (sem plataforma):**
- URL errada (endpoint renomeado).
- HTTPS cert expirado.
- Nginx/proxy reverso com rota quebrada.
- Servico por tras do webhook caido.

**Make / Zapier:**
- Plano estourou a cota do mes.
- Scenario/zap pausado automaticamente por erro.
- Conexao OAuth precisa reautenticar.

**GitHub Actions:**
- Workflow file com sintaxe errada no YAML.
- Secret expirado.
- Runner sem permissao.

**Cron + script:**
- Script nao tem shebang ou permissao de execucao.
- PATH do cron nao tem o binario (node, python, etc).
- Working directory diferente — caminhos relativos quebram.
- Script precisa de variavel de ambiente que o cron nao carrega (`.env` nao e lido automaticamente).

### 4. Teste manualmente o hop suspeito

Se voce acha que a quebra e no passo 2, rode o passo 2 isolado com um payload conhecido:

```bash
curl -X POST <url-do-hop> -H "Content-Type: application/json" -d '<payload-exemplo>'
```

Veja resposta. Compare com o que o passo 1 envia (pega do log do passo 1 se houver).

### 5. Relate

```
Pipeline: A -> B -> C -> D

Dado ultimo visto em: B (log B mostra processamento as 14:02)
Dado nao chegou em: C (nenhum registro apos 13:00)

Suspeita: quebra na chamada B->C.
Teste manual: curl em C com payload de B retornou 500.
Causa provavel: <especifica>

Correcao sugerida: <passo concreto>
```

### 6. Ofereca correcao — nao execute direto

Especialmente se for re-publicar workflow, rotacionar credencial, ou mexer em producao. Confirme antes.

## Regra de ouro

**Editou workflow? Republica.** Muitas plataformas (n8n inclusive) nao ativam edicao automaticamente. Se o workflow foi editado recentemente e silenciou, essa e a primeira hipotese.
