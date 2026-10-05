#!/usr/bin/env python3
"""Invariant 10: secrets are never in tracked files.

    ./check/secrets-check.py [--repo DIR]

Every file git tracks, read once, against the shapes a secret takes: a provider key (OpenAI,
Anthropic, GitHub, AWS, Slack), a private key block, a `.env` that is tracked, a `token:` with a
value in any YAML — a peers or members file names the *variable* (`token_env`) and nothing else —
and a path from somebody's machine, which is not a secret but is somebody's name in a file that
ships. The scan that used to be run by hand before each push, as a check, so it runs with the rest
and a push without it is not possible to make by forgetting.

Static, no server. `--repo` points it at another repository — the fire test plants each shape in a
temporary one and expects every one to be named.
"""
import argparse, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHAPES = [
    ("an OpenAI-style key",       re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}")),
    ("an Anthropic key",          re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}")),
    ("a GitHub token",            re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|\bgithub_pat_[A-Za-z0-9_]{30,}")),
    ("an AWS access key",         re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("a Slack token",             re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("a private key block",       re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("a token written in YAML",   re.compile(r"^\s*(?:token|secret|password|api_key|apikey)\s*:\s*['\"]?[A-Za-z0-9_./+=-]{16,}", re.M | re.I)),
    # Built from pieces so this file's own source does not carry the shape it looks for — the
    # first tracked run of this check found exactly one secret-shaped thing: this line.
    ("a path from somebody's machine", re.compile(r"/Users/[a-z][a-z0-9_-]+/|/home/[a-z][a-z0-9_-]+/|/private/tmp/" + "cla" + "ude")),
]
# Shapes that are documentation of the shape, not an instance of it.
ALLOW = re.compile(r"sk-proj-\.\.\.|sk-\.\.\.|xxx|your[-_ ]|example|placeholder|<[a-z_ -]+>|\$\{|\$[A-Z_]+", re.I)


def tracked(repo):
    out = subprocess.run(["git", "-C", repo, "ls-files", "-z"], capture_output=True, check=True).stdout
    return [p for p in out.decode("utf-8", "replace").split("\0") if p]


def scan(repo):
    found = []
    for rel in tracked(repo):
        p = os.path.join(repo, rel)
        if not os.path.isfile(p): continue
        base = os.path.basename(rel)
        if base == ".env" or (base.startswith(".env.") and not base.endswith(".example")):
            found.append((rel, 1, "a tracked .env", base)); continue
        try: raw = open(p, "rb").read()
        except OSError: continue
        if b"\0" in raw[:4096]: continue                    # binary
        text = raw.decode("utf-8", "replace")
        for what, rx in SHAPES:
            for m in rx.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                context = text[max(0, m.start() - 40): m.end() + 10].replace("\n", " ")
                if ALLOW.search(context): continue
                found.append((rel, line, what, m.group(0)[:12] + "…"))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=ROOT)
    a = ap.parse_args()
    found = scan(a.repo)
    n = len(tracked(a.repo))
    for rel, line, what, snip in found:
        print(f"  FAIL {rel}:{line}: {what} ({snip})")
    if found:
        print(f"\n{len(found)} secret-shaped thing(s) in {n} tracked files"); sys.exit(1)
    print(f"  ok   {n} tracked files, nothing secret-shaped in any of them")


if __name__ == "__main__":
    main()
