# Installing, and the first two things after

The one-line version is in the [README](../README.md):

```sh
./install.sh --port 9000
```

This is everything that did not fit beside it.

## Start from the worked example, not an empty map

An empty install is a backbone with no areas: correct, and hard to read.
[`examples/back-office`](../examples/) is five areas and 74 documents (79 entities with the areas' own pages), five levels deep. On a first install
`install.sh` asks whether to start from it (Enter says yes); `--example` answers yes without asking,
`--no-example` no. It has to go in **before** the first boot — that boot is what makes `data/repo` a git
repository and commits what is there.

Already installed? The reset replaces the map in one commit and tags the one it replaces, so it can
be brought back ([DATA-REPO.md](DATA-REPO.md#starting-over)):

```sh
./ontology/reset.sh --example      # or --empty; add --yes where there is no terminal to ask on
```

## Without install.sh

If another RouteMind already runs on this machine, use `./install.sh`: it refuses rather than take
that one's containers over. By hand, the steps are the ones it takes:

```sh
cp .env.example .env
printf 'KNOWLEDGE_UID=%s\nKNOWLEDGE_GID=%s\n' "$(id -u)" "$(id -g)" >> .env
# This checkout's own name — the one install.sh gives a new install: the directory plus six digits of its path
NAME="$(basename "$PWD" | tr 'A-Z' 'a-z' | tr -c 'a-z0-9.\n-' '-' | cut -c1-32)-$(printf '%s' "$(pwd -P)" | cksum | cut -d' ' -f1 | cut -c1-6)"
printf 'COMPOSE_PROJECT_NAME=%s\nIMAGE_TAG=%s\n' "$NAME" "$NAME" >> .env
# The key another backbone's circuit presents (docs/CIRCUIT.md); nothing crosses until an area is exported
printf 'KNOWLEDGE_CIRCUIT_TOKEN=%s\n' "$(head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n')" >> .env
# The port is WEB_PORT in .env, 8080 as copied — edit that line if 8080 is taken
mkdir -p data/repo data/overlays data/walks data/harness data/access
docker compose up -d --build
./check/smoke.sh                  # checks the install on .env's WEB_PORT
```

The name is not decoration. Without it compose names the containers after the directory and tags the
images `0.1.0` — and a second checkout called `routemind` (the README's own clone target) gets the
same names as the first, so `up` rebuilds the first one's images and recreates its containers from
this checkout's code.

The `mkdir` is not tidiness. Docker creates a missing bind-mount path as **root**, and this container
is not root, because it commits into a repository you own. A list short by one directory is a
container that never becomes healthy.

## When it does not come up

| What you see | Why | What to do |
|---|---|---|
| `./install.sh: Permission denied` | The tree arrived without its exec bits — a zip, or a share that does not carry them | `chmod +x install.sh check/*.sh check/*.py check/*.mjs` |
| `FATAL: /data/repo is not writable by uid …`, then a restart loop | Docker invented a bind-mount path as root | Remove it, `mkdir` **all five** as above, check `KNOWLEDGE_UID`/`KNOWLEDGE_GID` against `id -u` / `id -g`, start again |
| `exec /app/entrypoint.sh: no such file or directory`, on a file that is plainly there | CRLF line endings, so the kernel read the shebang as `/bin/sh\r` | Re-clone with `git clone`, which honours the repository's `eol=lf`. In place: `git add --renormalize . && git checkout -- .` |
| `! port 8080 is already in use by something else` (or Docker's `port is already allocated`) | Something else holds the port | `./install.sh --port <the one it suggests>`, or `WEB_PORT=…` in `.env` and `docker compose up -d`. Claude Code follows: the MCP server reads the port from `.env` |
| `! another RouteMind is running under the name …` | A checkout elsewhere on this machine has the same compose project name — starting would replace its containers | Give this one its own name: the two `echo … >> .env` lines it prints, then `./install.sh` |
| `The install is up, and the checks above found something wrong` | One of the install's own checks failed | The full output is in `data/install-checks.log`, and printed above the message |
| Every write is refused **read-only** | `data/repo` has uncommitted changes | Commit or revert them |
| A save fails with `git add -A failed: … index.lock` | Something else is running git in `data/repo` — your own shell, an editor's git integration, a second ontology on the same mount | Wait and retry; the service's own polling no longer does this. If it persists, `docker compose logs ontology` and look for a second writer |
| A change to `static/` or `ontology/` does nothing | Both are `COPY`ed into the image | `docker compose up -d --build` |
| A node is refused with "kind … not in vocab" | Its `kind` is not in `vocab.yaml` — the point of that file | Below |
| `regions.json <area>: … no longer matches the files it is derived from` | Someone edited an area's `.md` by hand and did not regenerate | **[docs/DATA-REPO.md](DATA-REPO.md)** |
| Anything else | | `docker compose logs -f ontology web` |

---

## First — `vocab.yaml` is your domain

A node's `kind` **must appear in the vocabulary**. Anything added without one gets `default_kind` —
`document` in the starter set — so nothing is refused at first. The starter set (`document` · `topic`
· `system` · `tool` · `store` · `host` · `channel` · `task` · `party`) is a starting point, not a
schema: replace it with the words your domain uses. Edit `data/repo/vocab.yaml` and commit — there is
no vocabulary editor on screen yet.

It is also where you say what may leave. `export: no` on a kind stops that sort of thing crossing to
another domain — one decision per kind rather than per document.

## Second — one area

On an empty map, **Create the first area**; later ones from the Back-Bone box → **New AS**. One sentence
decides everything:

| Field | What it is | Without it |
|---|---|---|
| **When to choose this area** (`use_when`) | why an agent picks this row out of the list | a row with a title and no reason — **nobody picks it** |

Then, on that area's rack: **+ New data** for a document. **+ New node** makes a holder — a heading
documents sit under — when there are enough to group.

## Uninstall

From inside the checkout. `data/repo` is your ontology, with its whole history — copy it out first if
you want it:

```sh
cp -a data/repo ~/routemind-backup            # optional
docker compose down --rmi all --remove-orphans  # this install's containers, network and images
cd .. && rm -rf <the checkout>
```

Then remove the `knowledge` server from any MCP client config you added it to by hand (Claude Code's
comes from `.mcp.json` in the checkout, and goes with it). An install made before each checkout had
its own `IMAGE_TAG` (2026-10-10) has images tagged `0.1.0`, which another checkout may share: there,
use `docker compose down --remove-orphans` and delete the images by hand once nothing uses them.

---

**[docs/DATA-REPO.md](DATA-REPO.md)** — your ontology as a git repository, and the one derived file
in it. **[docs/PLATFORMS.md](PLATFORMS.md)** — what differs on macOS, Linux and Windows.
