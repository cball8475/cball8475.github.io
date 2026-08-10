# Florence SC Services — site repo

Static lead site for `florencescservices.com`, served by GitHub Pages from the
repo root. No build step: the `.html` files in the repo are the files on the
live site, so a push to `main` is the deploy.

## Layout

- 41 pages at the repo root, 10 more under `blog/` — 51 in total.
- `seo-patch.js` — the head-metadata generator, and the source of truth for
  canonical URLs, OG data, the site origin and the business phone.
- `sitemap.xml` — what is indexed. `CNAME` — the live domain.
- `WORKFLOW.md` — how a new city or vertical site gets duplicated from this one,
  including the find-and-replace substitution table.
- `data/` — leads, pipeline, prospects and outreach state.

## Source of truth

Never decide any of these from the page you are editing. Pages are copies; the
copies are what drift.

| Fact | Lives in |
|---|---|
| Canonical path, OG title, OG description | `PAGE_META` in `seo-patch.js` |
| Site origin | `const SITE` in `seo-patch.js` |
| Business phone | `const PHONE_TEL` in `seo-patch.js` — `tel:+18439380480` |
| Live domain | `CNAME` |
| Indexed pages | `sitemap.xml` |

`seo-patch.js` **rewrites every HTML file in the repo when it runs.** Do not run
it to inspect anything. Read it.

## Agent Fleet

`.claude/agents/` holds read-only subagent definitions. Every page here came out
of the same template through a find-and-replace list, which makes per-page
checking wide and fully independent — 51 items, each answerable without seeing
any other. That is the shape fan-out is for.

### Doctrine

**Agents read, Charlie approves, the main session writes.** Every agent is
read-only: no edits, no commits, no network, and no running `seo-patch.js`. That
is what makes fan-out safe — read-only agents cannot overwrite each other, so
all 51 can run at once.

**One job per agent, scoped to one page.** Fan-out comes from spawning N agents,
not from handing one agent the file list.

**Every agent file restates the rules it depends on.** No agent inherits this
file. The read-only rule, the source-of-truth table and the link-resolution
rules are written into each definition even though that repeats them.

**Documented false positives live in the file.** This matters more here than
anywhere. A naive scan of this repo reported every root-absolute link as broken
(51 pages, zero real breaks), every form placeholder as a wrong phone number,
and every brand mention of "Florence" as a wrong city. The exclusion lists are
dated and derived from those runs.

**Structured output block at the end of every definition**, so 51 results read
side by side.

**Findings go through `finding-verifier`** before Charlie sees them. It defaults
to `REFUTED`.

### The agents

| Agent | Item | Reports |
|---|---|---|
| `page-seo-auditor` | one page | canonical, OG, Twitter, JSON-LD, sitemap membership |
| `page-nap-auditor` | one page | wrong business name, phone, city, domain |
| `page-link-auditor` | one page | internal `href` and `src` that do not resolve |
| `finding-verifier` | one finding | `CONFIRMED` / `REFUTED` / `UNVERIFIABLE` |

### When to fan out, when to single-thread

**Fan out** when the items are independent and nothing writes: a full-site sweep,
a batch of pages after a duplication, verification of a set of findings.

**Single-thread** when steps depend on each other, when the first result changes
the second, or when anything writes. Every edit to a page, every
`seo-patch.js` run, every commit stays sequential and stays in the main session.
Parallel writers to 51 files that share a template is the collision this fleet
exists to avoid.

### Watch the first minute

Read the opening of a run before stepping away — whether the agent understood
which page it had and read the source of truth rather than the page. Signals
worth catching early: work on a file nobody asked about, the same failed read
repeated, findings appearing after a grep that returned nothing, scope widening
past the one page it was given. A correction in the first minute is cheap; a
wrong finding found at review is not.

### Known-good, site-wide

Written into the agent files, repeated here because it is the thing a human
re-derives most often:

- `google1067d2b418ee6f0f.html` is a Google Search Console verification stub.
  No canonical, no OG, no JSON-LD, no sitemap entry — correct as it stands.
- `href="/foo.html"` is root-absolute and resolves to the repo root.
- `(843) 555-0123` and `(843) 555-1234` are form input placeholders.
- Third-party phone numbers on landfill guides are content, not NAP.
- "Florence" on any page is usually the brand name, not a locality claim.
- `index.html` sits in `sitemap.xml` as the bare origin, not by filename.
- Absence from `PAGE_META` is a script coverage gap, not a broken page.
