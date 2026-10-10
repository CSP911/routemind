# Does a larger map lose the agent? — 5 areas against 30

The README names it as a way the bet is lost: *"A large map loses the agent. No one has measured a map
with dozens of areas."* This is the first measurement, and a small one.

**The maps.** `examples/back-office` (5 areas), and the same with 25 more areas from
[distractors.yaml](distractors.yaml) — 30 areas, 179 entities. Several sit next to a real area on
purpose: a travel desk beside expense, legal beside procurement's contract custody, an IT helpdesk beside
the lost-card steps, people-benefits beside parental leave, facilities beside the purchasing desk. None
of their documents answers a question here. Hop 0 grows from about 300 words to about 900.

**The walk.** Ten questions ([questions.yaml](questions.yaml)), each answered in one real area and
worded to pull toward its neighbour (`lure`); Claude Code (`sonnet`, `haiku`) through the MCP door, as in
[eval/philosophy](../philosophy/). Scored on the first area entered — the hop-0 decision — and on the
answer.

```sh
./eval/scale/build.py <install>/data/repo      # commit, then tidy.py --fix in the container
./eval/philosophy/run.py --questions eval/scale/questions.yaml --api … --repo … --compose-dir … \
    --models sonnet,haiku --out eval/runs/<date>-scale-30areas
./eval/scale/score.py eval/runs/<date>-scale-5areas eval/runs/<date>-scale-30areas
```

## Result, 2026-10-10

| | 5 areas | 30 areas |
|---|---|---|
| sonnet — first area right · lure taken · answer right | 9/10 · 0 · 10/10 | 9/10 · 0 · 10/10 |
| haiku — first area right · lure taken · answer right | 8/10 · 0 · 10/10 | 9/10 · 0 · **9/10** |
| calls per question (sonnet / haiku) | 6.6 / 6.9 | 6.3 / 6.3 |
| cost, 10 questions (sonnet / haiku) | $0.38 / $0.03 | $0.46 / $0.03 |

Six times the areas cost about 20% more per Sonnet walk (the longer hop 0, read every time) and moved
nothing else. No walk took a lure.

**The one wrong answer was the map's, not the size's.** s5 — *who issues a new corporate card?* — went
to expense first in all four walks. The answer is in procurement's desk document ("issues and cancels
corporate cards"), but procurement's hop-0 sentence said nothing about cards. Three walks found it
anyway after 8–12 calls; Haiku on the 30-area map checked expense, approval and a distractor
(onboarding), then answered **"RouteMind doesn't say who issues a new corporate card"** — a false
absence, exactly the README's *"a missing sentence and a missing document look the same to the agent"*.
With 30 areas there were more plausible places to look before giving up.

The example's sentence was fixed (`… · getting a corporate card issued or cancelled`) and s5 re-run on
both maps: 4/4 straight to procurement, right, in 4–5 calls (`*-fixed/`).

## Korean questions on the English map

Four of the same questions asked in Korean ([../philosophy/questions-ko.yaml](../philosophy/questions-ko.yaml),
5 areas): 8/8 right, both models, answered in Korean, routed by English hop-0 sentences, and the absent
one (remote work) answered "없습니다" after reading the area (`eval/runs/2026-10-10-philosophy-ko/`).

## What this does not show

- **30 is not "dozens of areas with thousands of documents".** The distractors are thin (three short
  pages each); a real neighbouring area with real near-answers is harder than these.
- **Ten questions, one run each.** "Did not get worse" is all it can say.
- **The false absence is the finding.** A bigger map did not confuse the routing; it gave an agent more
  places to look before concluding wrongly that something is missing. That cost lands on whoever keeps
  the sentences complete.
