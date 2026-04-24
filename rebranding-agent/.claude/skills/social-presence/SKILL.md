---
name: social-presence
description: Gera presenca online completa pra marca rebranded — bios otimizadas, avatares, cover images, e 3 templates de post (reel cover, carrossel, story) pra cada canal ativo (Instagram, Facebook, LinkedIn, X, TikTok, YouTube, WhatsApp Business, Google Business Profile). Usa o logo final e a direcao de marca aprovada. Use depois de logo-design e brand-direction.
---

# Social Presence

> **Source & credit**: Bio structure baseada nos padroes de high-converting bio (hook + value + proof + CTA) de [Justin Welsh](https://www.justinwelsh.me) e [CopyAI](https://www.copy.ai/blog/instagram-bio-ideas). Asset dimensions conferidas no [Sprout Social size guide](https://sproutsocial.com/insights/social-media-image-sizes-guide/). Template generation via HTML + Playwright screenshot.

## Purpose

Quando o site ganha rebranding e o Instagram ainda ta com a logo antiga e bio de 2021, a marca quebra. Essa skill sincroniza todos os canais ao mesmo tempo.

## Input

- `./rebrand/01-discovery.md` — canais ativos + handles + canais a ativar
- `./rebrand/.selected-name.json` — nome + taglines
- `./rebrand/06-direction.md` + tokens da direcao escolhida
- `./rebrand/logo/final/` — assets do logo

## Procedure

### 1. Lista canais em escopo

Do discovery, combina:
- Canais ativos (refresh)
- Canais a ativar (bootstrap)

Pra cada canal, gere um diretorio `./rebrand/social/<canal>/`.

### 2. Dimensoes oficiais (refs)

```yaml
instagram:
  avatar: 320x320              # display 110x110
  cover_story_highlight: 1080x1920
  post_square: 1080x1080
  post_portrait: 1080x1350
  reel_cover: 1080x1920
  bio_char_limit: 150

facebook:
  avatar: 170x170
  cover: 820x312 (desktop) / 640x360 (mobile-safe)
  bio_char_limit: 101         # "About"

linkedin:
  avatar_company: 300x300
  cover_company: 1128x191
  tagline_char_limit: 120
  about_char_limit: 2000

x:
  avatar: 400x400
  cover: 1500x500
  bio_char_limit: 160

tiktok:
  avatar: 200x200
  bio_char_limit: 80

youtube:
  avatar: 800x800
  channel_banner: 2048x1152   # safe area 1546x423
  about_char_limit: 1000

whatsapp_business:
  avatar: 500x500
  description_char_limit: 256

google_business_profile:
  logo: 720x720
  cover: 1024x576
  description_char_limit: 750
```

### 3. Gera a bio pra cada canal

Bio otimizada segue a formula:

```
<hook> — <o que voce faz> em <quem voce serve>
<valor concreto / numero ou promessa>
<CTA + link>
```

Exemplo (IG, 150 chars):
```
Pagamentos sem codigo pra lojas Shopify
Cresca 2x sem contratar dev.
⬇ Testa gratis 14 dias
```

Regras:
- **Hook na primeira linha** (aparece antes do "...more"). Nunca comece com "Bem-vindo a...".
- **Valor concreto** na segunda linha — numero, prazo, ou promessa especifica.
- **CTA direto** com simbolo visual (⬇ ✨ 👇) pra apontar pro link.
- **1 link so** na bio do IG/TikTok — use um linktree-like se tiver varios destinos, ou direto pro ofer principal.

Pra LinkedIn (pode ser mais longo), use:
- **Tagline (120 chars)**: o one-liner da empresa
- **About (2000 chars)**: problem → solution → social proof → CTA

### 4. Gera os assets visuais

Pra cada canal, em paralelo:

**Avatar** — usa `avatar-1080.png` do logo-design, redimensiona pros tamanhos do canal. Se o canal tem circulo (IG), confirma que o logo tem safe area suficiente (senao, usa a versao quadrada com padding).

**Cover** — HTML + Playwright render. Template-base:

```html
<!DOCTYPE html>
<html>
<head>
<style>
  body { margin:0; width:1500px; height:500px;
         background: var(--brand-primary); color: var(--text-inverse);
         display:flex; align-items:center; justify-content:space-between;
         font-family: var(--heading-font); padding: 0 80px; }
  h1 { font-size: 64px; line-height:1.1; margin:0; max-width:70%; }
  .logo { height:96px; }
</style>
</head>
<body>
  <h1>{{TAGLINE_FUNCTIONAL}}</h1>
  <img class="logo" src="file://<path-to-logo-dark.svg>" />
</body>
</html>
```

Renderiza em resolucao nativa do canal via Playwright (`page.setViewportSize({width:1500,height:500})` + `page.screenshot({path:'...'})`).

Variantes:
- Cover base com tagline funcional
- Cover alternativa com tagline emocional
- Cover mobile-safe (FB/LinkedIn cortam em aspect ratios diferentes em mobile)

**Story highlight covers** (IG) — 6 icones (Sobre, Produto, Depoimentos, FAQ, Contato, Bastidores) em circulos coloridos com iconografia simples. Gera como SVG inline.

### 5. Gera 3 templates de post por canal

Pra cada canal visual (IG, TikTok, LinkedIn, FB), gera 3 templates editaveis:

1. **Template "Hook"** — post unico de texto grande com uma frase-gancho. Fundo brand, tipografia grande.
2. **Template "Carrossel"** — 5 slides: capa / problema / solucao / prova / CTA. Cada slide em HTML separado.
3. **Template "Reel cover / Story"** — formato vertical 9:16 com hook grande e logo no topo.

Cada template vai como HTML editavel em `./rebrand/social/<canal>/templates/<nome>/index.html` + render PNG de preview.

Os templates usam **tokens CSS vars** da direcao escolhida, entao qualquer ajuste futuro de cor propaga.

### 6. Output final

`./rebrand/18-social-presence.md`:

```markdown
# Presenca online — <nome>
_Generated <date> by the `social-presence` skill_

## Canais cobertos
- [x] Instagram (@nomix — refresh)
- [x] TikTok (@nomix — bootstrap)
- [x] LinkedIn Company (nomix-io — refresh)
- [x] WhatsApp Business (bootstrap)

## Por canal

### Instagram @nomix
**Bio nova** (150/150 chars):
> Pagamentos sem codigo pra lojas Shopify
> Cresca 2x sem contratar dev.
> ⬇ Testa gratis 14 dias

**Assets**: `./rebrand/social/instagram/`
- avatar.png (320x320)
- story-highlight-covers/ (6 icones)
- templates/hook/, templates/carousel/, templates/reel-cover/

**Checklist de deploy** (o usuario executa):
- [ ] Trocar avatar no app
- [ ] Atualizar bio (copiar/colar)
- [ ] Publicar story com novo logo + anuncio do rebrand
- [ ] Fixar 3 posts novos com templates

---

### [outros canais]
...
```

## Quality bar

- **Bio NUNCA passa do char limit** — se passar, pipeline falha e avisa o usuario.
- **Avatar em circulo tem que ler bem** — se o logo tem texto, confirme que nao e cortado.
- **Templates tem que ser editaveis** — HTML + CSS vars, nao PNG rasterizado. O usuario/agencia vai querer mudar headlines.
- **Bio em PT-BR se o negocio for BR**, EN se for internacional, as duas se atender ambos.
- **Sempre gere um checklist de deploy** — canais precisam ser atualizados manualmente pelo usuario (nenhuma API oficial permite login automatico em IG/TikTok em 2026).

## Handoff

Retorna path pra `18-social-presence.md` e um checklist consolidado de "o que voce precisa atualizar manualmente".
