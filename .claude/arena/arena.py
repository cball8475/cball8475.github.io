#!/usr/bin/env python3
"""Agent arena: score subagent setups by net dollars (value earned - API cost).

Claude Code writes every subagent run to
  ~/.claude/projects/<project>/<session>/subagents/agent-<id>.jsonl
with per-request token usage. This script turns those transcripts into a
durable ledger (runs.jsonl, committed to the repo, because cloud containers
and their transcripts are thrown away), grades each run, and ranks setups.

  harvest     copy new or changed runs from the transcripts into runs.jsonl
  board       harvest, then print the leaderboard and write LEADERBOARD.md
  runs        per-run breakdown: cost, churn, what earned or lost value
  rule        record Charlie's ruling on a run or one of its findings
  learnings   before/after comparison for every agent learning
  sync        promote, judge and retire learnings; rewrite learnings/<agent>.md
  sessions    per-session orchestrator breakdown: main vs agent cost, start-up, hoarding

Self-test: python3 .claude/arena/test_arena.py

Grading sources, strongest first:
  1. rulings.jsonl          Charlie's word. Overrides everything.
  2. canaries/answers.json  pages with planted defects, so the truth is known.
  3. finding-verifier runs  linked to an auditor finding by "RUN: <id>#<n>"
                            in the verifier's prompt.

Learnings: agents propose one rule per run on a LEARNING: line. They never
write files. sync is the only writer: it puts one learning on trial at a time
per agent, judges it on net $/run before vs after it was added, keeps it if
net did not drop and retires it if it did. The Stop hook runs harvest + sync.

Orchestrator: each session that spawned agents is also scored as one job
(sessions.jsonl): team value minus main-model cost from first spawn to last
result minus agent cost, per graded item. It flags over-division (agent spend
going to cold starts) and hoarding (the main model doing read-only work).

Stdlib only. Never stores prompt text beyond the item path and the RUN link.
"""
import argparse
import glob
import json
import os
import re
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

ARENA = os.path.dirname(os.path.realpath(__file__))  # realpath: transcripts record the resolved cwd
REPO = os.path.dirname(os.path.dirname(ARENA))
AGENTS_DIR = os.path.join(REPO, ".claude", "agents")
RUNS = os.path.join(ARENA, "runs.jsonl")
SESSIONS = os.path.join(ARENA, "sessions.jsonl")
RULINGS = os.path.join(ARENA, "rulings.jsonl")
LEARNINGS = os.path.join(ARENA, "learnings.jsonl")
LEARNINGS_DIR = os.path.join(ARENA, "learnings")
RULES = os.path.join(ARENA, "rules.json")
ANSWERS = os.path.join(ARENA, "canaries", "answers.json")
BOARD_MD = os.path.join(ARENA, "LEADERBOARD.md")
CANARY_DIR = ".claude/arena/canaries/"
PROJECTS = os.path.expanduser("~/.claude/projects")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def ts_key(ts):
    """Transcripts use '...Z' with milliseconds, git uses '+00:00'. Compare as datetimes."""
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def job_of(agent):
    """Challengers are named <job>--<variant>.md and compete in the same league."""
    return agent.split("--")[0]


# --------------------------------------------------------------------- files

def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def load_jsonl(path):
    try:
        with open(path) as f:
            return [json.loads(line) for line in f if line.strip()]
    except FileNotFoundError:
        return []


def write_if_changed(path, text):
    """Write only when the bytes differ, so a no-op run leaves git clean."""
    try:
        with open(path) as f:
            if f.read() == text:
                return False
    except FileNotFoundError:
        pass
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)
    return True


def write_jsonl(path, rows):
    return write_if_changed(path, "".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))


# ------------------------------------------------------------------- harvest

def subagent_files(session_transcript=None):
    """All subagent transcripts, or only one session's when the hook passes it."""
    if session_transcript:
        base = session_transcript[:-6] if session_transcript.endswith(".jsonl") else session_transcript
        return sorted(glob.glob(os.path.join(base, "subagents", "agent-*.jsonl")))
    return sorted(glob.glob(os.path.join(PROJECTS, "*", "*", "subagents", "agent-*.jsonl")))


def in_this_repo(records):
    """Transcripts from every project live side by side; keep this repo's."""
    for r in records:
        if r.get("cwd"):
            cwd = os.path.realpath(r["cwd"])
            return cwd == REPO or cwd.startswith(REPO + os.sep)
    return False


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True).stdout.strip()


def session_start(path):
    """First timestamp of the parent session. Claude Code loads agent files
    once, when the session starts (checked 2026-10-16: an edit mid-session left
    the subagent system-prompt hash unchanged), so that is the moment that
    decides which definition a run used."""
    main = os.path.dirname(os.path.dirname(path)) + ".jsonl"  # <session>/subagents/agent-x.jsonl -> <session>.jsonl
    try:
        with open(main) as f:
            for line in f:
                ts = json.loads(line).get("timestamp")
                if ts:
                    return ts
    except (FileNotFoundError, ValueError):
        pass
    return None


def agent_version(agent, ts):
    """Git short hash of the agent definition committed at session start.

    Built-in agents (general-purpose, Explore, ...) have no file: 'builtin'.
    A session started after the last commit while the file has uncommitted
    edits gets '+dirty'. The prompt hash in each run record is the check on
    this: two versions sharing one prompt hash mean the label is wrong.
    """
    rel = f".claude/agents/{agent}.md"
    if not os.path.exists(os.path.join(REPO, rel)):
        return "builtin"
    return file_version(rel, ts)


def file_version(rel, ts):
    """Git short hash of a repo file as committed at ts."""
    sha = git("log", "-1", "--format=%h", f"--before={ts}", "--", rel)
    if not sha:
        return "uncommitted"
    last_commit = git("log", "-1", "--format=%cI", "--", rel)
    if git("status", "--porcelain", "--", rel) and last_commit and ts_key(ts) > ts_key(last_commit):
        return sha + "+dirty"
    return sha


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text")
    return ""


def parse_findings(report):
    """Split a FINDINGS block into one text chunk per '- CLASS:' item."""
    m = re.search(r"^FINDINGS:[^\n]*$(.*?)(?=^[A-Z][A-Z_-]+:|\Z)", report, re.M | re.S)
    if not m:
        return []
    out = []
    for chunk in re.split(r"^\s*-\s*CLASS:", m.group(1), flags=re.M)[1:]:
        lines = [l.strip() for l in chunk.strip().splitlines()]
        cls = lines[0].split()[0] if lines and lines[0] else "unknown"
        out.append({"class": cls, "text": ("CLASS: " + " ".join(lines))[:400]})
    return out


