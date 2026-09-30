#!/usr/bin/env python3
"""Take what a backbone exports and write it as one encrypted file, for somewhere a link cannot go.

A circuit or a peer reads a remote backbone live. This is for the case where neither can: a partner
behind a firewall, an air-gapped site, an auditor who gets a copy and nothing else. The file is
handed over the way anything else is handed over, and the recipient reads it with `import.py`.

    ./transfer/export.py --api http://localhost:8110 --token "$TOK" --out partner.rmx

The same file is offered from the web screen's **Export** button, which calls the same `collect()`
and `seal()` in `bundle.py` — the format lives there rather than in whichever tool happens to write
it, because a format defined twice is two formats that agree until they do not.

**It reads `/v1/export/…` and nothing else.** Not the store, not the ordinary API. That surface is
built from the set of areas somebody set `export` on, rather than filtered on the way
out — server.py: "there is no path through this code, and no bug in a token check, that can serve an
area nobody decided to share. A filter applied on the way out would have to be right every time; a
surface built from the exported set is right by construction." Re-implementing the filter here would
throw that away and be the second place it has to be correct.

So an export contains exactly what a peer would have been able to read, and the line in it is
`use_when` — the one sentence, the same one this backbone routes on. There used to be a second one
written for outsiders; operator, 2026-09-29: one sentence, and `export` decides whether it crosses.

The file's layout, the choice of AES-256-GCM, and why the header is authenticated rather than secret
are all documented in `bundle.py`.
"""
import argparse, getpass, os, sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from transfer.bundle import BundleError, collect, seal


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--api", default=os.environ.get("ROUTEMIND_API", "http://localhost:8110"),
                    help="the backbone to export from — its own address, not the web proxy")
    ap.add_argument("--token", default=os.environ.get("ROUTEMIND_TOKEN", ""),
                    help="a peer token the backbone accepts. Prefer ROUTEMIND_TOKEN in the environment")
    ap.add_argument("--out", required=True)
    ap.add_argument("--passphrase-env", default="ROUTEMIND_EXPORT_PASSPHRASE",
                    help="environment variable holding the passphrase; prompted for if unset")
    a = ap.parse_args()
    if not a.token: sys.exit("  --token or ROUTEMIND_TOKEN is required")

    try:
        payload = collect(a.api, a.token)
    except BundleError as e:
        sys.exit(f"  {e}")
    print(f"  {len(payload['regions'])} exported area(s) · {len(payload['nodes'])} node(s) "
          f"· revision {payload['source'].get('revision')}", file=sys.stderr)
    if not payload["regions"]:
        # Not an error and worth stopping for: a backbone with nothing exported produces a valid,
        # encrypted, empty file, and the person who receives it has no way to tell that from a
        # mistake at this end.
        sys.exit("  this backbone exports no areas — nothing to send. Set `export: yes` on the "
                 "areas that should cross, then run this again.")

    pw = os.environ.get(a.passphrase_env) or getpass.getpass("  passphrase for the recipient: ")
    if len(pw) < 12:
        sys.exit("  passphrase is short. It is the only thing between this file and whoever finds it.")
    try:
        blob = seal(payload, pw)
    except BundleError as e:
        sys.exit(f"  {e} — or run it in the ontology container, where it is installed")
    with open(a.out, "wb") as f: f.write(blob)
    os.chmod(a.out, 0o600)
    print(f"  {a.out}  ({len(blob):,} bytes)\n"
          f"  Send the passphrase by a different route than the file.", file=sys.stderr)


if __name__ == "__main__":
    main()
