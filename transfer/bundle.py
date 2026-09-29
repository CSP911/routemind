"""The export file format, in one place because three things read it.

`transfer/export.py` writes one from a command line, `transfer/import.py` opens one, and the web
screen offers the same file as a download. A format defined in the tool that writes it and re-read
by hand somewhere else is two formats that agree until they do not — the same reason the web image
already ships the MCP's formatter rather than rendering "what the agent is handed" a second way.

## The file

    RMEXPORT/1\\n           magic and version, ASCII — `head -c 11` says what it is
    {header json}\\n        salt, KDF parameters, when, where from, how many
    <ciphertext>          AES-256-GCM over the gzipped payload

The header is **not** secret and **is** authenticated: it goes to GCM as additional data, so
somebody holding the file can see what it claims to be before typing a passphrase at it, and editing
a byte of it fails the tag rather than quietly deriving a different key.

AES-256-GCM comes from `cryptography` rather than a construction assembled here. `openssl enc` was
the alternative — nothing new to install, and the recipient already has it — but it refuses AEAD
outright (`enc: AEAD ciphers not supported`), which leaves encrypt-then-MAC bolted together by hand.
A standard shape, and still one more thing that has to be right in a file whose whole purpose is to
be trusted by someone who cannot check it against the original.

Integrity is not decoration here. The recipient imports this into their own ontology, and this
design's own 700-question census measured what a wrong row does once it is in: a confident answer
from the wrong place, with a source attached, in a walk log that reads as a clean success.
"""
from __future__ import annotations

import base64, gzip, json, os, time
import urllib.error, urllib.request

MAGIC = b"RMEXPORT/1\n"
# Deliberately slow, and written into the header so a file made today still opens when the default
# moves. n=2**17 with r=8 is ~128MB and a noticeable pause, which is the point.
KDF = {"kdf": "scrypt", "n": 1 << 17, "r": 8, "p": 1}


class BundleError(Exception):
    pass


def _crypto():
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
        return AESGCM, Scrypt
    except ImportError:
        raise BundleError("this needs `cryptography` — pip install cryptography")


def _key(passphrase: str, salt: bytes, params: dict) -> bytes:
    # The library's scrypt, not `hashlib.scrypt`. The stdlib one needs OpenSSL support compiled in
    # and is simply absent on some builds — Xcode's python3 among them — which made a bundle
    # unopenable on the machine that had just written it.
    _, Scrypt = _crypto()
    return Scrypt(salt=salt, length=32, n=params["n"], r=params["r"],
                  p=params["p"]).derive(passphrase.encode())


_HELD: dict[tuple, str] = {}