def parse_learning(report):
    m = re.search(r"^LEARNING:\s*(.+)$", report, re.M)
    if not m:
        return None
    text = m.group(1).strip().strip("`").strip()
    return None if re.fullmatch(r"(none|n/?a|-)\.?", text, re.I) else text[:300]


def group_requests(records):
    """One API request is split across several records (one per content block)
    that share message.id. Returns them in order, each with its final usage
    (the record with the highest output count), first timestamp and tool names."""
    requests = {}
    for r in records:
        if r.get("type") != "assistant":
            continue
        msg = r["message"]
        usage = msg.get("usage") or {}
        req = requests.setdefault(msg.get("id") or r.get("requestId"),
                                  {"usage": usage, "model": msg.get("model", ""), "ts": r.get("timestamp"), "tools": []})
        if usage.get("output_tokens", 0) >= req["usage"].get("output_tokens", 0):
            req["usage"] = usage
        req["tools"] += [b.get("name", "") for b in msg.get("content") or [] if b.get("type") == "tool_use"]
    return list(requests.values())


def new_bucket():
    return defaultdict(lambda: defaultdict(int))


def freeze(bucket):
    return {k: dict(v) for k, v in sorted(bucket.items())}


def add_usage(bucket, req, prices):
    """Add one request's tokens to bucket[model] or bucket[model@long].

    Standard and long-context are kept apart so board prices them with
    whatever rules.json says today. usage.iterations splits a request into the
    executor's and any advisor's share, each with its own model.
    """
    u = req["usage"]
    for it in [i for i in (u.get("iterations") or []) if isinstance(i, dict)] or [u]:
        model = it.get("model") or req["model"]
        cc = it.get("cache_creation") or {}
        cw1h = cc.get("ephemeral_1h_input_tokens", 0)
        cw5m = cc.get("ephemeral_5m_input_tokens", it.get("cache_creation_input_tokens", 0) - cw1h)
        total_in = it.get("input_tokens", 0) + it.get("cache_read_input_tokens", 0) + it.get("cache_creation_input_tokens", 0)
        long_at = (prices.get(model, {}).get("long_context") or {}).get("over_input_tokens")
        b = bucket[model + ("@long" if long_at and total_in > long_at else "")]
        b["input"] += it.get("input_tokens", 0)
        b["cache_write_5m"] += cw5m
        b["cache_write_1h"] += cw1h
        b["cache_read"] += it.get("cache_read_input_tokens", 0)
        b["output"] += it.get("output_tokens", 0)
        b["requests"] += 1


def harvest_file(path, prices):
    records = [json.loads(l) for l in open(path) if l.strip()]
    if not records or not in_this_repo(records):
        return None
    meta = load_json(path[:-6] + ".meta.json", {})
    run_id = records[0].get("agentId") or os.path.basename(path)[6:-6]
    agent = meta.get("agentType") or "unknown"
    ts = min((r["timestamp"] for r in records if r.get("timestamp")), key=ts_key)
    started = session_start(path) or ts
    prompt_hash = (load_json(path[:-6] + ".prefix.json", {}).get("state") or {}).get("systemHash")
    prompt = next((text_of(r["message"].get("content")) for r in records if r.get("type") == "user"), "")

    requests, models = group_requests(records), Counter()
    tool_calls, dups, advisor_calls, skills, seen = 0, 0, 0, [], set()
    handback, last_text = None, ""
    for r in records:
        if r.get("type") != "assistant":
            continue
        msg = r["message"]
        model = msg.get("model", "")
        if model and not model.startswith("<"):
            models[model] += 1
        text = text_of(msg.get("content"))
        if text.strip():
            last_text = text
        for block in msg.get("content") or []:
            if block.get("type") == "server_tool_use" and block.get("name") == "advisor":
                advisor_calls += 1  # "asking Fable": priced below at the advisor's own rates
            if block.get("type") != "tool_use":
                continue
            if block.get("name") == "SubagentHandback":
                handback = (block.get("input") or {}).get("message", "")
                continue
            if block.get("name") == "Skill":
                skills.append((block.get("input") or {}).get("skill", "?"))
            tool_calls += 1
            sig = block.get("name", "") + json.dumps(block.get("input"), sort_keys=True)
            dups += sig in seen
            seen.add(sig)
    report = handback if handback is not None else last_text

    errors = sum(
        1 for r in records if r.get("type") == "user" and isinstance(r["message"].get("content"), list)
        for c in r["message"]["content"] if isinstance(c, dict) and c.get("type") == "tool_result" and c.get("is_error"))

    # The first request is the cold start: system prompt, tools and task
    # written to cache before any work. Kept apart so the orchestrator score
    # can see how much of the delegated spend went to starting agents up.
    usage_by_model, startup = new_bucket(), new_bucket()
    for i, req in enumerate(requests):
        add_usage(usage_by_model, req, prices)
        if i == 0:
            add_usage(startup, req, prices)

    status_m = re.search(r"^(?:STATUS|VERDICT):\s*([A-Z_]+)", report, re.M)
    agent_file = os.path.join(AGENTS_DIR, f"{agent}.md")
    has_contract = os.path.exists(agent_file) and re.search(r"^(STATUS|VERDICT):", open(agent_file).read(), re.M)
    status = status_m.group(1) if status_m else ("UNPARSED" if has_contract else "DONE")

    item_m = re.search(r"^ITEM:\s*(\S+)", report, re.M) or re.search(r"([\w./-]+\.html)", prompt)
    item = item_m.group(1) if item_m else None
    if item and os.path.isabs(item):
        item = os.path.relpath(item, REPO)
    link_m = re.search(r"RUN:\s*([0-9a-f]{6,})(?:#(\d+))?", prompt)

    return {
        "run": run_id,
        "session": records[0].get("sessionId"),
        "ts": ts,
        "end_ts": max((r["timestamp"] for r in records if r.get("timestamp")), key=ts_key),
        "agent": agent,
        "version": agent_version(agent, started),
        "prompt_hash": prompt_hash,
        "model": models.most_common(1)[0][0] if models else "unknown",
        "item": item,
        "canary": os.path.basename(item) if item and item.startswith(CANARY_DIR) else None,
        "status": status,
        "findings": [] if job_of(agent) == "finding-verifier" else parse_findings(report),
        "learning": parse_learning(report),
        "verifies": {"run": link_m.group(1), "finding": int(link_m.group(2)) if link_m.group(2) else None} if link_m else None,
        "requests": len(requests),
        "tool_calls": tool_calls,
        "tool_errors": errors,
        "dup_calls": dups,
        "advisor_calls": advisor_calls,
        "skills": skills,
        "usage_by_model": freeze(usage_by_model),
        "startup_usage": freeze(startup),
    }


