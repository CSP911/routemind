# Writing a map an agent stays right on

Five rules for whoever keeps the sentences and the pages. Each comes from a measurement in which an
agent went wrong — or would have — and what stopped it. None of them is enforced by the software; they
are the human half of the bet.

## 1. An area's sentence names every question its documents answer

`use_when` is all an agent reads before it chooses. A question its documents answer but its sentence
does not name is, to the agent, not in that area.

*Measured* ([eval/scale](../eval/scale/)): "who issues a corporate card?" — the answer was in
procurement's desk page, but procurement's sentence never mentioned cards. Every walk went to expense
first; one looked in three areas and answered **"RouteMind doesn't say"**. Adding *"getting a corporate
card issued or cancelled"* to the sentence: every walk went straight there, in four or five calls.

A missing sentence and a missing document look the same to the agent. When a walk ends "not found" on
something you know is there, the fix is usually this sentence.

## 2. A page that covers part of a question says so, and says where the rest is

*Measured* ([eval/philosophy](../eval/philosophy/), the plausible wrong area): a false hop-0 sentence
sent agents into procurement for "what can a division head approve". Procurement's threshold table
answers it **for purchases only**. While the page said *"the authority itself is set by the delegation
rules in Documents & Approval"*, every agent went on and answered right. With that sentence removed,
both models answered with the purchase band alone.

Overview pages that end with *"What this area does not answer: … (Expenses > Travel expenses)"* do the
same work for a whole area. They are the cheapest defence there is against a wrong sentence at hop 0.

## 3. A line says what someone would come to the page for — not what the page says

*Measured* (placement, 2026-10-10): asked to file a one-paragraph policy, an agent wrote the paragraph
itself as the line. The table then prints the answer instead of when to open the page, and the next
reader takes the summary for the document. *"How many days a week may be worked from home, who approves
it, and how to book it"* is a line; the policy is the page.

## 4. Fold only as deep as the weakest agent that will read it

Holders keep tables short. *Measured* ([eval/depth](../eval/depth/)): with a Sonnet-class agent, a
folded tree and a flat one scored the same and the flat one cost 2.4× the tokens. With a Haiku-class
agent the **flat** tree scored higher (66 vs 61 of 73): every holder is one more decision to get wrong.
A holder whose line does not name what is under it costs the most.

## 5. When an agent says a line is wrong, fix the line

Agents are asked to name a line that disagrees with its page, and the server tells a walk when it has
switched areas so a wrong hop-0 sentence gets reported. *Measured*: once asked, both models named the
false line in every walk that passed one. The answer they gave was already right — so if nobody acts on
the note, the map stays wrong for the next agent that does not read the page.

Look for "the line … may need correcting" at the end of an answer, and for walks in the map's history
that went through two areas before answering.
