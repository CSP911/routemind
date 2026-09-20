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
#     ./bench/walkcensus.sh eval/gold/hard.yaml routing 8
#     ./bench/walkcensus.sh eval/gold/hard-temporal.yaml routing+overlay 8
#
# Resumable: a question already recorded in the campaign is skipped, so a killed run is restarted by
# running it again. Reports land in $OUT and are kept — they are the arm's raw data, not a temp file.
set -u
cd "$(dirname "$0")/.." || exit 1

GOLD="${1:?usage: walkcensus.sh <gold.yaml> [arm] [parallel]}"
ARM="${2:-routing}"
PAR="${3:-8}"
CAMPAIGN="${BENCH_CAMPAIGN:-2026-09-20-census}"
OUT="${BENCH_WALKS:-eval/runs/walks-census}"
: "${BENCH_PYLIB:?set BENCH_PYLIB to the directory holding pyyaml}"
export BENCH_PYLIB
export BENCH_USE_WHEN="${BENCH_USE_WHEN:-maintained}"
PY="PYTHONPATH=$BENCH_PYLIB python3"

mkdir -p "$OUT"
SUFFIX=""; OVERLAY=""
[ "$ARM" = "routing+overlay" ] && { SUFFIX="-overlay"; OVERLAY="--overlay"; }

# The fingerprint the walks are run against, recorded before the first one rather than after the
# last. A census that straddles two corpora is the failure this whole harness was built around.
FP=$(cat data/bench-repo/FINGERPRINT 2>/dev/null)
WANT=$(cat bench/corpus-hard/.fingerprint 2>/dev/null)
[ -n "$FP" ] && [ "$FP" = "$WANT" ] || { echo "  fingerprint mismatch: served=$FP want=$WANT"; exit 1; }
echo "  $GOLD · $ARM · $PAR at a time · fingerprint $FP · hop 0 $BENCH_USE_WHEN"

ALL=$(PYTHONPATH=$BENCH_PYLIB python3 -c "
import sys, yaml
print('\n'.join(q['id'] for q in yaml.safe_load(open('$GOLD'))['questions']))")
DONE=$(PYTHONPATH=$BENCH_PYLIB python3 -c "
import json, pathlib
p = pathlib.Path('eval/runs/$CAMPAIGN.json')
d = json.loads(p.read_text()) if p.exists() else {'walks': []}
print('\n'.join(w['id'] for w in d['walks'] if w['arm'] == '$ARM'))")
TODO=$(comm -23 <(echo "$ALL" | sort) <(echo "$DONE" | sort) | sort)
N=$(echo "$TODO" | grep -c . )
echo "  $N to walk ($(echo "$DONE" | grep -c .) already recorded)"
[ "$N" -eq 0 ] && exit 0

# One walk, as a script on disk rather than an exported shell function: `export -f` needs the parent
# to be bash, and the first run of this was launched from zsh, where the function simply did not
# exist in the child and sixty walks "finished" in four seconds having done nothing at all.
cat > "$OUT/.walk.sh" <<'WALK'
#!/bin/bash
qid="$1"
# An empty id must not reach this. It did once, from a debugging shell where $qid was unset, and the
# result was eval/runs/walks-census/walk-.md — a complete, plausible-looking walk report belonging to
# no question at all. Nothing downstream would have caught it: it is not missing from the census, it
# is extra, and an extra report is invisible to a count of what is missing.
[ -n "$qid" ] || { echo "  empty question id — refusing to walk" >&2; exit 2; }
f="$OUT/walk-$qid$SUFFIX.md"
[ -s "$f" ] && exit 0
prompt=$(PYTHONPATH=$BENCH_PYLIB python3 ./bench/walkprompt.py "$qid" $OVERLAY --out "$f") || exit 1
claude -p "$prompt" --model sonnet \
  --allowed-tools "Bash(./bench/rmcli.py:*)" "Write" \
  --permission-mode acceptEdits --max-turns 40 >/dev/null 2>&1
# The reply is discarded on purpose. The file is the deliverable, and scoring whatever the agent
# happened to say instead is how four early walks got summarised into a hit that hid a real defect.
[ -s "$f" ] || echo "  no report: $qid" >&2
WALK
chmod +x "$OUT/.walk.sh"
export OUT SUFFIX OVERLAY BENCH_PYLIB

echo "$TODO" | grep . | xargs -P "$PAR" -n1 "$OUT/.walk.sh"

echo "  walked; recording"
for qid in $TODO; do
  f="$OUT/walk-$qid$SUFFIX.md"
  [ -s "$f" ] || { echo "  MISSING $qid"; continue; }
  PYTHONPATH=$BENCH_PYLIB python3 ./bench/walkscore.py --campaign "$CAMPAIGN" \
    record --id "$qid" --arm "$ARM" < "$f" | tail -1
done
