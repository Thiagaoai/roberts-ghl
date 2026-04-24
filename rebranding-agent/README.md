# Rebranding Agent

Agente de rebranding **completo de empresa** pra Claude Code. Nao e um "gerador de site" — e o agente que pega uma marca (existente ou ideia) e entrega tudo que ela precisa pra **vender**: pesquisa, identidade, infraestrutura comercial, trafego pago, follow-up, distribuicao organica, lancamento.

Feito pra rodar dentro do [Claude Code](https://claude.com/claude-code) — um orchestrator + **25 skills** organizadas em 6 blocos, com checkpoints de aprovacao do usuario entre as fases criticas.

---

## O que ele entrega

### Bloco A — Pesquisa & identidade

| # | Skill | Entrega |
| --- | --- | --- |
| 01 | `discover-brand` | Brief completo: negocio, oferta, publico, concorrentes, canais, ads, nao-negociaveis |
| 02 | `competitor-research` | Estudo dos 3-5 maiores: site, tokens, social, **ads Meta Ad Library**, mapa 2x2, brecha |
| 03 | `naming` *(opcional)* | 15 nomes em 5 arquetipos + tagline + check `.com`/`.com.br` + handles — **checkpoint** |
| 04a | `site-audit` | Screenshots mobile/tablet/desktop + critica visual/UX/a11y/SEO |
| 04b | `style-extract` | JSON dos tokens (palette, tipografia, spacing, radius, shadows) do site atual |
| 05 | `conversion-angle` | Big promise + 3 hooks + offer stack + prova social + CTAs |
| 06 | `brand-direction` | 2-3 direcoes visuais + voz + mockup — **checkpoint** |
| 07 | `logo-design` *(opcional)* | 3 conceitos com SVG/PNG/favicon/avatar/OG — **checkpoint** |

### Bloco B — Infraestrutura comercial

| # | Skill | Entrega |
| --- | --- | --- |
| 08 | `legal-compliance` | Politica Privacidade (LGPD/GDPR), Termos, Cookies, disclaimers por nicho regulado, checklist Meta/Google Ads policies |
| 09 | `landing-page` | LP de venda (hero + problema + solucao + prova + oferta + FAQ + CTA) em Next.js/Astro/HTML + A/B plan |
| 10 | `lead-magnet` | PDF/checklist/template + LP opt-in + thank-you + 7 emails de nurture |
| 11 | `analytics-setup` | GA4 + Meta Pixel + **Conversion API server-side** + GTM + Consent Mode V2 + UTM discipline + dashboards Looker |

### Bloco C — Trafego pago & criativos

| # | Skill | Entrega |
| --- | --- | --- |
| 12 | `ad-creatives` | **27 criativos Meta** (3 hooks × 3 formatos × 3 copies) + CSV import + plano teste 7d |
| 13 | `ugc-scripts` | 6 scripts UGC (15s/30s/60s) com shot list + briefing de creator + overlay SRT |
| 14 | `google-ads` | Search (brand+non-brand) + Performance Max + YouTube + Remarketing + CSV pra Google Ads Editor |

### Bloco D — Relacionamento & follow-up

| # | Skill | Entrega |
| --- | --- | --- |
| 15 | `email-sequences` | 4 sequencias (welcome 5, carrinho 3, re-engagement 5, pos-venda 7) + import Mailchimp/AC/Klaviyo/RD |
| 16 | `whatsapp-flow` | Boas-vindas + FAQ (12 respostas) + funil conversacional + 7 templates Meta + scripts atendimento |
| 17 | `review-setup` | Google Business + Trustpilot + Reclame Aqui + G2 + templates de resposta + NPS gate + widget |

### Bloco E — Distribuicao organica

| # | Skill | Entrega |
| --- | --- | --- |
| 18 | `social-presence` | Bio + avatar + cover + 3 templates de post pra 8 canais (IG, FB, LI, X, TT, YT, WA, GBP) |
| 19 | `content-calendar` | 30 dias × cada canal ativo = ate 150 posts com copy pronto + hashtags + horario + export Notion/Airtable |
| 20 | `seo-content-plan` | 6 meses de pillars + clusters, keyword research, technical audit, link building, rebrand-SEO migration |
| 21 | `pr-kit` | Release PT-BR/EN + fact sheet + bio + logos + **media list BR/intl** + 4 templates de pitch + site imprensa |

### Bloco F — Consolidacao & lancamento

| # | Skill | Entrega |
| --- | --- | --- |
| 22 | `brand-book-pdf` | **Brand book PDF imprimivel** + site brand.< dominio > + Figma library (tokens W3C) |
| 23 | `launch-plan` | Timeline 14-30d (teaser → countdown → D=0 → sustain → optimize) + copy por canal + rollback plan |
| 24 | `apply-rebrand` | Detecta stack, aplica tokens no codigo, substitui copy, favicon/OG/Pixel, screenshots before/after, abre PR — **checkpoint** |

---

## Como usar

### 1. Copia esse `.claude/` pro teu projeto

```bash
# no repo da empresa que vai ser rebrand-ada
git clone https://github.com/Thiagaoai/Agent.rebranding-.git /tmp/rebrand
cp -r /tmp/rebrand/.claude .claude
```

Ou adiciona como submodule:

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

```
Use o agente rebrander pra fazer rebranding completo da minha empresa.
```

Ou `@rebrander`. O agente assume dali — faz o interview, roda competitor research, e ativa so as skills que fazem sentido pro caso (ver "Pipeline activation" abaixo).

---

## Pipeline activation — o que roda quando

Nem todas as 25 skills rodam em toda execucao. A decisao vem do `discover-brand` e e transparente no `01-discovery.md`:

| Condicao | Skills ativadas |
| --- | --- |
| **Sempre** | discover-brand, competitor-research, brand-direction, conversion-angle, legal-compliance, brand-book-pdf, launch-plan |
| Renomear = sim | + naming |
| Logo novo | + logo-design |
| URL do site existe | + site-audit, style-extract, apply-rebrand |
| Vende direto / roda ads | + landing-page, analytics-setup |
| B2B / high-ticket / email-strategic | + lead-magnet, email-sequences |
| Regiao BR | + whatsapp-flow (LGPD + Reclame Aqui automaticos) |
| Nicho regulado (saude/financeiro/crianca) | legal-compliance com disclaimer + **flag pra advogado** |
| Rodando ads Meta | + ad-creatives, ugc-scripts |
| B2B / intent-based / servico | + google-ads |
| Canais sociais ativos | + social-presence, content-calendar |
| Busca organica relevante | + seo-content-plan |
| Quer autoridade / imprensa | + pr-kit |
| Vende (DTC/SaaS/servico) | + review-setup |

Exemplos de combinacoes:

- **Rebrand DTC BR completo (padrao-ouro)**: Blocos A + B + C + D + E + F (~22 skills ativas) — pula google-ads/seo se publico e so-social
- **SaaS B2B internacional**: Blocos A + B + C (inclui google-ads) + D (G2/Capterra) + E (inclui seo) + F
- **So identidade pra empresa existente**: Bloco A + brand-book-pdf (6-8 skills)
- **Launch de produto novo em marca existente**: A (parcial) + B + C + D (email) + E (content-calendar) + F (launch-plan)

---

## Requisitos

- **Claude Code** CLI ou web (https://claude.com/claude-code)
- **Node.js** 18+ (pro Playwright + geracao de PDFs)
- **Playwright** (auto-instalado; ou `npm i -D playwright && npx playwright install chromium`)
- *Opcional*: `ImageMagick` (pra `favicon.ico`)
- *Opcional*: `gh` CLI (pra abrir PR automaticamente)
- *Opcional*: credenciais de providers (Mailchimp/ActiveCampaign/Klaviyo/Z-API) pra import direto — sem elas, o agente gera CSVs pra import manual

---

## Estrutura do repo

```
.claude/
├── agents/
│   └── rebrander.md          # orchestrator
└── skills/
    ├── discover-brand/             competitor-research/     naming/
    ├── site-audit/                 style-extract/           conversion-angle/
    ├── brand-direction/            logo-design/             legal-compliance/
    ├── landing-page/               lead-magnet/             analytics-setup/
    ├── ad-creatives/               ugc-scripts/             google-ads/
    ├── email-sequences/            whatsapp-flow/           review-setup/
    ├── social-presence/            content-calendar/        seo-content-plan/
    ├── pr-kit/                     brand-book-pdf/          launch-plan/
    └── apply-rebrand/
```

Durante execucao, **tudo** vai parar em `./rebrand/` no repo alvo:

```
./rebrand/
├── 01-discovery.md              02-competitor-research.md
├── 03-naming.md                 04-audit.md + 04-current-tokens.json
├── 05-conversion-angle.md       06-direction.md + 06-new-tokens.<slug>.json
├── 07-logo.md                   08-social-presence.md
├── 09-ad-creatives.md           10-before-after.md + 10-apply-report.md
├── 11-email-sequences.md        12-whatsapp-flow.md
├── 13-landing-page.md           14-analytics-setup.md
├── 15-legal-compliance.md       16-brand-book.md
├── 17-content-calendar.md       18-launch-plan.md
├── 19-google-ads.md             20-pr-kit.md
├── 21-review-setup.md           22-lead-magnet.md
├── 23-seo-content-plan.md
│
├── competitors/                 screenshots/
├── mockups/                     logo/{concept-1..3, final}/
├── social/{instagram, facebook, linkedin, x, tiktok, youtube, ...}/
├── ads/meta/                    ugc/                 google-ads/
├── email/                       whatsapp/            reviews/
├── content-calendar/            seo/                 press-kit/
├── brand-book/ (PDF + site)     lead-magnet/         landing-page/
└── launch-plan/
```

Tudo inspecionavel — voce pode abrir qualquer arquivo a qualquer momento.

---

## Filosofia

- **Checkpoints sao lei.** O agente NUNCA toma decisao irreversivel (nome, logo, direcao, PR, launch D=0) sem aprovacao explicita.
- **Nada de claim sem base.** Sem prova social real, `conversion-angle` flaga em vez de inventar. Sem CNPJ, `legal-compliance` marca placeholder visivel.
- **Brecha > lugar-comum.** `competitor-research` existe pra voce nao cair no mesmo visual/posicionamento de todo mundo.
- **Entregavel editavel.** SVG, HTML, JSON de tokens, CSV pra import — nada que trave refinamento.
- **Bilingue por default.** PT-BR, EN, ou ambos — detecta pelo idioma das respostas.
- **Nunca substitui advogado.** `legal-compliance` cobre baseline. Nicho regulado (saude/financeiro/crianca) **obrigatoriamente** pede revisao juridica antes de publicar.
- **Integracoes pragmaticas.** Se voce tem stack (Shopify, Mailchimp, WhatsApp Cloud API), o agente importa direto. Se nao, gera CSV pra voce subir manual.

---

## Credits

Cada SKILL.md lista as fontes especificas de onde o pattern foi destilado. Principais:

- [anthropics/skills/brand-guidelines](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines) — token application pattern
- [anthropics/knowledge-work-plugins/brand-voice](https://github.com/anthropics/knowledge-work-plugins/tree/main/partner-built/brand-voice) — discovery interview
- [garrytan/gstack/design-review](https://github.com/garrytan/gstack/tree/main/design-review) — site-audit critique
- [ivansong1981/ui-style-extractor](https://github.com/ivansong1981/ui-style-extractor) — style-extract
- [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill) — Playwright wrapping
- [coreyhaines31/marketingskills/seo-audit](https://github.com/coreyhaines31/marketingskills/tree/main/skills/seo-audit) — SEO audit
- [rohitg00/awesome-claude-design](https://github.com/rohitg00/awesome-claude-design) — aesthetic family taxonomy
- [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) — ad testing matrix
- [Copyhackers](https://copyhackers.com), [Val Geisler](https://val.geisler.co), [Klaviyo](https://www.klaviyo.com) — email sequences
- [Simo Ahava](https://www.simoahava.com), [Meta CAPI docs](https://developers.facebook.com/docs/marketing-api/conversions-api) — analytics-setup
- [iubenda](https://www.iubenda.com), [ANPD](https://www.gov.br/anpd), [GDPR.eu](https://gdpr.eu) — legal templates baseline
- [Savannah Sanchez](https://twitter.com/social_savannah), Foreplay / Motion teardowns — UGC scripts
- [Unbounce conversion benchmark](https://unbounce.com/conversion-benchmark-report/), [Julian Shapiro](https://www.julian.com/guide/growth/landing-pages) — landing-page
- [Jeff Walker PLF](https://productlaunchformula.com), DTC post-mortems — launch-plan
- [Ahrefs](https://ahrefs.com), [Backlinko](https://backlinko.com), [HubSpot topic clusters](https://www.hubspot.com/topic-clusters) — SEO
- [G2 Buyer Behavior Report](https://www.g2.com/research), [Jay Baer "Hug Your Haters"](https://www.jaybaer.com) — review-setup
- [AP Stylebook](https://www.apstylebook.com), [HARO](https://www.helpareporter.com) — PR kit
- [Justin Welsh](https://www.justinwelsh.me), [Sprout Social benchmarks](https://sproutsocial.com/insights/) — content-calendar
- [Drift](https://www.drift.com/), [Manychat](https://manychat.com) — whatsapp-flow
- [PPC Greg](https://www.youtube.com/@PPCGreg), [Aaron Young / Define Digital](https://www.youtube.com/@DefineDigital) — google-ads
- [Digital Marketer](https://www.digitalmarketer.com), [Ryan Levesque](https://askmethod.com) — lead-magnet
- [Stripe](https://stripe.com/brand), [Linear](https://linear.app/brand), [Figma brand](https://www.figma.com/brand/) — brand-book structure

---

## Licenca

MIT. Use, modifique, redistribua. So mantenha os creditos originais nos SKILL.md que referenciam projetos upstream.
