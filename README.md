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
finding something does not grow with how much there is. What each area holds behind its line is its
own business, which is why the vocabulary and the depth are yours to change without anything upstream
knowing.

The two things that make it work are the two easiest to get wrong. **`use_when` is the only text read
before a choice is made**, so an area with a title and no reason is one nobody picks. And **absence is
decided at hop 0 only** — an area's own table says what that area holds, never what RouteMind lacks.

**[docs/ROUTING.html](docs/ROUTING.html)** — the same structure in detail: how a change to an
advertisement is proposed and applied, what an overlay is, and how an agent walks all of it. Open it
in a browser.

## One question, several areas

Some questions do not sit in one area. Settling a trip is three: how many days count, how much they
pay, and whether any of it is taxed. Picking one area answers a third of it.

![How an overlay gets made: the agent reads hop 0, picks every area the question belongs to and says
why for each, works from the one merged table, and closes it with the addresses the answer actually
came from. RouteMind serves and checks; it never chooses.](docs/img/overlay-flow.svg)

An **overlay** is that working set, made as an object: the question it is for, the areas and nodes in
it and **why each one is in it**, the trail of what was added and dropped while reading, and — when it
closes — what was actually used to answer.

**The agent decides what goes in it.** RouteMind has no model of its own for this: it serves the
tables, refuses an address that resolves to nothing and an overlay over its caps, and keeps the
record — which rows a question belongs to is never its judgment. So the picking is done by whatever
model is driving the MCP client, from the `use_when` lines alone. A person can draw one too, by
ticking areas on the map and pressing **Draw VRF**; both make the same object, and the map draws
either.

Three rules are worth knowing before you rely on it:

- **It narrows where to look; it does not change what exists.** "Not in the overlay" never means "not
  in RouteMind" — absence is still decided at hop 0, and going back there is budgeted at three times
  a run.
- **It is run evidence, not ontology.** It is never committed to the data repository — a commit per
  question would bury the structure — so it lives in its own store, expires, and leaves a record.
- **Every change carries a reason**, because what was thought is the part worth learning from later.

Closing records each address as `member` or `reached` — `reached` meaning the answer came from
something that was never in the set, which says the overlay was drawn a level too coarse. That is
signal, not error, and it is the thing the design is trying to measure.

**[docs/OVERLAY.md](docs/OVERLAY.md)** — the object, the API and the caps.

---

## Quickstart

### What you need

Docker, with `docker compose`. That is all the service itself needs — the containers carry python and
git. The checks that run at the end use the host's `curl` and `python3`, and the screen half also uses
`node` if it is there; without those the install still comes up, it just verifies less.

### Where it runs

macOS, Linux and Windows. The service is two Linux containers, so it is identical on every host
Docker runs on; what differs is the handful of pieces that run on your own machine instead.

| | macOS | Linux | Windows |
|---|---|---|---|
| The two containers | yes | yes | yes — Docker Desktop, WSL2 backend |
| The map, in a browser | yes | yes | yes |
| `mcp/knowledge_mcp.py` | yes | yes | yes, natively — no WSL needed |
| `install.sh`, `check/*` | yes | yes | from WSL or Git Bash |

The MCP server is one file, stdlib only, and runs on **any python 3.7 or newer** — checked against
3.7, 3.8, 3.9, 3.11, 3.12 and 3.14. That includes Windows python, with no WSL and nothing to install.

#### Windows, in particular

Three things differ, and only the first one bites during normal use.

1. **Write `python`, not `python3`,** in every MCP config below. On Windows `python3` is usually not
   a program at all: it is an alias that opens the Microsoft Store. Give the script an absolute path
   too, unless your client lets you set a working directory.
2. **Run `install.sh` and anything in `check/` from WSL or Git Bash.** They are POSIX shell and there
   is no PowerShell port. Docker Desktop itself is driven normally from either.
3. **Let git give you the repository's own line endings.** `.gitattributes` pins them to LF, so a
   plain `git clone` is right even with `core.autocrlf=true` set globally. Unpacking a zip made on
   Windows, or overriding those attributes, turns `ontology/entrypoint.sh` into CRLF — and the
   container then refuses to start with `no such file or directory` naming a file that is plainly
   there, because the kernel read its shebang as `/bin/sh\r`.

