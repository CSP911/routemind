# How old is this row

Every routing row an agent reads carries two times:

```
  KIND   ADDRESS                          AGE          WHY YOU WOULD PICK THIS ROW
  table  /v1/nodes/corp-card              18d / today  Corporate card — the caps, and what to do …
  file   /v1/nodes/qualified-list/body    18d / 18d    What qualifies as evidence, and the ceiling …
  table  /v1/peers/ix/…/regions/payroll   —            what this payslip line means · whether an …
```

    route      how long this path has been here
    document   when what it points at last moved
    —          not known here

## Why two

Because one cannot say both, and the pair is the whole signal.

A route laid down in 2023 whose document was rewritten last week is **current** — somebody is
maintaining it. The same route over a document that has not moved in three years is the one worth
asking about before quoting it. A single "age" collapses those into the same warning, and the first
one is most of a healthy map: a rule that has not needed changing is the most reliable row in the
table, not the least.

So the second number is the one that answers *"should I look for something newer"*, and the first
says whether this path is settled or was just laid down.

## What it is not

**It is not a supersession record.** Old does not mean wrong, and new does not mean right. An agent
that prefers the newest row will pick a draft over a rule that has held for a decade. What the column
supports is *asking* — "this has not moved since 2023, is there a later one" — not deciding.

The thing that actually settles which of two documents is current is a statement that one replaced
the other, written by whoever knows. That is not this.

**It is not maintained state.** Both numbers come from git — the most recent commit that added the
file, and the most recent that touched it. A field carrying them would be a second copy that drifts,
and a wrong date here is worse than no date: it is a reason to trust the wrong row.

**`—` is not "new".** It is *not known*, and the row it most often appears on is one that came across
a link, where the history belongs to the backbone that owns it. A blank cell would have read as a row
somehow outside time; the em dash is there so that a reader does not quietly prefer the row the
system knows least about.

## Cost

One pass over the log per commit, cached on the revision the store already tracks. Measured on the
shipped repository: 677 commits, 82 documents, 0.34s — fine once, far too slow per request, which is
why it is keyed on the revision and not computed per call.

A repository with no git history answers nothing rather than failing. A backbone whose ages are
unknown still routes correctly, and making git a dependency of reading a document would be the wrong
trade in the other direction.

`./check/age-check.py`.
