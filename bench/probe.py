#!/usr/bin/env python3
"""Where does plain RAG break? A sweep, not a gold set.

`eval/DIFFICULTY.md` now defines the severe band as the place B1 stops coping. That is only a
definition until someone measures where the place is, and the pilot could not: its hardest question
scored 12 on a 15-point scale and B1 was still at 0.67 there. Nobody has asked this corpus anything
at the sums where a break could live.

This asks, at volume and cheaply.

    ./bench/probe.py gen              write the probe questions   (~90 LLM calls)
    ./bench/probe.py run              measure fusion, no reranker (embeddings only)
    ./bench/probe.py report           the curves

**Why fusion alone is enough to find the break.** The reranker only ever reorders the fused
candidates. If the answer is not in the fused top-20 the reranker cannot put it in the top-10, so

    fusion recall@20  is a hard ceiling on B1 hit@10

and wherever that ceiling falls below 0.50, B1 is broken — proved without spending a rerank call.
Where the ceiling holds up, fusion tells us nothing about B1 on its own and the reranker has to be
run; `run --rerank` does that, and the point of staging it is that the expensive half only runs in
the narrow region where it can change the answer.

**One factor is swept, not the sum.** A sum of 12 can be five mild factors or two extreme ones, and
those are not the same question. The sweep manipulates **A, the lexical bridge** — the only factor
that can be varied freely on a fixed document — across documents stratified by their own C+D+E. So
the output is a surface, difficulty-of-document against distance-of-wording, rather than one line
through a number that conflates both.

A is *measured* afterwards from the text, never trusted: `eval/gold/grade.py` defines it as the
fraction of the question's content tokens that appear in the answer document, and this uses the same
function. A question written to be a paraphrase often is not one.
"""
import argparse, collections, json, os, pathlib, re, sys, time, urllib.error, urllib.request
import yaml

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / "eval" / "gold"))
from retrieve import Hybrid, openai_post
from rerank import LLMReranker
import importlib.util
_s = importlib.util.spec_from_file_location("grade", ROOT.parent / "eval" / "gold" / "grade.py")
grade = importlib.util.module_from_spec(_s); _s.loader.exec_module(grade)

FM = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)
LOCK = ROOT / ".probe.lock"
QUESTIONS = ROOT / "probe-questions.json"
RESULTS = ROOT / "probe-results.json"
PER_CDE = 10          # documents drawn at each C+D+E level, where the corpus has that many

# What each rung of A asks the question writer for. The measured share decides the rung in the end;
# this is only the instruction, and DIFFICULTY.md's cuts are the definition.
RUNGS = {
 0: "Use the document's own vocabulary. Name the thing the way the document names it. This should be "
    "the easiest possible question to match by keyword.",
 1: "Mostly the document's vocabulary, lightly rephrased. Keep the distinctive nouns.",
 2: "Substantially rephrased. Replace the distinctive nouns with ordinary ones a person would use "
    "who had not read this document.",
 3: "A full paraphrase. Use none of the document's distinctive vocabulary — describe the situation "
    "in plain words, the way somebody would ask who knows their problem but not this system's terms. "
    "Do not name the document's subject with the document's word for it.",
}

SYSTEM = (
 "You write evaluation questions against a single source document.\n\n"
 "Rules that hold for every question you write:\n"
 "- It must be answerable from the document you are given, and anchored on something specific in it "
 "— a condition, a threshold, a named case — so that no other document would answer it just as well.\n"
 "- It is a question a person would actually ask. Not 'what does section 3 say'.\n"
 "- One sentence. No preamble.\n\n"
 "You will be asked for four versions of the same question, differing only in how closely the "
 "wording follows the document. The underlying question — the fact being asked for — must be the "
 "SAME in all four. Only the vocabulary changes.\n\n"
 "Reply with JSON only: {\"0\": \"...\", \"1\": \"...\", \"2\": \"...\", \"3\": \"...\"}")


