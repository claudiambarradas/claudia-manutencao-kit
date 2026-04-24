# Memory Templates

Essa pasta contem templates de memorias pro Claude — **nao sao ativas automaticamente**. Sao referencia.

## Como usar

Cada arquivo aqui e um exemplo de memoria bem-estruturada. Pra ativar uma delas:

1. Abra o Claude Code normalmente.
2. Fale pra ele: "Saiba isso: [cola o conteudo do template]".
3. Ele vai salvar em `~/.claude/projects/<projeto-atual>/memory/` com o nome adequado e atualizar o `MEMORY.md`.

Ou voce copia manualmente o arquivo pra la.

## O que tem aqui

- **`feedback_editou_workflow_republica.md`** — lembrar de reativar workflow apos editar.
- **`feedback_sem_acao_destrutiva.md`** — nunca executar rm/drop/reset sem confirmar.
- **`feedback_timezone_explicito.md`** — crons precisam ter TZ explicitado.
- **`feedback_secrets_nunca_inline.md`** — nunca logar tokens no terminal.
- **`reference_infra_snapshot_guia.md`** — guia do arquivo `infra-snapshot.md`.

## Tipos de memoria

- **feedback** — regra de comportamento pro Claude seguir.
- **project** — fato sobre o projeto/negocio que muda com o tempo.
- **reference** — ponteiro pra recurso externo ou arquivo interno.
- **user** — info sobre o usuario (voce).

Veja mais em: `~/.claude/` (procure por `auto memory` na doc do Claude Code).