READ_ONLY_TOOLS = {"Read", "Grep", "Glob", "LS", "WebFetch", "WebSearch", "NotebookRead"}


def read_only(tool):
    """Tools that only gather information. On the main model, a turn of these is
    work a cheaper agent could have done. Bash is not counted: a read and a write
    cannot be told apart without parsing the command."""
    return tool in READ_ONLY_TOOLS or (tool.startswith("mcp__") and bool(
        re.search(r"(search|read|get|list|fetch|scrape|query)", tool.rsplit("__", 1)[-1])))


def harvest_session(main_path, team, prices):
    """The orchestrator's side of a session that spawned agents here.

    Main-model spend is counted from the turn of the first spawn to the turn
    that took in the last result; earlier chat and planning is not
    orchestration. Within that window, a turn whose tool calls are all
    read-only is work the main model kept for itself (hoarding).
    """
    records = [json.loads(l) for l in open(main_path) if l.strip()]
    ends = [ts_key(r["end_ts"]) for r in team if r.get("end_ts")]
    if not records or not ends or not in_this_repo(records):
        return None
    requests = [q for q in group_requests(records) if q["ts"]]
    spawns = [q["ts"] for q in requests for t in q["tools"] if t in ("Agent", "Task")]
    if not spawns:
        return None
    w0, last_end = min(map(ts_key, spawns)), max(ends)
    w1 = min((ts_key(q["ts"]) for q in requests if ts_key(q["ts"]) > last_end), default=last_end)
    window, hoard, main_requests, hoard_calls = new_bucket(), new_bucket(), 0, 0
    for q in requests:
        if w0 <= ts_key(q["ts"]) <= w1:
            main_requests += 1
            add_usage(window, q, prices)
            if q["tools"] and all(read_only(t) for t in q["tools"]):
                add_usage(hoard, q, prices)
                hoard_calls += len(q["tools"])
    start = next(r["timestamp"] for r in records if r.get("timestamp"))
    models = Counter(q["model"] for q in requests if q["model"] and not q["model"].startswith("<"))
    efforts = Counter(r["effort"] for r in records if r.get("type") == "assistant" and r.get("effort"))
    return {
        "session": next(r["sessionId"] for r in records if r.get("sessionId")),
        "start": start,
        "model": models.most_common(1)[0][0] if models else "unknown",
        "effort": efforts.most_common(1)[0][0] if efforts else "default",
        "claude_md": file_version("CLAUDE.md", start),
        "spawns": len(spawns),
        "main_requests": main_requests,
        "hoard_calls": hoard_calls,
        "window_usage": freeze(window),
        "hoard_usage": freeze(hoard),
    }


def harvest(session_transcript=None, quiet=False):
    prices = load_json(RULES, {}).get("prices_usd_per_mtok", {})
    ledger = {r["run"]: r for r in load_jsonl(RUNS)}
    found = 0
    for path in subagent_files(session_transcript):
        try:
            rec = harvest_file(path, prices)
        except Exception as e:  # one bad transcript must not stop the rest
            if not quiet:
                print(f"skip {path}: {e}", file=sys.stderr)
            continue
        if rec:
            ledger[rec["run"]] = rec  # the transcript wins while it still exists
            found += 1
    rows = sorted(ledger.values(), key=lambda r: (ts_key(r["ts"]), r["run"]))
    changed = write_jsonl(RUNS, rows)

    team_of = defaultdict(list)
    for r in rows:
        team_of[r["session"]].append(r)
    sessions = {s["session"]: s for s in load_jsonl(SESSIONS)}
    for main in {os.path.dirname(os.path.dirname(p)) + ".jsonl" for p in subagent_files(session_transcript)}:
        try:
            rec = harvest_session(main, team_of.get(os.path.basename(main)[:-6], []), prices) if os.path.exists(main) else None
        except Exception as e:
            if not quiet:
                print(f"skip {main}: {e}", file=sys.stderr)
            continue
        if rec:
            sessions[rec["session"]] = rec
    changed |= write_jsonl(SESSIONS, sorted(sessions.values(), key=lambda s: ts_key(s["start"])))
    if not quiet:
        print(f"harvest: {found} transcripts read, {len(rows)} runs and {len(sessions)} sessions in ledger, "
              f"{'updated' if changed else 'no change'}")
    return rows


# ------------------------------------------------------------------- scoring

def run_cost(run, rules):
    return usage_cost(run["usage_by_model"], rules)


def usage_cost(usage_by_model, rules):
    prices, mult = rules["prices_usd_per_mtok"], rules["cache_write_multiplier"]
    total = 0.0
    for key, u in usage_by_model.items():
        model, _, tier = key.partition("@")
        p = prices.get(model)
        if p is None:
            return None  # unpriced model: show '?' rather than a wrong number
        if tier == "long" and p.get("long_context"):
            p = {**p, **p["long_context"]}
        total += (u.get("input", 0) * p["input"]
                  + u.get("cache_write_5m", 0) * p["input"] * mult["5m"]
                  + u.get("cache_write_1h", 0) * p["input"] * mult["1h"]
                  + u.get("cache_read", 0) * p.get("cache_read", p["input"] * 0.1)
                  + u.get("output", 0) * p["output"]) / 1e6
    return total


def canary_verdicts(run, answers):
    """Match an auditor's findings on a canary against the answer key.

    Order: planted, bonus, neutral, trap. Anything left over is a false finding.
    Each planted or bonus item earns once per run; a repeat of it scores zero.
    Returns (truth per finding index, labels, planted ids hit, planted ids missed).
    """
    key = (answers.get(run["canary"]) or {}).get(job_of(run["agent"]))
    if key is None:
        return {}, {}, set(), set()
    truth, labels, hit, credited = {}, {}, set(), set()
    for i, f in enumerate(run["findings"], 1):
        text, cls = f["text"], f["class"]

        def matches(item):
            return (not item.get("classes") or cls in item["classes"]) and (
                not item.get("match") or re.search(item["match"], text, re.I))

        planted = next((p for p in key.get("planted", []) if matches(p)), None)
        bonus = next((p for p in key.get("bonus", []) if matches(p)), None)
        trap = next((t for t in key.get("traps", []) if matches(t)), None)
        credit = planted or bonus
        if credit and credit["id"] in credited:
            # One defect reported twice earns once; splitting findings is not a strategy.
            truth[i], labels[i] = "neutral", "repeat:" + credit["id"]
        elif planted:
            truth[i], labels[i] = "real", "planted:" + planted["id"]
            hit.add(planted["id"])
            credited.add(planted["id"])
        elif bonus:
            truth[i], labels[i] = "real", "bonus:" + bonus["id"]
            credited.add(bonus["id"])
        elif cls in key.get("neutral", []):
            truth[i], labels[i] = "neutral", "neutral:" + cls
        elif trap:
            truth[i], labels[i] = "false", "trap:" + trap["id"]
        else:
            truth[i], labels[i] = "false", "unexpected"
    return truth, labels, hit, {p["id"] for p in key.get("planted", [])} - hit


