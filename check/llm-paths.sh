#!/bin/sh
# The two things an LLM does here, and what happens when there is none.
#
#   ./check/llm-paths.sh [base-url]
#
# Both modes matter and they are different products. With an LLM the form asks for a name and a
# one-liner; without one it also asks for an address, and a kind is taken from vocab.yaml. A check
# that only ever ran one of them would pass on half the installs.
set -eu
. "$(dirname "$0")/base.sh"
BASE="${1:-$(checkout_base "$(dirname "$0")/..")}"
W="$BASE/api/knowledge"
FAILS=0
# Its own scratch files. Fixed /tmp/llm* paths let two runs from two checkouts read each other's answers.
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
# Every write this check makes that lands, counted, so the end can say what it wrote rather than that
# it wrote nothing: "the install is unchanged" was printed beside two new commits in the install's
# history (docs audit DC-2, 2026-11-02).
WROTE=0
say() { if [ "$2" = "$3" ]; then printf '%-52s %s\n' "ok   $1" "$2"
        else printf '%-52s %s   ← expected %s\n' "FAIL $1" "$2" "$3"; FAILS=$((FAILS+1)); fi; }
post() { curl -s -o "$T/out" -w '%{http_code}' -H 'Content-Type: application/json' -X POST "$@"; }
# **Cleanup is an assertion, not a courtesy.** Unlike every other check here this one writes into a
# live install, so what it leaves behind is somebody's ontology. The three deletes used to be
# `curl -s -o /dev/null -X DELETE` with the status thrown away, and on 2026-09-12 one of them failed:
# the run printed `both LLM paths ok` while leaving an uncommitted deletion in the working tree, and
# every write to that install was refused from then on with "someone edited the repository by hand" —
# which nobody had. An unchecked cleanup is how a check hands you a broken install and a clean report.
drop() { c="$(curl -s -o "$T/del" -w '%{http_code}' -X DELETE "$W/nodes/$1")"
         [ "$c" = 200 ] && WROTE=$((WROTE+1)); say "  cleaned up $1" "$c" 200; }
field() { python3 -c "import json,sys; print(json.load(open('$T/out')).get('$1'))"; }
# What the map holds, without the revision: the content an agent reads, which this check must leave as
# it found it — the history it adds to cannot be taken back through the API, and is reported instead.
held() { curl -fsS "$W/graph" | python3 -c 'import json,sys,hashlib; d=json.load(sys.stdin); d.pop("revision",None); print(hashlib.sha1(json.dumps(d,sort_keys=True).encode()).hexdigest())'; }
head_now() { curl -fsS "$W/revision" | python3 -c 'import json,sys; print((json.load(sys.stdin).get("head") or "")[:7])'; }

derives=$(curl -fsS "$BASE/api/app-config" | python3 -c 'import json,sys; print(json.load(sys.stdin)["derives"])')
area=$(curl -fsS "$W/regions" | python3 -c 'import json,sys; r=json.load(sys.stdin).get("regions") or []; print(r[0]["fetch"].rsplit("/", 1)[-1] if r else "")')
[ -n "$area" ] || { echo "no area to test against"; exit 1; }
n="llmcheck-$(date +%s)"
HELD0="$(held)"; HEAD0="$(head_now)"

if [ "$derives" = "True" ]; then
  say "this install derives" "$derives" True

  # A kind is never asked for. With an LLM, Knowledge chooses one — and says that it did, so the
  # kinds nobody actually chose can be found later.
  code=$(post "$W/nodes" -d "{\"id\":\"$n\",\"name\":\"Check Node\",\"region\":\"$area\",\"one_liner\":\"made by a check\"}")
  [ "$code" = 200 ] && WROTE=$((WROTE+1))
  # 200, not the API's 201: this goes through the web layer, which answers with its own status.
  say "a node with no kind is created" "$code" 200
  say "  a kind was chosen" "$( [ -n "$(field kind)" ] && echo yes || echo no )" yes
  say "  and it says it chose it" "$(field kind_generated)" True
  drop "$n"

  # The line a document is chosen by is a person's, LLM or not (2026-10-07). It used to be written
  # here by the LLM when a raw API caller left it out; the screen never did, and the ✨ Suggest
  # button is how a draft is asked for. Refused before anything is written, so nothing to clean up.
  rep=$(curl -fsS "$W/regions" | python3 -c 'import json,sys; r=json.load(sys.stdin).get("regions") or []; print(r[0].get("representative") or "" if r else "")')
  code=$(curl -s -o "$T/out" -w '%{http_code}' -H 'Content-Type: application/json' -X PUT \
     "$W/nodes/$rep/files/llmcheck-nodesc.md" -d '{"content":"# Probe"}')
  say "a new file with no description is refused, LLM or not" "$code" 400

  # Drafting the one line an agent routes on.
  code=$(post "$W/suggest/use-when" -d '{"name":"Billing","one_liner":"where a payment goes until it settles"}')
  say "a condition can be drafted" "$code" 200
  say "  it came back non-empty" "$( [ -n "$(field use_when)" ] && echo yes || echo no )" yes
  code=$(post "$W/suggest/use-when" -d '{"name":"Billing"}')
  say "drafting without a one-liner is refused" "$code" 422
else
  say "this install does not derive" "$derives" False

  # No LLM: a kind still must not be asked for, so vocab.yaml's default_kind supplies it.
  code=$(post "$W/nodes" -d "{\"id\":\"$n\",\"name\":\"Check Node\",\"region\":\"$area\",\"one_liner\":\"made by a check\"}")
  [ "$code" = 200 ] && WROTE=$((WROTE+1))
  say "a node with no kind is still created" "$code" 200
  say "  the default kind was used" "$(field kind_generated)" True
  drop "$n"

  # And drafting says why it cannot, rather than failing vaguely.
  code=$(post "$W/suggest/use-when" -d '{"name":"Billing","one_liner":"x"}')
  say "drafting says it needs an LLM" "$code" 503
fi

# The install has to be left the way it was found. Every delete above can answer 200 and the tree
# still end up dirty — a write that commits nothing — and dirty is not a
# cosmetic state: it is the one in which the ontology refuses every subsequent write. So it is read
# back from the service rather than inferred from the statuses, and the recovery is printed here
# rather than left for whoever meets the refusal an hour later with no idea what touched it.
curl -fsS "$W/state" -o "$T/state" 2>/dev/null || : > "$T/state"
dirty=$(python3 -c "
import json
try: print(json.load(open('$T/state')).get('uncommitted') or '')
except Exception: print('unreadable')" )
say "the install is as it was found" "${dirty:-clean}" clean
[ -z "$dirty" ] || printf '\n  %s is uncommitted. Until that is settled every write to this install is\n  refused as a hand edit — whether this check left it or it was already there.\n  To discard it:\n\n      git -C <your data/repo> checkout -- .\n\n' "$dirty"

say "the map holds what it held" "$( [ "$(held)" = "$HELD0" ] && echo same || echo changed )" same

[ "$FAILS" -eq 0 ] || { printf '\n%s failed\n' "$FAILS"; exit 1; }
# Said exactly. The content is as it was; the history is not, and a commit cannot be taken back through
# the API — "the install is unchanged" about an install with two new commits was the false part.
printf '\nboth LLM paths ok (derives=%s). The map holds what it held; the history at %s gained\n' "$derives" "$BASE"
printf 'the %s commit(s) this check made, creating and deleting %s (head %s → %s).\n' "$WROTE" "$n" "$HEAD0" "$(head_now)"
