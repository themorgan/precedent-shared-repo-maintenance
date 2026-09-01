#!/bin/bash
# Two-direction test for check_session_trailer.py:
#   1. plant a commit with no Session: trailer -- require the check to fire;
#   2. the real, current, unplanted history -- require the check to stay clean.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROOT="$(pwd)"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

git clone -q "$ROOT" "$SCRATCH"
cd "$SCRATCH"
touch planted-violation.txt
git add planted-violation.txt
git -c user.name="Test" -c user.email="test@example.com" commit -q -m "planted violation: no session trailer at all"

if python3 tools/checks/check_session_trailer.py > /dev/null; then
  echo "FAIL: check_session_trailer.py did not fire on a commit with no Session: trailer" >&2
  exit 1
fi
echo "ok: fires on planted violation"

cd "$ROOT"
if ! python3 tools/checks/check_session_trailer.py > /dev/null; then
  echo "FAIL: check_session_trailer.py is not clean on the real, current history" >&2
  exit 1
fi
echo "ok: clean on real content"
