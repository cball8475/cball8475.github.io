# Agent Arena — Leaderboard

Generated 2026-10-16 20:57 UTC by `python3 .claude/arena/arena.py board`. 249 runs, $5.66 at API list price.

Net $/run = value earned − API cost. Churn = share of a run's cost above the cheapest correct run of the same job on the same item. Values and prices live in `rules.json`; editing them rescores everything.

## Orchestrator (main session)

One row per main model · effort · CLAUDE.md version. A session is scored as one job: what its team earned minus everything the job cost, main model included, per graded item. Main share = main-model cost from first spawn to last result. Start-up share = share of agent spend that went to cold starts (over-division shows up here). Hoarding = share of cost spent on main-model turns that only read (under-division).

| Setup | Sessions | Items | Net $/item | Cost $/item | Main share | Start-up share | Hoarding | Badges | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| opus-5-5 · xhigh · `CLAUDE.md@25bce72` | 2 | 233 | $0.0976 | $0.0502 | 53% | 36% | 0% | 🏅 Best Division | **ROOKIE** |
| opus-5-5 · xhigh · `CLAUDE.md@455ef33` | 1 | 15 | $-0.0401 | $0.4990 | 97% | 35% | 2% | – | **ROOKIE** |

## finding-verifier

| Setup | Model | Runs | Net $/run | Cost $/run | Churn | Precision | Planted found | Verdicts right | Badges | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `finding-verifier@455ef33` | sonnet-5-5 | 2 | $0.1794 | $0.0706 | – | – | – | 100% of 2 | – | **ROOKIE** |
| `finding-verifier@25bce72` | sonnet-5-5 | 74 | $0.1392 | $0.0579 | – | – | – | 90% of 10 | 🧹 Zero Churn | **KEEP** |

## general-purpose

| Setup | Model | Runs | Net $/run | Cost $/run | Churn | Precision | Planted found | Verdicts right | Badges | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `general-purpose@builtin` | haiku-5-5 | 1 | $-0.0653 | $0.0653 | – | – | – | – | – | **ROOKIE** |

## page-link-auditor

| Setup | Model | Runs | Net $/run | Cost $/run | Churn | Precision | Planted found | Verdicts right | Badges | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `page-link-auditor@455ef33` | haiku-5-5 | 4 | $0.5470 | $0.0030 | 9% | 100% of 4 | 100% of 4 | – | 🐤 Canary Hunter 🏆 Course Record ×2 | **ROOKIE** |
| `page-link-auditor@25bce72` | haiku-5-5 | 53 | $0.0877 | $0.0053 | 17% | 100% of 2 | 100% of 2 | – | – | **KEEP** |

## page-nap-auditor

| Setup | Model | Runs | Net $/run | Cost $/run | Churn | Precision | Planted found | Verdicts right | Badges | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `page-nap-auditor@455ef33` | haiku-5-5 | 4 | $0.4924 | $0.0076 | 40% | 54% of 13 | 100% of 4 | – | 🐤 Canary Hunter | **ROOKIE** |
| `page-nap-auditor@25bce72` | haiku-5-5 | 53 | $0.1603 | $0.0090 | – | 86% of 14 | 100% of 2 | – | – | **KEEP** |

## page-seo-auditor

| Setup | Model | Runs | Net $/run | Cost $/run | Churn | Precision | Planted found | Verdicts right | Badges | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `page-seo-auditor@455ef33` | haiku-5-5 | 5 | $0.4321 | $0.0046 | 16% | 71% of 7 | 100% of 4 | – | 🐤 Canary Hunter 🧹 Zero Churn 🏆 Course Record ×1 | **KEEP** |
| `page-seo-auditor@25bce72` | haiku-5-5 | 53 | $0.1058 | $0.0065 | 0% | 46% of 57 | 100% of 2 | – | 🧹 Zero Churn 🏆 Course Record ×2 🔁 False Alarm | **FIRE** |

## Learnings — before vs after

