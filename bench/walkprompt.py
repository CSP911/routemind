#!/usr/bin/env python3
"""The prompt a fresh agent is handed for one question. Printed, not hand-written.

The routing arm is a person spawning agents, and up to now that person was writing each prompt by
hand and reading each answer by eye. Two things go wrong that way and both did. The prompts drift —
a sentence phrased one way for the fifth question and another way for the sixth is a variable nobody
recorded — and there is no artefact afterwards that says what was asked.

So the prompt is generated from the gold file and nothing else. **It never contains the answer**:
`D_true`, `A_true` and `support` are not read here, and the question's own text is the only thing
that crosses over.

    ./bench/walkprompt.py h-perdiem-022-i
    ./bench/walkprompt.py t-accrual-04 --overlay

`--overlay` adds the working-set instructions, which is the difference between the `routing` arm and
`routing+overlay`. Nothing else differs between them.
"""
import argparse, os, pathlib, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLD = ["eval/gold/hard.yaml", "eval/gold/hard-temporal.yaml", "eval/gold/hard-sample35.yaml"]
# Where pyyaml lives for the walking agent. The host python has no pyyaml and the one in the
# image cannot be used from outside it, so it is vendored into a scratch directory; that
# directory is per-session and machine-specific, which is why it is an environment variable
# and not a path baked into a tracked file.
PYLIB = os.environ.get("BENCH_PYLIB", "")

BASE = """You are answering one question from a company knowledge base called RouteMind, reached through a command-line tool.

**The only command you may run is `./bench/rmcli.py`, from {root}.** Do not read, list, grep or open any file in the repository. Do not search the filesystem. Do not use any background, monitor, or waiting tool — every call is synchronous and returns immediately. Everything comes back from the tool. If you cannot find the answer through the tool, say "not found" — that is a valid outcome and more useful to me than an answer obtained another way.

The command:

    ./bench/rmcli.py table              the list of areas — every search starts here
    ./bench/rmcli.py table <address>    open a table at an address a previous table printed
    ./bench/rmcli.py read <address>     read one document at an address a table printed
{overlay_help}
Use addresses exactly as printed. Never construct one. Today's date is 2026-09-20.

**The question:**

> {question}

**Write your report to `{out}`** with the Write tool. That file is the deliverable — it is what gets scored and it is kept verbatim. Then reply with the single word `done` and nothing else: the file is the report, and repeating it in the reply only costs context in the process that collects it.

The report is exactly this and nothing else:

1. **Commands**: every command you ran, in order, one per line.
2. **Answer**: the figures, or "not found".
3. **Source**: the address of the document the answer came from; list all that contributed, in the order used.
4. **Notes**: where the walk was confusing or ambiguous, where you nearly went wrong and why. Be blunt — this is the part I most want."""

OVERLAY = """    ./bench/rmcli.py overlay create --question "..." --member <addr> "<why>" [--member ...]
    ./bench/rmcli.py overlay add|remove --id <id> --address <addr> --why "..."
    ./bench/rmcli.py overlay close --id <id> --outcome answered|not_found --used <addr> [<addr>...]

**Keep a working set.** After the first table, create one from the rows the question could be in, each with the reason you picked it. Narrow it as you learn more — add and remove with reasons. It is where a decision you have already made is kept, so you do not work the same choice out twice. Close it when you answer, naming what you actually used.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qid"); ap.add_argument("--overlay", action="store_true")
    # Where the report goes. Default keeps the hand-run form; the census passes a path under
    # eval/runs so the reports persist as the arm's raw data rather than as temp files.
    ap.add_argument("--out")
    a = ap.parse_args()
    for f in GOLD:
        p = ROOT / f
        if not p.exists(): continue
        for q in yaml.safe_load(p.read_text(encoding="utf-8"))["questions"]:
            if q["id"] == a.qid:
                # The two arms answer the same question and must not write to the same file.
                # They did: `routing` ran first and left /tmp/walk-<id>.md behind, so an overlay
                # agent that never wrote its report would have been scored on the routing arm's
                # report without a single sign that anything was wrong.
                suffix = "-overlay" if a.overlay else ""
                out = a.out or f"/tmp/walk-{a.qid}{suffix}.md"
                print(BASE.format(root=ROOT, question=q["q"], qid=a.qid, out=out,
                                  overlay_help=("\n" + OVERLAY) if a.overlay else ""))
                return
    sys.exit(f"  no question with id {a.qid} in {', '.join(GOLD)}")


if __name__ == "__main__":
    main()
