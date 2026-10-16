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

## MCP servers

`.mcp.json` is project scope — it is checked in, so every machine and every
web session that opens this repo sees the same server list. Currently:

| Server | Transport | URL |
|---|---|---|
| `firecrawl` | http | `https://mcp.firecrawl.dev/v2/mcp-oauth` |

Three things about it that are easy to get wrong:

**Approval is per machine, not per repo.** A `.mcp.json` server shows as
`⏸ Pending approval` until you approve it once in that checkout — run `claude`
in the repo and accept, or `claude mcp list` to see the state. Pulling the file
does not enable the server.

**Auth is per machine and never lands in the repo.** Firecrawl is OAuth:
`claude mcp login firecrawl` stores the token in `~/.claude/.credentials.json`,
outside the repo. That is the only supported path here.

**Never put a Firecrawl API key in `.mcp.json`.** The endpoint also accepts an
`x-firecrawl-api-key` header, and `claude mcp add -H` will happily write one into
this file — but **this repo is public**, so that key would be published to GitHub
the moment it is pushed. OAuth only. `.mcp.json` holds a URL and nothing else.

GitHub Pages runs Jekyll here (no `_config.yml`, no `.nojekyll`), and Jekyll drops
dotfiles from the build, so `.mcp.json` and `.claude/` are not served on the live
site — verified: `/.claude/agents/page-seo-auditor.md` returns 404 while
`/CLAUDE.md` returns 200. That protects the live site, not the repo. A public repo
still shows every tracked file.

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

| Agent | Item | Model | Reports |
|---|---|---|---|
| `page-seo-auditor` | one page | `haiku` | canonical, OG, Twitter, JSON-LD, sitemap membership |
| `page-nap-auditor` | one page | `haiku` | wrong business name, phone, city, domain |
| `page-link-auditor` | one page | `haiku` | internal `href` and `src` that do not resolve |
| `finding-verifier` | one finding | `sonnet` | `CONFIRMED` / `REFUTED` / `UNVERIFIABLE` |

### Which model, and why

Set by `model:` in each agent's frontmatter. These are aliases, not pinned
model IDs, so each agent follows whatever Haiku or Sonnet Claude Code currently
maps the alias to.

**The auditors run on Haiku because cache writes dominate fan-out cost.** Every
spawned agent starts cold: it writes its own prompt cache (system prompt, tool
definitions, its agent file), then writes every tool result it reads into that
cache too, and re-reads all of it on each later turn. A sweep pays that 51 times
over. Cache writes are billed at the model's input rate (plus a write premium),
so the model choice multiplies the biggest line item directly. The auditors'
judgment is already written into their files — a fixed checklist, a source of
truth to compare against, and dated exclusion lists — which is the kind of work
the smallest model does reliably.

**The verifier stays on Sonnet because it is the quality gate.** It is the last
step before Charlie sees a finding, its job is adversarial (default `REFUTED`,
decide whether a string is chrome or content), and it runs once per finding, not
once per page — a clean sweep spawns none. Auditor noise is affordable because
the verifier filters it. Verifier mistakes are not; they reach Charlie. If
confirmed findings start turning out wrong, raise the verifier a tier before
touching the auditors.

### Read scope: grep or line ranges, never a whole page

**No agent reads a whole HTML page.** Agents locate what they need with a grep
(line numbers, a few lines of context, or only-matching output) and read a line
range with `offset` and `limit` when they need more. This is the same cost as
above: whatever an agent reads is written to its cache and re-read every turn
after, and full pages run 300–1,100 lines when an audit needs a handful. Each
agent file spells out its own version — which tags to grep, which lines of
`seo-patch.js` to read — because agents do not inherit this file.

Two traps, also written into the agent files:

- **A grep that matches nothing has not proved absence.** Attribute order and
  quoting vary, so a strict pattern can miss a tag that is there. Before
  reporting anything missing, grep the bare token (`og:title`, `canonical`,
  `938-0480`) case-insensitively.
- **`index.html` lines 115 and 117 are minified inline CSS**, 23K and 5K
  characters (checked 2026-10-12). A grep that matches them returns the whole
  line. Use tight patterns or only-matching output.

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

## Arena

`.claude/arena/` scores every subagent run in dollars so setups compete and the
losers get fired. `python3 .claude/arena/arena.py board` prints the leaderboard
and writes `LEADERBOARD.md`; the script's docstring lists the other commands.

**The currency is API list price.** Net $/run = value earned − API cost. Cost
comes from each request's token usage at the prices in `rules.json`. Value
comes only from graded work. A pricier model pays its own premium; nothing
else penalizes it. How much quality is worth against spend is one dial,
`values_usd` in `rules.json`. Editing it rescores the whole ledger.

**Grading, strongest first:** Charlie's rulings (`rulings.jsonl`), the canaries
(`canaries/answers.json`), then `finding-verifier` verdicts. A `CLEAN` on a real
page is worth `clean` × that setup's hit rate on planted defects, because a
`CLEAN` cannot be checked on its own.

**Put both canaries in every sweep.** Add `.claude/arena/canaries/*.html` to each
auditor's item list. They are pages with planted defects (`hartsville-…`) and a
clean control (`darlington-…`). Without them a lazy `CLEAN` scores as well as a
careful one, and learnings cannot be compared like for like. They sit under
`.claude/`, so Jekyll does not serve them and `seo-patch.js` (root only) does not
touch them.

**Tag every verifier prompt.** First line: `RUN: <auditor agentId>#<finding
number>`. The agentId is in the Agent tool result. Untagged, the verdict cannot
be credited to the auditor or graded.

**Setups and challengers.** A setup is agent file commit + model. Commit a
definition change before running it; runs on uncommitted edits show `+dirty`.
A challenger is `.claude/agents/<job>--<variant>.md` and competes in `<job>`'s
league. Fire on a `FIRE` verdict: delete or rewrite that definition and commit.
Never fire on `ROOKIE` data.

**Learnings.** Agents propose one rule per run on a `LEARNING:` line and read
`learnings/<agent>.md` in their first turn. They never write it. `arena.py sync`
is the only writer, and the Stop hook runs it. One learning per agent is on
trial at a time, most-proposed first, so every before/after comparison measures
exactly one change. After 5 runs each side it is kept if net $/run did not drop
and retired if it did. A retired learning cannot come back. At 8 kept, the
weakest is evicted for the next one.

**The ledger lives in git.** Cloud containers lose their transcripts. The Stop
hook harvests this session's runs into `runs.jsonl` after each turn; commit it
with the work, along with `rulings.jsonl`, `learnings.jsonl`, `learnings/` and
`LEADERBOARD.md`.

**Rulings:** `arena.py rule <run>#<n> real|false "why"` for one finding,
`arena.py rule <run> good|bad "why"` for a whole run.
