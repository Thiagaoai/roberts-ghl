---
name: logo-design
description: Gera 3 conceitos de logo pra marca escolhida (wordmark + simbolo + lockup), cada um em variantes claro/escuro/monocromo, e exporta em SVG/PNG/favicon/social avatar. Usa o nome escolhido (do naming skill) e a direcao visual aprovada (do brand-direction). Checkpoint skill — usuario escolhe 1 conceito antes de seguir. Use quando o discovery ou naming indicar que logo novo e necessario.
---

# Logo Design

> **Source & credit**: Padroes de logo construction (wordmark / mark / combined / emblem / abstract) do [Brand.new](https://brandnew.underconsideration.com) e pattern de export pipeline adaptado de [anthropics/skills/brand-guidelines](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines). SVG generation via code (nao imagem IA) pra manter vetorial e editavel.

## Purpose

Entregar logo que funciona:
- Em 16x16px (favicon) e em outdoor
- Em preto puro, branco puro, e cor
- Em avatar redondo (Instagram) e em lockup horizontal (header de site)
- Exportavel e editavel — SVG, nao PNG rasterizado

## Input

- `./rebrand/.selected-name.json` (do naming skill) — nome + tagline
- `./rebrand/03-new-tokens.<slug>.json` (do brand-direction) — palette + tipografia
- `./rebrand/01-discovery.md` — nao-negociaveis sobre logo (manter simbolo antigo?)

## Skip condition

Se discovery disser `Logo = manter atual`, nao rode. Se disser `Logo = variantes do atual`, pule direto pra fase 3 (variantes + exports) usando o logo existente.

## Procedure

### 1. Escolha o tipo de construcao

3 arquetipos classicos — proponha 1 de cada se possivel:

| Tipo | Exemplo | Quando funciona |
| --- | --- | --- |
| **Wordmark** | Google, Coca-Cola, Ebay | Nome curto, quer reforcar o nome, simbolo so atrapalharia |
| **Lettermark (monogram)** | HBO, NASA, IBM | Nome longo, acronimo natural, ticket alto / autoridade |
| **Combined (mark + wordmark)** | Nike+swoosh, Adidas+trifolio | Flexibilidade: usa o mark no favicon, o combined no header |
| **Emblema** | Starbucks, Harley | Heritage, artesanato, contar historia |
| **Abstrato / geometrico** | Chase, Pepsi | Tech / fintech / escala global |

Pegue o discovery: se `familia estetica = Corporate Trust` → Combined ou Lettermark. Se `= Bold Playful` → Wordmark com personalidade ou Emblema. Se `= Tech Futurist` → Abstrato ou Combined.

### 2. Gera 3 conceitos

Cada conceito vira um diretorio:

```
./rebrand/logo/concept-1-<nome>/
  logo.svg                 # versao primaria, cor, em canvas 400x400 ou 800x200 horizontal
  logo-dark.svg            # pra fundo escuro
  logo-mono-black.svg      # uma cor, preto
  logo-mono-white.svg      # uma cor, branco
  favicon.svg              # simbolo sozinho, 32x32 quadrado
  avatar.svg               # simbolo em circulo com safe area, pra IG/X/etc
  lockup-horizontal.svg    # mark + wordmark lado a lado
  lockup-vertical.svg      # mark em cima, wordmark embaixo
  construction.md          # porque esse design, qual familia, qual metafora
```

**Implementacao tecnica**: voce gera SVG como codigo (escrever o XML direto via `Write`), nao usa gerador de imagem. Isso garante:
- Vetorial de verdade
- Editavel (cores trocam via `currentColor` ou `fill`)
- Pequeno em bytes
- Reproduzivel

Pra wordmark: usa a fonte da direcao escolhida (ex: Inter Bold) via `<text>` SVG com `font-family`. Pra simbolo: composicao geometrica simples (circulos, paths). Nao tenta gerar arte complexa como SVG — gera simbolo conceitual limpo (1-3 formas primitivas).

Exemplo de `logo.svg` minimo (wordmark com simbolo geometrico):

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 120" role="img" aria-label="Nomix">
  <g fill="#0A2540">
    <circle cx="60" cy="60" r="40"/>
    <circle cx="60" cy="60" r="20" fill="#00D4FF"/>
  </g>
  <text x="130" y="78" font-family="Inter, system-ui" font-weight="700"
        font-size="56" fill="#0A2540" letter-spacing="-1">Nomix</text>
</svg>
```

### 3. Gera o construction.md de cada conceito

```markdown
# Concept 1 — "Ponto de encontro"
- **Tipo**: Combined mark
- **Metafora**: circulo concentrico = o usuario (fora) e o produto (centro) convergindo
- **Tipografia**: Inter Bold, tracking -1%, proporcao 3:1 entre altura do simbolo e cap-height
- **Cor primaria**: `#0A2540` (brand_primary da direcao aprovada)
- **Cor acento**: `#00D4FF` (accent)
- **Safe area**: o raio do simbolo (40px) ao redor do lockup
- **Tamanho minimo**: 24px de altura pro combined, 16px pro simbolo sozinho
- **Construcao geometrica**: 2 circulos concentricos, ratio 2:1. O texto alinhado verticalmente pelo centro do simbolo.
```

### 4. Mockups do logo in situ

Gera PNGs (via Playwright renderizando HTML que usa o SVG) mostrando o logo:

- No header de um site mockup (`./rebrand/logo/concept-N/in-situ-site.png`)
- Como avatar de Instagram (`./rebrand/logo/concept-N/in-situ-instagram.png`)
- Em um anuncio 1080x1080 (`./rebrand/logo/concept-N/in-situ-ad.png`)
- Impresso em cartao de visita (`./rebrand/logo/concept-N/in-situ-card.png`)

Isso e o que vende o conceito — designer experiente sabe que logo fora de contexto nunca convence.

### 5. Checkpoint — usuario escolhe

Chama `AskUserQuestion`:

- Pergunta: "Qual conceito de logo seguimos?"
- Options: Concept 1, 2, 3, "Remix — pegar elementos de 2 e 3", "Nenhum — regerar"
- Cada option tem preview da in-situ-site.png como imagem

Se escolher um:
- Grava o slug em `./rebrand/.selected-logo`
- Copia os SVGs finais pra `./rebrand/logo/final/` (sem o prefixo `concept-N/`)
- Gera exports PNG em resolucoes-chave:
  - `logo-512.png`, `logo-256.png`, `logo-128.png`
  - `favicon-32.png`, `favicon-16.png`, `favicon.ico` (via ImageMagick se disponivel)
  - `avatar-1080.png` (pra IG / LinkedIn)
  - `og-1200x630.png` (pra OG image do site e link preview)

### 6. Output final

`./rebrand/07-logo.md`:

```markdown
# Logo final — <nome>
_Generated <date> by the `logo-design` skill_

## Escolhido
**Concept 2 — "Ponto de encontro"** (combined mark)

## Assets entregues em `./rebrand/logo/final/`
- `logo.svg` — primario
- `logo-dark.svg`, `logo-mono-black.svg`, `logo-mono-white.svg`
- `favicon.svg`, `favicon-32.png`, `favicon-16.png`, `favicon.ico`
- `avatar-1080.png` — pra redes sociais
- `og-1200x630.png` — pra link preview
- `lockup-horizontal.svg`, `lockup-vertical.svg`
- `construction.md` — docs do sistema

## Regras de uso
- Safe area: 1x a altura do simbolo em todos os lados
- Tamanho minimo: 24px altura (combined) / 16px (simbolo)
- Nunca estique, rotacione, ou mude as cores do logo
- Sobre fundo escuro: use `logo-dark.svg`
- Sobre foto: use `logo-mono-white.svg` com overlay escuro

## Proximo passo
Esses assets alimentam:
- `apply-rebrand` (favicon + header do site + og-image)
- `social-presence` (avatar + covers de redes sociais)
- `ad-creatives` (logo watermark nos criativos)
```

## Quality bar

- **Teste de 16px**: se o favicon fica ilegivel, o conceito falhou.
- **Teste monocromo**: se perde identidade em preto e branco, o design ta apoiado demais na cor.
- **Simbolo antes de nome**: se mostrar so o simbolo (sem wordmark) pro usuario, ele tem que pelo menos sentir "isso parece essa marca". Nao precisa saber o nome — precisa sentir o espirito.
- **Nao copie logos existentes.** Se um concorrente direto usa circulos concentricos, use outra geometria.
- **SVG tem que ser semantico**: `role="img"`, `aria-label`, sem texto rasterizado como path.

## Handoff

Retorna path pra `07-logo.md`, caminho do diretorio `final/`, e flag indicando se favicon.ico foi gerado (requer ImageMagick) ou se precisa que o usuario faca a conversao.
