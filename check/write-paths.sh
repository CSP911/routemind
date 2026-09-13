#!/bin/sh
# Every write path, against a throwaway ontology seeded from seed/.
#
#   ./check/write-paths.sh [port]
#
# What it proves, and why each one is here:
#   * a write commits AND publishes, in one step — a commit that does not publish is invisible
#   * a refused write leaves the tree clean and publishes nothing — the failure that corrupts is the
#     one that half-succeeds
#   * the first area can be created into an empty CORE table — the chicken-and-egg every new install
#     would otherwise hit
#   * a name that is not ASCII survives onto the commit — it used to become "web" silently
#   * a move changes both routing tables in one write — across areas too — and a loop is refused
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT="${1:-8109}"
T="$(mktemp -d)"

# This one starts the service itself rather than talking to the running container, so it needs the
# service's dependency on the machine running it. Without this it dies on an ImportError traceback
# from inside store.py, which reads as "the check is broken" rather than "install a package".
python3 -c 'import yaml' 2>/dev/null || {
  echo "write-paths.sh starts the ontology itself and needs pyyaml on this python:" >&2
  echo "  python3 -m pip install pyyaml     (or run it where the service's deps already are)" >&2
  exit 2
}
command -v curl >/dev/null || { echo "write-paths.sh needs curl" >&2; exit 2; }
trap 'kill ${PID:-0} 2>/dev/null || true; rm -rf "$T"' EXIT

cp -r "$ROOT/seed/." "$T/repo/" 2>/dev/null || { mkdir -p "$T/repo"; cp -r "$ROOT/seed/." "$T/repo/"; }
mkdir -p "$T/publish"
git -C "$T/repo" init -q
git -C "$T/repo" add -A
# Every commit here names its own author. Without that, a machine with no global git identity —
# CI, a container, a fresh checkout — aborts partway through with "Author identity unknown".
git -C "$T/repo" -c user.name=seed -c user.email=seed@local commit -qm seed

ONTOLOGY_DATA="$T/repo" ONTOLOGY_PUBLISH="$T/publish" PORT="$PORT" \
  python3 "$ROOT/ontology/service/server.py" >"$T/log" 2>&1 &
PID=$!
U="http://127.0.0.1:$PORT/v1"
i=0; while [ $i -lt 40 ]; do curl -fsS -o /dev/null "$U/../healthz" 2>/dev/null && break; sleep 0.25; i=$((i+1)); done

FAILS=0
say() { if [ "$2" = "$3" ]; then printf '%-56s %s\n' "ok   $1" "$2"
        else printf '%-56s %s   ← expected %s\n' "FAIL $1" "$2" "$3"; FAILS=$((FAILS+1)); fi; }
# The actor is deliberately a name that cannot be encoded in latin-1 — that is the whole point of the
# check. A name with accents would pass even with the bug, because latin-1 covers it; only a
# non-Latin script catches the header encoding. Percent-encoded, as the web app sends it.
code() { curl -s -o "$T/out" -w '%{http_code}' -H 'Content-Type: application/json' -H 'X-Actor: %EC%B2%9C%EC%88%98' "$@"; }
published() { cat "$T/publish/REVISION" 2>/dev/null || echo none; }

BEFORE="$(published)"
say "the empty seed validates" "$(curl -s "$U/validate" | python3 -c 'import json,sys; print(json.load(sys.stdin)["ok"])')" True

# The first area, into a CORE table that has a header and no rows.
say "first area into an empty CORE table" "$(code -X POST "$U/regions" -d '{"source":"alpha","core_description":"the first area","representative":{"id":"alpha-core","kind":"system","name":"Alpha","one_liner":"what alpha is","use_when":"when alpha is the question"}}')" 201
say "  it published"                      "$( [ "$(published)" != "$BEFORE" ] && echo moved || echo stuck )" moved
say "  CORE has exactly one row"          "$(grep -c '^| `ALPHA` |' "$T/repo/CORE.md")" 1
say "  hop 0 lists it"                    "$(curl -s "$U/regions" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["regions"]))')" 1
say "  a non-ASCII actor reached git"     "$(git -C "$T/repo" log -1 --pretty=%an)" "천수"

# A refused write must leave nothing behind — not a file, not a commit, not a publish.
HEAD_OK="$(git -C "$T/repo" rev-parse HEAD)"
say "node with a kind outside the vocabulary" "$(code -X POST "$U/nodes" -d '{"id":"bad-kind","name":"Bad","kind":"not-a-kind","region":"alpha","one_liner":"x"}')" 422
say "  no commit was made"                "$(git -C "$T/repo" rev-parse HEAD)" "$HEAD_OK"
say "  the tree is clean"                 "$(git -C "$T/repo" status --porcelain | wc -l | tr -d ' ')" 0
say "  and it does not exist"             "$(curl -s -o /dev/null -w '%{http_code}' "$U/nodes/bad-kind")" 404