def laplace(good, total):
    """Trust with no history is 0.5 and moves toward the observed rate."""
    return (good + 1) / (total + 2)


def setup_key(r):
    return (r["agent"], r["version"], r["model"])


def score(runs, rules, answers, rulings):
    V = rules["values_usd"]
    by_id = {r["run"]: r for r in runs}
    finding_rule = {(x["run"], x["finding"]): x["ruling"] for x in rulings if x.get("finding")}
    run_rule = defaultdict(list)
    for x in rulings:
        if not x.get("finding"):
            run_rule[x["run"]].append(x["ruling"])

    # Pass 1: the truth of every auditor finding. 'ground' is what verifiers
    # are graded against (canaries and rulings); verifier verdicts only fill
    # in truth for findings nothing stronger covers.
    truth, labels, canary_hit, canary_miss = {}, {}, {}, {}
    for r in runs:
        if r["canary"] and job_of(r["agent"]) != "finding-verifier":
            t, lab, hit, missed = canary_verdicts(r, answers)
            canary_hit[r["run"]], canary_miss[r["run"]] = hit, missed
            for i in t:
                truth[(r["run"], i)], labels[(r["run"], i)] = t[i], lab[i]
    for (rid, i), ruling in finding_rule.items():
        if ruling in ("real", "false"):
            truth[(rid, i)], labels[(rid, i)] = ruling, "ruled:" + ruling
    ground = dict(truth)
    verifier_of = {}
    for r in runs:
        v = r.get("verifies")
        if job_of(r["agent"]) != "finding-verifier" or not v or v["run"] not in by_id:
            continue
        n = v["finding"] or (1 if len(by_id[v["run"]]["findings"]) == 1 else None)
        if n is None:
            continue
        verifier_of[r["run"]] = (v["run"], n)
        if (v["run"], n) not in truth and r["status"] in ("CONFIRMED", "REFUTED"):
            truth[(v["run"], n)] = "real" if r["status"] == "CONFIRMED" else "false"
            labels[(v["run"], n)] = "verifier:" + r["status"].lower()

    # Pass 2: per-setup trust. Auditors: share of planted defects found.
    # Verifiers: share of graded verdicts that were right.
    recall_n, recall_hit, graded_n, graded_right = Counter(), Counter(), Counter(), Counter()
    verdict_grade = {}
    for r in runs:
        k = setup_key(r)
        if r["run"] in canary_hit:
            recall_hit[k] += len(canary_hit[r["run"]])
            recall_n[k] += len(canary_hit[r["run"]]) + len(canary_miss[r["run"]])
        g = ground.get(verifier_of.get(r["run"]))
        if g in ("real", "false") and r["status"] in ("CONFIRMED", "REFUTED"):
            right = (r["status"] == "CONFIRMED") == (g == "real")
            verdict_grade[r["run"]] = right
            graded_n[k] += 1
            graded_right[k] += right

    # Pass 3: value and cost of every run.
    scored = []
    for r in runs:
        k, job = setup_key(r), job_of(r["agent"])
        cost = run_cost(r, rules)
        value, notes, real, false = 0.0, [], 0, 0
        missed = canary_miss.get(r["run"], set())

        def add(v, note):
            nonlocal value
            value += v
            notes.append(f"{note} {v:+.2f}")

        if r["status"] in ("UNABLE", "UNPARSED"):
            add(V["failed_run"], r["status"].lower())
        elif job == "finding-verifier":
            if r["run"] in verdict_grade:
                ok = verdict_grade[r["run"]]
                add(V["verdict_right"] if ok else V["verdict_wrong"], "verdict right" if ok else "verdict WRONG")
            elif r["status"] in ("CONFIRMED", "REFUTED"):
                t = laplace(graded_right[k], graded_n[k])
                add(V["verdict_right"] * t, f"ungraded verdict x trust {t:.2f}")
        elif r["status"] in ("CLEAN", "FINDING"):
            for i in range(1, len(r["findings"]) + 1):
                t = truth.get((r["run"], i))
                real += t == "real"
                false += t == "false"
            if real:
                add(real * V["verified_finding"], f"{real} real")
            if false:
                add(false * V["false_finding"], f"{false} false")
            if missed:
                add(len(missed) * V["missed_planted"], "missed " + ",".join(sorted(missed)))
            if not (real or false or missed):
                if r["canary"]:  # nothing planted, nothing false reported: a verified clean
                    add(V["clean"], "clean (canary)")
                elif r["status"] == "CLEAN":
                    t = laplace(recall_hit[k], recall_n[k])
                    add(V["clean"] * t, f"clean x trust {t:.2f}")
        for ruling in run_rule.get(r["run"], []):
            add(V["ruled_good"] if ruling == "good" else V["ruled_bad"], "ruled " + ruling)
        bad = false or missed or r["status"] in ("UNABLE", "UNPARSED") or "bad" in run_rule.get(r["run"], [])
        scored.append({**r, "job": job, "setup": k, "cost": cost, "value": value,
                       "startup_cost": usage_cost(r["startup_usage"], rules) if r.get("startup_usage") else None,
                       "net": None if cost is None else value - cost, "real": real, "false": false,
                       "good": not bad, "notes": notes,
                       "labels": {i: labels.get((r["run"], i)) for i in range(1, len(r["findings"]) + 1)}})

    # Par: the cheapest good run of the same job on the same item, across every
    # setup in the league. Churn is what a run paid above it. A verifier's item
    # is the finding it judged, not the page. Par needs a rival: a run alone on
    # its item has no par, no churn and no record, rather than beating itself.
    good_costs, all_runs = defaultdict(list), Counter()
    for s in scored:
        f = verifier_of.get(s["run"])
        s["par_key"] = (s["job"], f"{f[0]}#{f[1]}" if f else s["item"])
        all_runs[s["par_key"]] += 1
        if s["good"] and s["cost"] is not None:
            good_costs[s["par_key"]].append(s["cost"])
    for s in scored:
        costs = good_costs.get(s["par_key"], [])
        has_rival = all_runs[s["par_key"]] > 1 and (len(costs) > 1 or bool(costs and not s["good"]))
        s["par"] = min(costs) if has_rival else None
        s["churn"] = None if s["par"] is None or s["cost"] is None else max(0.0, s["cost"] - s["par"])
        s["record"] = has_rival and s["good"] and s["cost"] == s["par"]
    return scored, (recall_hit, recall_n, graded_right, graded_n)


