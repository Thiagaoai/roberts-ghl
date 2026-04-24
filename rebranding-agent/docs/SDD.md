# SDD — Rebranding Agent System Design Document

**Document status**: v1.0 · 2026-04-24
**Owner**: Thiago do Carmo
**Companion doc**: [PRD.md](./PRD.md)

---

## 1. Overview

O **rebranding-agent** e um sistema multi-agente implementado como **Claude Code agent + skills package**. O design principio: cada skill e um **unit of work** indepente, documentada em markdown, versionada como arquivo, invocavel via `Skill()` tool. O **orchestrator** (`rebrander.md`) coordena a sequencia, respeita dependencias, pausa em checkpoints, e persiste estado em filesystem (`./rebrand/`).

Nao ha servidor. Nao ha database. O sistema roda 100% dentro da sessao Claude Code do usuario, com outputs em arquivos locais (committaveis). Isso e **deliberado** — portabilidade, inspecao, e usuario e dono do output.

## 2. High-level architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User                                      │
│                  (founder / consultant)                           │
└───────────────────────────────┬─────────────────────────────────┘
                                │ @rebrander
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code Runtime                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           Orchestrator Agent (rebrander.md)                │  │
│  │                                                            │  │
│  │   • TodoWrite → plan phases                               │  │
│  │   • AskUserQuestion → checkpoints                         │  │
│  │   • Skill() → invoke skills in sequence                   │  │
│  │   • Read/Write/Edit → manage ./rebrand/ artifacts         │  │
│  │   • Bash → run Playwright, curl, git, etc.                │  │
│  └─────────┬────────────────────────────────────────────┬────┘  │
│            │                                              │       │
│            ▼                                              ▼       │
│  ┌──────────────────┐                         ┌──────────────┐   │
│  │  Skills package  │                         │  ./rebrand/  │   │
│  │  (.claude/skills)│──── reads inputs ──────▶│  (state)     │   │
│  │                  │                         │              │   │
│  │  25 SKILL.md     │──── writes outputs ────▶│  MD/JSON/    │   │
│  │                  │                         │  SVG/PNG/... │   │
│  └──────────────────┘                         └──────┬───────┘   │
│                                                       │           │
└───────────────────────────────────────────────────────┼───────────┘
                                                        │
                            ┌───────────────────────────┴───────┐
                            │    Target repo (user's code)       │
                            │                                    │
                            │  • apply-rebrand edits codigo      │
                            │  • gh PR create                    │
                            │  • deploy via user's CI            │
                            └────────────────────────────────────┘
```

### Components

| Component | Type | Responsibility |
| --- | --- | --- |
| **Orchestrator** (`rebrander.md`) | Agent prompt | Coordena sequencia, checkpoints, trata falhas |
| **Skills** (`.claude/skills/*/SKILL.md`) | Prompt instructions | Unidade atomica de trabalho — discovery, design, copy, code gen |
| **Filesystem state** (`./rebrand/`) | Directory tree | Source of truth — todos artefatos em arquivos |
| **Claude Code tools** | Built-in | TodoWrite, AskUserQuestion, Skill, Read/Write/Edit, Bash, WebFetch, WebSearch |
| **External binaries** | Host-provided | Playwright (screenshots/PDF), git/gh, curl, optional ImageMagick |
| **Provider integrations** | Generated CSVs/JSON | User-imported no Mailchimp, Klaviyo, GTM, Meta Ads Manager, etc. |

## 3. Skill contract (the unit interface)

Cada skill e um arquivo `SKILL.md` com frontmatter YAML + markdown body. O orchestrator invoca via `Skill("name")` no Claude Code; o runtime carrega o prompt + contexto.

### 3.1 Frontmatter schema

```yaml
---
name: <kebab-case-id>           # MUST match directory name
description: <1-3 sentences>    # Used by auto-activation + documentation
---
```

### 3.2 Required sections in body

```markdown
# <Skill Display Name>

> **Source & credit**: <citations pra tecnicas aplicadas>

## Purpose
<por que essa skill existe, o problema que resolve>

## Skip condition (optional)
<quando pular com no-op, ex: "Se regiao nao e BR, pula whatsapp-flow">

## Input
<lista de ./rebrand/NN-*.md arquivos lidos + outros inputs>

## Procedure
<passos numerados, template de output, heuristica de qualidade>

## Output
<artefatos produzidos: path + format>

## Quality bar
<checklist de qualidade obrigatorio>

## Handoff
<o que retornar pro orchestrator>
```

### 3.3 Dependency contract

Cada skill declara inputs como paths `./rebrand/NN-<slug>.md`. O **grafo de dependencias e implicito** mas validavel via smoke test:

```python
# Pseudocode do validador
for skill in skills:
    for input_path in skill.inputs:
        assert any(
            other_skill.outputs contains input_path
            for other_skill in skills
        ), f"Orphan: {skill} reads {input_path} but nobody produces it"
```

Implementacao real: script Python em `docs/validate-graph.py` (TODO — hoje e ad-hoc bash).

## 4. Artifact layout & numbering

### 4.1 Canonical numbering (01-24)

Numeros sao **stable IDs**, nao ordem de execucao. Alinhados aos 6 blocos do orchestrator:

| Block | Numbers | Skills |
| --- | --- | --- |
| **A — Identity** | 01-07 | discover-brand, competitor-research, naming, (site-audit, style-extract), conversion-angle, brand-direction, logo-design |
| **B — Infra** | 08-11 | legal-compliance, landing-page, lead-magnet, analytics-setup |
| **C — Paid** | 12-14 | ad-creatives, ugc-scripts, google-ads |
| **D — Follow-up** | 15-17 | email-sequences, whatsapp-flow, review-setup |
| **E — Organic** | 18-21 | social-presence, content-calendar, seo-content-plan, pr-kit |
| **F — Consolidation** | 22-24 | brand-book-pdf, launch-plan, apply-rebrand (before-after + apply-report share 24) |

Outputs: `./rebrand/NN-<slug>.md` (umbrella) + subdirectory `./rebrand/<slug>/` (assets).

### 4.2 Directory tree

```
./rebrand/
├─ 01-discovery.md
├─ 02-competitor-research.md
├─ 03-naming.md                       # if rename
├─ 04-audit.md                        # if site exists
├─ 04-current-tokens.json             # if site exists
├─ 04-current-tokens.md
├─ 05-conversion-angle.md
├─ 06-direction.md
├─ 06-new-tokens.<slug>.json          # per direcao
├─ 07-logo.md                         # if new logo
├─ 08-legal-compliance.md
├─ 09-landing-page.md
├─ 10-lead-magnet.md
├─ 11-analytics-setup.md
├─ 12-ad-creatives.md
├─ 13-ugc-scripts.md
├─ 14-google-ads.md
├─ 15-email-sequences.md
├─ 16-whatsapp-flow.md
├─ 17-review-setup.md
├─ 18-social-presence.md
├─ 19-content-calendar.md
├─ 20-seo-content-plan.md
├─ 21-pr-kit.md
├─ 22-brand-book.md
├─ 23-launch-plan.md
├─ 24-apply-report.md                 # after apply-rebrand
├─ 24-before-after.md                 # screenshots before/after
├─ .selected-name.json                # checkpoint state
├─ .selected-direction                # checkpoint state
├─ .selected-logo                     # checkpoint state
│
└─ <skill-name>/                      # asset subdirs
   ├─ competitors/                    # screenshots + tokens
   ├─ screenshots/                    # site-audit Playwright
   ├─ mockups/                        # brand-direction visuals
   ├─ logo/{concept-1..3, final}/     # SVG + PNG + favicon exports
   ├─ social/{ig, fb, li, x, tt, yt, wa, gbp}/
   ├─ ads/meta/                       # CSV import + creatives
   ├─ ugc/                            # scripts by format/duration
   ├─ google-ads/editor-import/       # CSVs
   ├─ email/{welcome, cart, reeng, post}/ + _imports/
   ├─ whatsapp/import/                # provider-specific JSONs
   ├─ reviews/widgets/                # embed HTML
   ├─ content-calendar/_imports/      # Notion/Airtable/Trello
   ├─ seo/                            # keyword research CSV, briefs
   ├─ press-kit/                      # release, media list, bio
   ├─ brand-book/                     # HTML + PDF + Figma library JSON
   ├─ lead-magnet/pdf/                # final PDF + LP
   ├─ landing-page/                   # standalone if no repo stack
   └─ launch-plan/copy/               # per-channel copy files
```

### 4.3 Checkpoint state files

`.selected-name.json`, `.selected-direction`, `.selected-logo` — arquivos escritos pelo orchestrator quando user aprova checkpoint. Skills downstream leem esses pra saber qual variante usar.

```json
// Example .selected-direction
{
  "selected_slug": "dark-clean",
  "tokens_file": "06-new-tokens.dark-clean.json",
  "approved_at": "2026-04-24T18:00:00Z",
  "approved_by": "user"
}
```

## 5. Execution model

### 5.1 Control flow

```
┌──────────────────┐
│   @rebrander     │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│ Kickoff (4 questions)│
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐       ┌───────────────────────┐
│  discover-brand      │──────▶│ 01-discovery.md       │
│  (FR-2, FR-11)       │       │  + Pipeline Activation │
└────────┬─────────────┘       └────────┬──────────────┘
         │                               │
         │        ┌──────────────────────┴─────┐
         │        │                             │
         ▼        ▼                             ▼
    ┌────────────────┐              ┌──────────────────┐
    │ competitor-    │              │ site-audit +     │
    │ research       │              │ style-extract    │
    │ (sequential)   │              │ (parallel if URL)│
    └────────┬───────┘              └────────┬─────────┘
             │                                │
             ▼                                │
    ┌────────────────┐                        │
    │ naming ⏸        │◀──────────────────────┘ (waits)
    │ (if rename)     │
    │ CHECKPOINT      │
    └────────┬───────┘
             │
             ▼
    ┌────────────────┐
    │ conversion-    │
    │ angle          │
    └────────┬───────┘
             │
             ▼
    ┌────────────────┐
    │ brand-direction│
    │ CHECKPOINT ⏸   │
    └────────┬───────┘
             │
             ▼
    ┌────────────────┐
    │ logo-design    │
    │ CHECKPOINT ⏸   │
    └────────┬───────┘
             │
             ▼
    [Block A complete]
             │
             ▼
    ... Blocks B-F run based on activation flags ...
             │
             ▼
    ┌────────────────┐
    │ apply-rebrand  │
    │ CHECKPOINT ⏸   │
    └────────┬───────┘
             │
             ▼
    ┌────────────────┐
    │ PR created     │
    └────────────────┘
```

### 5.2 Parallelism rules

Skills podem rodar **em paralelo** quando:
- Nao compartilham inputs
- Nao compartilham outputs
- Nao ha checkpoint entre elas

Na pratica:
- **Block A**: site-audit + style-extract paralelos (ambos leem so discovery/URL)
- **Block B**: legal + LP + lead-magnet + analytics paralelos (todos leem de blocos A)
- **Block C**: todos 3 paralelos
- **Block D**: todos 3 paralelos
- **Block E**: todos 4 paralelos
- **Block F**: brand-book + launch-plan paralelos; apply-rebrand serializa (edita codigo)

O orchestrator invoca em paralelo via multiple `Skill()` calls numa so mensagem.

### 5.3 Checkpoint protocol

Checkpoints sao **nao-negociaveis** — pipeline pausa ate user responder.

```
Skill completes → orchestrator calls AskUserQuestion({
  question: "Qual dos 10 nomes voce quer usar?"
  options: [...10 names with preview...]
})
→ User picks → orchestrator writes .selected-name.json → next skill
→ User picks "None" → orchestrator invokes `naming --regenerate` with feedback
```

Fase com checkpoint obrigatorio:
- **naming** (se renomear)
- **brand-direction** (sempre)
- **logo-design** (se logo novo)
- **apply-rebrand** (antes do PR)

## 6. Skill categories (architectural grouping)

### 6.1 Research skills (read-only, produce understanding)
- discover-brand, competitor-research, site-audit, style-extract
- Sem side effects no codigo
- Outputs: markdown + JSON

### 6.2 Synthesis skills (produce strategic direction)
- conversion-angle, brand-direction, naming
- Podem requerer checkpoints
- Outputs: markdown + visual mockups

### 6.3 Design skills (produce visual assets)
- logo-design, social-presence, brand-book-pdf
- Outputs: SVG + PNG + PDF + HTML

### 6.4 Copy/Content skills (produce textual assets)
- email-sequences, whatsapp-flow, content-calendar, seo-content-plan, pr-kit, launch-plan, ad-creatives, ugc-scripts, google-ads, lead-magnet
- Outputs: markdown + CSV + JSON imports

### 6.5 Infrastructure skills (produce deployable code)
- landing-page, analytics-setup, legal-compliance, apply-rebrand
- Outputs: TypeScript/TSX/HTML + env vars + routes

### 6.6 Meta skills (consolidation + coordinate)
- brand-book-pdf (aggregates), apply-rebrand (commits), launch-plan (orchestrates timeline)

## 7. Data flow examples

### 7.1 Token flow (identity → implementation)

```
brand-direction
  ↓ produces
06-new-tokens.<slug>.json
  {
    "color": { "brand_primary": "#050508", ... },
    "typography": { ... },
    "spacing": [...],
    ...
  }
  ↓ consumed by
  → apply-rebrand (writes to code: tailwind.config.js, CSS vars)
  → landing-page (same CSS vars in generated HTML)
  → brand-book-pdf (renders in PDF)
  → social-presence (templates use tokens)
  → lead-magnet (PDF uses tokens)
  → email-sequences (HTML templates use tokens)
```

Single source of truth → many consumers.

### 7.2 Voice flow (brand → copy)

```
conversion-angle → big_promise + 3 hooks + offer_stack + CTAs
  ↓ used in
  → landing-page (HERO headline, FAQ)
  → ad-creatives (27 combinations)
  → ugc-scripts (hooks as openers)
  → email-sequences (subject lines)
  → whatsapp-flow (welcome message)
  → google-ads (RSA headlines)
  → pr-kit (boilerplate copy)
  → content-calendar (post hooks)
```

### 7.3 Checkpoint gating

```
User approves direction "X"
  → .selected-direction = {slug: "X", tokens_file: "06-new-tokens.X.json"}
  → logo-design reads .selected-direction, gera logos compatriotas
  → User approves logo "Y"
  → .selected-logo = {concept: "Y", variants: [...]}
  → apply-rebrand reads both, injects no codigo
```

## 8. Error handling & edge cases

### 8.1 Skill failure modes

| Mode | Example | Handling |
| --- | --- | --- |
| **Missing input** | `conversion-angle` invoked sem `01-discovery.md` | Skill fails loud, orchestrator reruns upstream |
| **Empty output** | `competitor-research` encontra 0 concorrentes | Skill writes markdown com "nao encontrado", sinaliza risk no final |
| **External dependency** | Playwright sem Chromium | Skill pula com log, ofereces manual alternative |
| **Network error** | WebFetch 403 (antibot) | Try alternative (curl with UA), fallback to ask user |
| **Invalid user input** | User digita "outro" em checkpoint | Orchestrator aceita texto livre, re-roda skill com feedback |
| **LLM refuses** | Content flagged | Orchestrator reports, asks user to rephrase scope |

### 8.2 Idempotency

Re-rodar uma skill DEVE sobrescrever outputs com nova versao. Nao ha append. Artefatos `.selected-*.json` so mudam via checkpoint consciente.

### 8.3 Resumability

Se sessao Claude Code cai, `./rebrand/` persiste. User re-invoca `@rebrander`, orchestrator le estado, continua de onde parou (detecta qual fase faltou).

## 9. Extensibility

### 9.1 Adding a new skill

1. Criar `.claude/skills/<new-skill>/SKILL.md` com frontmatter + sections obrigatorias
2. Declarar inputs em markdown (paths `./rebrand/NN-*.md`)
3. Declarar outputs (umbrella MD + asset dir)
4. Se quer aparecer no fluxo padrao, adiciona entrada no orchestrator + discover-brand Pipeline Activation
5. Rodar validador de grafo pra garantir zero orphans

### 9.2 Plugin skills (v1.2 planned)

Skills custom em `.claude/skills-custom/` — nao versionadas no repo principal, user-specific. Orchestrator detecta e pergunta se quer ativar.

### 9.3 I18n (v1.2 planned)

Currently: single-language skills com detecao de idioma do user.
Future: `SKILL.md` estrutura multilingual via `description.pt-BR`, `description.en`, body dividido em secoes `## Procedure (PT)`, `## Procedure (EN)`.

## 10. Security & privacy

### 10.1 Secrets handling
- Env vars (Pixel ID, API keys) NUNCA entram em prompts de skill
- Skills geram codigo que refer `process.env.*`, nao hardcoded
- `analytics-setup` gera route handlers com token server-side-only

### 10.2 User data
- Sistema nao coleta telemetria por default
- Tudo em `./rebrand/` e local; user responsavel por .gitignore se sensivel
- `legal-compliance` placeholders visiveis (`<CNPJ>`, `<endereco>`) pra garantir substituicao

### 10.3 LLM prompt injection
- Inputs do user nao sao escapados — documented limitation
- Artefatos gerados passam por user review (checkpoint) antes de aplicacao final
- `apply-rebrand` checkpoint final previne PR malicioso

## 11. Testing strategy

### 11.1 Static validation (existing)
- Smoke test de grafo (implementado em ad-hoc Python) — zero orphans
- Frontmatter YAML validation (TODO — adicionar script)

### 11.2 Unit-style (TODO)
- Cada skill tem fixture de input + expected output shape
- Run subset de skills em CI com fake LLM response

### 11.3 Integration (TODO)
- End-to-end run com discovery fixture
- Verifica que todos artefatos esperados aparecem em `./rebrand/`

### 11.4 Real-world validation (ongoing)
- thiagaoai rebrand case — documentado em `example-run/` (planned)
- 3+ additional rebrands antes de v1.1

## 12. Deployment

### 12.1 Install

```bash
git clone https://github.com/Thiagaoai/Agent.rebranding-.git /tmp/rebrand
cp -r /tmp/rebrand/.claude .claude
cd your-project
claude  # opens Claude Code
```

Ou via submodule:
```bash
git submodule add https://github.com/Thiagaoai/Agent.rebranding-.git .rebrand-agent
ln -s .rebrand-agent/.claude .claude
```

### 12.2 Update

```bash
cd .rebrand-agent && git pull
```

Zero migration needed entre versions (skills sao backward-compatible por contrato).

### 12.3 Customize

User pode:
- Overwriting uma skill especifica (`.claude/skills/<name>/SKILL.md`) — sobe-escreve vendor
- Adicionar skills em `.claude/skills-custom/` (v1.2)
- Modificar orchestrator (`.claude/agents/rebrander.md`) pra workflow-especifico

## 13. Appendix — Tool usage per skill

| Skill | Tools primary | Tools secondary |
| --- | --- | --- |
| discover-brand | AskUserQuestion, Write | — |
| competitor-research | WebFetch, WebSearch, Write | Bash (curl) |
| naming | WebFetch (domain check), Write | Bash (whois) |
| site-audit | Bash (Playwright), Read, Write | WebFetch |
| style-extract | Bash (Playwright CSS extract), Write | — |
| conversion-angle | Write | WebSearch |
| brand-direction | Write, Bash (mockup gen) | — |
| logo-design | Write (SVG), Bash (PNG export) | ImageMagick |
| legal-compliance | Write | — |
| landing-page | Read (detect stack), Edit/Write, Bash (Lighthouse) | — |
| lead-magnet | Write, Bash (Playwright PDF) | — |
| analytics-setup | Read, Edit/Write | — |
| ad-creatives | Write (CSV) | Bash (image gen) |
| ugc-scripts | Write | — |
| google-ads | Write (CSV) | — |
| email-sequences | Write, Bash (HTML render) | — |
| whatsapp-flow | Write (JSON) | — |
| review-setup | Write | — |
| social-presence | Write, Bash (Playwright images) | — |
| content-calendar | Write (CSV) | — |
| seo-content-plan | Write (CSV) | WebFetch |
| pr-kit | Write | Bash (Playwright PDF) |
| brand-book-pdf | Write, Bash (Playwright PDF) | — |
| launch-plan | Write | — |
| apply-rebrand | Read, Edit/Write, Bash (git/gh) | — |

## 14. Change log

| Version | Date | Changes |
| --- | --- | --- |
| 1.0 | 2026-04-24 | Initial SDD. Post-refactor numbering 01-24, 6 blocks, 25 skills. |