say "node into an area that does not exist" "$(code -X POST "$U/nodes" -d '{"id":"orphan","name":"Orphan","kind":"system","region":"nowhere","one_liner":"x"}')" 400
say "  the tree is still clean"           "$(git -C "$T/repo" status --porcelain | wc -l | tr -d ' ')" 0

# An id is a permanent address with no rename path. A name whose every letter is ASCII answers for
# itself — `No Id` is `no-id`, with no model asked (13934d8: asking one turned `Parcels` into
# `tracking-system`). A name a regex cannot take needs the translator, and with no LLM that is a 503
# (not configured), never a 422 and never a guess.
say "an ASCII name gives the id, no LLM"  "$(code -X POST "$U/nodes" -d '{"name":"No Id","kind":"system","region":"alpha","one_liner":"x"}')" 201
say "  it is the name, and nobody guessed" "$(python3 -c 'import json; d=json.load(open("'"$T"'/out")); print(d["id"], d["id_generated"])')" "no-id False"
# Non-ASCII is no longer the line. `romanize` handles what is mechanical — Latin with marks, hangul,
# kana — so a Korean team no longer types an id by hand for every entity while an English one types
# none. What it refuses is what needs a dictionary of readings rather than a rule, and this is that:
# 小包 is the same word as the 소포 that used to be here, in the script that cannot be read from its
# own characters.
say "a hangul name gives the id, no LLM"   "$(code -X POST "$U/nodes" -d '{"name":"소포","kind":"system","region":"alpha","one_liner":"x"}')" 201
say "  and it is a legible address"        "$(python3 -c 'import json; d=json.load(open("'"$T"'/out")); print(d["id"], d["id_generated"])')" "sopo False"
say "a kana name gives one too"            "$(code -X POST "$U/nodes" -d '{"name":"こづつみ","kind":"system","region":"alpha","one_liner":"x"}')" 201
say "  and Latin with marks"               "$(code -X POST "$U/nodes" -d '{"name":"Küçük Paket","kind":"system","region":"alpha","one_liner":"x"}')" 201
say "  spelt as somebody would read it"    "$(python3 -c 'import json; d=json.load(open("'"$T"'/out")); print(d["id"])')" "kucuk-paket"
say "a han name with no LLM refuses"       "$(code -X POST "$U/nodes" -d '{"name":"小包","kind":"system","region":"alpha","one_liner":"x"}')" 503
# A kind is different: nothing reads one until a domain declares edge_rules, so vocab.yaml supplies
# a default and the screen never asks. It is still recorded as not chosen by anyone.
say "no kind takes the default"           "$(code -X POST "$U/nodes" -d '{"id":"no-kind","name":"No Kind","region":"alpha","one_liner":"x"}')" 201
say "  and says nobody chose it"          "$(python3 -c 'import json; d=json.load(open("'"$T"'/out")); print(d["kind"], d["kind_generated"])')" "system True"
# And with no default declared, it refuses rather than inventing one. Done by editing the throwaway
# repository the way a person would — including the commit, without which every write is blocked.
# `sed -i` without an argument is GNU-only: BSD sed reads the next word as the backup suffix and the
# file as the script, and answers `invalid command code f`. With `set -e` that ended the run right
# here — so on macOS, where the README sends contributors to run this, everything below this line had
# never executed. Half the file. A check that stops early and says nothing is worse than no check.
edit_vocab() { python3 - "$T/repo/vocab.yaml" "$1" "$2" <<'EOF'
import sys
p, old, new = sys.argv[1:4]
s = open(p, encoding="utf-8").read()
assert old in s, f"{old!r} not in vocab.yaml"
open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))
EOF
}
edit_vocab "default_kind: system" "# no default"
git -C "$T/repo" -c user.name=seed -c user.email=seed@local commit -qam "drop default_kind"
say "  with no default_kind it refuses"   "$(code -X POST "$U/nodes" -d '{"id":"no-default","name":"X","region":"alpha","one_liner":"x"}')" 503
edit_vocab "# no default" "default_kind: system"
git -C "$T/repo" -c user.name=seed -c user.email=seed@local commit -qam "restore default_kind"

