# Probe records

Measurements that cost money to make, kept where the study's records live rather than in `bench/`,
which is ignored. The working copies in `bench/` are what the tools read and write; these are the
copies that survive.

| | |
|---|---|
| `2026-09-19-lexical-sweep-questions.json` | 368 questions over 92 documents, four wordings each, written by `gpt-5.2` from `bench/probe.py` |
| `2026-09-19-lexical-sweep-fusion.json` | all 368 measured on hybrid fusion — the free half |
| `2026-09-19-lexical-sweep-b1-partial.json` | 100 of them measured on B1 proper, reranked by `gpt-5`. **Partial**: the balance ran out at 100 |
| `2026-09-19-lever-questions.json` | 120 questions for the `near` and `two` levers. Written, never measured |

What they say is in `../2026-09-19-break-search.md`. The short version: B1 equals fusion recall@20 to
the second decimal, so the reranker recovers exactly what fusion puts in its top 20 — and a
paraphrase destroys BM25 (recall@20 0.13) while barely touching the dense side (0.95).