Under WSL, keep the clone inside the WSL filesystem rather than under `/mnt/c`. The ontology container
runs as a fixed uid:gid and commits into `data/repo` through a bind mount, and a Windows-mounted path
does not model POSIX ownership the way that needs.

### Languages

The screen speaks English, 한국어, 日本語 and 简体中文, chosen from the menu in the top-right corner. It
changes instantly, it is remembered in that browser, and a first visit follows the browser's own
language — **per viewer, not per install**, because one install is a team's ontology and an
install-time setting would serve everyone whatever the installer happened to speak.

What the agent is handed stays English on purpose, and the ontology stays in whatever words you wrote
it in. [docs/I18N.md](docs/I18N.md) says why, and how to add a language.

### More than one backbone

An install is **one backbone and an exchange** — the place backbones meet, wired from the first
`docker compose up` so that adding a second is a file and a registration rather than a migration.
Head office and a subsidiary, a company and its supplier: two RouteMinds that must not become one.

An area crosses by writing the line it wants to show in the *other* backbone's hop 0, and by nothing
else. Documents are relayed, so no agent ever holds a peer's credential, and adding the tenth backbone
changes nothing about the nine already running.

The part worth reading is what absence means once there is a link: hop 0 can only claim something is
missing while every link is up, and says so itself when one is not.
[docs/PEERING.md](docs/PEERING.md), and `docker compose -f docker-compose.yml -f
docker-compose.peer.yml up -d` for a second one.

### One command

```sh
git clone https://github.com/CSP911/routemind.git knowledge && cd knowledge
./install.sh
```

In order, `install.sh`:

1. copies `.env.example` to `.env` if you have none, and appends **your own uid/gid** to it;
2. asks once whether you have an LLM — Enter skips it, and it does not ask again;
3. `mkdir -p data/repo data/publish data/overlays` — **before** compose, on purpose;
4. `docker compose up -d --build`;
5. waits for the web container, reads `/api/app-config`, and tells you which mode you ended up in;
6. runs `check/smoke.sh` — the API, an agent's walk through the MCP server, and the map screen.

→ **http://localhost:8080**

It is safe to run again: an existing `.env` is kept and only the settings you pass are replaced.
Running it again is also how you add or change the LLM later. It never stops to ask when there is no
terminal to ask in, or when `.env` already answers.

```sh
./install.sh --no-llm      # do not ask; run without one
```

Two containers, no database. On first boot an empty ontology is laid into `data/repo`, and that
directory becomes a git repository. Every write — from the screen or the API — **commits** into it, so
undo is `git revert`.

### Start from the worked example, not an empty map

An empty install is a backbone with no areas: correct, and hard to read. To start from
[`examples/back-office`](examples/) instead — five areas, 79 entities, five levels deep — copy it in
**before** the first boot:

```sh
mkdir -p data/repo && cp -r examples/back-office/. data/repo/
./install.sh --no-llm
```

The container git-inits and commits whatever it finds there. It is a starting point to edit or
delete, not a schema.

### With an LLM

Optional, and it changes exactly one thing: a **✨ Suggest** button beside each routing line drafts it
for you to edit. Leave it out and those buttons are shown disabled — everything else is identical,
because you write every line either way.

**First, ask the provider what the key can actually use:**

```sh
./check/llm-probe.py --provider openai --base https://api.openai.com --key $KEY
./check/llm-probe.py --provider openai --base https://api.openai.com --key $KEY --model gpt-4o-mini
```

It lists the models the key can see, then makes one small call with the one you pick. No model list is
written into this repository — one would start going stale the day it was written, and would reject
new models rather than accept them.

**Then install with it.** Three providers, and they are genuinely different wires rather than one with
options — the path, the auth header, where the system prompt goes and the shape of the reply all differ:

```sh
# OpenAI
./install.sh --llm-provider openai \
             --llm-url https://api.openai.com --llm-key sk-... --llm-model gpt-4o-mini

# Anthropic
./install.sh --llm-provider anthropic \
             --llm-url https://api.anthropic.com --llm-key sk-ant-... --llm-model claude-sonnet-5

# A LiteLLM-style gateway, or anything OpenAI-shaped — the default
./install.sh --llm-provider litellm \
             --llm-url https://your-gateway --llm-key ... --llm-model ...
```

