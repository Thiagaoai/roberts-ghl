# PRD — Rebranding Agent

**Document status**: v1.0 · 2026-04-24
**Owner**: Thiago do Carmo
**Stakeholders**: Claude Code end-users; rebranding consultants; solopreneurs
**Validation case**: thiagaoai rebrand (thiagodocarmo.com → thiagao.ai)

---

## 1. Problem statement

Rebranding uma empresa hoje e:

- **Caro** — agencia cobra R$30k-500k, leva 3-6 meses
- **Fragmentado** — nome (naming studio), logo (designer freelancer), copy (copywriter), LP (dev), ads (growth agency), legal (advogado), analytics (growth ops) — 8+ fornecedores, orcamento mensal, zero coordenacao
- **Inconsistente** — cada fornecedor entrega no silo, resultado final e Frankenstein de estilos
- **Inescalavel pra solo-founder** — 95% dos founders nao tem budget pra agencia. Resultam em rebrand meia-boca ou nao-rebrand
- **Dificil de manter depois** — brand guidelines em PDF esquecido, time nao acha tokens, freelancer improvisa

O **rebranding-agent** resolve atraves de um agente de IA que orquestra 25 skills especializadas dentro do Claude Code. Um founder roda `@rebrander` no repo da propria empresa e, em ~1-2 dias de interacao, sai com: pesquisa de concorrentes, nome validado, logo, direcao visual, copy, LP, analytics, legal, ads, email, WhatsApp, social, SEO plan, PR kit, brand book PDF, e launch plan — tudo aplicado no codigo e num PR pronto.

## 2. Goals & non-goals

### Goals

| # | Goal | Metric |
| --- | --- | --- |
| G1 | Founder solo consegue rebrand completo sem contratar agencia | Time-to-PR < 3 dias, custo < $100 em tokens |
| G2 | Entregas sao **editaveis** (SVG, HTML, JSON — nao PNG final fechado) | 100% dos artefatos em formato aberto |
| G3 | Decisoes irreversiveis (nome, logo, direcao, PR) sempre tem checkpoint humano | Zero commits sem aprovacao explicita |
| G4 | Cada skill e indepenmente invocavel; pipeline flexivel | Usuario pode rodar "so identidade" ou "so ads" ou ciclo completo |
| G5 | Sistema e transparente — todo artefato em `./rebrand/` inspecionavel | Nenhum blackbox de decisoes |
| G6 | Qualidade dos outputs igual ou superior a agencia media | Validacao qualitativa em 5 rebrands |

### Non-goals (explicitamente fora do escopo v1)

- **Nao cria site do zero sem input** (agente adjacente `web-builder` faz isso)
- **Nao compra dominio automaticamente** (so checa disponibilidade)
- **Nao loga em redes sociais pra atualizar** (usuario faz manual via checklist)
- **Nao sobe ads direto no Meta/Google** (entrega CSVs + plano de teste)
- **Nao substitui advogado** em nichos regulados (saude/financeiro/crianca) — flag e recomendacao explicita
- **Nao roda A/B tests na LP gerada** (deixa plano, execucao e do usuario)
- **Nao otimiza SEO existente** (plano pra construir, nao corrigir)

## 3. Users & personas

### Persona primaria — "Solo founder tecnico"
- Dev/builder com produto em fase beta/lancamento
- Sem orcamento de agencia, quer autoridade visual rapido
- Ja usa Claude Code e GitHub pra desenvolvimento
- Sabe commitar codigo, abrir PR, ler markdown
- **Exemplo: Thiago do Carmo (validation case)**

### Persona secundaria — "Consultor de rebranding"
- Freelancer / small studio que quer entregar mais rapido
- Usa o agent pra primeira passada, polish manual depois
- Justifica premium pro cliente ("10x mais entregas por projeto")

### Persona terciaria — "Founder nao-tecnico ambicioso"
- Nao programa mas sabe seguir instrucoes
- Tem Claude Code Web (nao CLI)
- Executa o pipeline via chat com guidance
- Contrata dev pra "apply" final

### Anti-persona (nao mira)
- CMO de enterprise com time interno — prefere agencia
- Rebrand de marca regulada (farmaceutico, bank) — nao use sem advogado
- Founder que quer controle manual de cada pixel — use Figma, nao agent

## 4. User journeys

### Journey A — Ciclo completo (DTC Brazil)

