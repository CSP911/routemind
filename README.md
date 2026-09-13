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

**[docs/ROUTING.html](docs/ROUTING.html)** — the whole structure in detail, in a browser.
**[docs/OVERLAY.md](docs/OVERLAY.md)** — overlays.

---

## Quickstart

Docker, with `docker compose`. That is all the service needs — the containers carry python and git.
The checks at the end use the host's `curl`, `python3` and `node` if they are there; without them the
install still comes up, it just verifies less.

```sh
git clone https://github.com/CSP911/routemind.git knowledge && cd knowledge
./install.sh
```

→ **http://localhost:8080**

In order, `install.sh` copies `.env.example` to `.env` and appends **your own uid/gid**; asks once
whether you have an LLM (Enter skips it); `mkdir -p`s all six bind-mount directories **before**
compose, on purpose; brings the stack up; reads `/api/app-config` and tells you which mode you ended
up in; and runs `check/smoke.sh`.

Safe to run again — an existing `.env` is kept and only what you pass is replaced. `--no-llm` skips
the question entirely; `--llm-provider openai --llm-url … --llm-key … --llm-model …` answers it
without being asked. An LLM is optional and changes exactly one thing: a **✨ Suggest** button that
drafts a routing line for you to edit. **[docs/LLM.md](docs/LLM.md)**.

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

Three tools: `knowledge_table(path?)` for a routing table, `knowledge_read(path)` for one document,
and `knowledge_overlay(op)` for a working set where the install keeps overlays. The area list travels
in the server's `instructions`, so **you do not have to name RouteMind in the question** — what
decides whether the agent comes here is the `use_when` line on each area.

Without MCP, **Copy for an agent** on the map puts the same advertisement on the clipboard. All three
ways hand over one formatter's output; three descriptions of one ontology would drift.

```sh
./check/mcp-check.py http://localhost:8080/api/knowledge      # the protocol and a whole walk
./check/all.sh                                                # and everything else — docs/CHECKS.md
```

---

## More than one backbone

An install is **one backbone and an exchange**. A **domain** is one exchange and the backbones on it —
head office and a subsidiary are one domain; a company and its supplier are two.

An area crosses by writing the line it wants to show in the *other* backbone's hop 0, and by nothing
else:

| In the area's own `.md` | What it does |
|---|---|
| `use_when_export` | the line strangers see. No line, no crossing — this is the whole opt-in |
| `export_to` | which peers may see it at all. Absent means everyone linked |
| `use_when_export_for` | say it differently to one named peer |
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

**[docs/PEERING.md](docs/PEERING.md)** is the contract, including the operator's screen at `:8090`.

---

## Layout

```
ontology/     the ontology API — python + pyyaml + git. Knows nothing about any domain
exchange/     where backbones meet. No repository, no areas, no hop 0
web/          the map and a proxy — one FastAPI file. Knows nothing about any domain
admin/        the operator's screen for an exchange. Off unless EXCHANGE_ADMIN_TOKEN is set
mcp/          the MCP server, so any MCP-capable agent can read the ontology
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
| [PEERING.md](docs/PEERING.md) | links between backbones, domains, and the operator's screen |
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

---

## Contact

Business inquiries, collaboration, or just curious: **qct8377@gmail.com**
LinkedIn → [linkedin.com/in/cspark911](https://www.linkedin.com/in/cspark911/)
Bug reports and questions → [GitHub Issues](https://github.com/CSP911/routemind/issues)

## License

MIT — see [LICENSE](LICENSE).