Environment variables do the same, for CI:

```sh
KNOWLEDGE_LLM_PROVIDER=openai KNOWLEDGE_LLM_URL=https://api.openai.com \
KNOWLEDGE_LLM_KEY=sk-... KNOWLEDGE_LLM_MODEL=gpt-4o-mini ./install.sh
```

Two rules account for most misconfigurations:

- **Give the base URL without `/v1`.** The client appends the rest itself.
- **A provider this build does not know turns the LLM off** and says so, in the startup log and in what
  `install.sh` prints, rather than being quietly ignored.

Because `install.sh` finishes by reading `/api/app-config`, a wrong key or a trailing `/v1` shows up
there and not later:

```
RouteMind is at http://127.0.0.1:8080 — with openai: it derives addresses and drafts conditions.
RouteMind is at http://127.0.0.1:8080 — without an LLM: you type the address and the condition yourself.
```

To add or change one afterwards, run `./install.sh` again with the flags, or edit the `ONTOLOGY_LLM_*`
lines in `.env` and re-run it.

### By hand, without install.sh

**`mkdir` before compose.** Docker creates a missing bind-mount path as root, and this container is not
root, because it commits into a repository you own:

```sh
cp .env.example .env
printf 'KNOWLEDGE_UID=%s\nKNOWLEDGE_GID=%s\n' "$(id -u)" "$(id -g)" >> .env
mkdir -p data/repo data/publish data/overlays data/harness
docker compose up -d --build
./check/smoke.sh
```

### When it does not come up

| What you see | Why | What to do |
|---|---|---|
| `./install.sh: Permission denied` | The tree arrived without its exec bits — a zip, or a share that does not carry them | `chmod +x install.sh check/*.sh check/*.py check/*.mjs`. The container's ENTRYPOINT no longer needs this: the Dockerfile chmods it during the build |
| `FATAL: /data/repo is not writable by uid …`, then a restart loop | Docker invented the bind-mount path as root | Remove it, `mkdir -p data/repo data/publish data/overlays`, check `KNOWLEDGE_UID`/`KNOWLEDGE_GID` in `.env` against `id -u` / `id -g`, and start again |
| `exec /app/entrypoint.sh: no such file or directory`, on a file that is plainly there | Its line endings are CRLF, so the kernel read the shebang as `/bin/sh\r`. A zip made on Windows, or `core.autocrlf` overriding `.gitattributes` | Re-clone with `git clone`, which honours the repository's `eol=lf`. To repair in place: `git add --renormalize . && git checkout -- .`, then `docker compose up -d --build` |
| The MCP server dies at startup on Windows with `UnicodeEncodeError`, before any tool is called | An old copy from before this was fixed. Python uses the locale code page for a pipe, and cp1252/cp949/cp932 cannot encode `—` or `→` — both are in the area list sent with the `initialize` reply | Pull. If you must run an old copy, set `PYTHONUTF8=1` in the client's env |
| `port is already allocated` | Something else holds 8080 | Set `WEB_PORT=9000` in `.env`, then `docker compose up -d` |
| The map draws, but every write is refused **read-only** | `data/repo` has uncommitted changes — someone edited it by hand | Commit or revert them in `data/repo`, then `curl -X POST -H 'Content-Type: application/json' -d '{}' localhost:8080/api/knowledge/publish` |
| A change to `static/` or `ontology/` does nothing | Both are `COPY`ed into the image, not bind-mounted | `docker compose up -d --build` |
| Your first node is refused | Its `kind` is not in `vocab.yaml` — which is the point of that file | Edit `data/repo/vocab.yaml`, commit, publish |
| Anything else | | `docker compose logs -f ontology web` |

---

### ⚠ There is no authentication

This build has no login. **Anyone who can reach the port can call every write API.** Put it on a
network where that is acceptable, or put an authenticating reverse proxy in front of it.

The **name** field at the top right is a signature that goes on commits and proposals, kept in that
person's own browser. **It is not a permission.**

---

## First thing to do — `vocab.yaml` is your domain

A node's `kind` and an edge's `rel` **must appear in the vocabulary**, so until you edit this file
your first node is refused. The starter set (`system` · `tool` · `store` · `host` · `channel` ·
`task` · `party`) is a starting point, not a schema.

