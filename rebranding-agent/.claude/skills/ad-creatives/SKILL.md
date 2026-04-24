---
name: ad-creatives
description: Gera ad sets prontos pra Meta (Facebook + Instagram) — 3 hooks x 3 creatives x 3 copies cobrindo formatos 1:1, 4:5, 9:16, com UTM parameters e um plano de teste de 7 dias. Usa o angle que vende do conversion-angle skill + a marca do brand-direction + o logo final. Use depois de conversion-angle e logo-design, quando o discovery disser que o usuario roda ads ou quer comecar a rodar.
---

# Ad Creatives (Meta)

> **Source & credit**: Ad testing framework (3x3x3 matrix) adaptado de [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) (250+ checks, weighted scoring). Hook patterns de [Alex Hormozi's $100M Offers](https://www.acquisition.com/offers) e [swipe files publicos](https://swiped.co). Copy structures da Lei da Publicidade (AIDA, PAS, BAB). Export via HTML + Playwright render nos ratios oficiais do Meta.

## Purpose

Sai dessa skill com 27 criativos prontos pra subir no Meta Ads Manager (3 hooks x 3 creatives x 3 copies), em 3 formatos (feed 1:1, feed 4:5, reels/stories 9:16), com:
- UTM parameters estruturados
- Plano de teste de 7 dias com orcamento recomendado
- Checklist pre-flight (pixel, catalogo, eventos de conversao)
- Um CSV pra import/copy no Ads Manager

## Skip condition

So roda se discovery tiver:
- `Rodando ads? = Meta OU nenhum (e objetivo do site = vender direto)`

Se for so Google Ads ou so TikTok, a skill avisa e sugere uma variacao (por enquanto so cobre Meta — expandir pros outros e backlog).

## Input

- `./rebrand/05-conversion-angle.md` (do conversion-angle) — angle principal + 2-3 angles secundarios
- `./rebrand/.selected-name.json` + `06-direction.md` — nome, tagline, palette, tipografia
- `./rebrand/logo/final/` — logo exports
- Prova social do discovery (depoimentos, numeros, cases)

## Procedure

### 1. Defina a matriz de teste

**Eixo 1 — Hooks (3)**: 3 primeiros-3-segundos diferentes.

Archetypes pra pick 3 que combinem com o angle:

| Tipo | Exemplo | Quando |
| --- | --- | --- |
| **Pattern interrupt** | "Para. Voce ta perdendo R$ X por mes com isso." | Baixo awareness, precisa acordar |
| **Prova social direta** | "12.483 lojas ja usam [marca]" | Oferta madura, muitos users |
| **Contra-intuitivo** | "Pare de contratar dev. Faca voce mesmo." | Nicho tecnico, audiencia cansada do status quo |
| **Problema agitado** | "Checkout abandonado de novo? Aqui ta o porque." | High-awareness do problema |
| **Transformacao** | "De 10 vendas/mes pra 400 em 90 dias. Real." | Before/after / case study |
| **Pergunta direta** | "Quanto custa sua dev team esse mes?" | Audiencia qualificada |

**Eixo 2 — Creative types (3)**: forma do anuncio.

1. **Static image** — headline + imagem do produto ou mockup, logo watermark pequeno
2. **Carousel** — 5 cards: hook / problema / solucao / prova / CTA
3. **Video motion graphic** — 15s motion com texto animado sobre fundo brand (gera como HTML+CSS animacao se nao tiver video; caso contrario, descreve shot list pra o usuario gravar)

**Eixo 3 — Copy structures (3)**: texto do post.

1. **AIDA curto** (90-120 chars) — Attention / Interest / Desire / Action
2. **PAS** (160-220 chars) — Problem / Agitate / Solution
3. **Lista + prova** (200-280 chars) — bullet points com beneficios + 1 numero de prova social + CTA

### 2. Gera os 27 ads (3x3x3)

Estrutura em disco:

```
./rebrand/ads/
  meta/
    creative-01_static_hook1_copy1/
      1x1.png            1080x1080
      4x5.png            1080x1350
      9x16.png           1080x1920
      copy.txt           post body
      headline.txt       title ≤40 chars
      description.txt    ≤30 chars
      cta_button.txt     "Shop Now" | "Learn More" | "Sign Up" | custom
      html/              HTML source usado pra gerar o PNG (editavel)
        1x1.html
        4x5.html
        9x16.html
    creative-02_static_hook1_copy2/
    ...
    creative-27_video_hook3_copy3/
```

**Render pipeline**: cada HTML usa os tokens CSS da direcao escolhida (brand_primary, fonte heading, etc). Playwright abre com viewport do ratio exato e faz screenshot. Variations pra:
- Fundo brand_primary com texto branco
- Fundo surface (branco) com texto brand_primary
- Fundo imagem de produto (se o usuario forneceu na discovery) com overlay escuro

### 3. UTMs consistentes

Cada creative recebe UTM automatico no link:

```
https://<site>/?utm_source=meta
              &utm_medium=cpc
              &utm_campaign=<offer_slug>
              &utm_content=<creative_id>
              &utm_term=<hook_id>_<creative_type>_<copy_id>
```

### 4. Plano de teste de 7 dias

Output `./rebrand/ads/meta/test-plan.md`:

```markdown
# Plano de teste — 7 dias

## Setup
- **Pixel instalado**: ?  (checklist pro usuario)
- **Eventos de conversao registrados**: Purchase, AddToCart, InitiateCheckout
- **Catalogo conectado** (se ecommerce): sim / nao

## Estrutura de campanha
- **1 Campanha** — objetivo: Sales (ou Leads se lead magnet)
- **3 Ad Sets** — 1 por hook. Audiencias identicas. CBO off, budget no ad set.
- **9 Ads por ad set** — 3 creative types x 3 copies. Total: 27 ads.

## Audiencias
- **Ad set 1** (Hook 1): Broad 25-55 BR, interests leves
- **Ad set 2** (Hook 2): Lookalike 1% de compradores (se houver pixel data)
- **Ad set 3** (Hook 3): Retargeting — visitors 30d + engaged IG/FB 90d

## Budget
- Sugestao: R$ 50/dia por ad set x 3 = R$ 150/dia x 7 dias = R$ 1.050 total
- Ajustar pro discovery: se `investimento mensal < R$1k`, reduzir pra R$ 20/dia por ad set

## Regras de matanca
- **Dia 3**: qualquer ad com CPM > 2x media da conta E 0 adds to cart → pausa.
- **Dia 5**: qualquer ad set com CPA > 2x target → pausa.
- **Dia 7**: escolhe 1-2 winners, consolida budget. Gera novos criativos da "estetica" do winner (mesmo hook, novas variacoes).

## Metricas-alvo (baseline)
- CPM: R$ 20-40 BR (varia por nicho)
- CTR: ≥ 1.5%
- Hook rate (3s video views / impressoes): ≥ 25%
- Hold rate (15s video views / 3s views): ≥ 50%
- CPA target: <definido pelo ticket e margem do discovery>
```

### 5. CSV de import

`./rebrand/ads/meta/import.csv` com colunas compativeis com Meta Ads Manager bulk import:

```
Campaign Name,Ad Set Name,Ad Name,Headline,Primary Text,Description,Link,CTA Button,Image URL,UTM
Rebrand-2026-04,Hook1-Broad,Creative-01,...,...,...,https://...,Learn More,file://.../1x1.png,utm_...
```

### 6. Pre-flight checklist

`./rebrand/ads/meta/preflight.md`:

```markdown
# Pre-flight checklist — rode antes de subir os ads

## Pixel & Conversion API
- [ ] Meta Pixel instalado no site pos-rebrand (apply-rebrand skill adiciona automaticamente)
- [ ] Conversion API server-side configurada (se possivel)
- [ ] Eventos: ViewContent, AddToCart, InitiateCheckout, Purchase todos disparando
- [ ] Domain verification no Business Manager
- [ ] Aggregated Event Measurement: 8 eventos priorizados, Purchase no topo

## Conta
- [ ] Business Manager criado no nome novo
- [ ] Payment method ok, limite de gasto diario ≥ budget do teste
- [ ] Pixel compartilhado com Ad Account
- [ ] Usuario e admin do BM

## Creative compliance
- [ ] Nenhum criativo com >20% de texto na imagem (regra morta oficialmente mas ainda afeta reach)
- [ ] Claims de resultado tem disclaimer (se financeiro / saude / dieta)
- [ ] Sem imagens de "antes e depois" explicitas (politicas Meta)
- [ ] Logo aparece em todo creative (branding consistency)

## Post-launch day 1
- [ ] Todos os ads aprovados (nenhum "Em analise" >6h sem motivo)
- [ ] Pelo menos 100 impressions em cada ad set
- [ ] Pixel recebendo eventos em real-time no Events Manager
```

### 7. Output final

`./rebrand/12-ad-creatives.md`:

```markdown
# Ad creatives Meta — <nome>
_Generated <date> by the `ad-creatives` skill_

## Produzidos
- 27 creatives (3 hooks x 3 types x 3 copies)
- 3 formatos por creative: 1:1, 4:5, 9:16
- Total: 81 imagens + 27 copies + 27 UTMs

## Arquivos
- `./rebrand/ads/meta/` — todos os creatives
- `./rebrand/ads/meta/import.csv` — pra bulk upload
- `./rebrand/ads/meta/test-plan.md` — plano de 7 dias
- `./rebrand/ads/meta/preflight.md` — checklist pre-launch

## Proximos passos
1. Rode o preflight checklist
2. Importe o CSV no Ads Manager (ou crie manualmente se preferir)
3. Setup dos 3 ad sets conforme test-plan.md
4. Suba o orcamento recomendado
5. Dia 3 / 5 / 7: aplique as regras de matanca

## Depois do teste
Volte rodar essa skill com o criativo winner do teste na input pra gerar "variacoes do winner" — mesma hook, novas angulacoes.
```

## Quality bar

- **Cada creative deve ler em 3 segundos** mobile scroll-by. Se precisa parar pra entender, falhou.
- **Hook sempre nos primeiros 3 segundos do video / primeira metade do static / primeiro slide do carrossel.**
- **Logo presente mas pequeno** — a marca assina, nao domina.
- **CTA button condiz com estagio** do funil: "Learn More" pra awareness, "Sign Up" pra lead, "Shop Now" pra venda direta.
- **Nenhum claim nao-verificavel** ("melhor do mundo", "garantido 100%") — Meta rejeita e o pixel fica manchado.
- **Versao PT-BR por padrao** se o publico for BR; EN se for internacional; AMBOS se atender os dois (gera 54 creatives nesse caso).

## Handoff

Retorna path pra `12-ad-creatives.md`, contagem de creatives gerados, e flags se algum check falhou (ex: "sem prova social disponivel no discovery — criei mocks com placeholder, usuario precisa substituir antes de subir").
