# Installing, and the first two things after

The one-line version is in the [README](../README.md):

```sh
./install.sh --port 9000
```

This is everything that did not fit beside it.

## Start from the worked example, not an empty map

An empty install is a backbone with no areas: correct, and hard to read.
[`examples/back-office`](../examples/) is five areas, 79 entities, five levels deep. On a first install
`install.sh` asks whether to start from it (Enter says yes); `--example` answers yes without asking,
`--no-example` no. It has to go in **before** the first boot — that boot is what makes `data/repo` a git
repository and commits what is there.

Already installed with an empty map, and nothing in it you want to keep? Copy it over and commit it
yourself, or every write is refused as an uncommitted tree:

```sh
cp -r examples/back-office/. data/repo/
git -C data/repo add -A && git -C data/repo commit -m "start from examples/back-office"
docker compose restart ontology
```

## Without install.sh

```sh
cp .env.example .env
printf 'KNOWLEDGE_UID=%s\nKNOWLEDGE_GID=%s\n' "$(id -u)" "$(id -g)" >> .env
mkdir -p data/repo data/overlays data/walks data/harness data/access
docker compose up -d --build
./check/smoke.sh
```

The `mkdir` is not tidiness. Docker creates a missing bind-mount path as **root**, and this container
is not root, because it commits into a repository you own. A list short by one directory is a
container that never becomes healthy.

## When it does not come up

| What you see | Why | What to do |
|---|---|---|
| `./install.sh: Permission denied` | The tree arrived without its exec bits — a zip, or a share that does not carry them | `chmod +x install.sh check/*.sh check/*.py check/*.mjs` |
| `FATAL: /data/repo is not writable by uid …`, then a restart loop | Docker invented a bind-mount path as root | Remove it, `mkdir` **all five** as above, check `KNOWLEDGE_UID`/`KNOWLEDGE_GID` against `id -u` / `id -g`, start again |
| `exec /app/entrypoint.sh: no such file or directory`, on a file that is plainly there | CRLF line endings, so the kernel read the shebang as `/bin/sh\r` | Re-clone with `git clone`, which honours the repository's `eol=lf`. In place: `git add --renormalize . && git checkout -- .` |
| `port is already allocated` | Something else holds 8080 | `./install.sh --port 9000`, or `WEB_PORT=9000` in `.env` and `docker compose up -d`. Claude Code follows: the MCP server reads the port from `.env` |
| Every write is refused **read-only** | `data/repo` has uncommitted changes | Commit or revert them |
| A save fails with `git add -A failed: … index.lock` | Something else is running git in `data/repo` — your own shell, an editor's git integration, a second ontology on the same mount | Wait and retry; the service's own polling no longer does this. If it persists, `docker compose logs ontology` and look for a second writer |
| A change to `static/` or `ontology/` does nothing | Both are `COPY`ed into the image | `docker compose up -d --build` |
| Your first node is refused | Its `kind` is not in `vocab.yaml` — the point of that file | Below |
| `regions.json <area>: … no longer matches the files it is derived from` | Someone edited an area's `.md` by hand and did not regenerate | **[docs/DATA-REPO.md](DATA-REPO.md)** |
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

On the map, at the backbone: **`+ New AS`**. One sentence decides everything:

| Field | What it is | Without it |
|---|---|---|
| **When to choose this area** (`use_when`) | why an agent picks this row out of the list | a row with a title and no reason — **nobody picks it** |

Then, from that area's rack: `+ New node` → `+ New data` to attach documents.

---


---

**[docs/DATA-REPO.md](DATA-REPO.md)** — your ontology as a git repository, and the one derived file
in it. **[docs/PLATFORMS.md](PLATFORMS.md)** — what differs on macOS, Linux and Windows.
