#!/bin/sh
# First boot: lay the empty ontology into the mounted directory and commit it.
#
# The commit is not ceremony. Publishing only happens when the data repository has a HEAD, and the map
# follows the *published* revision — so an uncommitted seed boots into a screen that never fills in.
# Seeding is skipped the moment the directory has anything in it: this must be safe to run on every
# start, because it does.
set -e
DATA="${ONTOLOGY_DATA:-/data/repo}"

# Docker creates a missing bind-mount source as root. This container is not root — on purpose, because
# it commits into a repository the user owns — so a data directory it made for us is one we cannot
# write, and the only symptom is a restart loop. Say which directory and whose it has to be.
if [ ! -w "$DATA" ]; then
  echo "FATAL: $DATA is not writable by uid $(id -u)." >&2
  echo "       Create it before starting, owned by the uid in KNOWLEDGE_UID:" >&2
  echo "         mkdir -p data/repo data/publish" >&2
  echo "       (Docker made it root-owned because it did not exist.)" >&2
  exit 1
fi
# Seed when the ontology is not there, not when the directory is empty: a tracked `.gitkeep` — which
# is how a clone comes with the directory already owned by the right user — makes an empty directory
# non-empty, and the emptiness test then skipped seeding and served nothing.
if [ ! -f "$DATA/vocab.yaml" ]; then
  echo "seeding empty ontology into $DATA"
  cp -r /app/seed/. "$DATA"/
fi
# A seed that copied nothing is the failure that looks like success: git initialises, commits
# nothing, and the API serves an ontology with no vocabulary — which reads to a person as "my data
# did not save".
if [ ! -f "$DATA/vocab.yaml" ]; then
  echo "FATAL: $DATA has no vocab.yaml after seeding — is /app/seed readable?" >&2
  exit 1
fi
if [ ! -d "$DATA/.git" ]; then
  git -C "$DATA" init -q
  git -C "$DATA" add -A
  git -C "$DATA" -c user.name=knowledge -c user.email=knowledge@local commit -q -m "empty ontology" || true
  echo "initialised git in $DATA at $(git -C "$DATA" rev-parse --short HEAD 2>/dev/null || echo none)"
fi
exec "$@"
