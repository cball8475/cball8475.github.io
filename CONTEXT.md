# Project Context — florencescservices.com

Static site served via **GitHub Pages** from `cball8475/cball8475.github.io`
(custom domain in `CNAME` → `florencescservices.com`). Deploys automatically
on every push to `main` (workflow: *pages build and deployment*). Companion
repo: `cball8475/site-admin`.

---

## Google Search Console (GSC) — indexing strategy

The site intentionally **de-indexes duplicate / consolidated pages** using
`noindex` + canonical, rather than deleting them. Because of that, several
GSC "Page indexing" reports are **expected/by-design**, not errors.

### The golden rule
> Any page marked `noindex` must **NOT** appear in `sitemap.xml`.
> Any page **in** `sitemap.xml` must be indexable (no `noindex`).

Listing a `noindex` page in the sitemap is contradictory and triggers GSC's
**"Excluded by 'noindex' tag"** report. Keep these two in sync.

### Current `noindex` pages (all correctly excluded from sitemap)
| Page | Why noindex | Canonical / target |
| --- | --- | --- |
| `blog/florence-sc-dumpster-permit-guide.html` | consolidated | → `blog/dumpster-rental-permits-south-carolina.html` |
| `florence-sc-dumpster-rental.html` | duplicate of primary Florence page | → `dumpster-rental-florence-sc.html` |
| `blog/dillon-county-landfill-guide.html` | meta-refresh redirect stub | → `/dillon-county-landfill-guide.html` |
| `blog/marion-county-landfill-guide.html` | meta-refresh redirect stub | → `/marion-county-landfill-guide.html` |
| `partners.html` | private/partner page (`noindex, nofollow`) | n/a |

The `/blog/*-landfill-guide.html` files are tiny "this page has moved" stubs
(`<meta http-equiv="refresh">` + `noindex`). The real content lives at the
**root** versions, which are the ones in the sitemap.

---

## Session log — 2026-06-15 (GSC Coverage drilldown)

Reviewed three GSC Coverage drilldown exports. Findings:

1. **"Excluded by 'noindex' tag"** → `/blog/florence-sc-dumpster-permit-guide.html`
   — **REAL fix.** Page was `noindex` + canonicalised but **still listed in
   `sitemap.xml`**. Removed its `<url>` entry. (PR #3, merged to `main`,
   commit `66b576d`, deployed successfully.)
2. **"Not found (404)"** → `/blog/dillon-county-landfill-guide.html`
   — **Stale.** Redirect stub now serves 200 and isn't in the sitemap.
   No code change; just **Validate Fix** in GSC.
3. **"Redirect error"** → `/florence-sc-dumpster-rental.html`
   — **Stale.** Page no longer redirects; it's `noindex` + canonical to the
   primary page. No code change; just **Validate Fix** in GSC.

Verified across the whole repo: all 5 `noindex` pages are absent from the
sitemap. No remaining conflicts.

### Remaining manual steps (in GSC, no code)
- [ ] Resubmit `sitemap.xml` (Sitemaps → re-enter `sitemap.xml`).
- [ ] Click **Validate Fix** on all three issues above.

Sitemap URL: **https://florencescservices.com/sitemap.xml**
(declared in `robots.txt`).

---

## Environment / network notes (Claude Code on the web)

- The live domain `florencescservices.com` is **not** on this environment's
  network egress allowlist, so sessions can't `curl` the live site directly.
  Deployed content was verified through GitHub (`raw.githubusercontent.com` /
  API) instead, which reflects exactly what Pages serves.
- To allow live-URL fetches in **future** sessions: edit the environment
  (cloud icon at claude.ai/code) → **Network access** → **Custom** → add
  `florencescservices.com` and `www.florencescservices.com` to **Allowed
  domains**, keep "Also include default list of common package managers"
  checked. Changes apply only to **newly started** sessions.
- Docs: https://code.claude.com/docs/en/claude-code-on-the-web#network-access

---

## Useful files
- `sitemap.xml` — keep in sync with the `noindex` rule above.
- `robots.txt` — `Disallow: /site-admin/`; points to the sitemap.
- `seo-patch.js` — **build-time** script that injects canonical/OG/geo tags and
  the sticky CTA into pages (not a client-side redirector).
- `WORKFLOW.md`, `DIRECTORY-COPY.md`, `EXISTING-PAGE-MODIFICATIONS.txt` — prior
  process notes.
