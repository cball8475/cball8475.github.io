#!/usr/bin/env bash
#
# migrate-to-gitea.sh — copy a complete Git repository to a Gitea instance.
#
# Handles the three things that silently break a hand-rolled migration:
#   1. Shallow clones. A `git clone` made by CI or a cloud agent is often
#      shallow; pushing one moves a truncated history and the loss is silent.
#      This script refuses to run against a shallow source.
#   2. refs/remotes/*. Bundling a normal clone captures remote-tracking refs,
#      not branches, so the destination gets zero real branches.
#   3. refs/pull/*. GitHub exposes read-only PR refs. `git push --mirror`
#      tries to push them; Gitea uses that namespace for its own pull
#      requests and rejects them, failing the push partway.
#
# It pushes refs/heads/* and refs/tags/* explicitly, then verifies every ref
# against the destination by SHA before reporting success.
#
# Usage:
#   ./migrate-to-gitea.sh --dest https://gitea.example.com/owner/repo.git
#   ./migrate-to-gitea.sh --dest <url> --source ./repo.bundle
#   ./migrate-to-gitea.sh --dest <url> --source https://github.com/owner/repo.git
#   ./migrate-to-gitea.sh --dest <url> --dry-run
#
# Auth: create the empty repo in Gitea first (do NOT let Gitea initialise it
# with a README), then authenticate with a Gitea token:
#   https://<user>:<token>@gitea.example.com/owner/repo.git
# or configure an SSH remote and pass that instead.

set -euo pipefail

DEST=""
SOURCE=""
DRY_RUN=0
KEEP=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dest)    DEST="${2:?--dest needs a URL}"; shift 2 ;;
    --source)  SOURCE="${2:?--source needs a path or URL}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --keep)    KEEP=1; shift ;;
    -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

[[ -n "$DEST" ]] || { echo "error: --dest is required" >&2; exit 2; }

# Default source: the repo this script lives in.
if [[ -z "$SOURCE" ]]; then
  SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && git rev-parse --show-toplevel)"
fi

WORK="$(mktemp -d)"
cleanup() { [[ "$KEEP" -eq 1 ]] || rm -rf "$WORK"; }
trap cleanup EXIT
MIRROR="$WORK/mirror.git"

echo "==> source: $SOURCE"
echo "==> dest:   $DEST"

# ---- 1. Build a true bare mirror ------------------------------------------
if [[ -d "$SOURCE/.git" || -d "$SOURCE/objects" ]]; then
  # Local repository. Refuse to migrate a shallow one -- history would be lost.
  if [[ -f "$SOURCE/.git/shallow" || -f "$SOURCE/shallow" ]]; then
    echo "error: source is a SHALLOW clone; migrating it would silently truncate history." >&2
    echo "       run:  git -C '$SOURCE' fetch --unshallow origin" >&2
    echo "       (needs the original remote to be reachable)" >&2
    exit 1
  fi
  # Clone --mirror from a non-bare clone only copies refs/heads, which omits
  # branches that exist solely as remote-tracking refs. Build the mirror from
  # the source's own remote-tracking refs instead.
  git init --bare --quiet "$MIRROR"
  git -C "$MIRROR" remote add origin "$SOURCE"
  git -C "$MIRROR" fetch --quiet origin '+refs/heads/*:refs/heads/*' '+refs/tags/*:refs/tags/*'
  # Pull in branches the working clone only tracks remotely.
  git -C "$MIRROR" fetch --quiet origin '+refs/remotes/origin/*:refs/heads/*' 2>/dev/null || true
  git -C "$MIRROR" update-ref -d refs/heads/HEAD 2>/dev/null || true
else
  # A bundle or a remote URL -- git clone --mirror handles both.
  git clone --mirror --quiet "$SOURCE" "$MIRROR"
fi

# ---- 2. Drop refs Gitea will not accept ------------------------------------
PULL_REFS=$(git -C "$MIRROR" for-each-ref --format='%(refname)' refs/pull 2>/dev/null | wc -l | tr -d ' ')
if [[ "$PULL_REFS" -gt 0 ]]; then
  echo "==> dropping $PULL_REFS refs/pull/* refs (GitHub PR refs; Gitea reserves this namespace)"
  git -C "$MIRROR" for-each-ref --format='delete %(refname)' refs/pull | git -C "$MIRROR" update-ref --stdin
fi

BRANCHES=$(git -C "$MIRROR" for-each-ref --format='%(refname)' refs/heads | wc -l | tr -d ' ')
TAGS=$(git -C "$MIRROR" for-each-ref --format='%(refname)' refs/tags | wc -l | tr -d ' ')
COMMITS=$(git -C "$MIRROR" rev-list --count --all)
echo "==> prepared: $BRANCHES branches, $TAGS tags, $COMMITS commits"

if [[ "$BRANCHES" -eq 0 ]]; then
  echo "error: mirror contains zero branches -- refusing to push an empty repo." >&2
  exit 1
fi

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "==> dry run; nothing pushed. Branches that would be created:"
  git -C "$MIRROR" for-each-ref --format='    %(refname:short)' refs/heads
  exit 0
fi

# ---- 3. Push branches and tags explicitly (never --mirror) -----------------
echo "==> pushing branches and tags"
git -C "$MIRROR" push --follow-tags "$DEST" '+refs/heads/*:refs/heads/*'
if [[ "$TAGS" -gt 0 ]]; then
  git -C "$MIRROR" push "$DEST" '+refs/tags/*:refs/tags/*'
fi

# ---- 4. Verify by SHA, ref by ref -----------------------------------------
echo "==> verifying destination against source"
git -C "$MIRROR" for-each-ref --format='%(objectname) %(refname)' refs/heads refs/tags \
  | sort > "$WORK/want.txt"
git ls-remote --heads --tags "$DEST" | awk '{print $1" "$2}' \
  | grep -v '\^{}$' | sort > "$WORK/got.txt"

if diff -u "$WORK/want.txt" "$WORK/got.txt" > "$WORK/diff.txt"; then
  echo "==> OK: all $((BRANCHES + TAGS)) refs present on destination at matching SHAs"
else
  echo "!!! MISMATCH between source and destination:" >&2
  cat "$WORK/diff.txt" >&2
  exit 1
fi

echo
echo "Git data is migrated. These do NOT travel with a git push -- see"
echo "MIGRATION-TO-GITEA.md: pull requests, issues, releases, CI secrets,"
echo "Actions runners, branch protection, and any Pages hosting."
