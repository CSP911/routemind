# RouteMind

**An ontology you can see the agent reading.** Split a domain into areas, let each area advertise
itself in one line, and an agent picks from that list before reading anything else. The map draws
that structure as a wiring diagram, and one click shows you **the exact text an agent is handed**.

The domain is not in this code. The vocabulary and the areas are data, and the data is your own git
repository.

![The RouteMind map: a backbone carrying five areas, two of them opened to show the nodes they hold,
with the routing table each one hands an agent one button away.](docs/img/map.jpg)

---

## How it works

![Each area summarizes itself into one advertised route; the backbone holds one row per area, and no
more. An agent reads that list at hop 0, picks every area the question belongs to — a client dinner on
the corporate card is expense and approval, not one of them — and only then reads
documents.](docs/img/backbone-as-advertisement.svg)

The shape is borrowed from dynamic routing on a network, and the borrowed part is the useful one:
**an area advertises where it is relevant, rather than exposing everything it holds.** An agent reads
one line per area, routes on that, and reads documents only inside what it picked — so the cost of
finding something does not grow with how much there is.

The two things that make it work are the two easiest to get wrong. **`use_when` is the only text read
before a choice is made**, so an area with a title and no reason is one nobody picks. And **absence is
decided at hop 0 only** — an area's own table says what that area holds, never what RouteMind lacks.

Some questions do not sit in one area: settling a trip is three at once, and picking one answers a
third of it. An **overlay** is that working set made as an object — the areas, why each is in it, and
what was actually used to answer. The agent draws it; RouteMind serves it and keeps the record.

### Back-Bone, AS, and the line between them

Three words, and the screen uses them too.

```
   BACK-BONE ─ the whole of this ontology, and the only place absence may be claimed
       │       hop 0: one row per AS, nothing else
       │
       ├── AS  expense       "what to do with a receipt · whether the corporate card
       │                      may be used here · how much a business trip pays"
       │        │
       │        ├── AS  corp-card        ← an AS holds AS's. The map draws both the same
       │        │    ├── card-limit      because they are the same thing: a row that
       │        │    └── card-loss         advertises itself and may hold more
       │        └── AS  evidence
       │
       ├── AS  approval      "whom to put in the approval chain · whether a team
       │                      lead can sign this off"
       └── AS  payroll       "what this payslip line means · whether an allowance
                              is tax free"
```

**The Back-Bone holds one row per AS and nothing more.** Not a summary of what is inside, not a
sample — one line saying *when you would come here*. That line is `use_when`, and it is the only text
an agent reads before choosing.

**An AS advertises; it does not expose.** What is inside an AS is invisible from hop 0 and stays
invisible until something picks it. So hop 0 is the same size at 80 documents and at 8,000, and the
cost of choosing does not grow with what you have.

**Absence belongs to the Back-Bone alone.** An AS's own table says what that AS holds — never what
RouteMind lacks. An agent told otherwise answers "there is no such thing" from inside one area, with
five others unlooked-at. Every table says which of the two it is, in its own footer.

Advertising is the same act one level down: `corp-card` advertises to `expense` exactly as `expense`
advertises to the Back-Bone. That is why the map draws an AS and a node identically — they are the
same kind of thing, and a walk is the same step repeated.

**[docs/ROUTING.html](docs/ROUTING.html)** — the whole structure in detail, in a browser.
**[docs/OVERLAY.md](docs/OVERLAY.md)** — overlays.

---

## Measured

700 questions over one frozen corpus of 1,126 documents. Four arms, all of them a census — no
sampling. One fresh agent per question, nothing shared between questions.

| | plain RAG | + reranker | RouteMind |
|---|---|---|---|
| a question in codes the rows use | 0.991 | 1.000 | **1.000** |
| **a question in a person's words** | **0.028** | **0.069** | **1.000** |
| **a rule two revisions back** | **0.133** | **0.200** | **1.000** |
| overall | 0.516 | 0.541 | **0.999** |

The two bold rows are the point. Retrieval does not *degrade* there — it fails outright, because
every newer version of a subject outranks the one being asked for and they all look alike.

**And what it costs.** A walk is 6.7 tool calls, 23–111 seconds, and $0.12–$0.28 a question, against
one sub-second embedding call. **320 of those 700 questions are ones retrieval already answers first
time** — nothing here argues for walking those. Which arm to use is a question about the mix of
questions you actually get, and that is not measured here for anyone but this corpus.

