---
name: pr-kit
description: Monta press kit profissional — release em PT-BR/EN, boilerplate, fact sheet, bio do fundador, fotos em alta, logos, mockups, e lista de 30+ veiculos/jornalistas relevantes por nicho pra pitch. Inclui templates de pitch email (frio e warm intro). Use depois de brand-book-pdf e launch-plan — PR amplifica launch mas nao substitui.
---

# PR Kit

> **Source & credit**: Press release structure de [Associated Press Stylebook 2025](https://www.apstylebook.com) + templates de [PR Newswire](https://www.prnewswire.com). Pitch email patterns de [Justin Jackson's Marketing for Developers](https://marketingfordevelopers.com) e [HARO](https://www.helpareporter.com) best practices. Brazilian outlets list compilada de [Abracom (Associacao Brasileira das Agencias de Comunicacao)](https://www.abracom.org.br).

## Purpose

PR feito bem amplifica launch sem custo de midia paga — e da credibilidade (social proof: "como visto em [veiculo]"). Mas PR sem kit organizado = jornalista ignora. Essa skill entrega:

- **Press release** em PT-BR e EN
- **Boilerplate** (paragrafo padrao sobre a empresa)
- **Fact sheet** (numeros, datas, nomes — jornalista copia direto)
- **Bio + foto do founder** em alta resolucao
- **Logo pack** (PNG, SVG, EPS, em branco e preto)
- **Mockups em alta** (do skill mockups-generator, se rodou)
- **Media list** com jornalistas/veiculos do nicho
- **Templates de pitch email** (frio + warm intro)

## Input

- `./rebrand/01-discovery.md` — historia da marca, founder, numeros
- `./rebrand/05-conversion-angle.md` — angulos, proof stack
- `./rebrand/06-direction.md` — tom de voz
- `./rebrand/07-logo.md` + `./rebrand/logo/final/` — logos
- `./rebrand/mockups/` — mockups em alta
- `./rebrand/18-launch-plan.md` — data D=0

## Procedure

### 1. Press release — PT-BR

Estrutura AP classica:

```markdown
[logo pequeno no topo]

PARA DIVULGACAO IMEDIATA
<Cidade>, <data completa>

# <HEADLINE FORTE DE 60-80 CARACTERES>
## <subheadline complementar, 120 chars max>

<LEAD — paragrafo 1, 30-50 palavras respondendo who/what/when/where/why>
A <marca>, <descricao curta>, anuncia hoje <o que>. A novidade <por que importa>.

<Paragrafo 2 — contexto do mercado / problema>
"<quote do founder, 1-2 frases potentes>", afirma <nome>, <cargo> da <marca>.

<Paragrafo 3 — diferencial / numeros>
<Stats especificos: N clientes, N mercados, crescimento>

<Paragrafo 4 — o que vem a seguir / visao>
<Roadmap publico, expansion plans>

<Paragrafo 5 — disponibilidade / CTA>
<A partir de quando, onde encontrar, link>

## Sobre <marca>
<Boilerplate padrao, 3-5 frases — copia-cola em todo release futuro>

## Contato de imprensa
<nome pessoa> — <email> — <telefone>
Kit de imprensa completo: <link>
```

Regras:
- **Headline passa no "5 segundos test"**: jornalista le e entende imediatamente
- **Lead responde 5Ws**: who, what, when, where, why
- **Quote real do founder** (nao generica "estamos empolgados")
- **Numeros especificos** (nao "crescimento expressivo" — "R$ 2M ARR em 8 meses")
- **Max 1 pagina A4** (400-500 palavras)

### 2. Press release — EN

Mesma estrutura, adaptada pra conventions internacionais:

- Datelined ("SAO PAULO, Brazil — April 24, 2026")
- AP style (numbers spelled out 1-9, numerals 10+, no Oxford comma)
- Shorter sentences (US journalism style)
- Bilingual-friendly tail: "English media contact: <email>"

### 3. Boilerplate (3 versoes)

`./rebrand/press-kit/boilerplate.md`:

```markdown
## Versao longa (100 palavras)
<usada em release, anuncios formais>

## Versao media (50 palavras)
<usada em bio social, assinatura de email>

## Versao curta (25 palavras)
<usada em "about" de parcerias, podcast intros>
```

### 4. Fact sheet

`./rebrand/press-kit/fact-sheet.md`:

```markdown
# <Marca> — Fact Sheet

## Basicos
- **Nome juridico**: <razao social>
- **Nome fantasia**: <marca>
- **CNPJ**: <numero>
- **Fundacao**: <data>
- **Sede**: <cidade, estado>
- **Funcionarios**: <numero>
- **Fundadores**: <nomes, cargos>
- **Site**: <url>

## Produto
- **Categoria**: <e-commerce / SaaS / infoproduto / servico>
- **O que faz**: <1 frase>
- **Para quem**: <publico>
- **Preco**: <faixa>

## Numeros (atualizado em <data>)
- **Clientes ativos**: <numero>
- **Receita anual**: <se publico> ou "nao divulgada"
- **Crescimento YoY**: <%>
- **Mercados**: <paises/regioes>
- **Funding**: <bootstrap / serie / valor>

## Milestones
- <data>: fundacao
- <data>: primeiro produto lancado
- <data>: 1000 clientes
- <data>: expansao pra <mercado>
- <data>: rebranding <-- o evento atual

## Referencias / imprensa ja conquistada
- <veiculo 1> — <link>
- <veiculo 2> — <link>
```

### 5. Founder bio + foto

`./rebrand/press-kit/founder/<nome>/`:

```
bio-longa.md       # 200 palavras
bio-media.md       # 80 palavras  
bio-curta.md       # 30 palavras (pra speaker intros)
headshot-hires.jpg # 3000x3000 min
headshot-web.jpg   # 1200x1200
linkedin-bg.jpg    # 1584x396 pra cover LinkedIn
```

Bio inclui:
- Trajetoria (faculdade, experiencias anteriores)
- Por que fundou <marca>
- Conquistas notaveis
- Falas em eventos / publicacoes proprias
- Fora do trabalho (humaniza — "moro em SP, 2 filhos, corredor amador")

### 6. Logo pack

`./rebrand/press-kit/logos/`:
```
logo-color-hires.png   # 4000px largura
logo-color.svg
logo-color.eps         # pra impressao print (alguns veiculos pedem)
logo-dark.svg
logo-white.svg
logo-mono-black.svg
logo-mono-white.svg
symbol-only.svg        # so o simbolo, sem wordmark
```

Plus README explicando qual usar em qual contexto.

### 7. Media list

`./rebrand/press-kit/media-list.csv`:

```csv
veiculo,editoria,jornalista,email,twitter,linkedin,tipo_historia,last_contact,notes
Exame,Startups,<nome>,<email>,@...,linkedin.com/...,funding/growth,-,cobre SaaS BR
Neofeed,Tech,<nome>,<email>,...,...,rebrand/pivot,-,forte em fintech
MIT Tech Review Brasil,Emergente,<nome>,...,...,...,inovacao,-,"gosta de AI angle"
The Brief,Newsletter,<nome>,...,...,...,founder story,-,"newsletter DTC"
...
```

Lista baseada em discovery:
- **Nicho tech/SaaS**: Exame, Valor, Neofeed, Brazil Journal, Pipeline
- **DTC/e-commerce**: E-commerce Brasil, Ecommerce News, Consumidor Moderno
- **Infoproduto/creator**: Tiozada, Nuvemcreators blog
- **Podcasts**: G4, Like a Boss, Story Bozza
- **Newsletters**: The News, The Shift, Tecland, Thenewsletter
- **Internacional** (se aplica): TechCrunch, The Information, The Hustle, Business Insider BR

30-50 entries minimum.

### 8. Pitch email templates

`./rebrand/press-kit/pitch-templates/`:

**Template 1 — Cold pitch**:
```
Subject: <hook de 1 linha que fala direto com a editoria do jornalista>

Oi <nome>,

Vi teu texto sobre <topico especifico — nao generico> semana passada. <Comentario genuino sobre o que voce concordou/discordou>.

Queria te passar um angulo possivel:

<2 frases do que e a marca e por que importa pra pauta dele>

3 coisas que podem virar historia:
1. <numero forte>
2. <angulo diferenciado>
3. <quote ou tendencia>

Fact sheet completo, logo, foto HD em <link do kit>.

Se fizer sentido, topo conversa — 15 min esta semana. Se nao, nao se preocupa em responder, so queria deixar no radar.

Abrago,
<nome do founder ou PR>
<telefone>
```

**Template 2 — Warm intro** (via conexao mutua):
```
Subject: Intro: <marca> + <veiculo> (via <conexao>)

Oi <jornalista>,

<Conexao> sugeriu te passar um papo sobre <marca>.

Contexto em 3 frases:
<o que faz, pra quem, por que agora>

Se fizer sentido, aqui ta o kit: <link>.

<mesma estrutura de closing do cold>
```

**Template 3 — Embargo** (pra scoop):
```
Subject: Embargo ate <data> — <noticia>

Oi <nome>,

Quero oferecer o scoop dessa antes do anuncio publico. Embargo ate <data/hora>.

<resumo do que e>

Kit completo (embargado): <link com senha>

Se for relevante, topo call exclusiva de 30 min <dias possiveis>.

<closing>
```

**Template 4 — Follow-up** (apos 5 dias sem resposta):
```
Subject: Re: <assunto original>

Oi <nome>, so um follow up rapido caso tenha perdido.

<Resumo em 1 frase + 1 numero forte>

Se nao fizer sentido pra pauta, sem problemas — posso te avisar do proximo?

<closing>
```

### 9. Landing page de press kit

Gera `./rebrand/press-kit/site/index.html` — pagina publica, deployable em `imprensa.<dominio>.com`:

- Hero com release principal + logo
- Download links pra todos os assets (logos zip, fotos, release PDF)
- Fact sheet embedded
- Quotes ready-to-use
- Founder bio + foto
- Contato de imprensa dedicado
- "Como fomos citados" — gallery de logos de veiculos que ja falaram

### 10. Output umbrella

`./rebrand/20-pr-kit.md`:

```markdown
# PR Kit — <marca>

## Assets criados
- Release PT-BR + EN (em `./press-kit/releases/`)
- Boilerplate 3 versoes
- Fact sheet
- Founder bio (3 tamanhos) + fotos HD
- Logo pack 8 formatos
- Media list com <N> contatos
- Pitch email templates x4
- Press kit site (deployable)

## Timeline de pitch recomendada

### 2 semanas antes do D=0
- Pitch pros veiculos "top 5" com oferta de exclusividade (embargo)
- Resposta ate 5 dias — se nao aceitar, libera pra proximos

### 1 semana antes do D=0
- Blast pros proximos 20 veiculos (sem exclusividade)
- Agenda entrevistas pra semana do lancamento

### D=0
- Release publico em PR Newswire / Broadcast
- Follow-up pros que nao responderam na semana anterior

### D+3
- Segundo follow-up
- Engaja em LinkedIn com jornalistas que publicaram algo do nicho

### D+7
- Pacote "como foi o lancamento" — stats reais pra quem quiser cobrir pos
- Newsletter / podcasts pra falar numa entrevista longa

## KPIs
- Respostas / 100 pitches: 10-20% bom, 30%+ otimo
- Publicacoes geradas: 3-10 em launch bem executado
- Estimado alcance: somar audiencia dos veiculos

## Nao confunda PR com marketing pago
- PR e imprevisivel (cobertura nao garantida)
- PR da autoridade (nao conversao direta)
- Combina com ads: ad fecha, PR da "como visto em..."

## Proximos passos
1. Personaliza placeholders (CNPJ, numeros reais, datas)
2. Revisa release pra sua voz
3. Gera PDFs de release (Playwright similar ao brand-book-pdf)
4. Deploy site press-kit em imprensa.<dominio>.com
5. Comeca outreach 2 semanas antes do launch
```

## Quality bar

- **Release respondendo 5Ws no lead.** Se jornalista so ler o lead, entende.
- **Quote real.** "Estamos muito felizes" e lixo. Dizer algo contraintuitivo ou com numero.
- **Media list personalizada.** Nao copia lista generica. Ajusta por nicho.
- **Pitch personalizado.** Um pitch pra um jornalista > blast de 500. Comenta coisa especifica que ele publicou.
- **Follow-up sem ser chato.** Max 2 follow-ups. Depois disso, para.
- **Fotos em alta resolucao.** 72dpi nao serve — jornalista precisa de 300dpi pra print.

## Handoff

Retorna path pra `20-pr-kit.md`, site press-kit preview, media list CSV, e timeline sugerida de outreach.
