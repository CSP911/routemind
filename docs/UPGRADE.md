# Installing, and applying an update to an install you already have

Two routes. A new install is one command. An install that is already running — with your own
areas and documents in `data/repo` — takes three steps (1–3 below; 4 is a list of what went away),
and the rest of this page is what each one does, what it changes on its own, and how to see that it
worked.

Nothing on this page touches your documents. `data/` is bind-mounted into the containers and stays
on disk across a rebuild; the only file an update may rewrite there is `data/repo/regions.json`,
which is generated, and it does so in a commit that says why.

## 2026-11-02 (later) — what was checked, and what was read, are on the record

Nothing to do beyond the usual `git pull && ./install.sh`. What changes on its own:

- **"Still right" is recorded.** On the strip of lines that may be stale, it now asks why the line
  still holds and commits that as a keep — an empty commit carrying `Keep: <id>.<field> — <why>`. It
  used to dismiss the row in your browser and nothing else. When a line was last checked:
  `git -C data/repo log --grep 'Keep: <id>.<field>'`. Refused if the line changed since the strip showed it.
- **A walk step says which version it read.** Each table and document an agent reads records the
  commit it was served at; a document also its file and a hash of exactly what the agent was given.
  Reasons on the map shows the commit as `@1a2b3c4`; `git show <commit>:<file>` is the text it read.
  An MCP server from before this keeps working, without the record — update the checkout it runs from.

## 2026-11-02 — a full audit: every path a new user, an agent and a second install take

Nothing to do beyond the usual `git pull && ./install.sh`. What changes on its own:

- **Writes that could reach outside an area are refused.** An area name or a document file name is
  one plain directory entry under `regions/` or it is a 400 — before, `DELETE /v1/regions/..` on the
  ontology's own port removed the whole data repository, `.git` included, and a create could commit a
  file at the repository root.
- **The export surface answers two addresses per node,** `nodes/<id>` and `nodes/<id>/body`. A child
  is read at its own address; `nodes/<parent>/files/<child>.md` is a 404 there now, because it served
  drafts and kinds marked `export: no`.
- **A hand edit made while a write runs is never swept into it.** A write commits only the files it
  wrote; if anything else in the tree changed meanwhile it is refused with `409 tree_dirty` and you
  save again. A rollback restores only the write's own files, so a hand edit survives it. What
  Finder or Explorer leaves in a folder (`.DS_Store`, `._*`, `Thumbs.db`, `desktop.ini`) does not
  count — opening `data/repo` in Finder used to stop the map saving.
- **Names YAML would misread** (`on`, `no`, `017`, a date) are written quoted, and a hand-written date
  is read as its text. Existing files read as before.
- **The review queue** refuses a proposal identical to a pending one (`duplicate_pending`), refuses a
  change set its own dry run says cannot apply, and decides one proposal at a time.
- **The web port:** a document over 1 MB is refused with 413 (`KNOWLEDGE_MAX_DOCUMENT_BYTES` to change
  it); in proxy mode the trusted proxy is the socket's address, never `X-Forwarded-For`; an identity over
  64 characters is refused for writes instead of cut; "Copy for an agent" prints addresses that answer (they were
  404); `HEAD` works wherever `GET` does.
- **The agent:** one malformed line, a non-UTF-8 byte or a circuit to something that is not RouteMind no
  longer ends the session; `knowledge_read` reads document bodies only; a walk expires ten minutes after
  its last step, not after hop 0; a `.env` saved with a BOM or in another encoding is read, and a
  `WEB_PORT` that cannot be read is named instead of falling back to 8080.
- **The checks** (`check/smoke.sh`, `mcp-check.py`, `all.sh` …) default to this checkout's `WEB_PORT`,
  not 8080, so they test the install you are in and never another one on the machine.
- **Many clients at once:** the service listens with a backlog of 128, not 5 — on Linux, a map, a
  few agents and a health check together could have a write reset mid-connection.
- **install.sh** says plainly when Docker, `docker compose` or the daemon is missing, accepts
  `--port=N`, and a re-run no longer rebuilds the service (a `.dockerignore` keeps `__pycache__` out of
  the image).

## 2026-10-10 (later) — a second full pass: recovery, starting over, the agent's secret

Nothing to do beyond the usual `git pull && ./install.sh`. What changes on its own:

- **A file that does not parse no longer takes the service down.** It is left out, everything else is
  served, and `/healthz`, **Show what fails** and `validate` name it with its line. A broken
  `regions.json` is rewritten at start. A service that cannot validate at start still starts.
