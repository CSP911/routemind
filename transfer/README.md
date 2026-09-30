# Handing an ontology over

A **circuit** or a **peer** reads a remote backbone live. This is for when neither can reach: a
partner behind a firewall, an air-gapped site, an auditor who gets a copy and nothing else.

```sh
./transfer/export.py --api http://their-backbone:8100 --out partner.rmx   # they run this
./transfer/import.py partner.rmx --against data/repo                      # you run this
./transfer/import.py partner.rmx --into ./incoming
```

Or from the screen: **Export** in the header of `/knowledge`, which asks for the passphrase twice and
downloads the same file. It is the same `collect()` and `seal()` — `bundle.py` holds the format and
all three callers import it, rather than each writing out its own idea of the layout.

Typed twice because a mistyped passphrase makes a perfectly valid file that nobody can open, and the
mistake surfaces at the far end, days later, with nothing to go back to. The passphrase is in the
POST body, never in a URL: a URL is the part of a request that gets written down everywhere.

The web container needs `ONTOLOGY_PEER_TOKEN` to read the export surface — compose passes it the same
`EXCHANGE_TOKEN_HOME` the ontology gets. Not an escalation: the web process already proxies the whole
ordinary API on that network, and the token buys it the *narrower* surface. Without one, the button
says so instead of failing.

Needs `cryptography`. The ontology image does not carry it; run the tool where it is installed, or
in a throwaway container:

```sh
docker run --rm --network routemind_default -v "$PWD/transfer:/t:ro" -v "$PWD/out:/out" \
  -e ROUTEMIND_TOKEN -e ROUTEMIND_EXPORT_PASSPHRASE python:3.12-slim \
  sh -c "pip install -q cryptography && python /t/export.py --api http://ontology-b:8100 --out /out/partner.rmx"
```

## What goes in it

**Exactly what a peer would have been able to read, and not a byte more.** `export.py` reads
`/v1/export/…` and nothing else — not the store, not the ordinary API. That surface is built from
the areas somebody set `export` on rather than filtered on the way out, and re-deriving
the filter here would make it a second place that has to be right. So the lines in the file are the
ones written for an outside reader.

A backbone that exports nothing produces an error rather than a valid empty file. An encrypted empty
bundle and a mistake at the sending end look identical to whoever receives it.

## The file

```
RMEXPORT/1\n        magic and version — `head -c 11` tells you what it is
{header json}\n     salt, KDF parameters, when, where from, how many — not secret, and authenticated
<ciphertext>        AES-256-GCM over the gzipped payload
```

The header is passed to GCM as additional data, so editing it fails the tag rather than quietly
changing the key. Someone who has the file but not the passphrase can still see what it claims to
be before deciding whether to type anything at it — verified by changing `"nodes": 14` to `99` in a
copy, which then refuses to open.

AES-256-GCM comes from `cryptography`. `openssl enc` was the alternative and refuses AEAD outright
(`enc: AEAD ciphers not supported`), which leaves encrypt-then-MAC assembled by hand — a standard
shape, but one more thing that has to be right in a file whose purpose is to be trusted by somebody
who cannot check it against the original. The KDF is the library's scrypt rather than
`hashlib.scrypt`, which is absent on some Python builds — Xcode's among them, found by the file
failing to open on the machine that made it.

The format lives in `bundle.py` — `export.py`, `import.py` and the web endpoint all import it, so
there is one definition of the layout rather than one per caller.

### Opening a file that is not one

The KDF parameters sit in the header, and the header is authenticated — but only *after* the key
exists, and deriving the key is the thing the header describes. So a file claiming `n = 2**30` would
have a gigabyte or two spent on it before the tag could report it was never an export at all.
`bundle.py` reads the numbers first and refuses anything over 512MB, which costs nothing and turns
that into a sentence. Measured: 2**19 (512MB) is admitted and fails the tag in 0.9s; 2**20 and above
are refused in 0.00s.

Every malformed shape leaves as one sentence rather than a stack trace — truncated, unreadable
header, not an export at all, wrong passphrase, edited body, edited header. A wrong passphrase and a
tampered file get the *same* message on purpose: they are the same failure to this code, and naming
which one it was would be guessing.

**Send the passphrase by a different route than the file.**

## Grafting it in

```sh
./transfer/import.py partner.rmx --graft data/repo --prefix partner
```

Every id takes the prefix — all of them, not only the ones that clash, so the same export grafted
into two repositories comes out the same in both. The name takes a suffix too: this repository wants
names unique as well as ids, and grafting a corpus that shares an ancestor produced 19 collisions of
each. `regions.json` is regenerated from the files rather than composed here, because it is derived
and the validator compares it field by field against what the files say.

**It is an ordinary write.** A graft goes through `Writer.transact`, the same transaction the screen
and the API use: a dirty tree is refused before anything is written, then mutate, regenerate,
validate, **roll back on any failure**, commit. So a graft that would not validate leaves the
repository exactly as it was, and one that succeeds is already committed under its own message.

It used to do its own writing and its own regenerate, and that is where three bugs came from — no
rollback (files on disk after a failed validate, with "it is a git repository" offered as the undo),
no commit (a dirty tree, in which every later API write is refused), and an edge list it appended to
and could not take back. `--ungraft` and `ontology/tidy.py` go the same way now.

Because it is a write, it needs the service — run it in the ontology container, or from a checkout
whose python has pyyaml. It says so rather than falling back: a second discipline is what produced
the bugs.

The links between the documents come too, renamed with them. Only those with **both** ends in the
shared set: an edge naming a node in an area nobody shared would say that node exists, and every 404
on the export surface is written so "we do not have it" and "we did not share it" read the same. On
the shipped corpus 4 of 32 edges cross and 4 more are held back for exactly that reason, which leaves
12 grafted nodes with no relations — the same 12 that have none inside that area to begin with.

One thing a graft cannot bring: **the names.** A document's `kind`, and a link's relation, belong to
the sender's vocabulary. If the receiving `vocab.yaml` has never heard of one, `validate` refuses and
says which. Nothing here writes entries into somebody else's vocabulary.

And one thing it does bring that wants reading first: the sender's outward line becomes the area's
`use_when` in your table. It is the only line the file has, and an area without one is an area no
walk reaches — but it was written to describe that area to an outsider, not to route your searches.

## Or don't: unpack and look

Without `--graft` it unpacks and shows, and writes into no ontology at all.

An export is somebody else's map. Deciding where a subject lives changes the routing table, and that
table is the text every search reads before choosing anything — on this design's own 700-question
census one row of it lay on the path of 39.7% of walks, and the single wrong answer in all 700 came
from one false sentence in such a row. Importing a stranger's areas straight into a live backbone
would be writing the map from a file that arrived in the post.

`--against <repo>` lists the ids that already exist locally. It is worth running first: exporting
one example backbone into another gave 11 collisions out of 14, because two ontologies that share an
ancestor share names for different subjects. Nothing is renamed automatically — which of the two owns
`payroll` is a decision, not a merge.