def corpus_texts():
    """The retrieval pool, and optionally the hard extension on top of it.

    `bench/corpus/` is frozen at 700 documents. `BENCH_EXTRA_CORPUS=bench/corpus-hard` adds the
    qualifier families without touching it, so a result on 700 and a result on 780 are two rows of
    one table rather than one number that quietly changed meaning halfway through.
    """
    man = json.loads((ROOT / "manifest.json").read_text())
    roots = [ROOT / "corpus" / "regions"]
    extra = os.environ.get("BENCH_EXTRA_CORPUS")
    if extra:
        ex = pathlib.Path(extra)
        if not ex.is_absolute(): ex = ROOT.parent / ex
        roots.append(ex / "regions")
        cm = ex.parent / "crowd-manifest.json"
        if cm.exists(): man.update(json.loads(cm.read_text()))
    texts, area, raw = {}, {}, {}
    for r in roots:
        for p in r.rglob("*.md"):
            m = FM.match(p.read_text(encoding="utf-8")); fm = yaml.safe_load(m.group(1)) or {}
            i = fm.get("id") or p.stem
            area[i] = p.parent.name
            if man.get(i, {}).get("section"): continue
            raw[i] = f"# {fm.get('name','')}\n{fm.get('one_liner','')}\n\n{m.group(2)}"
            texts[i] = f"{fm.get('name','')} {fm.get('one_liner','')} {m.group(2)}"
    return texts, area, raw


def factors():
    path = ROOT / "factors.csv"
    return {r["id"]: r for r in __import__("csv").DictReader(l for l in open(path)
                                                             if not l.startswith("#"))}


def pick(fac, texts):
    """Documents stratified by their own C+D+E, so the sweep covers the whole difficulty floor.

    Deterministic — sorted by id and taken from the front. A random draw would make the probe
    unreproducible for the sake of an unbiasedness the sweep does not need: nothing here is an
    estimate of a population mean.
    """
    by = collections.defaultdict(list)
    for i, r in sorted(fac.items()):
        if i in texts: by[int(r["CDE"])].append(i)
    return {c: v[:PER_CDE] for c, v in sorted(by.items())}


def anthropic(prompt, model="claude-opus-5", system=None):
    body = {"model": model, "max_tokens": 2000, "system": system or SYSTEM,
            "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request(
        os.environ.get("BENCH_LLM_BASE_URL", "https://api.anthropic.com") + "/v1/messages",
        data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json", "anthropic-version": "2023-06-01",
                 "x-api-key": os.environ["ONTOLOGY_LLM_API_KEY"]})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r: d = json.load(r)
            return "".join(b.get("text", "") for b in d["content"] if b.get("type") == "text")
        except urllib.error.HTTPError as e:
            # The body is where the provider says what is actually wrong; without it a 400 is a
            # wall. A 4xx other than 429 will not fix itself on a retry, so it is raised at once.
            detail = e.read().decode("utf-8", "replace")[:400]
            if e.code == 429 or e.code >= 500:
                if attempt < 3: time.sleep(3 * (attempt + 1)); continue
            raise RuntimeError(f"probe gen: HTTP {e.code}: {detail}")
        except Exception as e:
            if attempt < 3: time.sleep(3 * (attempt + 1)); continue
            raise RuntimeError(f"probe gen: {type(e).__name__}: {e}")


# Question writing moved to OpenAI when the Anthropic balance ran out mid-session. The model floor
# in PREREGISTRATION.md §9 governs the router — it exists so a routing failure is not an
# instruction-following failure — and says nothing about who writes the questions. The threat it does
# raise (a GPT reranker judging GPT-written questions) is recorded in the run log, not hidden here.
GEN_MODEL = os.environ.get("PROBE_GEN_MODEL", "gpt-5.2")
GEN_PROVIDER = os.environ.get("PROBE_GEN_PROVIDER", "openai")


