---
name: lead-magnet
description: Cria lead magnet completo (PDF/ebook/checklist/template/mini-curso) baseado no angle do conversion-angle — com copy da LP de opt-in, thank-you page, entrega por email, e sequence de nurture pos-download. Essencial pra marca que nao converte em venda direta — captura email primeiro, vende depois. Use depois de conversion-angle e email-sequences.
---

# Lead Magnet

> **Source & credit**: Lead magnet framework de [Digital Marketer's "The Ultimate Guide to Lead Magnets"](https://www.digitalmarketer.com) e [Brian Dean's Backlinko content upgrades](https://backlinko.com). PDF quality bar de [Ahrefs' free resources approach](https://ahrefs.com). Nurture sequence pattern de [Ryan Levesque's Ask method](https://askmethod.com).

## Purpose

Em B2B, high-ticket, infoproduto ou qualquer nicho com venda consultiva, 95% do visitante nao compra na primeira visita. Lead magnet captura email pra nutrir depois — transforma visita em lista, lista em cliente.

Essa skill entrega:
- 1 lead magnet completo (PDF, template, checklist, ou mini-curso)
- LP de opt-in (integra com landing-page skill)
- Thank-you page com entrega + proximo passo
- Email de entrega automatizado
- Nurture sequence de 5-7 emails (integra com email-sequences)

## Input

- `./rebrand/01-discovery.md` — publico, oferta
- `./rebrand/02-competitor-research.md` — lead magnets dos concorrentes (pra diferenciar)
- `./rebrand/05-conversion-angle.md` — big promise, dores, prova
- `./rebrand/06-direction.md` — tokens visuais

## Procedure

### 1. Escolhe formato

Baseado em publico + nicho:

| Formato | Quando usar | Esforco pra criar | CVR tipica |
| --- | --- | --- | --- |
| **Checklist 1 pagina** | Publico ocupado, problema rapido | Baixo (2-4h) | 15-25% |
| **Template / swipe file** | "Mostra exatamente como fazer" | Baixo-Medio (4-8h) | 20-35% |
| **Ebook PDF 10-30 pag** | Topico profundo, autoridade | Alto (1-2 dias) | 10-20% |
| **Planilha / calculator** | Dados, ROI, metricas | Medio (6-10h) | 25-40% |
| **Mini-curso email (5 dias)** | Topico complexo, educa ao longo | Medio-Alto | 15-30% |
| **Video masterclass gratuito** | Alto-ticket, venda via webinar | Alto | 10-25% pra webinar, 2-5% pra compra |

Skill recomenda formato baseado em discovery + ticket.

### 2. Define o topico

O topico vence quando:
- Resolve **1 problema especifico** (nao "marketing" — "como escrever email de boas-vindas que converte")
- **Promessa especifica com prazo** ("em 24h", "em 10 minutos", "sem codigo")
- **Gap relevante** pro que o produto principal resolve (e a ponte)
- **Consumivel em <30 min** (nao "ebook de 300 paginas")

Exemplos concretos por nicho:
- **SaaS checkout** → "Checklist de 12 pontos pra aumentar CVR do teu Shopify em 14 dias"
- **Infoproduto marketing** → "Swipe file: 50 headlines que ja geraram R$ 1M em vendas"
- **Consultoria B2B** → "Calculadora: quanto teu site ta te custando em vendas perdidas"
- **DTC beauty** → "Ebook: rotina de skincare simplificada por tipo de pele"
- **Fitness app** → "Plano de treino 14 dias pra iniciantes (PDF imprimivel)"

### 3. Cria o conteudo

Pra cada formato, estrutura especifica:

**Ebook (padrao):**

```
Cover (1 pag)
├── Titulo grande
├── Subtitulo com promessa
├── Foto do founder ou mockup
└── Logo + URL

Intro (1-2 pag)
├── Problema que voce vai resolver
├── Quem voce e / autoridade
└── O que a pessoa vai conseguir ao terminar

Conteudo (5-20 pag)
├── Capitulo 1: conceito base
├── Capitulo 2: passo 1
├── Capitulo 3: passo 2
├── ...
└── Cada capitulo com: teoria curta + exemplo concreto + acao imediata

Conclusao (1-2 pag)
├── Recap dos aprendizados
├── Erro comum a evitar
└── "Pra ir alem": CTA pro produto principal

Bonus (1-3 pag)
├── Cheatsheet / checklist resumo
├── Links pra recursos mencionados
└── Conexao pra produto

Footer (1 pag)
├── Quem e a marca
├── Contato
└── Copyright
```

Total: 10-30 paginas. Menos = melhor (consumivel).

**Design**: usa tokens do `brand-direction` — mesmo palette, tipografia. Nao e design genérico.

### 4. Gera PDF via Playwright

Similar ao `brand-book-pdf` — gera HTML, converte pra PDF:

`./rebrand/lead-magnet/pdf/source.html` → `./rebrand/lead-magnet/pdf/<titulo>.pdf`

Inclui:
- Links clicaveis no PDF (CTA pro site, redes)
- Paginacao pra print
- Cover em 300dpi
- Alt text em imagens (acessibilidade + SEO do PDF)

### 5. LP de opt-in

Gera estrutura especifica (mais simples que a LP de venda):

```
Hero
├── Headline: promessa + o que a pessoa recebe
├── Sub: pra quem e / tempo de consumo
├── Mockup do PDF aberto
├── Form: 2 campos max (nome + email)
└── CTA: "Baixar agora gratis"

Sobre
├── 3 bullets do que aprende
└── Prova: "Baixado por X.XXX pessoas"

Autoridade
├── Foto + bio curta do founder
└── 1-2 reviews do lead magnet se ja tem

FAQ mini
├── E gratis mesmo?
├── Vou receber spam?
└── Posso compartilhar?

Footer: minimo
```

Integra com `landing-page` skill — pode gerar como pagina separada ou embed.

### 6. Thank-you page

**Pagina mais subutilizada do funil.** Quem baixou ta engajado — aproveita.

```
Hero
├── "Obrigado! Teu <lead magnet> ta no teu email em 2 minutos"
└── Botao "Baixar agora" (tambem direto, nao espera email)

Proximo passo (o ouro)
├── "Enquanto voce aguarda, veja isso:"
└── Uma das 3 opcoes:
    ├── Video de 5-10 min explicando o produto (melhor pra high-ticket)
    ├── Oferta trip-wire (produto barato R$ 27-97) com urgencia 15 min
    └── Booking de call (se servico B2B)

Social proof
└── 2-3 reviews do produto principal

Footer
```

Thank-you page converte 3-10% em venda imediata se bem feito.

### 7. Email de entrega

```
From: <founder name> <email@dominio>
Reply-to: email real

Subject: [<nome>] seu <lead magnet> ta aqui

Oi <nome>,

Como prometido, aqui esta teu <lead magnet>:

[BOTAO: Baixar PDF]

Ou clica aqui: <link direto>

Umas coisas que quero deixar claro:

1. Le quando der, nao tem pressa
2. Se tiver duvida, responde esse email — ta aqui pra isso
3. Amanha eu te mando <conteudo extra gratuito> que complementa esse PDF

Abrago,
<founder>

P.S. Se achou util, compartilha com quem precisa: <link de share>
```

### 8. Nurture sequence pos-download

5-7 emails ao longo de 14 dias, integrados com `email-sequences`:

```
D+0  → Email 1: delivery (acima)
D+1  → Email 2: estudo de caso relacionado
D+3  → Email 3: objecao-busting comum
D+5  → Email 4: "comecou a aplicar? 3 erros a evitar"
D+7  → Email 5: convite pra produto (soft sell)
D+10 → Email 6: depoimento + urgencia
D+14 → Email 7: ultima oferta com desconto lancamento
```

Cada email com copy pronta.

### 9. Conversion optimization

**Split test setup** automatico:

Variavel A: formato do lead magnet
- Versao A: checklist 1-pagina
- Versao B: ebook 15-pag
(mesmo topico, formatos diferentes)

Variavel B: copy de headline
- Versao A: promessa numerica ("14 dias")
- Versao B: promessa de resultado ("dobre CVR")

Rodando em paralelo, valida qual converte mais visitante em lead.

### 10. Output umbrella

`./rebrand/22-lead-magnet.md`:

```markdown
# Lead Magnet — <marca>

## Formato escolhido
<Ebook / Checklist / Template / etc>

## Titulo
"<titulo final>"

## Promessa
<1 frase de resultado + prazo>

## Arquivos gerados
- PDF: [./lead-magnet/pdf/<nome>.pdf](./lead-magnet/pdf/<nome>.pdf)
- LP de opt-in: [./lead-magnet/opt-in/](./lead-magnet/opt-in/)
- Thank-you page: [./lead-magnet/thank-you/](./lead-magnet/thank-you/)
- 7 emails de nurture: [./lead-magnet/nurture/](./lead-magnet/nurture/)

## Funnel integration
- Pixel: dispara `Lead` no form submit + `ViewContent` na thank-you
- UTM discipline: `utm_content=leadmagnet-<slug>`
- CRM: novo contato → tag `lead_magnet_<slug>`

## KPIs alvo
- Visitor → opt-in: >20%
- Thank-you → purchase (trip-wire): >3%
- 14-day lead → sale conversion: >2-5%

## Proximos passos
1. Review do PDF — ajusta fotos, ajusta placeholders
2. Deploy LP de opt-in + thank-you
3. Agenda emails de nurture no provider
4. Adiciona popup de exit-intent no site principal oferecendo o lead magnet
5. Test: baixa tu mesmo pra validar fluxo completo
6. Ativa ads (Meta/Google) apontando pra LP de opt-in
```

## Quality bar

- **Consumivel em <30 min.** Se demora mais, pessoa nao consome, e nao nutre.
- **Nao prometa o que produto paga entrega.** Lead magnet abre o apetite, nao substitui a refeicao.
- **Design bate com a marca.** PDF feio = percepcao de produto pago ruim.
- **Link interno pro produto em 2-3 pontos**, nao so no final.
- **Entrega em 2 minutos.** Email delay > 2 min mata conversao pra trip-wire.
- **Nao peca telefone/empresa no form.** 2 campos max (nome + email) — cada campo extra corta 10% de CVR.

## Handoff

Retorna path pra `22-lead-magnet.md`, PDF gerado, LP preview, lista de emails de nurture, e KPIs alvo.
