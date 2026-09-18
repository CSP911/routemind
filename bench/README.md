# bench — the tools the study runs on

The study is in [`eval/`](../eval/); this is what executes it. Scripts are versioned, everything they
generate is not: the corpus, the manifest, the embedding caches, the factor table and the logs are
all reproducible from what is here plus an API key.

| | |
|---|---|
| `spec.yaml` | 69 subject clusters — subject, ground covered, count, stratum, and the reason for the label. Written before anything was generated |
| `generate.py` | expands the spec into documents, resumable from the manifest |
| `restructure.py` | the tree: one section page per cluster, nothing over 25 children. Idempotent |
| `factors.py` | C, D and E per document — the document side of the difficulty scale |
| `coverage.py` | how specifically an area's description reaches each of its documents |
| `rows-check.py` | precondition P1: no two area descriptions are near-duplicates |
| `retrieve.py` | BM25 + dense + reciprocal rank fusion, and the OpenAI request helper |
| `rerank.py` | LLM reranking, blind to which area a candidate came from |
| `route.py` | the single-decision router: read hop 0, pick areas, stop |
| `agent.py` | the agent: walk the tree, open tables, read documents, go back |
| `run.py` | the arms, scored |
| `smoke.py` | retrieve + rerank end to end |

## Rebuilding from nothing

```sh
./bench/generate.py         # spec.yaml -> corpus/     (needs an LLM key)
./bench/restructure.py      # section pages and the tree
./bench/factors.py --csv > bench/factors.csv
./bench/run.py eval/gold/pilot.yaml
```

## Models

Pinned, and printed with every result, because a difficulty scale or a routing decision made by an
unnamed model cannot be compared with anything later.

| | | why |
|---|---|---|
| router / agent | `claude-opus-5` | the first run used a weaker model that invented row names — an instruction failure that would have been scored as a routing failure |
| reranker | `gpt-5` | a different vendor from the router on purpose; a reranker sharing the router's blind spots cannot correct for them |
| embeddings | `text-embedding-3-large` | also computes two difficulty factors. That overlap is a known limitation, measured: `eval/DIFFICULTY.md` |

Override with `ROUTER_MODEL`, `BENCH_RERANK_MODEL`, `EMBED_MODEL`, `FACTOR_EMBED_MODEL`.

The embedding cache is keyed by **model and** text. It was keyed by text alone, and a model-sensitivity
check came back 100% identical across two models — because the second was never called.