**The one miss in 700 was a wrong sentence in the map**, not a wrong document: a forwarding note said
a superseded page was still current, and both routing arms obeyed it identically. An agent that
trusts the map inherits the map's errors silently — retrieval cannot fail that way, because it reads
no map. `mapcheck` now refuses that class of defect before any run starts.

Still unmeasured: whether a **correct** map has a size at which it stops working. One corpus size,
and a limit cannot be seen from one point.

**[eval/report/report-en.html](eval/report/report-en.html)** — the whole thing with figures ·
**[한국어](eval/report/report-ko.html)** · **[eval/](eval/)** — corpus, gold sets, every run record.

---

## Quickstart

Docker, with `docker compose`. That is all the service needs — the containers carry python and git.

```sh
git clone https://github.com/CSP911/routemind.git routemind && cd routemind
./install.sh --name acme --port 9000
```

→ **http://localhost:9000**

Two answers, and both have working defaults. Run `./install.sh` bare and it asks for them:

    --name    what this domain is called. One word, lowercase.
              A domain is one exchange and the backbones that meet in it, and this
              name is in every address a linked backbone prints: /v1/peers/acme/…
              Asked once, at install — renaming it later rewrites addresses
              somebody may already have followed.

    --port    where the map answers. 8080 if you say nothing.

It then asks whether you have an LLM; Enter skips it. `--no-llm` does not ask, and
`--llm-provider … --llm-url … --llm-key … --llm-model …` answers without being asked. An LLM changes
exactly one thing: a **✨ Suggest** button that drafts a routing line for you to edit.
**[docs/LLM.md](docs/LLM.md)**.

Safe to run again — an existing `.env` is kept and only what you pass is replaced.

**Three containers, no database.** `ontology` is the API and the only thing that touches your git
repository; `web` is the map and a proxy in front of it; `exchange` is where backbones meet — **empty
and idle until you link one**, and there from the first boot so that adding a second backbone is a
file and a registration rather than a migration. On first boot an empty ontology is laid into
`data/repo` and that directory becomes a git repository. Every write **commits** into it, so undo is
`git revert`.

### Start from the worked example, not an empty map

An empty install is a backbone with no areas: correct, and hard to read.
[`examples/back-office`](examples/) is five areas, 79 entities, five levels deep. Copy it in **before**
the first boot:

```sh
mkdir -p data/repo && cp -r examples/back-office/. data/repo/
./install.sh --no-llm
```

### Without install.sh

```sh
cp .env.example .env
printf 'KNOWLEDGE_UID=%s\nKNOWLEDGE_GID=%s\n' "$(id -u)" "$(id -g)" >> .env
mkdir -p data/repo data/publish data/overlays data/harness data/exchange data/access
docker compose up -d --build
./check/smoke.sh
```

The `mkdir` is not tidiness. Docker creates a missing bind-mount path as **root**, and this container
is not root, because it commits into a repository you own. A list short by one directory is a
container that never becomes healthy.

### When it does not come up

| What you see | Why | What to do |
|---|---|---|
| `./install.sh: Permission denied` | The tree arrived without its exec bits — a zip, or a share that does not carry them | `chmod +x install.sh check/*.sh check/*.py check/*.mjs` |
| `FATAL: /data/repo is not writable by uid …`, then a restart loop | Docker invented a bind-mount path as root | Remove it, `mkdir` **all six** as above, check `KNOWLEDGE_UID`/`KNOWLEDGE_GID` against `id -u` / `id -g`, start again |
| `exec /app/entrypoint.sh: no such file or directory`, on a file that is plainly there | CRLF line endings, so the kernel read the shebang as `/bin/sh\r` | Re-clone with `git clone`, which honours the repository's `eol=lf`. In place: `git add --renormalize . && git checkout -- .` |
| `port is already allocated` | Something else holds 8080 | `WEB_PORT=9000` in `.env`, then `docker compose up -d` |
| Every write is refused **read-only** | `data/repo` has uncommitted changes | Commit or revert them, then POST `/api/knowledge/publish` |
| A save fails with `git add -A failed: … index.lock` | Something else is running git in `data/repo` — your own shell, an editor's git integration, a second ontology on the same mount | Wait and retry; the service's own polling no longer does this. If it persists, `docker compose logs ontology` and look for a second writer |
| A change to `static/` or `ontology/` does nothing | Both are `COPY`ed into the image | `docker compose up -d --build` |
| Your first node is refused | Its `kind` is not in `vocab.yaml` — the point of that file | Below |
| `regions.json <area>: … no longer matches the files it is derived from` | Someone edited an area's `.md` by hand and did not regenerate | **[docs/DATA-REPO.md](docs/DATA-REPO.md)** |
| Anything else | | `docker compose logs -f ontology web` |

