# RouteMind

**A routing table for an agent, written and kept by people.** You split a body of documents into
areas. Each area describes, in one sentence, when someone should come to it. An agent reads that list
of sentences first, chooses, and walks down a tree of short lines to the document. The map shows you
the tree, and one click shows you the exact text the agent is given at each step.

The domain is not in the code. The areas, the lines and the documents are data, kept in your own git
repository. Every change is a commit.

![The RouteMind map: a backbone carrying five areas, two of them opened to show the nodes they hold,
with the routing table each one hands an agent one button away.](docs/img/map.jpg)

---

## The bet

RouteMind does not replace retrieval. It makes one bet:

> **Where documents resemble each other — revisions of one rule, rows that differ by a code, policies
> that differ by one condition — a routing table that people write and maintain finds the right
> document more reliably than similarity search. The price is several times the cost per question,
> plus the labour of keeping the table true.**

The bet is lost if any of these turns out to be true:

- **Retrieval is already good enough** on real documents. Then the walk costs more and buys nothing.
- **Keeping the map costs more than the wrong answers it prevents.** The map is human work, every
  week.
- **A large map loses the agent.** Measured once, small: 5 areas against 30, with confusable
  neighbours, did not change which area was chosen ([eval/scale/](eval/scale/)). Dozens of real areas
  or tens of thousands of documents have not been tried.

None of these has been settled on real data. Everything measured so far is listed below, together
with what it does not show.

## How it works

![Each area summarizes itself into one advertised route; the backbone holds one row per area, and no
more. An agent reads that list at hop 0, picks every area the question belongs to, and only then reads
documents.](docs/img/backbone-as-advertisement.svg)

The idea is borrowed from routing on a network. An area advertises **when it is relevant**, not
everything it holds. That keeps the first list the same size whether the areas hold 80 documents or
8,000.

```
   BACK-BONE ─ the whole map. Hop 0: one row per area, nothing else,
       │       and the only place "it is not here" may be said
       │
       ├── AS  expense    "what to do with a receipt · whether the corporate card
       │        │          may be used here · how much a business trip pays"
       │        ├── AS  corp-card   ← an area holds areas: the same thing one level
       │        │    └── card-limit   down, describing itself the same way
       │        └── AS  evidence
       ├── AS  approval   "whom to put in the approval chain · …"
       └── AS  payroll    "what this payslip line means · …"
```

- **`use_when` is the only text the agent reads before it chooses an area.** An area with a title and
  no reason is an area nobody picks.
- **Each table describes only its own area.** An area's table says what that area holds, never what
  the whole map lacks. Only someone who has read hop 0 may conclude that something is not here.
- **Every walk starts at hop 0, and every step records why it was taken.** The MCP server enforces
  this. The map replays any walk from the last six hours.
- **Writing is a set of decisions.** When an agent files a document, it may create a holder and move
  siblings under it in the same change. Every line whose table changes must be either kept or
  rewritten, or nothing is written. ([docs/CHANGE.md](docs/CHANGE.md))

Two containers and no database. `ontology` is the API and the only process that touches your git
repository. `web` serves the map and acts as a proxy. `mcp/knowledge_mcp.py` is the agent's door: a
single stdlib-only file with four tools — read a table, read a document, place a document, read
another RouteMind.

## What was measured — and what it does not show

**The setting.** 700 questions over one frozen corpus of 1,126 documents, in four arms, with one fresh
agent per question:

| | plain RAG | + reranker | RouteMind walk |
|---|---|---|---|
| question in the documents' own codes | 0.991 | 1.000 | 1.000 |
| question in a person's words | 0.028 | 0.069 | 1.000 |
| a rule two revisions back | 0.133 | 0.200 | 1.000 |
| overall | 0.516 | 0.541 | 0.999 |

**Read it as a stress test, not a benchmark.**

- **The corpus is synthetic and was built so that retrieval fails.** Each answer has many near-identical
  rivals: other revisions, neighbouring codes. [eval/COLLAPSE.md](eval/COLLAPSE.md) describes how
  that was constructed. On questions phrased in the documents' own words, retrieval scores 0.99 and
  the walk adds nothing.
- **One domain, one map, one author side.** The corpus is a fictional back office. The questions are
  templated or written by a model. The map's sentences were written by people who knew the corpus. No
  real organisation's documents have been measured. The question of who labels the ground truth is
  still open ([eval/PREREGISTRATION.md](eval/PREREGISTRATION.md)).
- **It costs far more.** A walk takes 6.7 tool calls, 23–111 seconds and $0.12–$0.28 per question,
  against one sub-second embedding call. That is 20–100× the cost. For 320 of the 700 questions,
  retrieval already found the answer first time.
- **The map is a single point of failure.** The one miss in 700 came from a wrong sentence in the map,
  not a wrong document, and the agent followed it. An agent that trusts the map inherits the map's
  errors, and nothing flags them.

**Flat or folded** ([eval/depth/](eval/depth/), 2026-10-09/10). The same 73 questions on two trees:
area tables of 15–23 rows behind holders, against the same documents with every holder removed
(61–244 rows per area). With a Sonnet-class walker both trees scored **65/73**; the flat tree cost
**2.4×** the input. With a Haiku-class walker the flat tree scored *higher* — 66 vs 61 — because every
holder is one more decision a weak model can get wrong. Folding buys tokens, not accuracy, and costs
a weak model accuracy.

