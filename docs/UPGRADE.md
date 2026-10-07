# Installing, and applying an update to an install you already have

Two routes. A new install is one command. An install that is already running — with your own
areas and documents in `data/repo` — takes four steps, and the rest of this page is what each one
does, what it changes on its own, and how to see that it worked.

Nothing on this page touches your documents. `data/` is bind-mounted into the containers and stays
on disk across a rebuild; the only file an update may rewrite there is `data/repo/regions.json`,
which is generated, and it does so in a commit that says why.

## A new install

```sh
git clone https://github.com/CSP911/routemind.git routemind && cd routemind
./install.sh --name acme --port 9000
```

`install.sh` makes every directory under `data/`, writes `.env`, builds and starts the containers.
Details and troubleshooting: [INSTALL.md](INSTALL.md).

## Applying an update

### 1. Commit or set aside anything you changed by hand

```sh
git -C data/repo status --short
```

Empty is what you want. If you edited areas or documents in an editor, commit them in `data/repo`
first (`git -C data/repo add -A && git -C data/repo commit -m "…"`). The service refuses every write
on a dirty tree, and the startup step in 4 only repairs a clean one — it will not commit your
half-finished edit along with its own.

### 2. Get the new code

```sh
git pull
```

### 3. Make the directories a newer version needs

```sh
mkdir -p data/walks
```

`install.sh` makes these on a new install; an existing one has to make the ones added since. As of
2026-10-07 that is `data/walks`, where the footprint keeps every walk for six hours
([FOOTPRINT.md](FOOTPRINT.md)). Without it Docker creates the directory as root and the ontology
cannot write there.

### 4. Rebuild and restart

```sh
docker compose up -d --build
```

On start the ontology validates the repository and, if the only problem is that the generated
`regions.json` no longer matches the files, regenerates it and commits — one commit, its message
saying so. That covers two cases you may have:

- **An area whose directory name has a hyphen** (`back-office`). Before 2026-10-07 `regions.json`
  spelled it `back_office`, and a linked backbone could see the area but none of the documents in
  it. The table is rewritten with the directory name; nothing else changes.
- **An area file edited by hand** whose `use_when` or `export` was never regenerated into the table.

If the tree was not clean, nothing is committed: the log says so, and readers are still served what
the files say. Commit or discard, then restart.

### 5. What went away, and what you can delete

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

## Checking it worked

```sh
docker compose ps                                     # every container healthy
docker compose logs ontology --tail 20 | grep valid=  # valid=True
curl -s http://localhost:9000/api/knowledge/walks?since=0   # {"seq": …, "steps": […]} — the footprint is on
```

Then open the map. Above it there is a bar — **Live · a walk picker · Replay · Reasons**. Ask your
agent something; the map opens as it walks.

If the map does not show the bar, or opens the area but not the path inside it, reload the page
once: a browser holding a map cached by an older version refetches it after this update.

## The agent side

The MCP server is the file `mcp/knowledge_mcp.py`, run by your client from this checkout, so
`git pull` already updated it. Restart the client (or reconnect the server) so it picks the new
file up. Two things an agent now does differently:

- **It starts every question at hop 0** — `knowledge_table` with no address. Below hop 0 a call
  before that is refused with the way back ([INVARIANTS.md](INVARIANTS.md), 1). There is no id to
  pass: the server remembers hop 0 for its session.
- **It sees four tools** — `knowledge_table`, `knowledge_read`, `knowledge_place`,
  `knowledge_circuit`. `knowledge_resolve` is gone; `knowledge_overlay` and `knowledge_write` are off
  unless `KNOWLEDGE_TOOLS_EXTRA=overlay,write` is set in the MCP server's environment.
- **It gives a reason** — `why`, one line — on every table and document it opens. That is what the
  footprint records and the map shows.

If your client config points the MCP server at the web app (the shipped `.mcp.json` does,
`http://localhost:<port>/api/knowledge`), every path it calls is routed there; `check/mcp-routes-check.py`
keeps the two lists together.

## If something is wrong

- `valid=False` in the log: `docker compose logs ontology --tail 40` prints each error with what to
  do. `./ontology/tidy.py data/repo` lists leftovers from hand-deleted areas; `--fix` removes them.
- The ontology will not stay up: `docker compose logs ontology` from the first line.
- To go back: `git checkout <the commit you were on>` and step 4 again. `data/` is untouched by
  either direction, except the regenerated `regions.json` commit, which `git -C data/repo revert`
  undoes.
