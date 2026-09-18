#!/usr/bin/env python3
"""The router: read hop 0, pick the areas a question belongs to.

This is the human intervention under test. It sees the five frozen `use_when` sentences and nothing
else — not the documents, not the corpus size, not which areas are large. What it is given is
exactly what an agent reading hop 0 is given.

`AREAS_PER_HOP` is how many it may pick. One makes routing a binary hit; several make precision and
recall meaningful, and an overlay is several areas by design.
"""
import json, os, re, time, urllib.error, urllib.request

SYSTEM = ("You are choosing where to look for the answer to a question, from a list of areas. Each "
          "area advertises, in one line, the kinds of question it answers.\n\n"
          "Pick every area that plausibly contains an answer, up to the limit given. Fewer is better "
          "when one area plainly covers it; more is right when the answer genuinely spans areas.\n\n"
          "Answer with the area names on one line, comma-separated, and nothing else.")


class Router:
    def __init__(self, rows, per_hop=2, model=None, provider=None):
        """`rows`: area name -> its frozen use_when sentence."""
        self.rows, self.per_hop = rows, per_hop
        self.provider = provider or os.environ.get("ROUTER_PROVIDER", "anthropic")
        if self.provider == "openai":
            self.base = "https://api.openai.com"
            self.key = os.environ["EMBED_API_KEY"]
            self.model = model or os.environ.get("ROUTER_MODEL", "gpt-5")
        else:
            self.base = os.environ.get("BENCH_LLM_BASE_URL", "https://api.anthropic.com")
            self.key = os.environ["ONTOLOGY_LLM_API_KEY"]
            self.model = model or os.environ.get("ROUTER_MODEL", "claude-opus-5")

    def _ask(self, prompt):
        if self.provider == "openai":
            url, hdr = self.base + "/v1/chat/completions", {"Authorization": f"Bearer {self.key}"}
            body = {"model": self.model, "max_tokens": 1500,
                    "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}]}
        else:
            url, hdr = self.base + "/v1/messages", {"x-api-key": self.key, "anthropic-version": "2023-06-01"}
            body = {"model": self.model, "max_tokens": 1500, "system": SYSTEM,
                    "messages": [{"role": "user", "content": prompt}]}
        req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json", **hdr})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=120) as r: d = json.load(r)
                if self.provider == "openai": return d["choices"][0]["message"]["content"]
                return "".join(b.get("text", "") for b in d["content"] if b.get("type") == "text")
            except Exception as e:
                if attempt < 3: time.sleep(3 * (attempt + 1)); continue
                raise RuntimeError(f"router: {type(e).__name__}: {e}")

    def pick(self, question):
        listing = "\n".join(f"  {a} — {s}" for a, s in sorted(self.rows.items()))
        out = self._ask(f"Question: {question}\n\nAreas:\n{listing}\n\n"
                        f"Pick up to {self.per_hop}.")
        names = [w.strip().lower() for w in re.split(r"[,\n]", out) if w.strip()]
        picked = [a for a in self.rows if any(a == n or a in n for n in names)]
        # A router that names nothing usable has still made a decision, and scoring it as a miss is
        # the honest reading — but it is worth being able to see it in the log.
        return picked[:self.per_hop], out.strip()
