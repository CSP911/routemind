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

### Claude Code

```sh
claude mcp add knowledge -- python3 /abs/path/to/knowledge/mcp/knowledge_mcp.py \
  --api http://localhost:8080/api/knowledge
```

**This repository ships one.** `.mcp.json` at the root registers the server with a path relative to
the repository, so opening the repo in Claude Code offers it and one approval is the whole setup.
Point `--api` elsewhere if RouteMind is not on this machine. `claude mcp list` shows whether it
registered; `/mcp` inside a session shows the tools it exposes.

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

```
knowledge_table(path?)   a routing table — what is here, and where to go next.
                         No argument = the list of areas. That is where every search starts.
knowledge_read(path)     one document, as written.
knowledge_overlay(op)    the working set for one question (a VRF) — only where the install keeps
                         overlays (ONTOLOGY_OVERLAYS). create · get · add · remove · close.
```

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
