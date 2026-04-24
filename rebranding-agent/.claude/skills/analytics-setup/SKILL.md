---
name: analytics-setup
description: Configura o stack completo de tracking — GA4 + Meta Pixel + Conversion API server-side + GTM + Consent Mode pra LGPD/GDPR + UTM discipline + dashboards baseline (Looker Studio / PostHog). Gera codigo pronto pra Next.js/Astro/static e scripts de setup. Sem isso, voce nao consegue otimizar nada. Use depois de apply-rebrand.
---

# Analytics Setup

> **Source & credit**: GA4 + GTM setup pattern de [Simo Ahava](https://www.simoahava.com) (referencia mundial em tagging). Meta CAPI implementation de [developers.facebook.com/docs/marketing-api/conversions-api](https://developers.facebook.com/docs/marketing-api/conversions-api). Consent Mode V2 de [Google consent docs](https://developers.google.com/tag-platform/security/guides/consent).

## Purpose

"O que nao se mede, nao se melhora." Sem analytics bem montado:
- Ads otimizam no evento errado (ex: click em vez de compra)
- Voce nao sabe qual canal traz receita real
- Attribution apontando pro "organico" quando era ad
- Nao consegue re-marketing preciso

Essa skill entrega:
- GA4 configurado com eventos custom alinhados ao funil
- Meta Pixel + Conversion API server-side (critico pos-iOS14)
- Google Tag Manager com containers pre-configurados
- Consent Mode V2 pra LGPD/GDPR (banner + state management)
- UTM discipline (builder + taxonomy docs)
- Dashboards iniciais em Looker Studio

## Input

- `./rebrand/01-discovery.md` — modelo de receita, regiao (BR → LGPD, EU → GDPR)
- `./rebrand/13-landing-page.md` (se existir) — pagina que precisa de tracking
- Repo do site

## Procedure

### 1. Define os eventos-chave do funil

Por tipo de negocio, padroes:

**E-commerce (DTC)**
```
page_view → view_item → add_to_cart → begin_checkout → add_payment_info → purchase
                                                                        → purchase_return (opcional)
```

**SaaS**
```
page_view → view_pricing → start_free_trial → complete_onboarding → first_action → subscribe → upgrade
```

**Infoproduto**
```
page_view → view_offer → lead (form) → checkout_start → purchase → join_community → complete_module
```

**Servico / alto ticket**
```
page_view → view_service → schedule_call → call_completed → proposal_sent → contract_signed
```

Todos registrados em ambos GA4 + Meta Pixel (nomes alinhados mas respeitando requirements de cada).

### 2. Gera GTM container

`./rebrand/analytics/gtm-container.json` — importavel no GTM com:

- **Tag**: GA4 Config (com Measurement ID via env)
- **Tag**: GA4 Event (per evento-chave, com parameters mapeados)
- **Tag**: Meta Pixel base + events
- **Tag**: Meta CAPI gateway (envia evento server-side)
- **Tag**: Google Ads Conversion (se user roda Google Ads)
- **Triggers**: form submit, button click, custom event, timer (scroll depth)
- **Variables**: pegam dados da dataLayer, cookies, URL params
- **Consent state check**: tags nao disparam sem consent

### 3. Instala no codigo

Detecta stack (mesma logica do apply-rebrand) e adiciona:

**Next.js (App Router)**
```tsx
// app/layout.tsx
import { GTM, GTMNoscript } from '@/components/analytics/gtm'
import { ConsentBanner } from '@/components/analytics/consent'

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <head>
        <GTM id={process.env.NEXT_PUBLIC_GTM_ID!} />
      </head>
      <body>
        <GTMNoscript id={process.env.NEXT_PUBLIC_GTM_ID!} />
        <ConsentBanner />
        {children}
      </body>
    </html>
  )
}
```

Componentes gerados em `components/analytics/`:
- `gtm.tsx` — tag manager
- `consent.tsx` — banner LGPD + state
- `pixel-events.ts` — helpers pra disparar eventos
- `server-events.ts` — helpers pra Conversion API server-side

### 4. Conversion API (server-side)

Critico pos-iOS14 — Meta perde ~30% de eventos se so client-side.

Gera route handler:

```ts
// app/api/fb-events/route.ts
import { NextRequest } from 'next/server'
import crypto from 'crypto'

export async function POST(req: NextRequest) {
  const body = await req.json()
  const pixelId = process.env.META_PIXEL_ID!
  const accessToken = process.env.META_CAPI_TOKEN!

  const event = {
    event_name: body.event_name,
    event_time: Math.floor(Date.now() / 1000),
    action_source: 'website',
    event_source_url: body.url,
    user_data: {
      em: body.email ? hash(body.email) : undefined,
      ph: body.phone ? hash(body.phone) : undefined,
      fbc: body.fbc,  // Facebook click ID
      fbp: body.fbp,  // Facebook browser ID
      client_ip_address: req.headers.get('x-forwarded-for') ?? undefined,
      client_user_agent: req.headers.get('user-agent') ?? undefined,
    },
    custom_data: body.custom_data,
    event_id: body.event_id,  // dedup com client-side
  }

  await fetch(`https://graph.facebook.com/v18.0/${pixelId}/events`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ data: [event], access_token: accessToken }),
  })

  return Response.json({ ok: true })
}

