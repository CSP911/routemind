#!/usr/bin/env python3
"""Hybrid retrieval over the bench corpus: BM25 + dense, fused, with no dependencies beyond urllib.

Deliberately plain. The experiment is about whether a hand-written routing table earns its upkeep,
so the thing it is measured against has to be the retrieval a sceptic would actually build — not a
toy, and not something exotic enough that a result could be blamed on it.

  BM25      Okapi BM25, k1=1.2 b=0.75, pure python. 800 documents is nothing.
  dense     text-embedding-3-large, whole documents (median 94 tokens — there is nothing to chunk).
  fusion    Reciprocal rank fusion. No score normalisation to argue about, and it is what most
            production hybrid setups actually use.
"""
import json, math, os, pathlib, re, sys, urllib.request
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parent
STOP = set("a an and are as at be by for from has have how in into is it its of on or that the to "
           "what when where which who will with you your not no do does can may".split())


def tokens(text):
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP and len(w) > 1]


class BM25:
    """Okapi BM25. Built once over the corpus, queried per question."""

    def __init__(self, docs, k1=1.2, b=0.75):
        self.ids = list(docs)
        self.k1, self.b = k1, b
        self.tf = {i: Counter(tokens(docs[i])) for i in self.ids}
        self.len = {i: sum(self.tf[i].values()) for i in self.ids}
        self.avg = (sum(self.len.values()) / len(self.ids)) if self.ids else 0.0
        df = Counter()
        for i in self.ids: df.update(self.tf[i].keys())
        n = len(self.ids)
        # The +1 inside the log keeps the idf of a term in every document at a small positive number
        # rather than zero or negative — without it a query made entirely of common words scores
        # every document identically and the ranking is arbitrary rather than merely unhelpful.
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}

    def search(self, q):
        qt = tokens(q)
        out = []
        for i in self.ids:
            tf, dl, s = self.tf[i], self.len[i], 0.0
            for t in qt:
                f = tf.get(t)
                if not f: continue
                s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * dl / self.avg))
            if s: out.append((s, i))
        return sorted(out, reverse=True)


class Dense:
    """Embeddings, cached on disk — the corpus does not change between runs and the calls are not free."""

    def __init__(self, cache=ROOT / "embeddings.json"):
        self.cache_path = cache
        self.cache = json.loads(cache.read_text()) if cache.exists() else {}
        self.key = os.environ["EMBED_API_KEY"]
        self.base = os.environ.get("EMBED_BASE_URL", "https://api.openai.com")
        self.model = os.environ.get("EMBED_MODEL", "text-embedding-3-large")

    def _call(self, texts):
        r = urllib.request.Request(self.base.rstrip("/") + "/v1/embeddings",
            data=json.dumps({"model": self.model, "input": texts}).encode(), method="POST",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.key}"})
        with urllib.request.urlopen(r, timeout=180) as x:
            return [e["embedding"] for e in json.load(x)["data"]]

    def cache_key(self, text):
        """The cache is keyed by **model and** text.

        It was keyed by text alone, and the difficulty scale is supposed to be computed with a model
        other than the one under test. Switching the model changed nothing: every lookup hit the
        first model's vectors and the second model was never called. The check came back 100%
        identical across two models on 700 documents, which is the shape of a result that is not a
        result. Nothing errored, and nothing would have.
        """
        return f"{self.model}\u0000{text}"

    def embed(self, texts, *, use_cache=True):
        want = [t for t in texts if not (use_cache and self.cache_key(t) in self.cache)]
        for i in range(0, len(want), 96):
            batch = want[i:i + 96]
            for t, v in zip(batch, self._call(batch)):
                n = math.sqrt(sum(x * x for x in v))
                self.cache[self.cache_key(t)] = [x / n for x in v]   # unit-length; cosine is a dot product
            print(f"      embedded {min(i + 96, len(want))}/{len(want)}", file=sys.stderr)
        if want: self.cache_path.write_text(json.dumps(self.cache), encoding="utf-8")
        return [self.cache[self.cache_key(t)] for t in texts]


def rrf(rankings, k=60):
    """Reciprocal rank fusion. `rankings` is a list of ranked id lists, best first."""
    s = defaultdict(float)
    for r in rankings:
        for rank, i in enumerate(r, 1): s[i] += 1.0 / (k + rank)
    return sorted(((v, i) for i, v in s.items()), reverse=True)


class Hybrid:
    """BM25 and dense over one document set, fused. `scope` restricts it to a subset of ids."""

    def __init__(self, texts):
        self.texts = texts                      # id -> the text that is indexed
        self.bm25 = BM25(texts)
        self.dense = Dense()
        self.ids = list(texts)
        self.vecs = None

    def warm(self):
        vs = self.dense.embed([self.texts[i] for i in self.ids])
        self.vecs = dict(zip(self.ids, vs))
        return self

    def search(self, q, *, scope=None, n=20):
        pool = set(scope) if scope is not None else set(self.ids)
        qv = self.dense.embed([q])[0]
        dense = sorted(((sum(a * b for a, b in zip(qv, self.vecs[i])), i) for i in pool), reverse=True)
        sparse = [(s, i) for s, i in self.bm25.search(q) if i in pool]
        fused = rrf([[i for _, i in dense[:50]], [i for _, i in sparse[:50]]])
        return [i for _, i in fused[:n]]


def openai_body(model, max_tokens, messages, system=None):
    """OpenAI's chat body, with the parameter name the model actually accepts.

    The newer models refuse `max_tokens` outright and name the replacement in the error. The service
    already settles this argument by asking rather than guessing from a model name
    (ontology/service/curator.py); this is the same move, because a list of which models take which
    parameter is a list that is wrong the week after it is written.

    They are also reasoning models: a small budget is spent thinking and the answer comes back empty,
    which is why callers here pass thousands rather than hundreds.
    """
    msgs = ([{"role": "system", "content": system}] if system else []) + messages
    return {"model": model, "max_tokens": max_tokens, "messages": msgs}


def openai_post(url, key, body, timeout=180):
    """POST, retrying under the parameter name the model asks for.

    Two bugs worth keeping the shape of. `{**body, "max_completion_tokens": body.pop("max_tokens")}`
    unpacks before it pops, so the retry carried *both* names and was refused again — the swap has to
    be done on a copy, explicitly. And the loop fell out of the bottom returning `None`, so a run of
    failures arrived at the caller as `TypeError: 'NoneType' object is not subscriptable` several
    frames away from the thing that actually went wrong.
    """
    import json as _j, time as _t, urllib.request as _u, urllib.error as _e
    last = None
    for attempt in range(6):
        req = _u.Request(url, data=_j.dumps(body).encode(), method="POST",
                         headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
        try:
            with _u.urlopen(req, timeout=timeout) as r: return _j.load(r)
        except _e.HTTPError as e:
            msg = e.read().decode(); last = f"{e.code}: {msg[:200]}"
            if "max_completion_tokens" in msg and "max_tokens" in body:
                body = dict(body)
                body["max_completion_tokens"] = body.pop("max_tokens")
                continue
            if e.code in (429, 500, 502, 503) and attempt < 5:
                _t.sleep(4 * (attempt + 1)); continue
            raise RuntimeError(f"openai {last}")
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
            if attempt < 5: _t.sleep(4 * (attempt + 1)); continue
    raise RuntimeError(f"openai: gave up after 6 attempts — {last}")
