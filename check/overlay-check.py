#!/usr/bin/env python3
"""Overlays end to end, on a throwaway ontology — through the MCP server, the way an agent uses them.

    ./check/overlay-check.py [port]

docs/OVERLAY.md is the contract. What this proves:
  * an install without an overlay store offers no overlay tool and says nothing about one
  * with one, the instructions carry the flow, and the tool is listed
  * create → the one table holding every member, with the absence line on it
  * add / remove narrow it; close records what was used, and says when it was reached rather than named
  * the refusals an agent will actually meet come back as sentences, not stack traces
Nothing here touches a live install: the ontology runs from this checkout on a temp directory.
"""
import atexit, json, os, shutil, subprocess, sys, tempfile, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8129
results, procs = [], []


def check(name, cond, extra=""):
    results.append(("ok  " if cond else "FAIL") + " " + name + ("" if cond or not extra else f"   — {extra}"))


# A run that stopped early used to print a summary that read exactly like a clean one. The results
# list holds what ran, `_end` is an atexit handler so it prints whatever crashed the script, and
# "0 failed of 29" is then true of the 29 that ran and silent about the 40 that did not. The exit
# code was 1, so nothing automated was fooled — but the line a person reads said the run passed, and
# that is the one place a check must not be wrong about itself. Appended to on the last line.
finished = []


@atexit.register
def _end():
    for p in procs:
        try: p.terminate()
        except Exception: pass
    if results:
        print("\n".join(results))
        n = sum(r.startswith("FAIL") for r in results)
        print(f"\n{n} failed of {len(results)}" if finished else
              f"\n{n} failed of the {len(results)} that ran — but THE RUN STOPPED EARLY and the rest "
              f"never ran, so this is not a pass. What stopped it is printed above these results.")
    shutil.rmtree(T, ignore_errors=True)


T = tempfile.mkdtemp(prefix="overlay-check-")
repo = os.path.join(T, "repo")
shutil.copytree(os.path.join(ROOT, "seed"), repo)
for a in (["init", "-q"], ["add", "-A"], ["-c", "user.name=seed", "-c", "user.email=s@l", "commit", "-qm", "seed"]):
    subprocess.run(["git", "-C", repo, *a], check=True)


def start(port, overlays):
    env = {**os.environ, "ONTOLOGY_DATA": repo, "ONTOLOGY_PUBLISH": os.path.join(T, f"publish{port}"), "PORT": str(port)}
    for k in [k for k in env if k.startswith("ONTOLOGY_LLM_") or k == "ONTOLOGY_OVERLAYS"]: env.pop(k)
    if overlays: env["ONTOLOGY_OVERLAYS"] = os.path.join(T, "overlays")
    p = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")], env=env,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    procs.append(p)
    for _ in range(60):
        try: urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=1); return
        except Exception: time.sleep(0.25)
    raise SystemExit(f"ontology on {port} did not start")


