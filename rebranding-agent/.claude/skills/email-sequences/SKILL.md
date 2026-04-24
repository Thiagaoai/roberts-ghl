---
name: email-sequences
description: Gera 4 sequencias de email prontas (welcome, carrinho abandonado, re-engajamento, pos-venda) com copy PT-BR/EN, subject lines testaveis, delay recomendado, e templates HTML+texto. Integra com providers (Mailchimp, ActiveCampaign, Klaviyo, ConvertKit, RD Station) via JSON de import. Use depois de conversion-angle — ad traz lead, email converte, essa skill transforma trafego em receita recorrente.
---

# Email Sequences

> **Source & credit**: Sequence framework adaptado de [Copyhackers](https://copyhackers.com) welcome-series teardowns, [Val Geisler](https://val.geisler.co) onboarding email audits, e [Klaviyo e-commerce benchmarks 2025](https://www.klaviyo.com/marketing-resources). Subject line patterns de analise de 10k+ emails de [Really Good Emails](https://reallygoodemails.com).

## Purpose

Email marketing ainda e o canal com maior ROI (42:1 em media — DMA 2025). Sem email, seu ad e um funil furado. Essa skill cria 4 sequencias que cobrem os momentos-chave:

1. **Welcome** — primeiro contato, build trust, gera primeira venda
2. **Abandoned cart / lead** — recupera quem quase comprou
3. **Re-engagement** — reaquece lead frio
4. **Post-purchase** — onboarding + cross-sell + review request

## Input

- `./rebrand/01-discovery.md` — oferta, ticket, publico, prova social
- `./rebrand/05-conversion-angle.md` — big promise, hooks, offer stack
- `./rebrand/06-direction.md` — tom de voz
- `./rebrand/07-logo.md` (opcional) — logo pro header dos emails

## Procedure

### 1. Welcome Series — 5 emails em 14 dias

```
Email 1 — imediato apos signup
Email 2 — +1 dia
Email 3 — +3 dias
Email 4 — +7 dias
Email 5 — +14 dias
```

Cada email tem um job-to-be-done:

| # | Job | Subject patterns | CTA principal |
| --- | --- | --- | --- |
| 1 | Welcome + set expectations + delivery do que prometeu | "Bem-vindo(a) ao/a [marca]" / "[nome], ta aqui seu [lead magnet]" | Ver/baixar o lead magnet |
| 2 | Story + authority (quem voce e, por que faz isso) | "Por que eu comecei [marca]" | Ler post/video de origem |
| 3 | Problem education (agita o problema sem vender) | "O erro que 83% das [publico] comete" | Ler conteudo educacional |
| 4 | Social proof + produto (primeiro pitch) | "Como [nome] consegiu [resultado]" | Conhecer o produto |
| 5 | Oferta com urgencia (10% off 48h, bonus, etc.) | "[nome], garanti isso pra voce (48h)" | Comprar / agendar |

### 2. Abandoned Cart / Lead — 3 emails em 48h

```
Email 1 — 1 hora depois
Email 2 — 24 horas depois
Email 3 — 48 horas depois (cupom)
```

| # | Tom | Subject | CTA |
| --- | --- | --- | --- |
| 1 | "Esqueceu algo" — suave, helpful | "Seu [produto] ta esperando" | Voltar pro checkout |
| 2 | Objection-handling (garantia, frete, parcelamento) | "Tem duvida? Eu respondo" | Voltar + FAQ |
| 3 | Cupom 10% valido 24h | "10% seu em [produto] — expira amanha" | Aplicar cupom auto |

### 3. Re-engagement — 5 emails em 30 dias (dispara quando lead fica inativo 60+ dias)

```
Email 1 — dia 0
Email 2 — +7 dias
Email 3 — +14 dias
Email 4 — +21 dias
Email 5 — +30 dias (last chance)
```

| # | Tom | Subject |
| --- | --- | --- |
| 1 | "Senti sua falta" | "Ainda quer [beneficio]?" |
| 2 | Update da marca + novidade | "Mudamos [X] — voce precisa ver" |
| 3 | Conteudo de valor puro (sem pitch) | "[Tema que importa] — 3 min de leitura" |
| 4 | Survey (por que sumiu?) | "1 pergunta rapida" |
| 5 | Last chance / remocao | "Te removo da lista se nao responder" |

### 4. Post-Purchase — 7 emails em 60 dias

| # | Timing | Job |
| --- | --- | --- |
| 1 | Imediato | Confirmacao + obrigado + o que esperar |
| 2 | +1 dia | Onboarding / como usar |
| 3 | +3 dias | FAQ proativa / objecoes pos-compra |
| 4 | +7 dias | Quick win / tutorial |
| 5 | +14 dias | Review request (NPS/reviews Google/Trustpilot) |
| 6 | +30 dias | Cross-sell / upsell relacionado |
| 7 | +60 dias | Referral / indicacao com incentivo |

### 5. Output por email

`./rebrand/email/<sequence>/<NN>-<slug>/`:

```
email.md              # copia humana readable
email.html            # HTML pronto pra provider
email.txt             # versao texto-only (entregabilidade)
subject-ab-test.md    # 3 subject lines pra A/B test
send-trigger.md       # condicao e delay exatos
```

**email.md** — estrutura padrao:

```markdown
# Welcome Email 1 — Delivery do lead magnet
**Sequence**: Welcome  
**Trigger**: Imediatamente apos signup  
**Delay**: 0 min  
**From**: <nome> do <marca>  
**Reply-to**: email real do founder ou suporte

## Subject line (escolher 1 — testar 3)
- A (direto): "[Nome], seu [lead magnet] ta aqui"
- B (curiosity): "Abri isso no teu nome"
- C (beneficio): "O que 83% das lojas esquece no checkout"

## Preheader
"+ 2 bonus que decidi colocar de ultima hora"

## Body

Oi [Nome],

<Abertura curta — nao "bem-vindo a familia", direto ao valor>

Ta aqui seu [lead magnet]: [LINK BUTTON]

3 coisas que quero deixar claro antes:

1. Nao vou te encher de email — uma vez por semana, no maximo.
2. Se nao servir, responda esse email com "sai" que te tiro.
3. <coisa especifica pro nicho>

<Assinatura pessoal do founder, nao corporativa>

[Nome do founder]  
Fundador, [marca]

P.S. <hook pro proximo email>: Amanha te conto por que eu criei isso depois de perder R$ X com [problema] — e o que aprendi.

## Fallback text (caso HTML nao renderize)
<mesmo conteudo em txt sem HTML>
```

### 6. HTML template system

`./rebrand/email/_template/base.html` — template base que todos os emails usam, com vars:

- `{{BRAND_LOGO_URL}}`, `{{BRAND_PRIMARY_COLOR}}`, `{{BRAND_FONT_HEADING}}`
- `{{SUBJECT}}`, `{{PREHEADER}}`, `{{BODY}}`, `{{CTA_TEXT}}`, `{{CTA_URL}}`
- `{{FOOTER_ADDRESS}}` (LGPD/CAN-SPAM compliance), `{{UNSUBSCRIBE_URL}}`

Template usa mobile-first CSS inline (providers stripam `<style>`), max-width 600px, fonts system-safe com fallback web-font.

### 7. Import pros principais providers

Gera arquivos de import em `./rebrand/email/_imports/`:

- `mailchimp.json` — formato MC API
- `activecampaign.csv` — Automation + Email fields
- `klaviyo.json` — Flow definition JSON
- `convertkit.csv` — Sequences CSV
- `rdstation.json` — Automation BR-friendly

Cada um com os triggers, delays, e conteudos ja mapeados.

### 8. Output umbrella

`./rebrand/11-email-sequences.md`:

```markdown
# Email sequences — <marca>

## Sequencias criadas (20 emails total)
- Welcome: 5 emails / 14 dias
- Abandoned cart: 3 emails / 48h
- Re-engagement: 5 emails / 30d
- Post-purchase: 7 emails / 60d

## Provider setup
Escolha seu provider e siga o import:
- Mailchimp: [_imports/mailchimp.json](_imports/mailchimp.json)
- ActiveCampaign: [_imports/activecampaign.csv](_imports/activecampaign.csv)
- Klaviyo: [_imports/klaviyo.json](_imports/klaviyo.json)

## Benchmarks pra acompanhar
- Open rate welcome: >50% (se <35%, subject line fraca ou lista ruim)
- CTR welcome 1: >15%
- Cart recovery rate: >8% (benchmark e-commerce)
- Re-engagement re-activation: >3%
- Post-purchase review rate: >5%

## Proximos passos
1. Importa no teu provider
2. Troca os placeholders (nome, logo, cores ja estao puxados do brand-direction)
3. Conecta triggers (carrinho abandonado precisa de integracao com Shopify/Woo)
4. Testa envio pra ti mesmo antes de ativar
```

## Quality bar

- **From e reply-to de pessoa real.** `noreply@` mata entregabilidade e conversao.
- **Subject <50 chars pra mobile.** Preheader complementa.
- **1 CTA principal por email.** Nao empilha 3 botoes.
- **P.S. obrigatorio em email de venda.** Segunda coisa mais lida depois do subject.
- **Sem imagens pesadas no email 1.** Entregabilidade sofre. Use texto + 1 botao.
- **LGPD**: rodape com endereco fisico, link de unsubscribe funcional, checkbox de consentimento no signup (isso vira pro `legal-compliance`).
- **Voz bate com brand-direction.** Se a voz e "descontraida", nao use "prezado".

## Handoff

Retorna path pra `11-email-sequences.md`, contagem de emails, e lista de providers com import-file pronto.