```
Dia 0  → @rebrander
         ├ Kickoff: 4 perguntas (nome, URL, repo path, idioma)
         ├ Discovery interview: 8 rondas, ~30 min
         └ Competitor research: 10 min automatic
Dia 0 (cont.) → Checkpoint 1: naming (10-15 opcoes)
         └ User aprova "Nome X"
Dia 1  → Audit + style-extract + conversion-angle (paralelo, 15 min)
         └ Checkpoint 2: brand-direction (3 direcoes)
         └ User aprova "Direcao Y"
Dia 1 (cont.) → Logo design (3 conceitos)
         └ Checkpoint 3: logo pick
Dia 1 (cont.) → Legal + LP + lead-magnet + analytics (paralelo, 30 min)
Dia 2  → Ads Meta + UGC scripts + Google Ads (paralelo, 20 min)
Dia 2 (cont.) → Email + WhatsApp + Reviews (paralelo, 15 min)
Dia 2 (cont.) → Social + Calendar + SEO + PR (paralelo, 30 min)
Dia 3  → Brand book PDF + Launch plan + apply-rebrand PR
         └ Checkpoint 4: approve PR
Dia 3 (cont.) → Merge, deploy, cutover.

Total: ~6h de interacao humana, 3 dias corridos.
Outputs: 40+ arquivos, PR ao site, deploy-ready.
```

### Journey B — Parcial (so identidade)

```
Dia 0  → @rebrander ... "so quero direcao visual nova"
         ├ Discovery (minimal)
         ├ Competitor research
         ├ Conversion-angle
         └ Brand-direction + logo + brand-book

Total: 2-3h, 1 dia.
Outputs: 10-15 arquivos + brand book PDF.
```

### Journey C — Incremental (adiciona bloco depois)

```
Semana 1 → Bloco A rodou, founder satisfeito com identidade
Semana 3 → User volta: @rebrander --continue
         ├ Agent le ./rebrand/ existente
         ├ Executa bloco B (legal, LP, lead-magnet, analytics)
         └ Artefatos respeitam tokens/voz ja aprovados
```

## 5. Functional requirements

### 5.1 Core pipeline
- **FR-1**: Sistema DEVE aceitar invocacao via `@rebrander` no Claude Code
- **FR-2**: Sistema DEVE fazer discovery interview estruturado em 8+ rondas (`discover-brand` skill)
- **FR-3**: Sistema DEVE persistir todo estado em `./rebrand/` no cwd do usuario
- **FR-4**: Sistema DEVE numerar artefatos seguindo mapping canonico 01-24 (ver SDD §4)
- **FR-5**: Sistema DEVE respeitar grafo de dependencia (skill so roda apos inputs existirem)
- **FR-6**: Sistema DEVE permitir rodar skills individuais OU sequencia completa
- **FR-7**: Sistema DEVE pausar em cada checkpoint com `AskUserQuestion` e aguardar resposta
- **FR-8**: Sistema DEVE detectar idioma do usuario (PT-BR/EN) e responder alinhado
- **FR-9**: Sistema DEVE detectar regiao (BR/EU/US) pra ativar skills contextuais (WhatsApp/LGPD/GDPR)
- **FR-10**: Sistema DEVE detectar nicho regulado e flaguar obrigatoriedade de advogado

