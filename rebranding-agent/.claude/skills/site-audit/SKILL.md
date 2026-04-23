---
name: site-audit
description: Phase 2 of the rebranding pipeline. Uses Playwright to screenshot a live website at mobile/tablet/desktop breakpoints, then uses Claude vision to critique visual hierarchy, color harmony, typography, copy tone, CTA clarity, and accessibility signals. Also scrapes meta tags, Open Graph, and structured data for an SEO audit. Produces a severity-ranked audit report. Use when the user wants a website critique or as part of a full rebrand.
---

# Site Audit

> **Source & credit**: Design-review critique pattern adapted from [garrytan/gstack design-review](https://github.com/garrytan/gstack/blob/main/design-review/SKILL.md). Playwright usage adapted from [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill). SEO checks adapted from [coreyhaines31/marketingskills seo-audit](https://github.com/coreyhaines31/marketingskills/blob/main/skills/seo-audit/SKILL.md).

## Purpose

Produce an honest, specific, severity-ranked critique of the current website — **visual**, **UX/accessibility**, **copy**, and **SEO** — that Phase 3 (brand-direction) and Phase 5 (apply-rebrand) can act on.

## Inputs

- `url` — the live URL to audit *(required)*
- `pages` — list of additional paths to audit beyond `/` (default: `["/pricing", "/about", "/contact"]` if they exist)
- `discovery` — path to `./rebrand/01-discovery.md` (so the critique is judged against the user's actual goals, not generic best-practice)

## Prerequisites

Playwright must be installed. First run in a project:

```bash
npm init -y 2>/dev/null || true
npm install --save-dev playwright
npx playwright install chromium
```

If the target repo already has Playwright, reuse it.

## Procedure

### 1. Screenshot capture

Write a throwaway Node script at `./rebrand/.tmp/capture.js` that:

- Launches Chromium headless.
- For each page in the input list:
  - Visits `${url}${path}`.
  - Screenshots at 3 breakpoints: `375x812` (mobile), `768x1024` (tablet), `1440x900` (desktop).
  - Also captures a **full-page** desktop screenshot.
  - Saves to `./rebrand/screenshots/<page-slug>-<breakpoint>.png`.
- Dumps `document.documentElement.outerHTML` to `./rebrand/.tmp/<page-slug>.html` for later parsing.
- Extracts meta tags (`title`, `description`, `og:*`, `twitter:*`, `<link rel="canonical">`, `<script type="application/ld+json">`) into `./rebrand/.tmp/<page-slug>.meta.json`.

Run the script with `Bash`: `node ./rebrand/.tmp/capture.js`.

### 2. Visual critique via Claude vision

For each desktop full-page screenshot, use the `Read` tool to load the PNG (Claude Code reads images visually) and analyze. For each page, rate 0–10 on each dimension and write **2–3 sentences of specific evidence** — never generic.

Dimensions:

| Dimension | What a 10 looks like |
| --- | --- |
| **Visual hierarchy** | Eye lands on the primary CTA within 2 seconds; size/weight/color contrast guide reading order. |
| **Color harmony** | Palette feels intentional — 1 brand color, 1 accent, neutral base, enough contrast for WCAG AA. |
| **Typography** | Max 2 families; clear size scale; line-length 45–75ch for body; weights used purposefully. |
| **Spacing / rhythm** | Consistent spacing scale; sections breathe; no cramped or floating elements. |
| **Imagery** | Photos / illustrations feel on-brand, consistent style, not stock-y unless intentional. |
| **Copy clarity** | Headline states value in ≤12 words; no jargon the audience doesn't already use; CTAs are verbs. |
| **CTA clarity** | Single primary CTA per section; action-oriented label; visually dominant. |
| **Mobile experience** | Nothing overflows; tap targets ≥44px; font ≥16px; CTAs reachable with thumb. |
| **Accessibility signals** | Alt text present, heading order (h1→h2→h3) is logical, focus states visible, contrast ≥ 4.5:1. |

### 3. SEO / metadata scan

For each page, check:

- `<title>` — present, 30–60 chars, unique.
- `<meta name="description">` — present, 120–160 chars.
- `og:title`, `og:description`, `og:image`, `og:url` — present.
- `twitter:card` — `summary_large_image` recommended.
- Canonical tag present.
- One `<h1>` per page, heading order logical.
- `lang` attribute on `<html>`.
- JSON-LD structured data present if applicable (Organization / Product / Article).
- Image `alt` coverage — % of `<img>` tags with non-empty `alt`.

### 4. Write the audit report

Output: `./rebrand/02-audit.md` with this structure:

```markdown
# Site Audit — <url>
_Generated <date> by the `site-audit` skill_

## Scorecard
| Page | Visual | Typo | Spacing | Copy | Mobile | A11y | SEO | **Total /70** |
| --- | ---:| ---:| ---:| ---:| ---:| ---:| ---:| ---:|
| /    | 6 | 5 | 7 | 4 | 8 | 5 | 3 | **38** |
| /pricing | … |

## Findings (severity-ranked)

### 🔴 P0 — Blockers
- [page] Specific problem. Evidence: "<quote or screenshot region>". Suggested fix.

### 🟠 P1 — High impact
- …

### 🟡 P2 — Polish
- …

## SEO / metadata
_Table: page → missing tags → recommended values._

## Accessibility quick wins
_Bullet list with WCAG references._

## What to carry into Phase 3
_3–5 bullets the `brand-direction` skill should act on._
```

## Quality bar

- **Be specific.** "Hero is weak" is useless. "Hero headline 'Welcome' is 1 word and offers no value prop; replace with a benefit-oriented line under 12 words" is useful.
- **Tie findings back to the discovery brief.** If the brand goal is "Corporate Trust" and the hero uses Comic Sans, rate that as P0 even if it's typographically fine in isolation.
- **No AI slop.** Skip "embrace modern design trends." Every bullet must be directly about what you see on screen.
- **Screenshots in the report.** Reference `screenshots/<slug>-desktop.png` in markdown so the user can open them inline.

## Handoff

Return to orchestrator with:
- Path to `02-audit.md`
- Path to `screenshots/`
- One-line overall verdict (e.g. "Visually tired but structurally sound — palette and typography are the highest-leverage fixes.")
