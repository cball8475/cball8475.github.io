# Migrating this site off GitHub to Gitea

Written 2026-08-27, while GitHub was reachable.

`migration/migrate-to-gitea.sh` moves the Git data. Read the hosting section
first — for this repo, moving the Git data is the easy half and the half that
does not keep the site up.

## Read this before moving anything

**GitHub Pages is the web host for florencescservices.com, and Gitea has no
equivalent.** This repo is not just source; the `.html` files at the root are
the live site, and a push to `main` is the deploy. `CNAME` points
florencescservices.com at GitHub's Pages servers.

Push this repo to Gitea and nothing happens to the live site — it keeps serving
from GitHub Pages, because Pages is tied to the GitHub repo, not to your Git
remote. Delete the GitHub repo and **florencescservices.com goes down.** This
is a lead site for a business; treat that as the constraint it is.

Gitea has no built-in Pages feature. Pick a host before you cut over:

- **Cloudflare Pages** — the natural fit, since the site's forms already post
  to a Cloudflare Worker and DNS is likely already there. Connects to a Git
  repo, or takes a direct upload via `wrangler pages deploy`, which needs no
  Git host at all.
- **Netlify / Vercel** — same shape, both take a direct CLI deploy.
- **Gitea Actions + rsync** to any box you control.

Whichever you choose, the cutover is a DNS change, and `CNAME` becomes dead
weight (it is a GitHub Pages file; other hosts ignore it). Keep the GitHub repo
alive and serving until the new host answers on the domain.

## What this repo actually is, as of 2026-08-27

Counts read back from `git ls-remote` and the GitHub API:

| | cball8475.github.io |
|---|---|
| Visibility | **public** |
| Branches | 12 |
| Tags | 0 |
| Commits (all refs) | 624 |
| Open pull requests | 1 (#1, Cloudflare Workers configuration) |
| Issues | 0 |
| Actions workflows | 0 |
| Hosting | GitHub Pages → florencescservices.com |

## Moving the Git data

Create the repo in Gitea first — empty, no README, matching visibility
(this one is public). Then:

    ./migrate-to-gitea.sh --dest https://gitea.example.com/cball8475/site.git

The script verifies every ref by SHA against the destination and exits non-zero
on a mismatch. Add `--dry-run` to see what it would create first.

To work with GitHub down, build a bundle while it is up and migrate from that:

    git clone --mirror https://github.com/cball8475/cball8475.github.io.git site.git
    cd site.git && git for-each-ref --format='delete %(refname)' refs/pull \
      | git update-ref --stdin
    git bundle create ../site.bundle --all
    git bundle verify ../site.bundle    # must say "records a complete history"
    ./migrate-to-gitea.sh --dest <gitea-url> --source ../site.bundle

## Three traps, all hit while building the script

**Your clone is probably shallow.** Cloud and CI clones use `--depth 1`. This
repo's session clone held 54 of 624 commits — under 9%. Pushing it to Gitea
moves a truncated history silently. The script refuses a shallow source; fix it
with `git fetch --unshallow origin` while GitHub is still reachable.

**Bundling a working clone captures `refs/remotes/*`, not branches.** A bundle
built that way restores as remote-tracking refs and almost no branches. Build a
bare mirror first, as above.

**`git push --mirror` chokes on `refs/pull/*`.** GitHub publishes read-only PR
refs — 10 here. Gitea uses that namespace for its own pull requests and rejects
them, leaving a half-pushed repo. The script deletes them and pushes
`refs/heads/*` and `refs/tags/*` explicitly instead.

## What does not travel with a git push

- **PR #1** — its branch survives in `refs/heads/*`, so no code is lost, but
  the description and discussion are not in Git. Gitea's *New Migration →
  GitHub* importer carries them across; it needs a GitHub token and needs the
  **Gitea server** to reach github.com, so it is no help during an outage.
- **GitHub Pages hosting.** See above. This is the one that matters.
- **The `cball8475.github.io` name.** The repo name is what makes GitHub serve
  it at that address. On Gitea the name is just a name; call it whatever fits.

## After the push

1. `git ls-remote --heads <gitea-url> | wc -l` → expect 12.
2. `main` is the default branch.
3. New host builds and serves the root `.html` files with no build step.
4. florencescservices.com resolves to the new host and serves HTTPS.
5. Spot-check a form submission end to end — the Worker endpoint is unchanged,
   but the page origin is not.
6. `git remote set-url origin <gitea-url>` in local clones.
7. Only after the domain is live elsewhere, retire the GitHub repo.

`seo-patch.js` and `sitemap.xml` are unaffected by the move — they encode the
site origin and canonical paths, and the origin does not change as long as the
domain does not.
