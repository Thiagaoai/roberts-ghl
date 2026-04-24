---
name: launch-plan
description: Monta plano de lancamento (ou re-lancamento pos-rebranding) com timeline de 14-30 dias — pre-lancamento (teaser + lista de espera), dia 0 (anuncio multi-canal), pos-lancamento (sustain). Inclui copy por canal, sequencia de emails de lancamento, assets de social, checklist dia-a-dia, e rollback plan se der ruim. Use depois de conversion-angle, email-sequences, content-calendar.
---

# Launch Plan

> **Source & credit**: Launch framework destilado de [Jeff Walker's Product Launch Formula](https://productlaunchformula.com) adaptado pra rebranding, [Jason Fried's Basecamp launches](https://basecamp.com) shape-up style, e pos-mortems publicos de lancamentos DTC (Allbirds, Away, Liquid Death). "Pre-launch list" pattern de [Ryan Hoover's Product Hunt playbook](https://www.ryanhoover.me).

## Purpose

Rebranding sem lancamento e cair na arvore na floresta — ninguem percebe. Essa skill entrega um plano estruturado pra:

- Construir antecipacao pre-lancamento (lista de espera, teaser)
- Coordenar anuncio multi-canal no dia 0
- Sustentar momentum nas primeiras 2 semanas
- Medir sucesso com KPIs especificos
- Ter plano B se alguma coisa derreter

## Input

- `./rebrand/01-discovery.md` — timeline desejada, budget, time
- `./rebrand/05-conversion-angle.md` — hooks, big promise
- `./rebrand/11-email-sequences.md` — lista atual de email
- `./rebrand/17-content-calendar.md` — pipeline de conteudo

## Procedure

### 1. Escolhe template de lancamento

**Pattern A: Soft launch (padrao)** — 14 dias
- Bom pra: rebranding, pivot, atualizacao de produto
- Risco: baixo
- Intensidade: media

**Pattern B: Big launch** — 30 dias
- Bom pra: produto novo, entrada em mercado novo, startup recem-saida-do-stealth
- Risco: alto (requer budget + assets + PR)
- Intensidade: alta

**Pattern C: Stealth to waitlist** — 60 dias
- Bom pra: produto B2B, early access model
- Risco: baixo mas lento
- Intensidade: baixa mas longa

Skill escolhe baseado em discovery (budget, timeline, tipo de oferta).

### 2. Pattern A — Soft launch 14 dias (default)

```
Dia -14 a -8  → TEASER PHASE (8 dias)
Dia -7 a -1   → COUNTDOWN PHASE (7 dias)
Dia 0         → LAUNCH DAY
Dia +1 a +7   → SUSTAIN PHASE
Dia +8 a +14  → OPTIMIZE PHASE
```

### 3. Teaser phase (dia -14 a -8)

Objetivo: build list de espera + curiosidade.

**Assets gerados**:
- Post de social "algo novo em X semanas" (sem revelar)
- Email pra lista atual: "Novidade a caminho — quer ser avisado primeiro?"
- LP de waitlist: email capture + "receba 10% no dia do lancamento"
- Story/reels teaser: closeup de logo novo, sem revelar ainda
- DM pros top 20 clientes com preview exclusive

**Copy exemplos**:
```
Post IG:
"Uma coisa muda aqui nos proximos 10 dias.
Nao vou spoilar, mas... se voce assinar a lista ali na bio,
garante 10% no dia. E nao, nao e mais um curso. 😄"
```

### 4. Countdown phase (dia -7 a -1)

Objetivo: intensificar — 1 post/email por dia, cada um revelando mais.

```
Dia -7 → "7 dias pra mudar algo aqui"
Dia -6 → Reveal do problema: "Por que decidimos mudar"
Dia -5 → Reveal do beneficio 1: "O que voces vao ganhar"
Dia -4 → Social proof teaser: "Quem ja testou diz..."
Dia -3 → Reveal do produto (ainda sem comprar): "Ta quase"
Dia -2 → Preview de preco/oferta
Dia -1 → "Amanha 9h" — lembrete final pra waitlist
```

Cada dia tem post IG + story + email + tweet + post LinkedIn coordenados.

### 5. Dia 0 — Launch day

Timeline do dia:

```
07h00  → Email blast pra lista completa
08h00  → Post principal IG/LinkedIn com reveal
08h30  → Thread Twitter/X contando historia
09h00  → Abertura oficial (LP vai ao ar, checkout funciona)
09h15  → DM pros top 20 com link exclusivo + 15% off extra
10h00  → Stories mostrando primeiros compradores
12h00  → Reel com reacao / depoimentos
14h00  → Post LinkedIn B2B
17h00  → Email 2 "Como ta indo" pra lista (social proof real das primeiras horas)
18h00  → Reel IG "Respondendo a primeira pergunta que chegou"
20h00  → Stories final do dia — sneak peek do dia 1 / planos
```

**Checklist tecnico do dia 0**:
- [ ] LP ao vivo e testada em mobile + desktop
- [ ] Checkout funcional (compra teste ontem)
- [ ] Pixel/analytics disparando
- [ ] WhatsApp + atendimento on de 8h a 22h
- [ ] Time avisado do que fazer se site cair
- [ ] Email provider configurado pra volume (Mailchimp/AC avisado se >10k envios)
- [ ] Dominio aguentando trafego (vercel/CF scaling)

### 6. Sustain phase (dia +1 a +7)

Nao some depois do dia 0 — maioria vende MAIS na semana seguinte.

- Dia +1: "Dia 1 — obrigado" + primeiras entregas
- Dia +2: Responde duvidas comuns publicamente
- Dia +3: Caso real de cliente que comprou ontem
- Dia +4: Live (IG ou LinkedIn) respondendo perguntas
- Dia +5: "Ultimas 72h do bonus de lancamento"
- Dia +6: Sense of urgency (bonus acaba amanha)
- Dia +7: "Ultimo dia — fechamos hoje 23h59"

### 7. Optimize phase (dia +8 a +14)

- Remove urgencia (oferta normal agora)
- Inicia social proof compilado (stories com "o que a galera falou")
- Retargeting ads pro pessoal que visitou mas nao comprou
- Case study longo de 1-2 clientes
- Ajusta LP baseado no CVR real (se <2%, troca headline)

### 8. KPIs obrigatorios

Dashboard no Looker Studio (ja criado em analytics-setup) com:

- Waitlist signups (pre-launch meta: >500)
- LP visits dia 0 (meta: >2000)
- Dia 0 conversoes (meta: >5% da waitlist ativa)
- Dia 0 receita
- ROAS cumulativo (15 dias)
- NPS das primeiras 100 compras
- Taxa de reembolso dia 30 (alerta se >10%)

### 9. Copy por canal

`./rebrand/launch-plan/copy/`:
```
copy/
  email-teaser-1.md
  email-teaser-2.md
  ...
  email-launch-morning.md
  email-launch-afternoon.md
  ...
  ig-post-day-minus-7.md
  ig-post-day-0.md
  ...
  twitter-thread-day-0.md
  linkedin-post-day-0.md
  whatsapp-blast-day-0.md
```

Cada um com copy final + hashtags + CTA + melhor horario (do content-calendar).

### 10. Rollback plan

Se algo explode:

**Site cai no dia 0**:
- Rota de contingencia: LP estatica em Vercel/CF Pages
- Comunicacao: story "Estamos recebendo mais trafego que esperado — volte em 30min" + email pedindo desculpas
- Nao oferecer desconto extra imediatamente (vira expectativa futura)

**Checkout quebrado**:
- Link alternativo pra compra manual via WhatsApp
- Recuperacao: email pra todos que chegaram no checkout avisando do bug + cupom 10%

**Reaction negativa (ex: novo preco nao cai bem)**:
- Nao defenda na primeira hora. Escuta 24h primeiro.
- Depois post longo explicando razoes, com humildade
- Se for realmente ruim: concede (ex: "ok, mantemos grandfather por mais 60d")

**Produto falha pra cliente**:
- Pede desculpa publica em 1h
- Reembolso rapido + bonus de retencao
- Estudo de caso pos-crise: "o que aprendemos"

### 11. Output umbrella

`./rebrand/18-launch-plan.md`:

```markdown
# Launch Plan — <marca> — Soft launch 14 dias

## Data D=0
<inferido do discovery ou a definir>

## Fase atual
Teaser / Countdown / Launch / Sustain / Optimize

## Assets gerados
- 14 emails de sequencia de lancamento
- 40+ posts de social (todos canais)
- 7 templates de stories
- LP de waitlist
- Dashboard de KPIs

## Checklist pre-launch
- [ ] Waitlist criada
- [ ] Email sequence agendada no provider
- [ ] Posts scheduled no tool de social
- [ ] Checkout testado
- [ ] Time avisado
- [ ] Rollback plan documentado
- [ ] Legal compliance revisado (claims do launch dentro da Politica)

## Proximos passos
1. Define data exata do D=0
2. Revisa toda a copy (personaliza placeholders)
3. Agenda os 14 emails + 40 posts no scheduler
4. Loop de validacao: peca pra 3 pessoas fora do projeto darem review
5. Dia -14: comeca teaser

## Pos-launch (dia +14)
- Review completo: o que funcionou, o que nao
- Guarda como `launch-retro.md` pra proxima vez
- Ajusta content-calendar permanente baseado nos hooks que mais performaram
```

## Quality bar

- **Data especifica.** Sem data, nao ha launch. "Em breve" e morte.
- **Cada dia 1 asset agendado.** Nao vale "posto quando der". Scheduler (Metricool/Buffer) obrigatorio.
- **Rollback testado.** Site de contingencia tem que estar DEPLOYED antes, nao so "pronto pra deploy".
- **Top 20 clientes tem tratamento especial.** DM pessoal antes de qualquer blast. Ele vira first advocate.
- **Sustain phase importa mais que o dia 0.** Maioria do revenue vem nos dias 1-7, nao no dia 0.

## Handoff

Retorna path pra `18-launch-plan.md`, lista de assets, timeline completa, e data D=0 recomendada.
