# The checks

```sh
./check/all.sh              # every suite but install-check
./check/all.sh --quick      # skip concurrency and the slow block that starts its own services
./check/all.sh --only walk  # the ones whose name contains "walk"
```

There is no test framework here. Each check is one file you can read top to bottom and run on its
own, and most of them build the world they need — a throwaway ontology, sometimes a second backbone
to open a circuit to — rather than asking you to have one. That is deliberate: a check that needs a particular
install is a check nobody runs on a different one.

`all.sh` is not a framework either. It knows one thing the individual files cannot: **where** each
of them can run — this machine, the ontology container, the web container — which is the part that
is not obvious and was carried around in somebody's head until 2026-09-14. A suite it cannot run
fails the run and says why, rather than being quietly skipped.

The suites that use an install — `smoke.sh`, `mcp-check.py`, `circuit-check.py`, and in a full run
`llm-paths.sh` — go to `$BASE`, which is this checkout's install unless you set it: the last
`WEB_PORT` in `.env`, read by `check/base.sh` (8080 only when `.env` names none). Set it to check
another install (`BASE=http://127.0.0.1:9000 ./check/all.sh`). The container suites go to this
checkout's own compose project. Until 2026-11-02 the default was 8080 whatever `.env` said, so from a
checkout on another port those suites tested — and `llm-paths.sh` wrote into — whatever answered there.

Two rules the whole set is written against, and they are worth knowing before adding one:

- **Reproduce and measure, never assert.** A check exists because a failure was produced first. The
  comments name the failure, and usually the date.
- **Every fix leaves a check that fails without it.** Reverting the fix must make the new assertion
  fail — not "would probably fail". Several comments here say what was seen when that was tried.

## Before a release

```sh
./check/install-check.sh          # a few minutes; it builds
./check/install-check.sh --keep   # leave it running to poke at
INSTALL_CHECK_PORT=8490 INSTALL_CHECK_PROJECT=ic2 INSTALL_CHECK_TAG=ic2 ./check/install-check.sh   # beside another run
```

Clones the **committed** tree into a temporary directory and installs it there, then walks the export
decision as another backbone sees it — a circuit from a second MCP server, at the install's web
address: advertise, reword, withdraw. Its own directory, its own compose project, its own port and its
own image tags, so nothing of yours is touched.

Run it after a change large enough that you would not want to be the first person to find out. The
ordinary checks build their own world; this one is about the world a person arrives in, and that is a
different set of mistakes. Six real defects came out of its first two runs, and four could not have
come from any other check: a key written twice in `.env` that the installer and docker read
differently, a status code believed over a body, an `IndexError` where a sentence belonged, and a
`mkdir` that was in `install.sh` and missing from the one command you copy out of a guide.

## Everything there is

The middle column is how many assertions each one made on 2026-11-02, for the checks that start what
they need and so could be counted on any machine; a count that has gone **down** since is worth
looking at. The ones that run against an install, and the ones whose number is the size of the tree
rather than a count of assertions, have a dash: the number to trust is the one the check itself
prints. Nothing checks this table against the checks.

### The install, from outside

These take the install's address as their first argument, and default to this checkout's install (`WEB_PORT` in `.env`).

| | | |
|---|---|---|
| `check/smoke.sh` | — | Does this install work — API, an agent's walk, the map screen. What `install.sh` finishes with. It also runs `mcp-check.py`, `screen-check.mjs` and the static checks |
| `check/install-check.sh` + `install-walk.py` | — | A clean clone, installed in its own directory and walked. Above. Not run by `all.sh` |
| `check/mcp-check.py` | — | The MCP protocol over stdio, and an agent's whole walk from the area list to a document |
| `check/llm-paths.sh` | — | Creating a node with an LLM and without one. **Writes into the install** — removes what it wrote, asserts the map's content is as it found it, and names the commits it added to the history — and tests the one mode that install is in — the other needs an install configured the other way |
| `check/circuit-check.py` | — | Another backbone's circuit into this install, through the web port: what it may mint, what it may read, and an agent's walk through it — [CIRCUIT.md](CIRCUIT.md). On an install with no area set to export, the walk into one is reported as not run, in its count too (`0 failed of 7 (1 not run …)`) |
| `check/session-check.py` | — | The six-hour session tokens. Mostly about what must **not** work: an enrolment key that still reads, or a session that can mint another. Runs in the ontology container |
| `check/llm-probe.py` | — | Not a check: asks a real provider what a real key can use. Needs both, so nothing runs it for you |

