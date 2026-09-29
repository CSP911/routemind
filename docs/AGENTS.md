# Connecting an agent

The structure behind all of this is drawn in **[ROUTING.html](ROUTING.html)**.

An agent reads this ontology the same way in every case: **fetch the list of areas, pick one, fetch
that area, read what it points at.** Two operations, and never a third.

What differs between engines is only how those two operations reach them.

| Way | For | What it is |
|---|---|---|
| **MCP** | Claude Code, Codex, any MCP client | `mcp/knowledge_mcp.py` — two tools over stdio, three where overlays are kept |
| **Paste** | any chat agent, a notebook, someone else's tool | the **Copy for an agent** button on the map |
| **Launch URL** | a web console that accepts a run | `KNOWLEDGE_AGENT_URL` |

All three hand over the **same advertisement**. That is the point, and it is why there is one
formatter rather than three descriptions of the ontology: three would drift, and the one that drifts
is the one nobody is checking.

---

## MCP

```sh
python3 mcp/knowledge_mcp.py --api http://localhost:8080/api/knowledge
```

Stdlib only — no install, no virtualenv, nothing to build. It speaks stdio JSON-RPC, on any python
3.7 or newer.

`--api` is the **v1 root**: the web proxy at `/api/knowledge`, which is the one to use, or an ontology
directly at `…/v1`. `--actor NAME` is the name recorded on anything the connection writes; it defaults
to `mcp`. Both also read the environment — `KNOWLEDGE_API` and `KNOWLEDGE_ACTOR` — for clients that
give you no way to pass arguments. Point `--api` at another host and it works the same: the agent does
not have to be where RouteMind is.

### In a container

Normally there is no need: the server is one stdlib-only file and the client launches it. The `Dockerfile` at the repository root
is for directories and harnesses that want to start a server and introspect it without standing up a
backbone first — it is at the root because that is where they look, and `./install.sh` remains how
you actually run RouteMind.

```sh
docker build -t routemind-mcp .
docker run -i --rm routemind-mcp                       # introspection only
docker run -i --rm -e KNOWLEDGE_API=http://host.docker.internal:8080/api/knowledge routemind-mcp
```

`-i` and no `-t`: the protocol is JSON-RPC on stdin and stdout, and a tty in the middle of that is a
tty in the middle of the protocol. With nothing at `--api`, `initialize` and `tools/list` still
answer — the area list a tool description would have carried is replaced by the reason it could not
be fetched, so an agent is told why rather than handed an empty table.

### Claude Code

Nothing to configure. `./install.sh` has already written `.mcp.json` at the repository root, so:

```sh
cd routemind
claude
```

Claude Code sees the file, offers the server, and one approval is the whole setup. `/mcp` inside the
session lists the tools; `claude mcp list` shows whether it registered at all.

**The port follows your install.** `install.sh --port 9000` rewrites `.mcp.json` to match. It used to
ship with 8080 hard-coded, which on any other port gave Claude Code a server that registers, lists
its tools and fails on every call — worse than no server, because the tools are visibly there.

Ask it something your ontology covers, without naming RouteMind. The area list reaches the model
through the server's `instructions`, so what decides whether it comes here is the `use_when` line on
each area, not the word "RouteMind" in your question. If it answers from its own knowledge instead,
that is the finding: some area's `use_when` does not say when to come to it.

`/circuit <url> <token>` is also registered, as a project command — it reads another backbone for the
length of the session. **[../docs/PEERING.md](PEERING.md)**.

#### Somewhere else, or another project

```sh
claude mcp add knowledge -- python3 /abs/path/to/routemind/mcp/knowledge_mcp.py \
  --api http://localhost:8080/api/knowledge
```

Point `--api` at another host and it works the same — the agent does not have to be where RouteMind
is.

For a different project, put the same block in its own `.mcp.json` with an absolute path:

```json
{
  "mcpServers": {
    "knowledge": {
      "command": "python3",
      "args": ["/abs/path/to/knowledge/mcp/knowledge_mcp.py",
               "--api", "http://localhost:8080/api/knowledge",
               "--actor", "claude-code"]
    }
  }
}
```

### Codex, and other MCP clients

The same command, in whatever that client calls its MCP config. Most take the identical shape:

```toml
[mcp_servers.knowledge]
command = "python3"
args = ["/abs/path/to/knowledge/mcp/knowledge_mcp.py", "--api", "http://localhost:8080/api/knowledge"]
```

`~/.codex/config.toml`. Everything else takes JSON of one shape — Cursor reads `.cursor/mcp.json` in
the project or `~/.cursor/mcp.json` globally; Claude Desktop reads
`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS and
`%APPDATA%\Claude\claude_desktop_config.json` on Windows, and has to be restarted afterwards:

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

On Windows write `python`, not `python3`: there, `python3` is usually an alias that opens the
Microsoft Store rather than a program. And give the script an absolute path unless the client lets
you set a working directory.

### The tools

Two do the reading, and the rest appear only where the install has the thing they need — a tool for
a feature that is not configured would be a tool that fails when used, which is worse than absent.

```
knowledge_table(path?)   a routing table — what is here, and where to go next.
                         No argument = the list of areas. That is where every search starts.