### 5.2 Skills individualmente
- **FR-11**: `discover-brand` DEVE produzir `01-discovery.md` com Pipeline Activation explicita por bloco
- **FR-12**: `competitor-research` DEVE analisar 3-5 concorrentes com mapa 2x2 + brecha
- **FR-13**: `naming` DEVE gerar 10-15 opcoes com check de dominio + handles social
- **FR-14**: `site-audit` DEVE usar Playwright pra screenshots 3 breakpoints + critique
- **FR-15**: `style-extract` DEVE extrair tokens (palette, type, spacing, radius, shadows) em JSON
- **FR-16**: `conversion-angle` DEVE entregar big promise + 3 hooks + offer stack + proof + CTAs
- **FR-17**: `brand-direction` DEVE propor 2-3 direcoes com tokens JSON + mockup
- **FR-18**: `logo-design` DEVE entregar 3 conceitos em SVG com variantes (color/dark/mono)
- **FR-19**: `legal-compliance` DEVE gerar Privacy + Terms + Cookies + nicho-specific disclaimer
- **FR-20**: `landing-page` DEVE detectar stack (Next/Astro/static/WP) e gerar codigo apropriado
- **FR-21**: `lead-magnet` DEVE gerar PDF + LP opt-in + 7 emails de nurture
- **FR-22**: `analytics-setup` DEVE instalar GA4+Pixel+CAPI+Consent Mode server-side
- **FR-23**: `ad-creatives` DEVE gerar 27 criativos Meta (3x3x3) + CSV de import
- **FR-24**: `ugc-scripts` DEVE gerar 6 scripts (15s/30s/60s) com shot list + briefing creator
- **FR-25**: `google-ads` DEVE gerar Search + PMax + YouTube + Remarketing com CSV import
- **FR-26**: `email-sequences` DEVE gerar 4 sequencias (welcome/abandoned/re-eng/post-purchase)
- **FR-27**: `whatsapp-flow` DEVE gerar boas-vindas + FAQ + funil + templates Meta-approvable
- **FR-28**: `review-setup` DEVE gerar links + templates de resposta + widget embed
- **FR-29**: `social-presence` DEVE gerar bio + avatar + cover + templates em 8 canais
- **FR-30**: `content-calendar` DEVE gerar 30 dias × canal com copy pronto + horarios
- **FR-31**: `seo-content-plan` DEVE gerar 6 meses de pillars/clusters + technical audit
- **FR-32**: `pr-kit` DEVE gerar release bilingue + media list + pitch templates
- **FR-33**: `brand-book-pdf` DEVE gerar PDF A4 + site interno + Figma library JSON
- **FR-34**: `launch-plan` DEVE gerar timeline 14-30d + copy por canal + rollback
- **FR-35**: `apply-rebrand` DEVE detectar stack e abrir PR com tokens aplicados

### 5.3 Integrations
- **FR-36**: Sistema DEVE gerar CSVs importaveis por Mailchimp / ActiveCampaign / Klaviyo / RD Station
- **FR-37**: Sistema DEVE gerar JSON importavel por Meta Ads Manager / Google Ads Editor
- **FR-38**: Sistema DEVE gerar Figma Tokens compatible JSON (W3C Design Tokens spec)
- **FR-39**: Sistema DEVE gerar Notion/Airtable/Trello CSVs pro calendario
- **FR-40**: Sistema DEVE gerar GTM container JSON importavel

## 6. Non-functional requirements

### Performance
- **NFR-1**: Pipeline full (24 fases) DEVE completar em <6h de interacao humana total
- **NFR-2**: Skills individuais DEVEM completar em <10 min cada
- **NFR-3**: Artefatos de `landing-page` DEVEM respeitar Lighthouse perf ≥90

### Reliability
- **NFR-4**: Falha de 1 skill NAO DEVE quebrar pipeline — reporta e permite skip
- **NFR-5**: Checkpoints DEVEM ser idempotentes — usuario pode voltar e mudar
- **NFR-6**: Estado em `./rebrand/` DEVE sobreviver reinicio da sessao Claude Code

### Security & Privacy
- **NFR-7**: Sistema NAO DEVE exfiltrar credenciais (env vars, tokens) pra LLM
- **NFR-8**: Artefatos legais DEVEM explicitamente disclaimar "nao substitui advogado"
- **NFR-9**: Em nicho regulado, sistema DEVE bloquear publicacao ate user confirmar revisao juridica
- **NFR-10**: Conversion API token DEVE ser sempre server-side, nunca em client code

### Maintainability
- **NFR-11**: Cada SKILL.md DEVE ter frontmatter YAML com `name` + `description`
- **NFR-12**: Cada skill DEVE declarar Input + Output sections
- **NFR-13**: Grafo de dependencia DEVE ser validavel automaticamente (sem orphans)
- **NFR-14**: Atualizar uma skill NAO DEVE quebrar as outras (contratos publicos em artifact layout)

### Usability
- **NFR-15**: CLI DEVE pedir no maximo 4 perguntas por momento (`AskUserQuestion` limit)
- **NFR-16**: Artefatos markdown DEVEM ser lidos/editados sem ferramenta especial
- **NFR-17**: Outputs DEVEM usar idioma do usuario (PT-BR/EN detectado)

### Compliance
- **NFR-18**: Conteudo gerado em `legal-compliance` DEVE incluir placeholders visiveis (`<CNPJ>`, `<ENDERECO>`)
- **NFR-19**: `analytics-setup` DEVE implementar Consent Mode V2 (default denied) pra LGPD/GDPR
- **NFR-20**: `ad-creatives` + `email-sequences` DEVEM respeitar policy Meta/Google/LGPD

## 7. Success metrics

