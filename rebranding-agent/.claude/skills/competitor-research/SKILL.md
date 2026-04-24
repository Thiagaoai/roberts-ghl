---
name: competitor-research
description: Pesquisa os 3-5 maiores concorrentes do nicho e entrega um estudo profundo do que eles fazem — site, posicionamento, oferta, palette/tipografia, presenca social, e ads rodando agora na Meta Ad Library. Produz um mapa de oportunidades (onde eles sao fortes, onde tem brecha) que alimenta todas as fases seguintes (naming, brand-direction, logo-design, conversion-angle, ad-creatives). Use como Fase 2, logo depois do discover-brand.
---

# Competitor Research

> **Source & credit**: SERP + content analysis patterns de [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills). Meta Ad Library scraping via URL publica (https://www.facebook.com/ads/library) — dado publico, nenhum login. Visual/brand audit pattern adaptado do `site-audit` e `style-extract` deste mesmo agente (DRY intencional). Positioning-map e 2x2 framework do Seth Godin's *Positioning* e Al Ries *Positioning: The Battle for Your Mind*.

## Purpose

**Nao rebrand no vacuo.** Antes de propor nome novo, palette nova, ou angle novo, voce precisa saber o que os maiores do nicho estao fazendo — pra copiar o que funciona, evitar o que esta saturado, e achar a brecha onde voce pode dominar.

Saida: um estudo de ~6-10 paginas com screenshots, tokens extraidos, ads vivos, e um **mapa de posicionamento 2x2** que mostra onde a marca pode jogar pra vencer.

## Input

- `./rebrand/01-discovery.md` — especialmente:
  - Categoria / nicho
  - Concorrentes diretos (se o usuario citou)
  - Audiencia / dor principal
  - Mercados (PT-BR, EN, regional)

## Procedure

### 1. Identifica os concorrentes

Se o discovery listou 3+: usa eles direto.

Se nao listou (ou listou poucos): busca automaticamente via `WebSearch`:

```
# queries-base (adapte pro idioma/regiao do discovery)
"top 10 <categoria>"
"melhor <categoria> <pais>"
"<nicho> <segmento> 2026"
"<dor principal> solucao"
"<categoria> comparacao"
"alternativa <concorrente-ja-conhecido>"
```

Tambem roda buscas em sites de review/comparison:
- G2 (B2B SaaS)
- Capterra
- Product Hunt (early-stage)
- Reclame Aqui + Trustpilot (DTC)
- Google Maps (local)

**Rankeia por tamanho/relevancia**: trafego estimado (via similarweb/semrush se possivel), followers, review count, ou "aparece em N listas de top X". Pega os top 5.

Imprime a lista pro usuario confirmar via `AskUserQuestion`:
- "Detectei esses 5 concorrentes. Confirma, adiciona, remove?"

### 2. Pra cada concorrente, coleta:

Em paralelo (1 job por concorrente; use `Bash` + Playwright script):

**Site**
- Screenshot desktop full-page da home, pricing, about, e 1 blog post (se existir)
- Screenshot mobile da home
- Headline H1 + sub-H1 + CTA principal
- Oferta visible (preco, trial, garantia)
- Prova social visivel (logos, numeros, depoimentos)
- Tecnologia detectada (basta olhar `Built with...` hints ou ferramentas como Wappalyzer via CDN)

**Visual identity**
- Extrai tokens do site (reusa logica da skill `style-extract`, mas so pras principais paginas)
- Captura o logo (screenshot do header)
- Palette principal + secundaria (top 5 cores mais usadas)
- Fonte heading + fonte body
- Estilo de imagem (foto, ilustracao, 3D, iconografia)

**SEO / conteudo**
- Top 10 palavras-chave organicas (se tiver acesso a SEMrush/Ahrefs — senao, pula com flag)
- Numero aproximado de posts no blog
- Tipo de conteudo dominante (guias, cases, opiniao, tutorial)

**Social**
- URLs de IG / LinkedIn / YouTube se aparecem no site
- Follower count em cada (scrape da pagina publica — nao precisa login)
- Frequencia de post recente (ultimo mes)
- Formato dominante (reels / carrossel / foto unica / video longo)

**Ads rodando agora** *(esse e o ouro)*
- Meta Ad Library: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&q=<concorrente>`
  - Scrape quantidade de ads ativos
  - Baixa thumbnail dos top 5 ads com mais impressoes (se Ad Library mostrar)
  - Extrai texto dos top 5 (hook / body / CTA)
- Google Ads (se dispunser de data): copia dos anuncios que aparecem em buscas-chave
- Adiciona checklist: "Se o concorrente ta em ads ha 30+ dias, o criativo esta funcionando. Estude-o."

### 3. Estrutura dos arquivos

```
./rebrand/competitors/
├── concorrente-1-<slug>/
│   ├── screenshots/
│   │   ├── home-desktop.png
│   │   ├── home-mobile.png
│   │   ├── pricing-desktop.png
│   │   └── about-desktop.png
│   ├── tokens.json                  # mesma estrutura do 04-current-tokens.json
│   ├── meta-ads/
│   │   ├── ad-01.png
│   │   ├── ad-01.txt                # hook + body + cta
│   │   └── ...
│   └── summary.md                   # 1 pagina de resumo do concorrente
├── concorrente-2-<slug>/
├── ...
└── concorrente-5-<slug>/
```

### 4. Mapa de posicionamento

Define 2 eixos que importam pro nicho. Exemplos:

- **Preco** (barato ↔ premium) × **Persona** (iniciante ↔ avancado)
- **Foco** (generico ↔ nicho especifico) × **Tom** (corporativo ↔ descontraido)
- **Automacao** (tudo manual ↔ tudo IA) × **Integracao** (isolado ↔ plataforma)

Plota os 5 concorrentes no 2x2 e identifica:
- **Clusters** — onde todos estao amontoados (mercado saturado, evite)
- **Quadrante vazio** — brecha de posicionamento
- **Outliers** — concorrente que ja rompeu e ta sozinho

Gera o 2x2 como HTML+SVG renderizado pra PNG via Playwright: `./rebrand/competitors/positioning-map.png`.

### 5. Tabela comparativa

`./rebrand/competitors/comparison.md`:

```markdown
# Comparativo — <nicho>

| Dimensao | Concorrente 1 | Concorrente 2 | Concorrente 3 | Concorrente 4 | Concorrente 5 |
| --- | --- | --- | --- | --- | --- |
| **Headline** | ... | ... | ... | ... | ... |
| **Preco entrada** | R$ X | R$ Y | Free | R$ Z | R$ W |
| **Oferta** | Trial 14d | Freemium | Demo | Pago so | Setup fee |
| **Prova principal** | 10k clientes | Y Combinator | G2 leader | Logo Fortune 500 | Case Globo |
| **Palette** | 🔵 azul + 🟢 verde | ⚫ preto + 🟡 amarelo | 🟣 roxo mono | 🔴 vermelho + branco | 🟤 terroso |
| **Fonte heading** | Inter | Custom sans | Söhne | Satoshi | Playfair |
| **Estilo visual** | Ilustracao 3D | Foto real | Minimalista flat | Gradientes | Editorial |
| **IG followers** | 45k | 12k | 120k | 8k | 34k |
| **Ads ativos Meta** | 42 | 8 | 0 | 23 | 17 |
| **Hook dominante nos ads** | "Cresca 2x" | "Mais barato que dev" | — | "Para times serios" | "Do zero ao lucro" |
```

### 6. Análise — o que estudar e replicar, o que evitar

`./rebrand/competitors/insights.md`:

```markdown
# Insights — brecha e oportunidade

## O que todos fazem bem (base de mercado — voce precisa ter tambem)
- Trial gratis de 14d
- Prova social com numero (ex: "X clientes")
- Tom direto, nao corporativo

## O que voce DEVE FAZER DIFERENTE
- **Visual**: 4 dos 5 usam azul. A brecha e ir pra <cor contrastante>.
- **Tom**: todos sao corporativos/neutros. Um tom <humano/irreverente> chamaria atencao.
- **Oferta**: todos cobram mensal. Voce pode testar anual com desconto agressivo.
- **Canal**: ninguem ta forte em TikTok. Ha audiencia la.

## O que voce NAO deve fazer (ja esta saturado)
- Dizer "fastest", "best", "#1"
- Headline "Welcome to <x>"
- Fonte Inter no heading (todo mundo usa)

## Hooks de ad que estao funcionando (30+ dias rodando)
_Isso e ouro — estude esses 5 ads em detalhe e faca variacoes pro seu angle._
1. [Concorrente 1] "Pare de perder dinheiro com checkout lento"
2. [Concorrente 4] "Feito pra donas de loja que ja cansaram de dev"
3. ...

## O que alimenta:
- `naming` — evite nomes parecidos fonetica ou visualmente
- `brand-direction` — brecha de palette / tom identificada
- `logo-design` — evite geometrias que 2+ concorrentes ja usam
- `conversion-angle` — stage de sophistication que voce precisa atingir (1 acima do top)
- `ad-creatives` — inspiracao pros 3 hooks a testar
```

### 7. Output final

`./rebrand/02-competitor-research.md` (o doc-umbrella que referencia tudo):

```markdown
# Competitor research — <nicho>
_Generated <date> by the `competitor-research` skill_

## TL;DR em 3 frases
O mercado e dominado por <cluster visual/posicional>. Ha brecha em <quadrante vazio>. Os ads vencedores estao testando <hook dominante>, e voce pode entrar com <angle oposto>.

## Concorrentes estudados
1. [Concorrente 1](url) — player dominante, <N> anos, R$<receita estimada>
2. Concorrente 2 — ...
3. Concorrente 3 — ...
4. Concorrente 4 — ...
5. Concorrente 5 — ...

## Positioning map
![](./competitors/positioning-map.png)

## Comparativo detalhado
Ver [comparison.md](./competitors/comparison.md).

## Insights acionaveis
Ver [insights.md](./competitors/insights.md).

## Assets coletados
- 25 screenshots (5 por concorrente)
- 5 tokens.json extraidos
- ~20 ads do Meta Ad Library com texto + imagem
```

## Quality bar

- **Estudo real, nao teatro.** Se voce nao conseguiu screenshot de um concorrente (bloqueio, Cloudflare), diz — nao inventa dados.
- **Meta Ad Library e LEI.** Se o concorrente roda ads, isso e publico. Sempre inclua. Se nao roda, flag "oportunidade: concorrente X nao esta em ads Meta — voce pode dominar essa midia."
- **Positioning map com eixos defensaveis.** Os 2 eixos tem que fazer sentido pro nicho — nao use "preco × qualidade" por padrao porque e ruido.
- **Insights acionaveis.** Nada de "voce deve inovar." Quero "Voce deve usar verde porque 4/5 usam azul."
- **Respeite direitos.** Nunca copie assets visuais; o estudo e pra entender padroes, nao pra clonar. Cite todos os concorrentes com link.

## Handoff

Retorna:
- Path pra `02-competitor-research.md`
- TL;DR em 3 frases
- Brecha de posicionamento identificada (frase de 1 linha)
- Top 3 hooks vencedores dos ads dos concorrentes (alimenta `ad-creatives`)
- Palette / tipografia a EVITAR (alimenta `brand-direction` e `logo-design`)