# --------------------------------------------------------------- leaderboard

def model_price(model, rules):
    p = rules["prices_usd_per_mtok"].get(model)
    return p["input"] if p else float("inf")


def mean_or_none(xs):
    xs = [x for x in xs if x is not None]
    return statistics.mean(xs) if xs else None


def leaderboard(scored, rules, stats):
    recall_hit, recall_n, graded_right, graded_n = stats
    T = rules["thresholds"]
    setups = defaultdict(list)
    for s in scored:
        setups[s["setup"]].append(s)
    leagues = defaultdict(list)
    for key, rs in setups.items():
        agent, version, model = key
        real, false = sum(r["real"] for r in rs), sum(r["false"] for r in rs)
        churns = [r["churn"] / r["cost"] for r in rs if r["churn"] is not None and r["cost"]]
        leagues[rs[0]["job"]].append({
            "agent": agent, "version": version, "model": model, "runs": len(rs),
            "first_seen": min((r["ts"] for r in rs), key=ts_key),
            "cost": mean_or_none(r["cost"] for r in rs), "net": mean_or_none(r["net"] for r in rs),
            "churn": statistics.median(churns) if churns else None,
            "precision": real / (real + false) if real + false else None, "judged": real + false,
            "recall": recall_hit[key] / recall_n[key] if recall_n[key] else None, "planted": recall_n[key],
            "verdict_acc": graded_right[key] / graded_n[key] if graded_n[key] else None, "graded": graded_n[key],
            "errors": sum(r["tool_errors"] for r in rs), "dups": sum(r["dup_calls"] for r in rs),
            "records": sum(r["record"] for r in rs),
        })

    for rows in leagues.values():
        rows.sort(key=lambda x: (x["net"] is None, -(x["net"] or 0)))
        costs = [x["cost"] for x in rows if x["cost"] is not None]
        med = statistics.median(costs) if costs else None
        cheapest = min(rows, key=lambda x: x["cost"] if x["cost"] is not None else float("inf"))
        cheapest_price = min(model_price(x["model"], rules) for x in rows)
        eligible = [r for r in rows if r["runs"] >= T["min_runs"]]
        for pos, x in enumerate(rows):
            badges, flags = [], []
            quality = [q for q in (x["precision"], x["recall"], x["verdict_acc"]) if q is not None]
            if med and x["cost"] is not None and x["cost"] <= T["featherweight_cost_ratio"] * med \
                    and quality and min(quality) >= T["featherweight_min_quality"]:
                badges.append("🪶 Featherweight")
            if x["judged"] >= T["sharpshooter_min_findings"] and x["precision"] >= T["sharpshooter_precision"]:
                badges.append("🎯 Sharpshooter")
            if x["recall"] == 1.0 and x["planted"] >= T["canary_hunter_min_planted"]:
                badges.append("🐤 Canary Hunter")
            if x["runs"] >= T["zero_churn_min_runs"] and x["errors"] == 0 and x["dups"] == 0:
                badges.append("🧹 Zero Churn")
            if x["records"]:
                badges.append(f"🏆 Course Record ×{x['records']}")
            if pos == 0 and len(rows) > 1 and model_price(x["model"], rules) > cheapest_price and (x["net"] or 0) > 0:
                badges.append("💎 Earned Its Keep")
            if pos == 0 and len(eligible) > 1 and eligible[0] is x and x["first_seen"] > eligible[1]["first_seen"]:
                badges.append("🧪 Innovator")

            if x["churn"] is not None and x["runs"] >= T["min_runs"] and x["churn"] >= T["churner_median_churn"]:
                flags.append("🔥 Churner")
            if x["recall"] is not None and x["planted"] >= T["lazy_clean_min_planted"] and x["recall"] < T["lazy_clean_recall"]:
                flags.append("🙈 Lazy CLEAN")
            if any(q is not None and n >= T["false_alarm_min_findings"] and q < T["false_alarm_precision"]
                   for q, n in ((x["precision"], x["judged"]), (x["verdict_acc"], x["graded"]))):
                flags.append("🔁 False Alarm")
            if x is not cheapest and x["cost"] and cheapest["cost"] and x["cost"] >= T["spendthrift_cost_ratio"] * cheapest["cost"]:
                if not any(a is not None and (b is None or a > b) for a, b in (
                        (x["precision"], cheapest["precision"]), (x["recall"], cheapest["recall"]),
                        (x["verdict_acc"], cheapest["verdict_acc"]))):
                    flags.append("💸 Spendthrift")

            if "🙈 Lazy CLEAN" in flags or "🔁 False Alarm" in flags:
                verdict = "FIRE"
            elif (x["net"] or 0) < 0 and ("🔥 Churner" in flags or "💸 Spendthrift" in flags):
                verdict = "FIRE" if x["runs"] >= T["min_runs"] else "WATCH"
            elif x["runs"] < T["min_runs"]:
                verdict = "ROOKIE"
            elif flags or (x["net"] or 0) < 0:
                verdict = "WATCH"
            else:
                verdict = "KEEP"
            x.update(badges=badges, flags=flags, verdict=verdict)
    return leagues


# -------------------------------------------------------------- orchestrator

def score_sessions(sessions, scored, rules, rulings):
    """Score each session as one job. The orchestrator's net is everything its
    team earned minus everything the job cost, main model included, so it wins
    by dividing work well: not spawning agents whose start-up costs more than
    their work, and not doing on the main model what a cheap agent could."""
    V = rules["values_usd"]
    ruled = defaultdict(list)
    for x in rulings:
        if not x.get("finding"):
            ruled[x["run"]].append(x["ruling"])
    team_of = defaultdict(list)
    for r in scored:
        team_of[r["session"]].append(r)
    out = []
    for S in sessions:
        team = team_of.get(S["session"], [])
        main_cost = usage_cost(S["window_usage"], rules)
        if not team or main_cost is None or any(r["cost"] is None for r in team):
            continue  # unpriced model somewhere: no number beats a wrong one
        sub_cost = sum(r["cost"] for r in team)
        startup = sum(r["startup_cost"] or 0 for r in team)
        hoard = usage_cost(S["hoard_usage"], rules) or 0.0
        value = sum(r["value"] for r in team) + sum(
            V["ruled_good"] if x == "good" else V["ruled_bad"] for x in ruled[S["session"]])
        total = main_cost + sub_cost
        items = sum(r["status"] != "DONE" for r in team)
        # Asking again about the same thing. Canaries are re-run on purpose.
        asked = Counter(r["par_key"] for r in team if not r["canary"] and r["par_key"][1])
        out.append({**S, "team": len(team), "items": items, "value": value, "net": value - total,
                    "main_cost": main_cost, "sub_cost": sub_cost, "total": total,
                    "startup_cost": startup, "hoard_cost": hoard,
                    "tiny": sum(1 for r in team if r["startup_cost"] is not None and r["cost"]
                                and r["startup_cost"] >= 0.5 * r["cost"]),
                    "reasks": sum(n - 1 for n in asked.values())})
    return out


