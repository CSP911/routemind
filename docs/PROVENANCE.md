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
   has this defect; only an install that already has data hides it.** (`CORE.md` has since been
   retired here; the defect is still IRIS's.)

2. **A non-ASCII name on a commit silently became `web`** (`ontology/service/server.py`,
   `web/app.py`). HTTP headers are latin-1 and the actor crosses two of them. `X-Actor` is
   percent-encoded on both hops and decoded on receipt. ASCII names are unchanged, so it is
   backward-compatible.

3. **`/healthz` reports `llm`** (`ontology/service/server.py`). The screen has to know whether this
   install can derive an id and a kind, or must ask for them.

## Removed here

- **IRIS's authentication.** IRIS backs it with PostgreSQL; this build does not. It consumes an
  identity instead of keeping one: `KNOWLEDGE_AUTH` is `open` (the default), `token` or `proxy` —
  [AUTH.md](AUTH.md).
- **The Pi coupling.** `▶ Start` and `KNOWLEDGE_AGENT_URL`, the publish step that copied a checkout
  for Pi to mount, the service fragments, and the curator's sleep and observations — all retired on
  2026-10-07, none of them with anything behind it here.
- **IRIS's 602 i18n keys.** The screen has its own dictionaries now — English, Korean, Japanese and
  Simplified Chinese ([I18N.md](I18N.md)).

## Added here

- `mcp/` — an MCP server, so Claude Code, Codex and other MCP clients can read the ontology directly
  instead of going through a web console. See `docs/AGENTS.md`.
- `install.sh`, `check/smoke.sh`, `check/screen-check.mjs`.

## Not done

**No editor for `vocab.yaml`, which is the domain** — and why, on the evidence, day one does not
need one: `docs/DOMAIN-NEUTRALITY.md`, which also records the domain constants that were taken out
of the code.
