# Handing an ontology over

A **circuit** or a **peer** reads a remote backbone live. This is for when neither can reach: a
partner behind a firewall, an air-gapped site, an auditor who gets a copy and nothing else.

```sh
./transfer/export.py --api http://their-backbone:8100 --out partner.rmx   # they run this
./transfer/import.py partner.rmx --against data/repo                      # you run this
./transfer/import.py partner.rmx --into ./incoming
```

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
the areas somebody wrote `use_when_export` on rather than filtered on the way out, and re-deriving
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

**Send the passphrase by a different route than the file.**

## Import does not write into an ontology

It unpacks and shows. That is the design, not a missing stage.

An export is somebody else's map. Deciding where a subject lives changes the routing table, and that
table is the text every search reads before choosing anything — on this design's own 700-question
census one row of it lay on the path of 39.7% of walks, and the single wrong answer in all 700 came
from one false sentence in such a row. Importing a stranger's areas straight into a live backbone
would be writing the map from a file that arrived in the post.

`--against <repo>` lists the ids that already exist locally. It is worth running first: exporting
one example backbone into another gave 11 collisions out of 14, because two ontologies that share an
ancestor share names for different subjects. Nothing is renamed automatically — which of the two owns
`payroll` is a decision, not a merge.