def orchestrator_league(sessions, rules):
    T = rules["thresholds"]
    groups = defaultdict(list)
    for S in sessions:
        groups[(S["model"], S["effort"], S["claude_md"])].append(S)
    rows = []
    for (model, effort, claude_md), ss in groups.items():
        add = lambda k: sum(S[k] for S in ss)
        items, spawns = add("items"), add("spawns")
        rows.append({"model": model, "effort": effort, "claude_md": claude_md, "sessions": len(ss), "items": items,
                     "spawns": spawns, "first_seen": min((S["start"] for S in ss), key=ts_key),
                     "net_item": add("net") / items if items else None,
                     "cost_item": add("total") / items if items else None,
                     "main_share": add("main_cost") / add("total") if add("total") else None,
                     "startup_share": add("startup_cost") / add("sub_cost") if add("sub_cost") else None,
                     "hoard_share": add("hoard_cost") / add("total") if add("total") else None,
                     "tiny": add("tiny"), "reasks": add("reasks")})
    rows.sort(key=lambda x: (x["net_item"] is None, -(x["net_item"] or 0)))
    for pos, x in enumerate(rows):
        flags, badges = [], []
        if x["spawns"] >= 3 and ((x["startup_share"] or 0) >= T["over_divider_startup_share"]
                                 or x["tiny"] / x["spawns"] >= T["over_divider_tiny_share"]):
            flags.append("🪓 Over-Divider")
        if (x["hoard_share"] or 0) >= T["hoarder_share"]:
            flags.append("🐌 Hoarder")
        if x["spawns"] and x["reasks"] / x["spawns"] >= T["reasker_share"]:
            flags.append("🔁 Re-asker")
        if not flags and x["spawns"] >= 3 and (x["net_item"] or 0) > 0 \
                and (x["startup_share"] or 0) <= T["conductor_max_startup_share"] \
                and (x["hoard_share"] or 0) <= T["conductor_max_hoard_share"]:
            badges.append("🎼 Conductor")
        if pos == 0 and len(rows) > 1 and (x["net_item"] or 0) > 0:
            badges.append("🏅 Best Division")
        verdict = ("ROOKIE" if x["sessions"] < T["orchestrator_min_sessions"]
                   else "WATCH" if flags or (x["net_item"] or 0) < 0 else "KEEP")
        x.update(flags=flags, badges=badges, verdict=verdict)
    return rows


# ----------------------------------------------------------------- learnings

def norm(text):
    return re.sub(r"[^a-z0-9 ]+", "", re.sub(r"\s+", " ", text.lower())).strip()


def active_set(learnings, agent, at):
    return frozenset(l["id"] for l in learnings if l["agent"] == agent and l.get("added")
                     and ts_key(l["added"]) <= at and not (l.get("retired") and ts_key(l["retired"]) <= at))


def learning_windows(learnings, agent):
    """Split time into windows over which this agent's active learning set
    was constant: [(start, end, set)], start/end None meaning open-ended."""
    events = sorted({ts_key(t) for l in learnings if l["agent"] == agent
                     for t in (l.get("added"), l.get("retired")) if t})
    if not events:
        return []
    windows = [(None, events[0], frozenset())]
    for i, e in enumerate(events):
        windows.append((e, events[i + 1] if i + 1 < len(events) else None, active_set(learnings, agent, e)))
    return windows


def compare_learning(l, learnings, scored, T):
    """Net $/run with this learning vs without it, everything else equal.

    After = the window that opened when it was added. Before = every earlier
    window whose active set was the same minus this learning. So when one
    learning is retired and the next goes on trial in the same sync, the next
    is compared with the baseline both were missing, not with its
    predecessor's trial. Canary runs are the basis when both sides have some
    (same items, known answers); otherwise all runs.
    """
    if not l.get("added"):
        return None
    t0 = ts_key(l["added"])
    windows = learning_windows(learnings, l["agent"])
    after_w = next(w for w in windows if w[0] == t0)
    target = after_w[2] - {l["id"]}
    before_w = [w for w in windows if w[1] is not None and w[1] <= t0 and w[2] == target]

    def inside(s, w):
        t = ts_key(s["ts"])
        return (w[0] is None or t >= w[0]) and (w[1] is None or t < w[1])

    mine = [s for s in scored if s["agent"] == l["agent"] and s["net"] is not None]
    before = [s for s in mine if any(inside(s, w) for w in before_w)]
    after = [s for s in mine if inside(s, after_w)]
    cb, ca = [s for s in before if s["canary"]], [s for s in after if s["canary"]]
    basis, b, a = ("canary", cb, ca) if cb and ca else ("all", before, after)
    out = {"n_before": len(b), "n_after": len(a), "basis": basis,
           "net_before": mean_or_none(s["net"] for s in b), "net_after": mean_or_none(s["net"] for s in a),
           "cost_before": mean_or_none(s["cost"] for s in b), "cost_after": mean_or_none(s["cost"] for s in a),
           "confounded": len({(s["version"], s["model"]) for s in b + a}) > 1}
    out["delta"] = None if out["net_before"] is None or out["net_after"] is None else out["net_after"] - out["net_before"]
    enough = len(b) >= T["learning_min_runs"] and len(a) >= T["learning_min_runs"]
    out["call"] = "NO SIGNAL" if not enough or out["delta"] is None else "HELPS" if out["delta"] >= 0 else "HURTS"
    return out


def render_learnings_file(agent, learnings):
    active = [l for l in learnings if l["agent"] == agent and l["status"] in ("trial", "kept")]
    lines = [f"# Learnings — {agent}", "",
             "Rules earlier runs of this agent proposed. Each one is on trial or was kept because net $/run did not",
             "drop after it was added. They are advice. They never override the agent file: read-only, the source of",
             "truth, and the known-good lists always win. Managed by `.claude/arena/arena.py sync`; do not hand-edit.", ""]
    if not active:
        lines.append("No learnings yet.")
    for l in active:
        tag = "on trial" if l["status"] == "trial" else "kept"
        lines.append(f"- **{l['id']}** ({tag}) {l['text']}")
    return "\n".join(lines) + "\n"