### The data model

| | | |
|---|---|---|
| `ontology/check.py` | 131 | The invariants, each stated as an **absence** — the body that must still be there, the old scope spelling that must not be filed. It is not in `check/`, and it is the one people forget |
| `check/scenarios.py` | 56 | The routing table over a whole lifetime: areas created, advertised, emptied, deleted, created again. [SCENARIOS.md](SCENARIOS.md) is the contract |
| `check/overlay-check.py` | 17 | Overlays end to end, through the MCP server, the way an agent uses them |
| `check/romanize-check.py` | 38 | A name in another script, as an address — and the names that must not become one |
| `check/concurrency-check.py` | 5 | Reads happening while writes happen, through HTTP, on one server. Probabilistic by nature — the deterministic half of the same question is in `ontology/check.py` |
| `check/age-check.py` | 14 | The two times on a routing row, built from a repository it commits into itself. Mostly about *not known* staying not known |
| `check/tidy-check.py` | 11 | What `rm -rf regions/<area>` leaves, and that tidy mends exactly that. Half of it is that a healthy repository is left alone |

### Agents writing, invariants on a live service, and what goes wrong

Each starts the service itself on a throwaway repository.

| | | |
|---|---|---|
| `check/write-paths.sh` | 63 | Every write path, against a throwaway ontology |
| `check/place-check.py` | 21 | Placing a document the way an agent does, through the MCP — [CHANGE.md](CHANGE.md) |
| `check/change-check.py` | 42 | Change sets: one commit or none, the cascade of lines over a change, the queue for hop-0 sentences |
| `check/b2c-check.py` | 17 | What a non-expert meets on the screen's own flows: names in any script, refusals that say why, the review queue |
| `check/robust-check.py` | 20 | What an operator meets: a write killed mid-way, SIGTERM, a hand edit, a 200-row table on a large map, a file that does not parse, an area deleted by hand, `reset.sh`, the agent's secret, the area-switch note |
| `check/drift-check.py` | 17 | A hand-edited repository served while `regions.json` is stale |
| `check/walk-check.py` | 17 | Invariant 1 at the agent's door: every walk starts at hop 0 |
| `check/same-answer-check.py` | 2 | Invariant 4: every reader of one fact gets the same answer — each of the two a sweep of every fact × every path, which prints how many cells it read |
| `check/transact-check.py` | 75 | Invariants 5 and 7: a routing change is a commit, and nothing is reported done that did not happen |
| `check/follow-check.py` | 15 | Invariant 3: what a reader holds follows its source |
| `check/hyphen-check.py` | 10 | An area whose directory has a hyphen, on every path that used to spell it two ways |
| `check/footprint-check.py` | 23 | Invariant 11: every walk recorded — the store, the service, and an agent through the MCP |
| `check/export-check.py` | 20 | The export surface: a denied kind and a draft refused at every address it answers, and a 401 that names the configured session lifetime — [CIRCUIT.md](CIRCUIT.md) |
| `check/mcp-edge-check.py` | 60 | The MCP server against what a client, a `.env` and a far end that is not RouteMind can hand it — a batch on the stream, a BOM, an SSH banner at `--api`, a circuit to an HTML page |
| `check/footprint-screen-check.py` | 52 | The footprint on the screen — the real `static/knowledge.js`, a stub DOM, against a fresh service it starts. Not `footprint-screen.mjs` against a live install: that one's map holds every walk of the last six hours |
| `check/circuit-client-check.py` | 7 | The circuit's client against far ends that misbehave |

### The screen, and the shape of the tree