After installing, edit `data/repo/vocab.yaml` and commit — there is no vocabulary editor on screen
yet.

## Second — one area

On the map, at the backbone: **`+ New AS`**. Two sentences are written together:

| Field | What it is | Without it |
|---|---|---|
| **When to choose this area** (`use_when`) | why an agent picks this row out of the list | a row with a title and no reason — **nobody picks it** |
| **Core one-liner** | this area's row in `CORE.md` | hop 0 goes out with an empty description |

Then, from that area's rack: `+ New node` → `+ New data` to attach documents.

---

## More about the LLM

Configuring one is in the quickstart. What that does not say:

**You write every routing line yourself**, with a model or without: when an agent should choose an
area, what a node holds, what a document is for. Each field shows how to write it, and **Suggest fills
the box — it does not save.** Nothing is written until you press the form's own button. The address a
name gives is filled in as you type the name, and you can change it before saving. The one thing only
a model can do is give an address to a name that is not in Latin letters; without one, you type that
address.

**A kind is never asked for.** Nothing reads one until you declare `edge_rules`, so RouteMind picks it
with an LLM where there is one and takes `default_kind` from `vocab.yaml` where there is not. The
response says `kind_generated` either way, so a domain that later makes kinds mean something can find
the ones nobody actually chose.

`ONTOLOGY_LLM_MAX_TOKENS` and `ONTOLOGY_LLM_TEMPERATURE` are yours. **`response_format` is not**: the
code sets it per call — the two prompts whose answer is parsed as JSON ask for JSON, the four that read
one line do not. Setting it by hand breaks the parsing, and the only symptom is that the model seems to
be answering strangely.

`./check/llm-paths.sh` runs both modes, so a change to one does not quietly break the other.

## Connecting an agent

Optional — the map works on its own. Full detail is in **[docs/AGENTS.md](docs/AGENTS.md)**; this is
enough to get an agent reading.

An agent reads this ontology the same way in every case: **fetch the list of areas, pick one, fetch
that area, read what it points at.** Two operations, never a third. What differs between engines is
only how those two reach them.

| Way | For | What it is |
|---|---|---|
| **MCP** | Claude Code, Codex, Claude Desktop, Cursor, any MCP client | `mcp/knowledge_mcp.py` — stdio, stdlib only |
| **Paste** | any chat agent, a notebook, someone else's tool | the **Copy for an agent** button on the map |
| **Launch URL** | a web console that accepts a run | `KNOWLEDGE_AGENT_URL` |

All three hand over the **same advertisement**, from one formatter — three descriptions of one
ontology would drift, and the one that drifts is the one nobody is checking.

### The MCP server

```sh
python3 mcp/knowledge_mcp.py --api http://localhost:8080/api/knowledge
```

One file, stdlib only: no install, no virtualenv, nothing to build. `--api` is the v1 root — the web
proxy at `/api/knowledge` (use this) or an ontology directly at `.../v1`. `--actor NAME` sets the name
recorded on anything the connection writes; it defaults to `mcp`. Both also read `KNOWLEDGE_API` and
`KNOWLEDGE_ACTOR` from the environment.

Every config below writes `python3`. On Windows write `python` — and if your client offers no way to
set a working directory, give the script an absolute path.

Point `--api` at another host and it works the same — the agent does not have to be where RouteMind is.

### Claude Code

**Opening this repository is the whole setup.** `.mcp.json` at the root registers the server with a
path relative to the repository, so Claude Code offers it and one approval connects it.

From any other directory, register it once with an absolute path:

```sh
claude mcp add knowledge -- python3 /abs/path/to/knowledge/mcp/knowledge_mcp.py \
  --api http://localhost:8080/api/knowledge --actor claude-code
```

`claude mcp list` shows it; `/mcp` inside a session shows the tools it exposes.

### Codex

`~/.codex/config.toml`:

```toml
[mcp_servers.knowledge]
command = "python3"
args = ["/abs/path/to/knowledge/mcp/knowledge_mcp.py",
        "--api", "http://localhost:8080/api/knowledge",
        "--actor", "codex"]
```

### Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS,
`%APPDATA%\Claude\claude_desktop_config.json` on Windows — then restart the app:

