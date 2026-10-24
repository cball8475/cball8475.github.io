---
name: frontend-design
description: Visual and markup work on florencescservices.com — a new page or section, a component, CSS, header/nav/footer, CTAs, forms, layout or mobile fixes. The brand is already decided; this skill holds the tokens, the stylesheet cascade and its traps, the reusable components, and a screenshot review loop. Load it before writing or changing any HTML or CSS in this repo.
license: Adapted from the frontend-design skill in anthropics/skills (Apache-2.0, see LICENSE.txt). Modified for this repo, 2026-10-24.
---

# Front-end work on florencescservices.com

## The brief is fixed

The upstream version of this skill is for inventing a new visual identity. This
site already has one, on 47 pages, and every new page is a copy of the template.
Here the job is the opposite: **no new palette, typeface, radius, shadow or
spacing system.** A better page is one that does its job (get a quote request or
a call) more clearly, not one that looks different from its neighbors. When a
craft rule below conflicts with the established brand, the brand wins.

## Tokens

Use `var(--token)`, never a hex value. The values come from `/fsc-brand.css`,
which overrides the `:root` in `styles.css`.

| Token | Value | Use |
|---|---|---|
| `--green-dark` | `#1E3A52` | primary navy: header text, `.btn-call`, submit buttons, dark sections |
| `--green` | `#2E547A` | links, hover state of navy buttons, focus borders |
| `--green-light` / `--green-xlight` | `#E4EAF2` / `#F4F6FA` | tints, `.cta-section` background, hero background |
| `--amber` / `--amber-dark` | `#9a5a0a` / `#7c4a12` | `.btn-primary` (the quote CTA), `.eyebrow`, step numbers, check icons |
| `--dark` `--dark-2` `--dark-3` | `#1E3A52` `#162D41` `#111E2C` | headings, footer, CTA banner |
| `--text` / `--muted` | `#1e293b` / `#4A5A6E` | body / secondary text |
| `--radius` `--radius-sm` `--radius-lg` | 10 / 6 / 16px | from `styles.css` |
| `--font-display` | Barlow Condensed 600/700/800 | all headings, buttons |
| `--font-body` | Barlow 400/500/600 | everything else |
| `--max-w` / `--transition` | 1100px / 0.18s ease | container width, hover timing |

**Naming trap: every `--green*` token is navy.** `styles.css` still defines the
pre-rebrand green values (`--green: #16a34a`); `fsc-brand.css` overrides them.
A page that loads `styles.css` without `fsc-brand.css` renders green.

Contrast, computed 2026-10-24 (WCAG AA needs 4.5:1 for text under 24px, or under
18.66px bold):

| Pair | Ratio |
|---|---|
| white on `--green-dark` | 11.78 |
| white on `--green` | 7.88 |
| white on `--amber` | 5.47 |
| `--muted` on white | 7.05 |
| white on `#C4801C` | **3.26 — fails** |

`#C4801C` is hardcoded in the sticky mobile call button (`.fsc-sticky-call`) on 43
pages. Do not copy it into anything new. Compute the ratio for any new pair;
do not eyeball it.

## The cascade, and where a CSS change actually lands

On the 45 pages that load both files the order is: `styles.css` in the `<head>`
(relative link, `../styles.css` under `blog/`) → `/fsc-brand.css` later in the
`<head>` → an inline `<style>` in the `<body>` on 42 of them (the sticky-CTA
block). Later wins at equal specificity, so `fsc-brand.css` beats `styles.css`,
and the body block beats both. Only one page has an inline `<style>` between the
two links (checked 2026-10-24).

Exceptions, all checked 2026-10-24:

- **`index.html` loads neither file.** Both are minified and inlined in its
  `<head>` (around lines 114–117; those lines are 23K and 5K characters, so grep
  them with tight patterns). The inlined brand block is **not** a copy of
  `fsc-brand.css`: it has homepage-only rules and is longer. A site-wide CSS
  change has to be merged into it by hand. Never paste the file over it.
- **`partners.html` is off-template:** DM Serif Display and DM Sans, no
  `styles.css`, `fsc-brand.css` only. Known drift. Don't copy its fonts.
- **Stubs carry no styles and are left alone:** `florence-sc-dumpster-rental.html`,
  `blog/dillon-county-landfill-guide.html` and `blog/marion-county-landfill-guide.html`
  are meta-refresh redirects; `google1067d2b418ee6f0f.html` is Search Console
  verification.

Where a new rule goes:

- One page → an inline `<style>` placed after the `/fsc-brand.css` link, or the
  brand file will override it.
- Site-wide → append to `fsc-brand.css` (keep it minified, one line, note the
  change in its header comment), then merge the same rule into `index.html`.
- Not `styles.css`. `WORKFLOW.md` treats it as fixed outside a rebrand.

