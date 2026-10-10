#!/bin/sh
# Start the map over — empty, or from the example back office — without losing the one you have.
#
#   ./ontology/reset.sh --empty            an empty map: no areas, the starting vocabulary
#   ./ontology/reset.sh --example          the example back office (five areas, 79 documents)
#   ./ontology/reset.sh --example --yes    without asking (no terminal, or a script)
#   ./ontology/reset.sh --repo PATH ...    another data repository than ./data/repo
#
# One commit, in the data repository's own history. The map as it was is tagged first
# (`before-reset-<time>`), so going back is `git -C data/repo reset --hard <that tag>` — nothing is
# deleted that git cannot give back. The running service picks the new commit up by itself.
#
# Before this, starting over meant deleting 74 documents and 5 areas one at a time, or emptying the
# directory by hand — which left an uncommitted seed and a read-only map — or copying the example over
# the top, which merged into what was there instead of replacing it (QA, 2026-10-10).
set -e
cd "$(dirname "$0")/.."
REPO=data/repo; FROM=""; YES=""
while [ $# -gt 0 ]; do
  case "$1" in
    --empty)   FROM=seed ;;
    --example) FROM=examples/back-office ;;
    --yes|-y)  YES=1 ;;
    --repo)    REPO="${2:-}"; shift ;;
    -h|--help) sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) printf 'unknown option: %s (try --help)\n' "$1" >&2; exit 2 ;;
  esac
  shift
done
[ -n "$FROM" ] || { printf 'say what to start from: --empty or --example (try --help)\n' >&2; exit 2; }
[ -d "$REPO/.git" ] || { printf '%s is not a data repository (no .git) — has the service run once?\n' "$REPO" >&2; exit 2; }
if [ -n "$(git -C "$REPO" status --porcelain)" ]; then
  printf '%s has changes that are not committed — commit or discard them first:\n' "$REPO" >&2
  git -C "$REPO" status --short | head -10 >&2
  exit 1
fi
N="$(find "$REPO/regions" -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
if [ -z "$YES" ]; then
  [ -t 0 ] || { printf 'no terminal to ask on — pass --yes\n' >&2; exit 2; }
  printf 'Replace the map in %s (%s documents) with %s? It is tagged first and can be brought back. [y/N] ' "$REPO" "$N" "$FROM"
  read -r ans || ans=""
  case "$ans" in [yY]*) ;; *) printf 'nothing changed\n'; exit 0 ;; esac
fi
TAG="before-reset-$(date +%Y%m%d-%H%M%S)"
# Two resets in one second would name the same tag, and the second stopped on it.
n=2; base="$TAG"
while git -C "$REPO" rev-parse -q --verify "refs/tags/$TAG" >/dev/null; do TAG="$base-$n"; n=$((n+1)); done
G="git -C $REPO -c user.name=reset -c user.email=reset@routemind.local"
$G tag "$TAG"
# Everything the map is made of goes; git's own files, and anything git ignores, stay.
$G rm -rq --ignore-unmatch regions regions.json vocab.yaml REVISION >/dev/null
rm -rf "$REPO/regions"
cp -R "$FROM/." "$REPO/"
$G add -A
$G commit -qm "reset: start over from $FROM

The map as it was is tagged $TAG — git reset --hard $TAG brings it back."
printf 'The map now starts from %s (commit %s).\n' "$FROM" "$(git -C "$REPO" rev-parse --short HEAD)"
printf 'The one before is tagged %s. To bring it back:\n  git -C %s reset --hard %s\n' "$TAG" "$REPO" "$TAG"