# The ordinary path, end to end.
say "node with its first edge (one txn)"  "$(code -X POST "$U/nodes" -d '{"id":"beta","name":"Beta","kind":"tool","region":"alpha","one_liner":"what beta is","edges":[{"from":"alpha-core","rel":"CONSISTS_OF","to":"beta"}]}')" 201
# One entity is one file. The old shape put a node in a directory with an INDEX.md and its documents
# beside it, so these lines checked for that directory; an entity is `regions/<area>/<id>.md` now.
# What they were really checking — that the write reached disk, and in the format the reader expects —
# is what they check here.
say "  it is one file on disk"            "$( [ -f "$T/repo/regions/alpha/beta.md" ] && echo yes || echo no )" yes
say "  it declares its own id"            "$(grep -c '^id: beta$' "$T/repo/regions/alpha/beta.md")" 1
say "a file needs a description with no LLM" "$(code -X PUT "$U/nodes/beta/files/x.md" -d '{"content":"# x"}')" 503
say "  with one, it is written"           "$(code -X PUT "$U/nodes/beta/files/x.md" -d '{"description":"what x holds","content":"# x"}')" 200
# Hierarchy is declared by the child, not listed by the parent — so a list and the directory can no
# longer disagree. `beta` is directly in the area and has no parent; `x` hangs under it and says so.
say "  the child declares its parent"     "$(grep -c '^parent: beta$' "$T/repo/regions/alpha/x.md")" 1
say "  and the routing table carries its fetch" "$(curl -s "$U/regions/alpha" | python3 -c 'import json,sys; print(any(e.get("fetch") for e in json.load(sys.stdin)["entries"]))')" True

# Promotion makes room for a sibling. One document was enough on its own; a second arrives that
# belongs with it, so a container is created — named by the person — and the first moves under it.
# That is what the button was designed for, and under one type it is cheap: the promoted entity keeps
# its id, its name and its body, so nothing that pointed at it has to move.
#
# It creates an entity, so it needs a name for it — the same rule as `POST /v1/nodes`, and the same
# refusal when there is neither an id nor an LLM to derive one. Refusing beats the quiet alternative,
# which was renaming the document to what the container should have been called.
say "promotion, untranslatable, no LLM"  "$(code -X POST "$U/nodes/beta/files/x.md/promote" -d '{"name":"束","one_liner":"what groups them"}')" 503
say "promotion makes the container"       "$(code -X POST "$U/nodes/beta/files/x.md/promote" -d '{"id":"group","name":"Group","one_liner":"what groups them"}')" 201
say "  it answers with the new container" "$(python3 -c 'import json; print(json.load(open("'"$T"'/out"))["id"])')" group
say "  the container stands where x stood" "$(curl -s "$U/nodes/group" | python3 -c 'import json,sys; print(json.load(sys.stdin)["parent"])')" beta
say "  x kept its own address"            "$(curl -s -o /dev/null -w '%{http_code}' "$U/nodes/x")" 200
say "  and now hangs under the container" "$(curl -s "$U/nodes/x" | python3 -c 'import json,sys; print(json.load(sys.stdin)["parent"])')" group
say "  its body came along"               "$(curl -s "$U/nodes/x/body" | grep -c '^# x')" 1
# Nothing had to be repointed, which is the part two types made expensive: the old promotion minted a
# new id for the document, so every edge naming it had to be rewritten in the same transaction.
say "  no edge had to move"               "$(curl -s "$U/edges" | python3 -c 'import json,sys; print(sum(1 for e in json.load(sys.stdin)["edges"] if "group" in (e["from"], e["to"])))')" 0