**Behaviour** ([eval/philosophy/](eval/philosophy/), 2026-10-10). Twelve questions through the real
MCP door, Sonnet and Haiku: every walk started at hop 0 with a reason on every step; every question
with no answer in the documents was answered "not here", with no invented rule; deliberately false
lines were answered around by reading the document. But the agents did not *report* the false lines
until one instruction asked them to (1/4 → 4/4), nor a false hop-0 sentence until the server pointed out
that the walk had switched areas (0/2 → 2/2).
Twelve questions, one run each — read it as "did not fail", not as a rate.

Everything is in the repository: the corpus generator (`bench/`), the gold sets (`eval/gold/`), and
every run including the failures (`eval/runs/`). Re-running needs an API key —
[bench/README.md](bench/README.md).

## When not to use it

- **Your documents do not resemble each other.** If retrieval already finds the right page, a walk
  only adds cost and latency.
- **The cost of each question matters more than its accuracy.** A walk takes several model calls and
  tens of seconds.
- **Nobody will own the map.** A table that no one maintains goes stale. A stale table is worse than
  none, because the agent follows it confidently.
- **You need it hosted, multi-tenant or hardened today.** See below.

## Known limits

| | |
|---|---|
| **Evidence** | one synthetic corpus, one domain, model-written or templated questions; no real organisation's data |
| **Scale** | routing measured at 5 and 30 areas (30 with thin distractor areas); about 1,100 documents. Nothing larger has been tried |
| **Models** | Sonnet- and Opus-class on the stress test; Haiku-class only on the depth and behaviour runs, where folded tables cost it accuracy |
| **Staleness** | no mechanism decides which version is current. That is said by a person, in a line. Ages from git help someone ask; they do not decide ([docs/AGE.md](docs/AGE.md)) |
| **Maintenance** | change sets keep the lines over a change in step, but they are days old and unproven in real use. The map has no editor for a multi-step change |
| **Absence** | "not here" is only as good as hop 0's sentences. A missing sentence and a missing document look the same to the agent |
| **Operations** | one maintainer; single node; one git repository; basic auth; the default install listens on the network ([docs/AUTH.md](docs/AUTH.md)) |
| **Overlays** | the working set for multi-area questions is off by default ([docs/OVERLAY.md](docs/OVERLAY.md)) |

## Where it stands

**A research prototype with one maintainer and no outside team known to be running it.**

| measured | not measured | next |
|---|---|---|
| the collapse stress test above | any real organisation's documents | a corpus someone else wrote, with questions someone else wrote |
| cost per walk | how much it costs to maintain the map over months | a maintenance log from a real install |
| flat vs folded, both a strong and a weak walker | scale: dozens of areas, 10k+ documents | a larger synthetic map |
| invariants: 12, each with a check ([docs/INVARIANTS.md](docs/INVARIANTS.md)) | a misroute into an area that holds a plausible wrong answer | a map whose facts each live once |

Worth trying if your team keeps answering from the wrong revision, or retrieval keeps returning the
neighbouring row. Reports of where it fails are the most useful thing you can send:
[GitHub Issues](https://github.com/CSP911/routemind/issues).

## Quickstart

Docker with `docker compose`. The containers include Python and git.

```sh
git clone https://github.com/CSP911/routemind.git routemind && cd routemind
./install.sh --port 9000
```

→ **http://localhost:9000**. On a first install it asks whether to start from the example back office
([`examples/back-office`](examples/): five areas, 79 documents) — say yes unless you have data of your
own ready. You can run it again safely: an existing `.env` is kept. An optional LLM adds a **✨ Suggest**
button that drafts a line for you to edit; nothing else depends on it.
[docs/INSTALL.md](docs/INSTALL.md) · already running one: [docs/UPGRADE.md](docs/UPGRADE.md).

**An agent.** Claude Code finds the server in `.mcp.json`, which reads the port from `.env`:

```sh
claude          # in the same directory; approve the "knowledge" server once, then /mcp lists four tools
```

For any other MCP client, run the same server — it finds the install the same way, or take `--api`:

```sh
python3 mcp/knowledge_mcp.py      # or: --api http://localhost:9000/api/knowledge
```

The area list reaches the agent in the server's instructions, so you do not have to name RouteMind in
the question. [docs/AGENTS.md](docs/AGENTS.md).

## More

| | |
|---|---|
| [ROUTING.html](docs/ROUTING.html) | the whole structure, in a browser |
| [INVARIANTS.md](docs/INVARIANTS.md) | the twelve rules that are true on every path, and the check behind each |
| [CHANGE.md](docs/CHANGE.md) | change sets: several decisions, one commit, the lines above them decided |
| [FOOTPRINT.md](docs/FOOTPRINT.md) | watching and replaying a walk |
| [AGE.md](docs/AGE.md) | the two ages on each routing row |
| [CIRCUIT.md](docs/CIRCUIT.md) | reading another RouteMind for one session |
| [DATA-REPO.md](docs/DATA-REPO.md) | your map as a git repository, and editing it by hand |
| [AGENTS.md](docs/AGENTS.md) · [LLM.md](docs/LLM.md) · [AUTH.md](docs/AUTH.md) | agents, the optional LLM, who may write |
| [CHECKS.md](docs/CHECKS.md) · [PLATFORMS.md](docs/PLATFORMS.md) · [I18N.md](docs/I18N.md) | checks, platforms, languages |
| [TODO.md](docs/TODO.md) | known gaps |
| [eval/](eval/) | the study, pre-registered before it ran |

Layout: `ontology/` the API · `web/` the map and proxy · `mcp/` the agent's door · `static/` the
screen · `check/` every check · `data/repo` your map, the only thing to back up.

## Contact

**qct8377@gmail.com** · [linkedin.com/in/cspark911](https://www.linkedin.com/in/cspark911/) ·
[GitHub Issues](https://github.com/CSP911/routemind/issues)

## License

MIT — see [LICENSE](LICENSE).
