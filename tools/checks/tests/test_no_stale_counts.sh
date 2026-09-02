#!/bin/bash
# Two-direction test for check_no_stale_counts.py:
#   1. plant a wrong "<N> practices" count in a tracked markdown file --
#      require the check to fire;
#   2. the real, current, unplanted repo -- require the check to stay clean.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROOT="$(pwd)"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

git clone -q "$ROOT" "$SCRATCH"
cd "$SCRATCH"
echo "" >> README.md
echo "This set has 999 practices, definitely not the real count." >> README.md
git add README.md
git -c user.name="Test" -c user.email="test@example.com" commit -q -m "planted violation: wrong practice count"

if python3 tools/checks/check_no_stale_counts.py > /dev/null; then
  echo "FAIL: check_no_stale_counts.py did not fire on a planted wrong count" >&2
  exit 1
fi
echo "ok: fires on planted violation"

cd "$ROOT"
if ! python3 tools/checks/check_no_stale_counts.py > /dev/null; then
  echo "FAIL: check_no_stale_counts.py is not clean on the real, current repo (including its own 40-practices line)" >&2
  exit 1
fi
echo "ok: clean on real content"
