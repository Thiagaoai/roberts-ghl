---
name: google-ads
description: Monta setup completo de Google Ads — Search campaigns (branded + non-branded keywords), Performance Max com asset groups, YouTube Video ads, Display remarketing. Gera keyword research, ad copy (RSA), extensoes, negativas, e estrutura de campanha pronta pra importar via Google Ads Editor CSV. Complementa ad-creatives (que foca Meta). Use se discovery indicar intent-based audience (B2B, high-ticket, servicos).
---

# Google Ads

> **Source & credit**: Campaign structure destilada de [PPC Greg](https://www.youtube.com/@PPCGreg) e [Aaron Young / Define Digital](https://www.youtube.com/@DefineDigital) playbooks, keyword research method de [Brian Dean's Backlinko](https://backlinko.com/google-ads), Performance Max best practices de [Optmyzr 2025 report](https://www.optmyzr.com).

## Purpose

Meta Ads cria demanda (interrupcao). Google Ads captura demanda (intent-based — pessoa ja procura solucao). Canais sao complementares, nao substitutos. Essa skill entrega:

- **Search campaigns**: branded (defensivo) + non-branded (aquisicao)
- **Performance Max**: catch-all com AI do Google
- **YouTube ads**: skippable pra aquisicao + discovery
- **Display remarketing**: reaquecer visitantes

## Skip condition

Se discovery indicar publico "passive" (TikTok/IG native, impulse buyer, nao procura no Google), pula com no-op log. Indicado:
- B2B SaaS
- Servico local/profissional
- Produto alto-ticket
- Nicho com buscas reais ("melhor [X]", "como fazer [Y]")

## Input

- `./rebrand/01-discovery.md` — publico, ticket, regiao
- `./rebrand/02-competitor-research.md` — concorrentes (pra analisar Ads deles via SEMrush/Spyfu lookup)
- `./rebrand/05-conversion-angle.md` — big promise, CTAs
- `./rebrand/09-landing-page.md` — LP URL (melhor que homepage pra ads)

## Procedure

### 1. Keyword research

Gera 3 groups:

**Branded (defensivo — sempre primeiro)**:
- `<marca>`, `<marca> login`, `<marca> preco`, `<marca> reviews`, `<marca> alternativa`
- Objetivo: nao perder quem ja te procura pra concorrente
- Budget: 5-10% do total

**Non-branded aquisicao (intent alto)**:
- `melhor [categoria]`, `[categoria] barato`, `[categoria] para [caso de uso]`, `alternativa [concorrente]`
- Match types: exact + phrase (nao broad sem supervisao)
- Objetivo: capturar quem ainda nao conhece voce mas tem intent

**Problem-aware (intent medio)**:
- "como [resolver problema]", "o que fazer quando [problema]"
- Match types: phrase
- Objetivo: educar + captar lead (nao venda direta)

Volumes estimados via Keyword Planner API (ou CSV manual se usuario nao conectou). Min 30 keywords por group.

### 2. Estrutura de campanhas

```
Account
├── Campaign: Brand Search
│   ├── Ad Group: Exact brand
│   └── Ad Group: Brand + modifier (login, preco, reviews)
├── Campaign: Non-Brand Search — <categoria>
│   ├── Ad Group: Alternativa a concorrente
│   ├── Ad Group: Comparacao ("melhor X")
│   ├── Ad Group: Caso de uso especifico
│   └── Ad Group: Feature-based
├── Campaign: Performance Max
│   └── Asset Group: produto principal (imagens, videos, copy, feed)
├── Campaign: YouTube — Discovery
│   └── Ad Group: video 15s + 30s (reaproveita UGC)
└── Campaign: Display Remarketing
    ├── Ad Group: visitor 30d sem compra
    ├── Ad Group: add_to_cart sem purchase
    └── Ad Group: cliente antigo (win-back)
```

### 3. Responsive Search Ads (RSA) por ad group

Cada ad group tem 2-3 RSAs com 15 headlines + 4 descriptions:

```yaml
ad_group: "Alternativa a <concorrente>"
rsa_1:
  headlines:
    - "Alternativa <concorrente>: <sua diferenca>"      # <30 chars
    - "<Marca> vs <concorrente>"
    - "<Marca> — Feito pra <publico>"
    - "Troca <concorrente> em 5min"
    - "Ja usa <concorrente>? Veja isso"
    - "<resultado> em 30 dias"
    - "Gratis por <X> dias"
    - "R$ <preco>/mes. Sem fidelidade."
    - "Suporte em portugues"
    - "Integrado com <plataforma chave>"
    - "Avaliado 4.8/5 (<N> reviews)"
    - "Usado por <tipo de cliente>"
    - "Setup em 10 minutos"
    - "<big_promise curta>"
    - "Teste gratis"
  descriptions:
    - "Chega de <dor>. <Marca> faz <funcao 1> + <funcao 2>, com suporte em PT-BR e integracao nativa."
    - "<N> empresas ja migraram de <concorrente>. Motivos: preco melhor, setup rapido, suporte humano."
    - "Teste <X> dias gratis, sem cartao. Se nao gostar, desinscreve em 1 click."
    - "Garantia de <X> dias. Migration gratuita do <concorrente>."
  final_url: <LP url com UTM>
  path1: "alternativa"
  path2: "<concorrente>"
```

Google faz A/B de combinacoes — voce da insumo, ele mixa.

### 4. Extensoes (Assets, na nova nomenclatura Google Ads)

Obrigatorias:
- **Sitelinks**: 4-6 links secundarios (pricing, reviews, demo, sobre)
- **Callouts**: frases curtas de diferenciacao ("Suporte PT-BR", "Free trial", "Sem fidelidade")
- **Structured snippets**: ex: "Features: dashboard, API, exports, alerts"
- **Call extension**: numero de telefone (se relevante)
- **Lead form extension**: form diretamente no SERP (pra lead-gen)
- **Promotion extension**: se tem desconto ("10% OFF primeira compra")
- **Price extension**: 3-8 items com preco
- **Image extension**: 3-5 imagens 1:1 e 1.91:1

### 5. Keyword negativas

Criticas — economiza budget eliminando query ruim.

Negatives comuns (generate automaticamente):
- "gratis", "free" (se produto e pago)
- "download", "torrent", "crackeado" (se SaaS/info)
- "emprego", "vagas" (se nao contrata)
- "como ganhar" (se nao e MLM)
- "curso" (se produto nao e curso)

Em campaign negative list + shared library pra aplicar em multiplas campanhas.

### 6. Performance Max (PMax)

Uma campanha com 1 asset group completo:

- **Imagens**: 5-15 (1:1, 1.91:1, 4:5)
- **Logos**: 1:1 e 4:1
- **Videos**: 3-5 (15s, 30s, 60s — reaproveita UGC)
- **Headlines**: 5 (30 chars) + 5 long (90 chars)
- **Descriptions**: 5 (90 chars)
- **Audience signals**: upload de lista de clientes + interesse declarados + concorrentes
- **Final URL expansion**: OFF no inicio (deixa Google gastar so na LP, nao em /blog)

Budget sugerido: 30-40% do total.

### 7. YouTube Discovery + Skippable

Reaproveita videos UGC do `ugc-scripts`:

```yaml
campaign: YouTube Discovery
type: Video Views / Action
ad_formats:
  - Skippable in-stream: 15s + 30s (obrigatorio hook forte nos primeiros 5s)
  - Bumper: 6s (reforco de brand pra quem ja viu skippable)
targeting:
  - Custom intent: keywords do Search campaign
  - In-market: relevantes pro nicho
  - Similar audiences: lista de clientes uploaded
cta_overlay: "Teste gratis" → LP url
```

### 8. Display Remarketing

```yaml
campaign: Display Remarketing
targeting:
  - Audience 1: visitantes ultimos 30 dias, sem compra
  - Audience 2: add_to_cart sem purchase (window 7 dias)
  - Audience 3: clientes 60+ dias sem compra (win-back)
creative:
  - Responsive Display Ads: upload imagens + logo + headlines + descriptions
  - Google gera banners automaticamente em varios tamanhos
frequency_cap:
  impressions: 3/user/dia
  lifetime: 20/user
```

### 9. Google Ads Editor CSV

Exporta tudo pra importar via Google Ads Editor (mais rapido que criar manual):

`./rebrand/google-ads/editor-import/`:
```
campaigns.csv
adgroups.csv
keywords.csv
rsa.csv
extensions-sitelinks.csv
extensions-callouts.csv
negatives.csv
```

Usuario abre Editor → Import → seleciona pasta → revisa → publica.

### 10. Budget recommendation

Por tamanho de operacao:
- **Bootstrap (<R$5k/mes)**: 70% Brand Search + 30% Remarketing. Sem PMax (precisa de dados).
- **Small (R$5k-20k)**: 30% Brand + 40% Non-brand + 20% Remarketing + 10% YouTube
- **Medium (R$20k+)**: 20% Brand + 30% Non-brand + 30% PMax + 10% YouTube + 10% Remarketing

### 11. Output umbrella

`./rebrand/14-google-ads.md`:

```markdown
# Google Ads Setup — <marca>

## Campanhas criadas
- Brand Search (2 ad groups, ~20 keywords)
- Non-brand Search (4 ad groups, ~80 keywords)
- Performance Max (1 asset group)
- YouTube Discovery (1 ad group, 3 videos)
- Display Remarketing (3 audiences)

## Keyword research
- Total: <N> keywords
- Export: [keywords-research.csv](./google-ads/keywords-research.csv)
- Negatives: <N> termos

## Budget sugerido
R$ <X>/mes distribuido como:
- Brand 20%
- Non-brand 40%
- PMax 20%
- YouTube 10%
- Remarketing 10%

## Proximos passos
1. Baixa Google Ads Editor
2. Importa `editor-import/` folder
3. Conecta conversion actions (vem do analytics-setup — importar do GA4)
4. Configura attribution: "Data-driven" (se conversoes >300/mes) ou "Linear" (se menor)
5. Aguenta 14 dias sem pausar nada — Google precisa de data pra otimizar
6. Semana 3 em diante: pausa keywords/ads com baixo performance, escala os bons

## KPIs
- Brand Search CPA: deve ser <R$ <10-30>
- Non-brand CPA: <R$ <50-200> dependendo do nicho
- PMax ROAS: >2x nos primeiros 30 dias, >3x apos 60
- YouTube view rate: >25%
- Remarketing CPA: <R$ <20-100>

## Anti-pattern evitados
- Broad match sem supervisao
- PMax sem audience signals
- Final URL expansion on no inicio
- Sem negative keywords
- Mesmo LP pra todas as campanhas (nao — Brand → homepage, Non-brand → LP especifica)
```

## Quality bar

- **Brand search sempre primeiro.** Perder quem ja te busca pra concorrente e pecado.
- **Message match LP ↔ ad.** Se ad promete "7 dias gratis", LP tem que dizer 7 dias gratis no H1.
- **Negatives antes de broad match.** Sem negatives, broad queima budget.
- **PMax precisa de audience signals.** Sem signal, Google gasta em publico errado.
- **14 dias de learning obrigatorios.** Nao pausa nada antes.
- **Conversion tracking funcionando.** Se conversion nao dispara, Google otimiza no vazio.

## Handoff

Retorna path pra `14-google-ads.md`, CSVs de import, keyword research, e checklist de conversion actions a configurar no GA4 antes de ativar.
