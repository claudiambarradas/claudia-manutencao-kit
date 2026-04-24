# Minha Infra

> Template do Kit de Manutencao IA. Preencha os campos [entre colchetes].
> Se tiver duvida do que preencher, rode a skill `ops-infra-scan` — ela te entrevista
> e escaneia tudo pra preencher sozinha.

## Quem sou eu (operacionalmente)

- Nome: [seu nome]
- Negocio / projeto: [nome]
- Maquina principal: [MacBook / Mac Mini / Linux desktop]
- Fuso horario: [ex: America/Sao_Paulo]

## Minha VPS

- Provedor: [Hostinger / Hetzner / DigitalOcean / nao tenho]
- IP / hostname: [ex: 123.45.67.89 ou srv.meudominio.com]
- Usuario SSH: [ex: root, ubuntu, seu_user]
- Chave SSH: [~/.ssh/id_ed25519 ou caminho da chave]
- Sistema: [ex: Ubuntu 22.04]
- Funcao: [o que roda la — agentes, bots, scripts, banco, etc.]

## Meus agentes / bots

> Liste cada agente com: nome, o que faz, como e disparado, onde loga.

- **[nome-do-agente]** — [o que faz]. Roda via [cron / webhook / manual]. Log em [caminho].
- **[...]**

## Meus workflows / automacoes

> Tipos: n8n, Make, Zapier, OpenClaw, scripts Python, GitHub Actions, etc.

- **[nome]** — [o que faz]. Plataforma: [n8n/Make/...]. URL: [se aplicavel].

## Meus servicos externos

> APIs e plataformas que voce paga / depende.

- **[Supabase / Vercel / Meta / Google / Telegram / ...]** — [pra que uso]

## Meus backups

- O que e protegido: [banco de dados / arquivos / codigo / ...]
- Onde: [Backblaze B2 / Drive / S3 / ...]
- Frequencia: [diario / semanal]
- Como verifico: [comando / dashboard / ...]

## Tokens e credenciais com expiracao

> NAO cole secrets aqui. Liste so o que existe e quando vence.

- **[nome do token]** — vence em [data]. Onde recarrega: [link do painel].

## Regras da operacao (como eu gosto que a IA me ajude)

- Sempre responder em portugues brasileiro.
- Nunca executar acoes destrutivas (rm -rf, reset --hard, drop table) sem confirmar.
- Ao editar workflow n8n/automacao, sempre lembrar de reativar/publicar.
- [suas proprias regras aqui — veja memory-templates/ pra exemplos]
