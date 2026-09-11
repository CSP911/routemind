# Knowledge

**An ontology you can see the agent reading.** Split a domain into areas, let each area advertise
itself in one line, and an agent picks from that list before reading anything else. The map draws
that structure as a wiring diagram, and one click shows you **the exact text an agent is handed**.

The domain is not in this code. The vocabulary and the areas are data, and the data is your own git
repository.

---

## Install

```sh
git clone <this repository> knowledge && cd knowledge
./install.sh
```

It asks once whether you have an LLM (optional — see below), brings up both containers, and runs the
checks. Safe to run again; that is also how you add or change the LLM later.

Scripted, with no question asked:

```sh
./install.sh --no-llm
./install.sh --llm-url https://api.openai.com --llm-key sk-... --llm-model gpt-4o-mini
KNOWLEDGE_LLM_URL=... KNOWLEDGE_LLM_KEY=... KNOWLEDGE_LLM_MODEL=... ./install.sh
```

By hand — **`mkdir` before compose.** Docker creates a missing bind-mount path as root, and this
container is not root, because it commits into a repository you own:

```sh
cp .env.example .env
printf 'KNOWLEDGE_UID=%s\nKNOWLEDGE_GID=%s\n' "$(id -u)" "$(id -g)" >> .env
mkdir -p data/repo data/publish
docker compose up -d
./check/smoke.sh
```

→ http://localhost:8080

Two containers, no database. On first boot an empty ontology is laid into `data/repo` and that
directory becomes a git repository.

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

## An LLM is optional — it is a button

**You write every routing line yourself**, with or without an LLM: when an agent should choose an
area, what a node holds, what a document is for. Each field shows how to write it. The address a name
gives is filled in as you type the name, and you can change it before saving.

Set the three `ONTOLOGY_LLM_*` variables and a **✨ Suggest** button beside each of those fields drafts
the line for you to edit — nothing is saved until you press the form's own button. Leave them unset and
the same buttons are shown disabled; nothing else changes. The one thing only a model can do is give an
address to a name that is not in Latin letters — without one, you type that address.

**A kind is never asked for.** Nothing reads one until you declare `edge_rules`, so Knowledge picks
it with an LLM where there is one and takes `default_kind` from `vocab.yaml` where there is not. The
response says `kind_generated` either way, so a domain that later makes kinds mean something can find
the ones nobody actually chose.

Three providers, and they are genuinely different wires rather than one with options — the path, the
auth header, where the system prompt goes and the shape of the reply all differ:

| `ONTOLOGY_LLM_PROVIDER` | for |
|---|---|
| `litellm` (default) | a LiteLLM-style gateway, or anything OpenAI-shaped |
| `openai` | `api.openai.com` |
| `anthropic` | `api.anthropic.com` |

Give the base URL **without** `/v1` — the client appends the rest itself. A provider this build does
not know turns the LLM off and says so, in the startup log and in what `install.sh` prints, rather
than being quietly ignored.

`ONTOLOGY_LLM_MAX_TOKENS` and `ONTOLOGY_LLM_TEMPERATURE` are yours. **`response_format` is not**: the
code sets it per call — the two prompts whose answer is parsed as JSON ask for JSON, the four that
read one line do not. Setting it by hand breaks the parsing, and the only symptom is that the model
seems to be answering strangely.

`./install.sh` asks for these, or takes them as flags, and writes them into `.env`. It finishes by
reading `/api/app-config` and telling you which mode the install ended up in, so a wrong key or a
`/v1` on the end of the URL shows up there rather than later.

To find out what a key can actually use before configuring anything:

```sh
./check/llm-probe.py --provider openai --base https://api.openai.com --key $KEY
./check/llm-probe.py --provider openai --base https://api.openai.com --key $KEY --model <one of them>
```

It asks the provider which models the key lists, then makes one small call with the model you pick.
No list of models is written into this repository: one would start going stale the day it was
written, and would reject new models rather than accept them.

## Connecting an agent is optional too

See **[docs/AGENTS.md](docs/AGENTS.md)**. In short, an agent reaches this ontology one of three ways:

| Way | For | Set up |
|---|---|---|
| **MCP server** | Claude Code, Codex, any MCP client | `mcp/knowledge_mcp.py` — two tools (three with overlays), stdlib only |
| **Launch URL** | a web console that takes a run (Pi, your own) | `KNOWLEDGE_AGENT_URL` |
| **Copy the context** | any chat agent, by hand | the **Copy for an agent** button on the map |

With no `KNOWLEDGE_AGENT_URL` set, **the start button and the tick boxes are not drawn at all** —
rather than leaving a control that does nothing.

---

## Layout

```
ontology/     the ontology API — python + pyyaml + git. Knows nothing about any domain
web/          the map and a proxy — one FastAPI file. Knows nothing about any domain
mcp/          the MCP server, so any MCP-capable agent can read the ontology
static/       the map screen
seed/         an empty ontology, copied into data/repo on first boot
data/repo     ← your ontology. A git repository, and the only thing to back up
data/publish  derived from data/repo. Safe to delete; it is rebuilt
check/        smoke.sh (API + agent + screen) · write-paths.sh (every write path, atomically)
              mcp-check.py (the protocol, and an agent's walk) · llm-paths.sh (both LLM modes)
```

Every write **commits** into `data/repo`. Undo is `git revert`.

## How it works

**[docs/ROUTING.html](docs/ROUTING.html)** — the structure in diagrams: what an area advertises and
how the rest is aggregated behind one line, how a change to an advertisement is proposed and applied,
what an overlay is, and how an agent walks all of it. Open it in a browser.

## Not yet domain-neutral

Written down rather than glossed over: **[docs/DOMAIN-NEUTRALITY.md](docs/DOMAIN-NEUTRALITY.md)**.
Nothing there blocks a new domain, but some rules in the validator belong to the domain this code
came from, and knowing which is better than being surprised.

## Where this came from

Split out of the Knowledge unit of IRIS. **This repository is the canonical source** of the
ontology service. See [docs/PROVENANCE.md](docs/PROVENANCE.md).
