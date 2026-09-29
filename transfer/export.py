#!/usr/bin/env python3
"""Take what a backbone exports and write it as one encrypted file, for somewhere a link cannot go.

A circuit or a peer reads a remote backbone live. This is for the case where neither can: a partner
behind a firewall, an air-gapped site, an auditor who gets a copy and nothing else. The file is
handed over the way anything else is handed over, and the recipient reads it with `import.py`.

    ./transfer/export.py --api http://localhost:8110 --token "$TOK" --out partner.rmx

**It reads `/v1/export/…` and nothing else.** Not the store, not the ordinary API. That surface is
built from the set of areas somebody wrote `use_when_export` on, rather than filtered on the way
out — server.py: "there is no path through this code, and no bug in a token check, that can serve an
area nobody decided to share. A filter applied on the way out would have to be right every time; a
surface built from the exported set is right by construction." Re-implementing the filter here would
throw that away and be the second place it has to be correct.

So an export contains exactly what a peer would have been able to read, and the lines in it are
`use_when_export` — written for an outside reader. That is the right text for a file leaving the
building.

## The file

    RMEXPORT/1\\n           magic and format version, ASCII, readable with `head -c 12`
    {header json}\\n        salt, KDF parameters, nonce, when, and what it came from
    <ciphertext>          AES-256-GCM over the gzipped payload

The header is **not** secret and **is** authenticated: it is passed to GCM as additional data, so
changing a single byte of it — the KDF cost, say — fails the tag rather than silently producing a
different key. The payload is gzipped before encryption because it compresses well and the size of
an ontology is not what anyone is trying to hide.

AES-256-GCM comes from `cryptography`, not from a construction assembled here. `openssl enc` was the
alternative and it refuses AEAD outright ("enc: AEAD ciphers not supported"), which leaves
encrypt-then-MAC bolted together by hand — a standard shape, but one more thing that has to be right
in a file whose whole purpose is to be trusted by somebody who cannot check it against the original.

Integrity matters here more than it looks. The recipient imports this into their own ontology, and
this study measured what a wrong row does once it is in: a confident answer from the wrong place,
with a source attached, that reads as a clean success.
"""
import argparse, base64, getpass, gzip, hashlib, json, os, sys, time
import urllib.error, urllib.parse, urllib.request

MAGIC = b"RMEXPORT/1\n"
# Deliberately slow, and recorded in the header so a file made today still opens when the default
# moves. RFC 9106 territory: n=2**17 with r=8 is ~128MB and a noticeable pause, which is the point.
KDF = {"kdf": "scrypt", "n": 1 << 17, "r": 8, "p": 1}


def fetch(api: str, token: str, path: str, accept: str = "application/json"):
    url = api.rstrip("/") + "/v1/export/" + path.lstrip("/")
    req = urllib.request.Request(url, headers={"Accept": accept, "X-Peer-Token": token})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        detail = (e.read().decode("utf-8", "replace") or "").strip()[:200]
        sys.exit(f"  {url} → HTTP {e.code}" + (f" — {detail}" if detail else ""))
    except urllib.error.URLError as e:
        sys.exit(f"  cannot reach {url} — {e.reason}")
    return json.loads(raw) if accept == "application/json" else raw


def collect(api: str, token: str) -> dict:
    """Everything the export surface will give, walked from the areas down.

    Nodes are gathered by following each area's `entries` rather than by asking for a list, because
    a list is a second thing that can disagree with the tree. What a walk would reach is what goes
    in the file.
    """
    regions = fetch(api, token, "regions")
    nodes, seen = [], set()

    def descend(nid: str):
        if nid in seen: return
        seen.add(nid)
        n = fetch(api, token, f"nodes/{nid}")
        nodes.append(n)
        for e in (n.get("entries") or []):
            if e.get("id"): descend(e["id"])

    for r in (regions.get("regions") or []):
        rep = r.get("representative") or r.get("source")
        if rep: descend(rep)

    out = {"format": "routemind-export/1", "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "source": {"api": api, "revision": regions.get("revision")},
           "regions": regions.get("regions") or [], "nodes": nodes}
    for extra in ("vocab", "edges"):
        try: out[extra] = fetch(api, token, extra)
        except SystemExit: pass          # not every backbone exports these; the file says what it has
    return out


def seal(payload: dict, passphrase: str) -> bytes:
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
    except ImportError:
        sys.exit("  this needs `cryptography` (pip install cryptography), or run it in the ontology "
                 "container where it is installed")
    salt, nonce = os.urandom(16), os.urandom(12)
    # The library's scrypt, not `hashlib.scrypt`. The stdlib one needs OpenSSL support compiled
    # in and is simply absent on some builds — Xcode's python3 among them — which would have made
    # the file unopenable on a machine that has everything this document says it needs.
    key = Scrypt(salt=salt, length=32, n=KDF["n"], r=KDF["r"], p=KDF["p"]).derive(passphrase.encode())
    header = {**KDF, "salt": base64.b64encode(salt).decode(), "nonce": base64.b64encode(nonce).decode(),
              "created": payload["created"], "source": payload["source"],
              "counts": {"regions": len(payload["regions"]), "nodes": len(payload["nodes"])}}
    hb = json.dumps(header, sort_keys=True).encode()
    body = gzip.compress(json.dumps(payload, ensure_ascii=False).encode())
    # The header is the additional data, so it cannot be edited without failing the tag. A reader
    # can still see what the file claims to be before deciding to type a passphrase at it.
    return MAGIC + hb + b"\n" + AESGCM(key).encrypt(nonce, body, hb)


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

    payload = collect(a.api, a.token)
    print(f"  {len(payload['regions'])} exported area(s) · {len(payload['nodes'])} node(s) "
          f"· revision {payload['source'].get('revision')}", file=sys.stderr)
    if not payload["regions"]:
        # Not an error and worth stopping for: a backbone with nothing exported produces a valid,
        # encrypted, empty file, and the person who receives it has no way to tell that from a
        # mistake at this end.
        sys.exit("  this backbone exports no areas — nothing to send. Write `use_when_export` on the "
                 "areas that should cross, then run this again.")

    pw = os.environ.get(a.passphrase_env) or getpass.getpass("  passphrase for the recipient: ")
    if len(pw) < 12:
        sys.exit("  passphrase is short. It is the only thing between this file and whoever finds it.")
    blob = seal(payload, pw)
    with open(a.out, "wb") as f: f.write(blob)
    os.chmod(a.out, 0o600)
    print(f"  {a.out}  ({len(blob):,} bytes)\n"
          f"  Send the passphrase by a different route than the file.", file=sys.stderr)


if __name__ == "__main__":
    main()
