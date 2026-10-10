#!/usr/bin/env python3
"""Walk the philosophy questions through the real MCP door, with Claude Code as the agent.

    ./eval/philosophy/run.py --api http://localhost:9431/api/knowledge --repo <install>/data/repo \
        --compose-dir <install> --models sonnet,haiku --out eval/runs/<date>-philosophy

An install of examples/back-office, its own — the wrong-map half commits deliberate falsehoods into
its data repository and reverts them afterwards, so never point this at a map anyone uses.

Each question is one `claude -p` with nothing but the knowledge MCP server: no built-in tools, no
settings, no memory, its instructions exactly what the server hands any client. The whole stream is
kept — every tool call and its arguments — so hop-0 discipline and "read before claiming absence"
are read from what the agent did, not from what it said it did.
"""
import argparse, json, os, pathlib, re, subprocess, sys, tempfile, time

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bench"))
import yaml
from agent import _limit_wait

HERE = pathlib.Path(__file__).resolve().parent


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, "-c", "user.name=philosophy-eval", "-c", "user.email=eval@routemind.local", *a],
                          capture_output=True, text=True, check=True).stdout.strip()


def set_field(path, field, value):
    text = path.read_text(encoding="utf-8")
    new, n = re.subn(rf"^{field}: .*$", f"{field}: {json.dumps(value, ensure_ascii=False)}", text, count=1, flags=re.M)
    if not n: raise SystemExit(f"{path}: no {field} line")
    path.write_text(new, encoding="utf-8")


def regenerate(compose_dir):
    # The derived area table, so hop 0 reads the mutated sentence from regions.json as well as from the
    # files (the service serves the files' truth either way; this keeps the tree valid).
    subprocess.run(["docker", "compose", "exec", "-T", "ontology", "python3", "/app/tidy.py", "/data/repo", "--fix"],
                   cwd=compose_dir, capture_output=True, text=True)


def walk(q, model, api, workdir):
    cfg = {"mcpServers": {"knowledge": {"command": sys.executable,
                                        "args": [str(ROOT / "mcp" / "knowledge_mcp.py"), "--api", api]}}}
    cmd = ["claude", "-p", q, "--model", model, "--output-format", "stream-json", "--verbose",
           "--mcp-config", json.dumps(cfg), "--strict-mcp-config", "--tools", "", "--setting-sources", "",
           "--disable-slash-commands", "--no-session-persistence",
           "--allowedTools", "mcp__knowledge__knowledge_table,mcp__knowledge__knowledge_read"]
    for attempt in range(6):
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=workdir, timeout=900)
        events = []
        for line in r.stdout.splitlines():
            try: events.append(json.loads(line))
            except Exception: pass
        final = next((e for e in reversed(events) if e.get("type") == "result"), {})
        if final.get("subtype") == "success" and final.get("result"):
            calls = [{"tool": c["name"].split("__")[-1], "input": c.get("input", {})}
                     for e in events if e.get("type") == "assistant"
                     for c in (e.get("message", {}).get("content") or []) if c.get("type") == "tool_use"]
            return {"answer": final["result"], "calls": calls, "turns": final.get("num_turns"),
                    "cost_usd": final.get("total_cost_usd"), "models": sorted((final.get("modelUsage") or {}).keys())}
        wait = _limit_wait(f"{r.stdout[-2000:]}\n{r.stderr}")
        if wait:
            sys.stderr.write(f"  usage limit — waiting {int(wait)}s\n"); time.sleep(wait); continue
        time.sleep(10 * (attempt + 1))
    return {"answer": None, "error": (r.stderr or r.stdout)[-500:], "calls": []}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", required=True); ap.add_argument("--repo", required=True)
    ap.add_argument("--compose-dir", required=True); ap.add_argument("--models", default="sonnet")
    ap.add_argument("--out", required=True); ap.add_argument("--only", default="")
    ap.add_argument("--questions", default=str(HERE / "questions.yaml"), help="another question file (eval/scale uses its own)")
    a = ap.parse_args()
    spec = yaml.safe_load(pathlib.Path(a.questions).read_text())
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    work = tempfile.mkdtemp(prefix="philosophy-")
    qs = [q for q in spec["questions"] if not a.only or q["id"] in a.only.split(",")]
    if git(a.repo, "status", "--porcelain"): raise SystemExit(f"{a.repo} is not clean")
    start = git(a.repo, "rev-parse", "HEAD")

    def run(batch, phase):
        for model in a.models.split(","):
            for q in batch:
                f = out / f"{model}-{q['id']}.json"
                if f.exists(): continue          # resumable: a run cut short picks up where it stopped
                sys.stderr.write(f"{phase} {model} {q['id']}\n")
                res = walk(q["q"], model, a.api, work)
                f.write_text(json.dumps({"id": q["id"], "kind": q.get("kind", ""), "model": model, "phase": phase,
                                         "q": q["q"], **res}, ensure_ascii=False, indent=1) + "\n")

    run([q for q in qs if q.get("kind") != "wrong-map"], "clean")
    wrong = [q for q in qs if q.get("kind") == "wrong-map"]
    if wrong:
        repo = pathlib.Path(a.repo)
        for m in spec["mutations"]:
            set_field(repo / m["file"], m["field"], m["to"])
        git(a.repo, "commit", "-qam", "philosophy eval: deliberate falsehoods in the map (reverted after)")
        regenerate(a.compose_dir)
        try:
            run(wrong, "mutated")
        finally:
            git(a.repo, "revert", "--no-edit", f"{start}..HEAD")
            regenerate(a.compose_dir)
    (out / "meta.json").write_text(json.dumps({"api": a.api, "start": start, "models": a.models.split(","),
                                               "questions": str(pathlib.Path(a.questions).resolve().relative_to(ROOT))}, indent=1) + "\n")


if __name__ == "__main__":
    main()
