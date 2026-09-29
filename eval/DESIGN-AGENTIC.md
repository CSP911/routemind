# The baseline the study is missing — an agent that searches instead of walking

Written before any of it is built or run, in the discipline of `PREREGISTRATION.md`: the arm, what
is held fixed, the prediction and what would falsify it are fixed here. A result not described in
advance does not enter the report.

---

## 1. Why this arm, and why now

Every comparison so far is a **walking agent** against a **single-shot retriever**. `rag` makes one
embedding call; `routing` makes 6.7 tool calls and reads 14k–26k tokens (`eval/runs/2026-09-22-cost.md`).
The gap in the headline table is therefore two things at once:

1. **the table** — a human-written partition, descriptions and hierarchy
2. **the agency** — iterating, reading a document and deciding the next step from what it said

The study's claim is about (1). Nothing measured so far separates it from (2). The objection a
sceptic raises first is not "your retriever is weak", it is **"give the same model the same budget
and a search box, and see whether it still loses."** That agent is what people actually deploy now,
and it is the sceptic's build in the sense `run.py` already uses the phrase.

So the arm is: **same model, same harness, same questions, same report, same scoring — the table
replaced by search tools over the same corpus.** Only the thing the study claims credit for is removed.

---

## 2. The arm

**`search`** — a fresh headless agent per question, whose only command is `./bench/searchcli.py`:

    ./bench/searchcli.py search "<query>"     top 10 by the hybrid retriever, over the whole corpus
    ./bench/searchcli.py grep "<pattern>"     lines matching a regex, across every document, max 50
    ./bench/searchcli.py read <address>       one document, as written

| command | returns | why this and not more |
|---|---|---|
| `search` | 10 rows: `address — name` and the first 160 characters of the body | the identical `Hybrid.search` the `rag` arm uses. A second retriever would make the arm a comparison of retrievers |
| `grep` | `address: line`, case-insensitive, 50 lines, then a count of what was cut | what a coding agent does first. On a corpus of codes (`G1`, `B1`, `S1`) it is the strongest tool a sceptic has, so leaving it out would hand the result to routing |
| `read` | the document text, clipped at `READ_CLIP` = 6000 | the same clip `agent.py` and the real server use |

Addresses are printed as `/v1/nodes/<id>/body`, the form the routing arm prints, so
`walkscore.py` scores both with the same regex and nothing downstream has to know which arm it is.

**One ablation, `search-only`**: the same arm without `grep`. It says how much of the result is
lexical matching on codes, which is a property of this corpus rather than of agentic search.

### What the search agent never sees

| withheld | because |
|---|---|
| the five `use_when` sentences | they **are** the table. `run.py` already keeps them out of the index for the same reason |
| section pages (`manifest[id].section`) | signposts the study added for the tree. They are out of the `rag` pool; they stay out of this one |
| `parent`, the tree, the table views | the hierarchy is one of the three things under test |
| the frontmatter `one_liner` as a separate field | it is part of the indexed text already (`name. one_liner\n\nbody`), exactly as `rag` indexes it. Printing it again in a result line would give search a second look at routing's descriptions |

### What it does see that routing also sees

Document ids in addresses. They are descriptive (`hard-perdiem-row-grade-g1-band-b1-stay-s1`), and
that is a leak of the code structure to **both** arms equally, since the routing arm's tables print
the same ids. Not fixed here; recorded, because anonymising ids would change the routing arm too and
invalidate the existing census.

---

## 3. Held identical — and how, not just that

| held | how |
|---|---|
| corpus text | `searchcli.py` builds from `run.corpus()`, the function the `rag` arm uses. It computes run.py's fingerprint at start-up and refuses to answer if it differs from `BENCH_FINGERPRINT`, which the census sets from the retrieval run being compared against |
| retriever | `retrieve.Hybrid`, same BM25 constants, same embedding model and cache |
| model | the model the routing census ran on (`claude -p --model sonnet`, recorded in `2026-09-22-cost.md` as claude-sonnet-5). Pinned by the census script, printed in the campaign file |
| turn ceiling | `--max-turns 40`, as `walkcensus.sh` |
| prompt | `walkprompt.py --arm search`. The template is the routing one with **only the command block swapped**; the question, the date, the report format and the "say not found" line are the same bytes. Diffable, and the diff is committed with the first run |
| isolation | one question, one process, `--allowed-tools "Bash(./bench/searchcli.py:*)" "Write"`. No file reads, so the corpus on disk is as invisible as it is to a walker |
| scoring | `walkscore.py`, unchanged: addresses from the **Source** section against `D_true` and `D_alt`, `needs: all` honoured |
| gold | `hard.yaml` (640) + `hard-temporal.yaml` (60) = the same 700 |
| hop 0 policy | not applicable — but the routing numbers compared against are named: `BENCH_USE_WHEN=maintained`, the census default |

---

## 4. What is recorded

Everything `walkscore.py record` already keeps — the report verbatim, sources, hit, command count — plus:

| field | from | why |
|---|---|---|
| `tokens_in/out/cache`, `cost_usd`, `duration_ms` | `claude -p --output-format json`, written beside the report as `walk-<id>-search.meta.json` | the routing cost figures are n=5. This arm gets them for every walk, and the routing census should be re-run the same way for a like-for-like cost column (§7) |
| `surfaced` | `searchcli.py` appends every returned address to a per-question log | the analogue of `routing-scoped`: did a `D_true` document ever appear in a result the agent saw? Separates **never found** from **found and not chosen** — two different failures with two different fixes |
| `commands` by verb | the Commands section | how many searches, greps and reads a hit took |

---

## 5. Prediction — written down before a single walk

