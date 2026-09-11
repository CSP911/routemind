# Examples

One worked ontology, so that a fresh install has something to read before it has anything of its own.
`seed/` stays empty on purpose — what every install starts with is still an open question
(`docs/TODO.md`), and an example that ships as the default is no longer an example.

## back-office

The corporate-support desk of one fictional company: leave, expenses, purchasing, approvals, payroll.
Five areas, 79 entities, five levels deep, 30 relations, 37 documents.

Every amount and deadline in it is that company's own policy, **not the law** — where a real statute
sets something (retention, tax-free caps, insurance rates), the document names it.

What it is there to show:

- **Areas cut by where a question is headed, not by which team owns it.** One business trip splits
  three ways: how many days count is `ATTENDANCE`, how much is paid is `EXPENSE`, whether it is taxed
  is `PAYROLL`. That is what makes each `use_when` line worth reading before choosing.
- **A vocabulary that is the domain.** `vocab.yaml` carries nine kinds and ten relations that a
  back office actually uses, and two `edge_rules` that make a kind mean something — a form cannot be
  an authority, a system cannot approve anything. Both are refused at the write, with those words.
- **Depth that is real.** `Expenses → Corporate card → Card limits → Entertainment → the cap table`.
- **Questions that genuinely cross areas**, which is what an overlay (VRF) is for.

## Using it

Copy it over a **fresh** `data/repo` — before the first `docker compose up`, or over an install whose
ontology you do not mind losing:

```sh
mkdir -p data/repo && cp -r examples/back-office/. data/repo/
docker compose up -d          # the entrypoint git-inits and commits it on first boot
./check/smoke.sh
```

It is a starting point to edit or delete, not a schema. The first thing to change is `vocab.yaml`:
until it says the words your domain uses, your first node is refused.
