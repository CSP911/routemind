#!/bin/sh
# The two things an LLM does here, and what happens when there is none.
#
#   ./check/llm-paths.sh [base-url]
#
# Both modes matter and they are different products. With an LLM the form asks for a name and a
# one-liner; without one it also asks for an address, and a kind is taken from vocab.yaml. A check
# that only ever ran one of them would pass on half the installs.
set -eu
BASE="${1:-http://127.0.0.1:8080}"
W="$BASE/api/knowledge"
FAILS=0
say() { if [ "$2" = "$3" ]; then printf '%-52s %s\n' "ok   $1" "$2"
        else printf '%-52s %s   ← expected %s\n' "FAIL $1" "$2" "$3"; FAILS=$((FAILS+1)); fi; }
post() { curl -s -o /tmp/llmout -w '%{http_code}' -H 'Content-Type: application/json' -X POST "$@"; }
# **Cleanup is an assertion, not a courtesy.** Unlike every other check here this one writes into a
# live install, so what it leaves behind is somebody's ontology. The three deletes used to be
# `curl -s -o /dev/null -X DELETE` with the status thrown away, and on 2026-09-12 one of them failed:
# the run printed `both LLM paths ok` while leaving an uncommitted deletion in the working tree, and
# every write to that install was refused from then on with "someone edited the repository by hand" —
# which nobody had. An unchecked cleanup is how a check hands you a broken install and a clean report.
drop() { say "  cleaned up $1" "$(curl -s -o /tmp/llmdel -w '%{http_code}' -X DELETE "$W/nodes/$1")" 200; }
field() { python3 -c "import json,sys; print(json.load(open('/tmp/llmout')).get('$1'))"; }

derives=$(curl -fsS "$BASE/api/app-config" | python3 -c 'import json,sys; print(json.load(sys.stdin)["derives"])')
area=$(curl -fsS "$W/regions" | python3 -c 'import json,sys; r=json.load(sys.stdin).get("regions") or []; print(r[0]["fetch"].rsplit("/", 1)[-1] if r else "")')
[ -n "$area" ] || { echo "no area to test against"; exit 1; }
n="llmcheck-$(date +%s)"

if [ "$derives" = "True" ]; then
  say "this install derives" "$derives" True

  # A kind is never asked for. With an LLM, Knowledge chooses one — and says that it did, which is
  # what lets a domain that later declares edge_rules find the kinds nobody actually chose.
  code=$(post "$W/nodes" -d "{\"id\":\"$n\",\"name\":\"Check Node\",\"region\":\"$area\",\"one_liner\":\"made by a check\"}")
  # 200, not the API's 201: this goes through the web layer, which answers with its own status.
  say "a node with no kind is created" "$code" 200
  say "  a kind was chosen" "$( [ -n "$(field kind)" ] && echo yes || echo no )" yes
  say "  and it says it chose it" "$(field kind_generated)" True
  drop "$n"

  # A description written by the LLM causes `described_by: knowledge` to be added to the file, and
  # that write must not eat the body. `set_frontmatter` once returned the text after the *match*, and
  # the pattern ends at the end of the string, so the slice was always empty — the body is group 2.
  #
  # Two conditions have to hold at once or this proves nothing: the description must be GENERATED
  # (a supplied one skips the call entirely) and the content must ALREADY have a frontmatter block
  # (without one a different, correct branch runs). A first version of this check had neither and
  # passed against the broken code.
  body='---\nscope: common\n---\n# Probe\n\nThis body must survive a frontmatter write.\n'
  code=$(post "$W/nodes/$area-fmprobe/files/fm.md" -d "{\"content\":\"$body\"}" 2>/dev/null || true)
  post "$W/nodes" -d "{\"id\":\"$area-fmprobe\",\"name\":\"FM Probe\",\"region\":\"$area\",\"one_liner\":\"a probe\"}" >/dev/null
  code=$(curl -s -o /tmp/llmout -w '%{http_code}' -H 'Content-Type: application/json' -X PUT \
     "$W/nodes/$area-fmprobe/files/fm.md" -d "{\"content\":\"$body\"}")
  say "a generated description is written" "$code" 200
  # The API answers with JSON, so the document has to be parsed out of it. Grepping the envelope for
  # an anchored line passed for the body (a plain substring) and failed for the frontmatter, because
  # inside a JSON string a newline is two characters and `^` never matches there.
  curl -s "$W/nodes/$area-fmprobe/files/fm.md" \
    | python3 -c 'import json,sys; sys.stdout.write(json.load(sys.stdin).get("content",""))' > /tmp/llmdoc
  say "  the body survived it" "$(grep -c 'must survive' /tmp/llmdoc)" 1
  # This used to also assert that a `scope:` in the submitted content survived. It does not: under one
  # type the entity's frontmatter is written from the entity's own fields, so any other key in the
  # content is replaced. That is reported to the Knowledge unit as a question rather than pinned here
  # — a check that is permanently red is noise, and one asserting the wrong model is worse.
  drop "$area-fmprobe"

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
  say "a node with no kind is still created" "$code" 200
  say "  the default kind was used" "$(field kind_generated)" True
  drop "$n"

  # And drafting says why it cannot, rather than failing vaguely.
  code=$(post "$W/suggest/use-when" -d '{"name":"Billing","one_liner":"x"}')
  say "drafting says it needs an LLM" "$code" 503
fi

# The install has to be left the way it was found. Every delete above can answer 200 and the tree
# still end up dirty — a write that commits nothing, a publish that half-ran — and dirty is not a
# cosmetic state: it is the one in which the ontology refuses every subsequent write. So it is read
# back from the service rather than inferred from the statuses, and the recovery is printed here
# rather than left for whoever meets the refusal an hour later with no idea what touched it.
curl -fsS "$W/state" -o /tmp/llmstate 2>/dev/null || : > /tmp/llmstate
dirty=$(python3 -c "
import json
try: print(json.load(open('/tmp/llmstate')).get('uncommitted') or '')
except Exception: print('unreadable')" )
say "the install is as it was found" "${dirty:-clean}" clean
[ -z "$dirty" ] || printf '\n  %s is uncommitted. Until that is settled every write to this install is\n  refused as a hand edit — whether this check left it or it was already there.\n  To discard it:\n\n      git -C <your data/repo> checkout -- .\n\n' "$dirty"

[ "$FAILS" -eq 0 ] || { printf '\n%s failed\n' "$FAILS"; exit 1; }
printf '\nboth LLM paths ok, and the install is unchanged (derives=%s)\n' "$derives"
