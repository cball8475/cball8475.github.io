# Agent Arena — Leaderboard

Generated 2026-10-16 19:41 UTC by `python3 .claude/arena/arena.py board`. 15 runs, $0.21 at API list price.

Net $/run = value earned − API cost. Churn = share of a run's cost above the cheapest correct run of the same job on the same item. Values and prices live in `rules.json`; editing them rescores everything.

## Orchestrator (main session)

One row per main model · effort · CLAUDE.md version. A session is scored as one job: what its team earned minus everything the job cost, main model included, per graded item. Main share = main-model cost from first spawn to last result. Start-up share = share of agent spend that went to cold starts (over-division shows up here). Hoarding = share of cost spent on main-model turns that only read (under-division).

| Setup | Sessions | Items | Net $/item | Cost $/item | Main share | Start-up share | Hoarding | Badges | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| opus-5-5 · xhigh · `CLAUDE.md@455ef33` | 1 | 15 | $-0.1734 | $0.4990 | 97% | 35% | 2% | – | **ROOKIE** |

## finding-verifier

| Setup | Model | Runs | Net $/run | Cost $/run | Churn | Precision | Planted found | Verdicts right | Badges | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `finding-verifier@455ef33` | sonnet-5-5 | 2 | $0.1794 | $0.0706 | – | – | – | 100% of 2 | – | **ROOKIE** |

## page-link-auditor

| Setup | Model | Runs | Net $/run | Cost $/run | Churn | Precision | Planted found | Verdicts right | Badges | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `page-link-auditor@455ef33` | haiku-5-5 | 4 | $0.5470 | $0.0030 | 9% | 100% of 4 | 100% of 4 | – | 🐤 Canary Hunter 🏆 Course Record ×2 | **ROOKIE** |

## page-nap-auditor

| Setup | Model | Runs | Net $/run | Cost $/run | Churn | Precision | Planted found | Verdicts right | Badges | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `page-nap-auditor@455ef33` | haiku-5-5 | 4 | $0.1174 | $0.0076 | – | 54% of 13 | 100% of 4 | – | 🐤 Canary Hunter | **ROOKIE** |

## page-seo-auditor

| Setup | Model | Runs | Net $/run | Cost $/run | Churn | Precision | Planted found | Verdicts right | Badges | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `page-seo-auditor@455ef33` | haiku-5-5 | 5 | $0.3321 | $0.0046 | 0% | 71% of 7 | 100% of 4 | – | 🐤 Canary Hunter 🧹 Zero Churn 🏆 Course Record ×1 | **KEEP** |

## Learnings — before vs after

No learnings proposed yet.

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
