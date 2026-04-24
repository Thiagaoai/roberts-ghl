---
name: seo-content-plan
description: Monta plano de SEO + conteudo organico de 6 meses — pillar pages (topical authority) + cluster posts (long-tail), keyword research com intent mapping, estrutura tecnica (sitemap, schema, internal linking), e calendario editorial mensal. Trafego organico e gratuito e compounding, diferente de ads. Use depois de conversion-angle pra nichos com search volume real.
---

# SEO + Content Plan

> **Source & credit**: Pillar-cluster model de [HubSpot's "Topic Clusters"](https://www.hubspot.com/topic-clusters) + [Brian Dean's Skyscraper technique](https://backlinko.com/skyscraper-technique). Intent mapping de [Ahrefs 2025 keyword playbook](https://ahrefs.com). Technical SEO baseline de [Google Search Central docs](https://developers.google.com/search).

## Purpose

Ad paga traz trafego hoje, **SEO traz trafego pros proximos 3-5 anos**. Trafego organico e compounding — artigo publicado 2024 ainda traz lead em 2026. Mas SEO demanda:
- Plano de 6-12 meses (curto prazo nao funciona)
- Keyword research serio
- Pillar pages + clusters
- SEO tecnico (site rapido, schema, internal links)
- Publicacao consistente

Essa skill entrega tudo isso em formato acionavel.

## Skip condition

Se discovery indicar produto com busca zero (ex: "sistema proprietario de nome unico que ninguem busca", "lancamento stealth sem demanda"), pula com sugestao de focar em social + ads e voltar em 6 meses quando houver busca de brand.

## Input

- `./rebrand/01-discovery.md` — categoria, publico, concorrentes
- `./rebrand/02-competitor-research.md` — concorrentes SEO (quem ranqueia)
- `./rebrand/05-conversion-angle.md` — topicos do produto
- `./rebrand/13-landing-page.md` — LP que precisa ranquear
- Site atual (pra auditoria tecnica)

## Procedure

### 1. Keyword research — 3 tiers de intent

**Tier 1 — Commercial intent (alta conversao, baixo volume):**
- "melhor [produto]", "[produto] vs [concorrente]", "review [produto]"
- "alternativa a [concorrente]", "[produto] preco"
- Volume: 100-5k/mes por keyword
- CVR: 5-15%

**Tier 2 — Informational/problem-aware (medio volume):**
- "como resolver [problema]", "o que e [conceito]"
- "[categoria] para [caso de uso]"
- Volume: 1k-50k/mes
- CVR: 1-3%

**Tier 3 — Top-of-funnel (volume alto, conversao baixa mas branding):**
- "guia completo [area]", "tudo sobre [tema]"
- Volume: 5k-500k/mes
- CVR: <1% mas educa e atrai backlinks

Ferramenta: Ahrefs / Semrush / Ubersuggest. Se usuario nao tem, gera usando Google Keyword Planner (gratis) + scraping de "People Also Ask" + Google Suggest.

Min 80 keywords distribuidos.

### 2. Topical authority: pillar + clusters

Estrutura:

```
Pillar Page (2000-4000 palavras)
└── "Guia completo de <tema grande>"
    ├── Cluster Post 1 (800-1500 palavras): "Como fazer X"
    ├── Cluster Post 2: "Erros em X"
    ├── Cluster Post 3: "Ferramentas pra X"
    ├── Cluster Post 4: "X vs Y" (comparacao)
    ├── Cluster Post 5: "Case: como empresa Z fez X"
    ├── Cluster Post 6: "Tendencias de X em 2026"
    └── Cada cluster linka pro pillar + entre si (topic cluster linking)
```

Pra uma marca, 2-3 pillars + 10-20 clusters cada cobre bem.

Exemplo pra uma marca de checkout optimization:
```
Pillar 1: "Guia completo de conversao em e-commerce"
├── Cluster: "12 otimizacoes de checkout que aumentam CVR"
├── Cluster: "Abandonment rate — como calcular e reduzir"
├── Cluster: "Shopify vs WooCommerce: qual converte mais"
├── Cluster: "Psicologia de scarcity em checkout"
├── Cluster: "Trust badges funcionam? Estudo com 10 lojas"
├── Cluster: "Pay later (BNPL) no Brasil: Pix, boleto ou parcelado?"
└── ...
```

### 3. Content calendar (6 meses)

```csv
mes,semana,tipo,titulo,keyword_primaria,keyword_volume,intent,palavras,pillar_parent,status
1,1,pillar,"Guia completo de conversao","otimizar conversao",4400,commercial,3500,-,planejar
1,1,cluster,"12 otimizacoes de checkout","checkout shopify",2900,commercial,1500,"Guia completo de conversao",planejar
1,2,cluster,"Como reduzir abandonment","abandono de carrinho",1800,problem,1200,"Guia completo de conversao",planejar
1,3,cluster,"Shopify vs WooCommerce","shopify vs woocommerce",3200,commercial,2000,"Guia completo de conversao",planejar
1,4,cluster,"Trust badges que funcionam","trust badge ecommerce",480,commercial,1000,"Guia completo de conversao",planejar
...
```

Ritmo sugerido: 2-4 posts por mes nos primeiros 3 meses, 4-8 do mes 4 em diante.

### 4. Briefing por post

Pra cada post, gera briefing completo:

```markdown
# Post Brief — "12 otimizacoes de checkout que aumentam CVR"

## Metadados
- Keyword primaria: "checkout shopify" (2.9k/mes)
- Secundarias: "otimizar checkout" (880), "conversao checkout" (320)
- Intent: commercial
- SERP competitivo: medio (ahrefs KD 28)

## SERP analysis
Top 10 atual:
1. <concorrente>.com — 1800 palavras, cobre 8 pontos
2. <concorrente 2>.com — 2500 palavras, cobre 15 pontos, video embebido
3. <concorrente 3>.com/br — so 900 palavras, mal ranqueado (gap)
...

## Nossa diferenca
Vamos cobrir 12 pontos (mais que o top 1), com:
- 3 pontos exclusivos que nenhum cobre
- Screenshots reais (nao generic stock)
- Estudo de caso de nosso cliente
- Calculadora embedded de ROI de checkout

## Estrutura
H1: 12 otimizacoes de checkout Shopify que aumentam CVR em 2026
H2: 1. Simplifique formularios pra 4 campos
H2: 2. Mostre valor total sem surpresas
...
H2: Como a <cliente> aumentou CVR em 47% (case)
H2: Calculadora: quanto voce perde por mes com checkout ruim
H2: Checklist final pra executar

## CTA primario
Link pra <produto principal> em 3 momentos:
- Apos ponto #4 (soft)
- No case study (middle)
- No CTA final (forte)

## Internal links
- Pillar "Guia completo de conversao" (apex)
- Cluster "Abandonment rate" (lateral)
- LP de produto (conversion)

## Externo (outbound)
- Google Analytics docs (authority)
- Baymard Institute research (data)

## Schema
- Article + BreadcrumbList + FAQPage (pra pegar rich snippet)

## Palavras
Target 1500 palavras. Nao enche linguica.
```

### 5. Estrutura tecnica

`./rebrand/seo/technical-audit.md`:

**Checklist tecnico a implementar:**

- [ ] **Core Web Vitals**: LCP <2.5s, CLS <0.1, INP <200ms (usa `analytics-setup` dashboards pra monitorar)
- [ ] **Sitemap.xml**: auto-gerado, submitted no GSC
- [ ] **Robots.txt**: permite crawl, bloqueia admin/checkout
- [ ] **HTTPS**: sempre, com redirect http→https
- [ ] **Canonical tags**: em todas paginas
- [ ] **Mobile-first**: responsive, testado no Mobile-Friendly Test
- [ ] **Schema markup**: Organization, Product, Article, BreadcrumbList, FAQPage onde cabe
- [ ] **Open Graph + Twitter Cards**: em todas paginas
- [ ] **Internal linking**: toda pagina linkada de >=2 outras
- [ ] **404 page**: custom, com CTA pra home/produto
- [ ] **Redirects 301** pra URL antigas (criticas em rebranding!)
- [ ] **Site speed**: imagens WebP/AVIF, fonts self-hosted, CSS critico inline, defer JS nao-critico
- [ ] **Alt text**: em toda imagem
- [ ] **Heading hierarchy**: H1 unico, H2/H3 sequenciais

### 6. Rebranding-specific SEO risks

Se e rebrand de site existente, ALERTA especifico:

⚠️ **URLs mudando**: implementar 301 de todo URL antigo pra novo. Perder isso = perde 30-80% do trafego organico.

⚠️ **Dominio mudando**: notificar GSC, implementar change-of-address. Esperar 3-6 meses pra recuperar ranking completo.

⚠️ **Nome de marca mudando**: novo nome nao tem autoridade SEO. Pillar sobre "<nome antigo> agora <nome novo>" e key.

⚠️ **Backlinks antigos**: lista todos backlinks atuais (Ahrefs/GSC), outreach pra donos updates o link.

Gera `./rebrand/seo/rebrand-seo-migration.md` com checklist dessas migrations.

### 7. Internal linking strategy

Mapa de links:

```
<dominio>/
├── / (home) → linka pra pillars + LP principal
├── /guia-conversao/ (pillar 1) → linka pra todos clusters 1
├── /otimizacao-checkout/ (cluster) → linka pra pillar 1 + 2 outros clusters + LP
├── /produto/ (LP) → linka pra pillar 1 (ref) + case studies
└── /blog/ (hub) → linka pra todos posts ordenados
```

Toolagem: `./rebrand/seo/internal-links-map.html` — grafo visual de link equity.

### 8. Link building inicial

`./rebrand/seo/link-building-plan.md`:

**Tier 1 — Quick wins (mes 1)**:
- Perfis: LinkedIn, Crunchbase, AngelList, ProductHunt → link pro site
- Guest post em 3 blogs do nicho (pitch preparado)
- HARO (Help A Reporter Out) — responder 5 pitches/semana
- Podcasts: aparece em 5 de nicho

**Tier 2 — Conteudo (mes 2-3)**:
- Skyscraper: pega post top-10 do nicho, faz versao 10x melhor, outreach pra sites que linkam pro original
- Research original: pesquisa com numeros reais, publica — jornalista cita

**Tier 3 — Relacionamento (mes 4+)**:
- Parcerias com marcas nao-concorrentes mas mesmo publico
- Conteudo colaborativo (ebook a 4 maos)

### 9. Monitoring

`./rebrand/seo/monitoring-setup.md`:

- Google Search Console: connect + verify
- Semrush/Ahrefs: tracking project com 30 keywords-alvo
- Rank tracker: semanal
- Backlinks: alerta de novo link + link perdido
- Crawl errors: alerta se aparecer

Dashboard Looker Studio: trafego organico, impressoes vs clicks, CTR por pagina, ranking medio.

### 10. Output umbrella

`./rebrand/23-seo-content-plan.md`:

```markdown
# SEO + Content Plan — <marca>

## 6-month roadmap

### Mes 1 — Fundacao
- SEO tecnico fixes (ver technical-audit.md)
- Pillar 1 publicado
- 2 clusters de pillar 1
- GSC + tracker configurados

### Mes 2 — Momentum
- 4 clusters de pillar 1
- Pillar 2 draft
- Link building tier 1

### Mes 3 — Expansao
- Pillar 2 publicado + 3 clusters
- Comeca conteudo pilar 3
- HARO responses comecam

### Mes 4-5 — Autoridade
- Ritmo: 4-6 posts/mes
- 2 skyscrapers/mes
- Research original publica

### Mes 6 — Review + ajuste
- Audita keywords que rankearam vs nao
- Dobra aposta no que funcionou
- Poda posts que nao geraram trafego em 90d

## Assets gerados
- 80+ keywords pesquisadas
- 3 pillar pages briefadas
- 20 cluster posts briefados
- Technical SEO checklist (25+ itens)
- Rebrand-SEO migration plan
- Link building plan (3 tiers)
- Monitoring setup

## KPIs (medir mensalmente)
- Keywords em top 10 no GSC
- Trafego organico mensal (meta M6: 5k-30k/mes dependendo nicho)
- Backlinks referring domains
- Leads organicos gerados
- Conversao organico → lead → cliente

## Proximos passos
1. Valida keyword research — alguma que nao faz sentido pro publico?
2. Aprova 3 primeiros posts pra escrever
3. Resolve technical-audit.md (da pra fazer em 1 sprint)
4. Se rebranding: EXECUTA migration plan ANTES de renomear URLs
5. Setup GSC + rank tracker
6. Comeca publicacao — ritmo semanal
```

## Quality bar

- **Keyword research com volume real.** Nao chuta volume — usa ferramenta.
- **SERP analysis antes de escrever.** Olha o que ta ranqueando, faz diferente/melhor.
- **Pillar ≠ cluster.** Pillar e introdutorio amplo, cluster e profundo em nicho.
- **Internal linking obrigatorio.** Sem linkar, equity nao flui.
- **Rebrand SEO-aware.** 301 de todo URL antigo pro novo — sem perdoar.
- **Ritmo sustentavel.** Pior publicar 20 posts mes 1 e zero mes 2 do que 4 consistentes por mes.
- **SEO e 6+ meses.** Nao prometa resultado em 30 dias.

## Handoff

Retorna path pra `23-seo-content-plan.md`, keyword research CSV, 6-month calendar, briefings de 3 primeiros posts.