| | | |
|---|---|---|
| `check/screen-check.mjs` | — | The map, drawn against a fake DOM. No browser. Run by `smoke.sh`, against the install |
| `check/css-check.mjs` | — | Every class the screen puts on an element, against every class the stylesheets define |
| `check/i18n-check.mjs` | — | The four dictionaries, against each other and against the screen |
| `check/auth-check.py` | 34 | The door on the screen's side — [AUTH.md](AUTH.md) |
| `check/env-check.py` | 4 | Every setting `.env.example` documents reaches a container, every `mkdir` recipe covers every bind mount, and the installer reads `.env` the way docker does |
| `check/eol-check.py` | — | What a checkout on another operating system has to survive — line endings and exec bits, over every tracked file |
| `check/secrets-check.py` | — | Invariant 10: nothing secret-shaped in a tracked file. Run before every push |
| `check/mcp-routes-check.py` | — | Every path the MCP server calls exists on the web app |
| `check/all.sh` | — | Runs all of the above except `install-check.sh` and `llm-probe.py`, each where it can run |

## Where each one can run

Neither environment satisfies all of them, and the split is not arbitrary.

**On the host.** `smoke.sh`, `mcp-check.py` and `llm-paths.sh` need `curl` and to see the install's
web port, which the containers cannot. `write-paths.sh` and every check in the third table start the
service themselves. Everything static — `css-check.mjs`, `i18n-check.mjs`, `screen-check.mjs`,
`env-check.py`, `eol-check.py` — runs anywhere.

**In the ontology container**, or on any host python with pyyaml: the checks that import the
service. `all.sh` runs `scenarios.py` in the container, because the image has pyyaml and a host
often does not; with pyyaml it passes on the host just the same (`python3 check/scenarios.py`):

```sh
docker cp check $(docker compose ps -q ontology):/tmp/check
docker cp mcp   $(docker compose ps -q ontology):/tmp/mcp
docker compose exec ontology python3 /tmp/check/scenarios.py
# session-check needs the circuit key it tests — the one in .env:
docker compose exec -e ROUTEMIND_TOKEN="$(sed -n 's/^KNOWLEDGE_CIRCUIT_TOKEN=//p' .env | tail -1)" \
    -e ROUTEMIND_API=http://127.0.0.1:8100 ontology python3 /tmp/check/session-check.py
```

`rm -rf /tmp/check` in the container **first** if you have copied before: `docker cp` copies *into*
an existing directory, and you end up running a stale file and disbelieving the result.

**In the web container**, for `auth-check.py`, which needs fastapi and uvicorn — `all.sh` runs it
there; any python with those two runs it as well. Same shape, `web` instead of `ontology`. `circuit-check.py` runs on the host against the install and needs the circuit
key, from `ROUTEMIND_TOKEN` or `KNOWLEDGE_CIRCUIT_TOKEN` in `.env`, and fails rather than skipping
without one — a check whose subject is that an export stays narrow is the last one that should
quietly not run.

Anything on the host that imports the service needs pyyaml on that python. If `pip` is not available,
the pure-python copy can be lifted out of the image:

```sh
docker cp $(docker compose ps -q ontology):/usr/local/lib/python3.12/site-packages/yaml ./pylib/yaml
rm -f ./pylib/yaml/_yaml*.so        # the Linux C extension; PyYAML falls back to pure python
PYTHONPATH=./pylib python3 check/follow-check.py
```

## Reading a result

Every check prints one line per assertion, and most end with a count; a few end with a sentence
instead (`all pass`, `all write paths ok`), and for those the exit code is the verdict. Two things a
count line can say:

```
0 failed of 62
0 failed of the 29 that ran — but THE RUN STOPPED EARLY and the rest never ran…
```

The second is not a pass. The summary is printed by an `atexit` handler, so it prints whatever
crashed the script — and until 2026-09-13 it said `0 failed of 29` in that case, which read exactly
like a clean run. The exit code was always 1, so nothing automated was fooled; the person reading the
terminal was.

---

Back to [the README](../README.md).
