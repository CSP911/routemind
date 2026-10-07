# Your ontology is a git repository

`data/repo` is the artefact. Not a database export, not a cache of one — the reviewed thing itself,
which is why every write through the screen or the API **commits** into it and undo is `git revert`.
It is also the only directory here worth backing up: `data/overlays` and `data/walks` are run
evidence that expires.

That makes editing it by hand not merely allowed but the point. A pull request against an ontology is
a pull request. One file in it is the exception.

`data/repo` is meant to be edited by hand — it is the reviewed artefact, and a pull request against it
is the point. One file in it is not: `regions.json` is **derived** from the areas' own `.md` files and
from the table in `CORE.md`, and it is also committed, which is the combination that lets it go stale.
Every write through the API regenerates it; an edit made in an editor does not.

Stale, it is not inert. `regions.json` is what hop 0 advertises, and `use_when` is the sentence an
agent reads to decide which area answers a question. A stale one routes on wording that is no longer
in the repository, and until 2026-09-13 nothing said so: `validate` compared which areas and which
nodes were listed, never the text. It does now, and it names the fields.

To regenerate after editing by hand, from the checkout:

```sh
docker compose exec ontology python3 -c \
  "import pathlib; from service.store import Store; from service.derive import regenerate; \
   print(regenerate(Store(pathlib.Path('/data/repo'))) or 'already in sync')"
```

then commit what it changed. Or make any write through the screen — that regenerates, validates,
commits in one transaction, which is what the API is for.

### Deleting an area by hand

`rm -rf regions/payroll` leaves two things behind, and only one of them is loud:

- **edges whose ends are gone.** The validator names them, so every write is refused until they go.
- **the CORE.md row for that area.** CORE.md is carried *whole* into every prompt and its table is
  where each area's description at hop 0 comes from — so the row goes on advertising something that
  is not there. It was silent until 2026-09-30; it is an error now.

```sh
./ontology/tidy.py data/repo          # what is left over. Changes nothing
./ontology/tidy.py data/repo --fix    # removes exactly that, and regenerates
```

`--fix` touches only those two, and goes through the same transaction as any other write — a dirty
tree is refused, the result is validated, anything that fails rolls the repository back, and what
succeeds is committed under its own message. An edge between two documents that both exist is
somebody's statement and is never removed, nor is a CORE row whose area is there. Deleting an area *through the
API* has always done all of this in one transaction — this is for the times you did it in an editor,
which is the workflow this file is about.


---

## What validates it

Every write validates before it commits, so an ontology that came in through the API is already
checked. One that came in through an editor is checked at the next write, at boot, and whenever you
ask:

```sh
curl -s localhost:8080/api/knowledge/validate | python3 -m json.tool
```

`ok: false` names every rule that was broken, with the file and the field. The drift above is one of
those rules now.

---

Back to [the README](../README.md).
