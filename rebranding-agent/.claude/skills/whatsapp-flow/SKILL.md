---
name: whatsapp-flow
description: Gera flow completo de WhatsApp Business pra BR — mensagem de boas-vindas, FAQ automatizada (respostas rapidas), funil de vendas via WhatsApp, scripts de atendimento humano, e templates aprovaveis pela Meta (pra notificacao ativa). Exporta em formato importavel pelo WhatsApp Cloud API e pelas principais plataformas de CRM (Zenvia, Take, SleekFlow, Z-API). Use se o discovery indicar publico BR — 80% compra via WhatsApp.
---

# WhatsApp Flow

> **Source & credit**: Conversational marketing pattern adaptado de [Drift](https://www.drift.com/) e [Manychat Instagram playbooks](https://manychat.com). WhatsApp Cloud API specs de [developers.facebook.com/docs/whatsapp](https://developers.facebook.com/docs/whatsapp). Templates que passam aprovacao Meta baseados em guidelines oficiais de 2025.

## Purpose

No Brasil, WhatsApp e o canal dominante de compra em muitos nichos — DTC, high-ticket, servicos locais, infoproduto. Sem um flow de WhatsApp, voce perde lead no "me manda mais info" e no "posso parcelar?". Essa skill entrega:

- Mensagem de boas-vindas automatica
- 10+ respostas rapidas pra FAQ
- Funil de venda conversacional (SPIN/qualificacao)
- Scripts pra atendimento humano quando escala
- Templates aprovaveis pela Meta pra enviar notificacao ativa (confirmacao, abandono, re-engagement)

## Skip condition

Se discovery disse que publico nao e BR e nao usa WhatsApp, pula com um no-op + log.

## Input

- `./rebrand/01-discovery.md` — oferta, ticket, objecoes comuns, horario de atendimento
- `./rebrand/05-conversion-angle.md` — big promise, offer stack, prova social
- `./rebrand/11-email-sequences.md` (se ja existir) — pra alinhar copy

## Procedure

### 1. Mensagem de boas-vindas automatica

Dispara quando usuario manda primeira mensagem:

```
Oi! Aqui e o atendimento da [marca] 👋

Como posso te ajudar? Responde com o numero:

1️⃣ Quero conhecer o produto
2️⃣ Ja sou cliente / suporte
3️⃣ Quero parcelar
4️⃣ Outra coisa

(Se preferir, me manda sua duvida direto que eu respondo.)
```

Regras:
- **Nunca mais de 5 opcoes** — rolagem mata engagement
- **Sempre opcao "outra coisa / falar com humano"** — escala pra atendente se necessario
- **Emoji 1-2 max** — parecer humano, nao robo

### 2. FAQ — respostas rapidas

Pra cada pergunta comum do discovery (ou das objecoes do conversion-angle), gera resposta rapida:

```yaml
- trigger: "preço|preco|quanto custa|valor"
  response: |
    O [produto] sai por R$ X a vista (10% off PIX) ou 12x de R$ Y no cartao.

    Se quiser, te mando o link direto pro checkout: <link>

    Tem alguma duvida especifica antes?

- trigger: "garantia|funciona|devolucao|reembolso"
  response: |
    Tem garantia de 30 dias, incondicional. Se nao gostar, devolvemos 100% do valor, sem perguntas.

    <depoimento de cliente 1 frase>

- trigger: "frete|entrega|prazo"
  response: |
    Frete gratis pro Brasil todo em compras acima de R$ 200. Entrega em 3-8 dias uteis dependendo da regiao.
```

Total: 10-15 respostas cobrindo preco, garantia, parcelamento, frete, formas de pagamento, horario, suporte, "fale com humano", "posso ver depois?".

### 3. Funil de venda conversacional (qualification flow)

Se o usuario escolher "1 - Quero conhecer o produto":

```
Boa! Antes, me responde 3 coisas rapidas pra te ajudar melhor:

1) Qual seu principal problema com [categoria]? (em 1 frase)
```

Apos resposta:

```
Entendi. E voce ja tentou [solucao comum do concorrente]?

a) Sim
b) Nao ainda
c) Nao sei
```

Apos resposta:

```
[Resposta customizada por branch]

Ultima pergunta: em quanto tempo voce quer esse resultado?

a) Tenho urgencia (0-30 dias)
b) 1-3 meses
c) 6+ meses
```

**Branching baseado em respostas**:
- Se urgencia alta + ja tentou concorrente → oferece demo ou chamada
- Se urgencia media + novato → mandar video de explicacao
- Se urgencia baixa → add na lista de nurture (email series)

### 4. Template de mensagem ativa (Meta Approval)

Meta exige approval previo pra mandar mensagem ativa (nao-resposta). Templates comuns:

```yaml
- name: abandoned_cart_br
  category: MARKETING
  language: pt_BR
  body: |
    Oi {{1}}, voce deixou o {{2}} no carrinho.

    Ta valendo cupom de 10% de desconto, valido por mais {{3}} horas.

    Quer que eu mande o link pra voltar e finalizar?
  buttons:
    - type: QUICK_REPLY, text: "Sim, manda o link"
    - type: QUICK_REPLY, text: "Nao quero agora"
    - type: QUICK_REPLY, text: "Tenho uma duvida"

- name: order_confirmation_br
  category: UTILITY
  ...

- name: reengagement_br
  category: MARKETING
  ...

- name: delivery_update_br
  category: UTILITY
  ...
```

**Categoria `UTILITY`** (confirmacao, tracking, lembrete) = barato e aprovavel facil.
**Categoria `MARKETING`** (cupom, reengagement) = mais caro por mensagem, review manual.

Total 6-8 templates cobrindo os casos principais.

### 5. Scripts pra atendimento humano

Quando a conversa escala pra humano, o atendente precisa de scripts:

`./rebrand/whatsapp/human-scripts.md`:

```markdown
# Scripts pra atendimento humano

## Abertura (quando a conversa chega em voce)
"Oi [nome], sou a [atendente]. Vi que voce ta interessado em [produto]. Em que posso ajudar?"

## Qualificacao
- "Me conta um pouco do seu caso — [publico]?"
- "Qual o maior problema hoje com [categoria]?"
- "Ja tentou [concorrente/solucao]? Como foi?"

## Apresentacao do produto (30s ou menos)
"O [produto] faz [funcao 1] + [funcao 2]. Diferente de outras opcoes, a gente [diferencial do conversion-angle]. Clientes como voce tipicamente veem [resultado em prazo]."

## Lidar com objecoes
- **Preco**: "Entendo. Pensa assim: <calculo de ROI / comparacao com concorrente / parcelamento>"
- **"Preciso pensar"**: "Claro. O que especificamente voce quer pensar? (descobrir objecao real)"
- **"Tem garantia?"**: "Sim, 30d incondicional. <reforcar>"
- **"Vou falar com minha socia"**: "Perfeito. Quer que eu te mande um resumo em audio pra ela ouvir? 3 minutos."

## Fechamento
- **Soft close**: "Faz sentido pra voce? Quer que eu mande o link?"
- **Assumptive close**: "Vou deixar reservado entao. Prefere pix ou cartao?"
- **Alternative close**: "A gente tem o plano mensal e o anual. Qual faz mais sentido pra voce?"

## Pos-objecao-final
"Entendo. Fica a vontade. Vou te mandar 1 caso de alguem no seu perfil — se fizer sentido depois, e so responder aqui."
```

### 6. Arquivo de import

`./rebrand/whatsapp/import/`:

- `cloud-api-templates.json` — pronto pra criar via Meta Cloud API
- `z-api-flow.json` — pra Z-API (BR popular)
- `zenvia-flow.json`
- `sleekflow-flow.json`
- `take-blip-flow.json`

### 7. Output umbrella

`./rebrand/12-whatsapp-flow.md`:

```markdown
# WhatsApp Flow — <marca>

## Criado
- Mensagem de boas-vindas
- 12 respostas rapidas (FAQ)
- Funil de qualificacao conversacional (3 perguntas + branching)
- 7 templates pra notificacao ativa (3 UTILITY + 4 MARKETING)
- Scripts pra atendimento humano (objecoes, qualificacao, fechamento)

## Provider setup
- WhatsApp Cloud API (oficial Meta): melhor custo pra volume
- Z-API (BR): mais facil de comecar, sem approval complexa pra templates
- Take Blip / Zenvia: enterprise, bom pra >100k mensagens/mes

## Proximos passos
1. Escolhe provider, cria conta business
2. Verifica numero (precisa ser numero nao-pessoal ou novo chip)
3. Importa templates do `_imports/` — envia pra review Meta (2-24h)
4. Configura auto-response com `welcome.json`
5. Treina atendentes com `human-scripts.md`

## Metrica-chave
- **Response rate**: % de conversas que respondem apos welcome → >40% bom, >60% excelente
- **Qualification completion**: % que responde as 3 perguntas → >50%
- **Conversion rate from WA**: venda / conversas qualificadas → varia por nicho, 5-25%
```

## Quality bar

- **Copy parece humano, nao robo.** Usa "boa", "tranquilo", "ta bom?" quando cai natural.
- **Nao manda 2 mensagens seguidas sem resposta do user.** Quebra conversation flow.
- **Template Meta-approvable.** Nao promocional demais em UTILITY. Nao promete resultado nao-verificavel.
- **LGPD**: opt-in explicito antes de add na lista de mensagem ativa. Disparar pra quem nao autorizou e crime.
- **Horario**: atendimento humano so em horario declarado (8h-20h padrao). Fora disso, auto-response que avisa e dispara flow.

## Handoff

Retorna path pra `12-whatsapp-flow.md`, lista de providers, e checklist de setup (numero, verificacao, templates pra review).
