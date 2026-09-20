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
import knowledge_mcp as K

API = os.environ.get("KNOWLEDGE_API", "http://127.0.0.1:8101/v1")


def main():
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