# Moving an entity: drag it onto what should hold it. Containment is one field, and both routing
# tables are read off it — so one write has to take the entity out of the table it was in and put it
# into the one it joined, keep its address, and publish. Into another area too (operator, 2026-09-11):
# the area is the directory, which follows from the parent, so the file moves with it. And the move
# Knowledge must refuse, refused with nothing left behind: into something inside itself.
ids_in() { curl -s "$U/$1" | python3 -c 'import json,sys; print(" ".join(sorted(e["id"] for e in json.load(sys.stdin)["entries"])))'; }
say "move x out of group, into beta"       "$(code -X PUT "$U/nodes/x" -d '{"parent":"beta"}')" 200
say "  beta's table lists it"              "$(ids_in nodes/beta | tr ' ' '\n' | grep -cx x)" 1
say "  group's table does not"             "$(ids_in nodes/group | tr ' ' '\n' | grep -cx x || true)" 0
say "  it kept its address and body"       "$(curl -s "$U/nodes/x/body" | grep -c '^# x')" 1
say "  and the move was published"        "$(published)" "$(git -C "$T/repo" rev-parse HEAD)"
say "move x to the representative"         "$(code -X PUT "$U/nodes/x" -d '{"parent":"alpha-core"}')" 200
say "  the area's own table lists it"      "$(ids_in regions/alpha | tr ' ' '\n' | grep -cx x)" 1
HEAD_OK="$(git -C "$T/repo" rev-parse HEAD)"
say "beta into group, which is inside it"  "$(code -X PUT "$U/nodes/beta" -d '{"parent":"group"}')" 409
say "  nothing was committed"              "$(git -C "$T/repo" rev-parse HEAD)" "$HEAD_OK"
say "  the tree is clean"                  "$(git -C "$T/repo" status --porcelain | wc -l | tr -d ' ')" 0
code -X POST "$U/regions" -d '{"source":"gamma","core_description":"a second area","representative":{"id":"gamma-core","kind":"system","name":"Gamma","one_liner":"what gamma is","use_when":"when gamma is the question"}}' >/dev/null
say "x into another area"                  "$(code -X PUT "$U/nodes/x" -d '{"parent":"gamma-core"}')" 200
say "  its file moved with it"             "$( [ -f "$T/repo/regions/gamma/x.md" ] && [ ! -e "$T/repo/regions/alpha/x.md" ] && echo moved || echo not)" moved
say "  gamma's table lists it"             "$(ids_in regions/gamma | tr ' ' '\n' | grep -cx x)" 1
say "  alpha's does not"                   "$(ids_in regions/alpha | tr ' ' '\n' | grep -cx x || true)" 0
say "  same address, same body"            "$(curl -s "$U/nodes/x/body" | grep -c '^# x')" 1
say "  and it validates"                   "$(curl -s "$U/validate" | python3 -c 'import json,sys; print(json.load(sys.stdin)["ok"])')" True
say "an area's representative stays"       "$(code -X PUT "$U/nodes/alpha-core" -d '{"parent":"gamma-core"}')" 409
code -X DELETE "$U/nodes/x" >/dev/null
say "the second area goes again"           "$(code -X DELETE "$U/regions/gamma")" 200

# Clearing an area and starting over. This ships with example areas, so removing them is the first
# thing a real user does, and the cycle has to close: the API refuses while anything is still inside,
# an empty CORE table must survive the last removal, and the next area has to be creatable into it.
say "an area with contents refuses"        "$(code -X DELETE "$U/regions/alpha")" 409
say "  and says what is in the way"        "$(python3 -c 'import json; print("nodes remain" in json.load(open("'"$T"'/out")).get("error",""))')" True
# Ask what is in there rather than listing what this file happens to have created — a hardcoded list
# goes stale the moment a check above it adds one more, and the symptom is this delete quietly
# failing. Children first: a parent refuses while something hangs under it.
for n in $(curl -s "$U/nodes" | python3 -c '
import json, sys
ns = [n for n in json.load(sys.stdin)["nodes"] if n.get("region") == "alpha" and n.get("role") != "representative"]
print(" ".join(n["id"] for n in sorted(ns, key=lambda n: -len(n.get("parent") or ""))))'); do
  code -X DELETE "$U/nodes/$n" >/dev/null
done
say "emptied, the area goes"               "$(code -X DELETE "$U/regions/alpha")" 200
say "  the CORE row went with it"          "$(grep -c '^| `ALPHA` |' "$T/repo/CORE.md")" 0
say "  the table header survived"          "$(grep -cE '^\|[ \t]*:?-+:?[ \t]*\|' "$T/repo/CORE.md")" 1
say "  and nothing is advertised"          "$(curl -s "$U/regions" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["regions"]))')" 0
# The chicken-and-egg again, from the other direction: a tree emptied by deleting must be as usable
# as a tree that was never filled.
say "a new area goes into the empty table" "$(code -X POST "$U/regions" -d '{"source":"mine","core_description":"my own","representative":{"id":"mine-core","kind":"system","name":"Mine","one_liner":"what it is","use_when":"when to come here"}}')" 201
say "  hop 0 shows it and nothing else"    "$(curl -s "$U/regions" | python3 -c 'import json,sys; r=json.load(sys.stdin)["regions"]; print(len(r), r[0]["fetch"].rsplit("/",1)[-1])')" "1 mine"

say "everything still validates"          "$(curl -s "$U/validate" | python3 -c 'import json,sys; print(json.load(sys.stdin)["ok"])')" True
say "published head matches git head"     "$(published)" "$(git -C "$T/repo" rev-parse HEAD)"

[ "$FAILS" -eq 0 ] || { printf '\n%s failed\n' "$FAILS"; exit 1; }
printf '\nall write paths ok\n'