---

## First — `vocab.yaml` is your domain

A node's `kind` and an edge's `rel` **must appear in the vocabulary**, so until you edit this file
your first node is refused. The starter set (`system` · `tool` · `store` · `host` · `channel` ·
`task` · `party`) is a starting point, not a schema. Edit `data/repo/vocab.yaml` and commit — there is
no vocabulary editor on screen yet.

It is also where you say what may leave. `export: no` on a kind stops that sort of thing crossing to
another domain — one decision per kind rather than per document.

## Second — one area

On the map, at the backbone: **`+ New AS`**. Two sentences are written together:

| Field | What it is | Without it |
|---|---|---|
| **When to choose this area** (`use_when`) | why an agent picks this row out of the list | a row with a title and no reason — **nobody picks it** |
| **Core one-liner** | this area's row in `CORE.md` | hop 0 goes out with an empty description |

Then, from that area's rack: `+ New node` → `+ New data` to attach documents.

---

## Connecting an agent

Optional — the map works on its own. An agent reads this ontology the same way in every case: **fetch
the list of areas, pick one, fetch that area, read what it points at.** Two operations, never a third.

```sh
python3 mcp/knowledge_mcp.py --api http://localhost:8080/api/knowledge
```

One file, stdlib only, python 3.7 or newer: no install, no virtualenv, nothing to build. **Opening
this repository in Claude Code is the whole setup** — `.mcp.json` registers it. For Codex, Cursor,
Claude Desktop and anything else, one config block each in **[docs/AGENTS.md](docs/AGENTS.md)**.

Two tools do the reading — `knowledge_table(path?)` for a routing table and `knowledge_read(path)` for
one document — and the rest of the set appears only where the install has the thing it needs:
`knowledge_overlay(op)` where overlays are kept, `knowledge_write(...)` where there is a `workspace`
AS to write into, and `knowledge_circuit(op)` always. Five here; your install may offer three.

`/circuit <url> <token>` is the same thing from a person's side, and the MCP `circuit` prompt is the
same again with fields instead of a tool call.

The area list travels in the server's `instructions`, so **you do not have to name RouteMind in the
question** — what decides whether the agent comes here is the `use_when` line on each area.

Without MCP, **Copy for an agent** on the map puts the same advertisement on the clipboard. All three
ways hand over one formatter's output; three descriptions of one ontology would drift.

```sh
./check/mcp-check.py http://localhost:8080/api/knowledge      # the protocol and a whole walk
./check/all.sh                                                # and everything else — docs/CHECKS.md
```

---

## How old is this row

Material goes stale and gets replaced; the old record still has to exist. Both versions are in the
map, both look valid, and an agent reads both as current — so it sometimes answers from the one that
was replaced. That is the failure this is for.

Every routing row carries two times:

```
  KIND   ADDRESS                          AGE          WHY YOU WOULD PICK THIS ROW
  table  /v1/nodes/card-limit             2y / today   Card limits — what the card may be used for …
  file   /v1/nodes/qualified-list/body    2y / 2y      What qualifies as evidence, and the ceiling …
  table  /v1/peers/acme/…/regions/payroll  —           what this payslip line means …

         └─ route ─┘ └─ document ─┘
            how long        when what it
            this path       points at last
            has been here   moved
```

**Two, because one cannot say both.** A route laid down two years ago whose document was rewritten
today is **current** — somebody is maintaining it. The same route over a document that has not moved
in two years is the one worth asking about before quoting it. A single "age" collapses those into one
warning, and the first is most of a healthy map: a rule that has not needed changing is the most
reliable row in the table, not the least.

So the second number answers *"should I look for something newer"*, and the first says whether this
path is settled or was only just laid down.

**Both come from git** — the last commit that added the file, the last that touched it. Not a stored
field: that would be a second copy that drifts, and a wrong date here is worse than none, because it
is a reason to trust the wrong row. One pass over the log per commit, cached on the revision.