def openai(prompt, model=None, system=None, max_tokens=4000):
    body = {"model": model or GEN_MODEL, "max_tokens": max_tokens,
            "messages": ([{"role": "system", "content": system or SYSTEM}] +
                         [{"role": "user", "content": prompt}])}
    d = openai_post("https://api.openai.com/v1/chat/completions", os.environ["EMBED_API_KEY"], body)
    return d["choices"][0]["message"]["content"] or ""


def ask(prompt, system=None, model=None):
    """Whichever provider is configured. One seam, so a switch is one environment variable."""
    if GEN_PROVIDER == "anthropic":
        return anthropic(prompt, model=model or "claude-opus-5", system=system)
    return openai(prompt, model=model, system=system)


def cmd_gen(a):
    texts, area, raw = corpus_texts()
    fac = factors()
    chosen = pick(fac, texts)
    out = json.loads(QUESTIONS.read_text()) if QUESTIONS.exists() else {}
    todo = [i for v in chosen.values() for i in v if i not in out]
    print(f"  {sum(len(v) for v in chosen.values())} documents across CDE "
          f"{min(chosen)}-{max(chosen)} · {len(todo)} still to write", file=sys.stderr)
    for n, i in enumerate(todo, 1):
        prompt_text = ("Document:\n\n" + raw[i][:6000] + "\n\nWrite the four versions.\n\n" +
                       "\n".join(f"{k}: {v}" for k, v in RUNGS.items()))
        txt = ask(prompt_text)
        m = re.search(r"\{.*\}", txt, re.S)
        if not m: print(f"    {i}: no JSON, skipped", file=sys.stderr); continue
        try: qs = json.loads(m.group(0))
        except json.JSONDecodeError: print(f"    {i}: bad JSON, skipped", file=sys.stderr); continue
        out[i] = {str(k): qs[str(k)] for k in range(4) if str(k) in qs}
        QUESTIONS.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    {n}/{len(todo)}  {i}", file=sys.stderr)
    print(f"  {len(out)} documents have questions -> {QUESTIONS.name}", file=sys.stderr)


def guard():
    """One sweep at a time, because two of them silently ruin each other.

    Both write the same results file whole, so the second to finish wins and the first one's work
    is gone — and the log interleaves, which is the only way it shows. This happened: two rerank
    sweeps ran for 45 and 24 minutes against the same file, and the symptom was a progress counter
    that went 40, 125, 60, 70. Also the reason a machine with two of these in memory ran out of it.
    """
    if LOCK.exists():
        try: pid = int(LOCK.read_text().strip())
        except ValueError: pid = None
        alive = False
        if pid:
            try: os.kill(pid, 0); alive = True
            except OSError: alive = False
        if alive: sys.exit(f"  a sweep is already running as pid {pid}; {LOCK.name} holds it")
        print(f"  clearing a stale lock from pid {pid}", file=sys.stderr)
    LOCK.write_text(str(os.getpid()))
    import atexit; atexit.register(lambda: LOCK.exists() and LOCK.unlink())


def cmd_run(a):
    guard()
    texts, area, raw = corpus_texts()
    fac = factors()
    qs = json.loads(QUESTIONS.read_text())
    h = Hybrid(texts).warm()
    rr = LLMReranker() if a.rerank else None
    # Every probe question at once, so the embedding call batches instead of trickling.
    flat = [(i, int(rung), q) for i, v in sorted(qs.items()) for rung, q in sorted(v.items())]
    h.dense.embed([q for _, _, q in flat])
    # Resumable, and written as it goes. Two of these sweeps running at once exhausted this machine's
    # memory and both were killed; the fusion half had finished and the rerank half lost 50 probes it
    # had already paid for. A long run that keeps nothing until the end is a run you cannot afford to
    # interrupt, which is the same as a run you cannot afford to start.
    done = {}
    if RESULTS.exists():
        for r in json.loads(RESULTS.read_text()):
            if not a.rerank or "b1_rank" in r: done[(r["doc"], r["rung"])] = r
    rows = []
    for n, (doc, rung, q) in enumerate(flat, 1):
        if (doc, rung) in done:
            rows.append(done[(doc, rung)]); continue
        fused = h.search(q, n=50)
        rank = fused.index(doc) + 1 if doc in fused else None
        r = {"doc": doc, "rung": rung, "q": q, "area": area[doc], "CDE": int(fac[doc]["CDE"]),
             "C": int(fac[doc]["C"]), "D": int(fac[doc]["D"]), "E": int(fac[doc]["E"]),
             # A measured from the text, by the same definition the gold set is graded with.
             "A": measured_A(q, texts[doc]), "fusion_rank": rank}
        if rr is not None:
            # The reranker sees the fused top-20 and nothing else, which is exactly B1's shape.
            ranked = rr.rank(q, fused[:20], texts) + fused[20:]
            r["b1_rank"] = ranked.index(doc) + 1 if doc in ranked else None
        rows.append(r)
        if n % 10 == 0 or n == len(flat):
            RESULTS.write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
            print(f"    {n}/{len(flat)}", file=sys.stderr)
    RESULTS.write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"  {len(rows)} probes -> {RESULTS.name}", file=sys.stderr)


