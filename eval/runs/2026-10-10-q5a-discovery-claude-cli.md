# Q5a discovery boundary — exploratory run with a `claude -p` walker (2026-10-10)

**Status: exploratory only.** GovKM selected option (b) on PR #1 (2026-10-09): this run is preserved as
a separate exploratory observation. It is **not** the authorized scored execution of the frozen
discovery fixture. A run under the approved configuration (`claude-opus-5` through the Anthropic API)
can be authorized separately once that configuration is available; because these outcomes are now
known, that run must be identified as **non-blind**.

**Not a claim about the shipped product.** The discovery mechanism tested here is the resolver on this
branch (`ontology/service/resolve.py`, `fixture/no-supersession-sentence`). It was removed from
RouteMind's main branch on 2026-10-07. The outcome below says nothing about what the product on main
currently does.

## Files

| file | what it is |
|---|---|
| `2026-10-10-q5a-discovery-claude-cli.json` | the complete raw record as `score.py` wrote it: every arm and question, the discovery block exposed to the walker verbatim (`discovery.exposed`), each walk's turn-by-turn log (`log`), documents read in order (`read`), opens, returns, turns, and usage |
| `2026-10-10-q5a-discovery-claude-cli.log` | the console output of the same invocation, including the aggregate lines |
| `2026-10-10-q5a-discovery-claude-cli.wrapper.py` | the substitution wrapper — the only code that differs from the approved configuration |

Nothing frozen was changed: not the fixture, the authority relationships, the map, the names file,
the scoring semantics, `bench/agent.py`, or the sealed result `e4cb893`.

## Model and invocation

- **Walker model:** `claude -p --model opus`, which resolved to `claude-opus-5-5` at run time (from the
  CLI's `modelUsage`). The approved model is `claude-opus-5` through the API.
- **Session isolation:** a fresh `claude -p` per turn with `--tools ""`, `--strict-mcp-config`,
  `--setting-sources ""`, `--disable-slash-commands`, `--no-session-persistence`, an empty working
  directory (no CLAUDE.md), and `--system-prompt` set to `bench/agent.py`'s own system prompt in place
  of Claude Code's.
- **Harness:** the frozen harness at `aa35c7d`, run unchanged through the wrapper:

  ```sh
  python3 2026-10-10-q5a-discovery-claude-cli.wrapper.py <this worktree> \
      eval/fixtures/supplier-selection-retrospective.yaml --discovery \
      --out eval/runs/2026-10-10-q5a-discovery-claude-cli.json
  ```

  with the install's environment loaded only for the embedding key the `rag` arms use. All four arms
  ran in one invocation; the control was walked afresh beside the discovery arm.
- **Discovery exposure:** the block shown to the walker is identical, line for line, to
  `eval/fixtures/supplier-selection-retrospective.discovery.md` (checked with `--dry-run` before the
  run), and is recorded per question in the JSON.

## Deviations from the approved configuration — all of them

1. The model is `claude-opus-5-5`, not `claude-opus-5`.
2. Each turn sends the whole conversation as one transcript to a fresh session, not as API messages.
3. One run per question, as before, so there is no variance estimate.
4. The outcomes are now known, so any later run under the approved configuration is non-blind.

## Outcome, against GovKM's frozen expectations for `routing+discovery`

| | expected | routing+discovery | routing (control, re-walked) |
|---|---|---|---|
| Q1 current supplier | PASS | PASS | PASS |
| Q2 new order with E | PASS (strongest falsifier) | **FAIL (order)** — read `z-supplier-e-approved` before `z-supplier-f-approved` | PASS |
| Q3 delivery window today | same as control | same as control — both MISS | MISS |
| Q4 historical E performance | PASS | PASS | PASS |

Aggregates: `rag` found 1.000 / operative 0.250 · `rag+rerank` 1.000 / 0.250 · `routing` 0.750 / 0.750
· `routing+discovery` 0.750 / 0.500.

GovKM's reading (PR #1, 2026-10-09): Q2 shows structural discovery improving access to named evidence
while directing the walker to a superseded record before establishing the operative relationship — the
distinction between relevance-driven discovery and continuity-aware authority ordering. Q3 confirms that
reachability remains unresolved when discovery has no recognized entity to anchor navigation.
