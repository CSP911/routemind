#!/usr/bin/env python3
"""Does a continuity fixture fit the corpus? Shape, ids, kinds, area, and the one rule that matters.

    ./eval/fixtures/check.py eval/fixtures/<name>.yaml [--corpus bench/corpus]

Run it before sending a fixture. Everything it refuses is something the scoring run would have
refused later, with less explanation.
"""
import pathlib, re, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
KINDS = {"topic", "rule", "procedure", "form", "table", "case", "system", "role", "deadline"}
STATES = {"active", "superseded", "withdrawn"}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def corpus_ids(corpus: pathlib.Path):
    out, areas = set(), set()
    for p in corpus.rglob("*.md"):
        areas.add(p.parent.name)
        m = FM.match(p.read_text(encoding="utf-8"))
        fm = yaml.safe_load(m.group(1)) if m else {}
        out.add((fm or {}).get("id") or p.stem)
    return out, areas


def main(path, corpus):
    fx = yaml.safe_load(pathlib.Path(path).read_text(encoding="utf-8"))
    bad = []
    say = bad.append

    for k in ("id", "area", "subject", "documents", "truth", "questions"):
        if k not in fx: say(f"missing top-level `{k}`")
    if bad: return bad
    if not ID_RE.match(fx["id"]): say(f"fixture id {fx['id']!r} is not kebab-case")

    existing, areas = corpus_ids(corpus)
    if fx["area"] not in areas: say(f"area {fx['area']!r} is not in the corpus ({', '.join(sorted(areas))})")

    ids = []
    for d in fx["documents"]:
        for k in ("id", "date", "kind", "name", "one_liner", "body"):
            if not d.get(k): say(f"document {d.get('id', '?')}: missing `{k}`")
        i = d.get("id", "")
        if not ID_RE.match(i): say(f"document id {i!r} is not kebab-case")
        if i in existing: say(f"document id {i!r} already exists in the corpus")
        if i in ids: say(f"document id {i!r} appears twice in the fixture")
        ids.append(i)
        if d.get("kind") not in KINDS: say(f"document {i}: kind {d.get('kind')!r} is not in the vocabulary")
        # PyYAML reads an unquoted 2025-03-03 as a datetime.date, so it is a string from here on.
        date = str(d.get("date", ""))
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date): say(f"document {i}: date must be YYYY-MM-DD")
        # The rule that matters: nothing in the document may say what the scorer knows. A person
        # writing "this replaces the March decision" in the prose is fine — that is a document. A
        # field is not, because the baseline could never have read it.
        for forbidden in ("state", "supersedes", "superseded_by", "operative", "current"):
            if forbidden in d: say(f"document {i}: `{forbidden}` is truth, not document — move it under `truth:`")
        if date not in d.get("body", "") and date.split("-")[0] not in d.get("body", ""):
            say(f"document {i}: the date is not in the body — a person would have written it")

    t = fx["truth"]
    if t.get("operative") not in ids: say(f"truth.operative {t.get('operative')!r} is not one of the documents")
    for i, s in (t.get("states") or {}).items():
        if i not in ids: say(f"truth.states names {i!r}, not a document here")
        if s not in STATES: say(f"truth.states[{i}] = {s!r}; one of {', '.join(sorted(STATES))}")
    for i in ids:
        if i not in (t.get("states") or {}): say(f"truth.states has no entry for {i}")
    for newer, olders in (t.get("supersedes") or {}).items():
        if newer not in ids: say(f"truth.supersedes names {newer!r}, not a document here")
        for o in olders or []:
            if o not in ids: say(f"truth.supersedes[{newer}] names {o!r}, not a document here")
            if (t.get("states") or {}).get(o) == "active": say(f"{o} is superseded by {newer} but its state is `active`")

    if not fx["questions"]: say("no questions")
    for n, q in enumerate(fx["questions"], 1):
        for k in ("q", "answer", "operative"):
            if not q.get(k): say(f"question {n}: missing `{k}`")
        if q.get("operative") not in ids: say(f"question {n}: operative {q.get('operative')!r} is not a document here")
        for dd in q.get("distractors") or []:
            if dd not in ids: say(f"question {n}: distractor {dd!r} is not a document here")
            if dd == q.get("operative"): say(f"question {n}: {dd} is both operative and a distractor")
    return bad


if __name__ == "__main__":
    args = sys.argv[1:]
    corpus = ROOT / "bench" / "corpus" / "regions"
    if "--corpus" in args:
        corpus = pathlib.Path(args[args.index("--corpus") + 1]) / "regions"; args = [a for a in args if a != "--corpus" and a != str(corpus.parent)]
    if not args: sys.exit(__doc__)
    if not corpus.is_dir(): corpus = ROOT / "examples" / "back-office" / "regions"
    problems = main(args[0], corpus)
    if problems:
        print("\n".join("  " + p for p in problems)); sys.exit(1)
    fx = yaml.safe_load(pathlib.Path(args[0]).read_text(encoding="utf-8"))
    print(f"  ok   {fx['id']}: {len(fx['documents'])} documents into {fx['area']}, {len(fx['questions'])} questions, "
          f"operative {fx['truth']['operative']}   (checked against {corpus.parent.relative_to(ROOT)})")