def sync_learnings(runs, scored, rules, quiet=False):
    """The only writer of learnings. One trial at a time per agent, so every
    before/after comparison measures exactly one change."""
    T = rules["thresholds"]
    learnings = load_jsonl(LEARNINGS)
    by_norm = {(l["agent"], norm(l["text"])): l for l in learnings}
    next_id = 1 + max((int(l["id"][1:]) for l in learnings), default=0)
    log = []

    # 1. Fold proposals into pending entries. A retired learning stays retired.
    for r in runs:
        if not r.get("learning") or not os.path.exists(os.path.join(AGENTS_DIR, f"{r['agent']}.md")):
            continue
        key = (r["agent"], norm(r["learning"]))
        l = by_norm.get(key)
        if l is None:
            l = {"id": f"L{next_id}", "agent": r["agent"], "text": r["learning"], "status": "pending",
                 "proposed_by": [], "first_proposed": r["ts"], "added": None, "retired": None, "reason": None}
            next_id += 1
            learnings.append(l)
            by_norm[key] = l
        if r["run"] not in l["proposed_by"]:
            l["proposed_by"].append(r["run"])

    for agent in sorted({l["agent"] for l in learnings}):
        mine = [l for l in learnings if l["agent"] == agent]
        # 2. Judge the learning on trial.
        for l in mine:
            if l["status"] != "trial":
                continue
            c = compare_learning(l, learnings, scored, T)
            if c and c["call"] == "HELPS":
                l["status"], l["reason"] = "kept", f"net {c['delta']:+.4f}/run ({c['basis']})"
                log.append(f"{agent} {l['id']} kept: {l['reason']}")
            elif c and c["call"] == "HURTS":
                l["status"], l["retired"], l["reason"] = "retired", now(), f"hurt: net {c['delta']:+.4f}/run ({c['basis']})"
                log.append(f"{agent} {l['id']} retired: {l['reason']}")
        # 3. Nothing on trial: promote the most-proposed pending learning,
        #    evicting the weakest kept one if the agent is at its cap.
        if any(l["status"] == "trial" for l in mine):
            continue
        pending = sorted((l for l in mine if l["status"] == "pending"),
                         key=lambda l: (-len(l["proposed_by"]), ts_key(l["first_proposed"])))
        if not pending:
            continue
        kept = [l for l in mine if l["status"] == "kept"]
        if len(kept) >= T["max_active_learnings"]:
            def delta(l):
                c = compare_learning(l, learnings, scored, T)
                return c["delta"] if c and c["delta"] is not None else float("inf")
            weakest = min(kept, key=delta)
            weakest["status"], weakest["retired"], weakest["reason"] = "retired", now(), f"evicted for {pending[0]['id']}"
            log.append(f"{agent} {weakest['id']} evicted")
        pending[0]["status"], pending[0]["added"] = "trial", now()
        log.append(f"{agent} {pending[0]['id']} on trial: {pending[0]['text']}")

    learnings.sort(key=lambda l: int(l["id"][1:]))
    write_jsonl(LEARNINGS, learnings)
    for path in sorted(glob.glob(os.path.join(AGENTS_DIR, "*.md"))):
        agent = os.path.basename(path)[:-3]
        write_if_changed(os.path.join(LEARNINGS_DIR, f"{agent}.md"), render_learnings_file(agent, learnings))
    if not quiet:
        print("\n".join(log) or "sync: no learning changes")
    return learnings


# ----------------------------------------------------------------- rendering

def usd(v, places=4):
    return "?" if v is None else f"${v:,.{places}f}"


def pct(v):
    return "–" if v is None else f"{v:.0%}"


def learnings_table(learnings, scored, T):
    rows = ["| Agent | ID | Learning | Status | Runs before → after | Net $/run before → after | Δ | Call |",
            "|---|---|---|---|---|---|---:|---|"]
    for l in learnings:
        if l["status"] == "pending":
            continue
        c = compare_learning(l, learnings, scored, T) or {}
        note = " ⚠ definition or model changed" if c.get("confounded") else ""
        rows.append(f"| {l['agent']} | {l['id']} | {l['text'][:90]} | {l['status']} | "
                    f"{c.get('n_before', 0)} → {c.get('n_after', 0)} ({c.get('basis', '–')}) | "
                    f"{usd(c.get('net_before'))} → {usd(c.get('net_after'))} | {usd(c.get('delta'))} | "
                    f"{c.get('call', '–')}{note} |")
    pending = [l for l in learnings if l["status"] == "pending"]
    if pending:
        rows += ["", "Waiting for a trial slot (most-proposed first):", ""]
        rows += [f"- {l['agent']} {l['id']} ×{len(l['proposed_by'])}: {l['text'][:120]}"
                 for l in sorted(pending, key=lambda l: -len(l["proposed_by"]))]
    return rows


def render_orchestrators(rows):
    lines = ["## Orchestrator (main session)", "",
             "One row per main model · effort · CLAUDE.md version. A session is scored as one job: what its team earned "
             "minus everything the job cost, main model included, per graded item. Main share = main-model cost from "
             "first spawn to last result. Start-up share = share of agent spend that went to cold starts (over-division "
             "shows up here). Hoarding = share of cost spent on main-model turns that only read (under-division).", "",
             "| Setup | Sessions | Items | Net $/item | Cost $/item | Main share | Start-up share | Hoarding | Badges | Verdict |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---|---|"]
    for x in rows:
        lines.append(f"| {x['model'].replace('claude-', '')} · {x['effort']} · `CLAUDE.md@{x['claude_md']}` | {x['sessions']} | "
                     f"{x['items']} | {usd(x['net_item'])} | {usd(x['cost_item'])} | {pct(x['main_share'])} | "
                     f"{pct(x['startup_share'])} | {pct(x['hoard_share'])} | {' '.join(x['badges'] + x['flags']) or '–'} | "
                     f"**{x['verdict']}** |")
    return lines + [""]


