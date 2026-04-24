---
name: content-calendar
description: Gera calendario de conteudo de 30 dias pra cada canal social ativo — com tema, hook, formato (reel/carrossel/foto/story), copy pronto, hashtags, melhor horario, e CTA. Usa os templates de social-presence + angles do conversion-angle. Exporta em CSV/Notion/Airtable. Use depois de social-presence e conversion-angle.
---

# Content Calendar

> **Source & credit**: Content pillar framework de [Justin Welsh's LinkedIn playbook](https://www.justinwelsh.me) — 30 posts em 30 dias com 3-4 pillars. Posting time benchmarks de [Sprout Social 2025 report](https://sproutsocial.com/insights/best-times-to-post-on-social-media/) e [Later 2025 analysis](https://later.com). Hashtag strategy de [Kicksta research 2025](https://kicksta.co).

## Purpose

Apos rebranding, o time de social (ou o founder sozinho) precisa postar. Sem calendario, vira "o que eu posto hoje?" toda manha — e nada consistente acontece. Essa skill entrega **30 dias de conteudo mapeado** pra cada canal, com tudo pronto pra executar ou delegar.

## Input

- `./rebrand/01-discovery.md` — canais ativos, horarios, quem cuida
- `./rebrand/05-conversion-angle.md` — angles, offer stack, prova social
- `./rebrand/06-direction.md` — voz e tom
- `./rebrand/08-social-presence.md` — templates ja criados

## Procedure

### 1. Define content pillars (3-4 por marca)

Pillars sao categorias tematicas que refletem positioning. Pega do discovery:

- **Pilar 1: Educacional** — ensina o nicho (ex: "Como calcular CAC", "5 erros no checkout")
- **Pilar 2: Bastidores** — humaniza (ex: "Um dia no time", "Reunião com cliente")
- **Pilar 3: Social proof** — cliente, caso, depoimento
- **Pilar 4: Oferta/CTA** — venda direta (max 20% dos posts)

Proporcao sugerida: 40% educacional, 20% bastidores, 20% social proof, 20% oferta. Ajusta por canal (LinkedIn mais educacional, TikTok mais trend + bastidores, Instagram misto).

### 2. Formato por canal

| Canal | Formato dominante 2026 | Frequencia recomendada |
| --- | --- | --- |
| Instagram | Reel 15-30s > Carrossel > Foto unica | 5-7x/semana |
| TikTok | Video vertical 15-60s | 1-2x/dia |
| LinkedIn | Post texto + carrossel PDF > Video curto | 3-5x/semana |
| Facebook | Foto + texto longo (mata bem no orgânico ainda) | 3x/semana |
| X | Thread > Post unico | 1-3x/dia |
| YouTube | Long-form 8-20min + Shorts | 1 long + 2-3 shorts/semana |

### 3. Gera 30 posts por canal ativo

Pra cada canal ativo no discovery, gera uma grid:

```csv
data,pilar,formato,hook,copy,hashtags,horario,cta,template_usado
2026-05-01,Educacional,Reel 30s,"3 erros que matam checkout","Hook: 3 erros...\n\nBody: ...\n\nCTA: salva pra depois",#ecommerce #shopify,18:30,salvar,templates/reel-cover/
2026-05-02,Social proof,Carrossel 5 slides,"Loja X cresceu 2x em 30d","Slide 1: ...\nSlide 2: ...",#casesucesso,12:00,ver mais,templates/carousel/
...
```

Total: 30 linhas por canal, com 4 pillars distribuidos.

### 4. Cada post com copy pronto

Nao so "tema", mas **texto final pronto pra copiar e colar**:

```markdown
## Post 1 — Instagram Reel — 01/05

**Pilar**: Educacional
**Formato**: Reel 30s
**Template usado**: `templates/reel-cover/index.html`
**Horario**: 18:30 BRT (quarta-feira)

### Hook (0-3s)
"3 erros que matam seu checkout Shopify"

### Script (on-screen text + audio)
| Tempo | Texto overlay | Narracao / audio |
| --- | --- | --- |
| 0-3s  | "3 ERROS" | "Para. Se voce tem Shopify, presta atencao" |
| 3-10s | "#1: Usar padrao" | "Erro 1: voce usa o checkout padrao..." |
| 10-18s| "#2: Sem recovery" | "Erro 2: nao roda recuperacao de carrinho..." |
| 18-26s| "#3: Sem A/B test" | "Erro 3: nao testa nada..." |
| 26-30s| "SALVA →" | "Salva esse pra nao esquecer" |

### Caption (texto do post)
3 erros que vao te custar R$ 5k esse mes. 🚨

Salva pra ler depois, e me diz qual desses voce ja comete.

Link na bio pra nossa auditoria gratis. ⬇

---

**Hashtags** (mix de grandes + nicho + brandeadas):
#shopifybrasil #ecommercebrasil #checkout #cvr #lojaonline #vendassuas #<marca>

**CTA primario**: "Salva" (aumenta reach algoritmo)
**CTA secundario**: Link na bio → LP
```

### 5. Melhores horarios por canal (BR, 2026 benchmarks)

```
Instagram: seg-qua-sex 11h-13h e 18h-20h
TikTok:    ter-qui-sab 19h-22h (1a posta 11h)
LinkedIn:  ter-qui 08h-10h e 17h-18h (corporate dia util)
Facebook:  qua-dom 13h-16h
X:         ter-qui 09h-11h e 18h-20h
YouTube:   dom 18h (long-form) / ter-sab 20h (shorts)
```

A skill permite override via discovery — se usuario sabe que audiencia dele e diferente, usa o que ele disse.

### 6. Hashtags por canal

Nao copia cegamente 30 hashtags genericas. Mix de:

- **Grandes (1M+ posts)**: 3-5 pra visibilidade ampla
- **Medias (100k-1M)**: 5-7 pra nicho
- **Pequenas (<100k)**: 3-5 pra audiencia hiper-especifica
- **Brandeadas**: 1-2 (`#<marca>`, `#<campanha>`)

Total: 15-20 por post no Instagram, 3-5 no LinkedIn, 1-2 no TikTok (algoritmo TikTok depende pouco de hashtag).

### 7. Grid master

`./rebrand/content-calendar/master-grid.csv`:

```csv
data,canal,pilar,formato,hook,template,status
2026-05-01,Instagram,Educacional,Reel,"3 erros checkout",reel-cover/,pronto
2026-05-01,LinkedIn,Social proof,Post + carrossel PDF,"Como a Loja X cresceu 2x",linkedin-carousel/,pronto
2026-05-02,TikTok,Educacional,Video 15s,"POV: voce descobre que checkout padrao perde 30% vendas",tiktok-hook/,pronto
...
```

### 8. Export pras ferramentas

Gera `./rebrand/content-calendar/_imports/`:

- `notion-database.csv` — importavel como Database no Notion
- `airtable.csv` — mesma estrutura pra Airtable
- `trello.json` — cards por dia pra board kanban
- `ics/calendar.ics` — calendario importavel em Google Calendar / Outlook com reminders 1h antes de cada post

### 9. Rotina sugerida

```markdown
## Rotina de execucao (2-3h/semana)

### Domingo a tarde (2h) — producao
- Grava 7 videos (1 pra cada post da semana)
- Desenha os carrosseis no Figma usando templates
- Revisa caption de cada post

### Dia util (15 min por dia)
- Abre o calendario (ou scheduler tipo Metricool, Later, Buffer)
- Confere: post vai sair hoje?
- Responde comentarios dos ultimos 3 posts

### Sexta (30 min) — analise
- Olha metrica dos 7 posts da semana
- Quais hooks performaram melhor?
- Ajusta os pillars da proxima semana baseado em dados
```

### 10. Output umbrella

`./rebrand/17-content-calendar.md`:

```markdown
# Content Calendar — <marca> — 30 dias

## Total gerado
- 150 posts em 30 dias (30 por canal × 5 canais ativos)
- 4 content pillars
- CSV + Notion + Trello + ICS exports
- Rotina semanal de 2-3h sugerida

## Ferramentas de scheduling recomendadas
- Metricool (BR-friendly, boa analytics)
- Later (IG + TikTok focused)
- Buffer (multi-canal, gratuito ate 3 canais)
- Instagram Creator Studio (nativo, gratis)

## Proximos passos
1. Importa CSV no teu tool preferido
2. Agenda domingo de gravacao (bloco de 2h)
3. Faz 7 posts do Pilar 1 no domingo — ja tem estoque pra semana
4. Semana 1: executa
5. Sexta semana 1: revisa metrica, ajusta semana 2
```

## Quality bar

- **Copy pronto, nao briefing.** Se a pessoa abrir o CSV e tiver "fazer post sobre X", falhou. Tem que ser colar-e-postar.
- **Hooks variados.** Nao 30 posts com "3 erros que voce comete" — vira repetitivo.
- **80/20 educar/vender.** Se 50% dos posts vendem, conta vira "loja" e perde engajamento.
- **Respeita canal.** LinkedIn com giria TikTok vai mal. TikTok com LinkedIn-speak tambem.
- **Horarios testados.** Primeira semana usa o benchmark; da semana 2 em diante, ajusta com os dados reais do usuario.

## Handoff

Retorna:
- Path pra `17-content-calendar.md`
- CSVs de import
- Total de posts por canal
- Link pro primeiro dia de producao (checklist "faz isso dia X")
