#!/bin/sh
# Does this install work? Run it after `docker compose up -d`.
#
#   ./check/smoke.sh [base-url]
#
# Two halves, and the second is the one that matters: the API half proves the ontology accepts and
# publishes a write, the screen half proves the map draws what the API holds. An install where the
# API is perfect and the screen is blank is an install nobody can use.
set -e
BASE="${1:-http://127.0.0.1:8080}"
say() { printf '%s\n' "$*"; }

say "== API =="
curl -fsS "$BASE/api/app-config" >/dev/null && say "ok   config"
curl -fsS "$BASE/api/knowledge/regions" >/dev/null && say "ok   hop 0"
curl -fsS "$BASE/knowledge" >/dev/null && say "ok   the map page"
for f in knowledge.js knowledge.css i18n.js theme.css theme.js iris_ui.css; do
  curl -fsS -o /dev/null "$BASE/static/$f" || { say "FAIL static/$f"; exit 1; }
done
say "ok   static"

# A refusal has to carry its reasons through the proxy. Without this the screen prints "validation
# failed — nothing was written" and a person has no way to learn that their kind is not in the
# vocabulary. The screen is written to show `details[]`; the proxy used to drop it.
#
# It has to be a refusal that *has* reasons. A node aimed at an area that does not exist is rejected
# before validation ever runs and carries none — the first version of this check used one, and failed
# against a correct build.
area=$(curl -fsS "$BASE/api/knowledge/regions" | python3 -c 'import json,sys; r=json.load(sys.stdin).get("regions") or []; print(r[0]["fetch"].rsplit("/", 1)[-1] if r else "")')
if [ -z "$area" ]; then
  say "--   no areas yet; the refusal-reasons check needs one"
else
  reasons=$(curl -s -H 'Content-Type: application/json' -X POST "$BASE/api/knowledge/nodes" \
    -d "{\"id\":\"smoke-bad-kind\",\"name\":\"Smoke\",\"kind\":\"definitely-not-a-kind\",\"region\":\"$area\",\"one_liner\":\"x\"}" \
    | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d.get("details") or []))')
  if [ "$reasons" -ge 1 ]; then say "ok   a refusal carries its reasons"
  else say "FAIL a refusal arrived with no reasons — details[] is being dropped"; exit 1; fi
fi

# The state behind the status bar. It asked for service fragments unconditionally, and a standalone
# install has none — so it answered 502 and the bar silently lost the publish and validate state.
ps=$(curl -s -o /dev/null -w '%{http_code}' "$BASE/api/knowledge/publish-state")
[ "$ps" = 200 ] && say "ok   publish-state answers" || { say "FAIL publish-state answered $ps"; exit 1; }

# A move reaches Knowledge. The proxy used to drop `parent` on purpose, so a drag would have been
# answered "nothing to update" and moved nothing. Aimed at an id that does not exist, so it writes
# nothing: Knowledge's own "not found" is the proof the field got through, and a malformed parent is
# refused by the proxy before it goes anywhere.
mv=$(curl -s -o /dev/null -w '%{http_code}' -H 'Content-Type: application/json' -X PUT \
  "$BASE/api/knowledge/nodes/smoke-no-such-entity" -d '{"parent":"smoke-nowhere"}')
bad=$(curl -s -o /dev/null -w '%{http_code}' -H 'Content-Type: application/json' -X PUT \
  "$BASE/api/knowledge/nodes/smoke-no-such-entity" -d '{"parent":"Not An Id"}')
if [ "$mv" = 404 ] && [ "$bad" = 422 ]; then say "ok   a move reaches Knowledge"
else say "FAIL a move: expected 404 from Knowledge and 422 for a bad id, got $mv and $bad"; exit 1; fi

command -v node >/dev/null 2>&1 && node "$(dirname "$0")/i18n-check.mjs" | sed 's/^/  /'
# Static, so it runs here rather than in the screen half: a class with no rule is a bug the API
# cannot see and the fake DOM does not render.
command -v node >/dev/null 2>&1 && node "$(dirname "$0")/css-check.mjs" | sed 's/^/  /'

say "== an agent =="
if command -v python3 >/dev/null 2>&1; then
  cd "$(dirname "$0")/.." && ./check/mcp-check.py "$BASE/api/knowledge" | sed 's/^/  /'
else
  say "--   python3 not installed; skipping the agent half"
fi

# The popup — "what the agent is handed" — for every kind of thing on the map. It called a helper
# that only existed in the system this was split out of, so every click on a tile answered 500, and
# nothing noticed: the screen check draws the map but never opens a popup.
view_fail=0
area=$(curl -fsS "$BASE/api/knowledge/regions" | python3 -c 'import json,sys; r=json.load(sys.stdin).get("regions") or []; print(r[0]["fetch"].rsplit("/", 1)[-1] if r else "")')
targets=""
[ -n "$area" ] && targets=$(curl -fsS "$BASE/api/knowledge/regions/$area" \
  | python3 -c 'import json,sys; print(" ".join(e["fetch"] for e in (json.load(sys.stdin).get("entries") or [])))')
for t in "" "/v1/core" ${area:+/v1/regions/$area} $targets; do
  enc=$(python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=""))' "$t")
  st=$(curl -s "$BASE/api/knowledge/view?path=$enc&service=" \
       | python3 -c 'import json,sys; print(json.load(sys.stdin).get("status"))' 2>/dev/null || echo broken)
  [ "$st" = "ok" ] || { say "FAIL the popup for ${t:-hop 0} answered $st"; view_fail=1; }
done
[ "$view_fail" = 0 ] && say "ok   every tile's popup renders" || exit 1

# llm-probe.py is not run here: it needs a real provider and a real key, and a smoke test that
# silently skips itself is worse than one that is not there. `./check/llm-probe.py --help`.

say "== screen =="
command -v node >/dev/null 2>&1 || { say "--   node not installed; skipping the screen half"; exit 0; }
cd "$(dirname "$0")/.."
node check/screen-check.mjs "$BASE"