- **A write interrupted by a kill or a restart is rolled back at the next start** (a marker under
  `.git` says it was the service's own), and stopping the container waits for a write in progress.
- **Starting over:** `./ontology/reset.sh --empty | --example` — one commit, the old map tagged first
  ([DATA-REPO.md](DATA-REPO.md)). Restoring a backup is *stop, copy, start*; a directory swapped under a
  running service now reads as not writable instead of writable.
- **Install:** a new install names its containers and images after its directory *and* path, so a
  second clone with the same directory name no longer replaces the first; and install.sh refuses to
  take over another checkout's containers. It asks for the port on a first install, refuses an
  invalid or occupied one before building, and keeps the checks' ninety lines in
  `data/install-checks.log`. An existing install keeps its names.
- **Agents in token mode** send `KNOWLEDGE_TOKEN` from `.env`, so they can place, not only read.
  The screen asks for the token when a write is refused for want of it.
- **The review queue** also holds change sets that create an area or reword a hop-0 sentence, with
  `Proposed-by:` in the commit when accepted. Every refusal on the screen has a named reason in four
  languages.
- **Files the service writes** keep their mode, or get 0644, instead of 0600.
- **An empty map** shows a "Create the first area" button; the starter vocabulary's default kind is
  `document`, not `system`.
- **Large maps:** a 200-row table on a few thousand entities went from 20 s to under 0.2 s.
- **Closed doors and re-runs:** `./install.sh` re-run on an install in token mode (or with reads
  guarded) no longer fails its own checks — they present `KNOWLEDGE_TOKEN` from `.env`.
- **Names:** an area can be named in Hangul or kana on the screen; it gets a romanised address and keeps
  the name as its title, as documents already did.
- **Agents:** a walk ends as *ended* when the client stops the MCP server, instead of staying
  *walking*; an agent now says which line was wrong when a line and its document disagree, and looks
  at the area list again when what it found answers a narrower question ([eval/philosophy](../eval/philosophy/)).
- **On a phone** the map no longer scrolls the page sideways and opens on the Back-Bone.
- **New doc:** [WRITING.md](WRITING.md) — five rules for sentences and pages an agent stays right on.

## 2026-10-10 — install, circuits and the agent, after a full pass as a new and an updating user

- **`.mcp.json` names no port any more.** The MCP server reads `WEB_PORT` from `.env` itself, so
  `install.sh` no longer rewrites a tracked file. **If your `.mcp.json` shows as modified** (`git status`
  says ` M .mcp.json` — any install on a port other than 8080), run `git checkout -- .mcp.json` before
  `git pull`, or the pull stops on it.
- **`install.sh`** asks once whether to start from the example back office (first install only),
  gives each checkout its own image tag (`IMAGE_TAG` in `.env` — and since the later pass its own
  container names too), runs compose with
  `--remove-orphans`, asks about an LLM only once, and ends with what to do next.
- **Export says what it shares:** the card is called **Export**, and saying yes lets any circuit
  holding your key read the area's sentence *and every document in it* — the old wording said "the
  line above". Accepting an export or a withdrawal is now named in its commit message.
- **Circuits:** a name is made from any address (`127.0.0.1:9330` works), redirects are refused, the
  far end's refusals say what to fix, hop 0 lists the circuits open in the session,
  `ONTOLOGY_PEER_SESSION_TTL` reaches the container, and the access log records where a read came
  from, which session it carried, and every failed key.
- **The agent:** hop 0 takes a `question`, recorded on the walk; `knowledge_place` opens a walk and
  takes an optional `kind`; a queued change set ends its placement (do not file it again another
  way), and accepting a queued set after the tree moved says it is stale.
- **The map:** a document can be named in Hangul or kana (`출장비 기준` gets the address
  `chuljangbi-gijun` and keeps its name), a document added to an area shows at once, and the strip of
  stale lines drops a line once it has been rewritten. `/healthz` answers on the web port.

## 2026-10-09 — `knowledge_place` writes a change set

`here` no longer puts a page in and leaves the line above untouched. It is one commit of several
decisions — the page, a holder if it needs one, siblings moved under it — and the line over every
table it changes has to be kept or reworded in the same call, or it writes nothing and prints the
lines (docs/CHANGE.md). An agent that calls `here` the old way gets that refusal and the way to answer
it; nothing to configure. Every write's answer now also carries `impacted`, the lines a write may
have left stale, and the map shows them in a strip. `use_when` in an entity's frontmatter is written
quoted from now on; files written earlier read as before.

## A new install

```sh
git clone https://github.com/CSP911/routemind.git routemind && cd routemind
./install.sh --port 9000
```

`install.sh` makes every directory under `data/`, writes `.env`, asks whether to start from the
example back office, builds and starts the containers, and ends with what to do next. Details and
troubleshooting: [INSTALL.md](INSTALL.md).

## Applying an update

### 1. Commit or set aside anything you changed by hand

```sh
git -C data/repo status --short
```

Empty is what you want. If you edited areas or documents in an editor, commit them in `data/repo`
first (`git -C data/repo add -A && git -C data/repo commit -m "…"`). The service refuses every write
on a dirty tree, and the startup step in 3 only repairs a clean one — it will not commit your
half-finished edit along with its own.

### 2. Get the new code

```sh
git status --short        # ` M .mcp.json` here? then: git checkout -- .mcp.json
git pull
```

An install made before 2026-10-10 on a port other than 8080 has a `.mcp.json` that `install.sh`
rewrote; the file no longer names a port, so put it back before pulling and the pull goes through.

### 3. Rebuild and restart

```sh
./install.sh --no-llm   # or plain ./install.sh if you want to add an LLM now
```

That is the whole step: it makes every directory under `data/` a newer version needs (as of
2026-10-07 that includes `data/walks`, where the footprint keeps every walk for six hours —
[FOOTPRINT.md](FOOTPRINT.md)), carries the circuit key across under its new name, builds, and restarts
with `--remove-orphans`, which takes down the `exchange` container an install made before 2026-10-08
is still running. Safe to re-run.

On start the ontology validates the repository and, if the only problem is that the generated
`regions.json` no longer matches the files, regenerates it and commits — one commit, its message
saying so. That covers two cases you may have:

- **An area whose directory name has a hyphen** (`back-office`). Before 2026-10-07 `regions.json`
  spelled it `back_office`, and a linked backbone could see the area but none of the documents in
  it. The table is rewritten with the directory name; nothing else changes.
- **An area file edited by hand** whose `use_when` or `export` was never regenerated into the table.

If the tree was not clean, nothing is committed: the log says so, and readers are still served what
the files say. Commit or discard, then restart. The repair commit is easiest to see in the repository
itself — `git -C data/repo log -3 --oneline` — since the log line goes with the container it came from.

### 4. What went away, and what you can delete

Retired on 2026-10-07, because nothing read them:

- **`data/publish`** — a checkout copied out on every write for an agent runtime that mounted it.
  Agents read the repository through the API, so the screen's "agents are reading an older tree"
  warning and its **Publish** button are gone with it. Compose no longer mounts the directory;
  `rm -rf data/publish` once you have restarted.
- **`KNOWLEDGE_AGENT_URL`** and the **▶ Start** button — remove the line from `.env` if you set it.
- **Service fragments** (`ONTOLOGY_SERVICES`, `/v1/services`) and the curator's **sleep** and
  **observations**. A proposal the sleep filed long ago, still pending in your queue, can only be
  rejected now; routing changes a person filed are accepted as before.
- **Filing a routing change under an old scope spelling** (`dr`, `peer`, `peer-line`) is refused;
  one already in the queue is still read and applied under its new name.
- **A new document with no description** is refused, with or without an LLM. The ✨ Suggest button
  drafts one for you to edit; the LLM no longer writes it on its own.
- **`edges.yaml` and `CORE.md`** are no longer read: no agent was ever shown either, and the map drew
  no edge. Yours stay in `data/repo` untouched and can be deleted. `relations` and `edge_rules` in
  `vocab.yaml` are ignored; `kinds` stay, because `export: no` on a kind still keeps that sort of
  thing from crossing a circuit. A new area needs one sentence (`use_when`), not a CORE.md row as well.
  On the first start `regions.json` is regenerated without its `description` column, in one commit.
- **`aliases`** are not checked or served. A file that has them keeps them across an edit.
- **`knowledge_place`** shows each row's line and nothing else — no column of shared words — and no
  longer queues proposals to widen the lines above. If a line no longer covers what was placed, the
  agent says so and a person changes it.
- **`./ontology/tidy.py`** now mends only `regions.json` after a hand edit; that is all a hand edit
  can leave out of step.

Retired on 2026-10-08 — **a circuit is the one way left to read another backbone** ([CIRCUIT.md](CIRCUIT.md)):

- **Standing links** (`peers.yaml`), the **exchange** and its **operator screen** (`admin/`), and
  **encrypted export bundles** (`transfer/`, and the map's old bundle-download button — the
  **Export** card on an area today is the circuit export decision, not that). Another backbone's areas no
  longer appear in your hop 0, and the map draws no domain wall. `data/repo/peers.yaml` and
  `data/exchange` are inert; delete them when you like, and the image with them:
  `docker image ls | grep exchange`, then `docker image rm` it.
- **The circuit key** is `KNOWLEDGE_CIRCUIT_TOKEN` now. `install.sh` copies your old
  `EXCHANGE_TOKEN_HOME` across, and compose reads the old name if the new one is unset — so whoever
  held your key still can read what you export. Once `KNOWLEDGE_CIRCUIT_TOKEN` is in `.env`, the
  `EXCHANGE_TOKEN_*` lines can go. A circuit's URL is your install's web address
  (`http://host:8080`); it used to need the ontology's own port, which compose never published.
- **An audience** (`export_to`) is ignored: it named peers, and every reader now presents the one key.
  An area set to export can be read by any circuit holding it. A file that has `export_to` keeps it.
  A queued `audience` or `core` proposal can only be rejected.
- **Overlays are off by default**, on the map as well as for the agent. `ONTOLOGY_OVERLAYS=/data/overlays`
  in `.env` turns the store and the map's half back on ([OVERLAY.md](OVERLAY.md)).

And two things changed rather than went: hop 0 prints every area's `use_when` whole, never cut with
`…`; and the map shows every recent walk at once, each in its own colour, with a replay that keeps the
walk's own timing at a speed you choose ([FOOTPRINT.md](FOOTPRINT.md)).

## Checking it worked

```sh
docker compose ps                                       # every container healthy
curl -s "http://localhost:$(grep '^WEB_PORT=' .env | tail -1 | cut -d= -f2)/healthz"   # "valid": true, "writable": true
curl -s "http://localhost:$(grep '^WEB_PORT=' .env | tail -1 | cut -d= -f2)/api/knowledge/walks?since=0"   # the footprint is on
```

Then open the map. Above it there is a bar — **Live · speed · Replay · Reasons**, and under the map a walk history. Ask your
agent something; the map opens as it walks.

If the map does not show the bar, or opens the area but not the path inside it, reload the page
once: a browser holding a map cached by an older version refetches it after this update.

## The agent side

The MCP server is the file `mcp/knowledge_mcp.py`, run by your client from this checkout, so
`git pull` already updated it. Restart the client (or reconnect the server) so it picks the new
file up. What an agent now does differently:

- **It starts every question at hop 0** — `knowledge_table` with no address, and the question in
  `question`, which the walk records (a walk with none shows "—" in the history). Below hop 0 a call
  before that is refused with the way back ([INVARIANTS.md](INVARIANTS.md), 1). There is no id to
  pass: the server remembers hop 0 for its session.
- **It sees four tools** — `knowledge_table`, `knowledge_read`, `knowledge_place`,
  `knowledge_circuit`. `knowledge_resolve` is gone; `knowledge_overlay` and `knowledge_write` are off
  unless `KNOWLEDGE_TOOLS_EXTRA=overlay,write` is set in the MCP server's environment.
- **It gives a reason** — `why`, one line — on every table and document it opens. That is what the
  footprint records and the map shows.

The shipped `.mcp.json` runs the server with no address, and it finds this install's web app from
`.env`; every path it calls is routed there, and `check/mcp-routes-check.py` keeps the two lists
together. With overlays off (the default) a walk is not closed "answered" by the agent: it stays open
until the next question starts, which closes it `abandoned` — the next question started, not that
this one failed; or until the client stops the MCP server, which closes it `ended`. One left open
an hour untouched is closed `abandoned` too ([FOOTPRINT.md](FOOTPRINT.md)).

**A change set the agent's `here` reports as `QUEUED`** waits in the review queue for a person; the
placement ends there. Accept or reject it on the map (the Back-Bone's ⚑, for an area's sentence). If
the tree moved on before it is accepted, accepting it says it is stale rather than applying it.

## If something is wrong

- `"valid": false` from `/healthz`: `docker compose logs ontology | grep -A40 valid=False` prints each
  error with what to do. `./ontology/tidy.py data/repo` says what a hand edit left out of step, and
  `--fix` regenerates `regions.json`; it needs Python with PyYAML on the host (`pip install pyyaml`). Without that,
  the regeneration in [DATA-REPO.md](DATA-REPO.md) runs inside the container.
- The ontology will not stay up: `docker compose logs ontology` from the first line.
- To go back: `git checkout <the commit you were on>` and step 3 again. `data/` is untouched by
  either direction, except the regenerated `regions.json` commit, which `git -C data/repo revert`
  undoes.
