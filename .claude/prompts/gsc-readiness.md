<!--
  GSC readiness prompt for florencescservices.com.
  Target: Claude Code, run in a session on cball8475/cball8475.github.io.
  Paste everything below the line into a new session (or say "run .claude/prompts/gsc-readiness.md").
  Read-only job: it writes one report file under .claude/reports/ and nothing else.
  Written 2026-11-04. Lives under .claude/ so Jekyll does not serve it on the live site.
-->
---

<role>
You are a technical SEO engineer preparing florencescservices.com for Google Search Console. You report what Google's crawler will actually see on the live site, with the command output that proves it. You do not fix anything.
</role>

<hard_rules>
1. READ-ONLY. Never edit, create, move or delete any file except the one report file named in <output>. No commits, no pushes.
2. NEVER run seo-patch.js. It rewrites every HTML file in the repo. Read it.
3. The live site is the evidence. Fetch https://florencescservices.com with curl. Use the repo only to (a) list which pages should exist and (b) locate the source line a fix belongs in. If a live fetch fails, that check is UNVERIFIED. Never fill it from the repo copy.
4. A check you could not run is UNVERIFIED, never PASS. Never write "won't be rejected" about anything you did not test.
5. Tag every finding [Certain] (command output proves it), [Likely] (strong inference) or [Guessing]. Every [Certain] carries the command and one line of its output.
6. Never copy a name, email address or phone number out of data/*.json into the report or the chat. Report counts and paths only.
7. Fixes respect the source of truth: canonical path, OG title and OG description live in PAGE_META in seo-patch.js; the origin in const SITE; the phone in const PHONE_TEL (tel:+18439380480). Write such a fix as "change PAGE_META['<file>'] ..., then Charlie runs seo-patch.js", never as a hand edit to the page.
</hard_rules>

<known_good>
Do not report these:
- google1067d2b418ee6f0f.html is the GSC verification stub. No canonical, OG, JSON-LD or sitemap entry is correct.
- index.html is in sitemap.xml as the bare origin.
- href="/foo.html" is root-absolute and resolves from the repo root.
- (843) 555-0123 and (843) 555-1234 are form placeholders.
- "addressLocality": "Florence" / "postalCode": "29501" in LocalBusiness JSON-LD is the business address on every page. A page's own city goes in areaServed.
- A page missing from PAGE_META is a script coverage gap, not a GSC error.
- A grep that matches nothing has not proved absence. Re-check the bare token case-insensitively. index.html lines 115 and 117 are minified CSS; use only-matching output.
</known_good>

<method>
Write ONE Python script to the scratchpad (stdlib, plus curl via subprocess) that does all fetching and parsing, and run it once. Do not read pages one at a time in the main context. Do not spawn the page-seo, page-nap or page-link auditors; the script replaces them for this job.

URL set = every <loc> in the live sitemap.xml + every *.html at the repo root and in blog/ + every internal href found on those pages.

Per URL, record:
- final HTTP status, every redirect hop, Content-Type
- <meta name="robots"> and the X-Robots-Tag header
- <link rel="canonical">: absolute? https apex? self-referencing? equal to its sitemap <loc>? equal to PAGE_META?
- <title>, meta description present, count of <h1>
- each JSON-LD block: parses with json.loads? its @type values
- in sitemap Y/N; inbound internal link count; visible body word count
Also fetch one page without ".html" and https://florencescservices.com/index.html, to see whether GitHub Pages serves duplicate URLs.

Site-level checks:
A. Host and verification. http://, http://www. and https://www. each reach https://florencescservices.com/ in one 301 hop. /google1067d2b418ee6f0f.html returns 200 with body exactly "google-site-verification: google1067d2b418ee6f0f.html". Look for a google-site-verification meta tag on the home page. DNS TXT via https://dns.google/resolve?name=florencescservices.com&type=TXT. TLS succeeds without -k. Any http:// asset reference on an https page (mixed content).
B. robots.txt. 200, text/plain, Sitemap line matches the live sitemap URL, no rule blocks a sitemap URL or CSS/JS a page needs.
C. sitemap.xml. 200, XML content type, well-formed, sitemaps.org namespace, no duplicate <loc>, every <loc> absolute https apex, every <lastmod> a valid W3C date and not in the future.
D. Structured data. For each @type, check Google's required properties against developers.google.com/search/docs/appearance/structured-data and cite the page you used; if you cannot fetch it, tag the finding [Likely]. Schema telephone must equal PHONE_TEL and appear in visible text. Flag Review or AggregateRating on the business's own LocalBusiness or Organization (self-serving, ineligible). FAQ rich results only show for government and health sites, so FAQPage markup is not an error; it earns nothing.
E. Near-duplicates. Shingle the visible body text of every indexable page (5-word shingles, Jaccard). List pairs at or above 0.80. City and vertical pages built by find-and-replace (see WORKFLOW.md) are the doorway-page and "Crawled - currently not indexed" risk.
F. Public non-page files. Every tracked file GitHub Pages serves (not a dotfile, not under _): .md, .json, .js, .txt, data/. Record each status. Flag any 200 that holds internal notes or contact data. robots.txt Disallow does not hide a file, and the repo is public.

Map every problem to the exact GSC label it will surface under: "Submitted URL marked 'noindex'", "Submitted URL blocked by robots.txt", "Not found (404)", "Page with redirect", "Duplicate without user-selected canonical", "Duplicate, Google chose different canonical than user", "Alternate page with proper canonical tag", "Soft 404", "Crawled - currently not indexed", "Unparsable structured data", and the sitemap errors "Couldn't fetch", "Invalid date", "URL not allowed".

Send every finding not tagged [Certain] to finding-verifier: one agent per finding, all spawned in one message, prompt first line "RUN: gsc#<n>" (there is no auditor run to credit). Drop REFUTED. Keep UNVERIFIABLE, marked as such.
</method>

<output>
Write .claude/reports/gsc-readiness-<YYYY-MM-DD>.md, date from `TZ=America/New_York date +%F`. Sections, in this order:
1. Verdict: READY / READY WITH EXCLUSIONS / NOT READY, with counts of submission blockers, excluded pages, rich-result losses, policy risks and UNVERIFIED checks.
2. GSC entry sheet, exactly what to type: recommended property type and exact string; verification method in place and its live status; sitemap URL to submit and the URL count in it; preferred host; the 10 URLs to push through URL Inspection > Request Indexing first, one-line reason each.
3. Rejection table: # | GSC label | URL(s) | Evidence | Impact (Blocks submission / Page excluded / Rich result lost / Policy risk) | Fix (file:line, or PAGE_META entry + seo-patch.js) | Confidence.
4. Page inventory: one row per URL, fields above.
5. Structured data: page | @types | parses | missing required | policy flag.
6. UNVERIFIED: every check that could not run, and why.
7. Fix order: blockers, then exclusions, then rich results, then policy.
In chat, reply with the verdict line, the five counts and the report path. Nothing else.
</output>

<stop_conditions>
- Live home page or sitemap.xml unreachable after 3 tries: stop, report the error, write nothing.
- The script fails twice on the same step: stop and show the traceback.
- Any step that would write outside .claude/reports/: stop and ask.
After each of these finishes, output one line "✅ <what finished>": script written, script run, verifier results back, report written.
</stop_conditions>

<done_when>
Every URL in the set has a row. Every sitemap <loc> has a live status. Every finding has evidence and a confidence tag. Every check reads PASS, FAIL or UNVERIFIED, none blank. No page file was edited, seo-patch.js was not run, and no contact data from data/*.json appears in the report.
</done_when>
