# Domain neutrality

This system was split out on the premise that it applies to any domain. That is now broadly true —
it was brought up empty and driven through domains it had never seen, end to end: areas, nodes,
documents, and the routing table an agent is handed.

Four things that carried the original domain inside the code have been taken out of it — two of
them later retired along with the feature they served — and are recorded here because knowing they
were there is the point. The fifth, a vocabulary editor, looked like the important open one; on the
evidence, day one does not need it.

## 1. Area labels were constants in three files — fixed

`store.REGION_KEY`, `validate.REGION_DIR_OF` and `validate_service.REGION_DIR` each held the same
table of the original domain's seven areas, written three times.

They are derived from the areas that actually exist now. While removing them, the two "key for this
area" functions turned out to **disagree**: `store.region_key("orchestration")` returned `ORCH` while
`derive.region_label` returned `ORCHESTRATION` — so one area had two names, one in hop 0 and the
CORE table (since retired), the other in the routing table's `key` and in the graph the map groups by. They agree.

`REGION_KEY` remains as an empty, optional table of hand-written abbreviations. It is not a registry:
an area not in it still works and gets the derived key.

## 2. Rules keyed on an area named `learned` — fixed, then retired

Drafts were allowed only in an area literally called `learned`, whose nodes had to hold pointers,
and the curator's promotion target was two more literals. That was a role, not a name, so it moved
into `vocab.yaml` as `area_rules` and `curator.draft_*` — and on 2026-10-07 both were retired with
the curator's sleep that wrote the drafts. Still in a vocabulary, `area_rules` is ignored; a draft
can only be found in an older repository now, and is allowed anywhere.

## 3. Edge rules branched on Korean kind names — fixed, then retired

Four Korean kind names were module constants, compared against an area named `svn`. In any other
domain neither side ever matched, so three rules could not fire and validation ran short while
looking complete. They moved into `vocab.yaml` as `edge_rules` — and on 2026-10-07 edges were
retired altogether, with `relations` and `edge_rules`: no agent was shown an edge and the map drew
none. Still in a vocabulary, they are ignored.

## 4. The UI's language is a dictionary, not code

`static/i18n.js` used to carry a Korean dictionary plus a runtime machine that walked the DOM
rewriting Korean sentences into English — a phrase table, a pattern table, a skip selector, ~100 KB
of it. It is a lookup now: the machinery in `static/i18n.js`, and one dictionary per language in
`static/i18n/<code>.js` — English, Korean, Japanese and Simplified Chinese. A key with no entry
falls back to English, so a half-finished translation degrades to English rather than to blanks.
Adding a language, and what is deliberately not translated: [I18N.md](I18N.md).

## 5. There is no vocabulary editor — and on the evidence, day one does not need one

`vocab.yaml` is the domain, and the only way to change it is to edit `data/repo/vocab.yaml` and
commit. That was written here as the largest remaining hole. Measured, it is not:

* **The screen never asks a person for a kind.** With an LLM configured, RouteMind picks one from
  the list; without one, `vocab.yaml`'s `default_kind` supplies it (below). A "kind not in vocab"
  refusal is reachable by calling the API directly and not through the map.
* **A kind matters in two places:** `export: no` on a kind keeps that sort of thing from crossing a
  circuit, and `knowledge_place`'s description lists the kinds with their `desc`, so an agent
  placing a document can choose one. It is not in hop 0 or any routing table an agent is handed —
  confirmed by reading what the MCP server prints.

A whole domain was built through the screen's own payloads without touching the vocabulary: an
area, two nodes, a document, and the routing table an agent receives.

So a vocabulary editor is a **later** feature, for when a domain outgrows the
nine kinds the example ships with. What day one actually needs is that the
screen never asks a person for a word the system will reject — which it does not.

The one real edge — `kind` being a required field whose only default effect was to be rejected if
wrong — is gone (operator, 2026-09-11). The screen never asks. RouteMind chooses with an LLM where
there is one, `vocab.yaml`'s `default_kind` supplies it where there is not, and `kind_generated`
records that nobody picked it, so a domain that relies on `export: no` can find them.
