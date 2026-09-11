# Where this came from, and how it diverged

Split out of the Knowledge unit and the map screen of IRIS (`iris_v1.0.1`), 2026-09-11.

**This repository is the canonical source of the ontology service** (operator decision,
2026-09-11). IRIS takes from here. It does not flow the other way — once both copies are edited,
they are two products.

## What was taken

| Here | IRIS |
|---|---|
| `ontology/service/` | `docker/ontology/service/` (2,256 lines, verbatim) |
| `static/knowledge.*` | `static/knowledge.*` (verbatim, plus the changes below) |
| `static/{theme,iris_ui}.*` | same |
| `web/app.py` | `iris_web/runtime.py` lines 6804–7347 (35 Knowledge proxy routes) |

Dropped on the way: `docker/ontology/web/` (2D/3D graph viewers, referenced by nothing here).

## Fixed here — these should go upstream to IRIS

1. **A fresh ontology could not create its first area** (`ontology/service/write.py`).
   The `CORE.md` row is inserted after the last existing row, and an empty table has none, so no row
   could ever be first — a 500. It now falls back to the separator line. **Every new IRIS install
   has this defect; only an install that already has data hides it.**

2. **A non-ASCII name on a commit silently became `web`** (`ontology/service/server.py`,
   `web/app.py`). HTTP headers are latin-1 and the actor crosses two of them. `X-Actor` is
   percent-encoded on both hops and decoded on receipt. ASCII names are unchanged, so it is
   backward-compatible.

3. **`/healthz` reports `llm`** (`ontology/service/server.py`). The screen has to know whether this
   install can derive an id and a kind, or must ask for them.

## Removed here

- **All authentication.** IRIS backs it with PostgreSQL; this build has none (operator decision).
  The seam is `_require_admin` in `web/app.py` — putting a gate back is that one function.
- **The Pi coupling.** `▶ Start` no longer navigates to `/playbooks`; it goes to
  `KNOWLEDGE_AGENT_URL`, and with none set the button and the tick boxes are not drawn.
- **The second source for the service list.** IRIS reconciled ontology fragments against Pi's
  capability list. Here there is one source: the ontology.
- **i18n keys 602 → English only.**

## Added here

- `mcp/` — an MCP server, so Claude Code, Codex and other MCP clients can read the ontology directly
  instead of going through a web console. See `docs/AGENTS.md`.
- `install.sh`, `check/smoke.sh`, `check/screen-check.mjs`.

## Not done

`docs/DOMAIN-NEUTRALITY.md`: three area-name constants, the `learned` rules, Korean kind names used
as semantic constants in edge rules that consequently never fire, and — the real gap — **no editor
for `vocab.yaml`, which is the domain**.
