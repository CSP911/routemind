#!/usr/bin/env python3
"""Add the distractor areas to a data repository holding examples/back-office.

    ./eval/scale/build.py <install>/data/repo        # then commit, and regenerate regions.json

Each area gets a face (its use_when) and three short documents that answer nothing in questions.yaml.
"""
import pathlib, sys, json
import yaml

HERE = pathlib.Path(__file__).resolve().parent
repo = pathlib.Path(sys.argv[1])
spec = yaml.safe_load((HERE / "distractors.yaml").read_text())["areas"]
for area, a in spec.items():
    d = repo / "regions" / area; d.mkdir(parents=True, exist_ok=True)
    title = area.replace("-", " ").capitalize()
    (d / f"{area}.md").write_text(
        f"---\nid: {area}\nname: {json.dumps(title)}\nkind: topic\none_liner: {json.dumps(title)}\nrole: representative\n"
        f"use_when: {json.dumps(a['use_when'])}\n---\n# {title}\n\nWhat this area holds is listed below.\n", encoding="utf-8")
    for doc, line in a["docs"].items():
        did = f"{area}-{doc}"
        (d / f"{did}.md").write_text(
            f"---\nid: {did}\nname: {json.dumps(line.split(' — ')[0])}\nkind: procedure\none_liner: {json.dumps(line)}\n"
            f"parent: {area}\n---\n# {line}\n\n{line}. Ask the {title.lower()} owner for anything this page does not "
            f"cover.\n\n1. Read the steps below before you start.\n2. Use the form on the intranet.\n3. Expect an answer "
            f"within five working days.\n", encoding="utf-8")
print(f"{len(spec)} areas added to {repo}")