**`—` is not "new". It is *not known*** — usually a row that came across a link, whose history belongs
to the backbone that owns it. It was blank at first, which reads as a row somehow outside time and
would have made a reader quietly prefer the row the system knows least about.

**What this is not: a supersession record.** Old is not wrong and new is not right — an agent that
prefers the newest row picks a draft over a rule that has held for a decade. The column supports
*asking*, not deciding. What settles which of two documents is current is somebody's statement that
one replaced the other, and that is not this.

**[docs/AGE.md](docs/AGE.md)**.

---

## More than one backbone

An install is **one backbone and an exchange**. A **domain** is one exchange and the backbones on it —
head office and a subsidiary are one domain; a company and its supplier are two.

An area crosses by somebody deciding it does, and by nothing else. The line a peer reads is the
area's own `use_when` — one sentence, the same one this backbone routes on:

| In the area's own `.md` | What it does |
|---|---|
| `export: yes` | this area crosses a link. Absent means it crosses none — the whole opt-in |
| `use_when` | the sentence it crosses with, and the one this backbone routes on. One, not two |
| `export_to` | which peers may see it at all. Absent means everyone linked |
| `export: no` on a kind, in `vocab.yaml` | that sort of thing never leaves, whatever an area says |

Three properties are worth knowing before relying on it:

- **Nothing is copied.** A document is relayed, held for one request and discarded. No agent ever
  holds a peer's credential, and nothing at the far end keeps a copy — so the only record that a read
  happened is the one the **owner** writes. That is `ONTOLOGY_ACCESS`: one JSON line per read, naming
  which link carried it and who was at the far end, refusals included.
- **No transit.** A room offers a neighbour its own backbones and never a third room's. Two
  organisations meet without either joining the other's.
- **Absence suspends itself.** Hop 0 may only claim something is missing while every link is up, and
  says so itself when one is not.

The screen draws one card per domain — what this backbone holds, what reaches it, and any link that
is not answering. `./examples/seed-demo.sh` builds six backbones across two rooms, one deliberately
down, which is the shape the screens are designed against.

### Two ways to reach another backbone

```
  PEERING — a standing arrangement, committed, everyone sees it
  ─────────────────────────────────────────────────────────────
     your BB ──── peers.yaml ────▶  EXCHANGE  ◀──── members.yaml ──── their BB
                  (in git)                              (in git)

     their AS appears in YOUR hop 0, mixed in with your own rows.
     An agent never learns there is a link.


  CIRCUIT — this session only, nothing written on either side
  ──────────────────────────────────────────────────────────
     /circuit http://their-host:8100 <token>

     you ────────────────────────────────────────▶ their BB
                                                   read-only

     their AS appears under /v1/circuits/<name>/… , beside yours but
     never in it. Closing the connection ends it. No file changes.
```

Both halves of a **peering** are declarations — the backbone names the room, the room names the
backbone — so nobody is enrolled by one side alone. A **circuit** is the opposite by design: one
person, one session, one address and a token somebody handed them.

Use peering for a relationship. Use a circuit to look at somebody's ontology now.

### The credential is good for six hours

The secret in `.env` used to be presented on every read across every link — so it was in every
request, every proxy log and every transcript, and it never expired.

```
     enrolment key ──▶  POST /v1/peers/token  ──▶  session token, 6h
     (in .env, rarely used)                        (what every read carries)
```

The key now opens one thing: asking for a session. It is presented about four times a day per link
instead of thousands of times, and a session that leaks off the read path stops being worth anything
by the end of the shift. **A session cannot mint another** — otherwise a leaked one renews itself for
ever and the six hours bound nothing. Sessions live in memory, so a restart revokes every one of
them, and clients re-mint on a 401.

It does **not** prove who is at the far end. A short-lived token handed to an endpoint that is not who
it claims to be is still handed over; what refuses is a separate rule, that a token never crosses
plain `http` to a public address.

**[docs/PEERING.md](docs/PEERING.md)** is the contract, including the operator's screen at `:8090`.

---

## Carrying one where a link cannot reach

A partner behind a firewall, an air-gapped site, an auditor who gets a copy and nothing else.

```sh
./transfer/export.py --api http://localhost:8100 --token "$TOK" --out partner.rmx
```

or **Export** in the map's header, which downloads the same file.

