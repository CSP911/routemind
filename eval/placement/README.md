# Placement gap — where a person's routing table and `knowledge_place`'s part ways

`knowledge_place` builds a routing table the way a question is answered: it walks hop 0, follows the
rows whose sentences share words with the document, and places it where the walk stops; then it
walks back up and widens any ancestor whose line does not already say such a thing, stopping at the
first that does. A person places a document where a **reader** would look for it, and decides what
to advertise by what a reader needs to be told. Those two procedures agree often enough to be
dangerous — a table that is right in the easy cases and quietly wrong in the hard ones looks like a
good table until somebody asks a hard question.

This set exists to make the disagreement **large and nameable**. Every document here was written to
sit in one of eight classes where the two procedures are predicted to differ, and the result is
reported per class, so the finding is "the tool is wrong *here*, in *this way*" rather than one
agreement percentage.

## The question

> On documents a back office actually produces, where does a routing table built by walking the
> table differ from one built by a person — in **placement**, and in **what is advertised** — and
> which kinds of document produce the difference?

## The classes

| class | what the document is | why the two procedures should differ |
|---|---|---|
| `vocab-miss` | about something no line on the way to its place mentions — parking, toner, condolence money | the walk sees no shared word anywhere and either places it at hop 0 (asks for a new area) or follows a stray match; a person knows it is a small purchase, a trip cost, an expense |
| `false-friend` | shares strong words with the **wrong** area's sentence — "approval chain for a leave request", "payslip line for a lost card fee" | the walk follows the words into the wrong area; a person follows the subject |
| `cross-cutting` | belongs at a join between areas — a cancelled trip's leave, fare and allowance | the walk counts words and picks the area with more; a person places it at the handover node that exists for exactly this |
| `supersession` | a **new version** of a rule that already has a page — next year's domestic rates, a revised card limit | both put it beside the old page; but a person **changes the parent's line** to say which is current, and the tool's propagation rule stops because the parent "already covers" rates — the line is widened by nothing. The gap is in `advertise`, not `parent` |
| `depth` | belongs three or four levels down, under a section index — a specific overseas-trip exchange-rate case | the walk stops at the first row that shares a word, which is usually the shallow one; a person goes to the case section |
| `generic` | named like a signpost — "Checklist", "Who to call", "Overview" | the words match everywhere or nowhere |
| `korean` | written in Korean against an English map | no Hangul token matches an English line; this is the real install's situation and the one the resolver was built for |
| `none` | genuinely new — a fire-drill schedule, bicycle parking | **the control.** A person says "new area"; the walk should say the same (every row shares nothing). Agreement is expected and its absence would be a finding of its own |

## Gold — who decides what "right" is, and why it is the same mind that built the tool

`documents.yaml` carries a `human:` block per document — the area, the parent node, and the
ancestors whose lines should be widened (`advertise`). **Every one was written by the model that
also wrote `knowledge_place`**, and the field says so: `gold: model`. That is the design, not a
shortcut. The question is whether the *procedure* — walking the table on shared words — reaches a
different table from the *judgement* of the mind that wrote the procedure. Authorship is held
constant on both sides, so a gap cannot be explained by two people disagreeing about a back office;
it can only be the walk and the judgement parting ways. If they do not part, that is the finding.

The placements are judgements about where a reader would look, made with the whole tree in view
and no word-matching. A person who disagrees with one should change it and say so in `note`; the
harness reports `gold: model` and `gold: confirmed` rows separately.

**Predictions, written before the run.** The two should part most on `supersession` (same parent,
different `advertise`: the walk stops because the parent already covers "rates", the judgement
widens the line to say which table is current) and on `depth` (the walk stops at the first row that
shares a word, shallow). They should part least on `none` (both say new area) and may agree on
`false-friend` less often than the walk's confidence suggests. `korean` should be all NXDOMAIN for
the walk and all placed for the judgement.

The host corpus is `bench/corpus` — 860 nodes, five areas, depth up to five — copied fresh for every
run and never written to. Each document is placed against the pristine corpus, so trials are
independent and the order of the file carries no information.

## What is measured

Per document, from the walk the tool takes and the propagation it proposes:

| field | what |
|---|---|
| `tool.parent`, `tool.area` | where the walk stopped |
| `same_area`, `same_parent` | agreement with the person |
| `distance` | hops between the two parents through their lowest common ancestor — 0 is agreement, 1 is a sibling or a level, large is a different area |
| `depth_delta` | tool depth minus human depth — negative is shallow placement |
| `nxdomain` | the walk found no row at hop 0 and asked for a new area |
| `advertise_match` | the set of ancestors the tool would widen equals the set the person would |

Reported per class and overall. The `none` class is reported as agreement expected; every other
class as disagreement expected, with the kind of disagreement predicted above.

## The driver

The walk is driven **by the tool's own evidence column, literally**: at each table the row with the
most shared words is opened; a tie goes to the first row; when no row shares a word the document is
placed where the walk stands. No model. This is the floor — what the tool's evidence says on its own
— and it is the right first measurement because it is reproducible to the byte. An agent reading the
same table with the same evidence is the realistic driver and is the obvious second run (`--llm`,
not yet built); it will do better than the floor on some classes and the difference is itself a
number worth having.

## Running

```sh
PYTHONPATH=<pylib> ./eval/placement/gap.py                      # table by class
PYTHONPATH=<pylib> ./eval/placement/gap.py --out eval/runs/<date>-placement-gap.json
```

Starts an ontology on a temporary copy of `bench/corpus`, drives `POST /v1/place` hop by hop for
every document, writes nothing to the corpus, and removes the copy. Needs the vendored pyyaml on the
host (see `check/all.sh`).
