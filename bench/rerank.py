#!/usr/bin/env python3
"""Reranking the candidates a retriever handed back.

Neither OpenAI nor Anthropic has a rerank endpoint, so this is an LLM scoring candidates — which is
a real technique and not a stand-in, but it is *not* a cross-encoder and it is slower and dearer than
one. `Reranker` is the seam: a Cohere or Voyage key swaps the class and changes nothing else.

**It is told nothing about areas.** The reranker sees a question and some documents. If it knew which
area a document came from it could infer what the routing table decided, and the arm that is supposed
to run without a table would be reading the table's answer out of its own input.
"""
import json, os, re, urllib.request, urllib.error, time


class LLMReranker:
    """Score each candidate 0-10 for whether it answers the question, then order by the score.

    Scoring beats asking for a ranked list: a list has to be parsed against the candidates and a
    model that drops or invents an id makes the whole answer unusable, where a missing score is one
    candidate falling back to its retrieval order.
    """

    SYSTEM = ("You judge whether a document answers a question. For each candidate, give a score from "
              "0 to 10: 10 means it directly and completely answers it, 5 means it is about the right "
              "subject but does not contain the answer, 0 means it is unrelated.\n\n"
              "Answer with one line per candidate, `<number> <score>`, and nothing else. Judge each "
              "candidate on its own — do not spread the scores out to make a ranking.")

    def __init__(self, model=None, provider=None, base=None, key=None):
        self.provider = provider or os.environ.get("RERANK_PROVIDER", "openai")
        if self.provider == "openai":
            self.base = base or "https://api.openai.com"
            self.key = key or os.environ["EMBED_API_KEY"]
            # A different vendor from the router on purpose: a reranker that shares the router's
            # blind spots cannot correct for them.
            self.model = model or os.environ.get("BENCH_RERANK_MODEL", "gpt-5")
        else:
            self.base = base or os.environ.get("BENCH_LLM_BASE_URL", "https://api.anthropic.com")
            self.key = key or os.environ.get("BENCH_LLM_API_KEY") or os.environ["ONTOLOGY_LLM_API_KEY"]
            self.model = model or os.environ.get("BENCH_RERANK_MODEL", "claude-sonnet-5")

    def _ask(self, prompt, max_tokens=4000):
        if self.provider != "anthropic":
            # Through the shared helper, which retries under `max_completion_tokens` when the model
            # refuses `max_tokens`. gpt-5 does, and names the replacement in the error — the same
            # argument ontology/service/curator.py settles by asking rather than by a model list.
            from retrieve import openai_body, openai_post
            d = openai_post(self.base.rstrip("/") + "/v1/chat/completions", self.key,
                            openai_body(self.model, max_tokens,
                                        [{"role": "user", "content": prompt}], system=self.SYSTEM))
            return d["choices"][0]["message"]["content"]
        url = self.base.rstrip("/") + "/v1/messages"
        hdr = {"x-api-key": self.key, "anthropic-version": "2023-06-01"}
        body = {"model": self.model, "max_tokens": max_tokens, "system": self.SYSTEM,
                "messages": [{"role": "user", "content": prompt}]}
        req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json", **hdr})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=180) as r: d = json.load(r)
                return "".join(b.get("text", "") for b in d["content"] if b.get("type") == "text")
            except urllib.error.HTTPError as e:
                if e.code in (429, 500, 502, 503, 529) and attempt < 3:
                    time.sleep(5 * (attempt + 1)); continue
                raise RuntimeError(f"rerank {e.code}: {e.read().decode()[:200]}")

    def rank(self, question, candidates, texts, *, chars=900):
        """candidates: ids, best-first from retrieval. Returns them reordered."""
        if len(candidates) < 2: return list(candidates)
        listing = "\n\n".join(f"[{n}]\n{texts[i][:chars]}" for n, i in enumerate(candidates, 1))
        out = self._ask(f"Question: {question}\n\nCandidates:\n\n{listing}")
        scores = {}
        for line in out.splitlines():
            m = re.match(r"\s*\[?(\d+)\]?[\s:.\-]+(\d+(?:\.\d+)?)\s*$", line)
            if m:
                n, s = int(m.group(1)), float(m.group(2))
                if 1 <= n <= len(candidates): scores[candidates[n - 1]] = s
        # A candidate the model did not score keeps its retrieval position rather than being dropped:
        # the reranker is allowed to reorder, never to decide something is not a candidate at all.
        return sorted(candidates, key=lambda i: (-scores.get(i, -1), candidates.index(i)))