```
  their BB ──▶  partner.rmx  ──▶  your repository
                (encrypted)        under a prefix you choose

  AES-256-GCM · scrypt · the header is authenticated, so it says what the file
  claims to be before anyone types a passphrase at it, and editing a byte of it
  fails the tag rather than quietly deriving a different key.
```

**It holds exactly what a peer would have been able to read** — the AS's somebody set `export` on,
their documents, and the links between them where both ends are inside that set. Nothing else. That
is not a filter applied on the way out; it is read from the same surface a link reads, so there is no
path through the code that can serve an AS nobody decided to share.

Opening it:

```sh
./transfer/import.py partner.rmx --against data/repo      # what would collide
./transfer/import.py partner.rmx --graft data/repo --prefix partner
```

Every id takes the prefix, not only the ones that clash, so the same file grafted into two
repositories comes out the same in both. The receiving repository's **own validator** decides whether
the result is coherent — a graft it rejects is one the service would refuse to serve. Without
`--graft` it unpacks to a directory and writes into no ontology at all.

One thing to look at first afterwards: the sender's routing line is now a row in **your** table. It
is the sentence they route on, which is the right kind of sentence — but it was written about their
map.

**[transfer/README.md](transfer/README.md)**.

---

## Layout

```
ontology/     the ontology API — python + pyyaml + git. Knows nothing about any domain
exchange/     where backbones meet. No repository, no areas, no hop 0
web/          the map and a proxy — one FastAPI file. Knows nothing about any domain
admin/        the operator's screen for an exchange. Off unless EXCHANGE_ADMIN_TOKEN is set
mcp/          the MCP server, so any MCP-capable agent can read the ontology
transfer/     export, import and graft — one encrypted file, for where a link cannot reach
static/       the map screen
seed/         an empty ontology, copied into data/repo on first boot
examples/     one worked ontology, and seed-demo.sh — six backbones across two rooms
check/        every check. docs/CHECKS.md
docs/         everything below

data/repo     ← your ontology. A git repository, and the only thing to back up
data/publish  derived from data/repo. Safe to delete; it is rebuilt
data/overlays one question's working set each — run evidence, not structure
data/harness  the curator's store: the review queue behind "Advertise upstream"
data/exchange members.yaml — who meets at this install's exchange
data/access   who read what across a link, one file per UTC day
```

## Everything else

| | |
|---|---|
| [ROUTING.html](docs/ROUTING.html) | the whole structure, in a browser |
| [PEERING.md](docs/PEERING.md) | links between backbones, circuits, six-hour sessions, the operator's screen |
| [AGE.md](docs/AGE.md) | the two times on a routing row, and what they deliberately do not say |
| [transfer/README.md](transfer/README.md) | carrying a backbone somewhere a link cannot reach |
| [OVERLAY.md](docs/OVERLAY.md) | the working set for one question |
| [AGENTS.md](docs/AGENTS.md) | connecting an agent — every client, and the tools |
| [LLM.md](docs/LLM.md) | the optional ✨ Suggest buttons, and the three provider wires |
| [AUTH.md](docs/AUTH.md) | who may write, and whose name goes on the change |
| [DATA-REPO.md](docs/DATA-REPO.md) | your ontology as a git repository, and the one derived file in it |
| [CHECKS.md](docs/CHECKS.md) | every check, what it proves, and where it can run |
| [PLATFORMS.md](docs/PLATFORMS.md) | macOS, Linux, Windows — and what differs on each |
| [I18N.md](docs/I18N.md) | English, 한국어, 日本語, 简体中文 — and adding one |
| [SCENARIOS.md](docs/SCENARIOS.md) | the routing table over a whole lifetime |
| [DOMAIN-NEUTRALITY.md](docs/DOMAIN-NEUTRALITY.md) | which rules still belong to the domain this came from |
| [PROVENANCE.md](docs/PROVENANCE.md) · [DELTA-FROM-IRIS.md](docs/DELTA-FROM-IRIS.md) | where this came from, and what changed |
| [TODO.md](docs/TODO.md) | known gaps, written down rather than glossed over |
| [eval/](eval/) | the study — pre-registered before it is run |

---

## Contact

Business inquiries, collaboration, or just curious: **qct8377@gmail.com**
LinkedIn → [linkedin.com/in/cspark911](https://www.linkedin.com/in/cspark911/)
Bug reports and questions → [GitHub Issues](https://github.com/CSP911/routemind/issues)

## License

MIT — see [LICENSE](LICENSE).
