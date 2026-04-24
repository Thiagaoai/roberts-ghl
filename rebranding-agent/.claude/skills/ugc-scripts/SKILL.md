---
name: ugc-scripts
description: Gera scripts de video UGC-style (15s, 30s, 60s) prontos pra gravar ou passar pra um creator — com hook nos primeiros 3s, shot list detalhada, B-roll, texto overlay, CTA, e variantes. Usa o conversion-angle + competitor-research como inputs. Essencial em 2026 porque ad estatico esta ficando barato (low CVR) — ads que ganham CPA baixo sao UGC video. Use depois de conversion-angle, em paralelo com ad-creatives.
---

# UGC Scripts

> **Source & credit**: Hook frameworks de [Alex Cattoni / Copy Posse](https://copyposse.com) e [Savannah Sanchez](https://twitter.com/social_savannah) UGC ad playbooks. Shot-list pattern adaptado de briefings de agencias UGC (Insense, Billo, Trend). Formato 3-act-in-15s destilado de analise de 500+ winning Meta ads da Foreplay / Motion.

## Purpose

Em 2026, os ads que tem menor CPA em Meta sao **videos UGC verticais 9:16 de 15-30s que parecem organicos**. Imagem estatica esta sendo vencida por video em quase todo nicho DTC/infoproduto/SaaS B2C. Essa skill entrega:

- 6 scripts de video (2 por hook do conversion-angle)
- Shot list frame-a-frame
- Texto overlay exato por segundo
- Briefing editavel pra mandar pra creator (Insense/Billo/freelancer)
- Alternativa: instrucao pra o usuario gravar sozinho no celular

## Input

- `./rebrand/05-conversion-angle.md` — os 3 hooks + big promise + prova social
- `./rebrand/02-competitor-research.md` — hooks vencedores que ja rodam
- `./rebrand/01-discovery.md` — tom, publico, oferta

## Procedure

### 1. Escolhe formatos

Padrao por hook: **1 video 15s + 1 video 30s**. Se discovery indicar "high-ticket" ou "nicho complexo", adiciona 1 video 60s (testimonial longo ou VSL-lite).

Total padrao: **6 scripts** (3 hooks × 2 duracoes).

### 2. Estrutura 3-act em 15s

```
0-3s   → HOOK (pattern interrupt, frase, ou acao visual inesperada)
3-8s   → PROBLEMA + AGITACAO (dor especifica do publico)
8-12s  → SOLUCAO + PROVA (seu produto + 1 numero/depoimento)
12-15s → CTA (acao verbal + texto overlay + link)
```

Em 30s: mesma estrutura com dobro de tempo pra cada etapa, adiciona 1 B-roll extra do produto.

Em 60s: vira quase VSL curta — hook / problema (15s) / jornada pessoal (15s) / solucao + demo (15s) / prova + CTA (15s).

### 3. Tipos de UGC por arquetipo

| Arquetipo | Hook visual | Quando usar |
| --- | --- | --- |
| **Talking head** | Creator falando direto pra camera, casual | Default, funciona em quase tudo |
| **Before/after** | Split screen ou cut rapido | Produto com resultado visivel |
| **POV unboxing** | Camera baixa, maos aparecem | Fisico, packaging importa |
| **Problema dramatizado** | Mini-cena encenada | Nicho saude/beleza/casa |
| **Reaction** | Alguem reagindo ao produto | Social proof amplificada |
| **Tutorial** | "Como eu...", step-by-step | Educa e vende |
| **Trend-jack** | Formato de trend do TikTok + produto | Bom pra reach organico tambem |

### 4. Output por script

`./rebrand/ugc/script-<NN>-<duracao>s-<arquetipo>/`:

```
brief.md            # briefing de creator editavel
script.md           # script completo timed
shot-list.md        # shot by shot
overlay-text.srt    # legenda/overlay .srt pra editor
thumbnail-frame.png # frame 0 sugerido pra thumbnail
```

**brief.md** (o que voce manda pro creator):

```markdown
# UGC Brief — Script 01 — 15s — Talking Head

## Contrato
- **Duracao**: 15s exatos (maximo 16s — Meta corta em 15)
- **Formato**: 9:16 vertical, 1080x1920, 30fps
- **Audio**: microfone do celular OK, mas em ambiente silencioso
- **Iluminacao**: luz natural de janela de dia, ou ring light
- **Local**: nao usa cenario corporativo — casa, cafe, rua, carro = melhor
- **Vestuario**: casual, nada de logo de outras marcas

## Persona
Mulher/homem 28-42, <descricao do discovery>, tom <confiante + amiga>.

## Hook obrigatorio (0-3s)
Frase EXATA (nao improvise): "<hook 1 do conversion-angle>"
Acao visual: olha direto pra camera, serio, sem sorrir ainda.

## Desenvolvimento (3-12s)
Conte em suas palavras:
- Problema: <dor do discovery>
- O que testou antes que nao funcionou (brevemente)
- Encontrou <produto> e <resultado especifico com numero>

Pode improvisar, mas mantenha a ordem.

## CTA (12-15s)
Frase EXATA: "<CTA do conversion-angle>. Link na bio."
Acao: aponta pra baixo (pra bio) ou pro link (dependendo da plataforma).

## Evite
- Nao fale o nome completo do produto mais de 2x (parece script vendedor)
- Nao leia claramente do papel/teleprompter
- Nao use filtro de beleza
- Nao use musica copyrighted — deixa sem musica que a gente adiciona depois

## Entrega
- 1 take principal de 15s
- 3 takes alternativos do hook (mesmo texto, energias diferentes)
- 5 segundos extras de B-roll do produto em uso
```

**script.md** — o timing detalhado:

```markdown
# Script 01 — "Para de perder dinheiro" — 15s

| Tempo | Shot | Audio (dialogo) | Overlay text | B-roll |
| --- | --- | --- | --- | --- |
| 0-3s  | Close-up rosto | "Se voce tem loja Shopify e ainda nao usa isso..." | HOOK: "loja Shopify" | - |
| 3-6s  | Mesmo shot | "...voce ta perdendo uns R$ 8 mil por mes sem saber." | "R$ 8.000/mes" | Corta pra screenshot de analytics |
| 6-10s | Close-up mao no celular | "Eu achava que meu checkout tava bom. Instalei o <produto>..." | - | Screen recording do produto |
| 10-13s| Split screen antes/depois | "...e em 14 dias meu CVR dobrou." | "2x CVR em 14 dias" | Grafico animado |
| 13-15s| Rosto sorrindo | "Link na bio pra testar gratis." | "TESTE GRATIS 14D ⬇" | - |

## Audio notes
- 0-3s: velocidade normal, serio
- 3-6s: enfatiza "R$ 8 mil"
- 13-15s: mais rapido, tom confidente
```

**shot-list.md** — resumo pro creator ou pra voce mesmo:

```markdown
# Shot list

## Shot A (obrigatorio)
- Rosto close-up, janela do lado esquerdo (luz)
- 3 takes: 1 serio, 1 frustrado, 1 confidente
- Segurar celular pra parecer natural, nao precisa aparecer

## Shot B (obrigatorio)
- Mao no celular na tela do produto
- Filma de cima, shallow depth of field
- 10 segundos

## Shot C (opcional mas recomendado)
- Split screen antes/depois — pode ser edicao, nao precisa filmar 2x
```

### 5. SRT overlay file

Pra editor usar direto no CapCut/Premiere:

```srt
1
00:00:00,000 --> 00:00:03,000
HOOK: loja Shopify

2
00:00:03,000 --> 00:00:06,000
R$ 8.000/mes

3
00:00:10,000 --> 00:00:13,000
2x CVR em 14 dias

4
00:00:13,000 --> 00:00:15,000
TESTE GRATIS 14D ⬇
```

### 6. "Gravar sozinho" vs "Contratar creator"

Pra cada script, inclui 2 recomendacoes:

**Gravar sozinho (budget R$0)**:
- Celular recente (ultimos 3 anos)
- Tripé de R$50
- Luz de janela
- Tempo: 2-3 horas pra 6 scripts
- Pro: autenticidade maxima se o usuario e o founder

**Contratar creator (R$300-1500 por video)**:
- Insense, Billo, Trend (internacional)
- Creatori, Guil (BR)
- Freelancer via Workana/99freelas
- Tempo: 7-10 dias do briefing ate entrega
- Pro: qualidade + persona que bate melhor com o publico

## Integracao com ad-creatives

Depois dessa skill rodar, o `ad-creatives` pode regerar a matriz de teste **incluindo os UGC videos** em vez de so static+carrossel:

- Ad set 1 (Hook 1): UGC 15s + UGC 30s + static 1:1
- Ad set 2 (Hook 2): UGC 15s + UGC 30s + carrossel
- Ad set 3 (Hook 3): UGC 15s + UGC 30s + static 4:5

Isso geralmente traz CPA 30-50% menor que matriz so-static.

## Quality bar

- **Hook nos 3s primeiros nao e opcional.** Sem hook, o video morre no feed scroll-by.
- **Nao use texto empilhado.** Max 1 linha de overlay por vez, tamanho grande, legivel em scroll.
- **Autenticidade > producao.** Um video filmado no celular com hook certo bate produtora fancy com hook fraco.
- **Evite musica copyrighted.** Meta detecta e derruba o ad. Use so royalty-free.
- **Scripts PT-BR devem soar falados, nao escritos.** Le em voz alta. Se travou, reescreve.

## Handoff

Retorna:
- Path pra `./rebrand/ugc/`
- Numero de scripts gerados
- Lista de creators/plataformas recomendadas pro nicho
- Sinalizador pro `ad-creatives` regerar matriz com UGC
