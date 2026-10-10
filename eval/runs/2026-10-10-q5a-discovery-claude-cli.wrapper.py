#!/usr/bin/env python3
"""Run eval/fixtures/score.py unchanged, with one substitution: the walker's model call goes to a
fresh, isolated `claude -p` session instead of the Anthropic API (the API credit is exhausted).

Everything else is the frozen harness: bench/agent.py's system prompt, tables, READ text, 30-turn
ceiling, the discovery block, the scorer. The session gets no tools, no MCP servers, no settings, no
CLAUDE.md (an empty working directory), and the agent's own system prompt in place of Claude Code's.
Each turn sends the whole conversation so far as one transcript — the API path sends it as messages.
"""
import json, os, pathlib, subprocess, sys, tempfile, runpy

W = pathlib.Path(sys.argv.pop(1))           # the PR worktree
sys.path.insert(0, str(W / "bench"))
import agent as A

EMPTY = tempfile.mkdtemp(prefix="walker-")
MODEL = os.environ.get("WALKER_MODEL", "opus")

def _ask(self, convo):
    parts = []
    for m in convo:
        parts.append(("USER" if m["role"] == "user" else "YOU (your earlier reply)") + ":\n" + m["content"])
    prompt = ("The conversation so far, oldest first. Reply to the last USER message with commands only, "
              "exactly as your instructions say.\n\n" + "\n\n---\n\n".join(parts))
    for attempt in range(3):
        r = subprocess.run(["claude", "-p", "--model", MODEL, "--tools", "", "--strict-mcp-config",
                            "--setting-sources", "", "--disable-slash-commands", "--no-session-persistence",
                            "--system-prompt", self._sys, "--output-format", "json"],
                           input=prompt, capture_output=True, text=True, cwd=EMPTY, timeout=600)
        try: d = json.loads(r.stdout)
        except Exception: d = {}
        if d.get("terminal_reason") == "completed" and d.get("result") is not None:
            u = d.get("usage") or {}
            self.usage["in"] += u.get("input_tokens", 0); self.usage["out"] += u.get("output_tokens", 0)
            self.usage["cache_write"] += u.get("cache_creation_input_tokens", 0)
            self.usage["cache_read"] += u.get("cache_read_input_tokens", 0)
            self.models = sorted(set(getattr(self, "models", [])) | set((d.get("modelUsage") or {}).keys()))
            return d["result"]
    raise RuntimeError(f"claude -p failed: {r.stderr[-300:]} {r.stdout[-300:]}")

A.Agent._ask = _ask
_init = A.Agent.__init__
def __init__(self, *a, **k):
    _init(self, *a, **k)
    self.provider, self.model = "claude-cli", f"claude -p --model {MODEL} (isolated)"
A.Agent.__init__ = __init__

os.chdir(W)
sys.argv = [str(W / "eval/fixtures/score.py")] + sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
