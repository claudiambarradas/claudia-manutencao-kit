---
name: Editou workflow automatizado? Sempre republicar
description: Muitas plataformas de workflow (n8n, Make, algumas no-code) nao ativam edicoes automaticamente — precisa toggle de ativacao apos salvar
type: feedback
---

Sempre que eu editar um workflow de automacao (n8n, Make, OpenClaw, etc.), antes de encerrar a conversa: **lembrar a Claudia de reativar/republicar o workflow.**

**Why:** Ja aconteceu de um bot ficar mudo por >24h porque o workflow foi editado e o toggle de "Active" nao foi religado. A edicao salva mas nao executa ate voce re-ativar.

**How to apply:** Ao terminar qualquer mudanca em plataforma de workflow, encerrar a resposta com um lembrete explicito: "Nao esqueca de ativar o workflow no painel antes de fechar." Se possivel, validar via webhook-test que o workflow esta processando input novamente.
