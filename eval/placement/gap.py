#!/usr/bin/env python3
"""Where the walk and the judgement put the same document — measured, per class.

    PYTHONPATH=<pylib> ./eval/placement/gap.py [--out eval/runs/<date>-placement-gap.json]

Starts an ontology on a fresh copy of `bench/corpus`, and for every document in `documents.yaml`
drives `POST /v1/place` hop by hop the way `knowledge_place` does — but with the tool's own
evidence column as the only driver: open the row that shares the most words, first row on a tie,
stop when no row shares one. No model. Nothing is written; every document meets the pristine
corpus, so the trials are independent.

Then the comparison with the `human:` block (written by the model that wrote the tool — README):
same area, same parent, the distance between the two parents through their lowest common ancestor,
how much shallower the walk stopped, whether it asked for a new area, and whether the ancestors it
would widen are the ones the judgement would. Reported per class, because the point is which kind
of document produces which kind of gap.
"""
import argparse, json, os, pathlib, shutil, subprocess, sys, tempfile, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bench"))
import yaml
import run as runner

MAX_HOPS = 12


def post(port, body):
    req = urllib.request.Request(f"http://127.0.0.1:{port}/v1/place", data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "X-Knowledge-Actor": "placement-gap"})
    with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read())


def walk(port, doc, min_hits=2):
    """The evidence-greedy walk. Returns where it stopped and what it would advertise.

    `min_hits` is the floor's one rule: a row is opened only if it shares at least that many words.
    The first run used 1 and 36 of its 74 descents rode on a single word — "apply", "new", "why".
    One shared word is a coincidence; two is a reason. A row that shares a *name* (an alias or the
    node's own name) outranks one that shares only line words, on ties.
    """
    at, path, hops = "/v1/regions", [], []
    while len(path) < MAX_HOPS:
        d = post(port, {"at": at, "doc": doc, "path": path})
        rows = d.get("rows") or []
        best = max(rows, key=lambda r: (r["evidence"]["hits"], len(r["evidence"]["names"]), -rows.index(r)), default=None)
        hops.append({"at": at, "rows": len(rows),
                     "best": (best["address"], best["evidence"]["hits"]) if best else None})
        if not best or best["evidence"]["hits"] < min_hits:
            if at == "/v1/regions":
                return {"nxdomain": True, "parent": None, "area": None, "path": path, "hops": hops, "advertise": [], "stop_at": None}
            prop = d.get("propagation") or {}
            return {"nxdomain": False, "parent": d["here"]["parent"], "area": d["here"]["region"], "path": path, "hops": hops,
                    "advertise": [q.get("entity") or q.get("region") for q in prop.get("proposals") or []],
                    "stop_at": (prop.get("stop_at") or {}).get("label")}
        path.append(best["address"]); at = best["address"]
    d = post(port, {"at": at, "doc": doc, "path": path})
    prop = d.get("propagation") or {}
    return {"nxdomain": False, "parent": d["here"]["parent"], "area": d["here"]["region"], "path": path, "hops": hops,
            "advertise": [q.get("entity") or q.get("region") for q in prop.get("proposals") or []],
            "stop_at": (prop.get("stop_at") or {}).get("label"), "hit_ceiling": True}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default=str(ROOT / "eval" / "placement" / "documents.yaml"))
    ap.add_argument("--port", type=int, default=18130)
    ap.add_argument("--min-hits", type=int, default=2, help="shared words a row needs before the walk opens it (run 1 used 1)")
    ap.add_argument("--out")
    a = ap.parse_args()

    spec = yaml.safe_load(pathlib.Path(a.docs).read_text(encoding="utf-8"))
    docs = spec["documents"]
    host = ROOT / spec.get("host", "bench/corpus")

    # The tree, for distances. The same corpus the server will serve.
    _, area, one_liner, children, _ = runner.corpus()
    parent = {c: p for p, cs in children.items() for c in cs}
    def chain(i):
        out = [i]
        while out[-1] in parent and parent[out[-1]] != out[-1]: out.append(parent[out[-1]])
        return out                      # i … area root
    def depth(i): return len(chain(i)) - 1
    def distance(x, y):
        cx, cy = chain(x), chain(y)
        common = next((n for n in cx if n in cy), None)
        if common is None: return len(cx) + len(cy)      # different areas: up to each root and across
        return cx.index(common) + cy.index(common)

    tmp = tempfile.mkdtemp(prefix="placement-gap-")
    repo = os.path.join(tmp, "corpus")
    shutil.copytree(host, repo)
    for cmd in (["init", "-q"], ["config", "user.email", "gap@routemind"], ["config", "user.name", "placement-gap"],
                ["add", "-A"], ["commit", "-qm", "the host corpus, as served"]):
        subprocess.run(["git", "-C", repo, *cmd], check=True, capture_output=True)
    env = {**os.environ, "ONTOLOGY_DATA": repo, "PORT": str(a.port),
           "PYTHONPATH": os.pathsep.join(x for x in [os.environ.get("PYTHONPATH", ""), str(ROOT / "ontology")] if x)}
    log = open(os.path.join(tmp, "svc.log"), "w")
    svc = subprocess.Popen([sys.executable, str(ROOT / "ontology" / "service" / "server.py")], env=env, stdout=log, stderr=subprocess.STDOUT)
    try:
        for _ in range(120):
            try: urllib.request.urlopen(f"http://127.0.0.1:{a.port}/healthz", timeout=1); break
            except Exception: time.sleep(0.25)
        else:
            sys.exit("  the ontology never answered — its log:\n" + open(os.path.join(tmp, "svc.log")).read()[-2000:])

        results = []
        for d in docs:
            doc = {"name": d["name"], "one_liner": d["one_liner"], "aliases": d.get("aliases") or [], "content": d.get("body") or ""}
            t = walk(a.port, doc, min_hits=a.min_hits)
            h = d["human"]
            r = {"id": d["id"], "class": d["class"], "gold": h.get("gold"), "human": {k: h.get(k) for k in ("area", "parent", "advertise")}, "tool": t}
            if h.get("parent") is None:
                r.update(same_area=t["nxdomain"], same_parent=t["nxdomain"], distance=None, depth_delta=None,
                         advertise_match=(set(t["advertise"]) == set(h.get("advertise") or [])))
            elif t["nxdomain"]:
                r.update(same_area=False, same_parent=False, distance=None, depth_delta=None, advertise_match=False)
            else:
                r.update(same_area=(t["area"] == h["area"]), same_parent=(t["parent"] == h["parent"]),
                         distance=distance(t["parent"], h["parent"]), depth_delta=depth(t["parent"]) - depth(h["parent"]),
                         advertise_match=(set(t["advertise"]) == set(h.get("advertise") or [])))
            results.append(r)
            mark = "==" if r["same_parent"] else ("~ " if r["same_area"] else ("NX" if t["nxdomain"] else "!="))
            print(f"  {mark} {d['class']:<13} {d['id']:<36} tool {str(t['parent']):<38} judged {str(h.get('parent')):<38}"
                  f" adv {'ok' if r['advertise_match'] else 'DIFF'}", file=sys.stderr)
    finally:
        svc.terminate()
        try: svc.wait(5)
        except Exception: svc.kill()
        shutil.rmtree(tmp, ignore_errors=True)

    classes = list(dict.fromkeys(d["class"] for d in docs))
    print()
    print(f"  {'class':<13} {'n':>3}  {'area':>5} {'parent':>7} {'adv':>5}  {'dist':>5} {'depth':>6}  {'nx':>3}")
    table = {}
    for c in classes + ["all"]:
        rs = [r for r in results if c == "all" or r["class"] == c]
        n = len(rs)
        dist = [r["distance"] for r in rs if r["distance"] is not None]
        dd = [r["depth_delta"] for r in rs if r["depth_delta"] is not None]
        row = {"n": n, "same_area": sum(r["same_area"] for r in rs) / n, "same_parent": sum(r["same_parent"] for r in rs) / n,
               "advertise_match": sum(r["advertise_match"] for r in rs) / n,
               "mean_distance": (sum(dist) / len(dist)) if dist else None, "mean_depth_delta": (sum(dd) / len(dd)) if dd else None,
               "nxdomain": sum(r["tool"]["nxdomain"] for r in rs)}
        table[c] = row
        dist_s = f"{row['mean_distance']:.1f}" if row["mean_distance"] is not None else "—"
        depth_s = f"{row['mean_depth_delta']:+.1f}" if row["mean_depth_delta"] is not None else "—"
        print(f"  {c:<13} {n:>3}  {row['same_area']:>5.2f} {row['same_parent']:>7.2f} {row['advertise_match']:>5.2f}  "
              f"{dist_s:>5} {depth_s:>6}  {row['nxdomain']:>3}")
    print()
    print("  area/parent/adv: share of documents where the walk agrees with the judgement · dist: hops between the two parents"
          "\n  depth: walk depth minus judged depth (negative = shallower) · nx: documents the walk sent to 'new area'")

    if a.out:
        p = ROOT / a.out
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"host": str(host.relative_to(ROOT)), "documents": len(docs),
                                 "driver": f"evidence-greedy, no model, min_hits={a.min_hits}", "min_hits": a.min_hits,
                                 "at": time.strftime("%Y-%m-%dT%H:%M:%S"), "table": table, "results": results},
                                indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"  -> {a.out}")


if __name__ == "__main__":
    main()
