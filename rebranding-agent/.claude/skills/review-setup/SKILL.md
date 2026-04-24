---
name: review-setup
description: Configura estrategia de reviews pra Google Business, Trustpilot, Reclame Aqui (BR), G2 (SaaS), ProductHunt (launch dia), Capterra. Inclui fluxo de coleta automatica pos-venda, templates de resposta pra review bom/ruim, estrategia de incentivo ethical, e monitoring. Reviews sao o social proof mais barato de escalar. Use depois de email-sequences e launch-plan.
---

# Review Setup

> **Source & credit**: Review flywheel framework de [G2's 2025 Buyer Behavior Report](https://www.g2.com/research) + [Harvard Business Review on review influence](https://hbr.org). Brazilian-specific playbook (Reclame Aqui, Google Business) de [Neoassist's CX reports](https://www.neoassist.com). Response templates adapted from [Jay Baer's "Hug Your Haters"](https://www.jaybaer.com).

## Purpose

Em 2026, 93% dos compradores le review antes de comprar (BrightLocal). Sem review strategy:
- Voce entra na categoria "marca sem historia"
- CVR em LP cai 30-50% vs concorrente com reviews visiveis
- Google nao te ranqueia bem sem Google Business reviews
- No BR, sem Reclame Aqui score = pe atras automatico

Essa skill entrega:
- Setup em todas as plataformas relevantes pro nicho
- Fluxo de coleta automatica pos-venda
- Templates de resposta (positivo + negativo)
- Estrategia ethical de incentivo
- Monitoring + alerts
- Widget pra embed de reviews no site

## Input

- `./rebrand/01-discovery.md` — categoria, regiao, modelo
- `./rebrand/11-email-sequences.md` — ja tem email 14 no post-purchase ("Review request")
- `./rebrand/13-landing-page.md` — pra embed de widget

## Procedure

### 1. Plataformas por categoria

**E-commerce (DTC)**:
- Google Business Profile (obrigatorio)
- Trustpilot
- Reclame Aqui (BR) — obrigatorio no Brasil
- Review on-site (Judge.me, Loox, Yotpo)

**SaaS**:
- G2 (obrigatorio B2B)
- Capterra
- TrustRadius
- ProductHunt (launch day)
- Google Business Profile

**Servico local**:
- Google Business Profile (super critico)
- TripAdvisor (se hospitality)
- Yelp (menos relevante BR)
- Reclame Aqui

**Infoproduto**:
- Trustpilot
- Reclame Aqui
- Google Business
- Review on-site

**Restaurante / food**:
- Google Business
- TripAdvisor
- iFood (BR)
- ifood rating aparece no Google direct

### 2. Setup de cada plataforma

Pra cada plataforma relevante, gera `./rebrand/reviews/<plataforma>/setup.md`:

**Google Business Profile**:
- Criar conta em business.google.com
- Verificacao: cartao postal, video, telefone (depende de categoria)
- Completar 100% do perfil (fotos, horarios, produtos, atributos)
- Primeiro post semanal (Google valoriza atividade)
- Pedir pra 10-20 clientes iniciais deixar review organico
- Link de review: `https://g.page/r/<place-id>/review`

**Trustpilot**:
- Criar conta Business
- Claim do dominio
- Invite emails (via integracao ou CSV upload)
- Widget pra site (4 estilos pre-configurados)
- Resposta publica visivel (responda 100%, bom ou ruim)

**Reclame Aqui (BR)**:
- Criar conta corporativa
- Processo de verificacao CNPJ (7-15 dias)
- Target indice RA >8.5
- Fluxo de resposta interno: reclama chega → responde em 24h → encaminha setor → resolve → pede avaliacao final
- Badge "RA1000" / "Great" vem com volume + nota

**G2 (SaaS)**:
- Vendor profile setup (free)
- Claim by email corporativo
- Categorizacao correta (Grid ranking depende)
- Invite via G2's own invite tool OR CSV
- Foco em reviewers com LinkedIn profile (da credibilidade)

**ProductHunt (launch day)**:
- Criar submission 7 dias antes
- Agendar pra 00:01 PST (maximiza 24h window)
- Rally da base: email + social no D=0 pedindo "comment + upvote"
- Mais importante: comentario thoughtful > upvote
- Maker comment no topo com historia

### 3. Fluxo de coleta automatica pos-venda

Ja tem no `email-sequences` (Email 5 do post-purchase — day 14). Essa skill reforca e adiciona:

**Timeline**:
```
D+0 compra
D+7 email "como ta indo?" (NPS interno, nao vai pra plataforma)
  └─ Se NPS 9-10 → envia pra review publica
  └─ Se NPS 7-8 → agradece + pedido de melhoria privada
  └─ Se NPS 0-6 → escala pra suporte (fix before damage)
D+14 email review request (so pros 9-10 do NPS)
D+30 segundo lembrete se nao reviewou
D+60 last try, menciona "5 min ajuda muito"
```

Esse **NPS gate** protege — evita mandar cliente insatisfeito direto pra Trustpilot.

**Implementacao**:
- Tool: Delighted / Hotjar / Typeform simples
- Campos: "De 0-10, quanto voce indicaria pra um amigo?" + "Por que?"
- Logic: score >8 → email de review-request com link direto + 1-click
- Score <=8 → email "quer me contar mais?" → vira conversa de retencao

### 4. Templates de resposta

`./rebrand/reviews/response-templates/`:

**Review 5 estrelas positivo**:
```
Oi <nome>! 🙌

Obrigado por compartilhar. O que voce falou sobre <detalhe especifico do review> e exatamente o que a gente quer ouvir — significa que <resultado desejado> funcionou.

Se precisar de algo, estamos aqui em <email/whatsapp>.

<nome do atendente> — <marca>
```

**Review 4 estrelas (bom com ressalva)**:
```
Oi <nome>, obrigado pelo review!

Vi que voce mencionou <ressalva>. Concordo — essa e uma area que estamos trabalhando ativamente. <O que especificamente estamos fazendo>.

Quer conversar por <canal>? Topo ouvir mais detalhes pra melhorar.

<nome> — <marca>
```

**Review 1-3 estrelas negativo**:
```
Oi <nome>, antes de tudo, desculpa por essa experiencia.

O que voce descreveu <especificidade do problema> nao e o padrao que a gente se propoe. Quero entender melhor o que aconteceu e fazer certo.

Pode me mandar email em <dpo@dominio> com numero do pedido? Respondo em 24h com uma resolucao.

<nome> — fundador/CX da <marca>
```

**Review fake / injusto**:
```
Oi <nome>, infelizmente nao encontramos registro de compra com esse nome/email na nossa base.

Se for engano, ficamos a disposicao pra validar: <email>. Se voce for cliente e esqueceu de qual email usou, tambem podemos ajudar.

Estamos comprometidos em responder 100% dos reviews — e ajudar mesmo fora da compra.

<nome> — <marca>
```

Regras de tom:
- Nunca defensivo
- Nunca "voce ta errado" em publico (resolva privado)
- Sempre convidar pra conversa privada pra resolver
- Nunca oferecer reembolso em publico (vira template pros haters)
- Assina com NOME DE PESSOA (nao "Equipe X")

### 5. Estrategia de incentivo ethical

**O que voce PODE fazer**:
- Pedir review (sem exigir nota positiva)
- Facilitar (link direto, email templatizado)
- Dar pequeno incentivo **pelo ato de reviewar** (nao pela nota): ex "quem reviewar ganha 10% no proximo pedido"
- Fazer follow-up 2-3x

**O que voce NAO PODE**:
- Pagar por review positiva
- Incentivar review 5 estrelas especificamente
- Mandar email so pra clientes felizes (selection bias — Amazon / Google ja banem)
- Criar review fake (crime em BR — Lei 12.965/2014)
- Deletar review negativo sem motivo legitimo

**Plataformas sao rigorosas**: TrustPilot ja baniu marcas com review suspeitas. G2 da warning publico. Google shadow-bans.

### 6. Widget pra site

Gera embed codes pra cada plataforma:

`./rebrand/reviews/widgets/trustpilot.html`:
```html
<div class="trustpilot-widget" 
     data-locale="pt-BR" 
     data-template-id="53aa8912dec7e10d38f59f36" 
     data-businessunit-id="<your-id>" 
     data-style-height="240px" 
     data-style-width="100%">
  <a href="https://www.trustpilot.com/review/<dominio>" target="_blank">Trustpilot</a>
</div>
<script src="//widget.trustpilot.com/bootstrap/v5/tp.widget.bootstrap.min.js" async></script>
```

Integracao com LP do skill `landing-page` — bloco "Social proof" vira widget real.

### 7. Monitoring & alerts

Setup de monitoring:
- Google Alerts: `"<marca>" site:trustpilot.com OR site:reclameaqui.com.br`
- Mention.com ou Talkwalker (free tier) pra nome da marca
- Slack webhook integration: novo review chega → notifica canal #reviews
- Weekly digest email: volume + NPS medio + responses pendentes

### 8. Output umbrella

`./rebrand/21-review-setup.md`:

```markdown
# Review Setup — <marca>

## Plataformas configuradas
- Google Business Profile: <link>
- Trustpilot: <link>
- Reclame Aqui: <link>
- <outras por nicho>

## Fluxo de coleta
- NPS interno em D+7 (Delighted)
- Review request em D+14 (so NPS 9-10)
- Reminders em D+30 e D+60
- Incentivo: 10% off proximo pedido

## Templates
- 4 response templates (5 star, 4 star, 1-3 star, fake)
- Pasta: `./rebrand/reviews/response-templates/`

## Widget
Embed no site em <onde na LP>:
- Trustpilot widget
- Google reviews widget
- "Amado por <N> clientes" counter

## Monitoring
- Google Alerts configurado
- Slack webhook: #reviews
- Weekly digest: segundas 09h

## KPIs alvo (6 meses)
- Google Business reviews: >50 (5 estrelas >4.6)
- Trustpilot: >100 (>4.5)
- Reclame Aqui: nota >8.5, "Otimo" ou "RA1000"
- Response rate: 100% em <24h
- Review request conversion: >15%

## Proximos passos
1. Claim das contas nas plataformas (alguma leva 7-15 dias)
2. Integra NPS em D+7 no email-sequences ja criado
3. Treina time CX nos templates
4. Embed widget no site
5. Setup Slack webhook + Google Alerts
6. D=0 do launch: pede review primeiros 20 clientes amigos
```

## Quality bar

- **Responde 100% dos reviews.** Nao responder review negativo = pior que receber.
- **Tempo de resposta <24h.** Reviews ficam la pra sempre — resposta lenta marca.
- **Nome de pessoa real.** "Equipe X" e robotico.
- **Resolve em privado.** Em publico, so reconhece e convida.
- **Nunca compra review.** Risco de banimento + multa CDC + perda de trust permanente.
- **NPS gate.** Nao mande email de review pra cliente insatisfeito.

## Handoff

Retorna path pra `21-review-setup.md`, lista de links de cada plataforma, templates, e checklist de ativacao semanal.
