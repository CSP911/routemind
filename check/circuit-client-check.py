#!/usr/bin/env python3
"""The circuit's client, against far ends that misbehave — no install needed.

    ./check/circuit-client-check.py

Three fake far ends, each a few lines of http.server:

  redirect   mints a session, then answers every read with a 302 to a second server that records
             what it was sent. A circuit must not follow it: the session rides in a header, and the
             plain-http check only ever saw the address the circuit was opened with. Found 2026-10-10,
             when the second server received `X-Peer-Token: <session>`.
  no key     answers the mint with 501 — the far end has KNOWLEDGE_CIRCUIT_TOKEN empty. The circuit
             used to say "refused the token", which sends the reader looking at their key.
  wrong url  answers 404 — the reader gave /api/knowledge, or the wrong host. Same.

And the name a circuit takes when none is given: from the address, so `127.0.0.1:<port>` works. It
was the bare host, and a dot is not allowed in a name, so every address but `localhost` was refused.
"""
import http.server, json, os, sys, threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "mcp"))
import knowledge_mcp as M                                            # noqa: E402

results = []
def check(name, cond, extra=""):
    results.append(("ok   " if cond else "FAIL ") + name + ("" if cond or not extra else f"   — {str(extra)[:200]}"))

seen = []                       # what the redirect's target was sent


def serve(handler):
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s, s.server_address[1]


class Sink(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        seen.append(self.headers.get("X-Peer-Token") or "")
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(b'{"regions": []}')


sink, SINK = serve(Sink)


class Redirect(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(json.dumps({"token": "SESSION-MUST-NOT-LEAK", "expires_in": 60}).encode())
    def do_GET(self):
        self.send_response(302); self.send_header("Location", f"http://127.0.0.1:{SINK}/v1/export/regions"); self.end_headers()


def status(code):
    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_POST(self):
            self.send_response(code); self.send_header("Content-Type", "application/json"); self.end_headers()
            self.wfile.write(b'{"error": "nope"}')
        do_GET = do_POST
    return H


_, RED = serve(Redirect)
_, NOKEY = serve(status(501))
_, WRONG = serve(status(404))

out = M.circuit_call({"op": "open", "url": f"http://127.0.0.1:{RED}", "token": "enrol"})
check("a far end that redirects: the circuit does not open", "Could not open circuit" in out and "redirect" in out, out)
check("  and the session it minted never reaches the host it was redirected to", "SESSION-MUST-NOT-LEAK" not in seen, seen)
check("  the name was made from the address, dots and port and all", f"127-0-0-1-{RED}" in out, out)

out = M.circuit_call({"op": "open", "url": f"http://127.0.0.1:{NOKEY}", "token": "enrol", "name": "nokey"})
check("a far end with no circuit key says so, and names the setting", "KNOWLEDGE_CIRCUIT_TOKEN" in out and "refused the token" not in out, out)

out = M.circuit_call({"op": "open", "url": f"http://127.0.0.1:{WRONG}", "token": "enrol", "name": "wrong"})
check("a wrong address says to give the install's own address", "without /api/knowledge" in out, out)

# A key kept out of the conversation: KNOWLEDGE_CIRCUIT_KEYS fills it in for an address opened alone.
os.environ["KNOWLEDGE_CIRCUIT_KEYS"] = f"http://127.0.0.1:{WRONG}/knowledge=from-env"
check("a key in KNOWLEDGE_CIRCUIT_KEYS is found for the address, page path and all",
      M._circuit_key_for(f"http://127.0.0.1:{WRONG}") == "from-env" and M._circuit_key_for("http://elsewhere") == "")
out = M.circuit_call({"op": "open", "url": "http://elsewhere.invalid"})
check("  and an address with no key anywhere says how to keep one out of the conversation", "KNOWLEDGE_CIRCUIT_KEYS" in out, out)

print("\n".join(results))
n = sum(r.startswith("FAIL") for r in results)
print(f"\n{n} failed of {len(results)}")
sys.exit(1 if n else 0)
