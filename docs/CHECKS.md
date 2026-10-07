# The checks

```sh
./check/all.sh              # everything, ~22 suites
./check/all.sh --quick      # skip the slow ones
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

Two rules the whole set is written against, and they are worth knowing before adding one:

- **Reproduce and measure, never assert.** A check exists because a failure was produced first. The
  comments name the failure, and usually the date.
- **Every fix leaves a check that fails without it.** Reverting the fix must make the new assertion
  fail — not "would probably fail". Several comments here say what was seen when that was tried.

## Before a release

```sh
./check/install-check.sh          # a few minutes; it builds
./check/install-check.sh --keep   # leave it running to poke at
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

Counts are what each one asserted on 2026-09-14. A count that has gone **down** is worth looking at —
and this table is not checked against anything, so if you are reading it a long time from now, the
number to trust is the one the check itself prints.

### The install, from outside

| | | |
|---|---|---|
| `check/smoke.sh` | 6 + the static checks it runs | Does this install work — API, an agent's walk, the map screen. What `install.sh` finishes with |
| `check/install-check.sh` + `install-walk.py` | 24 | A clean clone, installed in its own directory and walked. Above |
| `check/mcp-check.py` | 19 | The MCP protocol over stdio, and an agent's whole walk from the area list to a document |
| `check/write-paths.sh` | 66 | Every write path, against a throwaway ontology |
| `check/llm-paths.sh` | 12 | Both LLM modes, so a change to one does not quietly break the other |
| `check/circuit-check.py` | 8 | Another backbone's circuit into this install, through the web port: what it may mint, what it may read, and an agent's walk through it — [CIRCUIT.md](CIRCUIT.md) |
| `check/session-check.py` | 12 | The six-hour session tokens. Mostly about what must **not** work: an enrolment key that still reads, or a session that can mint another |
| `check/age-check.py` | 13 | The two times on a routing row, built from a repository it commits into itself. Mostly about *not known* staying not known |
| `check/tidy-check.py` | 11 | What `rm -rf regions/<area>` leaves, and that tidy mends exactly that. Half of it is that a healthy repository is left alone |
| `check/llm-probe.py` | — | Not a check: asks a real provider what a real key can use. Needs both, so nothing runs it for you |

### The data model

| | | |
|---|---|---|
| `ontology/check.py` | 106 | The invariants, each stated as an **absence** — the body that must still be there, the old scope spelling that must not be filed. It is not in `check/`, and it is the one people forget |
| `check/scenarios.py` | 56 | The routing table over a whole lifetime: areas created, advertised, emptied, deleted, created again. [SCENARIOS.md](SCENARIOS.md) is the contract |
| `check/overlay-check.py` | 17 | Overlays end to end, through the MCP server, the way an agent uses them |
| `check/romanize-check.py` | 38 | A name in another script, as an address — and the names that must not become one |
| `check/concurrency-check.py` | 5 | Reads happening while writes happen, through HTTP, on one server. Probabilistic by nature — the deterministic half of the same question is in `ontology/check.py` |

### The screen, and the shape of the tree

| | | |
|---|---|---|
| `check/screen-check.mjs` | — | The map, drawn against a fake DOM. No browser |
| `check/css-check.mjs` | 147 classes | Every class the screen puts on an element, against every class the stylesheets define |
| `check/i18n-check.mjs` | 382 keys × 4 | The dictionaries, against each other and against the screen |
| `check/auth-check.py` | 32 | The door on the screen's side — [AUTH.md](AUTH.md) |
| `check/env-check.py` | 3 | Every setting `.env.example` documents reaches a container, every `mkdir` recipe covers every bind mount, and the installer reads `.env` the way docker does |
| `check/eol-check.py` | 190 files | What a checkout on another operating system has to survive — line endings and exec bits |
| `check/all.sh` | — | Runs all of the above, each where it can run |

## Where each one can run

Neither environment satisfies all of them, and the split is not arbitrary.

**On the host.** `smoke.sh` and `mcp-check.py` need `curl` and to see the web proxy at :8080, which
the containers cannot. `write-paths.sh` and `llm-paths.sh` start the service themselves. Everything
static — `css-check.mjs`, `i18n-check.mjs`, `screen-check.mjs`, `env-check.py`, `eol-check.py` — runs
anywhere.

**In the ontology container**, because they import the service and need pyyaml, which the image has
and a host usually does not:

```sh
docker cp check $(docker compose ps -q ontology):/tmp/check
docker cp mcp   $(docker compose ps -q ontology):/tmp/mcp
docker compose exec ontology python3 /tmp/check/scenarios.py
```

`rm -rf /tmp/check` in the container **first** if you have copied before: `docker cp` copies *into*
an existing directory, and you end up running a stale file and disbelieving the result.

**In the web container**, for `auth-check.py`, which needs fastapi and uvicorn. Same shape, `web`
instead of `ontology`. `circuit-check.py` runs on the host against the install and needs the circuit
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

Every check prints one line per assertion and a count at the end. Two things that line can say:

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
