#!/usr/bin/env python3
"""Score one agent's walk against the answer key, and keep the whole report.

The routing arm's results were being read by eye, which is not a record. This takes the agent's
report on stdin, pulls the addresses out of its **Source** section, compares them with `D_true`, and
appends everything — including the report verbatim — to a campaign file.

**Verbatim matters.** On the first six walks a fresh reader found two things the desk audit had
missed: a second "receipt threshold" of a different kind sitting in the same area, and a delegation
limit of 450 thousand KRW on a twelve-million-won purchase. Both were in the Notes. Neither would
have survived being summarised into a hit or a miss, and the second was a real defect in the corpus.

    ./bench/walkprompt.py h-perdiem-022-i | pbcopy       # ask
    ./bench/walkscore.py record --id h-perdiem-022-i --arm routing < report.md
    ./bench/walkscore.py report                          # the campaign so far

`needs: all` is honoured: a question that needs two documents is a hit only when both are named.
"""
import argparse, json, os, pathlib, re, sys, subprocess, time
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLD = ["eval/gold/hard.yaml", "eval/gold/hard-temporal.yaml", "eval/gold/hard-sample35.yaml"]
# Greedy, and `/` is outside the class so it stops before `/body` on its own. It was lazy with an
# optional `/body` and a `\b`, which matched "hard" out of "hard-accrual-v2": a hyphen is a word
# boundary, so the shortest match that satisfied the pattern was the first four characters. Every
# walk scored as a miss and the reported source read "hard".
ADDR = re.compile(r"/v1/nodes/([A-Za-z0-9._-]+)")


def gold(qid):
    for f in GOLD:
        p = ROOT / f
        if not p.exists(): continue
        for q in yaml.safe_load(p.read_text(encoding="utf-8"))["questions"]:
            if q["id"] == qid: return q
    sys.exit(f"  no question with id {qid}")


def sources(report):
    """Addresses from the Source section, falling back to the whole report.

    The section is what the agent says it answered from; addresses elsewhere are places it looked.
    Scoring on everything it opened would credit a walk for passing near the answer, which is the
    thing `routing-scoped` exists to keep separate.
    """
    m = re.search(r"\*\*Source\*\*:?(.*?)(?=\n\s*\d+\.\s*\*\*|\Z)", report, re.S | re.I)
    body = m.group(1) if m else report
    seen, out = set(), []
    for i in ADDR.findall(body):
        if i not in seen: seen.add(i); out.append(i)
    return out, bool(m)


def scored(q, got):
    """Does what the walk named satisfy the key?

    `D_alt` maps a `D_true` id to documents that carry the same answer — the prose page and the
    table page it points at, say. It **stands in for** that one entry; it is not simply added to
    what the walk named. Written as a flat list first, which quietly did the wrong thing under
    `needs: all`: a walk that named the substitute and the second required document still failed,
    because the substitute satisfied nothing. Per-entry is the only form that is right for both.

    An alternative goes in only when the document has been read and does carry the answer, it is
    recorded in eval/gold/AUDIT.md with the walk that surfaced it, and it is applied to **every**
    question keyed on that document rather than to the ones that happened to trip on it — then
    `rescore` re-runs both arms.
    """
    got = set(got)
    alt = q.get("D_alt") or {}
    ok = lambda m: m in got or bool(set(alt.get(m) or ()) & got)
    return all(map(ok, q["D_true"])) if q.get("needs") == "all" else any(map(ok, q["D_true"]))


def campaign_path(name):
    return ROOT / "eval" / "runs" / f"{name}.json"


def load(name):
    p = campaign_path(name)
    return json.loads(p.read_text()) if p.exists() else {"walks": []}


def cmd_record(a):
    q = gold(a.id)
    report = sys.stdin.read()
    if not report.strip(): sys.exit("  nothing on stdin")
    got, had_section = sources(report)
    hit = scored(q, got)
    cmds = len(re.findall(r"rmcli\.py", report))
    fp = subprocess.run([sys.executable, str(ROOT / "bench" / "crowd.py"), "fingerprint"],
                        capture_output=True, text=True,
                        env={**os.environ, "BENCH_EXTRA_CORPUS": "bench/corpus-hard"})
    data = load(a.campaign)
    data.setdefault("meta", {}).update(
        fingerprint=fp.stdout.strip().split()[-1] if fp.returncode == 0 else "?",
        use_when=os.environ.get("BENCH_USE_WHEN", "frozen"))
    data["walks"] = [w for w in data["walks"] if not (w["id"] == a.id and w["arm"] == a.arm)]
    data["walks"].append(dict(id=a.id, arm=a.arm, lever=q.get("lever"), family=q.get("family"),
                              needs=q.get("needs"), d_true=q["D_true"], sources=got, hit=hit,
                              commands=cmds, source_section=had_section,
                              at=time.strftime("%Y-%m-%dT%H:%M:%S"), report=report))
    campaign_path(a.campaign).parent.mkdir(parents=True, exist_ok=True)
    campaign_path(a.campaign).write_text(json.dumps(data, indent=1, ensure_ascii=False),
                                         encoding="utf-8")
    mark = "ok  " if hit else "MISS"
    print(f"  {mark} {a.id:<20} {a.arm:<16} {cmds:>2} calls   "
          f"{'·'.join(got[:3]) if got else 'no address reported'}"
          f"{'' if had_section else '   (no Source section — scored on the whole report)'}")


