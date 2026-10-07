# RouteMind

**An ontology you can see the agent reading.** Split a domain into areas, let each area advertise
itself in one line, and an agent picks from that list before reading anything else. The map draws
that structure as a wiring diagram, and one click shows you **the exact text an agent is handed**.

The domain is not in this code. The vocabulary and the areas are data, and the data is your own git
repository.

![The RouteMind map: a backbone carrying five areas, two of them opened to show the nodes they hold,
with the routing table each one hands an agent one button away.](docs/img/map.jpg)

On 700 questions over one frozen corpus, asked **in a person's words** rather than in the codes the
documents use, retrieval scores **0.028** and this scores **1.000** — and it costs 6.7 tool calls and
20–100× more per question, which is why 320 of those 700 are questions nothing here argues for
walking. [The study](#measured), the corpus and every run are in this repository.

```sh
./install.sh --port 9000   # then `claude` in the same directory
```

---

## How it works

![Each area summarizes itself into one advertised route; the backbone holds one row per area, and no
more. An agent reads that list at hop 0, picks every area the question belongs to — a client dinner on
the corporate card is expense and approval, not one of them — and only then reads
documents.](docs/img/backbone-as-advertisement.svg)

The shape is borrowed from dynamic routing on a network, and the borrowed part is the useful one: an
area advertises **where it is relevant**, not everything it holds. So the cost of finding something
does not grow with how much there is.

The thing easiest to get wrong is that **`use_when` is the only text read before a choice is made** —
an area with a title and no reason is one nobody picks.

### Back-Bone, AS, and the line between them

```
   BACK-BONE ─ the whole of this ontology. Hop 0: one row per AS, nothing else,
       │       and the only place absence may be claimed
       │
       ├── AS  expense    "what to do with a receipt · whether the corporate card
       │        │          may be used here · how much a business trip pays"
       │        ├── AS  corp-card   ← an AS holds AS's: the same thing one level
       │        │    └── card-limit   down, advertising itself the same way
       │        └── AS  evidence
       ├── AS  approval   "whom to put in the approval chain · whether a team
       │                   lead can sign this off"
       └── AS  payroll    "what this payslip line means · whether an allowance
                           is tax free"
```

**An AS advertises; it does not expose.** What is inside is invisible from hop 0 until something
picks it — so hop 0 is the same size at 80 documents and at 8,000.

**Absence belongs to the Back-Bone alone.** An AS's table says what that AS holds, never what
RouteMind lacks. Every table says which of the two it is, in its own footer.

### Overlays

Some questions do not sit in one area: settling a trip is three at once. An **overlay** is that
working set made as an object — the areas, why each is in it, and what was used to answer.
**[docs/OVERLAY.md](docs/OVERLAY.md)**.

## Measured

700 questions over one frozen corpus of 1,126 documents. Four arms, all of them a census — no
sampling, one fresh agent per question.

| | plain RAG | + reranker | RouteMind |
|---|---|---|---|
| a question in codes the rows use | 0.991 | 1.000 | **1.000** |
| **a question in a person's words** | **0.028** | **0.069** | **1.000** |
| **a rule two revisions back** | **0.133** | **0.200** | **1.000** |
| overall | 0.516 | 0.541 | **0.999** |

The two bold rows are the point: retrieval does not *degrade* there, it fails outright, because every
newer version of a subject outranks the one being asked for and they all look alike.

**What it costs.** A walk is 6.7 tool calls, 23–111 seconds and $0.12–$0.28 a question against one
sub-second embedding call — and **320 of those 700 are questions retrieval already answers first
time.** Nothing here argues for walking those.

**The one miss in 700 was a wrong sentence in the map**, not a wrong document, and both routing arms
obeyed it identically. An agent that trusts the map inherits the map's errors silently. Still
unmeasured: whether a *correct* map has a size at which it stops working.

**Check it rather than take it.** The corpus is 865 documents in `bench/corpus/`, the gold sets are
in `eval/gold/`, the generator that made the corpus is `bench/spec.yaml` + `bench/generate.py`, and
every run — including the ones that failed — is in `eval/runs/`. Re-running needs an API key and
`./bench/run.py eval/gold/<set>.yaml`; **[bench/README.md](bench/README.md)** has the order.

**[eval/report/report-en.html](eval/report/report-en.html)** — the whole thing with figures ·
**[한국어](eval/report/report-ko.html)** · **[eval/PREREGISTRATION.md](eval/PREREGISTRATION.md)** —
written and frozen before any of it ran.

## Quickstart

Docker, with `docker compose`. That is all it needs — the containers carry python and git.

```sh
git clone https://github.com/CSP911/routemind.git routemind && cd routemind
./install.sh --port 9000
```

→ **http://localhost:9000**

`--port` is where the map answers, 8080 by default. Run `./install.sh` bare and it asks, then asks
whether you have an LLM — Enter skips it, and
`--no-llm` does not ask. An LLM changes one thing: a **✨ Suggest** button that drafts a routing line
for you to edit.

Safe to run again; an existing `.env` is kept and only what you pass is replaced.

**Two containers, no database.** `ontology` is the API and the only thing that touches your git
repository; `web` is the map and a proxy. On first boot an empty ontology is laid into `data/repo` and that becomes a git repository —
every write **commits**, so undo is `git revert`.

Start from [`examples/back-office`](examples/) rather than an empty map: five areas, 79 entities,
five levels deep. **[docs/INSTALL.md](docs/INSTALL.md)** — that, the manual route, what to do when it
does not come up, and the first two things to write.

**Already running one?** [docs/UPGRADE.md](docs/UPGRADE.md) — applying an update to an install that
holds your own data: four steps, what the restart changes on its own, and how to check it worked.

## Connecting an agent

Optional — the map works on its own. An agent reads this ontology the same way every time: **fetch
the list of areas, pick one, fetch that area, read what it points at.** Two operations, never a third.

```sh
python3 mcp/knowledge_mcp.py --api http://localhost:8080/api/knowledge
```

One file, stdlib only: no install, nothing to build. For **Claude Code** there is nothing to do at
all — `install.sh` writes `.mcp.json` at the root, pointed at the port you chose, so `cd routemind &&
claude` is the whole setup and `/mcp` shows the tools.

`knowledge_table(path?)` and `knowledge_read(path)` do the reading. Every walk starts at hop 0 —
`knowledge_table` with no address, the list of areas — and below it every call needs a one-line `why`,
or is refused with the way back. The agent carries no id; the server remembers hop 0 for its session.
Only someone who has seen the whole list may say something is not here (`docs/INVARIANTS.md`).
`knowledge_place` finds where a new page belongs, and `knowledge_circuit` reads another backbone —
four tools in all. `/circuit <url> <token>` is the same thing from a person's side.

The area list travels in the server's `instructions`, so **you do not have to name RouteMind in the
question** — what decides whether the agent comes here is the `use_when` line on each area. Without
MCP, **Copy for an agent** on the map puts the same text on the clipboard; all of them hand over one
formatter's output, because three descriptions of one ontology would drift.

**[docs/AGENTS.md](docs/AGENTS.md)** — every client, the tools, and the prompts.

## How old is this row

Material goes stale and gets replaced; the old record still has to exist. Both versions are in the
map, both look valid, and an agent reads both as current — so it sometimes answers from the one that
was replaced.

Every routing row carries two times:

```
  KIND   ADDRESS                        AGE          WHY YOU WOULD PICK THIS ROW
  table  /v1/nodes/card-limit           2y / today   Card limits — what the card may be used for …
  file   /v1/nodes/qualified-list/body  2y / 2y      What qualifies as evidence, and the ceiling …

         how long this path ─┘    └─ when what it points at last moved
         has been here
```

**One number cannot say both.** A two-year-old route over a document rewritten today is current —
somebody is maintaining it. The same route over a document that has not moved is the one to ask about
before quoting it. Both come from git, so there is nothing to keep in sync.

It is **not** a supersession record: old is not wrong, and an agent that prefers the newest row picks
a draft over a rule that has held for a decade. The column supports asking, not deciding.

**[docs/AGE.md](docs/AGE.md)**.

## Reading another backbone

Another RouteMind can read yours — and you theirs — through a **circuit**: one agent session, nothing
written on either side, gone when the session ends.

```
/circuit http://their-host:8080 <their key>
Their areas appear under /v1/circuits/<name>/… , beside yours, never in it.
```

An area crosses by somebody setting `export: yes` on it, through the review queue, and by nothing
else; the line a reader sees is that area's own `use_when`. A kind marked `export: no` in
`vocab.yaml` never leaves, whatever an area says. Nothing is copied — every read through a circuit is
a read of the far end, recorded there in `data/access`.

The key is `KNOWLEDGE_CIRCUIT_TOKEN` in `.env` (`install.sh` makes one). It is an **enrolment key**
that buys a six-hour session and opens nothing else; it shortens how long a leak is worth something,
and it does not prove who is at the far end.

Standing links between backbones, the exchange they met at, its operator screen, and encrypted
export bundles were retired on 2026-10-08: a circuit is the one way left.

**[docs/CIRCUIT.md](docs/CIRCUIT.md)**.

## Layout

```
ontology/     the ontology API — python + pyyaml + git. Knows nothing about any domain
web/          the map and a proxy — one FastAPI file. Knows nothing about any domain
mcp/          the MCP server, so any MCP-capable agent can read the ontology
static/       the map screen
seed/         an empty ontology, copied into data/repo on first boot
examples/     one worked ontology
check/        every check. docs/CHECKS.md
docs/         everything below

data/repo     ← your ontology. A git repository, and the only thing to back up
data/*        overlays, walks, harness, access — all local.
              docs/DATA-REPO.md
```

## A hand-edited repository

The data repository is yours to edit in an editor. One file in it is generated: `regions.json`,
hop 0's table, derived from the areas' `.md` files and committed beside them.
Edit an area's file by hand — its `use_when`, its `export` — and that table is stale until it is
regenerated.

Three things make that safe. The validator says so, naming the area and the field. Readers are
served what the files say meanwhile, not the stale table — hop 0 and the export surface read the
files' truth. And the server regenerates and commits the table at startup when the tree is clean;
any write through the API does the same, and so does `./ontology/tidy.py data/repo --fix`. With
uncommitted changes in the tree nothing is committed on your behalf: commit or discard, then
restart. `/healthz` carries `valid` and the first reasons it is not.

## Everything else

| | |
|---|---|
| [ROUTING.html](docs/ROUTING.html) | the whole structure, in a browser |
| [INSTALL.md](docs/INSTALL.md) | installing by hand, what to do when it does not come up, the first two things to write |
| [CIRCUIT.md](docs/CIRCUIT.md) | reading another backbone, what crosses, six-hour sessions |
| [AGE.md](docs/AGE.md) | the two times on a routing row, and what they deliberately do not say |
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
