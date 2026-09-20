#!/bin/bash
# Walk every question in a gold file, one fresh headless session each.
#
# The routing arm was a sample of 50 because the operator was spawning agents by hand. That made the
# comparison lopsided: `rag` is a census of 700 with no sampling error, `routing` was 50 walks, and
# only one of those two numbers carries an interval. This runs the same walk over the whole gold set
# so both sides have the same denominator.
#
# **One question, one process.** `claude -p` starts a session with nothing in it, so no walk can
# learn from the walk before it. Batching questions into one agent would be far cheaper and would
# also quietly invalidate the arm — an agent on its tenth accrual question already knows where the
# revision legend lives, and that is not what is being measured.
#
#     ./bench/walkcensus.sh eval/gold/hard.yaml routing 4
#     ./bench/walkcensus.sh eval/gold/hard-temporal.yaml routing+overlay 4
#
# Resumable: reports already on disk are not re-walked, and questions already recorded are skipped.
# Reports are the arm's raw data and are kept, not temp files.

# Everything lives inside main(), and main is called on the last line. Bash reads a script
# incrementally by byte offset, so editing one while it runs shifts every offset after the edit and
# the shell resumes in the middle of whatever now sits there — which is how the first census died,
# landing inside a heredoc with `syntax error near unexpected token`. Wrapped in a function, bash
# parses the whole file before executing a line of it, and an edit mid-run is harmless.
main() {
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1

local GOLD="${1:?usage: walkcensus.sh <gold.yaml> [arm] [parallel]}"
local ARM="${2:-routing}"
local PAR="${3:-4}"
local CAMPAIGN="${BENCH_CAMPAIGN:-2026-09-20-census}"
local OUT="${BENCH_WALKS:-eval/runs/walks-census}"
: "${BENCH_PYLIB:?set BENCH_PYLIB to the directory holding pyyaml}"
export BENCH_PYLIB
# rmcli.py puts BENCH_PYLIB on its own path; walkprompt.py and walkscore.py import yaml directly and
# need it on PYTHONPATH. Both are needed, for different programs.
export PYTHONPATH="$BENCH_PYLIB${PYTHONPATH:+:$PYTHONPATH}"
export BENCH_USE_WHEN="${BENCH_USE_WHEN:-maintained}"

mkdir -p "$OUT"
local SUFFIX="" OVERLAY=""
[ "$ARM" = "routing+overlay" ] && { SUFFIX="-overlay"; OVERLAY="--overlay"; }

# The fingerprint the walks run against, checked before the first one rather than after the last.
local FP WANT
FP=$(cat data/bench-repo/FINGERPRINT 2>/dev/null)
WANT=$(cat bench/corpus-hard/.fingerprint 2>/dev/null)
[ -n "$FP" ] && [ "$FP" = "$WANT" ] || { echo "  fingerprint mismatch: served=$FP want=$WANT"; exit 1; }
echo "  $GOLD · $ARM · $PAR at a time · fingerprint $FP · hop 0 $BENCH_USE_WHEN"

local ALL DONE TODO N
ALL=$(python3 -c "
import sys, yaml
print(chr(10).join(q['id'] for q in yaml.safe_load(open('$GOLD'))['questions']))")
DONE=$(python3 -c "
import json, pathlib
p = pathlib.Path('eval/runs/$CAMPAIGN.json')
d = json.loads(p.read_text()) if p.exists() else {'walks': []}
print(chr(10).join(w['id'] for w in d['walks'] if w['arm'] == '$ARM'))")
TODO=$(comm -23 <(echo "$ALL" | sort) <(echo "$DONE" | sort) | sort)
N=$(echo "$TODO" | grep -c .)
echo "  $N to do ($(echo "$DONE" | grep -c .) already recorded)"
[ "$N" -eq 0 ] && return 0

# Record first, walk second. 378 finished walks were lost to a crash because recording only happened
# after every walk returned. A report on disk is a completed walk and belongs in the campaign file
# immediately, whatever happens to the rest of the run.
record_existing "$TODO" "$OUT" "$SUFFIX" "$ARM" "$CAMPAIGN"

TODO=$(comm -23 <(echo "$ALL" | sort) <(python3 -c "
import json, pathlib
p = pathlib.Path('eval/runs/$CAMPAIGN.json')
d = json.loads(p.read_text()) if p.exists() else {'walks': []}
print(chr(10).join(sorted(w['id'] for w in d['walks'] if w['arm'] == '$ARM')))") | sort)
N=$(echo "$TODO" | grep -c .)
[ "$N" -eq 0 ] && { echo "  nothing left to walk"; return 0; }
echo "  $N to walk"

cat > "$OUT/.walk.sh" <<'WALK'
#!/bin/bash
qid="$1"
# An empty id must not reach this. It did once, from a debugging shell where $qid was unset, and
# produced a complete, plausible-looking report belonging to no question. Nothing downstream would
# have caught it: it is not missing from the census, it is extra, and extra is invisible to a count
# of what is missing.
[ -n "$qid" ] || { echo "  empty question id — refusing to walk" >&2; exit 2; }
f="$OUT/walk-$qid$SUFFIX.md"
[ -s "$f" ] && exit 0
prompt=$(python3 ./bench/walkprompt.py "$qid" $OVERLAY --out "$f") || exit 1
# Two attempts. 262 walks of the first census returned nothing at all — the provider refused them
# under load, and a refusal is indistinguishable from a walk that found nothing until you notice
# that no report was written. One retry after a pause turns most of those back into data.
for attempt in 1 2; do
  claude -p "$prompt" --model sonnet     --allowed-tools "Bash(./bench/rmcli.py:*)" "Write"     --permission-mode acceptEdits --max-turns 40 >/dev/null 2>&1
  [ -s "$f" ] && exit 0
  [ "$attempt" = 1 ] && sleep 20
done
# The reply is discarded on purpose. The file is the deliverable, and scoring whatever the agent
# happened to say instead is how four early walks got summarised into a hit that hid a real defect.
echo "$qid" >> "$OUT/.failed"
echo "  no report after 2 attempts: $qid" >&2
WALK
chmod +x "$OUT/.walk.sh"
export OUT SUFFIX OVERLAY
: > "$OUT/.failed"

echo "$TODO" | grep . | xargs -P "$PAR" -n1 "$OUT/.walk.sh"

record_existing "$TODO" "$OUT" "$SUFFIX" "$ARM" "$CAMPAIGN"

# A census that quietly loses walks is worse than one that stops. Say how many, and fail.
local FAILED
# grep -c on an empty file prints 0 and exits 1, so `|| echo 0` appended a second 0 and the test
# below got "0\n0" and raised. Count lines without letting grep's exit status into the value.
FAILED=$(wc -l < "$OUT/.failed" 2>/dev/null | tr -d " ")
FAILED=${FAILED:-0}
if [ "$FAILED" -gt 0 ]; then
  echo "  $FAILED questions produced no report — listed in $OUT/.failed"
  echo "  re-run this same command to retry only those"
  return 3
fi
echo "  complete"
}

record_existing() {
  local todo="$1" out="$2" suffix="$3" arm="$4" campaign="$5" qid f n=0
  for qid in $todo; do
    f="$out/walk-$qid$suffix.md"
    [ -s "$f" ] || continue
    python3 ./bench/walkscore.py --campaign "$campaign" record --id "$qid" --arm "$arm" < "$f" >/dev/null
    n=$((n+1))
  done
  [ "$n" -gt 0 ] && echo "  recorded $n report(s) already on disk"
  return 0
}

main "$@"