`fsc-brand.css` uses broad attribute selectors. `[class*="check"]` turns any class
containing "check" amber, `[class*="step-number"]` and `[class*="accent-bar"]`
restyle anything that matches. Name new classes so they don't collide, and
check the cascade in the screenshot, not in your head.

## Reuse the components that exist

Find a page that already uses the component and copy its markup
(`grep -l 'class="faq-item' *.html | head -1`, then read that block by line range).

- Buttons: `.btn` plus `.btn-primary` (amber, the quote CTA), `.btn-call` (navy,
  phone), `.btn-outline`, `.btn-outline-dark`, `.btn-white`; sizes `.btn-lg`,
  `.btn-sm`, `.btn-block`.
- Layout: `.container`, `.section`, `.section-alt`, `.section-header`, `.eyebrow`.
- Page top: `.page-hero`, `.breadcrumb`.
- Conversion: `.cta-banner` with `.cta-actions` (dark band), `.cta-section` with
  `.cta-btn` (light inline box, blog pages), `.fsc-sticky-cta` (mobile bar).
- Content: `.faq-list` / `.faq-item` / `.faq-q` / `.faq-a` / `.faq-chevron`,
  `.info-box`, `.check-list`.
- Forms: `.field`, `.field-err`, `.form-row-2`, `.req`.

The upstream skill calls all-caps eyebrows a templated tell. Here `.eyebrow` is the
established pattern (163 uses). Keep it where the template uses it; don't add new
kinds of decoration.

## Shared chrome is copied, not included

There is no build step and no include system. The header, nav, mobile menu, footer
and sticky CTA are pasted into about 46 pages, and the JavaScript behind them (nav
toggle, dropdowns, FAQ accordion) is inline on each page. `script.js` is not loaded
by any page (checked 2026-10-24); editing it changes nothing live.

So a chrome change is the same edit on every page: sequential, in the main session,
never by parallel agents. Afterwards, fan out `page-link-auditor` and
`page-nap-auditor` per `CLAUDE.md`.

Two things are never decided in the page you are editing:

- **Head metadata** (canonical, OG, Twitter) belongs to `PAGE_META` in
  `seo-patch.js`. Read the script; never run it, because it rewrites every HTML file.
- **The phone** is `PHONE_TEL` in `seo-patch.js`: `tel:+18439380480`, displayed as
  `(843) 938-0480`. CallRail swaps the number client-side, so the markup always
  carries the real one.

## Quality floor

Build to these without announcing them:

- Phone first. No horizontal overflow at 390px. Existing breakpoints are 600, 720,
  900 and 1024px; use those rather than new ones.
- Visible keyboard focus. `styles.css` has five `:focus-visible` rules; don't
  remove or override them.
- Reduced motion. Neither stylesheet has a `prefers-reduced-motion` rule today, so
  any motion beyond a hover color change ships with its own guard. At most one
  deliberate moment per page; no fade-up entrance on every section.
- Contrast at AA, computed (see the table above).
- Body text under 80 characters per line.
- Numbered markers only for a real sequence. A how-it-works process qualifies; a
  list of benefits does not.
- Images get `width`/`height`, `alt`, and `loading="lazy"` below the fold.
- Watch specificity between section padding and component padding. It is easy to
  write two rules that cancel each other.

## Copy

Brand voice: professional, smart, solution-oriented, genuine. A knowledgeable
partner, not a salesy vendor.

- **FSC coordinates and refers. It does not own trucks or deliver dumpsters.**
  Never write copy that says or implies otherwise; `about.html` carries the
  disclaimer.
- No invented prices, reviews, ratings or certifications.
- A CTA says what happens: "Request a Free Quote", "Call (843) 938-0480". The same
  action keeps the same name across the page.
- Sentence case, plain verbs, no filler. Form errors say what is wrong and how to
  fix it, without apologizing.

## Process

1. Name the change's job: which page, and what the visitor should do next.
2. Find the closest existing component and reuse its markup.
3. Edit, in the main session.
4. Screenshot at phone and desktop width:

   ```bash
   node .claude/skills/frontend-design/shoot.cjs about.html pricing.html --out "$SCRATCH"
   ```

   It serves the repo root locally, blocks analytics and CallRail, and writes
   `<page>-phone.png` (390px) and `<page>-desktop.png` (1280px). Each output line
   reports the web fonts that loaded, any horizontal overflow, and local 404s.
   Read both PNGs.
5. Critique against this file. Before finishing, remove one accessory.
6. If the change touched chrome or many pages, run the auditors per `CLAUDE.md`.

Expected in local shots, not defects in your change (as of 2026-10-24):

- The footer email reads `[email protected]` because Cloudflare's email-decode
  script is blocked.
- At 1280px the header nav wraps "Junk Removal" and "Service Area" onto two
  lines. This is pre-existing.