function hash(value: string) {
  return crypto.createHash('sha256').update(value.trim().toLowerCase()).digest('hex')
}
```

**Importante**: `event_id` deve bater com o client-side pra Meta dedupar. Sem isso, dobra eventos e estraga CPA.

### 5. Consent Mode V2

Pra LGPD/GDPR, tags so podem disparar apos consent. Gera:

**Banner** (componente):
- Aparece no primeiro page_view
- 2 botoes: "Aceitar tudo" / "So essenciais"
- Opcional: "Personalizar" (abre modal com toggles por categoria)
- Decisao salva em cookie 1st-party por 365 dias
- Respeita "Do Not Track" do browser

**State management**:
```js
// inicial (antes de consent)
gtag('consent', 'default', {
  ad_storage: 'denied',
  analytics_storage: 'denied',
  ad_user_data: 'denied',
  ad_personalization: 'denied',
  wait_for_update: 500,
})

// apos "Aceitar tudo"
gtag('consent', 'update', {
  ad_storage: 'granted',
  analytics_storage: 'granted',
  ad_user_data: 'granted',
  ad_personalization: 'granted',
})
```

Assim Google/Meta sao notificados do state e disparam tag so se autorizado, alem de ativar "Consent Mode Data Modeling" pra preencher gaps.

### 6. UTM discipline

`./rebrand/analytics/utm-taxonomy.md`:

```markdown
# UTM Taxonomy — padrao pra todos os links

## Format
utm_source=<canal>&utm_medium=<tipo>&utm_campaign=<campanha>&utm_content=<creative>&utm_term=<detalhe>

## Valores permitidos

### utm_source
- meta / google / tiktok / linkedin / email / whatsapp / instagram / youtube / blog / affiliate

### utm_medium
- cpc (paid click) / display / video / social / email / affiliate / referral / organic-social / sms

### utm_campaign
- <ano>-<mes>-<nome-kebab> (ex: 2026-04-checkout-launch)

### utm_content
- <creative-id> (mesmo id do ad-creatives skill)

### utm_term
- <hook-id>_<creative-type>_<copy-id>
```

Gera tambem `./rebrand/analytics/utm-builder.html` — mini ferramenta web pra montar URLs consistentes (evita erro humano).

### 7. Dashboards

Gera 3 dashboards Looker Studio como **template links** (usuario clica "Usar template" pra clonar):

1. **Overview** — sessoes, conversoes, top canais, receita por canal
2. **Ads performance** — cruzamento Meta/Google com GA4, CPA, ROAS
3. **Funil completo** — view → cart → checkout → purchase com drop-off rate por step

Alternativa: script Python que cria os dashboards via Looker Studio API (se user tem GCP project).

### 8. Output umbrella

`./rebrand/14-analytics-setup.md`:

```markdown
# Analytics Setup — <marca>

## Instalado
- GTM container: GTM-XXXXXX (em env)
- GA4 property: G-XXXXXXXXXX (em env)
- Meta Pixel: XXXXXXXXXXXX (em env)
- Meta CAPI: configurado em /api/fb-events
- Consent banner: ativo, LGPD-compliant

## Eventos rastreados
<tabela evento → trigger → destino (GA4/Meta) → parameters>

## .env adicionado
```env
NEXT_PUBLIC_GTM_ID=GTM-XXXXXX
NEXT_PUBLIC_GA4_ID=G-XXXXXXXXXX
NEXT_PUBLIC_META_PIXEL_ID=XXXXXXXXXXXX
META_CAPI_TOKEN=<nunca client-side>
```

## Dashboards
- [Overview](link-template-looker)
- [Ads Performance](link)
- [Funnel](link)

## UTM builder
Abrir `./rebrand/analytics/utm-builder.html` e bookmarkar pra criar links consistentes.

## Pre-launch checklist
- [ ] GTM publicado (nao so "preview mode")
- [ ] Eventos testados no GA4 DebugView
- [ ] Eventos testados no Meta Events Manager → Test Events
- [ ] Consent banner aparece em nova visita (teste janela anonima)
- [ ] CAPI recebendo eventos em real-time (Events Manager)
- [ ] Dedup entre Pixel e CAPI funcionando (event_id match)
- [ ] Consent Mode: sem consent → nao dispara tag; com consent → dispara
- [ ] UTM params persistindo em session (pra attribution cross-page)

## Post-launch (7 dias)
- [ ] Valida attribution: comparar Meta Ads Manager vs GA4 direct traffic
- [ ] Checar taxa de consent (quantos aceitam) — se <60%, revisar banner
- [ ] Validar que CAPI melhora match quality (Events Manager → Match Quality)
```

## Quality bar

- **Hash de email/telefone em CAPI e obrigatorio.** SHA-256, lowercase, trim. Sem hash = violacao LGPD/FB policy.
- **Access token server-side only.** Nunca em code client-side, nunca committado.
- **Dedup client vs server.** `event_id` alinhado; senao, dobra.
- **Banner antes de qualquer tag.** Sem consent = sem tracking. LGPD nao brinca.
- **Teste em janela anonima.** Cookie de consent antigo mascara bugs.

## Handoff

Retorna path pra `14-analytics-setup.md`, lista de env vars criadas, links dos dashboards, e checklist pre-launch.
