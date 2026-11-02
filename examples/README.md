# Examples

One worked ontology, so that a fresh install has something to read before it has anything of its own.
`seed/` stays empty on purpose — what every install starts with is still an open question
(`docs/TODO.md`), and an example that ships as the default is no longer an example.

## back-office

The corporate-support desk of one fictional company: leave, expenses, purchasing, approvals, payroll.
Five areas, 79 entities, five levels deep. **Every entity carries a document** —
until 2026-09-14, 42 of them were an address and a routing line with nothing written behind them,
which made the example good at showing the shape of an ontology and poor at showing what it is for.

Every amount and deadline in it is that company's own policy, **not the law** — where a real statute
sets something (retention, tax-free caps, insurance rates), the document names it.

What it is there to show:

- **Areas cut by where a question is headed, not by which team owns it.** One business trip splits
  three ways: how many days count is `ATTENDANCE`, how much is paid is `EXPENSE`, whether it is taxed
  is `PAYROLL`. That is what makes each `use_when` line worth reading before choosing.
- **A vocabulary that is the domain.** `vocab.yaml` carries the nine kinds a back office actually
  uses, each with a one-line `desc` — what an agent placing a document is shown when it chooses one.
  A kind outside the list is refused at the write.
- **Depth that is real.** `Expenses → Corporate card → Card limits → Entertainment → the cap table`.
- **Questions that genuinely cross areas**, which is what an overlay (VRF) is for.

## Using it

On a first install, `./install.sh` asks whether to start from it — or `./install.sh --example`.

By hand, over a **fresh** `data/repo`, before the first `docker compose up` — after the `.env` lines
in **[docs/INSTALL.md](../docs/INSTALL.md)**, "Without install.sh", which give this checkout its own
compose name, image tag and circuit key:

```sh
mkdir -p data/repo && cp -r examples/back-office/. data/repo/
docker compose up -d --build  # the entrypoint git-inits and commits it on first boot
./check/smoke.sh              # checks the install on .env's WEB_PORT
```

Without those lines compose names the install after its directory and tags its images `0.1.0` — names
another RouteMind on this machine may already have, whose containers `up` would then replace. Where
one exists, `./install.sh --example` is the safer way: it refuses rather than take another install over.

Over an install that has already booted, use the reset — it replaces the map rather than copying
over it (a copy *merges*: your own areas stay beside the example's, with the example's `vocab.yaml`),
and tags the map it replaces so it can be brought back:

```sh
./ontology/reset.sh --example      # or --empty for a map with no areas
```

It is a starting point to edit or delete, not a schema. The first thing to change is `vocab.yaml`:
its kinds are a back office's, and yours are probably different.