knowledge_read(path)     one document, as written.

knowledge_overlay(op)    the working set for one question (a VRF) — only where the install keeps
                         overlays (ONTOLOGY_OVERLAYS). create · get · add · remove · close.
knowledge_write(...)     record what was done, into the `workspace` area, under today's date —
                         only where that area exists. Creating it is how the feature is turned on.
knowledge_circuit(op)    read another backbone for the length of this connection. open · list ·
                         close. Always offered: it needs nothing of this install to work.
```

So an install offers between three and five. `check/mcp-check.py` asserts the set against the same
conditions the server uses rather than a fixed count, because it once expected three while the server
offered five and was right to.

### Prompts

Clients that show MCP prompts get two, and a prompt is where a *person* starts something rather than
an agent reaching for it:

```
knowledge_start          the list of areas — the same text as `instructions`.
circuit                  open a circuit. Arguments: url, token, name — so a client can show
                         fields instead of asking somebody to compose a tool call.
```

In Claude Code this repository also carries `/circuit <url> <token> [name]` as a project command.

Where overlays exist, the `instructions` describe the flow in docs/OVERLAY.md: pick every row the
question belongs to, create the overlay with a reason for each, work from its one table, come back to
the list at most three times, close with what was used. Measured with Claude Code on 2026-09-11
against a copy of this install, asked *"an order shipped with SlowPost 7 business days ago still has
not arrived — what should I do?"* without naming RouteMind: it created an overlay on the delivery area
("order has not arrived; courier is SlowPost"), opened the SLA node from the overlay's table, read the
document, answered from it, and closed the overlay `answered` — with the document recorded as
`reached`, because the overlay named the area and the answer was one level down.

**The list of areas travels in two places, and the second one is the one that matters.**

- In `knowledge_table`'s description, refreshed whenever the client lists tools.
- In the server's **`instructions`**, sent at initialize.

The first was the original design, on the reasoning that a tool description is the one text every
client shows the model. **Measured in Claude Code, that is false**: it loads MCP tools lazily, so the
model starts with two tool names and no descriptions. Asked *"an order sent by SlowPost is six
business days late, what do I do?"* — without being told to use RouteMind — it never called the
server, grepped the repository, found nothing, and answered from general courier advice. The answer
was in an area whose condition read *"an order has not arrived"*.

With the areas in `instructions`, the same question in the same setup loaded the tools by itself,
skipped the area list because it had already seen it, and answered from the document in three calls.
So **you do not have to name RouteMind in the question** — as long as the question falls inside an
area whose `use_when` says so. That is one more reason `use_when` is the field that matters.

One limit: `instructions` are built at initialize, i.e. when the session starts. An area created
mid-session is in the tool description at the next tool listing, but not in the instructions until
the next session.

### Why the agent never builds an address

Every row prints the exact address that fetches it. This is the one rule worth enforcing in your own
prompt if you write one, because the failure is silent: assembled addresses worked for months, then
documents moved one level down and a consumer that built its own paths returned empty answers
without erroring.

### What "not found" means

Only the **list of areas** may be read as a claim that something does not exist. An area's own table
lists what that area holds, and says so at the bottom. An agent told otherwise will answer "there is
no such thing" from inside one area, having never looked at the other six.

---

## Paste

**Copy for an agent** on the map puts the same starting block on the clipboard, with a `GET` URL
instead of a tool call. For an agent that can fetch, that is enough to navigate. For one that cannot,
it is still a map of where to ask a person to look.

---

## Launch URL

For a console that takes a run: set `KNOWLEDGE_AGENT_URL` and the map grows a **▶ Start** button and
tick boxes. The areas someone picked ride along:

```
${KNOWLEDGE_AGENT_URL}?root=/v1/regions/alpha&root=/v1/nodes/beta
```

Several `root` parameters mean an overlay — one run over several areas at once. Your console decides
what to do with them; the contract is only that they are addresses this ontology printed.

With `KNOWLEDGE_AGENT_URL` empty, **the button and the tick boxes are not drawn at all**. A control
that does nothing teaches people that the feature does not work.

It is a URL a browser opens, so it must be reachable from the browser — not a container name.

---

## Writing, not just reading

The MCP server is **read-only on purpose**. Writes commit into a git repository and carry an actor,
and an agent writing unattended into the thing that steers it is a loop worth being deliberate about
rather than getting by default. The HTTP API is open if you decide otherwise: `web/app.py` lists
every route, and `check/write-paths.sh` exercises them.

---

## Checking it

```sh
./check/mcp-check.py          # the protocol, and an agent's walk from the areas to a document
```

The last part of that check is the one that matters: it navigates using nothing but addresses the
tables printed, which is exactly what an agent can do and no more.

To see the bytes, one request is enough — the reply carries the `instructions`, which is where the
area list travels:

```sh
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"0"}}}' \
  | python3 mcp/knowledge_mcp.py --api http://localhost:8080/api/knowledge
```

One consequence of that being sent at initialize: **`instructions` are built when the session
starts.** An area created mid-session reaches the tool description at the next tool listing, but not
the instructions until the next session.
