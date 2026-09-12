#!/usr/bin/env python3
"""Every setting .env.example documents must actually reach a container.

    ./check/env-check.py

A variable named in .env.example that docker-compose.yml never passes through is a dead setting: the
person sets it, nothing reads it, and there is no error anywhere to tell them. Two of these have
shipped.

  * ONTOLOGY_HARNESS was never in docker-compose.yml, so `POST /v1/curator/proposals` answered 501 on
    every install ever made from that file. The review queue behind "Advertise upstream" — the only
    path that writes a `use_when` — had never worked, and the screen showed the operator the name of
    a variable that was not theirs to set.
  * .env.example is itself the other half: it did not exist at all, while README and install.sh both
    told people to copy it, so a fresh clone died on line 1.

Both directions are wrong, so both are checked. A variable compose passes that .env.example never
mentions is a setting nobody can discover; those go in UNDOCUMENTED with the reason.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
env_text = (ROOT / ".env.example").read_text(encoding="utf-8")
# Every compose file, not just the main one. The overlays that add a second backbone and an exchange
# read settings too, and a setting only they name is exactly as dead as one nothing names — it was
# only ever checked in the file that happened to exist when this was written.
COMPOSE = sorted(ROOT.glob("docker-compose*.yml"))
compose = "\n".join(p.read_text(encoding="utf-8") for p in COMPOSE)

# Both the set and the commented-out forms: a commented default is still a documented setting.
documented = {m.group(1) for m in re.finditer(r"^#?\s*([A-Z][A-Z0-9_]*)=", env_text, re.M)}
# Anything compose interpolates from the environment — `${NAME}` or `${NAME:-default}`.
passed = {m.group(1) for m in re.finditer(r"\$\{([A-Z][A-Z0-9_]*)", compose)}

# Passed through but deliberately not in .env.example. Each line is a decision.
UNDOCUMENTED = {}

dead = sorted(documented - passed)
hidden = sorted(v for v in passed - documented if v not in UNDOCUMENTED)
stale = sorted(v for v in UNDOCUMENTED if v in documented or v not in passed)

for v in sorted(UNDOCUMENTED):
    if v not in stale: print(f"--   {v} is not in .env.example, on purpose — {UNDOCUMENTED[v]}")
for v in stale: print(f"--   {v} is in UNDOCUMENTED but no longer needs to be; drop the entry")

bad = False
if dead:
    bad = True
    print("FAIL .env.example documents settings no compose file passes to a container:\n  " +
          "\n  ".join(dead) + "\n  Someone sets these and nothing reads them, with no error anywhere.")
if hidden:
    bad = True
    print("FAIL a compose file reads settings .env.example never mentions:\n  " +
          "\n  ".join(hidden) + "\n  Either document them, or add them to UNDOCUMENTED here with the reason.")
if bad: sys.exit(1)
print(f"ok   {len(documented)} settings documented, every one reaching a container ({len(COMPOSE)} compose files)")
