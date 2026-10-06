#!/usr/bin/env python3
"""The footprint on the screen, without an install: a real ontology, a pass-through for the page's
`/api/knowledge/*`, and check/footprint-screen.mjs driving the real static/knowledge.js against it.

    ./check/footprint-screen-check.py [port]

The web app proxies most of `/api/knowledge/<x>` one-to-one onto the ontology's `/v1/<x>`; this
does the same for the paths the map and the footprint use, and answers `/api/app-config` with an
open door. What the page cannot reach here (the review queue's own routes) it already treats as
absent, as it does on an install without them.
"""
import http.server, json, os, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18350
WEB = PORT + 1

T = tempfile.mkdtemp(prefix="footprint-screen-")
repo = os.path.join(T, "repo")
shutil.copytree(os.path.join(ROOT, "data", "repo"), repo, ignore=shutil.ignore_patterns(".git"))
for cmd in (["init", "-q"], ["config", "user.email", "s@r"], ["config", "user.name", "s"], ["add", "-A"], ["commit", "-qm", "as shipped"]):
    subprocess.run(["git", "-C", repo, *cmd], check=True, capture_output=True)
env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(PORT), "ONTOLOGY_WALKS": os.path.join(T, "walks"),
       "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), os.path.join(ROOT, "ontology")] if x)}
svc = subprocess.Popen([sys.executable, os.path.join(ROOT, "ontology", "service", "server.py")], env=env,
                       stdout=open(os.path.join(T, "svc.log"), "w"), stderr=subprocess.STDOUT)


class Pass(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _go(self, method):
        if self.path.startswith("/api/app-config"):
            body = json.dumps({"auth": "open", "auth_names_the_actor": False}).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(body); return
        if not self.path.startswith("/api/knowledge/"):
            self.send_response(404); self.end_headers(); return
        target = f"http://127.0.0.1:{PORT}/v1/" + self.path[len("/api/knowledge/"):]
        data = self.rfile.read(int(self.headers.get("Content-Length") or 0)) if method in ("POST", "PUT", "PATCH") else None
        req = urllib.request.Request(target, data=data, method=method,
                                     headers={"Content-Type": "application/json", "X-Knowledge-Actor": self.headers.get("X-Knowledge-Actor") or "screen"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r: code, body, ctype = r.status, r.read(), r.headers.get("Content-Type") or "application/json"
        except urllib.error.HTTPError as e: code, body, ctype = e.code, e.read(), "application/json"
        self.send_response(code); self.send_header("Content-Type", ctype); self.end_headers(); self.wfile.write(body)
    def do_GET(self): self._go("GET")
    def do_POST(self): self._go("POST")
    def do_PUT(self): self._go("PUT")


class Threaded(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True


try:
    for _ in range(80):
        try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1); break
        except Exception: time.sleep(0.25)
    else:
        sys.exit("  the ontology never answered — " + open(os.path.join(T, "svc.log")).read()[-1200:])
    web = Threaded(("127.0.0.1", WEB), Pass)
    threading.Thread(target=web.serve_forever, daemon=True).start()
    r = subprocess.run([os.path.join(ROOT, "check", "footprint-screen.mjs"), f"http://127.0.0.1:{WEB}"], cwd=ROOT)
    web.shutdown()
    code = r.returncode
finally:
    svc.terminate()
    try: svc.wait(5)
    except Exception: svc.kill()
    shutil.rmtree(T, ignore_errors=True)
sys.exit(code)
