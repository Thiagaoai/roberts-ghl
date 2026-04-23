---
name: discover-brand
description: Phase 1 of the rebranding pipeline. Interviews the user about their company, offer, audience, competitors, aesthetic references, existing channels, and ads goals to produce a complete brand brief that drives every downstream skill (naming, logo, site, social presence, ad creatives). Use this when starting a rebrand project, before any naming, design, or ads work.
---

# Discover Brand

> **Source & credit**: Discovery pattern adapted from Anthropic's [brand-voice/discover-brand](https://github.com/anthropics/knowledge-work-plugins/tree/main/partner-built/brand-voice) and [anthropics/skills/brand-guidelines](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines). Extended here to cover naming, online presence, and ads — because this pipeline isn't just a website rebrand, it's a full business rebrand.

## Purpose

Turn a fuzzy "quero rebranding" request into a concrete brief that drives every downstream skill:

- **naming** needs the offer + positioning + emotional register
- **logo-design** needs the aesthetic family + non-negotiables
- **site-audit / brand-direction** need the audience + competitors
- **social-presence** needs which channels are active + handles
- **ad-creatives / conversion-angle** needs the offer, price point, and what's been tried before

Without a real discovery, everything downstream is guessing.

## Output

A single file at `./rebrand/01-discovery.md` in the target repo, following the template at the end.

## Interview procedure

Use `AskUserQuestion` — never a wall of open text. Batch related questions. The user can always pick "Other" for custom input. **Conduct the interview in the user's language** (Portuguese if they've been writing in Portuguese, English otherwise).

### Round 1 — the business & offer

1. **Category / industria** — e.g. SaaS, ecommerce DTC, servico local, infoproduto, agencia, clinica, restaurante.
2. **Stage** — pre-lancamento, comecando, escalando, estabelecido.
3. **O que voce vende exatamente** — produto/servico principal em 1 frase + ticket medio (faixa).
4. **Modelo de receita** — venda unica, assinatura, high-ticket, marketplace, ads.

### Round 2 — the audience

1. **Quem compra** — 1 frase (ex: "mulheres 25-40 de classe B que querem emagrecer sem dieta").
2. **Nivel de sofisticacao** — novato, informado, especialista no tema.
3. **Dor principal** — em 1 frase, na linguagem que o cliente usa.
4. **Driver emocional** — confianca, pertencer, status, seguranca, eficiencia, alegria.

### Round 3 — positioning & competitors

1. **3 concorrentes diretos** — URLs ou @s; se nao souber, pule.
2. **O que voce quer que pensem de voce** vs. **o que voce nao quer que pensem**.
3. **Unfair advantage** — por que voce, e nao o concorrente.
4. **Oferta "so nossa"** — a promessa unica em 1 frase.

### Round 4 — naming (se aplica)

1. **Voce quer renomear a empresa?** — sim / nao / talvez, depende das opcoes.
2. Se sim:
   - **Nome atual** (pra referencia).
   - **Estilo de nome preferido**: inventado (Google/Kodak) / descritivo (General Electric) / metaforico (Amazon) / founder-based (Ferrari) / acronimo (IBM).
   - **Idiomas permitidos**: PT-BR, EN, ambos, outro.
   - **Dominio .com obrigatorio?** sim / nao / pode ser `.com.br` / outro.
   - **Handles @ precisam bater** em IG/TikTok? sim / nao.

### Round 5 — aesthetic

1. **2-3 marcas que voce admira** (qualquer setor) — pega URLs pra referencia visual via WebFetch se fornecidas.
2. **Familia estetica**: Modern Minimal / Bold Playful / Editorial / Corporate Trust / Tech Futurist / Warm Handcrafted / Luxury Restrained / Outra.
3. **Instinto de cor** — cores obrigatorias, cores proibidas.
4. **Logo**: criar novo / manter atual / quero variantes do atual.

### Round 6 — online presence

1. **Canais ativos hoje** (multi-select): Instagram, Facebook, LinkedIn, X, TikTok, YouTube, WhatsApp Business, Google Business Profile, nenhum.
2. Pra cada canal ativo: **handle/URL atual**.
3. **Canais que voce quer ativar**: multi-select.
4. **Quem cuida do conteudo hoje** — eu mesmo, social media, agencia, ninguem.