def measured_A(q, doc_text):
    qt = grade.toks(q); dt = grade.toks(doc_text)
    share = len(qt & dt) / len(qt) if qt else 0.0
    return next((n for n, c in enumerate(grade.A_CUTS) if share >= c), 3)


def rate(rows, key, hit):
    by = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        by[key(r)][0] += hit(r); by[key(r)][1] += 1
    return {k: (v[0] / v[1], v[1]) for k, v in sorted(by.items())}


def cmd_report(a):
    rows = json.loads(RESULTS.read_text())
    has_b1 = any("b1_rank" in r for r in rows)

    def at(field, k):
        return lambda r: bool(r.get(field)) and r[field] <= k

    print(f"\n  {len(rows)} probe questions over {len({r['doc'] for r in rows})} documents\n")
    print("  A is measured from the text, not the rung it was written for:")
    tab = collections.defaultdict(collections.Counter)
    for r in rows: tab[r["rung"]][r["A"]] += 1
    print("    rung \\ measured A   0    1    2    3")
    for rung in sorted(tab):
        print(f"         {rung}          " + "".join(f"{tab[rung][x]:>5}" for x in range(4)))

    for label, field, k in (("fusion recall@20  (the ceiling on B1)", "fusion_rank", 20),
                            ("fusion recall@10", "fusion_rank", 10),
                            *((("B1 hit@10", "b1_rank", 10),) if has_b1 else ())):
        print(f"\n  {label}")
        print("    by measured A")
        for aa, (v, n) in rate(rows, lambda r: r["A"], at(field, k)).items():
            print(f"      A={aa}   {v:5.2f}   n={n}")
        print("    by document C+D+E")
        for c, (v, n) in rate(rows, lambda r: r["CDE"], at(field, k)).items():
            print(f"      {c:>2}     {v:5.2f}   n={n}")
        print("    the surface, A down · CDE across")
        cs = sorted({r["CDE"] for r in rows})
        print("        " + "".join(f"{c:>6}" for c in cs))
        for aa in range(4):
            cells = []
            for c in cs:
                sub = [r for r in rows if r["A"] == aa and r["CDE"] == c]
                cells.append(f"{sum(at(field,k)(r) for r in sub)/len(sub):>6.2f}" if sub else "     ·")
            print(f"    A={aa} " + "".join(cells))
        print("    by the sum a question of this shape would score (A + CDE, B=0)")
        for s, (v, n) in rate(rows, lambda r: r["A"] + r["CDE"], at(field, k)).items():
            bar = "#" * round(v * 20)
            print(f"      {s:>2}     {v:5.2f}  n={n:<4} {bar}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("gen")
    r = sub.add_parser("run"); r.add_argument("--rerank", action="store_true")
    sub.add_parser("report")
    a = ap.parse_args()
    {"gen": cmd_gen, "run": cmd_run, "report": cmd_report}[a.cmd](a)
