# Who owns what

Two Claude Code sessions work this repository, the same two that work IRIS. The units carry over
from IRIS's own `OWNERSHIP.md`, because the boundaries are properties of the code and not of who is
typing.

| Unit | Owns here |
|---|---|
| **Knowledge** | `ontology/**`, `seed/**` — the API, the validator, the data model, the starting vocabulary |
| **Web / Platform** | `web/**`, `static/**`, `mcp/**`, `check/**`, `install.sh`, `docker-compose.yml`, `docs/**` |

Shared, owned by nobody: `README.md`, `.env.example`.

## Committing

One branch, two sessions, at the same time (operator, 2026-09-11). That works only if a commit picks
up exactly what its author changed, so:

- **Stage explicit paths. Never `git add -A`, `git add .`, or `git commit -a`.** The other session's
  work in progress lives in the working tree next to yours, and a sweep takes it. This is not
  hypothetical — `0048175` carries 117 lines of the Knowledge session's unfinished migration under
  the Web session's name, from exactly that.
- **Read `git status --porcelain` before staging**, and stage only paths your unit owns.
- **Never rewrite shared history.** No `--amend`, `reset`, or `rebase` of anything already committed:
  the other session may have built on it. If a commit came out wrong, say so and let its author
  decide — an ugly history is cheaper than a rewritten one under someone's feet.
- **Do not edit the other unit's file in place at all** — not even to reproduce something and put it
  back. Copy the repository and break the copy:

  ```sh
  cp -r . /tmp/probe && cd /tmp/probe          # break this, not the working tree
  ```

  "Put it back" is the trap, not the safeguard. A snapshot taken before you edit is only accurate
  until the other session saves, and restoring it then silently overwrites whatever they wrote in
  between — with no conflict, no error, and nothing in `git status` to show it, because the file was
  never committed. That happened here: an `entity_files()` that existed only in the working tree was
  lost to a `cp` restore, and was noticed only because its author looked for it. Restoring from git
  (`git checkout -- <path>`) has the same hole for the same reason.

## Crossing

The response shape is the seam, and it moves in two phases — the consumer stops depending on the old
shape first, and only then does the producer drop it. Two changes, not one, so each is separately
reversible:

1. **The consumer stops depending on the old shape.** The screen, the MCP server and the proxy keep
   working against both. Nothing breaks.
2. **The producer drops it**, once no consumer is left.

This is not theory here. The node/file merge (2026-09-11) ran exactly this way: `/v1/nodes/{id}/body`
opened while `/v1/nodes/{id}/files/{name}` stayed alive, the MCP reader stopped requiring `/files/`
in an address, and only then does the old address go.

`mcp/knowledge_mcp.py` and `static/knowledge.js` both **follow the `fetch` an entry carries** and
never assemble an address. That is what makes a phase-2 possible at all — and it is worth keeping
true, because the last time a consumer built its own paths, documents moved one level down and it
returned empty answers without erroring.