def post(port, path, body):
    req = urllib.request.Request(f"http://127.0.0.1:{port}/v1{path}", data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


class Mcp:
    def __init__(self, port):
        self.p = subprocess.Popen([sys.executable, os.path.join(ROOT, "mcp", "knowledge_mcp.py"),
                                   "--api", f"http://127.0.0.1:{port}/v1", "--actor", "overlay-check"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)
        procs.append(self.p); self.n = 0

    def call(self, method, params=None):
        self.n += 1
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": self.n, "method": method, "params": params or {}}) + "\n")
        self.p.stdin.flush()
        return json.loads(self.p.stdout.readline())

    def tool(self, name, args):
        r = self.call("tools/call", {"name": name, "arguments": args})["result"]
        return r["content"][0]["text"], r["isError"]


# Something to work with: an area with a node holding a document, and a second area.
start(PORT, overlays=True)
post(PORT, "/regions", {"source": "alpha", "core_description": "the first area", "representative": {
    "id": "alpha-core", "name": "Alpha", "one_liner": "what alpha is", "use_when": "when alpha is the question"}})
post(PORT, "/nodes", {"id": "shelf", "name": "Shelf", "region": "alpha", "one_liner": "where things stand", "parent": "alpha-core"})
req = urllib.request.Request(f"http://127.0.0.1:{PORT}/v1/nodes/shelf/files/rules.md", method="PUT",
                             data=json.dumps({"description": "the shelving rules", "content": "# Rules\n\nA1-A9 on shelf E."}).encode(),
                             headers={"Content-Type": "application/json"})
urllib.request.urlopen(req, timeout=30)
post(PORT, "/regions", {"source": "beta", "core_description": "the second area", "representative": {
    "id": "beta-core", "name": "Beta", "one_liner": "what beta is", "use_when": "when beta is the question"}})

# Without a store: no tool, no flow.
start(PORT + 1, overlays=False)
bare = Mcp(PORT + 1)
init = bare.call("initialize", {"protocolVersion": "2024-11-05"})["result"]
names = [t["name"] for t in bare.call("tools/list")["result"]["tools"]]
check("no store: no overlay tool", "knowledge_overlay" not in names, names)
check("no store: the instructions do not mention one", "knowledge_overlay" not in init["instructions"])

m = Mcp(PORT)
init = m.call("initialize", {"protocolVersion": "2024-11-05"})["result"]
names = [t["name"] for t in m.call("tools/list")["result"]["tools"]]
check("with a store: the tool is listed", "knowledge_overlay" in names, names)
check("the instructions carry the flow", "knowledge_overlay { op: create" in init["instructions"] and "at most 3 times" in init["instructions"])

text, err = m.tool("knowledge_overlay", {"op": "create", "question": "where do A-shelf books go",
                                         "members": [{"address": "/v1/regions/alpha", "why": "shelving lives here"}]})
check("create answers with the table", not err and "OVERLAY ov" in text and "/v1/nodes/shelf" in text, text[:300])
check("  under the member's heading", "── /v1/regions/alpha — shelving lives here" in text)
check("  with the absence line on it", "does not mean it does not exist" in text)
oid = text.split()[1] if not err else ""

text, err = m.tool("knowledge_overlay", {"op": "add", "id": oid, "address": "/v1/nodes/shelf", "why": "the shelf itself"})
check("add narrows: the node's rows join", not err and "/v1/nodes/rules/body" in text, text[:400])
text, err = m.tool("knowledge_overlay", {"op": "remove", "id": oid, "address": "/v1/regions/alpha", "why": "the shelf is enough"})
check("remove drops the area's section", not err and "── /v1/regions/alpha" not in text and "── /v1/nodes/shelf" in text)

text, err = m.tool("knowledge_table", {"path": f"/v1/overlays/{oid}"})
check("knowledge_table reads an overlay too", not err and f"OVERLAY {oid}" in text)
text, err = m.tool("knowledge_read", {"path": f"/v1/overlays/{oid}"})
check("  and knowledge_read refuses it as a table", err and "is a table" in text)

text, err = m.tool("knowledge_overlay", {"op": "add", "id": oid, "address": "/v1/nodes/not-a-thing", "why": "guess"})
check("an address that does not resolve is refused, in words", err and "not an address this ontology serves" in text, text)
text, err = m.tool("knowledge_overlay", {"op": "add", "id": oid, "address": "/v1/regions/beta"})
check("a change with no why is refused", err and "why" in text, text)
text, err = m.tool("knowledge_overlay", {"op": "close", "id": oid, "outcome": "answered",
                                         "used": ["/v1/nodes/rules/body", "/v1/nodes/shelf"]})
check("close records what was used", not err and "closed — answered" in text, text)
check("  and says when it was reached, not named", "reached" in text and "member" in text, text)
text, err = m.tool("knowledge_overlay", {"op": "add", "id": oid, "address": "/v1/regions/beta", "why": "late"})
check("a closed overlay does not change", err and "409" in text, text)
text, err = m.tool("knowledge_overlay", {"op": "get"})
check("an op that needs an id says so", err and "needs the overlay's id" in text, text)

finished.append(True)
sys.exit(1 if any(r.startswith("FAIL") for r in results) else 0)
