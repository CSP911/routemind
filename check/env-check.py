#!/usr/bin/env python3
"""Every setting .env.example documents must actually reach a container.

    ./check/env-check.py

A variable named in .env.example that docker-compose.yml never passes through is a dead setting: the
person sets it, nothing reads it, and there is no error anywhere to tell them. Two of these have
shipped.

  * ONTOLOGY_HARNESS was never in docker-compose.yml, so `POST /v1/curator/proposals` answered 501 on
    every install ever made from that file. The review queue behind "Advertise upstream" — the only
    path that writes a `use_when` — had never worked, and the screen showed the operator the name of
    a variable that was not theirs to set.
  * .env.example is itself the other half: it did not exist at all, while README and install.sh both
    told people to copy it, so a fresh clone died on line 1.

Both directions are wrong, so both are checked. A variable compose passes that .env.example never
mentions is a setting nobody can discover; those go in UNDOCUMENTED with the reason.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
env_text = (ROOT / ".env.example").read_text(encoding="utf-8")
# Every compose file, not just the main one. The overlays that add a second backbone and an exchange
# read settings too, and a setting only they name is exactly as dead as one nothing names — it was
# only ever checked in the file that happened to exist when this was written.
COMPOSE = sorted(ROOT.glob("docker-compose*.yml"))
compose = "\n".join(p.read_text(encoding="utf-8") for p in COMPOSE)

# Both the set and the commented-out forms: a commented default is still a documented setting.
documented = {m.group(1) for m in re.finditer(r"^#?\s*([A-Z][A-Z0-9_]*)=", env_text, re.M)}
# Anything compose interpolates from the environment — `${NAME}` or `${NAME:-default}`.
passed = {m.group(1) for m in re.finditer(r"\$\{([A-Z][A-Z0-9_]*)", compose)}

# Passed through but deliberately not in .env.example. Each line is a decision.
UNDOCUMENTED = {
    "EXCHANGE_TOKEN_HOME": "the circuit key's name before 2026-10-08, read only when KNOWLEDGE_CIRCUIT_TOKEN "
                           "is unset so an install updated in place keeps the key it had",
}

# ── and the installer has to read .env the way docker does ───────────────────
# `install.sh` waits on the port it thinks the screen is published at, and docker publishes the port
# it reads from the same file. When the file names one key twice — appending a line rather than
# editing the one already there, which is what a person does — docker takes the **last** and the
# installer took the first. It waited on 8080 while the container served 8480 and reported that
# nothing had come up, with a healthy stack behind it.
#
# The pipeline is lifted out of install.sh and run, rather than copied here: a check holding its own
# copy of the logic agrees with itself for ever.
import re as _re, subprocess, tempfile

_src = (ROOT / "install.sh").read_text(encoding="utf-8")
_m = _re.search(r'^PORT="(\$\(.*\))"$', _src, _re.M)
if not _m:
    port_reader = ['install.sh has no PORT="$(...)" line to check — did it move?']
else:
    with tempfile.TemporaryDirectory() as _d:
        # Named twice with the second winning, beside a key that merely starts the same way.
        (Path(_d) / ".env").write_text("WEB_PORT=8080\nWEB_PORT_B=8081\nWEB_PORT=8480\n",
                                       encoding="utf-8")
        _got = subprocess.run(["sh", "-c", 'cd "$1"; printf %s "' + _m.group(1) + '"', "sh", _d],
                              capture_output=True, text=True).stdout.strip()
    port_reader = [] if _got == "8480" else [
        f"install.sh reads WEB_PORT as {_got!r}, docker compose reads '8480'"]

# Read by docker compose itself, not passed to a container: compose takes the project name from .env.
COMPOSE_OWN = {"COMPOSE_PROJECT_NAME",
               # Read by the MCP server on the host, which reads .env itself (mcp/knowledge_mcp.py).
               "KNOWLEDGE_CIRCUIT_KEYS"}
dead = sorted(documented - passed - COMPOSE_OWN)
hidden = sorted(v for v in passed - documented if v not in UNDOCUMENTED)
stale = sorted(v for v in UNDOCUMENTED if v in documented or v not in passed)

for v in sorted(UNDOCUMENTED):
    if v not in stale: print(f"--   {v} is not in .env.example, on purpose — {UNDOCUMENTED[v]}")
for v in stale: print(f"--   {v} is in UNDOCUMENTED but no longer needs to be; drop the entry")

# ── and every `mkdir -p` recipe has to cover every bind mount ────────────────
# Docker creates a missing bind-mount path **owned by root** while the container runs as
# KNOWLEDGE_UID, so a recipe short by one directory is a container that never becomes healthy, with
# a message about the directory that *is* there. This has now happened twice: `data-b/…` was in
# install.sh and missing from the old peering guide (SCENARIOS Q6), and
# then `access` — added with the access record — was missing from three recipes in README.md and from
# the operator screen's plan, which is the screen written to prevent exactly this.
#
# So the recipes are compared to the mounts rather than to each other. A recipe naming one directory
# is exempt: that is the `mkdir -p data/repo && cp -r examples/…` form, where install.sh makes the
# rest. Two or more means the recipe is standing in for the whole preparation.
MOUNT_RE = re.compile(r"source:\s*(?:\$\{[A-Z_]+:-)?\./([a-z0-9-]+)/([a-z]+)\}?")
mounts: dict[str, set[str]] = {}
for f in COMPOSE:
    for root, sub in MOUNT_RE.findall(f.read_text(encoding="utf-8")):
        mounts.setdefault(root, set()).add(sub)
peer_layout: set = set()

# A recipe is not always one run of text. It is broken over lines with a trailing backslash in the
# shell, and it has been two adjacent Python string literals — so the text is joined
# before it is read, or the check reports a complete recipe as short and the next person "fixes" a
# file that was right. `\` + newline, and `"` + newline + `f"`, both become one space.
JOIN_RE = re.compile(r"\\\s*\n\s*|\"\s*\n\s*f?\"")
RECIPE_RE = re.compile(r"mkdir -p ((?:[A-Za-z0-9{}$_-]+/[a-z]+\s+)*[A-Za-z0-9{}$_-]+/[a-z]+)")
short = []
for f in sorted(ROOT.glob("*.sh")) + sorted(ROOT.glob("*.yml")) + sorted(ROOT.glob("docs/*.md")) \
       + [ROOT / "README.md"]:
    raw = f.read_text(encoding="utf-8")
    text = JOIN_RE.sub(" ", raw)
    for m in RECIPE_RE.finditer(text):
        dirs = [d for d in m.group(1).split() if "/" in d]
        if len(dirs) < 2: continue
        roots = {d.split("/")[0] for d in dirs}
        if len(roots) != 1: continue
        r = roots.pop()
        want = mounts.get(r) or (peer_layout if r.startswith("data-") or "{" in r or "$" in r else None)
        if not want: continue
        missing = sorted(want - {d.split("/", 1)[1] for d in dirs})
        if missing:
            # The joined text has different offsets, so the line is counted in the file as written.
            # Joining never removes a `mkdir -p`, so the nth one in the joined text is the nth one
            # here — which matters in README.md, where the first is a one-directory recipe this loop
            # skipped and naming it would send someone to edit the wrong line.
            nth = text[:m.start()].count("mkdir -p")
            at = -1
            for _ in range(nth + 1): at = raw.index("mkdir -p", at + 1)
            line = raw[:at].count("\n") + 1
            short.append(f"{f.relative_to(ROOT)}:{line}  {r}/ is missing " + ", ".join(missing))

bad = False
if short:
    bad = True
    print("FAIL a mkdir recipe does not cover every bind mount:\n  " + "\n  ".join(short) +
          "\n  Docker creates the missing one as root and the container never comes up.")
else:
    print(f"ok   every mkdir recipe covers its bind mounts ({sum(len(v) for v in mounts.values())} across {len(mounts)} layouts)")
for line in port_reader:
    bad = True
    print("FAIL the installer and docker compose disagree about which .env line wins:\n  " + line +
          "\n  A duplicated key is ordinary — appending a line instead of editing one — and the\n"
          "  installer then waits on a port nothing is serving and says the stack did not come up.")
if not port_reader:
    print("ok   install.sh reads WEB_PORT the way docker compose does (the last line wins)")
if dead:
    bad = True
    print("FAIL .env.example documents settings no compose file passes to a container:\n  " +
          "\n  ".join(dead) + "\n  Someone sets these and nothing reads them, with no error anywhere.")
if hidden:
    bad = True
    print("FAIL a compose file reads settings .env.example never mentions:\n  " +
          "\n  ".join(hidden) + "\n  Either document them, or add them to UNDOCUMENTED here with the reason.")
# ── a first run refused before anything starts takes its .env back ─────────
# Left behind, the next run read it as an existing install's .env: no port question, and no
# path-suffixed name, so a clone called `routemind` collided with another (operator QA, 2026-10-10).
# A bad port is refused before docker is touched, so this runs anywhere.
import shutil as _sh
with tempfile.TemporaryDirectory() as _d:
    for f in ("install.sh", ".env.example"): _sh.copy(ROOT / f, Path(_d) / f)
    _r = subprocess.run(["sh", "./install.sh", "--port", "99999", "--no-llm"], cwd=_d, capture_output=True, text=True,
                        stdin=subprocess.DEVNULL)
    if _r.returncode == 2 and not (Path(_d) / ".env").exists():
        print("ok   a first install refused for its port leaves no .env behind")
    else:
        bad = True
        print(f"FAIL a first install refused for its port left a .env (rc {_r.returncode}) — the next run would skip "
              f"the port question and the unique name")
# ── a check aimed at "the install" aims at this checkout's ───────────────────
# smoke.sh, all.sh, llm-paths.sh, mcp-check, circuit-check and screen-check all defaulted to :8080.
# From a checkout installed on another port they tested — and llm-paths wrote two commits into —
# whatever RouteMind held 8080, and passed (quickstart QS-1, suite CS-1, docs DC-2, 2026-11-02). The
# reader is check/base.sh, run here against a .env naming the port twice; each check must use it, or
# the MCP server's own reader, which mcp-check and circuit-check share.
_base = ROOT / "check" / "base.sh"
with tempfile.TemporaryDirectory() as _d:
    (Path(_d) / ".env").write_text("WEB_PORT=8080\nWEB_PORT_B=8081\nWEB_PORT='9471'\n", encoding="utf-8")
    _got = subprocess.run(["sh", "-c", '. "$1"; checkout_base "$2"', "sh", str(_base), _d],
                          capture_output=True, text=True).stdout.strip() if _base.exists() else "(no check/base.sh)"
    (Path(_d) / ".env").write_text("# no port here\n", encoding="utf-8")
    _none = subprocess.run(["sh", "-c", '. "$1"; checkout_base "$2"', "sh", str(_base), _d],
                           capture_output=True, text=True).stdout.strip() if _base.exists() else ""
USES = {"check/smoke.sh": "checkout_base", "check/all.sh": "checkout_base", "check/llm-paths.sh": "checkout_base",
        "check/mcp-check.py": "_default_api", "check/circuit-check.py": "_default_api",
        "check/screen-check.mjs": "WEB_PORT"}
_off = [f for f, needle in USES.items() if needle not in (ROOT / f).read_text(encoding="utf-8")]
if _got != "http://127.0.0.1:9471" or _none != "http://127.0.0.1:8080" or _off:
    bad = True
    print(f"FAIL a check's default install is not this checkout's: base.sh gives {_got!r} for WEB_PORT=9471 "
          f"(last line) and {_none!r} with none" + (f"; not reading it: {', '.join(_off)}" if _off else ""))
else:
    print(f"ok   every check aimed at the install defaults to this checkout's WEB_PORT ({len(USES)} checks)")

# ── no docker, or no compose plugin, is said in a sentence, before anything starts ──
# It was "docker: command not found" at the first compose call, or "'compose' is not a docker
# command", with a fresh .env left behind (scenarios audit, 2026-11-02). A fake docker on PATH stands in
# for a missing plugin; a PATH holding only the tools install.sh uses before it stands in for no docker.
# `--port=N` is read as `--port N`; it was "unknown option" (quickstart, 2026-11-02).
import os as _os, stat as _stat
def _run_install(args, path):
    with tempfile.TemporaryDirectory() as _d:
        for f in ("install.sh", ".env.example"): _sh.copy(ROOT / f, Path(_d) / f)
        r = subprocess.run(["/bin/sh", "./install.sh", *args], cwd=_d, capture_output=True, text=True,
                           stdin=subprocess.DEVNULL, env={**_os.environ, "PATH": path})
        return r.returncode, r.stderr, (Path(_d) / ".env").exists()
with tempfile.TemporaryDirectory() as _bin:
    for tool in ("dirname", "basename", "cp", "rm", "grep", "id", "mktemp", "mv", "cat", "tr", "cut", "sed", "head",
                 "tail", "cksum", "mkdir", "ls", "od", "sort", "pwd"):
        if _sh.which(tool): _os.symlink(_sh.which(tool), Path(_bin) / tool)
    rc, err, left = _run_install(["--port", "9479", "--no-llm"], _bin)
    no_docker = rc == 2 and "docker" in err.lower() and "not found" not in err and not left
    _fake = Path(_bin) / "docker"
    _fake.write_text("#!/bin/sh\n[ \"$1\" = compose ] && { echo \"docker: 'compose' is not a docker command.\" >&2; exit 1; }\nexit 0\n")
    _fake.chmod(_fake.stat().st_mode | _stat.S_IEXEC)
    rc2, err2, left2 = _run_install(["--port", "9479", "--no-llm"], _bin)
    no_compose = rc2 == 2 and "compose plugin" in err2 and not left2
    rc3, err3, _ = _run_install(["--port=99999", "--no-llm"], _bin + ":" + _os.environ.get("PATH", ""))
    eq_form = rc3 == 2 and "65535" in err3
for ok, what, why in ((no_docker, "no docker on PATH is refused in a sentence, leaving no .env", f"rc {rc}: {err.strip()[:160]!r}"),
                      (no_compose, "docker without the compose plugin is refused in a sentence, leaving no .env", f"rc {rc2}: {err2.strip()[:160]!r}"),
                      (eq_form, "--port=N is read as --port N", f"rc {rc3}: {err3.strip()[:120]!r}")):
    if ok: print(f"ok   {what}")
    else: bad = True; print(f"FAIL {what} — {why}")

# ── the build leaves out what the host writes ─────────────────────────────────
# The install's own checks import ontology/service on the host and leave __pycache__ there; with no
# .dockerignore, COPY carried it into the image, so the second ./install.sh rebuilt the ontology and
# recreated its container — 15 s of refused requests on a run the README calls safe to repeat
# (quickstart QS-3, 2026-11-02). data/ and .git are the operator's and the repository's, not the image's.
_ign = (ROOT / ".dockerignore").read_text(encoding="utf-8").split() if (ROOT / ".dockerignore").exists() else []
_want = {"**/__pycache__", "**/*.pyc", "data", ".git"}
_miss = sorted(_want - set(_ign))
if _miss:
    bad = True
    print(f"FAIL .dockerignore does not leave out {', '.join(_miss)} — a host-side run changes the build "
          f"context, and the next install rebuilds and restarts the service")
else:
    print(f"ok   the build context leaves out what the host writes ({', '.join(sorted(_want))})")

if bad: sys.exit(1)
print(f"ok   {len(documented)} settings documented, every one reaching a container ({len(COMPOSE)} compose files)")
