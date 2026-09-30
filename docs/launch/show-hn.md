# Show HN — draft

## Title

Under HN's 80 characters. It names the mechanism and picks no fight: the study's own finding is that
320 of 700 questions retrieval already answers first time, so "instead of RAG" would be a claim the
evidence does not support.

```
Show HN: RouteMind – routing instead of retrieval for agent knowledge
```

Alternates, same rule:

```
Show HN: RouteMind – areas advertise when they're relevant; agents route first
Show HN: An ontology you can see the agent reading
```

## URL

`https://github.com/CSP911/routemind`

## First comment

> I kept hitting the same failure with retrieval over an internal knowledge base: ask in the words a
> person actually uses, and you get documents that are *about* the right subject but answer a
> different question — usually an older version of the same rule, because every newer one outranks
> the one you asked for and they all look alike.
>
> So I stopped trying to fix the search and changed what the agent reads first. Each area of the
> domain carries one sentence saying *when you would come here*. The agent reads that list — one line
> per area, nothing else — picks, and only then opens documents. It is BGP's shape: advertise where
> you are relevant rather than export everything you hold. An exchange between backbones is a route
> reflector, and it declines transit for the same reason a route server does.
>
> **The numbers, with the part that costs me.** 700 questions over one frozen corpus of 1,126
> documents, four arms, every one a census:
>
>     | question type                 | RAG   | +rerank | RouteMind |
>     | a question in the rows' codes | 0.991 | 1.000   | 1.000     |
>     | a question in a person's words| 0.028 | 0.069   | 1.000     |
>     | a rule two revisions back     | 0.133 | 0.200   | 1.000     |
>
> And what it costs: 6.7 tool calls, 23–111 seconds, $0.12–$0.28 a question, against one sub-second
> embedding call. **320 of those 700 are questions retrieval already answers first time** — nothing
> here argues for walking those. Which one to use is a question about the mix of questions you
> actually get, and I have not measured that for anyone but this corpus.
>
> **The obvious objection is right, so here is what to check.** I wrote the benchmark. The corpus
> (865 files), the gold sets, the generator that produced the corpus, the pre-registration frozen
> before anything ran, and every run record including the failed ones are all in the repo. If the
> corpus is the problem, that is the thing to attack, and you have it.
>
> **What it does not do.** The map is written and kept by hand — I have moved the work, not removed
> it, and nothing here prices that labour. The single miss in all 700 was *a wrong sentence in the
> map*, not a wrong document: both routing arms obeyed it identically and answered confidently from
> the wrong era with a source attached. Retrieval cannot fail that way, because it reads no map. And
> I do not know whether a **correct** map has a size at which this stops working — one corpus size is
> one point, and you cannot see a limit from one point.
>
> MIT. `./install.sh --name acme --port 9000`, then `claude` in the same directory — it registers
> itself over MCP, and you can click any area on the map to see the exact text an agent is handed.
>
> What I would most like torn apart: the ergonomics of maintaining the map, and whether the corpus is
> fair.

## Before posting

- [x] `./check/install-check.sh` — a clean clone, installed and walked. **Run it.** It found seven
      failures the day this draft was written: the walk still spoke the pre-merge API, and it is the
      one suite `check/all.sh` does not run, so nothing else had noticed for a day
- [ ] the map screenshot in the README still matches what the install draws
- [ ] no uncommitted work, `main` pushed
- [ ] post on a weekday morning US Eastern; be at a keyboard for the next four hours

## What the replies will be, and the honest answer to each

**"You built the benchmark to win."** — Yes, I built it. That is why the corpus, the gold sets, the
generator and the pre-registration are in the repo. Attack the corpus; it is the right target.

**"This is a hand-maintained table of contents."** — It is. The claim is not that indexing is novel;
it is that *one sentence per area, read before anything else* is where the leverage is, and the 0.028
row is what that buys. The cost column is in the README for the same reason.

**"Who maintains it?"** — A person, and the study lost three runs to a map that had drifted. That is
why `mapcheck` runs before any arm does, and why a wrong map is the failure mode I flag rather than
hide.

**"30 seconds and $0.20 a question is unusable."** — For 320 of the 700, yes, and I say so. For the
questions retrieval scores 0.028 on, the alternative is a confident wrong answer.

**"Why not just fine-tune / bigger context / better chunking?"** — Untested here, and I will say so
rather than guess. The failure I measured is about *which* document is returned when several are
plausible and only one is current; a longer context does not decide that, it includes them all.

---

# awesome-mcp-servers

The PR is open and has been since 2026-09-12:
**[punkpeye/awesome-mcp-servers#14212](https://github.com/punkpeye/awesome-mcp-servers/pull/14212)**

It is blocked on the list's own requirement, not on the entry. The maintainer and their bot both
asked for the same thing:

1. **List the server on Glama** — https://glama.ai/mcp/servers. It needs an account, a claim on the
   repository, and a Dockerfile pasted into Glama's own form. The bar is low: *"we only need the
   server to start and respond to introspection requests."*
2. **Then add the badge** to the PR, after the description:

```
[![CSP911/routemind MCP server](https://glama.ai/mcp/servers/CSP911/routemind/badges/score.svg)](https://glama.ai/mcp/servers/CSP911/routemind)
```

Step 1 is an account action on somebody else's service, so it is yours to do. Step 2 is one line and
takes a minute afterwards.

**What is ready for it.** The `Dockerfile` at the repository root — moved there from `mcp/` once the
listing said "this server cannot be deployed", which is what a directory says when it cannot find a
way to start the thing it is scoring. It builds an image that starts the server over stdio and
answers `initialize` and `tools/list` with **no network at all** — which is exactly the check.
Verified:

```
docker run -i --rm routemind-mcp
  initialize: knowledge · protocol 2024-11-05
  tools/list: knowledge_table, knowledge_read, knowledge_circuit
```

There is no form: the submission never asked for one and the listing has no edit UI, so the root
Dockerfile is the way a directory finds it. If the score is still `---` after Glama next crawls the
repository, their [Discord](https://glama.ai/discord) is the channel the bot itself pointed at.

**The entry itself is also ready to improve when the PR is next touched.** The version in the open PR
predates the Glama requirement and carries no badge; a better one is drafted here — the format copied
from its neighbours, and the description trimmed to 142 characters because the list's own most recent
commit is "shorten long descriptions" and the entries around it run 144 median, 160 max:

```
- [CSP911/routemind](https://github.com/CSP911/routemind) [![CSP911/routemind MCP server](https://glama.ai/mcp/servers/CSP911/routemind/badges/score.svg)](https://glama.ai/mcp/servers/CSP911/routemind) 🐍 🏠 🍎 🪟 🐧 - Routes before it retrieves: each area advertises in one line when it is relevant, so the agent picks before it reads. Git-backed, no database.
```

Under **Knowledge & Memory**. The PR title already carries `🤖🤖🤖`, which their CONTRIBUTING asks for
when an automated agent prepared it.
