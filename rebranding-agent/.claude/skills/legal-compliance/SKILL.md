---
name: legal-compliance
description: Gera documentos legais baseline — Politica de Privacidade (LGPD/GDPR), Termos de Uso, Disclaimer pra nichos regulados (saude, financas, dieta, investimento), e checklist de compliance pra Meta/Google Ads policies. NAO substitui advogado, mas cobre 90% dos casos. Sem isso, Meta derruba conta e voce toma multa LGPD. Use depois de discovery.
---

# Legal Compliance

> **Source & credit**: LGPD template adaptado de [iubenda](https://www.iubenda.com) + [ANPD guidelines 2025](https://www.gov.br/anpd). GDPR patterns de [GDPR.eu](https://gdpr.eu) e [ICO UK templates](https://ico.org.uk). Meta Ads policies de [Facebook Advertising Policies 2025](https://www.facebook.com/policies_center/ads/). Google Ads policies de [support.google.com/adspolicy](https://support.google.com/adspolicy). **Essa skill NAO substitui advogado** — especialmente pra nichos regulados (saude, financeiro, investimento, crianca).

## Purpose

Sem documentos legais, voce:
- Leva multa LGPD (ate R$ 50 milhoes ou 2% do faturamento)
- Tem conta de ads derrubada sem aviso (Meta/Google auto-reject)
- Perde credibilidade ("nenhum link de privacidade? golpe?")
- Nao consegue coletar email / dados legalmente

Essa skill entrega:
- Politica de Privacidade (PT-BR LGPD + EN GDPR)
- Termos de Uso
- Cookie Policy
- Disclaimer pra nichos regulados
- Checklist de Meta/Google Ads compliance
- Checklist LGPD (e equivalente GDPR se regiao EU)

## Disclaimer obrigatorio

Templates sao **baseline**. Pra:
- Saude/medico/nutricao → revisao de advogado + CRM/CRN obrigatoria
- Financeiro/investimento → advogado + CVM/BACEN compliance
- Crianca <13 anos → advogado + ECA obrigatoria
- Dados sensiveis (biometria, orientacao sexual, religiao) → advogado obrigatorio

Se o discovery indicar qualquer um desses, a skill **avisa FORTEMENTE** no output e recomenda advogado antes de publicar.

## Input

- `./rebrand/01-discovery.md` — categoria (pra detectar nicho regulado), regiao (BR/EU/US), modelo (coleta dados, cobra, manda email)
- `./rebrand/.selected-name.json` — nome juridico vs fantasia
- (Opcional) CNPJ / endereco / contato legal se user informou

## Procedure

### 1. Detecta nicho regulado

Flags baseadas em discovery:

```python
regulated_niches = {
    "saude": ["saude", "medico", "nutricao", "suplemento", "estetica", "emagrecimento", "clinica"],
    "financeiro": ["investimento", "trading", "acoes", "cripto", "emprestimo", "financiamento", "seguro"],
    "crianca": ["infantil", "kids", "crianca", "bebe", "escola", "brinquedo"],
    "gambling": ["aposta", "casino", "bet", "bingo"],
    "adulto": ["18+", "adulto", "sex"],
}
```

Se bater, adiciona avisos pesados no output + clausulas extras no disclaimer.

### 2. Politica de Privacidade — LGPD (PT-BR)

`./rebrand/legal/politica-de-privacidade.md`:

Estrutura padrao:

```markdown
# Politica de Privacidade

_Ultima atualizacao: <data>_

## 1. Quem somos
- **Nome juridico**: <razao social>
- **CNPJ**: <numero ou "em constituicao">
- **Endereco**: <endereco fisico obrigatorio>
- **Contato DPO**: <email>@<dominio> (ou o fundador se nao tem DPO formal)

## 2. Quais dados coletamos
### Dados que voce fornece
- Nome, email, telefone (ao se cadastrar, comprar, entrar em contato)
- Endereco de entrega (se e-commerce)
- Dados de pagamento (via processador — nao armazenamos cartao)

### Dados coletados automaticamente
- IP, user agent, localizacao aproximada
- Paginas visitadas, tempo na pagina
- Fonte de trafego (UTM)
- Cookies (ver Politica de Cookies)

## 3. Base legal (LGPD art. 7)
<mapeia cada finalidade a sua base legal>
- Envio de email marketing → consentimento (art. 7 I)
- Processar compra → execucao de contrato (art. 7 V)
- Atender suporte → legitimo interesse (art. 7 IX)
- Cumprir obrigacao fiscal → obrigacao legal (art. 7 II)

## 4. Com quem compartilhamos
- Processador de pagamento: <Stripe/Pagarme/etc>
- Email provider: <Mailchimp/etc>
- Analytics: Google (GA4), Meta (Pixel)
- Hospedagem: <Vercel/AWS/etc>
- **Nao vendemos seus dados pra terceiros.**

## 5. Transferencia internacional
Alguns servicos citados acima hospedam dados fora do Brasil (EUA principalmente). Nos mantemos as salvaguardas contratuais exigidas pela LGPD (art. 33) com esses fornecedores.

## 6. Retencao de dados
- Conta ativa: enquanto voce usar
- Pos-cancelamento: <X> meses (obrigacao fiscal = 5 anos minimo pra dados de compra)
- Marketing: ate voce revogar consent

## 7. Seus direitos (LGPD art. 18)
Voce pode, a qualquer momento:
- Confirmar se tratamos seus dados
- Acessar os dados
- Corrigir dados incompletos/imprecisos
- Anonimizar, bloquear ou eliminar dados desnecessarios
- Portar dados pra outro fornecedor
- Revogar consentimento
- Opor-se a tratamento com base em legitimo interesse

Pra exercer: email <dpo@dominio>. Respondemos em ate 15 dias uteis.

## 8. Cookies
Ver [Politica de Cookies](/cookies).

## 9. Menores
Nossos servicos sao destinados a maiores de 18 anos. <SE nicho kids, substituir totalmente>

## 10. Alteracoes
Podemos atualizar essa politica. Mudancas significativas serao notificadas por email.

## 11. Contato
<email> | <telefone opcional>
```

### 3. Politica de Privacidade — GDPR (EN, se regiao EU)

Gera versao em ingles cobrindo Art. 13 GDPR: controller identity, purposes, legal basis, recipients, retention, rights (access, rectification, erasure, portability, objection, restriction), right to lodge complaint with DPA, if automated decision-making, if transfer outside EU (safeguards).

### 4. Termos de Uso

`./rebrand/legal/termos-de-uso.md`:

Cobre:
- Aceitacao dos termos
- Descricao do servico
- Cadastro (idade minima, veracidade de dados)
- Pagamento (forma, parcelamento, reembolso)
- **Politica de reembolso** — alinhada com CDC: 7 dias arrependimento pra compra online
- Propriedade intelectual (o conteudo e da empresa, user nao pode copiar)
- Condutas proibidas (uso comercial indevido, reverse engineer, etc.)
- Responsabilidade limitada
- Alteracoes no servico
- Rescisao
- Foro (comarca do CNPJ)

### 5. Cookie Policy

`./rebrand/legal/cookies.md`:

Lista todos os cookies que o site usa, agrupados por categoria:

| Categoria | Cookie | Fornecedor | Finalidade | Retencao |
| --- | --- | --- | --- | --- |
| Essencial | session_id | <marca> | Manter login | sessao |
| Essencial | consent_state | <marca> | Guardar consent LGPD | 365d |
| Analitico | _ga, _ga_* | Google | Analytics | 2 anos |
| Marketing | _fbp, _fbc | Meta | Attribution de ads | 3 meses |
| Marketing | gtag | Google | Conversions Google Ads | 90d |

Conecta com o Consent Banner do `analytics-setup` — categorias aqui batem com toggles la.

### 6. Disclaimer pra nicho regulado

Se detectou nicho regulado, gera disclaimer adicional:

**Saude**:
```
Este conteudo tem carater educativo e nao substitui consulta medica.
Resultados individuais variam. <depoimento de cliente> nao representa
garantia de resultado. Antes de iniciar qualquer tratamento, consulte
profissional habilitado.

Responsavel tecnico: <Dr./Dra. Nome, CRM/CRN xxxx>.
```

**Financeiro / investimento**:
```
<Marca> nao e instituicao financeira registrada na CVM/BACEN. O conteudo
e educacional e nao constitui recomendacao de investimento. Investimentos
envolvem risco de perda do capital. Resultados passados nao garantem
resultados futuros. Consulte profissional certificado antes de investir.
```

### 7. Checklist Meta/Google Ads compliance

`./rebrand/legal/ads-compliance.md`:

```markdown
# Ads Compliance Checklist

## Meta Ads
- [ ] Dominio verificado no Business Manager
- [ ] Privacy Policy URL ativa (Meta requer pra qualquer conta de ads)
- [ ] Sem claims de resultado nao-verificavel (ex: "ganhe R$ 10k/mes garantido")
- [ ] Sem antes/depois explicito em saude/beleza (politica 2023 ainda vale)
- [ ] Sem "voce" apontando pra caracteristicas pessoais proibidas (ex: "perdeu emprego?", "ta endividado?")
- [ ] Saude: sem imagem grafica, sem "cura", sem medical claims
- [ ] Financeiro: disclaimer obrigatorio + link pra termos no ad
- [ ] Gambling: license number visivel + regiao restrita

## Google Ads
- [ ] Privacy policy URL ativa
- [ ] Landing page funcional e sem redirect enganoso
- [ ] Consistencia: keyword → ad → LP → produto (ou Google da quality score baixo)
- [ ] Saude: restricted category (precisa certification)
- [ ] Finance: Brasil permite com limitacoes — checar "Financial services ads" policy
- [ ] Comparacoes legais: so com base verificavel

## Dark patterns a evitar (todas as plataformas)
- [ ] Countdown falso que reseta
- [ ] Prova social fake (logos de empresa sem autorizacao, depoimento falso)
- [ ] Scarcity falso ("so 3 vagas" quando sao 3 mil)
- [ ] Confirm-shaming no opt-out ("Nao, eu nao quero ter sucesso")

Ads com dark pattern = risco de conta banida + processo por publicidade enganosa (CDC).
```

### 8. Checklist LGPD

`./rebrand/legal/lgpd-checklist.md`:

- [ ] Politica de Privacidade publicada em URL estavel
- [ ] Cookie banner com opt-in (nao opt-out) pra nao-essenciais
- [ ] Campo de consent no signup/checkout (checkbox NAO pre-marcada)
- [ ] Endereco de DPO/encarregado publico
- [ ] Processo pra atender requisicao de direitos (resposta em 15d)
- [ ] Registro de operacoes de tratamento (RoPA — obrigatorio pra empresas medias+)
- [ ] Contrato de DPA com fornecedores (Mailchimp, Google, Meta tem padrao)
- [ ] Criptografia em transit (HTTPS sempre) e at-rest (DB criptografado)
- [ ] Processo de notificacao de incidente (data breach) em 72h pra ANPD
- [ ] Termo de consentimento guardado e versionado
- [ ] Minimizacao de dados: coleta so o necessario

### 9. Implementacao no codigo

Rotas obrigatorias no site:

- `/politica-de-privacidade` ou `/privacy` — PT-BR + EN se regiao mista
- `/termos-de-uso` ou `/terms`
- `/cookies`
- `/contato-dpo` ou email dedicado `dpo@<dominio>`

Link pra cada uma **no footer** de todas as paginas.

No form de signup:
```html
<label>
  <input type="checkbox" name="consent" required />
  Li e aceito a <a href="/politica-de-privacidade">Politica de Privacidade</a>
  e os <a href="/termos-de-uso">Termos de Uso</a>.
</label>
<label>
  <input type="checkbox" name="marketing_consent" />
  Quero receber dicas e ofertas por email.
</label>
```

### 10. Output umbrella

`./rebrand/15-legal-compliance.md`:

```markdown
# Legal Compliance — <marca>

## Documentos gerados
- /legal/politica-de-privacidade.md (PT-BR LGPD)
- /legal/privacy-policy.md (EN GDPR, se regiao EU)
- /legal/termos-de-uso.md
- /legal/cookies.md
- /legal/disclaimer-<nicho>.md (se nicho regulado)
- /legal/ads-compliance.md
- /legal/lgpd-checklist.md

## Avisos
⚠️ NICHO REGULADO DETECTADO: <nicho>. Consulte advogado especializado antes de publicar.
⚠️ ANPD pode exigir registro formal se voce processa dados em larga escala ou sensiveis.

## Proximos passos
1. Review pessoal: ler cada doc, substituir <placeholders> por dados reais (razao social, CNPJ, enderecos)
2. Review legal: mandar pra advogado se nicho regulado ou >10k dados pessoais/mes
3. Publicar: instalar no site em /legal/* e linkar no footer
4. Consent banner: integrar com analytics-setup
5. Atualizar a cada mudanca significativa (novo fornecedor, novo tipo de dado)
```

## Quality bar

- **Nunca afirme que o doc substitui advogado.** Esta escrito o disclaimer pra protecao sua e do usuario.
- **Placeholders visiveis.** `<RAZAO SOCIAL>` em uppercase pro user nao esquecer de substituir.
- **Idioma bate com publico.** BR → PT-BR. EU → EN + local. US → EN.
- **Retencao minima respeitada.** Dados fiscais: 5 anos minimo no BR.
- **Cookies declarados batem com os reais.** Analytics-setup e essa skill tem que estar alinhados — se cookie policy nao lista `_fbp` mas pixel esta instalado, e violacao.

## Handoff

Retorna path pra `15-legal-compliance.md`, lista de avisos, e se nicho regulado foi detectado (pra orchestrator reforcar).
