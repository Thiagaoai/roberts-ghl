---
name: brand-direction
description: Phase 3 of the rebranding pipeline. Synthesizes the discovery brief and audit findings into 2-3 proposed new brand directions (palette + type system + voice + mood), presents them to the user, and waits for an approval choice before proceeding. This is the key checkpoint skill — do not skip. Use when ready to propose a visual/verbal direction for a rebrand.
---

# Brand Direction

> **Source & credit**: Aesthetic-family taxonomy and remix patterns adapted from [rohitg00/awesome-claude-design](https://github.com/rohitg00/awesome-claude-design). Brand-guidelines structure adapted from [anthropics/skills/brand-guidelines](https://github.com/anthropics/skills/blob/main/skills/brand-guidelines/SKILL.md) and [anthropics/claude-cookbooks/applying-brand-guidelines](https://github.com/anthropics/claude-cookbooks/blob/main/skills/custom_skills/applying-brand-guidelines/SKILL.md).

## Purpose

Turn `01-discovery.md` + `04-audit.md` + `04-current-tokens.json` into 2–3 **named, opinionated** new brand directions the user can pick between. Each direction is a full, coherent system — not a mood board of vibes.

## Hard rule

This is a **checkpoint skill**. You MUST end by calling `AskUserQuestion` asking the user to pick a direction (or request revisions). Do not write any tokens to the repo's real config yet — that's Phase 5. All output stays under `./rebrand/`.

## Inputs

- `./rebrand/01-discovery.md`
- `./rebrand/04-audit.md`
- `./rebrand/04-current-tokens.json`
- Optional competitor screenshots (already in `./rebrand/screenshots/competitors/` if provided in Phase 1)

## Procedure

### 1. Re-read the brief

Extract from discovery:
- Aesthetic family (Modern Minimal / Bold Playful / Editorial / Corporate Trust / Tech Futurist / Warm Handcrafted / Luxury Restrained)
- Emotional driver (confidence / belonging / status / safety / efficiency / joy)
- Non-negotiables

Extract from audit:
- Top 3 visual P0s
- SEO gaps (so the new direction can fix meta/OG in-flight)

### 2. Generate 2–3 directions

Each direction is a coherent system. Produce them in a spectrum — e.g. `safe → bold → experimental` — so the user can calibrate. If the discovery was very narrow (strong non-negotiables), 2 is fine; otherwise 3.

For each direction, define:

```yaml
direction_name: "<evocative name, e.g. 'Quiet Authority'>"
one_liner: "<12-word positioning>"
aesthetic_family: "Corporate Trust"
mood_references: ["https://stripe.com", "https://linear.app"]
palette:
  brand_primary: { hex: "#0A2540", role: "trust anchor, used on headers + primary CTAs" }
  accent:        { hex: "#00D4FF", role: "links, highlights, never on large surfaces" }
  surface:       { hex: "#FFFFFF" }
  surface_alt:   { hex: "#F6F9FC" }
  text:          { hex: "#0A2540" }
  text_muted:    { hex: "#425466" }
  success:       { hex: "#0FB981" }
  warning:       { hex: "#F5A623" }
  danger:        { hex: "#E5484D" }
typography:
  heading: { family: "Söhne, Inter, system-ui", weights: [600, 700], scale: [32, 40, 56, 72] }
  body:    { family: "Inter, system-ui",         weights: [400, 500], scale: [14, 16, 18], line_height: 1.6 }
  mono:    { family: "JetBrains Mono, ui-monospace" }
spacing: { base_unit_px: 4, scale: [4, 8, 12, 16, 24, 32, 48, 64, 96] }
radius:  { sm: 4, md: 8, lg: 16, pill: 9999 }
shadow:
  sm: "0 1px 2px rgba(10,37,64,0.06)"
  md: "0 4px 12px rgba(10,37,64,0.08)"
  lg: "0 24px 48px rgba(10,37,64,0.12)"
voice:
  principles:
    - "Plain words, precise claims."
    - "Lead with the outcome, not the feature."
    - "One verb per CTA."
  swap_examples:
    - from: "Welcome to our platform"
      to:   "Cut reconciliation time in half."
    - from: "Learn More"
      to:   "See how it works"
imagery: "Photography: neutral backgrounds, candid B-roll, real people not stock. Illustration: line-work only, brand_primary stroke on surface_alt fill."
hero_mockup_prompt: "Single-sentence description of the redesigned home hero for a generated mockup."
```

### 3. Generate visual mockups

For each direction, produce at least one static HTML mockup of the redesigned home hero so the user can see it, not just read specs:

- Write `./rebrand/mockups/<direction-slug>/index.html` — a self-contained HTML file using the direction's tokens inline.
- Include: nav, hero headline + subhead + CTA, a feature row. That's enough to convey the system.
- Also produce a rendered PNG at `1440x900` using Playwright: `./rebrand/mockups/<direction-slug>/hero-desktop.png`.

Keep mockups honest — use real-looking content from the discovery brief, not "Lorem ipsum."

### 4. Write the direction doc

Output: `./rebrand/06-direction.md`

```markdown
# Brand directions — <company>
_Generated <date> by the `brand-direction` skill_

_Three candidates, calibrated safe → bold → experimental. Each is a complete system; pick one or ask for a remix._

## How to read this
Each direction ships with: a named point of view, a full token set, voice principles with before/after copy swaps, and a rendered hero mockup you can open inline.

---

## Direction 1 — Quiet Authority  _(safe)_
<yaml block above, rendered as markdown sections>

![hero mockup](./mockups/quiet-authority/hero-desktop.png)

**Why this fits the brief**: …  
**Trade-offs**: …

---

## Direction 2 — <name>  _(bold)_
…

---

## Direction 3 — <name>  _(experimental)_
…
```

And emit a machine-readable version: `./rebrand/03-new-tokens.<slug>.json` per direction, in the same shape as `04-current-tokens.json`. Phase 5 will consume whichever one the user picks.

### 5. Checkpoint — wait for approval

Call `AskUserQuestion` with:

- Question: "Which direction should we apply to the site?"
- Options: one per direction, each labeled with the direction name and its one-liner; include a "None of these — tell me what to change" option.

If the user picks a direction → write its slug to `./rebrand/.selected-direction` and hand back to the orchestrator.

If the user picks "None" → ask a follow-up (what to change), regenerate affected directions, re-checkpoint. Do not escape the loop without explicit approval.

## Quality bar

- Each direction must be **genuinely different** — if Directions 2 and 3 could swap names without anyone noticing, you've failed.
- Respect every non-negotiable from discovery. If "navy must stay primary," every direction uses navy in the `brand_primary` slot — only the accent, type, and voice move.
- The mockup is what sells the direction. Invest time there.
- Never output more than 3 directions. Choice paralysis kills rebrands.

## Handoff

Return:
- Path to `06-direction.md`
- The user's selected slug
- One-sentence rationale the orchestrator can echo to the user ("You chose *Quiet Authority* — proceeding to generate assets and apply code changes.")
