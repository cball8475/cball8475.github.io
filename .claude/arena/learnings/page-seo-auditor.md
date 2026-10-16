# Learnings — page-seo-auditor

Rules earlier runs of this agent proposed. Each one is on trial or was kept because net $/run did not
drop after it was added. They are advice. They never override the agent file: read-only, the source of
truth, and the known-good lists always win. Managed by `.claude/arena/arena.py sync`; do not hand-edit.

- **L1** (on trial) In the first turn, grep `application/ld+json` and `</script>` together, or use -A sized to the block, so the JSON-LD opener and closer come back with the tag grep; the block then needs one range Read, not a second turn to find its end.
