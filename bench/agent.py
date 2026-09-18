#!/usr/bin/env python3
"""An agent that walks the routing tree, the way the MCP server lets one.

The first version of the routed arm picked areas once and stopped. That is not this system: RouteMind
gives an agent two operations and expects it to iterate — read a table, open what looks right, and if
the answer is not there, go back and open something else. A question whose answer needs two areas is
the obvious case: one pass can only ever reach one of them.

    OPEN <id>    a node with children -> its table.  Costs a hop.
    READ <id>    a node with a body   -> collected as an answer. Free.
    BACK         return to hop 0 and choose again. Costs a hop.
    DONE         enough has been collected.

Hop 0 is the five frozen `use_when` sentences. Every table below it prints one row per child with its
one-liner, which is exactly what `mcp/knowledge_mcp.py` puts in the `why` column. Nothing else is
shown — not the body, not the corpus size, not which areas are large.

**Two budgets, because descending and starting over are not the same act.** The first version spent
one budget on both and starved: reaching the documents of two areas costs OPEN, OPEN, BACK, OPEN,
OPEN, and with a budget of three the agent had used it all before it read anything. It visited the
right areas and came back with nothing.

    returns   going back to hop 0. Budgeted at 3 — the figure the overlay design uses.
    steps     turns in total, a stop against looping rather than a measure of anything.

Descending is not rationed. A tree bounds it: five levels is five OPENs, and an agent that opens the
wrong table has still spent a turn, which is what `steps` catches.
"""
import json, os, re, time, urllib.error, urllib.request

SYSTEM = (
 "You are finding the documents that answer a question, by walking a routing table.\n\n"
 "At each step you see a table. Each row is either a **table** (open it to see what is inside) or a "
 "**document** (read it — it may contain the answer).\n\n"
 "Reply with one or more commands, one per line, and nothing else:\n"
 "  OPEN <id>    open a table\n"
 "  READ <id>    collect a document as part of the answer\n"
 "  BACK         return to the top-level list of areas and choose differently\n"
 "  DONE         you have collected everything the question needs\n\n"
 "Read every document that contributes to the answer. If the question has two parts that live in "
 "different places, collect both — going BACK to the top and opening another area is the way to do "
 "that, and it is expected rather than a failure. Say DONE only when nothing is missing.")


class Agent:
    def __init__(self, rows, children, one_liner, has_body, budget=3, steps=10,
                 model=None, provider=None):
        self.rows = rows                # area -> frozen use_when
        self.children = children        # id -> [child ids]
        self.one_liner = one_liner
        self.has_body = has_body
        self.budget = budget            # returns to hop 0
        self.steps = steps              # turns, a loop guard
        # Pinned. The first run used gpt-4o and it invented row names that were not in the table —
        # not a routing-logic failure, an instruction-following one, and the two are exactly what Q3
        # is trying to keep apart. A weak router turns every question into "was the model able".
        self.provider = provider or os.environ.get("ROUTER_PROVIDER", "anthropic")
        if self.provider == "openai":
            self.base, self.key = "https://api.openai.com", os.environ["EMBED_API_KEY"]
            self.model = model or os.environ.get("ROUTER_MODEL", "gpt-5")
        else:
            self.base = os.environ.get("BENCH_LLM_BASE_URL", "https://api.anthropic.com")
            self.key = os.environ["ONTOLOGY_LLM_API_KEY"]
            self.model = model or os.environ.get("ROUTER_MODEL", "claude-opus-5")

    def _ask(self, convo):
        if self.provider == "openai":
            url, hdr = self.base + "/v1/chat/completions", {"Authorization": f"Bearer {self.key}"}
            body = {"model": self.model, "max_tokens": 2000,
                    "messages": [{"role": "system", "content": SYSTEM}] + convo}
        else:
            url, hdr = self.base + "/v1/messages", {"x-api-key": self.key, "anthropic-version": "2023-06-01"}
            body = {"model": self.model, "max_tokens": 2000, "system": SYSTEM, "messages": convo}
        req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json", **hdr})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=120) as r: d = json.load(r)
                if self.provider == "openai": return d["choices"][0]["message"]["content"]
                return "".join(b.get("text", "") for b in d["content"] if b.get("type") == "text")
            except Exception as e:
                if attempt < 3: time.sleep(3 * (attempt + 1)); continue
                raise RuntimeError(f"agent: {type(e).__name__}: {e}")

    def _hop0(self):
        return ("The areas of this ontology:\n\n" +
                "\n".join(f"  table  {a}  —  {s}" for a, s in sorted(self.rows.items())))

    def _table(self, node):
        kids = self.children.get(node, [])
        if not kids: return f"`{node}` holds no further rows."
        lines = []
        for c in kids:
            kind = "document" if self.has_body.get(c) and not self.children.get(c) else "table"
            lines.append(f"  {kind:<9} {c}  —  {self.one_liner.get(c,'')}")
        return f"Inside `{node}`:\n\n" + "\n".join(lines)

    def walk(self, question):
        convo = [{"role": "user", "content": f"Question: {question}\n\n{self._hop0()}"}]
        collected, visited, log = [], [], []
        returns, opens, turns = 0, 0, 0
        while turns < self.steps:
            turns += 1
            out = self._ask(convo)
            log.append(out.strip())
            convo.append({"role": "assistant", "content": out})
            done, shown, refused, bad = False, [], False, []
            for c in [l.strip() for l in out.splitlines() if l.strip()]:
                m = re.match(r"(OPEN|READ|BACK|DONE)\b\s*(\S*)", c, re.I)
                if not m: continue
                verb, arg = m.group(1).upper(), m.group(2).strip("`,.")
                if verb == "DONE": done = True; break
                if verb == "BACK":
                    if returns >= self.budget: refused = True; continue
                    returns += 1; shown.append(self._hop0()); continue
                if arg not in self.one_liner:
                    # Saying nothing here is how a run burns its turns: the agent names something
                    # that is not in the table, the command is dropped in silence, the same table
                    # comes back, and it names it again. gpt-4o did this for a whole walk.
                    bad.append(arg or "(nothing)")
                    continue
                if verb == "READ":
                    collected.append(arg); visited.append(arg)
                else:
                    opens += 1; visited.append(arg); shown.append(self._table(arg))
            if done: break
            if refused and not shown:
                shown = [f"You have gone back to the start {self.budget} times, which is the limit. "
                         f"READ what the question needs from what you have seen, then say DONE."]
            if bad:
                shown.insert(0, "Not in the table: " + ", ".join(sorted(set(bad))[:5])
                             + ". Use an id exactly as it is printed in the rows above.")
            if not shown:
                shown = ["That named nothing in the table. Reply with OPEN, READ, BACK or DONE and an "
                         "id exactly as printed.\n\n" + self._hop0()]
            convo.append({"role": "user", "content": "\n\n".join(shown)})
        return {"collected": list(dict.fromkeys(collected)), "visited": visited,
                "returns": returns, "opens": opens, "turns": turns,
                "hops": opens + returns, "log": log}
