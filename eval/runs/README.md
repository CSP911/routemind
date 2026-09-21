# Results

What is here, what it was measured on, and what it is not.

Every number in this directory belongs to a **corpus fingerprint** — a sha256 over the retrieval
pool. Results from different fingerprints are never pooled, averaged or compared, because twice this
week two arms ran on corpora that differed and nothing in the output said so. A file without a
fingerprint is not a result; it is a recollection.

```sh
BENCH_EXTRA_CORPUS=bench/corpus-hard ./bench/crowd.py fingerprint   # a84ac6cf463a1a6d
```

## Of record — fingerprint `a84ac6cf463a1a6d`, hop 0 `maintained`

| file | what it is | n |
|---|---|---|
| `2026-09-20b-retrieval-hard.json` | `rag` and `rag+rerank` over the 640 hard questions — census | 1280 |
| `2026-09-20b-retrieval-temporal.json` | the same two arms over the 60 temporal questions — census | 120 |
| `2026-09-20-walks.json` | `routing` and `routing+overlay` over the fixed sample of 50 | 102 |
| `2026-09-20-census.json` | `routing` over all 700 — one fresh headless session per question | *running* |
| `walks-census/*.md` | every census walk's report, verbatim | — |
| `2026-09-20-campaign.md` | the n=50 comparison written out, with what it does not show | — |

The two retrieval files carry `fingerprint_provenance`, because they were produced before `run.py`
stamped the fingerprint itself. The attribution is an inference and says so: the runs post-date the
13:31 corpus rebuild, and `bench/corpus-hard` has not been written since. `run.py` now stamps it at
the moment the numbers are produced, so no later file needs an inference.

**The census is a separate measurement from the sample, not a correction of it.** When it finishes it
goes in beside `2026-09-20-campaign.md`, not over it. If a census of 700 disagrees with a stratified
50, the disagreement is the finding and both numbers have to be readable.

## Void — kept because a discarded run is evidence

| file | why |
|---|---|
| `2026-09-20-walks-VOID-wrong-corpus.json` | `data/bench-repo` had not been rebuilt, so the walks ran on a corpus the retrieval arms were not using. Caught only because a walking agent twice flagged an implausible delegation limit. |
| `2026-09-20-walks-VOID-7dfd5538.json` | same hour, the superseded fingerprint. |

These are not results and must never be quoted as any. They are here because `bench/rmcli.py`'s
fingerprint guard and `bench/serve.py` exist *because of them*, and a check whose reason has been
deleted is a check someone will eventually remove.

## Earlier runs, under the old arm names

Files dated 09-18 and 09-19 use the arm names this study started with — `A1`, `A3`, `B1` — before
they were renamed for what they are (`routing`, `routing-scoped`, `rag`). They ran on earlier
corpora and earlier gold sets. **None of them carries a fingerprint**, and for most the corpus is
not recoverable: the 13:31 rebuild on 2026-09-20 overwrote all 353 extension documents, so what a
12:18 run saw no longer exists.

Read them as a record of what was tried, not as measurements to compare against the ones above. The
conclusions that survived are carried in prose, where a number without a corpus belongs:
`eval/COLLAPSE.md` for where retrieval breaks, `eval/DIFFICULTY.md` for how the corpus was hardened,
`eval/gold/AUDIT.md` for the answer keys that turned out wrong.

`superseded/` holds the rest — intermediate sweeps that were never tracked and are not being added
now, for the same reason: a number whose corpus cannot be identified cannot be checked by anyone,
and a pile of them beside results that *can* be checked makes the directory look like more evidence
than it holds. The ones already in version control stay; removing published results is a different
decision from declining to publish new ones, and not one taken while tidying.

## Reading a file

Retrieval runs: `results` is one row per question per arm — `arm`, `retrieval_hit`, `rank`, `mrr`,
`routing_hit`, `areas_looked`, and `top`, the ranked candidate list.

**One redaction, applied to every walk campaign.** The agents echoed their own command lines back,
and on the machine this ran on those lines began `PYTHONPATH=/private/tmp/<user>/<session>/pylib`.
That prefix is an invocation artefact carrying a username and a session id into a public repository,
so it is replaced by `$BENCH_PYLIB`. Each file records how many occurrences in `meta.redaction`.
Nothing else in any report was touched — not a word of an agent's reasoning, not a figure, not a
note. The census runs have none of this: the prefix was removed from the tool itself, so headless
walks never echoed a path at all.

Walk campaigns: `walks` is one row per question per arm — `hit`, `sources` (what the agent named),
`d_true`, `commands`, and `report`, **the agent's own words kept verbatim**. The reports are the
point. Two defects this week were found in the notes of walks that scored a clean hit, and neither
would have survived being summarised into a boolean.

## Working sets — what the overlay arm actually held

`overlays-census/` is one file per `routing+overlay` walk: the rows the agent put in its working set,
the reason it gave for each, what it removed and why, and what it said it used when it closed.
`overlays-sample50/` is the same for the earlier sample.

They are here because the arm's headline result is a negative — same hit rate as plain routing, 16%
more calls — and "it bought nothing" is a claim someone should be able to check rather than take.
These files are what it was holding while buying nothing. They are also the only place the *reasons*
survive: the walk report lists commands, the working set lists why each row was kept.

The store the service writes to (`data/bench-overlays/`) is not tracked — `/data/` is a repository in
its own right. These are copies taken at the end of the run.
