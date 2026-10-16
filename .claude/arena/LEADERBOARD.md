# Agent Arena — Leaderboard

Generated 2026-10-16 19:30 UTC by `python3 .claude/arena/arena.py board`. 9 runs, $0.18 at API list price.

Net $/run = value earned − API cost. Churn = share of a run's cost above the cheapest correct run of the same job on the same item. Values and prices live in `rules.json`; editing them rescores everything.

## finding-verifier

| Setup | Model | Runs | Net $/run | Cost $/run | Churn | Precision | Planted found | Verdicts right | Badges | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `finding-verifier@455ef33` | sonnet-5-5 | 2 | $0.1794 | $0.0706 | 17% | – | – | 100% of 2 | 🏆 Course Record ×1 | **ROOKIE** |

## page-link-auditor

| Setup | Model | Runs | Net $/run | Cost $/run | Churn | Precision | Planted found | Verdicts right | Badges | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `page-link-auditor@455ef33` | haiku-5-5 | 2 | $0.5465 | $0.0035 | 0% | 100% of 2 | 100% of 2 | – | 🏆 Course Record ×2 | **ROOKIE** |

## page-nap-auditor

| Setup | Model | Runs | Net $/run | Cost $/run | Churn | Precision | Planted found | Verdicts right | Badges | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `page-nap-auditor@455ef33` | haiku-5-5 | 2 | $0.2409 | $0.0091 | – | 57% of 7 | 100% of 2 | – | – | **ROOKIE** |

## page-seo-auditor

| Setup | Model | Runs | Net $/run | Cost $/run | Churn | Precision | Planted found | Verdicts right | Badges | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `page-seo-auditor@455ef33` | haiku-5-5 | 3 | $0.3865 | $0.0051 | 0% | 100% of 2 | 100% of 2 | – | 🏆 Course Record ×3 | **ROOKIE** |

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

ROOKIE = fewer than 5 runs. FIRE = Lazy CLEAN, False Alarm, or negative net while churning or overspending.
