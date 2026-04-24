---
name: ops-backup-verify
description: Use when the user wants to confirm their backups are actually working — not just scheduled. Checks last backup timestamp, size plausibility, and when possible performs a restore smoke-test. Triggers include "meu backup ta rodando?", "confere o backup", "quando foi o ultimo backup?", or routine monthly verification.
---

# ops-backup-verify

## Quando usar

- Verificacao mensal/trimestral de rotina.
- Depois de um incidente ou perda de dado.
- Quando o usuario desconfia que algo parou.

## Pre-requisito

`infra-snapshot.md` com a secao "Backups" preenchida (o que, onde, com que frequencia). Se nao tiver, peca pra preencher ou rode `ops-infra-scan` antes.

## Passo a passo

### 1. Puxe a configuracao do snapshot

Identifique:
- **O que** e protegido (banco, arquivos, codigo)
- **Onde** vai (Backblaze B2, S3, Drive, pasta local, etc.)
- **Como** (restic, rsync, pg_dump, borg, nativo do provedor)
- **Frequencia** esperada (diario, semanal)

### 2. Checagem automatizada (nao destrutiva)

Dependendo da ferramenta:

**restic (B2, S3, local):**
```bash
restic -r <repo> snapshots --last 5
restic -r <repo> stats latest
```
Cheque: ultimo snapshot ta dentro da janela esperada? Tamanho bate com o esperado?

**rsync pra pasta/servidor:**
```bash
ls -lht <destino> | head -10
du -sh <destino>
```

**pg_dump / dumps SQL:**
```bash
ls -lht <pasta-dumps> | head -5
# Ultimo dump: tamanho razoavel? nao-zero? data recente?
```

**Backup nativo do provedor** (ex: Hostinger, DigitalOcean, Supabase):
Acesse o painel ou API. Relate pro usuario o que ver (voce nao tem credenciais de painel).

### 3. Classifique

- 🟢 **OK:** ultimo backup dentro da janela, tamanho no esperado, nenhum erro.
- 🟡 **Suspeito:** atrasado mas ainda recente, ou tamanho mudou >50% pra menos sem razao obvia.
- 🔴 **Quebrado:** sem backup ha mais que 2x a frequencia esperada, tamanho zero, credencial falhando.

### 4. (Opcional) Restore smoke-test

Se o usuario pedir ou for checagem trimestral profunda, proponha um restore de teste:

```bash
# restic exemplo — restaura 1 arquivo pra /tmp pra conferir integridade
restic -r <repo> restore latest --target /tmp/restore-test --include /caminho/conhecido
ls -la /tmp/restore-test/
```

**Sempre restaure pra diretorio temporario**, nunca em cima do dado real.

### 5. Relate

```
Backup: <nome/stack>
Ultimo: <data+hora> (<ha quanto tempo>)
Tamanho: <X GB> (esperado: ~<Y GB>)
Saude: 🟢 / 🟡 / 🔴

Observacoes:
- <algo que chamou atencao>

Proxima acao:
- <se 🟢: nada, proxima verificacao em X>
- <se 🟡: investigar Y>
- <se 🔴: ACAO URGENTE — X>
```

### 6. Registre

Se o usuario quiser, atualize `infra-snapshot.md` com a data da ultima verificacao bem-sucedida. Util pra saber que a ultima auditoria foi mes passado e nao ano passado.

## Regras

- **Nunca restaure em cima do dado de producao** pra "testar".
- **Nao delete snapshots antigos** sem confirmacao explicita, mesmo que paracam duplicados.
- Se a credencial do backup ta na VPS e voce nao tem acesso, peca pro usuario rodar os comandos e colar a saida — nao tente forcar.
