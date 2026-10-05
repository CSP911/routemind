# `supplier-selection-retrospective` — the continuity-discovery arm, for review before any run

**Status: unscored.** Proposed by GovKM on PR #1 (2026-10-01 14:58, 2026-10-02 11:56) as the next
experiment, with reachability isolated as the variable and the sealed result `e4cb893` left
untouched. This page records exactly what the new arm is and exactly what it shows the walker, so
the boundary can be reviewed and expectations preregistered before a single walk is made.

**The preregistered question, in GovKM's words:**

> Can a system that already possesses correct continuity metadata reliably locate the governing
> relationship from a user question, without encoding the answer into navigation text?

## What is held constant

Everything the sealed run used. The five documents, `truth:`, the four questions, the distractor
classifications, the scoring definition (`score_question`, read-order rank), the frozen map, the
walker (`bench/agent.py`, same model, same 30-turn ceiling), the frozen hop-0 sentences, the
ancestors' lines. `git diff 249dec7` on the fixture, the map and the review page is empty.

**The control is the existing `routing` arm, unchanged.** `Agent.walk()` gained an optional
`preface` argument; with it empty the first turn is byte-for-byte what it was, and `--dry-run`
asserts that on every question before printing anything.

## What the discovery arm adds — and nothing else

One block, placed between the question and hop 0 on the walker's first turn. The walker then sees
the same hop 0, the same tables, the same lines, and has to OPEN and READ exactly as the control
does. The block changes only whether it knows which table to open.

The mechanism is `ontology/service/resolve.py` — the resolver in front of hop 0 in the product,
not something written for this fixture. It matches names said in the question against the names
the map knows (node ids, node names, aliases), follows one hop along the map's own edges, and
reads what kind of thing is asked. From its answer the arm renders **where** each named thing is
recorded: the node, whether it is a table or a document, and the path to it from its area.

**Not rendered, by construction:** the node's line (the `current / replaced / history` sentence),
any date, any `use_when`, the names of nodes the question did not say. The block is checked
against a forbidden list — `current, replaced, history, in force, supersed, withdrawn, operative`
— and against the first forty characters of every map line, and the run refuses to start if any
appears. `score.py` records the block on every result as `exposed`, verbatim.

## The names it is allowed to know

`supplier-selection-retrospective.names.yaml`, four lines:

```yaml
sec-z-component-sourcing:        ["Z component", "component Z"]
z-supplier-e-approved:           ["Supplier E"]
z-supplier-f-approved:           ["Supplier F"]
z-supplier-e-performance-review: ["Supplier E"]
```

Without them nothing resolves: the documents are named "Supplier F approved for the Z component"
and a question says "Supplier F", and the resolver matches whole names. So these register the
**subjects** — the component and the two suppliers — as names of the nodes that are about them.

The test for each line, which is the review's to apply: it maps a name to the node *about* that
name. It does not say which registration is current, which was replaced, or any answer. "Supplier
E" names two nodes because two documents are about Supplier E; the mechanism reports both and says
nothing about which governs. Deliberately absent: any wording from the questions ("currently
approved", "delivery window", "new order"), anything on the November note or the inspection record.

## What the walker is shown — verbatim, from `--dry-run`

```
=== Q1: Which supplier is currently approved for the Z component?
Names in this question that the map knows, and where each is recorded:
  "Z component"  →  sec-z-component-sourcing (table) — in procurement, under vendor › sec-vendor-registration-cases  [alias]
Asking: what

=== Q2: Can I place a new order for Z with Supplier E?
Names in this question that the map knows, and where each is recorded:
  "Supplier E"  →  z-supplier-e-approved (document) — in procurement, under vendor › sec-vendor-registration-cases › sec-z-component-sourcing  [alias]
  "Supplier E"  →  z-supplier-e-performance-review (document) — in procurement, under vendor › sec-vendor-registration-cases › sec-z-component-sourcing  [alias]
Asking: whether (said "Can I")

=== Q3: What delivery window applies to a Z order placed today?
Names in this question that the map knows: none.
Asking: what

=== Q4: How did Supplier E perform on delivery while it was the source for Z?
Names in this question that the map knows, and where each is recorded:
  "Supplier E"  →  z-supplier-e-approved (document) — in procurement, under vendor › sec-vendor-registration-cases › sec-z-component-sourcing  [alias]
  "Supplier E"  →  z-supplier-e-performance-review (document) — in procurement, under vendor › sec-vendor-registration-cases › sec-z-component-sourcing  [alias]
Asking: how (said "How")
```

## Two things the dry run makes plain, stated before anyone predicts

**Q3 resolves nothing.** The question says "a Z order", and "Z" is one letter: the resolver drops
names under two characters, because a one-letter alias matches everything and resolves nothing.
The names file does not — cannot — register "Z". So on the question that exhausted the sealed
walk, the discovery arm is shown the control's first turn plus the line *"Names in this question
that the map knows: none."* That is not a defect to patch before the run; it is the boundary doing
what it says. Whether the arm behaves like the control on Q3 is one of the things the run measures.

**Q2 and Q4 are shown the same two documents.** Both say "Supplier E", and the mechanism cannot
tell a question about current orders from a question about past performance — it is not meant to.
Which of the two the walker reads first, and whether it reads the current registration at all on
Q2, is decided where it was decided in the control: at the map's lines.

## Not on this page

Predictions. GovKM asked to preregister expectations once the boundary is frozen, so none are
written here. The author's own are withheld on purpose.

## How it will be run, once

```
./eval/fixtures/score.py eval/fixtures/supplier-selection-retrospective.yaml --discovery \
    --out eval/runs/<date>-q5a-retrospective-discovery.json
```

One invocation scores `rag`, `rag+rerank`, `routing` (the control, walked afresh) and
`routing+discovery`. The control is walked again rather than copied from `e4cb893`, so the two
routing arms share a model, a day and a temperature; the sealed figures stay sealed beside it.
