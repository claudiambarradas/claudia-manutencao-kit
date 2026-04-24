---
name: Guia do infra-snapshot.md
description: Explicacao de para que serve o infra-snapshot.md e quando atualiza-lo
type: reference
---

O arquivo `infra-snapshot.md` (gerado pela skill `ops-infra-scan`) e o mapa vivo da infra operacional. Todas as skills `ops-*` leem ele antes de agir.

**Quando atualizar:**
- Adicionou ou removeu agente/bot.
- Migrou pra nova VPS ou mudou IP.
- Trocou de plataforma de workflow (ex: saiu de n8n pra Make).
- Trocou provedor de backup.
- Rotacionou tokens de forma estrutural (nao o valor — a estrutura de renovacao).

**Como atualizar:**
Rodar a skill `ops-infra-scan` de novo. Ela detecta mudancas e atualiza o arquivo.

**O que NAO colocar:**
- Valores de tokens/senhas (so referencia a onde vivem).
- Dados pessoais que nao sao necessarios pra manutencao.
