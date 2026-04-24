---
name: brand-book-pdf
description: Compila tudo que foi gerado (logo, palette, tipografia, voz, do's e don'ts, exemplos) num brand book PDF imprimivel e um site brand guidelines interno estilo Figma/Storybook. E o entregavel "oficial" da rebranding — mandar pra time, freelancers, agencia, parceiros usarem como referencia. Use depois de logo-design, brand-direction, conversion-angle.
---

# Brand Book PDF

> **Source & credit**: Brand book structure destilada de [Brand.new](https://brandnew.underconsideration.com) case studies e brand guidelines publicas de [Stripe](https://stripe.com/brand), [Linear](https://linear.app/brand), [Figma](https://www.figma.com/brand/), [Spotify Design](https://spotify.design/). PDF generation via Playwright + HTML (nao LaTeX — HTML e mais editavel).

## Purpose

Quando a rebranding termina, voce vai ter 5 designers freelancers, 2 agencias, time interno, parceiros — todos precisando aplicar a marca consistentemente. Brand book resolve:

- **Uma fonte da verdade** — sem perguntar "qual o hex mesmo?" toda vez
- **Defende a marca** — se agencia fizer algo feio, o book e seu argumento
- **Tempo economizado** — onboarding de novo designer cai de horas pra 15 min

Entrega:
- **PDF imprimivel** (A4, ~30-60 paginas)
- **Site brand guidelines interno** (HTML estatico, copia-cola friendly, dark/light mode)
- **Figma library file** (JSON de tokens importavel)

## Input

- `./rebrand/01-discovery.md` — brand brief, positioning
- `./rebrand/06-direction.md` + `06-new-tokens.<slug>.json` — palette, tipo, spacing
- `./rebrand/07-logo.md` + `./rebrand/logo/final/` — logo exports
- `./rebrand/05-conversion-angle.md` — voz e tom
- `./rebrand/mockups/` — mockups in situ

## Procedure

### 1. Estrutura do brand book

Capitulos padrao:

```
01. Introducao                    "Por que essa marca existe" (propositos do discovery)
02. Promessa de marca             Big promise do conversion-angle
03. Posicionamento                Mapa 2x2, onde estamos, com quem competimos
04. Publico                       Personas com foto + quote + comportamento
05. Personalidade                 Adjetivos + spectrum (ex: "casual mas nao infantil")
06. Voz e tom                     Principios + exemplos do / don't
07. Logo                          Construcao, variantes, clear space, min size, usos proibidos
08. Cores                         Palette com hex/RGB/CMYK/Pantone, pairings, contrast ratios
09. Tipografia                    Heading / body / mono, scale, weights, line-height, pairings
10. Spacing & radius              Sistema de espacamento (4px base), border radius, shadows
11. Imagery                       Photo style, illustration style, icon system
12. Aplicacoes                    Business card, social covers, ad templates, email, site hero, merch
13. Do's & Don'ts                 Side-by-side com exemplos reais
14. Contato                       Quem aprovar uso da marca, como pedir nova variante
```

### 2. Template HTML (gera PDF + site)

Gera um HTML unico multi-pagina (page-break-inside: avoid) que serve como fonte pra ambos PDF e site interno. Usa tokens CSS vars ja definidos, entao o book se atualiza junto com a brand.

`./rebrand/brand-book/brand-book.html`:

```html
<!DOCTYPE html>
<html>
<head>
<style>
  :root {
    /* pulled from 06-new-tokens.<slug>.json */
    --brand-primary: #0A2540;
    --accent: #00D4FF;
    --surface: #FFFFFF;
    --text: #0A2540;
    --font-heading: "Söhne", Inter, system-ui;
    --font-body: Inter, system-ui;
  }
  @page { size: A4; margin: 20mm; }
  body { font-family: var(--font-body); color: var(--text); background: var(--surface); }
  h1, h2 { font-family: var(--font-heading); }
  .page { page-break-after: always; min-height: 257mm; }
  .swatch { display: inline-block; width: 120px; height: 120px; border-radius: 8px; }
  /* ... */
</style>
</head>
<body>
  <section class="page cover">
    <img src="../logo/final/logo-dark.svg" />
    <h1>Brand Guidelines</h1>
    <p>v1.0 · <date></p>
  </section>

  <section class="page">
    <h2>01. Por que existimos</h2>
    <p>{{BRAND_BRIEF}}</p>
  </section>

  <!-- cada capitulo como <section class="page"> -->
  <!-- ... -->
</body>
</html>
```

### 3. Capitulo "Logo" — exemplo detalhado

```markdown
## 07. Logo

### Variantes
[mostra lockup-horizontal.svg] Lockup horizontal (padrao pra header site + email)
[mostra lockup-vertical.svg]    Lockup vertical (pra avatars, badges)
[mostra favicon.svg]             Simbolo isolado (pra favicon, avatar quando ha pouco espaco)

### Cores permitidas
- Logo full color: sobre fundo surface ou surface_alt
- Logo dark: sobre brand_primary ou fotos escuras
- Logo mono preto: print 1-cor, fax, embossed
- Logo mono branco: sobre qualquer fundo escuro

### Clear space
O simbolo tem que ter no minimo **1x a altura do simbolo** de espaco em volta. Sem exceções.
[diagrama mostrando]

### Tamanho minimo
- Digital: 24px altura (lockup), 16px (simbolo)
- Print: 10mm altura (lockup), 6mm (simbolo)

### Uso proibido (don'ts)
[side-by-side de don't → do]
❌ Esticar / distorcer       ✅ Sempre manter proporcao
❌ Rotacionar                ✅ Sempre horizontal
❌ Trocar cores              ✅ So as variantes oficiais
❌ Adicionar sombra/outline  ✅ Flat, limpo
❌ Sobre fundo colorido nao-brand ✅ So sobre surface / brand_primary / foto com overlay
```

### 4. Capitulo "Cores" — grids com contrast

```markdown
## 08. Cores

### Palette primaria

[swatch big] brand_primary    #0A2540    RGB(10,37,64)    CMYK(100,80,40,50)    Pantone 539C
[swatch big] accent           #00D4FF    RGB(0,212,255)   ...

### Contrast ratios (WCAG AA)
- brand_primary sobre surface: 16.2:1 ✓ AAA
- accent sobre surface: 2.1:1 ✗ nao use pra texto, so pra elemento decorativo
- text_muted sobre surface: 5.1:1 ✓ AA
...

### Pairings (combinacoes aprovadas)
[swatch bg brand_primary] [swatch text surface]  Header escuro
[swatch bg surface_alt] [swatch text brand_primary] Cards
...

### Usos proibidos
❌ brand_primary sobre accent (contrast baixo)
❌ Palette inteira na mesma tela (pick 2-3)
❌ Novos matizes nao listados aqui
```

### 5. Capitulo "Voz e tom" — exemplos side-by-side

```markdown
## 06. Voz

### Nossa voz e
- Direta — menos palavras
- Humana — como amiga, nao corporativo
- Especifica — numeros, nao adjetivos
- Confiante — sem hedging ("acho que", "talvez")

### Nao e
- Jargao ("synergize", "sinergia")
- Bullshit de marca ("a melhor experiencia")
- Baby talk ("amei demais!!!")
- Agressiva ("voce e burro se nao comprar")

### Exemplos
| ❌ Don't | ✅ Do |
| --- | --- |
| "Nossa plataforma oferece uma solucao end-to-end" | "A gente faz tudo do check-in ao recibo" |
| "Ative o seu potencial" | "Venda 2x mais em 30 dias" |
| "Claro! Obrigado pelo seu contato!!!" | "Boa. Vou te mandar isso ate sexta" |

### Por canal
- **Site**: mais formal, focado em clareza
- **Email**: pessoal, primeira pessoa
- **Social**: descontraido, pode usar giria leve
- **Ads**: hook direto, agressivo em hook, nunca em claim
- **Atendimento**: empatico, proativo, nunca defensivo
```

### 6. Gera PDF

Via Playwright:

```js
// ./rebrand/brand-book/generate-pdf.js
const { chromium } = require('playwright')
const browser = await chromium.launch()
const page = await browser.newPage()
await page.goto('file://.../brand-book.html', { waitUntil: 'networkidle' })
await page.pdf({
  path: './brand-book.pdf',
  format: 'A4',
  printBackground: true,
  margin: { top: '20mm', bottom: '20mm', left: '20mm', right: '20mm' },
})
await browser.close()
```

### 7. Gera site interno

Mesmo HTML, mas com nav lateral e dark mode toggle:

`./rebrand/brand-book/site/index.html` — versao web responsiva com:
- Nav lateral fixo com anchors pra cada capitulo
- Dark mode toggle (swatches renderizam em ambos)
- Copy-click em cada hex: clicou, copia pra clipboard
- Copy-click em fonts pra importar via npm/@import

Pode ser deployed em `brand.<dominio>.com` (subdominio) ou `/brand` path do site.

### 8. Figma library export

Gera `./rebrand/brand-book/figma-library.json` compativel com Figma Tokens plugin / Design Tokens W3C spec:

```json
{
  "color": {
    "brand": {
      "primary": { "value": "#0A2540", "type": "color" },
      "accent":  { "value": "#00D4FF", "type": "color" }
    }
  },
  "typography": {
    "heading": { "fontFamily": "Söhne", "fontWeight": 700, "fontSize": "32px", "lineHeight": 1.1 },
    ...
  },
  "spacing": { "1": "4px", "2": "8px", ... }
}
```

Designer importa no Figma, estilos aparecem como vars.

### 9. Output umbrella

`./rebrand/22-brand-book.md`:

```markdown
# Brand Book — <marca> v1.0

## Entregas
- [PDF imprimivel](./brand-book/brand-book.pdf) — 42 paginas A4
- [Site interno](./brand-book/site/) — deploy em brand.<dominio>
- [Figma library](./brand-book/figma-library.json) — importar no plugin Figma Tokens
- [HTML fonte](./brand-book/brand-book.html) — editavel, fonte de verdade

## Distribuir pra
- Time interno (todo onboarding)
- Freelancers (mandar link do site antes de comecar)
- Agencia (anexar ao contrato)
- Parceiros que mencionam a marca
- Repositorio de midia (pra jornalista ou imprensa)

## Atualizar quando
- Mudar palette / tipografia / voz (versao 2.0+)
- Adicionar nova aplicacao (ex: agora temos app → add tela de splash)
- Descobrir abuso de marca (add no don't)

## Proximos passos
1. Review pessoal do PDF
2. Testar impressao (cores CMYK podem mudar um pouco)
3. Deploy do site brand.<dominio>.com
4. Importar Figma library
5. Mandar pra time
```

## Quality bar

- **PDF tem que ser bonito.** Se fica feio, ninguem consulta. Investe em cover, spacing, swatches bem renderizados.
- **Copy-click no site e obrigatorio.** Designers vao usar — nao os forcce a selecionar texto.
- **Versao + data em tudo.** Mudanca no futuro vai existir; sem versao, vira chaos.
- **Exemplos concretos.** "Voz humana" e vago. "Nao: 'Ative seu potencial'. Sim: 'Venda 2x mais em 30 dias'" e acionavel.
- **Don'ts sao tao importantes quanto do's.** Exemplo do don't previne abuso.

## Handoff

Retorna path pra `22-brand-book.md`, PDF gerado, link pro site preview local, Figma JSON.
