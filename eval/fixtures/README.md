# Continuity fixtures

A fixture is one subject, several documents about it over time, and the truth about which of them
is **operative now**. It tests a failure that routing accuracy cannot see: hop 0 picks the right area,
retrieval returns every relevant document, and the answer is still wrong because a superseded
decision was treated as evidence equal to the one that replaced it.

Fixtures are contributed. This page is the whole contract.

## The shape

```yaml
id: supplier-selection-x          # kebab-case, unique among fixtures
area: procurement                 # the area its documents join. Must exist in the corpus
subject: which supplier is approved for X
contributed_by: GovKM             # optional

documents:                        # what goes INTO the corpus
  - id: x-a-approved              # unique across the whole corpus; kebab-case
    date: 2025-03-01              # ISO. Also written into the body, as a person would
    kind: rule                    # from the corpus vocabulary — see below
    name: Supplier A approved for X
    one_liner: one sentence, no trailing full stop
    body: |
      # Supplier A approved for X
      Decided 1 March 2025. ...

truth:                            # what the SCORER knows. Never enters the corpus
  operative: x-b-approved         # the document that holds the current answer
  states:                         # one of: active · superseded · withdrawn
    x-a-approved: superseded
    x-b-approved: active
  supersedes:                     # newer -> [older]
    x-b-approved: [x-a-approved]

questions:
  - q: Which supplier is currently approved for X?
    answer: Supplier B
    operative: x-b-approved       # the document a correct answer rests on
    distractors: [x-a-approved]   # relevant, findable, and wrong as the current state
```

## The three rules

**1. Documents are plain.** They are written the way a person in that back office would have written
them, with the date in the text. They carry **no** state, no supersession pointer, nothing that says
"this one is current". The baseline implementation (`git tag baseline-pre-continuity`) has no such
field, and the fixture's first job is to measure that baseline honestly. A document that says "this
supersedes the March decision" in its prose is fine — people write that. A frontmatter field saying
so is not, because it is not something the baseline could have read.

**2. Truth never enters the corpus.** `truth:` and `questions:` are read by the scorer only. The same
rule the corpus strata follow: the answer sheet is never in the text that gets embedded.

**3. Every id is new.** Check against the corpus before choosing one. `check.py` does.

## Kinds

`topic` · `rule` · `procedure` · `form` · `table` · `case` · `system` · `role` · `deadline`.
A decision is usually a `rule`; an incident or a retrospective is a `case`.

## What is measured

Two things, kept apart — the distinction the fixture exists for:

| | Question | Stage |
|---|---|---|
| found | is the operative document in the top-k at all | 1 — no generation |
| operative | is it ranked **above** its distractors; and, with generation, does the answer rest on it | 1 for the rank, 2 for the answer |

A system can score perfectly on the first and fail the second. That is the finding.

## Running one

```sh
./eval/fixtures/check.py eval/fixtures/<name>.yaml     # shape, ids, kinds, area — before you send it
```

The scoring run belongs to the study (`eval/PREREGISTRATION.md`, Q5) and runs every fixture against
the baseline tag first. Results are preserved beside the fixture once they exist.

## Contributing

Add one file under `eval/fixtures/`, run `check.py`, open a pull request. Say in the description what
the history is designed to expose — a correction, a supersession, a moved responsibility — so the
result can be read against the intent.
