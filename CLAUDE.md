# Florence SC Services — Priorities & Change Checklist

**This file is binding. Every change to this repo must be checked against it before commit.**

---

## Rule #0 — The site exists to make money

This website's only job is to **generate paying leads** (dumpster rental + junk
removal jobs in the Pee Dee region) or to **directly help generate them**.

For every change, the first question is: *Does this protect or grow revenue?*

- If a change **grows or protects** lead flow / rankings / conversions → proceed.
- If a change is **revenue-neutral** (cosmetics, refactors, compliance) → allowed,
  but it must **not** put any Protected Asset below at risk. State that it doesn't.
- If a change **could hurt** a Protected Asset → do not ship it without an explicit
  revenue reason and a rollback plan. Flag it to the owner first.

Revenue beats tidiness, "best practice," and personal preference. Always.

---

## Protected Assets — ranked by value to revenue

Higher = more money at stake. Guard the top of this list hardest.

1. **The money keyword: `dumpster rental florence sc`**
   - Owned by the pillar page **`/dumpster-rental-florence-sc.html`** — this is the
     single most valuable URL on the site.
   - It is the highest-impression commercial-intent query. Page 1 here = the business.
   - Baseline reference: it sat at **position ~9.5 (page 1)**, slid to **~19 (page 2)**
     in Jun 2026 after the homepage H1 was retargeted to the same exact-match phrase
     (self-inflicted cannibalization). **Target: back to page 1 (< 10), then hold.**
   - **No other page (especially the homepage `/`) may target this exact phrase** in
     its `<title>`, `<h1>`, or as internal-link anchor text. All internal links with
     "dumpster rental florence sc"-style anchors point to the pillar page.

2. **Commercial-intent local rankings (the rest of the lead engine)**
   - `dumpster rental` + each city (Darlington, Hartsville, Lake City, Marion, Dillon,
     Mullins, Sumter, Bishopville, Chesterfield, Kingstree, Latta), `dumpster rental
     near me`, size terms (20/30/40 yard), `junk removal florence sc` / city junk pages.
   - One page = one primary keyword. **No two pages compete for the same exact term**
     (keyword cannibalization is how we lost #1 above).

3. **Lead-capture infrastructure (the cash register)**
   - Every quote/contact form must submit successfully to the worker
     (`florence-crm-api`), including the required SMS-consent checkbox.
   - The phone number must be correct, visible above the fold, and click-to-call on
     mobile. A broken form or wrong number = zero revenue regardless of traffic.

4. **Conversion path & CTAs**
   - Quote CTA above the fold on every money page; transparent pricing; clear
     same-day / local trust signals and reviews. Don't bury or weaken CTAs.

5. **Indexability & crawl health (so Google can rank us)**
   - Correct self-canonical on every indexable page; intentional `noindex` only on
     true duplicates (and those stay out of `sitemap.xml`).
   - Every indexable page is in `sitemap.xml`; no accidental `noindex`; `robots.txt`
     keeps `/site-admin/` out and the sitemap referenced.
   - No broken internal links / 404s.

6. **Conversion tracking (so money is measurable)**
   - Google Ads conversion tracking + analytics must stay intact on all form pages.
     If we can't measure leads, we can't grow them.

7. **Local SEO trust: NAP, schema, reviews**
   - Name / Address / Phone identical everywhere; LocalBusiness + FAQ schema valid;
     real reviews kept as social proof.

8. **Performance & mobile**
   - Mobile-first; don't regress page speed / Core Web Vitals. Slow pages lose both
     rankings and conversions.

---

## Pre-change checklist (run before every commit)

- [ ] **Revenue:** Does this protect or grow leads/rankings/conversions? If neutral, confirm it risks nothing above.
- [ ] **Cannibalization:** No new page/title/H1/anchor competes with `dumpster rental florence sc` or any other page's primary term. Money-keyword anchors point to `/dumpster-rental-florence-sc.html`.
- [ ] **Indexability:** Canonical correct; not accidentally `noindex`; if indexable, it's in `sitemap.xml`.
- [ ] **Lead capture:** Forms still submit (with consent checkbox); phone number correct + click-to-call.
- [ ] **Tracking:** Google Ads / analytics conversion code intact on touched pages.
- [ ] **Links:** No broken internal links or 404s introduced.
- [ ] **Mobile/speed:** No layout break or speed regression on mobile.
- [ ] **NAP/schema:** Name/address/phone unchanged; schema still valid.

---

## Memory — update at the END of every session (do not skip)

**Canonical memory lives in git markdown in the `site-admin` repo, under
`memory/`** (cloned every session, so reliable even when MCP is down):
`memory/KNOWLEDGE.md`, `memory/SESSIONS.md`, `memory/ACHIEVEMENTS.md`. These
mirror the `florence-crm` D1 tables `knowledge` / `dev_session_log` /
`achievements` (`database_id 50e1fc12-682d-4d58-8506-93687a10dc36`).

- **Start of session:** read `site-admin/memory/SESSIONS.md` and `KNOWLEDGE.md`
  to recover context (fall back to the D1 tables if the repo isn't checked out).
- **End of any session that changed something, you MUST** update BOTH the
  matching markdown file and the matching D1 table:
  1. `memory/SESSIONS.md` + D1 `dev_session_log` — one session entry.
  2. `memory/KNOWLEDGE.md` + D1 `knowledge` — durable facts/decisions/gotchas.
  3. `memory/ACHIEVEMENTS.md` + D1 `achievements` — real milestones.

(This protocol lapsed once — `dev_session_log` stopped 2026-06-13 and `knowledge`
was empty until 2026-06-18. Don't let it lapse again.)

## How we verify (don't guess — measure)

Real ranking data lives in the `florence-crm` D1 database, refreshed daily by the
worker's `handleSeoSnapshot` cron:
- `seo_fix_snapshots` — daily position/impressions/clicks per tracked query.
- `seo_fixes` — queries being monitored, baselines, and the intended fix.
- `data_store` key `gsc_top_queries` — latest top-query window from Search Console.

Before claiming an SEO change worked, **check the snapshot trend**, not intuition.