**The honest prior is that this arm closes most of the gap.** The corpus was built so that one-shot
retrieval fails, and the mechanism of that failure is one an iterating agent can route around:

- **indirect**: every answer row says *"see the legends if you are not sure which values apply"*,
  and the legends are ordinary retrievable documents. `search "junior analyst grade"` should surface
  `hard-perdiem-legend-grade`; it maps the person's words to `G1`; then `grep "grade G1, band B1,
  stay S1"` lands on the row. Three to five calls — about what a walk spends.
- **stale**: every current row names its predecessor and the revision legend in its last line. An
  agent that reads the current row is handed the address of the old one.

So the prediction is not "routing wins by 0.9". It is:

| | prediction for `search` hit | routing (measured) |
|---|---|---|
| direct | ≥ 0.95 | 1.000 |
| indirect | 0.70 – 0.95 | 1.000 |
| stale / temporal | 0.60 – 0.90 | 1.000 |
| calls per question | comparable to routing, within ±30% | 6.7 |

**What would make each reading true, fixed now:**

| outcome | reading |
|---|---|
| `search` indirect or stale **< 0.70** | the table carries weight an iterating agent cannot recover. The headline claim holds against the build that matters, and the README can say so |
| `search` within **0.05** of routing on every lever | the gain in the headline table was agency, not the table. RouteMind's case moves to **cost, latency, predictability and auditability** — and §7's cost column decides whether it has one |
| `search` accuracy equal, **cost or variance clearly higher** (≥ 1.5× calls, or p95 turns at the ceiling) | the table is a cost device: it buys the same answer in fewer, more predictable steps. A real claim, and a different one from the one the README makes now |
| `search-only` ≪ `search` | the arm's strength was `grep` on codes — a property of this corpus. Report it as such, and say plainly that a corpus without literal codes would put `search` nearer `search-only` |

The threshold for "within" is fixed at **0.05 absolute**, and differences are tested per lever with
a **paired McNemar test** over the same questions (both arms answered all 700).

### The noise floor

The question set is a census, but an agent is not deterministic, so "no sampling error" is true of
the questions and not of the walks. Before comparing, **re-walk a fixed 100** — drawn once, stratified by
lever and family, and committed as `eval/gold/noise-100.yaml` before either arm runs — **twice in
each arm**. The disagreement rate between a run and its
own repeat is the floor; a between-arm difference smaller than it is not reported as a difference.

---

## 6. Where this could go wrong, and the check for each

| risk | check |
|---|---|
| `searchcli.py` indexes something `rag` does not, or the reverse | the fingerprint refusal (§3), and a smoke test asserting `searchcli.py search q` equals `Hybrid(corpus()).search(q)[:10]` for five queries |
| the agent answers from memory of the corpus's shape | the same guard as routing: a fresh process, no repository access. A report whose Source names no address is scored as a miss, as it is now |
| `grep` is too strong because the ids are descriptive | `grep` searches **bodies**, not ids. Recorded as a known asymmetry if it turns out ids are what hits |
| embedding calls under load fail, and a failed search reads as "nothing found" | `searchcli.py` exits non-zero with the HTTP error on stderr, never an empty result |
| one start-up per call makes each walk slow (loading ~1,126 cached vectors) | measure one cold call first. Over 2 s, run `searchcli.py serve` once and let the CLI be a thin client on `127.0.0.1` — the pattern `serve.py` already uses for the ontology |
| a search arm that quietly beats routing because the prompt tells it more | the prompt diff (§3) is committed with the first result |

---

## 7. What gets built — files, in order

| step | file | change |
|---|---|---|
| 1 | `bench/searchcli.py` | new. `search` / `grep` / `read` over `run.corpus()`; fingerprint check; `surfaced` log under `BENCH_SURFACED`; `serve` mode if §6 says it is needed |
| 2 | `bench/searchcheck.py` | new. The five-query equality check against `Hybrid`, plus: section pages and `use_when` text never appear in any output |
| 3 | `bench/walkprompt.py` | `--arm routing|routing+overlay|search|search-only`. `--overlay` kept as an alias. The command block is the only thing that varies |
| 4 | `bench/walkcensus.sh` | `ARM=search*` → suffix `-search`, allowed tool `Bash(./bench/searchcli.py:*)`, the served-ontology fingerprint check replaced by the searchcli one, and `--output-format json > …meta.json` instead of `>/dev/null` |
| 5 | `bench/walkscore.py` | `--arm` choices gain `search`, `search-only`; `record` reads the `.meta.json` and `surfaced` log when present; `report` prints cost and `surfaced` columns |
| 6 | — | smoke: `hard-smoke.yaml`, both arms, by hand; read every report. Fix the harness, not the numbers |
| 7 | — | noise floor (§5): 100 × 2 × {`routing`, `search`} |
| 8 | — | census: 700 × {`search`, `search-only`}, and 700 × `routing` again **with** `--output-format json` so the cost column is measured on both sides rather than on five walks |

### Budget

At the measured $0.12–0.28 a walk: the census is 2,100 walks ≈ **$250–600**, the noise floor 400
walks ≈ $50–110, the smoke a few dollars. Step 8's routing re-run is the most expensive line and the
one most worth paying for: without it the cost comparison is 700 measured walks against 5.

---

## 8. What the README says afterwards

The table gains a column, whatever it shows:

    | | plain RAG | + reranker | agentic search | RouteMind |

and the sentence under it changes to match §5's reading. If the column is close to RouteMind's, the
README says the gain was agency and states the cost comparison instead. That sentence is the reason
the arm is worth running: it is the only result in the study that can tell the table apart from the
agent reading it.
