#!/usr/bin/env python3
"""RouteMind's own MCP surface, as a command line — so an agent with no MCP client can still walk it.

The benchmark's `agent.py` re-implements the walk: it renders its own tables, and it has two of the
three operations the real server exposes. What it measures is therefore a model of RouteMind rather
than RouteMind. This is the other way round — it calls **`mcp/knowledge_mcp.py`'s own functions**, so
the tables, the absence lines, the address discipline and the working set are the server's, not a
second copy of them. Only the transport differs.

It exists so a fresh agent can be handed a question and this command, and nothing else: no repository,
no corpus on disk, no answer key. That agent has not seen the corpus being built, which is the one
thing the author of the corpus cannot arrange for himself.

    ./bench/rmcli.py table                       the areas — every walk starts here
    ./bench/rmcli.py table /v1/regions/expense   what an area holds
    ./bench/rmcli.py table /v1/nodes/<id>        what a node holds
    ./bench/rmcli.py read  /v1/nodes/<id>/body   one document, as written
    ./bench/rmcli.py overlay create --question "..." --member <addr> "<why>" ...
    ./bench/rmcli.py overlay add|remove --id <id> --address <addr> --why "..."
    ./bench/rmcli.py overlay close --id <id> --outcome answered|not_found --used <addr> ...

`KNOWLEDGE_API` picks the instance; it defaults to the benchmark ontology rather than the demo, so a
walk cannot wander into the wrong corpus by forgetting a flag.
"""
import argparse, os, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mcp"))
# The host python has no pyyaml and the one in the image cannot be reached from outside it, so it is
# vendored into a scratch directory named by BENCH_PYLIB. Putting that on the path **here** rather
# than in the caller's environment is what lets a walking agent run `./bench/rmcli.py table` with no
# prefix — which matters because a prefix is the difference between a permission rule that matches
# and one that does not, and a headless run that cannot match its own allow-rule just stops.
if os.environ.get("BENCH_PYLIB"):
    sys.path.insert(0, os.environ["BENCH_PYLIB"])
import knowledge_mcp as K

API = os.environ.get("KNOWLEDGE_API", "http://127.0.0.1:8101/v1")


def guard():
    """Refuse to walk a corpus that is not the one under measurement.

    `bench/corpus-hard` is what the retrieval arms index and what the fingerprint in the run records
    names. `data/bench-repo` is the copy the server reads. They are two paths to the same thing only
    for as long as somebody keeps them equal, and today they were not: a copy taken before a fix went
    on being served for an hour, so the routing arm and the retrieval arm were measured against
    different corpora and the comparison between them meant nothing.

    Nothing about that was visible from either side. What caught it was a walking agent remarking
    that a delegation limit of 200 thousand KRW did not fit the amount band its own row was indexed
    by — twice, because the first time it was waved off as already fixed.

    So the assumption becomes a check, and it costs two file reads.
    """
    want = ROOT / "bench" / "corpus-hard" / ".fingerprint"
    served = ROOT / "data" / "bench-repo" / "FINGERPRINT"
    if not want.exists() or not served.exists():
        sys.exit("error: no fingerprint to compare — run ./bench/serve.py")
    a, b = want.read_text().strip(), served.read_text().strip()
    if a != b:
        sys.exit(f"error: the served corpus is not the one under measurement\n"
                 f"  bench/corpus-hard  {a}\n  data/bench-repo    {b}\n"
                 f"  run ./bench/serve.py to rebuild and restart")


def main():
    guard()
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("table"); t.add_argument("path", nargs="?", default="")
    r = sub.add_parser("read"); r.add_argument("path")
    o = sub.add_parser("overlay")
    o.add_argument("op", choices=["create", "get", "add", "remove", "close"])
    o.add_argument("--question"); o.add_argument("--id"); o.add_argument("--address")
    o.add_argument("--why"); o.add_argument("--outcome"); o.add_argument("--used", nargs="*")
    o.add_argument("--member", nargs=2, action="append", metavar=("ADDRESS", "WHY"))
    a = p.parse_args()

    api = K.Api(API, os.environ.get("KNOWLEDGE_ACTOR", "bench-walker"))
    try:
        if a.cmd == "table":
            path = a.path.strip()
            if not path or path.rstrip("/").endswith("/regions"):
                print(K.hop0(api))
            elif "/regions/" in path:
                print(K.area(api, path))
            else:
                print(K.node(api, path))
        elif a.cmd == "read":
            print(api.text(a.path))
        else:
            body = {"op": a.op}
            for k in ("question", "id", "address", "why", "outcome"):
                if getattr(a, k): body[k] = getattr(a, k)
            if a.used: body["used"] = a.used
            if a.member:
                body["members"] = [{"address": m[0], "why": m[1]} for m in a.member]
            print(K.overlay_call(api, body))
    except K.ApiError as e:
        sys.exit(f"error: {e}")


if __name__ == "__main__":
    main()
