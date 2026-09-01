#!/bin/bash
# Two-direction test for check_default_branch.py:
#   1. a local bare "remote" whose HEAD points at a branch other than main
#      -- require the check to fire;
#   2. the real repo's actual origin -- require the check to stay clean.
# Uses a local bare repo instead of a real host for direction 1, so the
# test doesn't depend on being able to create or rename a real remote.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROOT="$(pwd)"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

BARE="$SCRATCH/bare-remote.git"
git init -q --bare -b trunk "$BARE"
WORK="$SCRATCH/work"
git clone -q "$BARE" "$WORK"
(
  cd "$WORK"
  git -c user.name="Test" -c user.email="test@example.com" commit -q --allow-empty -m "init"
  git push -q origin trunk
)

CHECKOUT="$SCRATCH/checkout"
git clone -q "$ROOT" "$CHECKOUT"
cd "$CHECKOUT"
git remote set-url origin "$BARE"

if python3 tools/checks/check_default_branch.py > /dev/null; then
  echo "FAIL: check_default_branch.py did not fire on a remote whose default is 'trunk'" >&2
  exit 1
fi
echo "ok: fires on planted violation"

cd "$ROOT"
status=0
python3 tools/checks/check_default_branch.py > /dev/null || status=$?
if [ "$status" -eq 2 ]; then
  echo "SKIPPED: could not reach the real origin from this environment -- not a check failure"
elif [ "$status" -ne 0 ]; then
  echo "FAIL: check_default_branch.py is not clean on the real repo's actual origin" >&2
  exit 1
else
  echo "ok: clean on real content"
fi
