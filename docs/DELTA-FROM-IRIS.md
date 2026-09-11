# What this copy changed, against IRIS's `docker/ontology/service/`

Forked 2026-09-11 and **this repository is canonical** (`docs/PROVENANCE.md`). Anyone arriving from
IRIS with work in progress needs this list: most of the ~900 changed lines are translation, and the
behaviour changes are these ten.

Regenerate the raw comparison with:

```sh
for f in ontology/service/*.py; do diff ~/iris_v1.0.1/docker/ontology/service/$(basename $f) $f; done
```

## Behaviour

| # | File | Change | Why |
|---|---|---|---|
| 1 | `write.py` | The CORE.md row is appended after the **separator** when there are no rows yet | A fresh ontology could never create its first area: no row meant no anchor, and no anchor meant no first row. **Every new IRIS install has this defect** |
| 2 | `server.py` | `X-Actor` is **percent-decoded** on receipt | HTTP headers are latin-1. A name that is not ASCII arrived mangled and silently became `web` on the commit |
| 3 | `server.py` | `/healthz` reports `llm`, `writable`, `uncommitted` | The screen has to know whether ids can be derived, and a dirty data repository makes the whole app read-only with nothing saying so |
| 4 | `server.py` | `POST /v1/suggest/use-when` | Drafts the one line an agent routes on, into an editable box. Never applied |
| 5 | `server.py` | `create_draft` / `apply_proposal` read `curator.draft_area` and `curator.draft_kind` from vocab | They were two literals naming one domain's area and one of its Korean kind names |
| 6 | `store.py` | `REGION_KEY` is **empty** and optional | It disagreed with `derive.region_label`: `orchestration` was `ORCH` in one and `ORCHESTRATION` in the other, so one area had two names — one reaching hop 0 and the CORE table, the other the routing table's `key` and the graph |
| 7 | `store.py` | `## Files` is written; `## Files` **and** `## 파일` are read | Format change that migrates itself as nodes are rewritten |
| 8 | `validate.py` | `_ref_exists` derives the key→directory table from the areas that exist | `REGION_DIR_OF` was a constant, so a reference into any area created afterwards was refused |
| 9 | `validate.py` | Edge rules come from `vocab.edge_rules`; the four Korean kind constants are gone | Compared against an area named `svn`, so in any other domain **three rules could never fire** while validation looked complete |
| 10 | `validate.py` | `learned`'s two rules come from `vocab.area_rules` | It is a role, not a name |
| 11 | `write.py` | `_resolve_kind` falls back to `vocab.default_kind` | Nothing reads a kind until `edge_rules` are declared, so the screen stopped asking |

## Data format

`## 파일` → `## Files` in written INDEX.md. Reading accepts both, so no migration pass is needed.

`vocab.yaml` gained four optional keys, all defaulting to off: `default_kind`, `edge_rules`,
`area_rules`, `curator.draft_area` / `curator.draft_kind`. See `seed/vocab.yaml`.

## Testing against real data

The seed here is empty on purpose, so `check/write-paths.sh` builds its own throwaway ontology. Work
that needs a populated tree — a data-model conversion, for instance — should keep IRIS's
`docker/ontology/data` as a fixture and point `ONTOLOGY_DATA` at a copy of it:

```sh
cp -r ~/iris_v1.0.1/docker/ontology/data /tmp/fixture && git -C /tmp/fixture status
ONTOLOGY_DATA=/tmp/fixture ONTOLOGY_PUBLISH=/tmp/pub PORT=8109 python3 ontology/service/server.py
```

That tree is still in the old format, which is the point: #7 above means this code reads it.
