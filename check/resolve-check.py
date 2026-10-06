#!/usr/bin/env python3
"""The resolver, on the question it was built for and on the ways it could go quietly wrong.

    ./check/resolve-check.py

No server. `resolve` is a pure function over a map, so the map here is written by hand — and the
first one is the 2026-09-30 incident, reconstructed: two areas, a node with an alias, an edge to the
node that actually held the record, and ages that make the answer the newest thing on the map. The
question is the question that was asked, as it was asked.

The rest are the failures a resolver has that a search engine does not — because every match is a
literal string, every way a string can match wrongly is a way this can route wrongly. Latin inside
Latin (`how` in `show`), Latin against a Hangul particle (`ATL에서`), a short alias that is also a
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
# The record of the reclaim lived on `relay`, under services, four levels down. "ATL" was said. `atlas`
# carries the alias, `relay` shares its network — an edge — and `relay` is the newest thing on the map.
REGIONS = [
    {"dir": "ops",   "key": "OPS",   "representative": "ops",
     "use_when": "점검 · 긴급배포 · 장애 대응 · 점검 도구"},
    {"dir": "services", "key": "SERVICES", "representative": "services",
     "use_when": "서비스 구성 및 운영 환경"},
]
NODES = [
    {"id": "ops",   "name": "Ops",   "region": "ops",   "aliases": [], "one_liner": "운영"},
    {"id": "services", "name": "Services", "region": "services", "aliases": [], "one_liner": "게임"},
    {"id": "incidents-atlas", "name": "ATL 장애 기록", "region": "ops", "aliases": [],
     "one_liner": "ATL 서비스 장애와 대응"},
    {"id": "atlas", "name": "Atlas Shop", "region": "services", "aliases": ["ATL", "아틀라스", {"name": "AtL", "scope": "kr"}],
     "one_liner": "Atlas Prod 망 안의 서비스"},
    {"id": "relay", "name": "Relay", "region": "services", "aliases": ["릴레이"],
     "one_liner": "예비 서버 2대는 2026-09-30 반납"},
    {"id": "relay-us-east-1", "name": "relay-us-east-1", "region": "services", "aliases": [], "one_liner": "US East host"},
    {"id": "nca", "name": "NCA", "region": "services", "aliases": [], "one_liner": "region group"},
]
EDGES = [
    {"from": "atlas", "rel": "SHARES_NETWORK", "to": "relay"},
    {"from": "relay", "rel": "HAS_HOST", "to": "relay-us-east-1"},   # a second hop; must not be taken
    {"from": "incidents-atlas", "rel": "ABOUT", "to": "atlas"},
]
AGES = {
    "ops":   {"changed": "2026-09-01T00:00:00Z"},
    "services": {"route_since": "2026-06-01T00:00:00Z", "changed": "2026-09-30T02:00:00Z"},
    "incidents-atlas": {"changed": "2026-09-30T01:00:00Z"},
    "atlas": {"changed": "2026-09-12T00:00:00Z"},
    "relay": {"changed": "2026-09-30T03:00:00Z"},
    "relay-us-east-1": {"changed": "2026-09-30T03:00:00Z"},
}


def R(q, **kw):
    return resolve(q, nodes=NODES, edges=EDGES, regions=REGIONS, ages=AGES, revision="r1", **kw)


# ── 1. the question that was asked ────────────────────────────────────────────
r = R("ATL에서 가장 최근에 한 작업은 뭐야?")
ids = [n["is"] for n in r["names"]]
check("the incident: 'ATL' resolves through its alias", "atlas" in ids, str(ids))
check("  and one hop along the map's edge reaches relay", "relay" in ids, str(ids))
check("  the edge is named as the reason", any(n["is"] == "relay" and n["via"].startswith("edge SHARES_NETWORK") for n in r["names"]),
      str([(n["is"], n["via"]) for n in r["names"]]))
check("  and incidents-atlas, which is ABOUT atlas, comes too", "incidents-atlas" in ids, str(ids))
check("  but not the host two hops away", "relay-us-east-1" not in ids, str(ids))
check("  '가장 최근' is read as latest", r["ask"]["kind"] == "latest", str(r["ask"]))
check("  so the newest changed leads — relay, 2026-09-30", r["start"][0] == "/v1/nodes/relay", str(r["start"]))
check("  the restatement names services, the area that was never opened", "services" in r["restated"], r["restated"])
check("  and says what it is in the asker's script", "가장 최근에 바뀐 기록" in r["restated"], r["restated"])
check("  hop 0 comes with it, both areas", sorted(a["area"] for a in r["areas"]) == ["ops", "services"], str(r["areas"]))
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
check("Latin against a Hangul particle: ATL에서 matches", "atlas" in [n["is"] for n in R("ATL에서 뭐 했어")["names"]])
check("Latin inside Latin does not: 'oatlx' is not atlas", "atlas" not in [n["is"] for n in R("the oatlx thing")["names"]])
check("case does not matter: 'atlas'", "atlas" in [n["is"] for n in R("atlas 최근")["names"]])
check("a scoped alias {name, scope} resolves: AtL", "atlas" in [n["is"] for n in R("AtL 서버")["names"]])
check("a Hangul alias resolves: 아틀라스", "atlas" in [n["is"] for n in R("아틀라스 언제 바꿨어")["names"]])
check("a Hangul alias resolves: 릴레이", "relay" in [n["is"] for n in R("릴레이 담당")["names"]])
check("the longer name wins: relay-us-east-1 is the host, not relay via the host",
      [n for n in R("relay-us-east-1 상태")["names"] if n["is"] == "relay-us-east-1"][0]["via"] == "name")
check("a node reached by two of its names is one row",
      [n["is"] for n in R("Atlas Shop ATL")["names"]].count("atlas") == 1)
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
r = R("ATL 담당 누구야")
check("not latest: what was named leads, what an edge reached follows",
      r["start"][0] == "/v1/nodes/atlas" and "/v1/nodes/relay" in r["start"][1:], str(r["start"]))

# ── 6. the language of the restatement follows the question ───────────────────
check("English question, English restatement", "the most recently changed record" in R("ATL latest")["restated"])
g = next(a for a in R("x")["areas"] if a["area"] == "services")
check("area rows carry their representative's age, both halves",
      g["changed"] == "2026-09-30T02:00:00Z" and g["route_since"] == "2026-06-01T00:00:00Z", str(g))

# ── 7. the absence sentence is the caller's when they have one ───────────────
check("a supplied absence sentence is used verbatim", R("x", absence="LINK DOWN — cannot claim")["absence"].startswith("LINK DOWN"))

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
