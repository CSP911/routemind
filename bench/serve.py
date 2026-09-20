#!/usr/bin/env python3
"""Rebuild the corpus the RouteMind server serves, and prove it is the one under measurement.

There are two copies of the benchmark corpus and there have to be: `bench/corpus-hard` is generated
and indexed by the retrieval arms, and `data/bench-repo` is the shape the product's own service
reads. They are the same thing only for as long as somebody keeps them the same, and for an hour
today they were not — a copy taken before a fix went on being served, so the routing arm and the
retrieval arm were measured against different corpora and the comparison between them was worth
nothing. The copying was a manual step, which is why it drifted.

This is that step, done once and checkable afterwards:

    merge      bench/corpus (the frozen 779) + bench/corpus-hard (the extension)
    derive     regions.json, through the service's own code rather than a second implementation
    hop 0      the maintained use_when, written onto each area's representative node — which is
               where the service reads it from; editing regions.json alone does nothing, because
               regions.json is derived and gets overwritten
    stamp      the fingerprint, so `rmcli.py` can refuse to walk the wrong corpus
    restart    the container, and check it answers

    ./bench/serve.py
"""
import json, os, pathlib, re, shutil, subprocess, sys, time
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT / "data" / "bench-repo"
FM = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)
AREAS = ["approval", "attendance", "expense", "payroll", "procurement"]
CONTAINER = "routemind-bench"
# The working set lives outside the corpus on purpose. `routing+overlay` writes overlays while it
# walks, and an overlay store under data/bench-repo would change the tree the fingerprint is taken
# over — the arm would alter the corpus it is being measured on. Its own directory, mounted
# separately, keeps the fingerprint a property of the documents alone.
OVERLAYS = ROOT / "data" / "bench-overlays"


def sh(*cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main():
    want = (ROOT / "bench" / "corpus-hard" / ".fingerprint")
    if not want.exists():
        sys.exit("  no bench/corpus-hard/.fingerprint — run ./bench/crowd.py write first")
    fp = want.read_text().strip()

    if REPO.exists(): shutil.rmtree(REPO)
    REPO.mkdir(parents=True)
    shutil.copytree(ROOT / "bench" / "corpus", REPO, dirs_exist_ok=True)
    n = 0
    for a in AREAS:
        src = ROOT / "bench" / "corpus-hard" / "regions" / a
        if not src.is_dir(): continue
        (REPO / "regions" / a).mkdir(parents=True, exist_ok=True)
        for f in src.glob("*.md"):
            shutil.copy2(f, REPO / "regions" / a / f.name); n += 1
    print(f"  merged: {len(list((REPO/'regions').rglob('*.md')))} documents ({n} from the extension)")

    # hop 0 lives on each area's representative node, not in regions.json.
    upd = yaml.safe_load((ROOT / "bench" / "use_when_maintained.yaml").read_text(encoding="utf-8"))
    done = 0
    for a in AREAS:
        for p in sorted((REPO / "regions" / a).glob("*.md")):
            m = FM.match(p.read_text(encoding="utf-8"))
            if not m: continue
            meta = yaml.safe_load(m.group(1)) or {}
            if meta.get("role") == "representative" and not meta.get("parent"):
                txt = re.sub(r"^use_when:.*$", 'use_when: "' + " ".join(upd[a].split()) + '"',
                             p.read_text(encoding="utf-8"), count=1, flags=re.M)
                p.write_text(txt, encoding="utf-8"); done += 1
                break
    print(f"  hop 0: maintained use_when on {done}/{len(AREAS)} areas")

    cid = sh("docker", "compose", "ps", "-q", "ontology").stdout.strip().splitlines()
    if not cid: sys.exit("  the ontology container is not up; regions.json cannot be derived")
    cid = cid[0]
    sh("docker", "exec", cid, "rm", "-rf", "/tmp/bench-repo")
    sh("docker", "cp", str(REPO), f"{cid}:/tmp/bench-repo")
    r = sh("docker", "exec", cid, "python3", "-c",
           "import sys;sys.path.insert(0,'/app')\n"
           "from service.store import Store\nfrom service import derive\n"
           "print(derive.regenerate(Store('/tmp/bench-repo')))")
    if r.returncode != 0: sys.exit(f"  regions.json failed: {r.stderr[:300]}")
    sh("docker", "cp", f"{cid}:/tmp/bench-repo/regions.json", str(REPO / "regions.json"))
    print(f"  regions.json: derived by the service's own code")

    (REPO / "FINGERPRINT").write_text(fp + "\n", encoding="utf-8")

    sh("docker", "rm", "-f", CONTAINER)
    OVERLAYS.mkdir(parents=True, exist_ok=True)
    r = sh("docker", "run", "-d", "--name", CONTAINER, "-v", f"{REPO}:/data/repo",
           "-v", f"{OVERLAYS}:/data/overlays",
           "-e", "ONTOLOGY_DATA=/data/repo", "-e", "ONTOLOGY_OVERLAYS=/data/overlays",
           "-p", "127.0.0.1:8101:8100", "knowledge-ontology:0.1.0")
    if r.returncode != 0: sys.exit(f"  container failed: {r.stderr[:300]}")
    for _ in range(20):
        time.sleep(1)
        if sh("curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
              "http://127.0.0.1:8101/v1/regions").stdout.strip() == "200":
            break
    else:
        sys.exit("  the container did not come up")
    print(f"  serving on 8101, fingerprint {fp}")

    got = sh(sys.executable, str(ROOT / "bench" / "rmcli.py"), "table")
    ok = "ROUTEMIND" in got.stdout
    print(f"  rmcli: {'ok' if ok else 'FAILED — ' + got.stderr[:200]}")

    # The bench container ran for a whole campaign without the overlay store configured, and the
    # only way that surfaced was `routing+overlay` failing on its first call. A 501 here is the
    # same fact, found before fifty agents are spawned instead of after one.
    code = sh("curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
              "http://127.0.0.1:8101/v1/overlays").stdout.strip()
    ov = code != "501"
    print(f"  overlays: {'configured' if ov else 'NOT CONFIGURED — routing+overlay cannot run'}"
          f"  (/v1/overlays -> {code})")
    sys.exit(0 if ok and ov else 1)


if __name__ == "__main__":
    main()
