#!/usr/bin/env python3
"""Every path the MCP server calls exists on the web app it is pointed at.

    ./check/mcp-routes-check.py

`.mcp.json` points an agent's MCP server at the web app (`/api/knowledge`), not at the ontology. So
every `/v1/...` the MCP server calls must have a route under `/api/knowledge/...`, or that tool works
in every check — which talks to the ontology directly — and fails on every install. On 2026-10-07
five did not: the resolver, the placement walk and the three writes that record a walk. The
footprint recorded nothing on a real install while 22 checks passed.

Static, no server. Reads the calls out of mcp/knowledge_mcp.py and the routes out of web/app.py and
compares them by shape — a `{param}` in a route matches any one segment.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mcp = open(os.path.join(ROOT, "mcp", "knowledge_mcp.py"), encoding="utf-8").read()
web = open(os.path.join(ROOT, "web", "app.py"), encoding="utf-8").read()

# Calls: api.json("/v1/..."), api.send("POST", "/v1/...", ...), api.text("/v1/..."), with f-strings.
calls = set()
for m in re.finditer(r'api\.(json|text)\(\s*f?"(/v1/[^"]*)"', mcp):
    calls.add(("GET", m.group(2)))
for m in re.finditer(r'api\.send\(\s*"([A-Z]+)",\s*f?"(/v1/[^"]*)"', mcp):
    calls.add((m.group(1), m.group(2)))
# Paths read through table_for/read_for come from tables the API printed — those are the shapes
# below, and the web app proxies them; the literal calls above are the ones a person wrote.

def shape(path):
    p = path.split("?", 1)[0]
    p = re.sub(r"\{[^}]+\}", "*", p)            # f-string fields and route params alike
    return [x for x in p.strip("/").split("/") if x]

routes = set()
for m in re.finditer(r'@_iris_route\("([A-Z]+)",\s*"/api/knowledge(/[^"]*)"', web):
    routes.add((m.group(1), m.group(2)))

def served(method, path):
    want = shape(path)[1:]                      # drop the leading v1
    for rm, rp in routes:
        if rm != method: continue
        have = shape(rp)
        if have and have[-1].startswith("*") and ":path" in rp:   # {rest:path}
            if len(want) >= len(have) - 1 and all(h == "*" or h == w for h, w in zip(have[:-1], want)): return True
        if len(have) == len(want) and all(h == "*" or w == "*" or h == w for h, w in zip(have, want)): return True
    return False

missing = sorted(f"{m} {p}" for m, p in calls if not served(m, p))
for x in missing: print(f"  FAIL the MCP server calls {x}, which the web app does not route")
print(f"\n{'ok  ' if not missing else 'FAIL'} {len(calls)} MCP calls, {len(routes)} web routes, {len(missing)} unrouted")
sys.exit(1 if missing else 0)
