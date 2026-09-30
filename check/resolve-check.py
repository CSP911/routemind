#!/usr/bin/env python3
"""The resolver, on the question it was built for and on the ways it could go quietly wrong.

    ./check/resolve-check.py

No server. `resolve` is a pure function over a map, so the map here is written by hand — and the
first one is the 2026-09-30 incident, reconstructed: two areas, a node with an alias, an edge to the
node that actually held the record, and ages that make the answer the newest thing on the map. The
question is the question that was asked, as it was asked.

The rest are the failures a resolver has that a search engine does not — because every match is a
literal string, every way a string can match wrongly is a way this can route wrongly. Latin inside
Latin (`how` in `show`), Latin against a Hangul particle (`BNS에서`), a short alias that is also a
word, a second hop that would pull in the neighbourhood.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ontology"))
from service.resolve import resolve, ask_of                              # noqa: E402

results = []


def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {extra}"))
    return bool(cond)


# ── the 2026-09-30 map, as it was ──────────────────────────────────────────────
# The record of the reclaim lived on `neo`, under games, four levels down. "BNS" was said. `bns`
# carries the alias, `neo` shares its VPC — an edge — and `neo` is the newest thing on the map.
REGIONS = [
    {"dir": "ops",   "key": "OPS",   "representative": "ops",
     "use_when": "점검 · 긴급배포 · 장애 대응 · 점검 도구 · 신규월드 구축"},
    {"dir": "games", "key": "GAMES", "representative": "games",
     "use_when": "게임 구성 및 서비스 환경"},
]
NODES = [
    {"id": "ops",   "name": "Ops",   "region": "ops",   "aliases": [], "one_liner": "운영"},
    {"id": "games", "name": "Games", "region": "games", "aliases": [], "one_liner": "게임"},
    {"id": "incidents-bns", "name": "BNS 장애 기록", "region": "ops", "aliases": [],
     "one_liner": "BNS 서비스 장애와 대응"},
    {"id": "bns", "name": "Blade & Soul", "region": "games", "aliases": ["BNS", "블소", {"name": "BnS", "scope": "kr"}],
     "one_liner": "BnS Prod VPC 안의 게임 서비스"},
    {"id": "neo", "name": "Neo", "region": "games", "aliases": ["네오"],
     "one_liner": "부스트 2대는 2026-09-30 회수"},
    {"id": "neo-us-east-1", "name": "neo-us-east-1", "region": "games", "aliases": [], "one_liner": "US East host"},
    {"id": "nca", "name": "NCA", "region": "games", "aliases": [], "one_liner": "region group"},
]
EDGES = [
    {"from": "bns", "rel": "SHARES_VPC", "to": "neo"},
    {"from": "neo", "rel": "HAS_HOST", "to": "neo-us-east-1"},   # a second hop; must not be taken
    {"from": "incidents-bns", "rel": "ABOUT", "to": "bns"},
]
AGES = {
    "ops":   {"changed": "2026-09-01T00:00:00Z"},
    "games": {"route_since": "2026-06-01T00:00:00Z", "changed": "2026-09-30T02:00:00Z"},
    "incidents-bns": {"changed": "2026-09-30T01:00:00Z"},
    "bns": {"changed": "2026-09-12T00:00:00Z"},
    "neo": {"changed": "2026-09-30T03:00:00Z"},
    "neo-us-east-1": {"changed": "2026-09-30T03:00:00Z"},
}


def R(q, **kw):
    return resolve(q, nodes=NODES, edges=EDGES, regions=REGIONS, ages=AGES, revision="r1", **kw)


# ── 1. the question that was asked ────────────────────────────────────────────
r = R("BNS에서 가장 최근에 한 작업은 뭐야?")
ids = [n["is"] for n in r["names"]]
check("the incident: 'BNS' resolves through its alias", "bns" in ids, str(ids))
check("  and one hop along the map's edge reaches neo", "neo" in ids, str(ids))
check("  the edge is named as the reason", any(n["is"] == "neo" and n["via"].startswith("edge SHARES_VPC") for n in r["names"]),
      str([(n["is"], n["via"]) for n in r["names"]]))
check("  and incidents-bns, which is ABOUT bns, comes too", "incidents-bns" in ids, str(ids))
check("  but not the host two hops away", "neo-us-east-1" not in ids, str(ids))
check("  '가장 최근' is read as latest", r["ask"]["kind"] == "latest", str(r["ask"]))
check("  so the newest changed leads — neo, 2026-09-30", r["start"][0] == "/v1/nodes/neo", str(r["start"]))
check("  the restatement names games, the area that was never opened", "games" in r["restated"], r["restated"])
check("  and says what it is in the asker's script", "가장 최근에 바뀐 기록" in r["restated"], r["restated"])
check("  hop 0 comes with it, both areas", sorted(a["area"] for a in r["areas"]) == ["games", "ops"], str(r["areas"]))
check("  and the absence sentence is attached", "absent" in r["absence"])
check("  resolved, valid while r1", r["resolved"] and r["valid_while"] == "r1")
check("  an absence is never cached", r["cache"]["absence"] == "never")

# ── 2. NXDOMAIN ───────────────────────────────────────────────────────────────
r = R("XYZ 담당자가 누구야?")
check("a name the map does not know: not resolved", not r["resolved"] and r["names"] == [], str(r["names"]))
check("  the ask is still read (who)", r["ask"]["kind"] == "who", str(r["ask"]))
check("  hop 0 still comes — absence is claimed from there, not here", len(r["areas"]) == 2)
check("  and the restatement says the name is unknown, not that the thing is",
      "없음" in r["restated"] and "여기에 없음" in r["restated"], r["restated"])
r = R("who owns the XYZ service?")
check("  same in English", not r["resolved"] and "not here" in r["restated"], r["restated"])

# ── 3. how strings match, which is the whole risk ─────────────────────────────
check("Latin against a Hangul particle: BNS에서 matches", "bns" in [n["is"] for n in R("BNS에서 뭐 했어")["names"]])
check("Latin inside Latin does not: 'obnsx' is not bns", "bns" not in [n["is"] for n in R("the obnsx thing")["names"]])
check("case does not matter: 'bns'", "bns" in [n["is"] for n in R("bns 최근")["names"]])
check("a scoped alias {name, scope} resolves: BnS", "bns" in [n["is"] for n in R("BnS 서버")["names"]])
check("a Hangul alias resolves: 블소", "bns" in [n["is"] for n in R("블소 언제 바꿨어")["names"]])
check("a Hangul alias resolves: 네오", "neo" in [n["is"] for n in R("네오 담당")["names"]])
check("the longer name wins: neo-us-east-1 is the host, not neo via the host",
      [n for n in R("neo-us-east-1 상태")["names"] if n["is"] == "neo-us-east-1"][0]["via"] == "name")
check("a node reached by two of its names is one row",
      [n["is"] for n in R("Blade & Soul BNS")["names"]].count("bns") == 1)
check("'how' does not fire inside 'show'", ask_of("show me the records")["kind"] != "how", str(ask_of("show me the records")))
check("'last' does not fire inside 'blast'", ask_of("blast radius")["kind"] != "latest")

# ── 4. every ask kind, by a word from each script ─────────────────────────────
for q, kind in [("최근 바뀐 게 뭐야", "latest"), ("what changed most recently", "latest"),
                ("언제까지 내야 해", "when"), ("by when is it due", "when"),
                ("누가 담당이야", "who"), ("who is in charge", "who"),
                ("어떻게 등록해", "how"), ("what are the steps", "how"),
                ("이거 해도 돼요?", "whether"), ("can I claim it", "whether"),
                ("이게 뭐야", "what"), ("tell me about it", "what")]:
    a = ask_of(q)
    check(f"ask: {q!r} → {kind}", a["kind"] == kind, f"got {a['kind']} on {a['said']!r}")

# ── 5. order when it is not `latest` ──────────────────────────────────────────
r = R("BNS 담당 누구야")
check("not latest: what was named leads, what an edge reached follows",
      r["start"][0] == "/v1/nodes/bns" and "/v1/nodes/neo" in r["start"][1:], str(r["start"]))

# ── 6. the language of the restatement follows the question ───────────────────
check("English question, English restatement", "the most recently changed record" in R("BNS latest")["restated"])
g = next(a for a in R("x")["areas"] if a["area"] == "games")
check("area rows carry their representative's age, both halves",
      g["changed"] == "2026-09-30T02:00:00Z" and g["route_since"] == "2026-06-01T00:00:00Z", str(g))

# ── 7. the absence sentence is the caller's when they have one ───────────────
check("a supplied absence sentence is used verbatim", R("x", absence="LINK DOWN — cannot claim")["absence"].startswith("LINK DOWN"))

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
