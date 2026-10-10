# Your ontology is a git repository

`data/repo` is the artefact. Not a database export, not a cache of one — the reviewed thing itself,
which is why every write through the screen or the API **commits** into it and undo is `git revert`.
It is also the only directory here worth backing up: `data/overlays` and `data/walks` are run
evidence that expires.

That makes editing it by hand not merely allowed but the point. A pull request against an ontology is
a pull request. One file in it is the exception: `regions.json` is **derived** from the areas' own
`.md` files, and it is also committed, which is the combination that lets it go stale.
Every write through the API regenerates it; an edit made in an editor does not.

Stale, it is not inert. `regions.json` is what hop 0 advertises, and `use_when` is the sentence an
agent reads to decide which area answers a question. A stale one routes on wording that is no longer
in the repository, and until 2026-09-13 nothing said so: `validate` compared which areas and which
nodes were listed, never the text. It does now, and it names the fields.

The service regenerates it at startup when that is the only thing wrong and the tree is clean, and
every write through the screen or the API regenerates it in the same transaction. To do it on demand:

```sh
docker compose exec ontology python3 /app/tidy.py /data/repo --fix   # regenerates, validates, commits
```

### Deleting an area by hand

`rm -rf regions/payroll` and a commit leave one thing behind: `regions.json` still listing the area.
The validator names it; the next write through the screen or the API regenerates it along with
whatever it writes, and so does the next start of the service. Adding an area directory by hand is the
same in reverse. Or on demand — `tidy.py` runs on the host if your Python has PyYAML, and in the
container always:

```sh
./ontology/tidy.py data/repo          # what is out of step. Changes nothing
./ontology/tidy.py data/repo --fix    # regenerates regions.json, validates, commits
```

(It used to leave dangling edges and a `CORE.md` row too. Neither file is read since 2026-10-07; one
still in an older repository is inert and can be deleted.)

`--fix` touches only those two, and goes through the same transaction as any other write — a dirty
tree is refused, the result is validated, anything that fails rolls the repository back, and what
succeeds is committed under its own message. An edge between two documents that both exist is
somebody's statement and is never removed, nor is a CORE row whose area is there. Deleting an area *through the
API* has always done all of this in one transaction — this is for the times you did it in an editor,
which is the workflow this file is about.


### A file that does not parse

An unclosed quote in a frontmatter, a `vocab.yaml` that is not YAML, a `regions.json` that is not
JSON. The file is left out and everything else is served; `/healthz`, the screen's **Show what
fails** and `validate` name it with its line:

```
regions/expense/travel-expense.md: the frontmatter does not parse (line 3: …) — fix it and commit,
or `git -C data/repo revert HEAD` if the last commit broke it
```

Writes are refused until it is fixed, because a document left out looks to every other rule like a
missing one. If the last commit broke it, `git -C data/repo revert HEAD` is the whole repair — the
service notices on its own. A broken `regions.json` is derived, so the service writes it again at its
next start.

## Backing up and restoring

`data/repo` is a git repository, so a backup is a clone or a copy of the directory. **Restore with the
service stopped**: the container holds the directory it was started with, and a directory swapped
underneath it is not seen (`/healthz` says `writable: false` with the reason).

```sh
docker compose stop ontology
rm -rf data/repo && cp -a /path/to/backup data/repo
docker compose start ontology
```

## Starting over

```sh
./ontology/reset.sh --empty      # no areas, the starter vocabulary
./ontology/reset.sh --example    # the example back office
```

One commit in the repository's own history, made only on a clean tree. The map as it was is tagged
first (`before-reset-<time>`) and the script prints how to bring it back:
`git -C data/repo reset --hard before-reset-…`. The running service picks it up without a restart.

---

## What validates it

Every write validates before it commits, so an ontology that came in through the API is already
checked. One that came in through an editor is checked at the next write, at boot, and whenever you
ask:

```sh
curl -s localhost:8080/api/knowledge/validate | python3 -m json.tool    # your port, from .env
```

`ok: false` names every rule that was broken, with the file and the field. The drift above is one of
those rules now.

---

Back to [the README](../README.md).
