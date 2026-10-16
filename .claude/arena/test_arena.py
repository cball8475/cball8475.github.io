#!/usr/bin/env python3
"""Self-test for the learnings trial in arena.py. Run: python3 .claude/arena/test_arena.py

Copies arena.py and rules.json into a temp repo so nothing here is touched, then
checks with synthetic runs that a learning that hurts net $/run is retired and
stays retired, one that helps is kept, and a learning promoted in the same sync
that retired another is compared with the baseline both were missing.
"""
import importlib.util, os, shutil, tempfile
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
tmp = tempfile.mkdtemp()
os.makedirs(os.path.join(tmp, ".claude", "arena"))
os.makedirs(os.path.join(tmp, ".claude", "agents"))
for f in ("arena.py", "rules.json"):
    shutil.copy(os.path.join(HERE, f), os.path.join(tmp, ".claude", "arena", f))
open(os.path.join(tmp, ".claude", "agents", "page-seo-auditor.md"), "w").write("STATUS:\n")
spec = importlib.util.spec_from_file_location("arena", os.path.join(tmp, ".claude", "arena", "arena.py"))
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)

rules = A.load_json(A.RULES, {})
T0 = datetime(2026, 10, 1, 12, 0, tzinfo=timezone.utc)
iso = lambda dt: dt.isoformat().replace("+00:00", "Z")
clock = [T0]
A.now = lambda: iso(clock[0])  # sync always runs after the runs it judges
runs = []


def batch(n, start_min, net, learning=None):
    for i in range(n):
        runs.append({"run": f"r{len(runs)}", "agent": "page-seo-auditor", "ts": iso(T0 + timedelta(minutes=start_min + i)),
                     "net": net, "cost": 0.005, "canary": "x.html", "version": "v1", "model": "m", "learning": learning})


def sync(at_min):
    clock[0] = T0 + timedelta(minutes=at_min)
    return {l["id"]: l for l in A.sync_learnings(runs, runs, rules, quiet=True)}


batch(3, -120, 0.50, "Batch the five head-tag greps in one turn")
batch(2, -110, 0.50, "Batch the five head-tag greps in one turn.")  # punctuation differs: same learning
batch(1, -100, 0.50, "Read seo-patch.js PAGE_META with one grep")
L = sync(0)
assert (L["L1"]["status"], len(L["L1"]["proposed_by"]), L["L2"]["status"]) == ("trial", 5, "pending"), L

batch(5, 1, 0.20)  # L1 on trial: net drops
L = sync(10)
assert (L["L1"]["status"], L["L2"]["status"]) == ("retired", "trial"), L

batch(5, 11, 0.60, "Batch the five head-tag greps in one turn")  # L2 on trial: net rises; L1 proposed again
L = sync(20)
assert (L["L1"]["status"], L["L2"]["status"]) == ("retired", "kept"), L
c = A.compare_learning(L["L2"], list(L.values()), runs, rules["thresholds"])
assert (c["n_before"], c["n_after"], round(c["net_before"], 2), round(c["net_after"], 2), c["call"]) == (6, 5, 0.5, 0.6, "HELPS"), c
assert open(os.path.join(A.LEARNINGS_DIR, "page-seo-auditor.md")).read().rstrip().endswith("Read seo-patch.js PAGE_META with one grep")

shutil.rmtree(tmp)
print("arena learnings: all checks passed")
