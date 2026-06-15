---
name: utm-builder
description: Use when the user wants to create, standardize, or audit tracking links with UTM parameters (utm_source, utm_medium, utm_campaign, utm_content, utm_term) — "monta um link de rastreio", "gera UTM pro Instagram", "cria link pra campanha", "padroniza meus links", "de onde vieram meus cliques". Reads utm-registry.md to keep naming consistent, builds clean tagged URLs, and flags links that quebram o padrao.
---

# utm-builder

## Quando usar

- "Monta um link de rastreio pro post de hoje."
- "Gera UTM pro link da bio do Instagram."
- "Cria os links pra campanha de Dia das Maes."
- "Padroniza esses links que eu ja tenho."
- "Audita meus links — tem coisa fora do padrao?"

## Por que isso importa

UTM so serve se for **consistente**. `instagram`, `Instagram`, `IG` e `insta`
viram quatro fontes diferentes no relatorio — e ai voce nao sabe de onde veio
nada. Esta skill existe pra garantir que todo link sai com o **mesmo padrao**,
sempre.

## A fonte de verdade: utm-registry.md

O padrao do usuario vive em `~/.claude/projects/<projeto>/memory/utm-registry.md`.
E o equivalente do `infra-snapshot.md` pras outras skills: personaliza tudo.

**Antes de gerar qualquer link, leia o registry:**

```bash
cat ~/.claude/projects/*/memory/utm-registry.md 2>/dev/null
```

Se nao existir, crie na primeira vez (veja secao "Primeira vez" abaixo).

## Regras de formato (padrao do projeto)

Aplique sempre, sem excecao:

- **Tudo minusculo.** `instagram`, nunca `Instagram`.
- **Sem espaco nem acento.** Use hifen pra separar: `dia-das-maes`, nao
  `Dia das Mães`.
- **Sem caractere especial.** Nada de `&`, `?`, `#`, emoji, `/` nos valores.
- **Sem dado pessoal.** Nunca coloque nome, email ou telefone de cliente em UTM.
- Valores curtos e previsiveis. Prefira do vocabulario do registry.

Convencao base dos cinco parametros:

| Parametro      | O que e                          | Exemplos                          |
|----------------|----------------------------------|-----------------------------------|
| `utm_source`   | DE ONDE veio (plataforma)        | `instagram`, `whatsapp`, `google` |
| `utm_medium`   | TIPO de trafego                  | `social`, `bio`, `stories`, `cpc` |
| `utm_campaign` | QUAL acao/campanha               | `dia-das-maes-2026`, `lista-vip`  |
| `utm_content`  | QUAL variacao (opcional)         | `botao-azul`, `story-3`           |
| `utm_term`     | palavra-chave paga (opcional)    | `maquiagem-noiva`                 |

## Primeira vez: montar o registry

Entreviste rapido (uma pergunta por vez, sem paredao):

1. "Quais canais voce usa pra divulgar? (Instagram, WhatsApp, email, Google, etc.)"
2. "Qual o site/link de destino principal? (loja, agendamento, WhatsApp)"
3. "Voce ja tem algum jeito de escrever esses links, ou comecamos do zero?"

Depois crie `utm-registry.md`:

```markdown
---
name: UTM Registry
description: Padrao e vocabulario de links de rastreio (UTM) do usuario — fontes, midias, campanhas
type: reference
---

# UTM Registry

**Ultima atualizacao:** <YYYY-MM-DD>

## Destino padrao
- Site principal: https://...
- Agendamento: https://...
- WhatsApp: https://wa.me/55...

## Vocabulario aprovado

### utm_source (de onde)
- instagram
- whatsapp
- email
- google
- facebook

### utm_medium (tipo)
- bio        (link da bio)
- stories    (story)
- post       (post no feed)
- social     (organico generico)
- cpc        (anuncio pago)
- newsletter (email)

### utm_campaign (acoes recorrentes)
- lista-vip
- agendamento
- dia-das-maes-2026
- promo-<mes>

## Links ja gerados
| Data | Link curto/descricao | URL com UTM |
|------|----------------------|-------------|
```

