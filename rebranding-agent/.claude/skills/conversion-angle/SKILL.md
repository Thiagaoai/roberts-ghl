---
name: conversion-angle
description: Pesquisa o que vende no nicho da marca e define o angle de venda vencedor — o big promise, os 3 hooks mais fortes, a oferta irresistivel, a prova social pronta pra usar, e os CTAs que convertem. E a skill que alimenta o copy do site (apply-rebrand) e os ads (ad-creatives). Use depois do discover-brand, antes do ad-creatives e apply-rebrand.
---

# Conversion Angle

> **Source & credit**: Offer framework do Alex Hormozi ($100M Offers: Value Equation, Grand Slam Offer). Swipe-file pattern de [swiped.co](https://swiped.co) e [copyhackers](https://copyhackers.com). SEO / SERP analysis pattern adaptado de [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills). CRO angle-testing dos playbooks publicos da ConversionXL.

## Purpose

Um site e um ad bonitos nao vendem se o angle ta errado. Essa skill responde:

1. **Qual e a grande promessa?** — uma frase que faz o cliente ideal parar de rolar.
2. **Quais sao os 3 hooks mais fortes?** — pra testar em ads e headlines.
3. **Como empacotar a oferta?** — pra parecer "impossivel recusar".
4. **Qual prova social alavancar?** — dos assets existentes, qual converte mais.
5. **Quais CTAs usar?** — verbos exatos, em cada pagina e cada ad.

## Input

- `./rebrand/01-discovery.md` — offer, ticket, dor, audiencia, driver emocional, prova social disponivel
- (Opcional) Acesso a web via `WebFetch` e `WebSearch` pra analise de SERP e concorrentes

## Procedure

### 1. Mapeia o ecosystem competitivo

Via `WebSearch` e `WebFetch`:

- Pesquisa 5-10 buscas-chave que o publico-alvo faria:
  - "melhor <categoria>"
  - "como resolver <dor>"
  - "<categoria> vs <concorrente>"
  - "quanto custa <categoria>"
  - "<categoria> para <segmento>"
- Pega top 5 resultados organicos de cada — anota headlines, value props, CTAs.
- Fetch dos concorrentes diretos (URLs do discovery): headline de home, oferta, prova social mostrada, CTA principal.

Outputs pra `./rebrand/.tmp/serp-analysis.md`:

```
Search: "melhor gateway de pagamento shopify"
Top 5:
1. Stripe — "The platform for modern online commerce"
   CTA: Start now
   Prova: "Millions of businesses"
2. ...
```

### 2. Identifica o market sophistication & awareness level

(Framework Eugene Schwartz / Breakthrough Advertising)

**Awareness**:
- Unaware → cliente nao sabe que tem o problema
- Problem-aware → sabe o problema mas nao que ha solucao
- Solution-aware → sabe que ha solucoes mas nao a sua
- Product-aware → sabe seu produto, nao tomou decisao
- Most aware → so falta o gatilho final

**Sophistication** (estagio do mercado):
- Stage 1: primeira de tudo — "Pagamentos online"
- Stage 2: claim mais forte — "Pagamentos online 10x mais rapido"
- Stage 3: mecanismo unico — "Pagamentos online por API Rails 1-click"
- Stage 4: mecanismo elaborado — "Checkout adaptativo por machine learning"
- Stage 5: identificacao + experiencia — "O checkout feito pra lojas brasileiras por fundadores que ja quebraram com gateway lento"

**Regra**: a copy e o angle tem que ser **1 estagio acima** do maior concorrente. Se todos ja estao stage 3 com "1-click", voce precisa ir pra 4 com novo mecanismo ou 5 com identificacao.

### 3. Aplica o Value Equation (Hormozi)

Monte uma planilha mental:

```
Valor percebido = (Sonho realizado × Probabilidade de conseguir) / (Tempo de espera × Esforco percebido)
```

Pro offer atual (do discovery), pontua 1-10 cada:
- **Sonho realizado** — o resultado e realmente desejado?
- **Probabilidade** — parece crivel que vai acontecer?
- **Tempo** — quanto demora? Menos e mais.
- **Esforco** — quanto o cliente tem que fazer? Menos e mais.

Cada ponto fraco vira uma alavanca: "Probabilidade fraca? → precisa de mais prova. Tempo lento? → precisa de quick win inicial."

### 4. Escreve 3 angles

**Angle A — safe (market-fit)**: espelha o melhor concorrente com uma melhoria pontual. Baixo risco.

**Angle B — differentiated (mecanismo unico)**: nomeia seu "como" diferente. Medio risco, medio retorno.

**Angle C — bold (identificacao / storytelling)**: fala direto pra uma sub-audiencia ultra-especifica. Alto risco, alto retorno se acertar.

Pra cada, define:

```yaml
angle_name: "B — Dev-Free Checkout"
big_promise: "Tenha um checkout de unicornio em 10 minutos, sem dev."
target_sub_audience: "Donas de loja Shopify que fazem 8-40k/mes e nao tem dev in-house"
awareness_level: "Problem-aware"
sophistication: "Stage 4"
value_equation_lever: "Reduz esforco (nao precisa dev) + reduz tempo (10 min)"

hooks:
  - "Stop paying devs R$ 8k/mes. Rode seu checkout voce mesma em 10 min."
  - "Sua loja perde R$ X/mes com checkout lento. Aqui ta a conta."
  - "12.483 lojas Shopify ja rodam sem dev. Veja como."

offer_stack:
  core: "Acesso vitalicio ao <produto> (valor R$ X)"
  bonus_1: "Templates de checkout prontos pra 8 nichos (R$ Y)"
  bonus_2: "Revisao 1-on-1 pelo time (R$ Z)"
  bonus_3: "Comunidade fechada de donas de loja (R$ W)"
  guarantee: "30 dias. Se nao aumentar CVR em 10%, devolvemos + R$ 500 pelo seu tempo."
  price_anchor: "Valor total: R$ X+Y+Z+W. Hoje: R$ (X+Y+Z+W)/3."

proof_stack:
  - { type: "numero", claim: "12.483 lojas ativas" }
  - { type: "case", claim: "Loja Z: de 2.1% pra 4.8% CVR em 30 dias", source: "depoimento video #12" }
  - { type: "autoridade", claim: "Parceria oficial Shopify Plus" }
  - { type: "midia", claim: "Featured em <veiculo>" }

ctas:
  primary: "Testa 14 dias gratis"          # site hero + ads
  secondary: "Ver demo ao vivo"            # site segunda dobra
  low_commitment: "Baixa o guia gratis"    # lead magnet pra audiencia fria
```

### 5. Escolhe 1 (ou deixa o usuario escolher)

Se o discovery ja deixou claro o angle (ex: `Unfair advantage = "so nos fazemos sem dev"`), use o angle que amplifica isso. Caso contrario, **chama `AskUserQuestion`** pra o usuario escolher entre A/B/C.

### 6. Output final

`./rebrand/06-conversion-angle.md`:

```markdown
# Conversion angle — <nome>
_Generated <date> by the `conversion-angle` skill_

## Contexto de mercado
- **Awareness do publico**: <level>
- **Sophistication do nicho**: Stage <N>
- **Concorrentes analisados**: <count>
- **Headline media dos top 5**: "..."

## Value Equation (atual)
- Sonho: 8/10
- Probabilidade: 5/10 ← alavanca
- Tempo: 9/10
- Esforco: 4/10 ← alavanca

## Angle escolhido: **B — Dev-Free Checkout**

### Grande promessa
> Tenha um checkout de unicornio em 10 minutos, sem dev.

### 3 hooks pra testar em ad
1. ... (primary, mais forte)
2. ...
3. ...

### Offer stack
<tabela do stack + preco>

### Prova social priorizada
<top 4 assets, por ordem de impacto>

### CTAs
- Site hero: "Testa 14 dias gratis"
- Seguinte dobra: "Ver demo ao vivo"
- Lead magnet: "Baixa o guia gratis"

### Headlines prontas pra site
- H1 home: "Checkout de unicornio em 10 minutos. Sem dev."
- Sub-H1: "12.483 lojas Shopify ja cresceram 2x sem contratar engenheiro."
- Pagina pricing: "Pague pelo resultado, nao pela horas do dev."
- Pagina sobre: "Feito por fundadores que quebraram duas vezes com gateway lento."

## O que alimenta:
- `ad-creatives` — os 3 hooks + offer stack + proof
- `apply-rebrand` — as headlines prontas trocam as atuais no site
- `social-presence` — as bios usam a grande promessa
```

## Quality bar

- **Cada angle tem que ser defensavel contra "e se?"** — se o usuario pergunta "e se meu publico for mais velho?", voce explica em 1 frase. Se nao sabe, o angle ta fraco.
- **Hooks tem que ser testaveis em Meta Ads** — nada de generico, nada de claim nao-verificavel.
- **Offer stack precisa fazer o preco parecer obvio** — se depois de ler o stack o cliente nao pensa "esse preco ta baixo pro que entrega", o stack ta fraco.
- **Prova social e ouro. Usa o que existe.** Se discovery disse "nenhuma prova disponivel", flag FORTE — voce vai rodar ads no vazio. Sugere pegar 5 depoimentos antes de subir ads.

## Handoff

Retorna:
- Path pra `06-conversion-angle.md`
- Angle escolhido
- Os 3 hooks e big promise (pros outros skills consumirem)
- Red flags (ex: "sem prova social", "sophistication do nicho exige stage 5 mas discovery aponta stage 3")