### Round 7 — ads & conversion

1. **Voce roda ads hoje?** — Meta, Google, TikTok, nenhum.
2. Se sim:
   - **Investimento mensal** (faixa: <R$1k, R$1-5k, R$5-20k, R$20k+).
   - **Melhor criativo ate hoje** — URL ou descricao.
   - **CAC atual** e **ticket medio** se souber.
3. Se nao, **objetivo principal** do site pos-rebrand: gerar lead, vender direto, marcar autoridade, captar investidor.
4. **Prova social disponivel**: depoimentos (texto/video), cases, numeros, imprensa, nenhum.

### Round 8 — site & constraints

1. **URL do site atual** (se existe).
2. **Path do repo/source** (se vai aplicar mudanca via PR).
3. **Nao-negociaveis** — o que NAO pode mudar (nome, logo, cor, CNPJ, dominio).
4. **Budget pra assets novos**: stock gratis / stock pago / ilustracao custom / fotografia custom / nenhum.
5. **Prazo** — quando precisa estar no ar.

## Output template

Write `./rebrand/01-discovery.md` with this structure:

```markdown
# Brand Discovery — <company name>
_Generated <date> by the `discover-brand` skill_

## Business & offer
- **Categoria**: …
- **Estagio**: …
- **O que vende**: …
- **Ticket medio**: …
- **Modelo**: …

## Audience
- **Quem compra**: …
- **Sofisticacao**: …
- **Dor principal**: …
- **Driver emocional**: …

## Positioning
- **Concorrentes**: …
- **Quer ser vista como**: …
- **Nao quer ser vista como**: …
- **Unfair advantage**: …
- **Promessa unica**: …

## Naming (se renomear)
- **Renomear?**: sim / nao
- **Nome atual**: …
- **Estilo**: …
- **Idiomas**: …
- **.com obrigatorio**: …
- **Handles precisam bater**: …

## Aesthetic
- **Marcas admiradas**: …
- **Familia**: …
- **Cores obrigatorias / proibidas**: …
- **Logo**: criar novo / manter / variantes

## Online presence
- **Canais ativos**: com handles
- **Canais a ativar**: …
- **Quem cuida**: …

## Ads & conversion
- **Rodando ads?**: …
- **Investimento mensal**: …
- **Melhor criativo**: …
- **CAC / ticket**: …
- **Objetivo do site**: …
- **Prova social disponivel**: …

## Site & constraints
- **URL atual**: …
- **Repo path**: …
- **Nao-negociaveis**: …
- **Asset budget**: …
- **Prazo**: …

## Synthesized brief
_3-5 frases, o norte da rebranding. Tem que ser especifico o suficiente pra dois designers lerem e chegarem no mesmo bairro visual._

## Pipeline activation
_Based on the answers, which skills will run:_
- [x] competitor-research (sempre — alimenta todas as fases seguintes)
- [x] naming (se renomear = sim)
- [x] logo-design (se logo = criar novo ou variantes)
- [x] site-audit + style-extract + apply-rebrand (se URL atual existe)
- [x] brand-direction (sempre)
- [x] social-presence (pros canais ativos + a ativar)
- [x] conversion-angle (se rodando ads ou objetivo = vender direto)
- [x] ad-creatives (se rodando ads ou quer comecar)
```

## Quality bar

- **Round 8 (constraints) nunca pode ser pulada.** Nao-negociavel perdido aqui vira retrabalho em Fase 5.
- **Synthesized brief e a parte mais importante.** Se ficar generico, todo o resto fica generico.
- **Se o usuario der respostas contraditorias** (ex: "luxury restrained" + "bold playful"), aponte a tensao antes de gravar o brief.
- **Detecte idioma** — se o usuario ta respondendo em portugues, mantenha o interview em portugues (o template acima ja esta em PT-BR).

## Handoff

Quando terminar, imprima:
1. Caminho para `01-discovery.md`
2. A secao "Pipeline activation" — que skills vao rodar
3. Retorne controle ao orchestrator, que vai decidir a ordem.