```json
{
  "mcpServers": {
    "knowledge": {
      "command": "python3",
      "args": ["/abs/path/to/knowledge/mcp/knowledge_mcp.py",
               "--api", "http://localhost:8080/api/knowledge",
               "--actor", "claude-desktop"]
    }
  }
}
```

### Cursor, and any other MCP client

The same block, in whatever that client calls its MCP config — Cursor reads `.cursor/mcp.json` in the
project or `~/.cursor/mcp.json` globally, and most others take this identical shape:

```json
{
  "mcpServers": {
    "knowledge": {
      "command": "python3",
      "args": ["/abs/path/to/knowledge/mcp/knowledge_mcp.py",
               "--api", "http://localhost:8080/api/knowledge"]
    }
  }
}
```

### What the agent gets

```
knowledge_table(path?)   a routing table — what is here, and where to go next.
                         No argument = the list of areas, where every search starts.
knowledge_read(path)     one document, as written.
knowledge_overlay(op)    the working set for one question, a VRF — create · get · add · remove · close.
                         Present only where the install keeps overlays (ONTOLOGY_OVERLAYS).
```

Two things about this are worth knowing before you write a prompt around it:

- **You do not have to name RouteMind in the question.** The list of areas travels in the server's
  `instructions`, sent at initialize, so a client that loads tools lazily has still seen it. What
  decides whether the agent comes here is therefore the `use_when` line on each area — which is why
  that is the field to spend time on.
- **`instructions` are built when the session starts.** An area created mid-session shows up in the
  tool description at the next tool listing, but not in the instructions until the next session.

### Checking it works

Before wiring a client, run the protocol and an agent's whole walk against your install:

```sh
./check/mcp-check.py http://localhost:8080/api/knowledge
```

It initializes, lists the tools, walks from the area list into an area and into a document, and checks
that an invented address is refused. `./check/smoke.sh` runs it as its middle third.

By hand, if you want to see the bytes:

```sh
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"0"}}}' \
  | python3 mcp/knowledge_mcp.py --api http://localhost:8080/api/knowledge
```

### Without MCP

**Copy for an agent** on the map puts the same advertisement on the clipboard — the area list, the
base URL, and the rule never to build an address — for pasting into any chat agent.

With `KNOWLEDGE_AGENT_URL` set, ticking areas on the map draws a **▶ Start** button that sends the
selection to a web console. With it unset, that button and the tick boxes are **not drawn at all**,
rather than left as a control that does nothing.

## Layout

```
ontology/     the ontology API — python + pyyaml + git. Knows nothing about any domain
web/          the map and a proxy — one FastAPI file. Knows nothing about any domain
mcp/          the MCP server, so any MCP-capable agent can read the ontology
static/       the map screen
seed/         an empty ontology, copied into data/repo on first boot
examples/     one worked ontology — copy it into data/repo instead of starting empty
data/repo     ← your ontology. A git repository, and the only thing to back up
data/publish  derived from data/repo. Safe to delete; it is rebuilt
data/overlays one question's working set each — run evidence, not structure
data/harness  the curator's store: the review queue behind "Advertise upstream"
check/        smoke.sh (API + agent + screen) · write-paths.sh (every write path, atomically)
              mcp-check.py (the protocol, and an agent's walk) · llm-paths.sh (both LLM modes)
```

Every write **commits** into `data/repo`. Undo is `git revert`.

## Not yet domain-neutral

Written down rather than glossed over: **[docs/DOMAIN-NEUTRALITY.md](docs/DOMAIN-NEUTRALITY.md)**.
Nothing there blocks a new domain, but some rules in the validator belong to the domain this code
came from, and knowing which is better than being surprised.

## Where this came from

Split out of the Knowledge unit of IRIS. **This repository is the canonical source** of the
ontology service. See [docs/PROVENANCE.md](docs/PROVENANCE.md).

## Contact

Business inquiries, collaboration, or just curious: **qct8377@gmail.com**
LinkedIn → [linkedin.com/in/cspark911](https://www.linkedin.com/in/cspark911/)
Bug reports and questions → [GitHub Issues](https://github.com/CSP911/routemind/issues)

---

## License

MIT — see [LICENSE](LICENSE).