Atualize o `MEMORY.md` index com:

```
- [utm-registry.md](utm-registry.md) — padrao e vocabulario de links de rastreio (UTM)
```

## Passo a passo: gerar um link

### 1. Leia o registry e pegue o que falta

Confirme com o usuario o minimo:
- URL de destino (do registry ou nova)
- `utm_source`, `utm_medium`, `utm_campaign` (obrigatorios)
- `utm_content` / `utm_term` (so se fizer sentido)

Se o usuario disser um valor fora do vocabulario (ex: "IG" em vez de
`instagram`), **normalize pro padrao do registry** e avise: "padronizei `IG`
pra `instagram` pra bater com seus outros links."

### 2. Monte a URL

Junte destino + parametros. Regras de montagem:
- Comeca com `?` se a URL nao tem query; senao usa `&`.
- Codifique espacos que sobrarem (mas o ideal e nao ter nenhum).
- Ordem fixa: source, medium, campaign, content, term.

Exemplo:
```
https://claudiamendesmakeup.com.br/agendar?utm_source=instagram&utm_medium=bio&utm_campaign=dia-das-maes-2026
```

Se quiser, ofereca gerar com um script simples pra varios de uma vez:

```bash
build_utm() {
  local base="$1" src="$2" med="$3" camp="$4" cont="$5"
  local sep="?"; [[ "$base" == *"?"* ]] && sep="&"
  local url="${base}${sep}utm_source=${src}&utm_medium=${med}&utm_campaign=${camp}"
  [[ -n "$cont" ]] && url="${url}&utm_content=${cont}"
  echo "$url"
}
build_utm "https://claudiamendesmakeup.com.br/agendar" instagram bio dia-das-maes-2026
```

### 3. Registre o link gerado

Anexe na tabela "Links ja gerados" do `utm-registry.md` (data + descricao + URL).
Assim da pra reusar e nao recriar variacoes diferentes do mesmo link.

### 4. Entregue

Mostre a URL final, limpa, pronta pra copiar. Se o usuario pediu varios,
entregue em lista. Ofereca encurtar depois (Bitly, etc.) — mas o UTM tem que
estar na URL **antes** de encurtar.

## Passo a passo: auditar links existentes

Quando o usuario colar uma lista de links ou apontar onde estao:

1. Para cada link, extraia os parametros UTM.
2. Compare com o vocabulario do registry e com as regras de formato.
3. Classifique:
   - 🟢 **OK:** bate com o padrao.
   - 🟡 **Atencao:** funciona, mas foge do padrao (maiuscula, sinonimo,
     `utm_campaign` faltando) — sugira a versao corrigida.
   - 🔴 **Quebrado:** parametro duplicado, espaco cru, dado pessoal, `?`/`&`
     errado que quebra a URL.

Relatorio:

```
Auditoria de UTM — <data>

🟢 link-bio-agendamento: ok
🟡 post-promo: utm_source=Instagram (maiusculo) → instagram
🟡 story-vip: sem utm_campaign → sugiro utm_campaign=lista-vip
🔴 link-loja: tem espaco cru em utm_campaign=dia das maes → dia-das-maes-2026

Quer que eu gere as versoes corrigidas?
```

## Regras

- **Consistencia acima de tudo.** Sempre normalize pro vocabulario do registry.
  Um valor novo so entra no padrao depois de adicionar no registry.
- **Nunca coloque dado pessoal** (nome, email, telefone de cliente) em UTM —
  isso vaza em relatorio e em link compartilhado.
- **Nao invente destino.** Se nao souber a URL de destino, pergunte; nao chute.
- **UTM antes de encurtar.** Encurtador depois, nunca antes.
- Se o registry nao existir, crie na hora (entrevista curta) em vez de gerar
  link solto sem padrao.
