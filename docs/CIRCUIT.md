# Reading another backbone — circuits

A **circuit** is one agent session reading another RouteMind: opened by the agent, read-only, nothing
written on either side, gone when the session ends. It is the one way left to read another backbone
(operator, 2026-10-08). Standing links (`peers.yaml`), the exchange they met at, its operator screen
and encrypted export bundles were retired that day; this page is what remains of docs/PEERING.md.

```
/circuit http://their-host:8080 <their key>              a person, in Claude Code
knowledge_circuit { op: open, url, token, name }           an agent, through the MCP server

Their areas appear under /v1/circuits/<name>/… , beside yours, never in it.
```

The URL is **their install's address** — the same one their map answers on. The web app passes the
two paths a circuit uses through to the ontology, outside its own login door, because they carry
their own key. (Until 2026-10-08 they lived only on the ontology's own port, which the shipped
compose does not publish, so a circuit could reach an install only where somebody had published 8100
by hand.)

## What crosses

**An area crosses by somebody setting `export: yes` on it, and by nothing else.** On the map that is
the area's **Export** card, which files the decision through the review queue like any other routing
change. The line a reader sees is the area's own `use_when` — one sentence, the same one this
backbone routes on (operator, 2026-09-29).

**A kind marked `export: no` in `vocab.yaml` never crosses, whatever its area says:**

```yaml
kinds:
  - id: table
    desc: a table of values — amounts, caps, rates, day counts
    export: no
```

An entity of that kind is left out of every listing and refused by address, and so is everything
under it; an area whose representative is of that kind is not offered at all. This is the one thing a
kind does.

**Drafts do not cross,** and neither does anything under one.

## The export surface is separate, not the ordinary one behind a check

`/v1/export/…` builds every answer from the exported set, so no path through it — and no mistake in a
key check — reaches an area nobody shared. A filter applied on the way out has to be right every time;
a surface built from the exported set is right by construction.

* **404, never 403,** for anything outside it. Whether this backbone holds something it has not shared
  is not the reader's business either.
* **Every address leaving it is moved onto it.** The ordinary reader prints `/v1/nodes/x`, and a
  reader following that would resolve it against *its own* ontology. The circuit then moves every
  address under `/v1/circuits/<name>/…` on the reader's side, so "use the address exactly as printed"
  stays true across it.
* **Read-only.** Writes go to the backbone that owns the area, through its own screen and its own
  review queue.

## The key, and six hours

`KNOWLEDGE_CIRCUIT_TOKEN` in `.env` — `install.sh` generates one on the first run and keeps it. Empty
makes the whole surface answer 501. Give it to whoever should be able to read you. (An install made
before 2026-10-08 has it as `EXCHANGE_TOKEN_HOME`; compose still reads that when the new name is
unset, and `install.sh` copies it across.)

It is an **enrolment key**. It opens one thing:

```
POST /v1/peers/token      X-Peer-Token: <key>
  → { "token": "...", "expires_in": 21600 }
```

and every read carries that six-hour session instead. The long-lived secret is then used about four
times a day per reader rather than on every request, and anything that leaks off the read path stops
being worth something by the end of the shift (operator, 2026-09-29).

**A session cannot mint another** — otherwise a leaked session renews itself for ever. **Sessions live
in memory,** so a restart revokes every one; the circuit re-mints on the 401 and carries on.
`ONTOLOGY_PEER_SESSION_TTL` overrides the six hours, in seconds.

**What this does not do** is prove who is at the far end. A circuit refuses to send a key over plain
`http` to a public address — that would be a bearer secret in clear text on the wire — and that is the
whole of the endpoint protection. Use https, or a private address.

## Who read what

**Nothing is copied.** Every read through a circuit is a read of the far end, held for one request and
discarded. So the owner records one JSON line per read of the export surface: when, what was asked for,
served or refused, and how big. **Refusals are recorded too, and matter more** — a run of them is the
only signal there is that the surface is being probed rather than used. A read without a valid
session is recorded before it is refused.

To stderr always, and to `data/access` as well — one file per UTC day, because stderr rotates away.

## What absence means across a circuit

Only a backbone's own hop 0 may say something is not there. A circuit's table says what *they*
exported: not finding something there means they did not share it, not that they do not have it. The
circuit's table says so under every listing.

## Checks

* `check/circuit-check.py` — against the install, through its web port: a wrong key mints nothing, the
  key itself reads nothing, a session reads only what is set to export, and an agent's circuit opens
  at the install's address and walks it.
* `check/follow-check.py` — two backbones: exporting, rewording and withdrawing on one is in the other's
  next read through a circuit, and a restart at the far end costs a re-mint, not the walk.
* `check/session-check.py` — the six-hour sessions, mostly what must **not** work.
* `check/drift-check.py` and `check/hyphen-check.py` — the export surface against the files' truth, and
  a hyphenated area on every path a reader takes.
* `check/install-check.sh` — a clean clone, then the export decision as another backbone's circuit
  sees it.