### Leading indicators (semanais)
- Numero de skill invocations / agent invocations
- Taxa de completion de cada checkpoint (aprovacao vs abandono)
- Tempo medio por fase
- Taxa de erro por skill

### Lagging indicators (mensais)
- Numero de rebrands completos (full-pipeline)
- Numero de PRs criados e mergeados via `apply-rebrand`
- NPS: "voce contrataria agencia ao inves de usar esse agent?" <30 = bad sign
- Qualidade qualitativa via user interviews (5/trimestre)

### Counter-metrics (nao quero subir)
- Tempo excessivo em 1 skill (>30 min = spec ruim)
- Numero de manual overrides (>50% = abstraction errada)
- Reclamacoes de output generico (>20% = prompt ruim)

## 8. Dependencies & risks

### Dependencies
- Claude Code (CLI, Desktop, ou Web)
- Node.js 18+ (pra Playwright)
- Chromium (auto-instalado via Playwright)
- `gh` CLI (opcional, pra PR automatico)
- ImageMagick (opcional, pra favicon.ico)
- Conta em providers externos (Meta Ads, GA4, provider de email) — user-managed

### Risks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| LLM alucina copy falsa (ex: "10k clientes felizes") | Medio | Alto | Quality bar em cada skill exige base verificavel; flag em `conversion-angle` |
| User ignora flag de nicho regulado | Alto | Muito alto | Warning obrigatorio + sem publish check automatico |
| Concorrente copia o sistema inteiro | Medio | Medio | MIT license aceita — diferencial e qualidade das prompts + evolucao continua |
| Meta muda Pixel API quebrando CAPI | Medio | Alto | Versionar em `analytics-setup` skill, updates trimestrais |
| Playwright falha em CI sem Chromium | Alto | Medio | Fallback: pular skills que dependem; instrucoes claras de setup |
| Artefatos PT-BR ruins quando LLM e treinado-EN | Baixo | Medio | Glossary + style sample em cada skill; validacao manual |
| Grafo de dependencia quebra em refactor | Medio | Alto | Script validador no CI (ja implementado em smoke test) |
| User confunde "agent rodando" com "agent ja deployou" | Medio | Alto | Checkpoint visual antes de `apply-rebrand` PR |

### Open questions
- **OQ-1**: Como versionar SKILL.md pra evolucao sem breaking changes?
- **OQ-2**: Deve haver CI auto-rodando smoke test de grafo? (Recomendacao: sim)
- **OQ-3**: Como lidar com skills customizadas por user? (Plugin system?)
- **OQ-4**: Deve haver telemetria opt-in pra entender failure rate? (Privacy risk)

## 9. Roadmap

### v1.0 (current — shipped)
- 25 skills organizadas em 6 blocos
- Orchestrator + discover-brand activation
- Numeracao canonica 01-24
- Grafo de dependencia validado (zero orphans)
- README + docs

### v1.1 (next 1 mes)
- Smoke test automatizado via GitHub Action
- Example run completo (thiagaoai case) versionado como fixture
- Troubleshooting guide pra erros comuns
- Video walkthrough de 10 min

### v1.2 (2-3 meses)
- Skills plugin system (drop-in skill em `.claude/skills-custom/`)
- i18n framework (PT-BR / EN / ES)
- Template library versioned (`gtm-container.json`, email imports, etc.)

### v2.0 (6+ meses)
- Vision-based logo generation (nao so SVG text)
- Multi-brand support (pra agencias rodando 10+ rebrands)
- Integracao nativa com Figma via MCP
- Skill marketplace (community contributions)

## 10. Validation

### Validation case: thiagaoai rebrand
- Pipeline Bloco A rodando agora sobre thiagodocarmo.com → thiagao.ai
- Discovery, competitor research, e proximas fases documentam real-world usage
- Artefatos disponiveis em `/home/user/thiagodocarmo-rebrand/rebrand/` como proof
- Lessons learned alimentam v1.1 improvements

### Planned validation cases (priorizados)
1. DTC e-commerce BR (ciclo completo com WA + LGPD)
2. SaaS B2B US (com Google Ads + G2 + PR)
3. Consultoria servico local (sem ads, foco organic + reviews)
4. Infoproduto creator (com lead-magnet + launch-plan + email heavy)

## 11. Stakeholder sign-off

| Role | Name | Date | Signature |
| --- | --- | --- | --- |
| Owner | Thiago do Carmo | 2026-04-24 | _pending_ |
| Tech reviewer | — | — | — |
| Design reviewer | — | — | — |
