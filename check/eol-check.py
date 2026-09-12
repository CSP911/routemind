#!/usr/bin/env python3
"""What a checkout on another operating system has to survive.

    ./check/eol-check.py

Two properties, both invisible to everything else here because everything else runs on a machine
where they already hold.

**Line endings.** Git's default on Windows is `core.autocrlf=true`, which rewrites LF to CRLF on
checkout. `ontology/entrypoint.sh` is the container's ENTRYPOINT and is COPYed into the image; the
kernel then reads its shebang as `/bin/sh\r`, which does not exist, and the container fails to start
with `no such file or directory` naming a file that is plainly there. Measured in this image: a CRLF
script answers `sh: /tmp/crlf.sh: not found` while `ls` shows it, executable. `.gitattributes` settles
it, and this is what says so out loud.

**The executable bit.** `ENTRYPOINT ["/app/entrypoint.sh"]` needs one. Git records it, and a
filesystem that cannot carry it — Windows, a zip, some shares — hands the build a file without it.
The Dockerfile chmods the entrypoint itself now, but the bit still has to be in the index or a plain
`./install.sh` fails before Docker is ever reached.
"""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True).stdout


bad = []

# `git ls-files --eol` reports the index and working-tree endings of every tracked file.
for line in git("ls-files", "--eol").splitlines():
    fields = line.split("\t", 1)
    if len(fields) != 2: continue
    flags, path = fields[0].split(), fields[1]
    i = next((f for f in flags if f.startswith("i/")), "")
    if i in ("i/crlf", "i/mixed"):
        bad.append(f"{path} is committed with {i[2:].upper()} endings — a shell script or a Dockerfile "
                   f"input this way fails on Linux with an error that names the wrong thing")

# A shebang alone does not mean a file is meant to be run as a program: mcp/knowledge_mcp.py,
# web/app.py and ontology/check.py all carry one and are all invoked as `python3 <path>`, by the
# README, by the Dockerfile's CMD, and by every MCP client config. What has to be executable is what
# something runs as `./<path>` — the installer, the container's ENTRYPOINT, and everything in check/,
# whose own usage lines all read `./check/...`.
need_exec = {p for p in git("ls-files").splitlines()
             if p.endswith(".sh") or p.startswith("check/")}
modes = {}
for line in git("ls-files", "-s").splitlines():
    mode, _, rest = line.partition(" ")
    modes[rest.split("\t", 1)[-1]] = mode
for path in sorted(need_exec):
    if modes.get(path) != "100755":
        bad.append(f"{path} is run as `./{path}` but git records mode {modes.get(path)} — "
                   f"`git update-index --chmod=+x {path}`")

if bad:
    print("FAIL a checkout on another operating system would not survive this:\n  " + "\n  ".join(bad))
    sys.exit(1)
print(f"ok   {len(git('ls-files').splitlines())} files LF-committed, {len(need_exec)} of them executable")
