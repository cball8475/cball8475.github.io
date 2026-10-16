# Learnings — page-nap-auditor

Rules earlier runs of this agent proposed. Each one is on trial or was kept because net $/run did not
drop after it was added. They are advice. They never override the agent file: read-only, the source of
truth, and the known-good lists always win. Managed by `.claude/arena/arena.py sync`; do not hand-edit.

- **L54** (on trial) On a page whose filename names no city, set PAGE-CITY to none and test locality with one grep for "in [A-Z][a-z ]+, S\.?C|serving|local [A-Z][a-z]+ provider" plus the areaServed block; "Florence, SC" in body copy on such pages is the business's home, so it is not a wrong-city finding.
