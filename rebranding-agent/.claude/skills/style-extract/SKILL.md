---
name: style-extract
description: Phase 2b of the rebranding pipeline. Extracts the live website's design tokens — color palette, type stack, spacing scale, border radii, shadows — into a structured JSON style guide. Runs in parallel with site-audit. Use when you need a machine-readable snapshot of a site's current visual system, either for rebranding or to document an existing design system.
---

# Style Extract

> **Source & credit**: Adapted from [ivansong1981/ui-style-extractor](https://github.com/ivansong1981/ui-style-extractor/blob/main/ui-style-extractor/SKILL.md), which produces a website style guide plus app UI style guide from a live URL. Streamlined here to produce a single `current-tokens.json` the apply-rebrand skill can diff against.

## Purpose

The audit tells you **what's wrong**. This tells you **what's there** — in tokens, not vibes. When Phase 5 has to rewrite `tailwind.config.js` or `:root` CSS vars, it needs a clean before/after delta.

## When to run

- In parallel with `site-audit` during Phase 2 of the rebrand pipeline.
- Standalone if a user wants "document our current design tokens."

## Inputs

- `url` — the live URL *(required)*
- `rendered-html-dir` — optional, defaults to `./rebrand/.tmp/` (where `site-audit` dumps `<page>.html`). If `site-audit` already ran, reuse its captures.

## Prerequisites

Playwright (same install as `site-audit`). Reuse its dumped HTML / computed styles if available — don't re-visit unless you must.

## Procedure

### 1. Collect computed styles

If fresh: write `./rebrand/.tmp/extract.js` that:

- Opens each page with Playwright.
- For a curated selector set (`body`, `h1`–`h6`, `p`, `a`, `button`, `input`, `.btn`, `[class*="card"]`, etc.), calls `getComputedStyle` and records:
  - `color`, `background-color`, `border-color`
  - `font-family`, `font-size`, `font-weight`, `line-height`, `letter-spacing`
  - `padding`, `margin`, `gap`
  - `border-radius`, `box-shadow`
- Dumps result to `./rebrand/.tmp/<page>.computed.json`.

### 2. Derive tokens

Aggregate across pages and cluster:

**Colors**
- Collect every unique color seen. Convert to hex.
- Cluster near-duplicates (ΔE ≤ 5 in LAB space, or just group by rounded HSL if you don't want a library).
- Label roles: the most-used color on primary CTAs → `brand-primary`; the most-used bg → `surface`; text color → `text`; etc.
- Flag any color with fewer than 3 occurrences as "noise / candidate for removal."

**Typography**
- Unique `font-family` stacks → `font.heading`, `font.body`, `font.mono`.
- Font-size frequency histogram → derive a scale (e.g. `12, 14, 16, 18, 24, 32, 48`). Flag sizes used only once as outliers.
- Weight set and line-height range.

**Spacing**
- Collect all padding/margin/gap values.
- Round to nearest multiple of 4 (or 8) and produce a scale. Report the "base unit" (usually 4 or 8).

**Radii & shadows**
- Unique values, each with a usage count.

### 3. Write the tokens file

Output: `./rebrand/04-current-tokens.json`

```json
{
  "meta": {
    "url": "https://example.com",
    "extracted_at": "2026-04-23T...",
    "pages_sampled": ["/", "/pricing", "/about"]
  },
  "color": {
    "brand_primary": { "hex": "#0B5FFF", "usage_count": 142, "role_evidence": "primary CTA bg on 5 pages" },
    "surface":        { "hex": "#FFFFFF", "usage_count": 301 },
    "text":           { "hex": "#111827", "usage_count": 278 },
    "_noise":         [ { "hex": "#F3E8FF", "usage_count": 1 } ]
  },
  "typography": {
    "font": {
      "heading": "Inter, system-ui, sans-serif",
      "body":    "Inter, system-ui, sans-serif",
      "mono":    "ui-monospace, SFMono-Regular, monospace"
    },
    "size_scale_px": [12, 14, 16, 18, 24, 32, 48],
    "size_outliers_px": [17, 23],
    "weights": [400, 500, 700],
    "line_heights": { "tight": 1.2, "normal": 1.5, "loose": 1.75 }
  },
  "spacing": {
    "base_unit_px": 4,
    "scale_px": [4, 8, 12, 16, 24, 32, 48, 64]
  },
  "radius_px": [0, 4, 8, 12, 9999],
  "shadow": [
    { "css": "0 1px 2px rgba(0,0,0,0.05)", "usage_count": 23 },
    { "css": "0 10px 25px rgba(0,0,0,0.1)", "usage_count": 4 }
  ]
}
```

### 4. Write a short readable companion

Also emit `./rebrand/04-current-tokens.md` — a human-readable view of the same data with color swatches (use `![swatch](https://via.placeholder.com/40/<hex>/<hex>.png)` or similar) and a one-paragraph summary: "The current system uses 14 distinct colors (target: 6–8), a single font family, and an inconsistent spacing scale."

## Quality bar

- Don't invent roles. If you can't confidently label a color's role, call it `accent_<hex>` rather than guessing.
- The `_noise` and `size_outliers` fields matter — they're Phase 5's cleanup checklist.
- If the site uses Tailwind, CSS vars, or a design-tokens file already (check for `tailwind.config.*`, `:root { --… }` in stylesheets, `tokens.json`), mention it in the `meta` block; Phase 5 will edit tokens at the source instead of inline.

## Handoff

Return the path to `04-current-tokens.json`, the one-paragraph summary, and the count of color/size/spacing outliers (a quick health metric the user will want).