def session(api: str, key: str, timeout: float = 30) -> str:
    """Trade the enrolment key for a six-hour session, and hold it.

    The key opens `/v1/peers/token` and nothing else since 2026-09-29 — it used to ride on every
    read, which put a secret that never expires into every request and every log. One mint per run
    here; an export is a handful of reads and does not outlive its session.
    """
    ident = (api.rstrip("/"), key)
    if ident in _HELD: return _HELD[ident]
    req = urllib.request.Request(api.rstrip("/") + "/v1/peers/token", data=b"", method="POST",
                                 headers={"X-Peer-Token": key, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            tok = str(json.loads(r.read().decode("utf-8")).get("token") or "")
    except urllib.error.HTTPError as e:
        raise BundleError(f"{api} refused the token (HTTP {e.code}) — check ROUTEMIND_TOKEN against "
                          f"what that backbone accepts")
    except urllib.error.URLError as e:
        raise BundleError(f"cannot reach {api} — {e.reason}")
    if not tok: raise BundleError(f"{api} answered the token request without a token")
    _HELD[ident] = tok
    return tok


def fetch(api: str, token: str, path: str, accept: str = "application/json", timeout: float = 60):
    url = api.rstrip("/") + "/v1/export/" + path.lstrip("/")
    req = urllib.request.Request(url, headers={"Accept": accept,
                                               "X-Peer-Token": session(api, token, timeout)})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        detail = (e.read().decode("utf-8", "replace") or "").strip()[:200]
        raise BundleError(f"{url} → HTTP {e.code}" + (f" — {detail}" if detail else ""))
    except urllib.error.URLError as e:
        raise BundleError(f"cannot reach {url} — {e.reason}")
    return json.loads(raw) if accept == "application/json" else raw


def collect(api: str, token: str) -> dict:
    """Everything the export surface will give, walked from the areas down.

    **Read from `/v1/export/…` and nowhere else.** That surface is built from the areas somebody
    set `export` on rather than filtered on the way out — server.py: "there is no path
    through this code, and no bug in a token check, that can serve an area nobody decided to share.
    A filter applied on the way out would have to be right every time; a surface built from the
    exported set is right by construction." Deriving the filter again here would make it a second
    place that has to be correct.

    Nodes are gathered by following each area's `entries` rather than by asking for a list, because
    a list is a second thing that can disagree with the tree. Measured against one area: the walk
    reaches 19 of 19 nodes the region holds on disk. Since the directory→file migration a node's
    "files" *are* its child nodes, so following the tree is what collects them — there is no separate
    attachment to fetch.

    **Edges cross; vocabulary does not.** `/v1/export/edges` serves the links whose two ends are
    both in the shared set, so a grafted tree keeps the connections across it. There is no
    `/v1/export/vocab` and this does not invent one: the names those edges use — and the `kind` on
    every node — belong to the sender's vocabulary, and writing entries into somebody else's is not
    something a file should do quietly. `validate` on the receiving side is what says so, by name.
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

    # The links between the exported nodes. Both ends are inside the shared set or the surface does
    # not serve it — an edge naming a node in an area nobody shared would say that node exists, and
    # every 404 here is written so "we do not have it" and "we did not share it" read the same.
    # Measured on the shipped corpus: 32 edges, 4 cross, 4 more are held back for exactly that reason.
    try:
        edges = (fetch(api, token, "edges") or {}).get("edges") or []
    except BundleError:
        edges = []            # an older backbone with no such path; the file then simply has none
    return {"format": "routemind-export/1",
            "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "source": {"api": api, "revision": regions.get("revision")},
            "regions": regions.get("regions") or [], "nodes": nodes, "edges": edges}


def seal(payload: dict, passphrase: str) -> bytes:
    AESGCM, _ = _crypto()
    salt, nonce = os.urandom(16), os.urandom(12)
    key = _key(passphrase, salt, KDF)
    header = {**KDF, "salt": base64.b64encode(salt).decode(),
              "nonce": base64.b64encode(nonce).decode(),
              "created": payload["created"], "source": payload["source"],
              "counts": {"regions": len(payload["regions"]), "nodes": len(payload["nodes"])}}
    hb = json.dumps(header, sort_keys=True).encode()
    body = gzip.compress(json.dumps(payload, ensure_ascii=False).encode())
    return MAGIC + hb + b"\n" + AESGCM(key).encrypt(nonce, body, hb)


def _split(blob: bytes):
    """magic, header, ciphertext — or a BundleError saying which part is wrong.

    Every malformed shape leaves through `BundleError`. A stray `JSONDecodeError` or `ValueError`
    from here reaches the web endpoint as a 500 with a stack trace instead of a sentence, and the
    file being opened is by definition one that arrived from somewhere else.
    """
    if not blob.startswith(MAGIC):
        raise BundleError("not a RouteMind export — it should begin RMEXPORT/1")
    rest = blob[len(MAGIC):]
    nl = rest.find(b"\n")
    if nl < 0:
        raise BundleError("the export is truncated — its header never ends")
    hb, ct = rest[:nl], rest[nl + 1:]
    try:
        header = json.loads(hb)
    except ValueError:
        raise BundleError("the export's header is not readable — the file has been damaged or edited")
    if not isinstance(header, dict) or not {"salt", "nonce", "n", "r", "p"} <= set(header):
        raise BundleError("the export's header is missing what is needed to open it")
    _check_kdf(header)
    try:
        if len(base64.b64decode(header["nonce"])) != 12 or not base64.b64decode(header["salt"]):
            raise ValueError
    except (ValueError, TypeError):
        raise BundleError("the export's header is damaged — its salt or nonce is not readable")
    return header, hb, ct


# 128 * n * r bytes is what scrypt allocates. The default below is ~128MB; this ceiling is 512MB.
MAX_KDF_BYTES = 512 * 1024 * 1024


def _check_kdf(h: dict):
    """Bound the work the header can ask for, before any of it is done.

    The header is authenticated, but only *after* the key exists — and deriving the key is what the
    header describes. So a file claiming `n = 2**30` gets a gigabyte or two spent on it before the
    tag can report that it was never a real export at all. Reading the numbers first costs nothing
    and turns that into a sentence.

    This is the same failure this project keeps meeting from the other side: a check written to
    prevent something, placed after the thing it prevents. The memory guard in the census runner
    computed its ceiling from a formula that returned exactly the value that had already killed the
    machine — right code, evaluated too late to matter.
    """
    if h.get("kdf") not in (None, "scrypt"):
        raise BundleError(f"this export uses {h['kdf']!r}, which this version cannot open")
    try:
        n, r, pp = int(h["n"]), int(h["r"]), int(h["p"])
    except (TypeError, ValueError):
        raise BundleError("the export's header is damaged — its KDF settings are not numbers")
    if n < 2 or n & (n - 1):
        raise BundleError("the export's header is damaged — its KDF cost is not a power of two")
    if not (1 <= r <= 32) or not (1 <= pp <= 16):
        raise BundleError("the export's header asks for KDF settings outside what this version allows")
    if 128 * n * r > MAX_KDF_BYTES:
        raise BundleError(
            f"this export asks for {128 * n * r // (1024 * 1024)}MB to derive its key, over the "
            f"{MAX_KDF_BYTES // (1024 * 1024)}MB this version will spend. Either it was made with "
            "settings this version does not support, or it is not a real export.")


def header_of(blob: bytes) -> dict:
    return _split(blob)[0]


def unseal(blob: bytes, passphrase: str) -> dict:
    AESGCM, _ = _crypto()
    from cryptography.exceptions import InvalidTag
    header, hb, ct = _split(blob)
    key = _key(passphrase, base64.b64decode(header["salt"]), header)
    try:
        body = AESGCM(key).decrypt(base64.b64decode(header["nonce"]), ct, hb)
    except InvalidTag:
        # One message for two causes on purpose: a wrong passphrase and a tampered file are the same
        # failure here, and telling the reader which it was would be guessing.
        raise BundleError("cannot open it — wrong passphrase, or the file has been changed since it "
                          "was made. The header is authenticated along with the contents, so an "
                          "edited header fails here too.")
    try:
        return json.loads(gzip.decompress(body))
    except (OSError, ValueError):
        # Past the tag, so this is not tampering: it is a file this version cannot read.
        raise BundleError("opened, but the contents are not in a form this version understands")