def render(leagues, scored, learnings, T, orchestrators=()):
    lines = [
        "# Agent Arena — Leaderboard", "",
        f"Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} by `python3 .claude/arena/arena.py board`. "
        f"{len(scored)} runs, {usd(sum(s['cost'] or 0 for s in scored), 2)} at API list price.", "",
        "Net $/run = value earned − API cost. Churn = share of a run's cost above the cheapest correct run of the same "
        "job on the same item. Values and prices live in `rules.json`; editing them rescores everything.", "",
    ]
    if orchestrators:
        lines += render_orchestrators(orchestrators)
    for job in sorted(leagues):
        lines += [f"## {job}", "",
                  "| Setup | Model | Runs | Net $/run | Cost $/run | Churn | Precision | Planted found | Verdicts right | Badges | Verdict |",
                  "|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|"]
        for x in leagues[job]:
            frac = lambda q, n: f"{pct(q)} of {n}" if n else "–"
            lines.append(f"| `{x['agent']}@{x['version']}` | {x['model'].replace('claude-', '')} | {x['runs']} | "
                         f"{usd(x['net'])} | {usd(x['cost'])} | {pct(x['churn'])} | {frac(x['precision'], x['judged'])} | "
                         f"{frac(x['recall'], x['planted'])} | {frac(x['verdict_acc'], x['graded'])} | "
                         f"{' '.join(x['badges'] + x['flags']) or '–'} | **{x['verdict']}** |")
        lines.append("")
    lines += ["## Learnings — before vs after", ""]
    lines += learnings_table(learnings, scored, T) if learnings else ["No learnings proposed yet."]
    lines += ["", "## Badges and flags", "",
              "- 🪶 Featherweight — costs half the league median or less, and every quality measure is at least 80%.",
              "- 🎯 Sharpshooter — 90%+ of judged findings were real, over 5+ findings.",
              "- 🐤 Canary Hunter — found every planted defect, over 3+ planted defects.",
              "- 🧹 Zero Churn — no tool errors and no repeated identical calls over 5+ runs.",
              "- 🏆 Course Record — holds the cheapest correct run on an item.",
              "- 💎 Earned Its Keep — leads its league on a pricier model than the league's cheapest, with positive net.",
              "- 🧪 Innovator — the newest eligible setup in the league took first place.",
              "- 🔥 Churner — median run spends 50%+ above par.",
              "- 🙈 Lazy CLEAN — found under half the planted defects. Fireable on its own.",
              "- 🔁 False Alarm — under half of its findings or verdicts held up. Fireable on its own.",
              "- 💸 Spendthrift — 5×+ the cost of the league's cheapest setup with no better quality.",
              "- 🎼 Conductor — orchestrator with positive net per item, start-up share ≤ 35%, hoarding ≤ 15%, no flags.",
              "- 🏅 Best Division — top orchestrator setup by net per item.",
              "- 🪓 Over-Divider — 50%+ of agent spend went to cold starts, or half its agents cost more to start than to work.",
              "- 🐌 Hoarder — 40%+ of the job's cost was the main model doing read-only work itself.",
              "- 🔁 Re-asker — 20%+ of spawns asked again about an item already asked about (canaries excepted).", "",
              "ROOKIE = fewer than 5 runs. FIRE = Lazy CLEAN, False Alarm, or negative net while churning or overspending.", ""]
    return "\n".join(lines)


# ----------------------------------------------------------------------- cli

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    h = sub.add_parser("harvest")
    h.add_argument("--hook", action="store_true", help="Stop hook: read hook JSON on stdin, harvest that session, sync learnings, never fail")
    sub.add_parser("board")
    sub.add_parser("sync")
    sub.add_parser("learnings")
    sub.add_parser("sessions")
    rp = sub.add_parser("runs")
    rp.add_argument("--agent")
    rl = sub.add_parser("rule")
    rl.add_argument("target", help="<run id> or <run id>#<finding number>")
    rl.add_argument("ruling", choices=["real", "false", "good", "bad"])
    rl.add_argument("note", nargs="?", default="")
    a = ap.parse_args()

    if a.cmd == "harvest" and a.hook:
        try:
            runs = harvest(json.load(sys.stdin).get("transcript_path"), quiet=True)
            rules = load_json(RULES, {})
            scored, _ = score(runs, rules, load_json(ANSWERS, {}), load_jsonl(RULINGS))
            sync_learnings(runs, scored, rules, quiet=True)
        except Exception:
            pass  # a scorer must never block a session
        return
    if a.cmd == "harvest":
        harvest()
        return
    if a.cmd == "rule":
        rid, _, n = a.target.partition("#")
        if (a.ruling in ("real", "false")) != bool(n):
            sys.exit("real/false rule a finding (<run>#<n>); good/bad rule a whole run (<run>)")
        rows = load_jsonl(RULINGS) + [{"run": rid, "finding": int(n) if n else None, "ruling": a.ruling,
                                       "note": a.note, "ts": now()}]
        write_jsonl(RULINGS, rows)
        print(f"ruled {a.target} {a.ruling}")
        return

    runs = harvest(quiet=True)
    rules = load_json(RULES, {})
    scored, stats = score(runs, rules, load_json(ANSWERS, {}), load_jsonl(RULINGS))

    if a.cmd == "sync":
        sync_learnings(runs, scored, rules)
    elif a.cmd == "sessions":
        for S in score_sessions(load_jsonl(SESSIONS), scored, rules, load_jsonl(RULINGS)):
            print(f"{S['session']}  {S['model'].replace('claude-', '')} · {S['effort']} · CLAUDE.md@{S['claude_md']}  "
                  f"started {S['start'][:16]}")
            print(f"    {S['spawns']} spawns, {S['items']} graded items, net {usd(S['net'])} = value {usd(S['value'])} "
                  f"- main {usd(S['main_cost'])} - agents {usd(S['sub_cost'])}")
            print(f"    start-up {usd(S['startup_cost'])} ({pct(S['startup_cost'] / S['sub_cost'] if S['sub_cost'] else None)} of agent spend), "
                  f"{S['tiny']} start-up-dominated runs, hoarding {usd(S['hoard_cost'])} over {S['hoard_calls']} read-only calls, "
                  f"{S['reasks']} re-asks")
    elif a.cmd == "learnings":
        print("\n".join(learnings_table(load_jsonl(LEARNINGS), scored, rules["thresholds"])))
    elif a.cmd == "runs":
        for s in scored:
            if a.agent and s["agent"] != a.agent:
                continue
            churn = "–" if s["churn"] is None else f"{s['churn'] / s['cost']:.0%}" if s["cost"] else "0%"
            print(f"{s['run']}  {s['agent']}@{s['version']}  {s['model'].replace('claude-', '')}  {s['item'] or '-'}")
            print(f"    {s['status']:<9} cost {usd(s['cost'])}  net {usd(s['net'])}  churn {churn}  requests {s['requests']}"
                  f"  tools {s['tool_calls']}  errors {s['tool_errors']}  repeats {s['dup_calls']}")
            if s["notes"]:
                print("    " + "; ".join(s["notes"]))
            for i, lab in s["labels"].items():
                print(f"    #{i} {s['findings'][i - 1]['class']}: {lab or 'pending verification'}")
            if s.get("learning"):
                print(f"    LEARNING: {s['learning']}")
    else:  # board
        leagues = leaderboard(scored, rules, stats)
        orchestrators = orchestrator_league(score_sessions(load_jsonl(SESSIONS), scored, rules, load_jsonl(RULINGS)), rules)
        md = render(leagues, scored, load_jsonl(LEARNINGS), rules["thresholds"], orchestrators)
        write_if_changed(BOARD_MD, md)
        print(md)


if __name__ == "__main__":
    main()
