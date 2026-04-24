---
name: landing-page
description: Gera uma landing page de venda focada em conversao (nao site institucional) — hero + problema + solucao + prova + oferta + garantia + FAQ + CTA, com A/B test plan. Entrega HTML+CSS pronto pra deploy ou Next.js/Astro page component no repo existente. Otimizada pra ad-traffic (Meta/Google). Use depois de conversion-angle e brand-direction.
---

# Landing Page

> **Source & credit**: LP structure destilada de [Unbounce's conversion benchmark report 2025](https://unbounce.com/conversion-benchmark-report/) e [Julian Shapiro's growth landing page playbook](https://www.julian.com/guide/growth/landing-pages). Anti-objection framework de [Russell Brunson's DotCom Secrets](https://www.dotcomsecrets.com). Performance patterns (LCP<2.5s, zero CLS) de Core Web Vitals guidelines.

## Purpose

Uma landing page de venda e **diferente do site institucional**. Site e pra quem ja conhece a marca; LP e pra quem clicou num ad frio. Precisa:

- Entregar a promessa do ad em 3 segundos
- Responder "o que e, pra quem, quanto custa, e se nao der certo?"
- Ter 1 conversao clara — nao 5 links no menu
- Carregar em <2.5s em 3G mobile

Essa skill entrega LP em codigo, nao em builder (Unbounce/Leadpages) — pra voce ter controle total, SEO nao ficar na mao de terceiro, e nao pagar assinatura.

## Input

- `./rebrand/05-conversion-angle.md` — big promise, hooks, offer stack, proof, CTA
- `./rebrand/06-direction.md` + `06-new-tokens.<slug>.json` — tokens visuais
- `./rebrand/07-logo.md` (se existir) — logo assets
- `./rebrand/01-discovery.md` — ticket, objecoes, provas sociais

## Procedure

### 1. Estrutura de 9 blocos

Cada LP de conversao tem esses blocos, nessa ordem:

```
1. NAV (minima)              → logo + 1 CTA "Quero agora" (sem menu distraindo)
2. HERO                       → headline + sub + CTA primario + hero image/video
3. SOCIAL PROOF BAR           → "12.483 clientes" + 5 logos de empresa / imprensa
4. PROBLEMA/SOLUCAO (PAS)     → "Voce cansou de X? A gente entende. Por isso fizemos Y"
5. BENEFICIOS (3-5 cards)     → nao features, beneficios — com icone + titulo + 1 linha
6. COMO FUNCIONA (3 passos)   → "1. Compre / 2. Instale / 3. Veja resultado"
7. PROVA SOCIAL (testemunhos) → 3-5 cards com foto + nome + resultado especifico
8. OFERTA                     → preco + offer stack do conversion-angle + garantia + urgencia
9. FAQ (8-12 perguntas)       → anti-objecao: preco, garantia, prazo, diferenciais
10. CTA FINAL                 → hero repeated, ou "Ultima chance" com urgencia
11. FOOTER MINIMO             → CNPJ + endereco + politica privacidade + termos
```

**Importante**: nao tem blog, nao tem "sobre nos" longo, nao tem newsletter signup distraindo.

### 2. Copy blocks com tokens

Usa o `conversion-angle.md` como fonte da verdade. Cada bloco puxa:

- **HERO headline**: `big_promise`
- **HERO sub**: `target_sub_audience` + diferencial
- **HERO CTA**: `ctas.primary`
- **PROBLEMA**: parafraseado do `audience.dor_principal`
- **BENEFICIOS**: 3-5 extraidos do `offer_stack`
- **PROVA**: do `proof_stack`, priorizando `numero` > `case` > `autoridade`
- **OFERTA**: `offer_stack` inteiro com prices
- **FAQ**: gera 8-12 perguntas baseadas em objecoes comuns + discovery

### 3. Detecta stack do repo alvo

Mesma logica do `apply-rebrand`:

- **nextjs** → gera em `app/ofertas/<slug>/page.tsx` (App Router) ou `pages/ofertas/<slug>.tsx` (Pages Router)
- **astro** → gera em `src/pages/ofertas/<slug>.astro`
- **static HTML** → gera como HTML standalone em `./ofertas/<slug>/index.html`
- **wordpress** → gera como template custom `page-<slug>.php` + CSS
- **nenhum / nao aplica** → gera HTML standalone em `./rebrand/landing-page/` pra deploy em Vercel/Netlify/Cloudflare Pages

### 4. Componentes (ou HTML) por bloco

**Exemplo Next.js + Tailwind** (variante padrao):

```tsx
// app/ofertas/[slug]/page.tsx
export default function LandingPage() {
  return (
    <main className="min-h-screen bg-surface">
      <Nav />
      <Hero />
      <SocialProofBar />
      <ProblemSolution />
      <Benefits />
      <HowItWorks />
      <Testimonials />
      <Offer />
      <Faq />
      <FinalCta />
      <Footer />
    </main>
  )
}
```

Cada componente em `/components/landing/<Block>.tsx` com tokens Tailwind da direcao.

**Exemplo static HTML** (se nao tem framework):

Single-file `index.html` com CSS inline crítico (pro LCP) + resto de CSS em `<style>` embedded + JS minimo (so countdown + FAQ accordion + form submit).

### 5. Formulario & captura

CTA primario pode ser:

- **Compra direta** → link pra checkout (Stripe, Pagar.me, Hotmart, Kiwify, Shopify)
- **Lead capture** → form com 3 campos max: nome, email, whatsapp (se BR)
- **Demo booking** → integra com Cal.com ou SavvyCal via link

Pra lead capture, gera form que:
- Dispara evento `Lead` no Meta Pixel (sem passar pra client-side manualmente — usa Conversion API)
- Salva no provider de email (import manual ou webhook pra ActiveCampaign/Mailchimp)
- Redireciona pra thank-you page com proximo passo claro

### 6. Thank-you page

Sempre gera tambem `./ofertas/<slug>/obrigado/` (ou equivalente) com:

- Confirmacao ("Cadastro recebido")
- **Proximo passo imediato** (o ouro dessa pagina) — "Veja esse video de 5 min", ou "Entra no grupo Telegram", ou "Aguarda email em 2 min"
- Tracking event `CompleteRegistration` ou `Purchase`

Conversion do thank-you importa pra ads: Meta otimiza pelo evento final, nao pelo click.

### 7. Performance budget

Toda LP gerada respeita:

- **LCP < 2.5s** — hero image otimizada (WebP, next/image se nextjs, <img loading="eager" fetchpriority="high">)
- **CLS = 0** — nenhum bloco pula (reserve space pra tudo que carrega async)
- **JS < 100kb** — sem libs pesadas; countdown + accordion em JS vanilla
- **Imagens otimizadas** — WebP com AVIF fallback, responsive srcset
- **Fontes self-hosted ou next/font** — nao carrega Google Fonts de CDN lenta

Validacao: roda Lighthouse apos build, falha se performance < 90.

### 8. A/B test plan

`./rebrand/landing-page/ab-test-plan.md`:

```markdown
# A/B Test Plan — LP <slug>

## Variante A (controle)
- Hero headline: "<big_promise>"
- CTA: "<ctas.primary>"

## Variante B (hipotese: urgencia aumenta CVR)
- Hero: + countdown "Oferta expira em 48h"
- CTA: "Garantir meu lugar (48h)"

## Variante C (hipotese: prova social no topo converte mais)
- Move bloco Testimonials pra logo depois do Hero
- Rest identico

## Setup
- Tool: GrowthBook / PostHog experiments / Vercel Edge Config
- Trafego: split 33/33/33
- Minimo pra decidir: 500 conversoes por variante ou 95% confidence

## Metrica
- Primary: visitor → CompleteRegistration rate
- Secondary: time on page, scroll depth, FAQ open rate
```

### 9. Output umbrella

`./rebrand/09-landing-page.md`:

```markdown
# Landing Page — <oferta>

## Arquivos
- Codigo: <path no repo detectado>
- Standalone: `./rebrand/landing-page/`
- Thank-you: `./ofertas/<slug>/obrigado/`
- A/B test: `./rebrand/landing-page/ab-test-plan.md`

## Conectores
- Form submit: <provider>
- Pixel events: PageView (auto), Lead (form submit), Purchase (thank-you)
- Conversion API: server-side via `/api/fb-events` route

## Checklist pre-deploy
- [ ] Pixel ID em env
- [ ] Conversion API access token em env
- [ ] Provider de email conectado (webhook ou manual import)
- [ ] Checkout link valido (se venda direta)
- [ ] Links internos sem broken
- [ ] Mobile test em iPhone real + Android Chrome
- [ ] Lighthouse score ≥ 90 em performance
- [ ] GTM/GA4 tag de event disparando

## Deploy
- Vercel: `vercel deploy` (se Next.js)
- Netlify: drag-and-drop `./rebrand/landing-page/` (se static)
- CF Pages: conecta repo + branch

## Dominio / path
- Se usa site principal: `/ofertas/<slug>`
- Se subdominio: `oferta.<dominio>.com` (recomendado pra LP pura — evita canonical conflict com site)
```

## Quality bar

- **Zero distracoes.** Menu top = 1 CTA, rodape = minimo legal. Sem links pra blog, sobre nos, instagram.
- **Hero promete o mesmo que o ad.** Message match critico — se ad diz "10 min", hero tambem fala "10 min".
- **CTA primario no minimo 4 vezes na pagina** — hero, depois de beneficios, depois de prova, bloco final.
- **Mobile-first, sempre.** 70% do ad-trafico e mobile. Testa de verdade no celular antes de lancar.
- **Urgencia so se for real.** Countdown fake mata trust. Use "Oferta de lancamento ate <data real>" ou "vagas limitadas (real)".

## Handoff

Retorna:
- Path pra `09-landing-page.md` + codigo gerado
- Link pra preview local (se Next.js/Astro: `npm run dev`)
- Score de Lighthouse pos-build
- Lista de env vars que precisam ser setadas
