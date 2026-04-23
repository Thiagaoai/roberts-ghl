# Rebranding Agent

Agente de rebranding **completo de empresa** pra Claude Code. Nao e um "gerador de site" — e o agente que pega uma marca (existente ou ideia) e entrega tudo que precisa pra **vender**: nome, logo, identidade visual, site, presenca online, e criativos de ad prontos pra subir na Meta.

Feito pra rodar dentro do [Claude Code](https://claude.com/claude-code) — um orchestrator + 10 skills, cada uma cuidando de uma fase, com checkpoints de aprovacao do usuario entre as fases criticas.

---

## O que ele entrega

| # | Fase | Skill | Entrega |
| --- | --- | --- | --- |
| 1 | Discovery | `discover-brand` | Brief completo: negocio, oferta, publico, concorrentes, canais ativos, ads, nao-negociaveis |
| 2 | Pesquisa de concorrentes | `competitor-research` | Estudo dos 3-5 maiores: site, tokens visuais, social, **ads rodando na Meta Ad Library**, mapa 2x2, brecha de posicionamento |
| 3 | Nomes *(se renomear)* | `naming` | 15 candidatos em 5 arquetipos + tagline + check de dominio `.com`/`.com.br` + check de handle @ — **checkpoint** |
| 4a | Auditoria do site | `site-audit` | Screenshots mobile/tablet/desktop + critica visual/UX/a11y/SEO com score 0-10 por dimensao |
| 4b | Tokens atuais | `style-extract` | JSON estruturado da palette / tipografia / spacing / radius / shadows do site atual |
| 5 | Angle de conversao | `conversion-angle` | Big promise + 3 hooks + offer stack + prova social priorizada + CTAs — o que **vende** |
| 6 | Direcao de marca | `brand-direction` | 2-3 direcoes visuais completas (palette + tipografia + voz + mockup) — **checkpoint** |
| 7 | Logo *(se novo)* | `logo-design` | 3 conceitos com exports SVG/PNG/favicon/avatar/OG — **checkpoint** |
| 8 | Presenca online | `social-presence` | Bio + avatar + cover + 3 templates de post pra IG, FB, LinkedIn, X, TikTok, YouTube, WhatsApp Business, Google Business Profile |
| 9 | Criativos de ad | `ad-creatives` | **27 criativos Meta** (3 hooks × 3 formatos × 3 copies), em 1:1, 4:5, 9:16, com UTM, CSV de import, e plano de teste de 7 dias |
| 10 | Aplicar tudo | `apply-rebrand` | Detecta stack (Next.js/Astro/React/static/WP), aplica tokens no codigo, substitui copy, instala favicon + OG + Meta Pixel, screenshots before/after, abre PR — **checkpoint** |

---

## Como usar

### 1. Copia esse `.claude/` pro teu projeto

```bash
# no repo da empresa que vai ser rebrand-ada
git clone https://github.com/Thiagaoai/Agent.rebranding-.git /tmp/rebrand
cp -r /tmp/rebrand/.claude .claude
```

Ou adiciona como submodule se quiser receber updates:

```bash
git submodule add https://github.com/Thiagaoai/Agent.rebranding-.git .rebrand-agent
ln -s .rebrand-agent/.claude .claude
```

### 2. Roda o Claude Code no repo

```bash
cd seu-repo
claude
```

### 3. Invoca o agente

No Claude Code:

```
Use o agente rebrander pra fazer rebranding completo da minha empresa.
```

Ou direto: `@rebrander`.

O agente assume dali — faz o interview, roda competitor research, etc.

---

## Requisitos

- **Claude Code** CLI ou web (https://claude.com/claude-code)
- **Node.js** 18+ no sistema (pro Playwright)
- **Playwright** (instalado automaticamente na primeira auditoria; ou `npm i -D playwright && npx playwright install chromium`)
- *Opcional*: `ImageMagick` (pra gerar `favicon.ico` a partir do SVG — sem ele, o agente gera PNGs mas pula o `.ico`)
- *Opcional*: `gh` CLI (pra abrir PR automaticamente; sem ele, o agente imprime o link de criacao manual)

---

## Estrutura do repo

```
.claude/
├── agents/
│   └── rebrander.md          # orchestrator
└── skills/
    ├── discover-brand/
    ├── competitor-research/
    ├── naming/
    ├── site-audit/
    ├── style-extract/
    ├── conversion-angle/
    ├── brand-direction/
    ├── logo-design/
    ├── social-presence/
    ├── ad-creatives/
    └── apply-rebrand/
```

Durante execucao, **tudo** vai parar em `./rebrand/` no repo alvo:

```
./rebrand/
├── 01-discovery.md
├── 02-competitor-research.md
├── 03-naming.md
├── 04-audit.md
├── 04-current-tokens.json
├── 05-conversion-angle.md
├── 06-direction.md
├── 07-logo.md
├── 08-social-presence.md
├── 09-ad-creatives.md
├── 10-before-after.md
├── 10-apply-report.md
├── competitors/
├── mockups/
├── logo/{concept-1, concept-2, concept-3, final}/
├── screenshots/
├── social/{instagram, facebook, linkedin, x, tiktok, youtube, ...}/
└── ads/meta/
```

Tudo inspecionavel — voce pode abrir qualquer arquivo a qualquer momento.

---

## Filosofia

- **Checkpoints sao lei.** O agente NUNCA toma decisao irreversivel (nome final, logo final, direcao, PR) sem aprovacao explicita do usuario.
- **Nada de claim sem base.** Se nao tem prova social, a skill de conversion-angle flaga em vez de inventar "10k clientes felizes".
- **Brecha > lugar-comum.** A skill de competitor-research existe pra identificar onde todos estao, pra voce nao ficar la tambem.
- **Entregavel editavel.** SVGs, HTML editavel, JSON de tokens — nada de PNG rasterizado final que trava o refinamento.
- **Bilingue por default.** Responde no idioma do usuario (PT-BR, EN, ou ambos).

---

## Credits (skills de que puxamos inspiracao)

- [anthropics/skills/brand-guidelines](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines) — token application pattern
- [anthropics/knowledge-work-plugins/brand-voice](https://github.com/anthropics/knowledge-work-plugins/tree/main/partner-built/brand-voice) — discovery interview pattern
- [garrytan/gstack/design-review](https://github.com/garrytan/gstack/tree/main/design-review) — site-audit critique structure
- [ivansong1981/ui-style-extractor](https://github.com/ivansong1981/ui-style-extractor) — style-extract tokens
- [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill) — Playwright skill wrapping
- [coreyhaines31/marketingskills/seo-audit](https://github.com/coreyhaines31/marketingskills/tree/main/skills/seo-audit) — SEO audit
- [rohitg00/awesome-claude-design](https://github.com/rohitg00/awesome-claude-design) — aesthetic family taxonomy
- [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) — ad testing matrix (3x3x3)

---

## Licenca

MIT. Use, modifique, redistribua. So mantenha os creditos originais nos SKILL.md que referenciam projetos upstream.