def cmd_rescore(a):
    """Re-score every recorded walk against the current keys, from the kept reports.

    A key that changes must change for both arms at once. Doing that by hand, one `record` at a
    time, is how you end up with a campaign scored under two different keys — so it is a command.
    Nothing is re-walked and no report is altered; only `hit` is recomputed.
    """
    data = load(a.campaign)
    changed = []
    for w in data["walks"]:
        q = gold(w["id"])
        got, _ = sources(w["report"])
        hit = scored(q, got)
        if hit != w["hit"]:
            changed.append((w["id"], w["arm"], w["hit"], hit)); w["hit"] = hit
        w["d_true"] = q["D_true"]
    campaign_path(a.campaign).write_text(json.dumps(data, indent=1, ensure_ascii=False),
                                         encoding="utf-8")
    print(f"  {len(data['walks'])} walks rescored · {len(changed)} changed")
    for i, arm, was, now in changed:
        print(f"    {i:<20} {arm:<16} {'ok' if was else 'MISS'} -> {'ok' if now else 'MISS'}")


def frame():
    """The fixed 50. A walk outside it is data, but it is not part of the denominator.

    Two questions were walked that are not in the sample — a lever was counted off the list of
    remaining ids rather than off the frame, and the fifth `stale-old` and a second `boundary`
    went out. Nothing about those two walks is wrong; what would be wrong is letting them into a
    rate whose denominator is supposed to be a frozen sample. So the report splits them out and
    says so, instead of a number that quietly means 52.
    """
    p = ROOT / "eval/gold/walk-sample50.yaml"
    return list(yaml.safe_load(p.read_text(encoding="utf-8"))["questions"]) if p.exists() else []


def cmd_report(a):
    import collections
    data = load(a.campaign)
    ws = data["walks"]
    if not ws: sys.exit("  nothing recorded yet")
    print(f"\n  {a.campaign}   fingerprint {data.get('meta',{}).get('fingerprint','?')}"
          f"   hop 0 {data.get('meta',{}).get('use_when','?')}\n")
    fr = set(frame())
    inside = [w for w in ws if not fr or w["id"] in fr]
    extra = [w for w in ws if fr and w["id"] not in fr]

    def table(rows):
        by = collections.defaultdict(lambda: [0, 0, 0])
        for w in rows:
            k = (w["arm"], w["lever"]); by[k][0] += w["hit"]; by[k][1] += 1; by[k][2] += w["commands"]
        print("    arm              lever         n    hit    calls/q")
        for (arm, lev), (h, n, c) in sorted(by.items()):
            print(f"    {arm:<16} {lev:<11} {n:>3}   {h/n:5.2f}   {c/n:5.1f}")

    table(inside)
    for arm in sorted({w["arm"] for w in inside}):
        got = [w for w in inside if w["arm"] == arm]
        left = [i for i in frame() if i not in {w["id"] for w in got}]
        print(f"\n    {arm}: {len(got)}/{len(fr)} of the frame"
              + (f" — {len(left)} not yet walked: {', '.join(left[:6])}"
                 f"{' …' if len(left) > 6 else ''}" if left else " — complete"))
    if extra:
        print(f"\n    outside the frame ({len(extra)}) — kept, not counted above")
        for w in extra: print(f"      {w['id']:<20} {w['arm']:<16} {w['lever']:<11} "
                              f"{'ok' if w['hit'] else 'MISS'}")
    bad = [w for w in ws if not w["hit"]]
    if bad:
        print(f"\n    misses ({len(bad)}) — read the reports, they say why")
        for w in bad: print(f"      {w['id']:<20} {w['arm']:<16} reported {w['sources'][:2]}")
    print()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign", default="2026-09-20-walks")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record")
    r.add_argument("--id", required=True)
    r.add_argument("--arm", required=True, choices=["routing", "routing+overlay"])
    sub.add_parser("report")
    sub.add_parser("rescore")
    a = ap.parse_args()
    {"record": cmd_record, "report": cmd_report, "rescore": cmd_rescore}[a.cmd](a)
