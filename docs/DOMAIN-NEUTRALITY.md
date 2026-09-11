# Domain neutrality

This system was split out on the premise that it applies to any domain. That is now broadly true —
it was brought up empty and driven through domains it had never seen, end to end: areas, nodes,
documents, edges, and the routing table an agent is handed.

Four things that carried the original domain inside the code have been moved out into
`vocab.yaml`, and are recorded here because knowing they were there is the point. The fifth is still
open, and it is the important one.

## 1. Area labels were constants in three files — fixed

`store.REGION_KEY`, `validate.REGION_DIR_OF` and `validate_service.REGION_DIR` each held the same
table of the original domain's seven areas, written three times.

They are derived from the areas that actually exist now. While removing them, the two "key for this
area" functions turned out to **disagree**: `store.region_key("orchestration")` returned `ORCH` while
`derive.region_label` returned `ORCHESTRATION` — so one area had two names, one in hop 0 and the
CORE table, the other in the routing table's `key` and in the graph the map groups by. They agree.

`REGION_KEY` remains as an empty, optional table of hand-written abbreviations. It is not a registry:
an area not in it still works and gets the derived key.

## 2. Rules keyed on an area named `learned` — fixed

Drafts were allowed only in an area literally called `learned`, whose nodes had to hold pointers.
That is a role, not a name. Both are declared per area in `vocab.yaml` now, and default to off:

```yaml
area_rules:
  learned:
    drafts: true      # this area may hold status: draft
    pointers: true    # every node but the representative must hold pointers
```

The curator's promotion target was two more literals (`region: learned`, `kind: <a Korean kind name>`). It reads
`curator.draft_area` and `curator.draft_kind` from the vocabulary, and refuses with a sentence
naming them when they are absent — better than writing into an area that does not exist.

## 3. Edge rules branched on Korean kind names — fixed

Four Korean kind names were module constants, compared against an area named `svn`. In any other domain neither side ever matched, so three rules could not
fire and validation ran short while looking complete.

Edge rules are declared in `vocab.yaml`, and none ship by default:

```yaml
edge_rules:
- from_kind: task
  to_region: config-store
  error: "a task pointing at the store is a step, not structure"
```

Keys: `from_kind`, `to_kind`, `rel`, `from_region`, `to_region` (all optional, all ANDed) and
`error` (required).

## 4. The UI is English only

`static/i18n.js` used to carry a Korean dictionary plus a runtime machine that walked the DOM
rewriting Korean sentences into English — a phrase table, a pattern table, a skip selector, ~100 KB
of it. None of it had anything to translate here, so it is a lookup now (~19 KB).

To add a language: put a second dictionary in `dictionaries` under its code and call
`IRISI18N.setLanguage("<code>")`. A key with no entry falls back to English, so a half-finished
translation degrades to English rather than to blanks.

## 5. There is no vocabulary editor — and on the evidence, day one does not need one

`vocab.yaml` is the domain, and the only way to change it is to edit `data/repo/vocab.yaml` and
commit. That was written here as the largest remaining hole. Measured, it is not:

* **The screen never lets a person choose a kind that is not in the vocabulary.** With an LLM
  configured, Knowledge picks one from the list. Without one, the form offers a dropdown of the
  list, defaulting to its first entry. A "kind not in vocab" refusal is reachable by calling the
  API directly and not through the map.
* **The screen never creates an edge**, so no relation from the vocabulary is ever needed to make
  something.
* **In the default configuration nothing consumes `kind`.** It is not in any prompt and not in any
  table an agent is handed — confirmed by reading what the MCP server prints. `edge_rules` ships
  empty, so the single thing that reads a kind is the check that it is in the list.

A whole domain was built through the screen's own payloads without touching the vocabulary: an
area, two nodes, a document, and the routing table an agent receives.

So a vocabulary editor is a **later** feature, for when a domain outgrows seven kinds and starts
declaring `edge_rules` that make kinds mean something. What day one actually needs is that the
screen never asks a person for a word the system will reject — which it does not.

The one real edge — `kind` being a required field whose only default effect was to be rejected if
wrong — is gone (operator, 2026-09-11). The screen never asks. Knowledge chooses with an LLM where
there is one, `vocab.yaml`'s `default_kind` supplies it where there is not, and `kind_generated`
records that nobody picked it, so a domain that later declares `edge_rules` can find them.
