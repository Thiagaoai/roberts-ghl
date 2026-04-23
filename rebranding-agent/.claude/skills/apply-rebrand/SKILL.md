---
name: apply-rebrand
description: Phase final. Detecta o stack do site (Next.js/React, static HTML, Astro, WordPress theme, outro), aplica os tokens da direcao escolhida no codigo, substitui as headlines pelas do conversion-angle, instala o favicon novo, troca a OG image, instala o Meta Pixel, re-screenshota o site pra before/after, e abre um PR. Checkpoint antes do PR. Use como ultima fase do pipeline de rebranding, apos todas as outras skills terem produzido seus artefatos.
---

# Apply Rebrand

> **Source & credit**: Stack detection heuristics baseadas nas convencoes de [package.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-json) dos frameworks. Token-editing patterns do [Tailwind design tokens](https://tailwindcss.com/docs/theme) e [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/--*). PR flow adaptado de [anthropics/skills/code-review](https://github.com/anthropics/skills).

## Purpose

Pegar todo output das skills anteriores e aplicar no codigo real, produzindo um PR revisavel com before/after. Nenhuma outra skill toca codigo-de-producao; essa e a unica.

## Input

- `./rebrand/01-discovery.md` — pra confirmar repo path e nao-negociaveis
- `./rebrand/03-direction.md` + `.selected-direction` + `03-new-tokens.<slug>.json` — tokens da direcao escolhida
- `./rebrand/04-logo.md` + `./rebrand/logo/final/` — favicon, og-image, avatar
- `./rebrand/06-conversion-angle.md` — headlines, CTAs, copy
- (Opcional) `./rebrand/02-audit.md` — corrige P0s de acessibilidade/SEO no processo

## Pre-conditions

- Usuario informou `repo_path` no discovery.
- Repo e um git repo limpo (ou com diff explicitamente salvo).
- `node` disponivel (pra rebuild / test).

## Procedure

### 1. Detecta o stack

Heuristicas (na ordem; para no primeiro match):

```python
# pseudo
if exists("package.json"):
    pkg = json.load("package.json")
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    if "next" in deps: stack = "nextjs"
    elif "astro" in deps: stack = "astro"
    elif "@remix-run/react" in deps: stack = "remix"
    elif "react" in deps: stack = "react-generic"
    elif "vue" in deps: stack = "vue"
    else: stack = "node-other"
elif exists("wp-config.php") or exists_glob("wp-content/themes/**/style.css"):
    stack = "wordpress"
elif exists("_config.yml") and exists("_layouts"):
    stack = "jekyll"
elif exists_glob("*.html") and not exists("package.json"):
    stack = "static-html"
else:
    stack = "unknown"

# Submodulo: detecta estilo
if exists("tailwind.config.*"): style = "tailwind"
elif grep_any(":root {", "*.css", "*.scss"): style = "css-vars"
elif exists_glob("**/*.module.css"): style = "css-modules"
elif grep_any("styled-components", "package.json"): style = "styled-components"
else: style = "plain-css"
```

Imprima a deteccao pro usuario logo de cara — se errou, e checkpoint informal: "Detectei `nextjs + tailwind`, confirma?"

### 2. Crea uma branch

```bash
cd <repo_path>
git checkout -b rebrand/<YYYY-MM-DD>-<name-slug>
```

### 3. Aplica os tokens (por stack)

**nextjs + tailwind** → edita `tailwind.config.{js,ts}`:

```js
// colors: mescla com o existente ou substitui inteiro dependendo dos nao-negociaveis
theme: {
  extend: {
    colors: {
      brand: { DEFAULT: '#0A2540', ... }, // de 03-new-tokens.json
      accent: { DEFAULT: '#00D4FF', ... },
      // ...
    },
    fontFamily: {
      heading: ['Söhne', 'Inter', 'sans-serif'],
      body: ['Inter', 'system-ui'],
    },
    borderRadius: { sm: '4px', md: '8px', lg: '16px' },
    boxShadow: { sm: '...', md: '...', lg: '...' },
  }
}
```

E substitui classes Tailwind no codigo via `Grep + Edit`:
- `bg-blue-500` (se era a brand antiga) → `bg-brand`
- `text-gray-900` → `text-ink`
- etc.

Dir class cleanup: se a direcao tem `radius.lg = 16px`, converte `rounded-md` → `rounded-lg` conforme a nova escala.

**css-vars** → edita `:root` no stylesheet principal:

```css
:root {
  --brand-primary: #0A2540;
  --accent: #00D4FF;
  --surface: #FFFFFF;
  --text: #0A2540;
  --font-heading: "Söhne", Inter, system-ui;
  --font-body: Inter, system-ui;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
}
```

Substitui qualquer hex hardcoded restante com um `Grep` por `#[0-9a-fA-F]{6}` e aplica `Edit` por arquivo.

**static-html** → stylesheet principal + favicon link no `<head>` de cada `*.html`.

**wordpress** → edita `style.css` do tema ativo (detectado via `wp-config.php` + `theme_name`), adiciona CSS custom no Customizer via `functions.php` hook. Copy edits vao no tema OU via wp-cli se disponivel. Se nao tiver wp-cli: gera um arquivo `rebrand-wp-changes.md` listando o que o usuario precisa colar no Customizer manualmente.

**unknown** → fallback: roda `Grep` pra todos os hexes, fontes, e classes de cor no repo; produz um `replacements.diff` com as trocas sugeridas mas NAO aplica automatico. Usuario revisa e aplica.

### 4. Instala logo + favicon + OG

- Copia `./rebrand/logo/final/favicon.ico`, `favicon-16.png`, `favicon-32.png` pra `/public` (nextjs/astro) ou `/` (static).
- Copia `logo.svg` + `logo-dark.svg` pra `/public/logo/` e atualiza imports em `Header`/`Footer` via `Grep + Edit`.
- Copia `og-1200x630.png` pra `/public/og-image.png` e atualiza `<meta property="og:image">` em todas as paginas.
- Atualiza `<title>`, `<meta name="description">`, `og:title`, `og:description` com strings do conversion-angle + direction.

### 5. Troca as headlines

Do `06-conversion-angle.md`:
- H1 home → substitui no componente `Hero`/`Home` (detecta via `Grep` pelo texto antigo, confirma com usuario se houver multipla ocorrencia).
- Sub-H1, CTA primario/secundario → substitui idem.
- Headlines de `/pricing`, `/about` → se existir.

**Importante**: antes de cada substituicao, mostra um diff preview pro usuario via texto no chat. Se a troca for ambigua (texto antigo aparece em 3+ lugares), pergunta onde aplicar.

### 6. Corrige os P0s do audit

Da secao "P0 — Blockers" do `02-audit.md`:

- **Contraste WCAG** — se um par de cores falhou, os novos tokens ja consertam.
- **Heading hierarchy** — troca `<h3>` mal-usado pra `<h2>` etc.
- **Alt text** — pra imagens sem alt, gera alt descritivo automatico via vision analysis das imagens.
- **Meta tags faltando** — ja cobertas na step 4.
- **Mobile viewport** — adiciona `<meta name="viewport" content="width=device-width, initial-scale=1">` se faltar.

### 7. Instala Meta Pixel (se ads vai rodar)

Se `01-discovery.md` indica ads ativos ou planejados:

- Se `nextjs`: adiciona componente `<MetaPixel>` no `layout.tsx` do App Router ou `_app.tsx` do Pages Router, lendo o ID de `NEXT_PUBLIC_META_PIXEL_ID` em `.env.local.example`.
- Se `static-html`: adiciona snippet direto no `<head>` de cada template.
- Adiciona evento `PageView` automatico + comentario com snippet pros eventos custom (AddToCart, InitiateCheckout, Purchase).

### 8. Re-screenshot & before/after

Invoca `site-audit` de novo, agora apontando pra `http://localhost:<dev-port>` (depois de `npm run dev` ou equivalente) ou pra build local:

- Gera `./rebrand/08-after-screenshots/` espelhando a estrutura do `screenshots/` da Fase 2.
- Monta `./rebrand/08-before-after.md` lado a lado:

```markdown
# Before / After

## / (home) — desktop
| Before | After |
| --- | --- |
| ![](screenshots/home-desktop.png) | ![](08-after-screenshots/home-desktop.png) |

## / (home) — mobile
...
```

### 9. Checkpoint — aprovacao antes do PR

Chama `AskUserQuestion`:

- Mostra:
  - Resumo do diff (`git diff --stat`)
  - Link pro `08-before-after.md`
  - Lista de arquivos mudados
- Opcoes: "Abrir PR", "Deixa eu revisar e ajustar antes", "Reverter tudo"

### 10. Commit + PR

Se aprovado:

```bash
git add -A
git commit -m "$(cat <<'EOF'
Rebrand: aplica nova identidade — <name>

- Novos tokens: palette, tipografia, spacing, radius, shadow
- Logo + favicon + OG image atualizados
- Headlines trocadas pelo novo angle de conversao
- Fixes dos P0s do audit: contraste WCAG, heading hierarchy, alt text
- Meta Pixel instalado (se aplicavel)
EOF
)"
git push -u origin rebrand/<YYYY-MM-DD>-<name-slug>
```

Pra abrir o PR: detecta se repo tem `origin` no GitHub. Se sim e o ambiente tiver `gh` CLI, cria o PR:

```bash
gh pr create --title "Rebrand: <name>" --body-file ./rebrand/08-before-after.md
```

Se nao tem `gh` CLI (este agente nao tem por padrao no web mode) ou o repo esta em outro host: imprime o link pra criar o PR manualmente + o body sugerido.

### 11. Output final

`./rebrand/09-apply-report.md`:

```markdown
# Apply report — <name>
_Generated <date> by the `apply-rebrand` skill_

## Stack detectado
- Framework: <nextjs>
- Styling: <tailwind>
- Confidence: alta

## Arquivos modificados (<N>)
<lista>

## Tokens aplicados
- Cores: X -> Y
- Fontes: old -> new
- ...

## Copy substituida
- H1 home: "..." -> "..."
- ...

## Fixes de acessibilidade
- <count> alt texts gerados
- <count> fixes de contraste
- ...

## Meta Pixel
- [x] Instalado em layout.tsx
- [x] Env var NEXT_PUBLIC_META_PIXEL_ID adicionada em .env.example
- [ ] Usuario precisa adicionar o ID real em producao

## PR
https://github.com/<owner>/<repo>/pull/<N>
```

## Quality bar

- **Nunca toque codigo sem diff preview no chat.** Mesmo com aprovacao geral, cada edit importante mostra antes/depois curto.
- **Respeita os nao-negociaveis do discovery.** Se "navy deve permanecer primary" esta la, verifica que a brand_primary e navy. Se nao for, aborta e pede confirmacao.
- **Builds quebrados = rollback.** Apos aplicar, roda `npm run build` (ou equivalente). Se falhar, reverte o commit e reporta o erro.
- **Acessibilidade nao regride.** Se um fix cria novo problema (ex: novo contraste falha), seta flag no apply-report.
- **PR description e extensa.** Usuario vai revisar — da contexto de tudo.

## Handoff

Esta e a ultima fase. Retorna:
- Link do PR (ou instrucoes pra abrir manual)
- Path pra `09-apply-report.md`
- Status de build (pass/fail)
- Um checklist final pro usuario executar (deploy, atualizar DNS pro novo dominio, trocar avatares nas redes, subir os ads).