| Agent | ID | Learning | Status | Runs before → after | Net $/run before → after | Δ | Call |
|---|---|---|---|---|---|---:|---|
| page-seo-auditor | L1 | In the first turn, grep `application/ld+json` and `</script>` together, or use -A sized to | trial | 58 → 0 (all) | $0.1339 → ? | ? | NO SIGNAL ⚠ definition or model changed |
| page-nap-auditor | L54 | On a page whose filename names no city, set PAGE-CITY to none and test locality with one g | trial | 57 → 0 (all) | $0.1836 → ? | ? | NO SIGNAL ⚠ definition or model changed |
| page-link-auditor | L107 | Same-domain absolute URLs (https://florencescservices.com/<path>, including canonical href | trial | 57 → 0 (all) | $0.1199 → ? | ? | NO SIGNAL ⚠ definition or model changed |
| finding-verifier | L159 | For a wrong-city finding on a head meta tag, grep that tag across all *.html to see the pe | trial | 76 → 0 (all) | $0.1402 → ? | ? | NO SIGNAL ⚠ definition or model changed |

Waiting for a trial slot (most-proposed first):

- page-seo-auditor L2 ×1: Before hand-parsing an application/ld+json block, run one grep over the page for non-ASCII whitespace and smart quotes, 
- page-seo-auditor L3 ×1: When checking sitemap membership, grep the filename with -i together with the comment markers "<!--|-->" in one call, be
- page-seo-auditor L4 ×1: In the first turn, grep the page for `<script|</script>` with -n in the same batch as the ld+json grep, so the JSON-LD b
- page-seo-auditor L5 ×1: When a page's og:title or og:description matches its own JSON-LD (Article headline or description), treat that as no evi
- page-seo-auditor L6 ×1: When a page carries a "SEO Patch:" marker comment, check the tag that follows it before judging the head; seo-patch.js l
- page-seo-auditor L7 ×1: In the first grep batch, add `(?i)</?script` on the target page next to the ld+json grep, so the JSON-LD start and end l
- page-seo-auditor L8 ×1: When grepping the sitemap for a filename, also grep `<!--|-->` -n in the same batch, so a hit inside a comment block is 
- page-seo-auditor L9 ×1: When a page is missing from sitemap.xml, grep the sitemap case-insensitively for "<!--" with line numbers before reporti
- page-seo-auditor L10 ×1: In the first turn, add a case-insensitive `</script>` grep to the head-tag grep, so the JSON-LD Read gets its offset and
- page-seo-auditor L11 ×1: In the first grep batch, add `<!--|-->` to the sitemap.xml and page greps. A sitemap entry inside a comment block is not
- page-seo-auditor L12 ×1: For a page audit, put `<!--|-->` and `</script>` in the first grep batch with the tag greps (-n), so the JSON-LD span an
- page-seo-auditor L13 ×1: When grepping sitemap.xml for a filename, use the exact filename with no -C context (output_mode content or files_with_m
- page-seo-auditor L14 ×1: Once a first-turn grep gives the line of an `application/ld+json` opener, Read from that line with a limit near 50 direc
- page-seo-auditor L15 ×1: Before counting a sitemap `<loc>` as indexed, grep sitemap.xml for `<!--|-->` and confirm the entry's line is outside ev
- page-seo-auditor L16 ×1: Grep a page's filename only in named files (sitemap.xml, seo-patch.js), never repo-wide; a repo-wide grep returns .claud
- page-seo-auditor L17 ×1: Find the JSON-LD block's closing line with a Grep for `</script>` using -n and head_limit 0, then Read that span in one 
- page-seo-auditor L18 ×1: To check that a page's JSON-LD parses, Read the block from its `ld+json` line (about 50 lines) rather than grepping `</s
- page-seo-auditor L19 ×1: In the first grep batch, include </script> (-n -o) alongside ld\+json, then Read the JSON-LD span starting at the opener
- page-seo-auditor L20 ×1: For the sitemap check, also grep sitemap.xml for "<!--|-->" and confirm the page's <loc> line falls outside every commen
- page-seo-auditor L21 ×1: When a tag grep prints "[Omitted long matching line]", the tag sits on a one-line script (the JSON-LD blocks on this tem
- page-seo-auditor L22 ×1: In the first grep batch, also grep seo-patch.js for the bare slug 'junk-removal' case-insensitive next to the '.html' fi
- page-seo-auditor L23 ×1: Put a grep for `</script>` (or `ld\+json|</script>`) in the same first batch as the tag greps, so the ld+json Read is on
- page-seo-auditor L24 ×1: When PAGE_META has an entry, grep seo-patch.js once for `ogDesc`: lines 125 and 133 write og:description and twitter:des
- page-seo-auditor L25 ×1: To check JSON-LD, grep "ld\+json|</script>" in the same turn as the tag greps to get the block's exact start and end lin
- page-seo-auditor L26 ×1: When grepping the page for the JSON-LD block, put `</script>` in the same pattern as `ld+json` so the block's start and 
- page-seo-auditor L27 ×1: After a sitemap.xml filename hit, run one case-insensitive grep for '<!--|-->' with -n and no context to confirm the <ur
- page-seo-auditor L28 ×1: When grepping sitemap.xml for a filename, add -C 2 so a <loc> sitting inside an XML comment block is visible, because th
- page-seo-auditor L29 ×1: To find where a page's ld+json block closes, grep the page for ^</script> anchored at line start, not bare </script>. Th
- page-seo-auditor L30 ×1: Before calling a head tag or sitemap entry present, grep '<!--|-->' in the page and in sitemap.xml in the same turn as t
- page-seo-auditor L31 ×1: For a page whose robots meta is noindex, one case-insensitive Grep with the alternation `canonical|og:|twitter:|ld\+json
- page-seo-auditor L32 ×1: In the first grep batch, add </script> and <!--|--> to the page's tag grep. That returns the JSON-LD block's end line an
- page-seo-auditor L33 ×1: After grepping sitemap.xml for the filename, also grep it for `<!--|-->`. Entries can sit inside comment blocks (sitemap
- page-seo-auditor L34 ×1: For not-in-sitemap, grep sitemap.xml for the filename and for `<!--|-->` in the same call. sitemap.xml has multi-line co
- page-seo-auditor L35 ×1: For JSON-LD parse checks, Grep `ld\+json|</script>` with -n in one call, then Read from the opening script line through 
- page-seo-auditor L36 ×1: In the first turn, grep `</script>` with -n alongside the ld+json grep; the JSON-LD block closes at the first `</script>
- page-seo-auditor L37 ×1: When checking sitemap.xml membership, grep `<!--|-->` in sitemap.xml alongside the filename, because the file wraps entr
- page-seo-auditor L38 ×1: Before reporting PAGE_META absent, grep the filename stem without ".html" case-insensitively in seo-patch.js, since a ke
- page-seo-auditor L39 ×1: In the first batch, grep the page for `ld\+json|</script>` alongside the tag greps and grep `<!--|-->` too, so the JSON-
- page-seo-auditor L40 ×1: On the first turn, grep `</script>|<script` on the page alongside the tag grep to get the ld+json block bounds, so the J
- page-seo-auditor L41 ×1: When a sitemap.xml grep hits a filename, also grep `<!--|-->` in the same turn and confirm the hit sits outside any comm
- page-seo-auditor L42 ×1: Put `</script>` in the first page grep alongside `ld\+json`, so the JSON-LD Read range (offset and limit) is known in th
- page-seo-auditor L43 ×1: For a page absent from PAGE_META, one grep of seo-patch.js for `PAGE_META\s*\[` returns the unmapped-page warning lines 
- page-seo-auditor L44 ×1: When checking a sitemap entry, grep sitemap.xml for `<!--|-->` with -n in the same turn as the filename grep. A `<loc>` 
- page-seo-auditor L45 ×1: In the first batch, grep the page for `ld\+json|</script>` together with the head-tag grep, so the JSON-LD block's closi
- page-seo-auditor L46 ×1: For blog/ pages, seo-patch.js scans only the repo root (the `fs.readdirSync(dir)` line near the end, about line 387), so
- page-seo-auditor L47 ×1: For a blog/ page, a grep of seo-patch.js for its quoted key returning nothing means no PAGE_META entry, so report page_m
- page-seo-auditor L48 ×1: For a short head (about 15 lines or fewer), one Read with offset 0 and limit 15 can replace the separate tag greps. It s
- page-seo-auditor L49 ×1: In the first page grep, add `<script` and `</script>` to the tag pattern so both ld+json block line ranges are known in 
- page-seo-auditor L50 ×1: On a page with several ld+json blocks, grep `</script>|ld\+json` with -n once to get every block's line span, then Read 
- page-seo-auditor L51 ×1: Before counting a sitemap hit as indexed, grep the filename with -B 2 -A 2 to confirm it is not inside a multi-line XML 
- page-seo-auditor L52 ×1: A page under `.claude/arena/canaries/` is not served and is not a root page, so a sitemap miss there is expected. Still 
- page-seo-auditor L53 ×1: For an item under .claude/arena/canaries/, a sitemap miss and a PAGE_META miss are expected, because the fixture is not 
- page-nap-auditor L55 ×1: For absolute-URL checks, grep with -o and the pattern https?://[A-Za-z0-9.-]+; a combined alternation (http://|www\.|cit
- page-nap-auditor L56 ×1: When a page's JSON-LD areaServed or footer names a city other than its own, grep that exact entry across the series' sib
- page-nap-auditor L57 ×1: For the domain check, grep `https?://[a-z0-9.-]+` with -o and -n, and write `<` literally in patterns, because an `&lt;`
- page-nap-auditor L58 ×1: In placeholder-token greps, drop `\}\}` from the pattern: inline `<style>` closing braces match on every page (here line
- page-nap-auditor L59 ×1: For the phone inventory, one grep with -o and -n over tel:[^"]* plus the (ddd) ddd-dddd pattern lists every tel: target 
- page-nap-auditor L60 ×1: For city-claim checks, grep with -o -n and a character-class pattern that skips the brand, e.g. Florence([,.;:)!?]|\s[^S
- page-nap-auditor L61 ×1: Footer tagline copy that names "Florence County" or "Pee Dee region" (e.g. "© 2026 Florence SC Services. Local dumpster 
- page-nap-auditor L62 ×1: When a page is in scope, grep -o its head geo tags (geo.placename, geo.position) and LocalBusiness "latitude" and compar
- page-nap-auditor L63 ×1: Grep `tel:` with -A 3 instead of no context: in the mobile bar and sticky CTA an SVG icon line sits between the href and
- page-nap-auditor L64 ×1: On these pages, long chrome lines print as "[Omitted long matching line]"; read their link text with a bounded grep -o, 
- page-nap-auditor L65 ×1: For the city sweep, grep explicit locality phrases first (in|serving|near <City>, <City>, SC, plus h1, title, meta descr
- page-nap-auditor L66 ×1: For files of 20 lines or fewer, confirm the length with a count grep (pattern "^", output_mode count), then run one case
- page-nap-auditor L67 ×1: On every page, grep the head for `geo\.position|ICBM|geo\.placename` and compare the coordinates to `geo\.position` in s
- page-nap-auditor L68 ×1: Add an HTML-comment sweep to the page grep set, `<!--[^>]*(Replace|TODO|FIXME|GBP)` with -n and -A 3, because template i
- page-nap-auditor L69 ×1: For google*.html verification stubs, grep the pattern "." with -n and head_limit 20 to see the entire file in one call, 
- page-nap-auditor L70 ×1: Run the phone check as a grep -o of the number patterns (`\(8[0-9]{2}\) ?[0-9]{3}-[0-9]{4}|tel:\+?[0-9]+`), not as conte
- page-nap-auditor L71 ×1: Run the tel: and phone-number patterns with -o first. Without -o, long chrome lines (header nav, mobile bar, footer NAP)
- page-nap-auditor L72 ×1: Add one grep to every page sweep for unreplaced template tokens, `\{\{|\[[A-Z][A-Z_ ]{2,}\]|TODO|XXX|555-[0-9]{4}` with 
- page-nap-auditor L73 ×1: When a plain grep on a page returns "[Omitted long matching line]", re-run it with output_mode content, -o and a `.{0,60
- page-nap-auditor L74 ×1: Also grep the head `geo.placename` meta, the footer "City Pages" anchor labels (label text against the href city) and th
- page-nap-auditor L75 ×1: For each tel: anchor, run one grep with -o -n on `<a href="tel:\+18439380480"[^>]*>[^<]{0,40}`; it returns every CTA's v
- page-nap-auditor L76 ×1: Run the phone, tel: and city checks first as Grep with output_mode content, -o and -n over the whole page. One call then
- page-nap-auditor L77 ×1: With -C context, minified header, mobile-bar, footer-nap and CTA lines come back as "[Omitted long matching line]", whic
- page-nap-auditor L78 ×1: Footer taglines reading "Florence County, SC" (site-wide, 26 pages) describe the business's home county, not the page's 
- page-nap-auditor L79 ×1: Add to the known-good list: the footer tagline "Connecting Florence County and Pee Dee region residents" is sitewide tem
- page-nap-auditor L80 ×1: For the city-claim check, grep the city name with -o and a short trailing window (e.g. "Florence.{0,24}") to list every 
- page-nap-auditor L81 ×1: When a Grep with context prints "[Omitted long matching line]", the hidden matches are often the header, sticky bar and 
- page-nap-auditor L82 ×1: On a first pass, run the phone and city pattern with `-o` and bounded `.{0,90}` context. Plain `-n` grep prints "[Omitte
- page-nap-auditor L83 ×1: On page-NAP audits, run one `-o -n` grep for `\(8[0-9]{2}\) ?[0-9]{3}-[0-9]{4}|tel:[^"'<> ]+` before any `-C` context gr
- page-nap-auditor L84 ×1: Search the name with a case-insensitive `Florence.{0,12}SC.{0,12}Serv` pattern, not the literal "Florence SC Services": 
- page-nap-auditor L85 ×1: Enumerate phone forms in one grep -o call with `\(\d{3}\)\s?\d{3}-\d{4}|\b\d{3}[-.]\d{3}[-.]\d{4}\b|\+1\d{10}|tel:[^"\s>
- page-nap-auditor L86 ×1: Cloudflare data-cfemail keys are per page, so a hash that appears on only one page is not a mismatch. Before mentioning 
- page-nap-auditor L87 ×1: Before flagging a "Florence" or "Florence County" string in body or footer copy, grep seo-patch.js for the same wording;
- page-nap-auditor L88 ×1: Grep runs ripgrep without PCRE2, so look-ahead patterns such as https?://(?!florencescservices\.com) fail with a parse e
- page-nap-auditor L89 ×1: When a grep prints "[Omitted long matching line]" with no content, re-run the same pattern with -o and a bounded prefix/
- page-nap-auditor L90 ×1: On city pages a plain content grep prints "[Omitted long matching line]" for the header, mobile bar, footer and sticky C
- page-nap-auditor L91 ×1: On city pages the header, mobile-bar, footer-nap and sticky-CTA lines are long. A plain -n grep prints them as "[Omitted
- page-nap-auditor L92 ×1: Before concluding, run one -o -i grep for `[A-Za-z0-9-]+\.(com|net|org|info)` on the page. It lists every host in one sh
- page-nap-auditor L93 ×1: In the first batch, run the phone, name and city greps together with `grep -o 'https?://[A-Za-z0-9.-]+'` and a placehold
- page-nap-auditor L94 ×1: Google Ads and Facebook tag IDs in the head (gtag 'AW-...', fbq) contain digit runs that match the bare-phone pattern 8[
- page-nap-auditor L95 ×1: For the locality sweep, skip reading body copy: one grep with -n -o and a bounded window (pattern `.{0,40}(CITY1|CITY2|.
- page-nap-auditor L96 ×1: On blog/ redirect stubs (meta http-equiv=refresh, no body chrome), put the chrome and city patterns (`<body|<footer|<nav
- page-nap-auditor L97 ×1: A bare-digit sweep with `843|803|938|0480` and -o -n finds every phone-like token in one call; on these pages the 803 hi
- page-nap-auditor L98 ×1: For blog/ posts and statewide guides whose filename names no city, write PAGE-CITY as "none (statewide)" and skip the pa
- page-nap-auditor L99 ×1: On blog pages the FAQPage JSON-LD sits on one very long line (line 192 here). Plain rg context output drops it as "[Omit
- page-nap-auditor L100 ×1: For a page whose filename names no city (index.html, blog/index.html), write PAGE-CITY as "none" and read locality again
- page-nap-auditor L101 ×1: For a page under about 20 lines, one grep -c "." sizes it, then one Read with offset and limit covering the whole stub r
- page-nap-auditor L102 ×1: Leave `}}` out of placeholder-token greps, since CSS closing braces in the inline style block (around line 498 of blog p
- page-nap-auditor L103 ×1: Batch the whole grep set into the first turn (tel:, (8[04]3), 938-0480, telephone/addressLocality/areaServed, <title, <h
- page-nap-auditor L104 ×1: For a page whose obfuscated footer email (data-cfemail hex) hides its domain, decode it by XOR-ing each later byte with 
- page-nap-auditor L105 ×1: To check domains, grep the page with -o for `https?://[^/"' ]+` and compare every host to CNAME, because an exact-domain
- page-nap-auditor L106 ×1: In the first grep batch, add one `-o` grep for `https?://[^"' <)]+` next to the NAP grep, since it lists every absolute 
- page-link-auditor L108 ×1: Treat absolute https://florencescservices.com/... URLs as internal, not external: strip the origin and test the repo-roo
- page-link-auditor L109 ×1: One python3 -I heredoc per page does the whole check in one tool call: regex (href|src)\s*=\s*("..."|'...') over the fil
- page-link-auditor L110 ×1: For each page, pipe the attribute grep straight into the existence loop (grep -o '(href|src)="[^"]*"' | sed to strip the
- page-link-auditor L111 ×1: Before reporting, reconcile the attribute total: grep -oiE "(href|src)[[:space:]]*=" count (104 here) must equal the quo
- page-link-auditor L112 ×1: Dedupe the extracted values with `grep -oE '(href|src)="[^"]*"' | sed | sort | uniq -c` before resolving, then test each
- page-link-auditor L113 ×1: Add a case-insensitive pass `(?i)(href|src)\s*=\s*\S+` and a `<base\b` check next to the quoted-attribute greps, because
- page-link-auditor L114 ×1: Own-domain absolute URLs (https://florencescservices.com/...) are internal, not external: strip the origin, resolve the 
- page-link-auditor L115 ×1: When running the unquoted-attribute check, the only hit on this template is `src=v;s=b.getElementsByTagName` at line 43,
- page-link-auditor L116 ×1: Resolve every unique normalized target in one Bash `for f in ...; do test -e` loop in a single call instead of one Glob 
- page-link-auditor L117 ×1: On a page like this, 83 internal attribute values collapse to 29 distinct targets. Test all of them in one Bash `test -e
- page-link-auditor L118 ×1: Resolve links with one bash loop over `grep -oE '(href|src)="[^"]*"'` piped through `sort -u`, stripping #/? and mapping
- page-link-auditor L119 ×1: In the first turn, run wc -c beside the href/src grep; a page under about 1 KB is a redirect stub whose links are absolu
- page-link-auditor L120 ×1: Test each unique resolved path once, not each occurrence. This page has 92 occurrences resolving to 37 unique paths, bec
- page-link-auditor L121 ×1: In the first turn, run one case-insensitive, whitespace-tolerant grep for `(?i)(href|src)\s*=` (only-matching, with line
- page-link-auditor L122 ×1: Size a page with wc -c, not wc -l. A one-line file with no trailing newline reports 0 lines and looks empty.
- page-link-auditor L123 ×1: When cross-checking the href/src count against a total grep, expect false hits from inline-script JS property assignment
- page-link-auditor L124 ×1: After de-duplicating the grep output, resolve every unique target in one bash `for p in ...; do test -e` loop under the 
- page-link-auditor L125 ×1: Extract with `(href|src)\s*=\s*["']` instead of `(href|src)=["']`, because the strict form misses spaced assignments suc
- page-link-auditor L126 ×1: Resolve own-domain absolute links (https://florencescservices.com/x.html and the canonical/sitemap/blog URLs) by strippi
- page-link-auditor L127 ×1: Grep `srcset=` alongside `(href|src)=` on each page, because the `src=` pattern does not match `srcset=` and image candi
- page-link-auditor L128 ×1: Count LINKS-CHECKED with a pipeline, grep -oE '(href|src)="[^"]*"' | grep -vE 'tel:|mailto:|https?:|"//|"#|cdn-cgi' | wc
- page-link-auditor L129 ×1: Count LINKS-CHECKED as every internal href/src occurrence in the grep output, repeats included (nav, footer and CTA bloc
- page-link-auditor L130 ×1: Run one Bash pipeline per page: grep -o -n for href/src, sed-split into line, attribute and value, skip http:, https:, m
- page-link-auditor L131 ×1: Dedupe before resolving: a page repeats its nav, footer and dropdown hrefs, so collapse the grep output to distinct inte
- page-link-auditor L132 ×1: Extract with two alternations, (href|src)="[^"]*" and (href|src)='[^']*', not one class that excludes both quote types (
- page-link-auditor L133 ×1: After the quoted-attribute grep, run one case-insensitive grep for (?i)(href|src)\s*=\s*[^"'\s] to catch unquoted and sp
- page-link-auditor L134 ×1: For each page, also grep once case-insensitively for `<base\b` and for unquoted `(href|src)=[^"'\s>]`. The quoted-only p
- page-link-auditor L135 ×1: The href/src grep also matches inline JS property writes such as "t.src=v;" in the Meta Pixel loader (line 43 of marion-
- page-link-auditor L136 ×1: Count internal links with one filter pipeline (grep -oE '(href|src)="[^"]*"' piped through sed to strip the wrapper, the
- page-link-auditor L137 ×1: Extract with one broad case-insensitive grep, (?i)(href|src|srcset|action)\s*=\s*['"]?[^'"\s>]+ with -o and -n, instead 
- page-link-auditor L138 ×1: Ripgrep (the Grep tool) has no look-ahead, so a negative filter such as (?!https?:|tel:) returns a regex parse error and
- page-link-auditor L139 ×1: Resolve every target against one `ls -1A` of the repo root plus `images/` and `blog/`, sent in the first turn alongside 
- page-link-auditor L140 ×1: Run a second case-insensitive grep for unquoted or space-around-`=` attributes, `(?i)\b(href|src)\s*=\s*[^\s>"']+`, in t
- page-link-auditor L141 ×1: Absolute URLs on the site's own origin (https://florencescservices.com/...) are not external: strip the origin and resol
- page-link-auditor L142 ×1: Resolve each attribute value by piping the only-matching grep output straight into a shell loop (strip the https://flore
- page-link-auditor L143 ×1: Absolute https URLs on florencescservices.com (the site's own origin) are internal, not external: strip the origin and t
- page-link-auditor L144 ×1: Extract the resolution-changing constructs in the same first-pass only-matching grep as href/src (add `<base[^>]*>` and 
- page-link-auditor L145 ×1: For LINKS-CHECKED, take the count from `Grep` with output_mode content, -o, -n and head_limit 0 on `(?i)(href|src)\s*=\s
- page-link-auditor L146 ×1: Treat protocol-relative values such as //cdn.callrail.com/... as external, the same as https; never strip one slash and 
- page-link-auditor L147 ×1: On pages in a subfolder such as blog/, map `../x` to repo-root `x` and `../` to `index.html` (and `blog/` to `blog/index
- page-link-auditor L148 ×1: Run the quoted href/src grep and a case-insensitive bare `href|src` count in the same first batch as the learnings Read;
- page-link-auditor L149 ×1: Own-domain absolute https links (https://florencescservices.com/...) fall under the https rule and get skipped silently;
- page-link-auditor L150 ×1: Extract with grep -oE '(href|src)="[^"]*"' (double quotes only): the mixed-quote class ["'][^"']*["'] cuts the value at 
- page-link-auditor L151 ×1: Test every unique resolved target in one Bash for-loop of `[ -e "$R/$f" ]` on absolute repo paths, and strip the origin 
- page-link-auditor L152 ×1: When a case-insensitive count of (?i)(href|src)\s*= is higher than the line count from the double-quoted grep, the extra
- page-link-auditor L153 ×1: Treat own-origin absolute URLs (https://florencescservices.com/x.html in canonical or og:url) as internal: strip the ori
- page-link-auditor L154 ×1: Extract attributes in one alternation grep, `(href|src)=([^'"\s>]|'[^']*'|"[^"]*")` with -o -n, so unquoted and single-q
- page-link-auditor L155 ×1: Before trusting an href/src grep, compare a case-insensitive count of `(href|src)\s*=` with the case-sensitive quoted co
- page-link-auditor L156 ×1: For each resolved target, also run `git ls-files --error-unmatch`; a file that is on disk but untracked passes test -e y
- page-link-auditor L157 ×1: When a resolved target is missing, run `ls | grep -i <stem>` in the same bash batch as the existence tests to find the n
- page-link-auditor L158 ×1: Extract with one grep, `(?i)\b(href|src)\s*=\s*("[^"]*"|'[^']*'|[^\s>"']+)` with -o -n, instead of the quoted-only patte
- finding-verifier L160 ×1: For wrong-city findings on lead-form payload strings, grep `lead_source_detail` across all *.html in one call. That show
- finding-verifier L161 ×1: When a finding cites a label/href mismatch in a shared footer, grep -o the anchor tags repo-wide, because sibling pages 

## Badges and flags

- 🪶 Featherweight — costs half the league median or less, and every quality measure is at least 80%.
- 🎯 Sharpshooter — 90%+ of judged findings were real, over 5+ findings.
- 🐤 Canary Hunter — found every planted defect, over 3+ planted defects.
- 🧹 Zero Churn — no tool errors and no repeated identical calls over 5+ runs.
- 🏆 Course Record — holds the cheapest correct run on an item.
- 💎 Earned Its Keep — leads its league on a pricier model than the league's cheapest, with positive net.
- 🧪 Innovator — the newest eligible setup in the league took first place.
- 🔥 Churner — median run spends 50%+ above par.
- 🙈 Lazy CLEAN — found under half the planted defects. Fireable on its own.
- 🔁 False Alarm — under half of its findings or verdicts held up. Fireable on its own.
- 💸 Spendthrift — 5×+ the cost of the league's cheapest setup with no better quality.
- 🎼 Conductor — orchestrator with positive net per item, start-up share ≤ 35%, hoarding ≤ 15%, no flags.
- 🏅 Best Division — top orchestrator setup by net per item.
- 🪓 Over-Divider — 50%+ of agent spend went to cold starts, or half its agents cost more to start than to work.
- 🐌 Hoarder — 40%+ of the job's cost was the main model doing read-only work itself.
- 🔁 Re-asker — 20%+ of spawns asked again about an item already asked about (canaries excepted).

ROOKIE = fewer than 5 runs. FIRE = Lazy CLEAN, False Alarm, or negative net while churning or overspending.
